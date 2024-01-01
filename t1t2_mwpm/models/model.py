from abc import ABCMeta, abstractmethod
from typing import Iterator, Sequence

from ..setup import Setup

from stim import CircuitInstruction

class Model(metaclass = ABCMeta):
    def __init__(self, setup: Setup) -> None:
        self._setup = setup

    @property
    def setup(self) -> Setup:
        return self._setup
    
    @abstractmethod
    def x_gate(self, qubits: Sequence[str]) -> Iterator[CircuitInstruction]:
        pass

    @abstractmethod
    def y_gate(self, qubits: Sequence[str]) -> Iterator[CircuitInstruction]:
        pass

    @abstractmethod
    def z_gate(self, qubits: Sequence[str]) -> Iterator[CircuitInstruction]:
        pass

    @abstractmethod
    def s_gate(self, qubits: Sequence[str]) -> Iterator[CircuitInstruction]:
        pass

    @abstractmethod
    def hadamard(self, qubits: Sequence[str]) -> Iterator[CircuitInstruction]:
        pass

    @abstractmethod
    def cnot(self, qubits: Sequence[str]) -> Iterator[CircuitInstruction]:
        pass

    @abstractmethod
    def cphase(self, qubits: Sequence[str]) -> Iterator[CircuitInstruction]:
        pass

    @abstractmethod
    def swap(self, qubits: Sequence[str]) -> Iterator[CircuitInstruction]:
        pass

    @abstractmethod
    def iswap(self, qubits: Sequence[str]) -> Iterator[CircuitInstruction]:
        pass

    @abstractmethod
    def measure(self, qubits: Sequence[str]) -> Iterator[CircuitInstruction]:
        pass

    @abstractmethod
    def idle(self, qubits: Sequence[str]) -> Iterator[CircuitInstruction]:
        pass