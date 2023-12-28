"""Module containing functions for generating circuits for a repetition code memory experiment."""
from itertools import chain, compress
from typing import List, Optional

from stim import Circuit, target_rec

from ..models import Model


def log_meas(
    model: Model,
    data_inds: List[int], 
    anc_inds: List[int], 
    comp_rounds: Optional[int] = None,
) -> Circuit:
    """
    log_meas _summary_

    Parameters
    ----------
    model : Model
        An error model.
    data_inds : List[int]
        The indices of the data qubits.
    anc_inds : List[int]
        The indices of the ancilla qubits.
    comp_rounds : Optional[int], optional
        The number of rounds with which to compare, by default None

    Returns
    -------
    Circuit
        The circuit for a logical measurement
    """
    circuit = Circuit()

    for instruction in model.measure(data_inds):
        circuit.append(instruction)

    duration = model.setup.gate_durations["M"]
    for instruction in model.idle(anc_inds, duration):
        circuit.append(instruction)

    num_data = len(data_inds)
    num_anc = len(anc_inds)

    for anc_ind in anc_inds:
        nbr_inds = (anc_ind + 1, anc_ind - 1)
        meas_inds = (data_inds.index(nbr_ind) for nbr_ind in nbr_inds)
        targets = [target_rec(ind - num_data) for ind in meas_inds]

        if comp_rounds is not None:
            meas_ind = anc_inds.index(anc_ind)
            for round_ind in range(1, comp_rounds + 1):
                target = target_rec(meas_ind - num_data - round_ind * num_anc)
                targets.append(target)
        circuit.append("DETECTOR", targets)

    targets = [target_rec(ind) for ind in range(-num_data, 0)]
    circuit.append("OBSERVABLE_INCLUDE", targets, 0)

    circuit.append("TICK")

    return circuit


def qec_round(
    model: Model,
    data_inds: List[int], 
    anc_inds: List[int], 
    comp_rounds: Optional[int] = None,
) -> Circuit:
    """
    qec_round generates a circuit for a single round of error correction for the repetition code

    Parameters
    ----------
    model : Model
        The error model used for modelling operations
    meas_comparison : bool, optional
        Whether to compare with previous measurements when declaring the detectors, by default True

    Returns
    -------
    Circuit
        The circuit for a single round of error correction

    Raises
    ------
    NotImplementedError
        If the stabilizer type is not z_type
    NotImplementedError
        If the stabilizer type of the ancilla qubits is not the same
    """
    qubit_inds = set(data_inds + anc_inds)

    sq_duration = model.setup.gate_durations["H"]
    cz_duration = model.setup.gate_durations["CZ"]
    meas_duration = model.setup.gate_durations["CZ"]
    reset_duration = model.setup.gate_durations["R"]

    circuit = Circuit()

    rot_inds = anc_inds
    for inst in model.hadamard(rot_inds):
        circuit.append(inst)

    idle_inds = qubit_inds - set(rot_inds)
    for inst in model.idle(idle_inds, sq_duration):
        circuit.append(inst)
    
    circuit.append("TICK")

    pair_generator = ((anc_ind - 1, anc_ind) for anc_ind in anc_inds)
    int_pairs = list(chain.from_iterable(pair_generator))
    for inst in model.cphase(int_pairs):
        circuit.append(inst)

    idle_inds = qubit_inds - set(int_pairs)
    for inst in model.idle(idle_inds, cz_duration):
        circuit.append(inst)

    circuit.append("TICK")

    pair_generator = ((anc_ind, anc_ind + 1) for anc_ind in anc_inds)
    int_pairs = list(chain.from_iterable(pair_generator))
    for inst in model.cphase(int_pairs):
        circuit.append(inst)

    idle_inds = qubit_inds - set(int_pairs)
    for inst in model.idle(idle_inds, cz_duration):
        circuit.append(inst)

    circuit.append("TICK")

    rot_inds = anc_inds
    for inst in model.hadamard(rot_inds):
        circuit.append(inst)

    idle_inds = qubit_inds - set(rot_inds)
    for inst in model.idle(idle_inds, sq_duration):
        circuit.append(inst)

    circuit.append("TICK")

    for inst in model.measure(anc_inds):
        circuit.append(inst)

    for inst in model.idle(data_inds, meas_duration):
        circuit.append(inst)

    # detectors ordered as in the measurements
    num_anc = len(anc_inds)

    if comp_rounds:
        round_offsets = (1, comp_rounds + 1)
        for ind in range(num_anc):
            targets = [target_rec(ind - num_anc * offset) for offset in round_offsets]
            circuit.append("DETECTOR", targets)
    else:
        for anc_ind in range(num_anc):
            target = target_rec(anc_ind - num_anc)
            circuit.append("DETECTOR", target)

    circuit.append("TICK")

    for inst in model.reset(anc_inds):
        circuit.append(inst)

    for inst in model.idle(data_inds, reset_duration):
        circuit.append(inst)

    circuit.append("TICK")

    return circuit


def init_qubits(model: Model, data_inds: List[int], anc_inds: List[int], data_init: List[int]) -> Circuit:
    """
    init_qubits Initializes the data qubits in the given bitstring state, and the ancilla qubits in the ground state

    Parameters
    ----------
    model : Model
        An error model.
    data_init : List[int]
        A an array indicating which data_qubits to initialize in the excited state.

    Returns
    -------
    Circuit
        The circuit for initializing the qubits.
    """
    qubit_inds = list(data_inds + anc_inds)
    ind_set = set(qubit_inds)  

    circuit = Circuit()
    for instruction in model.reset(qubit_inds):
        circuit.append(instruction)
    circuit.append("TICK")

    exc_inds = list(compress(qubit_inds, data_init))
    if exc_inds:
        for instruction in model.x_gate(exc_inds):
            circuit.append(instruction)

        idle_inds = list(ind_set.difference(exc_inds))
        duration = model.setup.gate_durations["X"]
        for instruction in model.idle(idle_inds, duration):
            circuit.append(instruction)
        circuit.append("TICK")

    return circuit
