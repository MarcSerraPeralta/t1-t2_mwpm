import pathlib
from typing import Tuple

import numpy as np
import stim
from pymatching import Matching

MEASUREMENTS = ["M", "MPP", "MR", "MRX", "MRY", "MRZ", "MX", "MY", "MZ"]
ANNOTATIONS = ["QUBIT_COORDS", "DETECTOR", "OBSERVABLE_INCLUDE", "TICK", "SHIFT_COORDS"]


def add_t1t2_noise(
    circuit: stim.Circuit, t1: dict, t2: dict, op_duration: dict
) -> stim.Circuit:
    """
    Returns circuit with amplitude and phase damping noise
    using the Pauli Twirl Approximation (PTA).

    Paramaters
    ----------
    circuit
        Stim circuit containing the QEC experiment without noise.
        It must have TICKs separating blocks of operations
        that are executed in parallel.
        Note: this function assumes that all qubits are measured
        at some point in the circuit.
    t1
        Dictionary with the T1 times of every qubit in the circuit
        following the same labelling as in the stim circuit.
        Note: use same units for t1, t2 and op_duration.
    t2
        Dictionary with the T2 times of every qubit in the circuit
        following the same labelling as in the stim circuit.
        Note: use same units for t1, t2 and op_duration.
    op_duration
        Dictionary with the operation times of every operation in the circuit
        following the same labelling as in the stim circuit.
        Note: use same units for t1, t2 and op_duration.

    Returns
    -------
    noisy_circuit
        Stim circuit corresponding to 'circuit' with the amplitude and phase
        damping noise under the PTA.
        Note: returns the circuit flattened.
    """
    # checks
    for q in t1:
        if t2[q] > 2 * t1[q]:
            raise ValueError(f"T2 > 2 * T1 for qubit {q}")

    if circuit.flattened() != circuit.without_noise().flattened():
        raise ValueError("The circuit provided contains noise")
    if circuit.num_ticks == 0:
        raise ValueError("The circuit must contain at least one TICK")

    qubits = [i.targets_copy() for i in circuit.flattened() if i.name in MEASUREMENTS]
    qubits = [x for xs in qubits for x in xs]  # flatten list
    qubits = set([q.qubit_value for q in qubits])
    if set(t1) < qubits:
        raise ValueError(
            "T1 must contain all the qubits in the circuit,"
            f"missing the following qubits: {set(qubits) - set(t1)}"
        )
    if set(t2) < qubits:
        raise ValueError(
            "T2 must contain all the qubits in the circuit,"
            f"missing the following qubits: {set(qubits) - set(t2)}"
        )

    # prepare inputs
    duration = {i: 0 for i in ANNOTATIONS}
    duration.update(op_duration)
    # adds TICK at the end of the circuit to include last block
    # note: make a copy of the circuit (using flattened)
    circuit_flattened = circuit.flattened()
    circuit_flattened.append(stim.CircuitInstruction("TICK", [], []))

    # add noise
    noisy_circuit = stim.Circuit()
    block = []
    length = len(circuit_flattened)

    for k, instr in enumerate(circuit_flattened):
        if instr.name not in duration:
            raise ValueError(f"{instr.name} not in 'op_duration'")

        if instr.name != "TICK":
            block.append(instr)
            continue

        # add noise in block
        t = max([duration[i.name] for i in block], default=0)

        for q in qubits:
            px, py, pz = get_perror_from_t1t2(t=t, t1=t1[q], t2=t2[q])
            block.append(
                stim.CircuitInstruction(
                    name="PAULI_CHANNEL_1", targets=[q], gate_args=[px, py, pz]
                )
            )

        # append block to noisy circuit
        for instr in block:
            noisy_circuit.append(instr)
        if k != length - 1:
            # does not add last TICK that was artificially added
            noisy_circuit.append(stim.CircuitInstruction("TICK", [], []))

        block = []

    return noisy_circuit


def get_perror_from_t1t2(t: float, t1: float, t2: float) -> Tuple[float, float, float]:
    """
    Returns the single-qubit Pauli error probabilities for the
    given duration t and T1 and T2 times, from an amplitude and
    phase damping noise with the Pauli Twirl Approximation.

    References:
    arXiv:1210.5799v2
    arXiv:1305.2021v1

    Paramters
    ---------
    t:
        Duration of the noise
    t1:
        T1 time
    t2:
        T2 time

    Returns
    -------
    px:
        X error probability
    py:
        Y error probability
    pz:
        Z error probability
    """
    if t == 0:
        return 0, 0, 0

    px = 0.25 * (1 - np.exp(-t / t1))
    py = px
    pz = 0.5 * (1 - np.exp(-t / t2)) - 0.25 * (1 - np.exp(-t / t1))
    return px, py, pz


def get_mwpm(
    circuit: stim.Circuit,
    t1: dict,
    t2: dict,
    op_duration: dict,
    approximate_disjoint_errors: bool = False,
) -> Matching:
    """
    Returns a MWPM initialized with amplitude and phase damping noise
    using the Pauli Twirl Approximation (PTA).

    Paramaters
    ----------
    circuit
        Stim circuit containing the QEC experiment without noise.
        It must have TICKs separating blocks of operations
        that are executed in parallel.
        Note: this function assumes that all qubits are measured
        at some point in the circuit.
    t1
        Dictionary with the T1 times of every qubit in the circuit
        following the same labelling as in the stim circuit.
        Note: use same units for t1, t2 and op_duration.
    t2
        Dictionary with the T2 times of every qubit in the circuit
        following the same labelling as in the stim circuit.
        Note: use same units for t1, t2 and op_duration.
    op_duration
        Dictionary with the operation times of every operation in the circuit
        following the same labelling as in the stim circuit.
        Note: use same units for t1, t2 and op_duration.
    approximate_disjoint_errors
        Flag for stim.Circuit.detector_error_model().
        See stim's documentation.

    Returns
    -------
    mwpm
        pymatching.Matching initialized with amplitude and phase damping noise
        using the Pauli Twirl Approximation (PTA) for the given circuit.
    """

    noisy_circuit = add_t1t2_noise(
        circuit=circuit, t1=t1, t2=t2, op_duration=op_duration
    )
    dem = noisy_circuit.detector_error_model(
        decompose_errors=True,
        allow_gauge_detectors=True,
        approximate_disjoint_errors=approximate_disjoint_errors,
    )
    mwpm = Matching(dem)

    return mwpm
