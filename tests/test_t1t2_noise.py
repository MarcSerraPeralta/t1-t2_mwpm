import pytest

import stim
from pymatching import Matching

from t1t2_mwpm import get_mwpm, add_t1t2_noise


def test_get_mwpm():
    circuit = stim.Circuit.generated(
        code_task="repetition_code:memory", distance=5, rounds=6
    )
    decoder = get_mwpm(
        circuit,
        t1={i: 20 for i in range(9)},
        t2={i: 10 for i in range(9)},
        op_duration={"MR": 50, "M": 50, "CX": 10, "R": 100},
        symmetrize_noise=True,
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
        symmetrize_noise=True,
    )
    assert isinstance(noisy_circuit, stim.Circuit)

    return


def test_add_t1t2_noise_T1_T2_relation():
    circuit = stim.Circuit.generated(
        code_task="repetition_code:memory", distance=5, rounds=6
    )

    with pytest.raises(ValueError) as e_info:
        noisy_circuit = add_t1t2_noise(
            circuit,
            t1={i: 2 for i in range(9)},
            t2={i: 10 for i in range(9)},
            op_duration={"MR": 50, "M": 50, "CX": 10, "R": 100},
        )

    return


def test_add_t1t2_noise_qubit_labels():
    circuit = stim.Circuit.generated(
        code_task="repetition_code:memory", distance=5, rounds=6
    )

    with pytest.raises(ValueError) as e_info:
        noisy_circuit = add_t1t2_noise(
            circuit,
            t1={f"D{i}": 10 for i in range(9)},
            t2={f"D{i}": 10 for i in range(9)},
            op_duration={"MR": 50, "M": 50, "CX": 10, "R": 100},
        )

    return


def test_add_t1t2_noise_operations():
    circuit = stim.Circuit.generated(
        code_task="repetition_code:memory", distance=5, rounds=6
    )

    with pytest.raises(ValueError) as e_info:
        noisy_circuit = add_t1t2_noise(
            circuit,
            t1={i: 10 for i in range(9)},
            t2={i: 10 for i in range(9)},
            op_duration={"Meas": 50, "CZ": 10, "Reset": 100},
        )

    return


def test_add_t1t2_noise():
    circuit = stim.Circuit("""X_ERROR(0.01) 0 1 2""")

    with pytest.raises(ValueError) as e_info:
        noisy_circuit = add_t1t2_noise(
            circuit,
            t1={i: 20 for i in range(9)},
            t2={i: 10 for i in range(9)},
            op_duration={"MR": 50, "M": 50, "CX": 10, "R": 100},
        )

    return
