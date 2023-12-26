from t1t2_mwpm import get_mwpm, add_t1t2_noise
import stim
from pymatching import Matching


def test_get_mwpm():
    circuit = stim.Circuit.generated(
        code_task="repetition_code:memory", distance=5, rounds=6
    )
    decoder = get_mwpm(
        circuit,
        t1={i: 20 for i in range(9)},
        t2={i: 10 for i in range(9)},
        op_duration={"MR": 50, "M": 50, "CX": 10, "R": 100},
    )
    assert isinstance(decoder, Matching)

    return


def test_add_t1t2_noise():
    circuit = stim.Circuit.generated(
        code_task="repetition_code:memory", distance=5, rounds=6
    )
    noisy_circuit = add_t1t2_noise(
        circuit,
        t1={i: 20 for i in range(9)},
        t2={i: 10 for i in range(9)},
        op_duration={"MR": 50, "M": 50, "CX": 10, "R": 100},
    )
    assert isinstance(noisy_circuit, stim.Circuit)

    return
