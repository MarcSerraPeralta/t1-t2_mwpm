from stim import Circuit

from ..models import Model
from .. import gates

def add_noise(
    circuit: Circuit,
    model: Model,
) -> Circuit:
    """
    add_noise _summary_

    Parameters
    ----------
    circuit : Circuit
        The circuit to add noise to.
    model : Model
        The error model to use.

    Returns
    -------
    Circuit
        The circuit with noise added.
    """
    num_qubits = circuit.num_qubits
    if num_qubits != model.setup.num_qubits:
        raise ValueError("Number of qubits in circuit and the setup do not match.")


    qubit_inds = set(range(num_qubits))
    noisy_circuit = Circuit()

    for inst in circuit.flattened():
        name = inst.name

        if name in gates.ANNOTATIONS:
            noisy_circuit.append(inst)
            continue

        targets = inst.targets_copy()
        inds = [target.value for target in targets]
        duration = model.setup.gate_durations[name]

        for inst in model.generic_gate(name, inds):
            noisy_circuit.append(inst)

        idle_inds = qubit_inds - set(inds)
        for inst in model.idle(idle_inds, duration):
            noisy_circuit.append(inst)
    

    return noisy_circuit