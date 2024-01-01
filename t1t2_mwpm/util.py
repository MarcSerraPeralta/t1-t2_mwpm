from stim import Circuit

from .models import Model
from . import gates


def add_noise_to_stim(
    circuit: Circuit,
    model: Model,
) -> Circuit:
    """
    add_noise_to_stim Adds noise to an ideal Stim circuit.

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

    active_inds = set()
    layer_duration = None

    for instruction in circuit.flattened():
        name = instruction.name
    
        if name in gates.ANNOTATIONS:
            if name == "TICK" and layer_duration is not None:
                idle_inds = qubit_inds - set(active_inds)
                for inst in model.idle(idle_inds, layer_duration):
                    noisy_circuit.append(inst)

                active_inds.clear()
                layer_duration = None

            noisy_circuit.append(instruction)
            continue

        targets = instruction.targets_copy()
        inds = [target.value for target in targets]

        if layer_duration is None:
            layer_duration = model.setup.gate_durations[name]
        else:
            if layer_duration != model.setup.gate_durations[name]:
                raise ValueError(
                    "Each layer must should be composed of gates that are of the same duration."
                )

        if active_inds.intersection(inds):
            raise ValueError(
                "Multiple gates acting on the same qubits in a given layer."
                "Each layer must should be composed of gates that are of the same duration and that are executed in parallel."
            )

        for inst in model.generic_op(name, inds):
            noisy_circuit.append(inst)

        active_inds.update(inds)

    return noisy_circuit
