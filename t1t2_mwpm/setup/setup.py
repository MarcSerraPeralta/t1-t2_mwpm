from typing import Dict, List

class Setup:
    def __init__(
        self,
        relax_times: List[float],
        deph_times: List[float],
        gate_durations: Dict[str, float],
    ) -> None:
        check_coherence_times(relax_times, deph_times)
        check_gate_durations(gate_durations)

        self.relax_times = relax_times
        self.deph_times = deph_times
        self.gate_durations = gate_durations

        self.num_qubits = len(relax_times)
        self.qubits = list(range(self.num_qubits))


def check_coherence_times(relax_times: List[float], deph_times: List[float]) -> None:
    num_relax_times = len(relax_times) 
    num_deph_times = len(deph_times)

    if num_relax_times != num_deph_times:
        raise ValueError(
            f"The number of elements in 'relax_times' and 'deph_times' must be the same. Instead, got {num_relax_times} and {num_deph_times} elements, respectively."
        )
    
    for relax_time, deph_time in zip(relax_times, deph_times):
        if relax_time <= 0:
            raise ValueError(
                f"The relaxation time (T1) must be positive. Instead, got {relax_time}."
            )
        if deph_time <= 0:
            raise ValueError(
                f"The dephasing time (T2) must be positive. Instead, got {deph_time}."
            )
        
        if deph_time > 2*relax_time:
            raise ValueError(
                f"The dephasing time (T2) must be less than or equal to twice the relaxation time (T1). Instead, got T2={deph_time} and T1={relax_time}."
            )
        
def check_gate_durations(gate_durations: Dict[str, float]) -> None:
    for gate, duration in gate_durations.items():
        if duration <= 0:
            raise ValueError(
                f"The operation duration for {gate} must be positive. Instead, got {duration}."
            )