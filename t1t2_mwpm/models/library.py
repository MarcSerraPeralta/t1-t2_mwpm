from typing import Iterator, Sequence

from stim import CircuitInstruction

from .model import Model
from .util import idle_error_probs

class DecoherenceModel(Model):
    """An coherence-limited noise model""" 

    def generic_op(self, name: str, qubits: Sequence[str]) -> Iterator[CircuitInstruction]:
        """
        generic_op Returns the circuit instructions for a generic operation (that is supported by Stim) on the given qubits.

        Parameters
        ----------
        name : str
            The name of the gate (as defined in Stim)
        qubits : Sequence[str]
            The qubits to apply the gate to.

        Yields
        ------
        Iterator[CircuitInstruction]
            The circuit instructions for a generic gate on the given qubits.
        """
        duration = self._setup.gate_durations[name]

        yield CircuitInstruction(name, qubits)
        yield from self.idle(qubits, duration)

    def x_gate(self, qubits: Sequence[str]) -> Iterator[CircuitInstruction]:
        """
        x_gate Returns the circuit instructions for an X gate on the given qubits.

        Parameters
        ----------
        qubits : Sequence[str]
            The qubits to apply the X gate to.

        Yields
        ------
        Iterator[CircuitInstruction]
            The circuit instructions for an X gate on the given qubits.
        """
        yield from self.generic_op("X", qubits)

    def y_gate(self, qubits: Sequence[str]) -> Iterator[CircuitInstruction]:
        """
        y_gate Returns the circuit instructions for an Y gate on the given qubits.

        Parameters
        ----------
        qubits : Sequence[str]
            The qubits to apply the Y gate to.

        Yields
        ------
        Iterator[CircuitInstruction]
            The circuit instructions for an Y gate on the given qubits.
        """
        yield from self.generic_op("Y", qubits)

    def z_gate(self, qubits: Sequence[str]) -> Iterator[CircuitInstruction]:
        """
        z_gate Returns the circuit instructions for an Z gate on the given qubits.

        Parameters
        ----------
        qubits : Sequence[str]
            The qubits to apply the Z gate to.

        Yields
        ------
        Iterator[CircuitInstruction]
            The circuit instructions for an Z gate on the given qubits.
        """
        yield from self.generic_op("Z", qubits)

    def s_gate(self, qubits: Sequence[str]) -> Iterator[CircuitInstruction]:
        """
        s_gate Returns the circuit instructions for an S gate on the given qubits.

        Parameters
        ----------
        qubits : Sequence[str]
            The qubits to apply the S gate to.

        Yields
        ------
        Iterator[CircuitInstruction]
            The circuit instructions for an S gate on the given qubits.
        """
        yield from self.generic_op("S", qubits)

    def hadamard(self, qubits: Sequence[str]) -> Iterator[CircuitInstruction]:
        """
        hadamard Returns the circuit instructions for a Hadamard gate on the given qubits.

        Parameters
        ----------
        qubits : Sequence[str]
            The qubits to apply the Hadamard gate to.

        Yields
        ------
        Iterator[CircuitInstruction]
            The circuit instructions for a Hadamard gate on the given qubits.
        """
        yield from self.generic_op("H", qubits)

    def cnot(self, qubits: Sequence[str]) -> Iterator[CircuitInstruction]:
        """
        cnot Returns the circuit instructions for a CNOT gate on the given qubits.

        Parameters
        ----------
        qubits : Sequence[str]
            The list of pairs of qubits to apply the CNOT gate to.
            The first qubit in each pair is the control qubit, while the second is the target qubit.

        Yields
        ------
        Iterator[CircuitInstruction]
            The circuit instructions for a CNOT gate on the given qubits.

        Raises
        ------
        ValueError
            If the number of qubits is not even.
        """
        yield from self.generic_op("CNOT", qubits)

    def cphase(self, qubits: Sequence[str]) -> Iterator[CircuitInstruction]:
        """
        cphase Returns the circuit instructions for a CPHASE gate on the given qubits.

        Parameters
        ----------
        qubits : Sequence[str]
            The list of pairs of qubits to apply the CPHASE gate to.
            The first qubit in each pair is the control qubit, while the second is the target qubit.

        Yields
        ------
        Iterator[CircuitInstruction]
            The circuit instructions for a CPHASE gate on the given qubits.

        Raises
        ------
        ValueError
            If the number of qubits is not even.
        """
        yield from self.generic_op("CZ", qubits)


    def swap(self, qubits: Sequence[str]) -> Iterator[CircuitInstruction]:
        """
        swap Returns the circuit instructions for a SWAP gate on the given qubits.

        Parameters
        ----------
        qubits : Sequence[str]
            The list of pairs of qubits to apply the SWAP gate to.

        Yields
        ------
        Iterator[CircuitInstruction]
            The circuit instructions for a SWAP gate on the given qubits.

        Raises
        ------
        ValueError
            If the number of qubits is not even.
        """
        yield from self.generic_op("SWAP", qubits)


    def iswap(self, qubits: Sequence[str]) -> Iterator[CircuitInstruction]:
        """
        iswap Returns the circuit instructions for a ISWAP gate on the given qubits.

        Parameters
        ----------
        qubits : Sequence[str]
            The list of pairs of qubits to apply the ISWAP gate to.

        Yields
        ------
        Iterator[CircuitInstruction]
            The circuit instructions for a ISWAP gate on the given qubits.

        Raises
        ------
        ValueError
            If the number of qubits is not even.
        """
        yield from self.generic_op("ISWAP", qubits)

    def cphase(self, qubits: Sequence[str]) -> Iterator[CircuitInstruction]:
        """
        cphase Returns the circuit instructions for a CPHASE gate on the given qubits.

        Parameters
        ----------
        qubits : Sequence[str]
            The list of pairs of qubits to apply the CPHASE gate to.
            The first qubit in each pair is the control qubit, while the second is the target qubit.

        Yields
        ------
        Iterator[CircuitInstruction]
            The circuit instructions for a CPHASE gate on the given qubits.

        Raises
        ------
        ValueError
            If the number of qubits is not even.
        """
        yield from self.generic_op("CZ", qubits)

    def measure(self, qubits: Sequence[str]) -> Iterator[CircuitInstruction]:
        """
        measure Returns the circuit instructions for a measurement on the given qubits.

        Parameters
        ----------
        qubits : Sequence[str]
            The qubits to measure.

        Yields
        ------
        Iterator[CircuitInstruction]
            The circuit instructions for a measurement on the given qubits.
        """
        yield from self.generic_op("M", qubits)

    def reset(self, qubits: Sequence[str]) -> Iterator[CircuitInstruction]:
        """
        reset Returns the circuit instructions for a reset on the given qubits.

        Parameters
        ----------
        qubits : Sequence[str]
            The qubits to reset.

        Yields
        ------
        Iterator[CircuitInstruction]
            The circuit instructions for a reset on the given qubits.
        """
        yield from self.generic_op("R", qubits)

    def idle(
        self, qubits: Sequence[int], duration: float
    ) -> Iterator[CircuitInstruction]:
        """
        idle Returns the circuit instructions for an idling period on the given qubits.

        Parameters
        ----------
        qubits : Sequence[str]
            The qubits to idle.
        duration : float
            The duration of the idling period.

        Yields
        ------
        Iterator[CircuitInstruction]
            The circuit instructions for an idling period on the given qubits.
        """
        for qubit in qubits:
            relax_time = self._setup.relax_times[qubit]
            deph_time = self._setup.deph_times[qubit]
    
            error_probs = list(idle_error_probs(relax_time, deph_time, duration))
            
            yield CircuitInstruction("PAULI_CHANNEL_1", [qubit], error_probs)


def check_valid_name(gate_name : str) -> None:
    pass