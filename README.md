# T1T2_mwpm
Adds amplitude and phase damping noise to a `stim` circuit given the T1 and T2 times and the operation durations. This is also used to initialize a `pymatching.Matching` MWPM decoder. 

# Example

The inputs of the functions in this repository are: (1) QEC circuit, (2) T1 times, (3) T2 times, (4) gate durations. 

**QEC circuit**
```
# memory experiment of the d=3 repetition code containing 2 QEC rounds. 
# the QEC circuit must include 'TICK' separating the blocks that are executed simultaneously. 

circuit = stim.Circuit('''
    R 0 1 2 3 4
    TICK
    CX 0 1 2 3
    TICK
    CX 2 1 4 3
    TICK
    MR 1 3
    DETECTOR(1, 0) rec[-2]
    DETECTOR(3, 0) rec[-1]
    TICK
    CX 0 1 2 3
    TICK
    CX 2 1 4 3
    TICK
    MR 1 3
    SHIFT_COORDS(0, 1)
    DETECTOR(1, 0) rec[-2] rec[-4]
    DETECTOR(3, 0) rec[-1] rec[-3]
    M 0 2 4
    DETECTOR(1, 1) rec[-2] rec[-3] rec[-5]
    DETECTOR(3, 1) rec[-1] rec[-2] rec[-4]
    OBSERVABLE_INCLUDE(0) rec[-1]
''')
```

**T1 and T2 times**
```
# the keys of the dictionary must match the qubit labels of the circuit
# the units of T1, T2 and operation durations must be the same, in this case microseconds. 

t1 = {0: 55.4, 1: 50.1, 2: 56.9, 3: 51.4, 4: 52.0}
t2 = {0: 22.3, 1: 20.6, 2: 26.1, 3: 23.9, 4: 21.7}
```

**Operation durations**
```
# all the operations in the circuit should be included here

op_duration = {"MR": 153, "M": 51, "CX": 40, "R": 102}
```

The MWPM decoder (`pymatching.Matching`) can be obtained by
```
from t1t2_mwpm import get_mwpm

mwpm_decoder = get_mwpm(circuit, t1=t1, t2=t2, op_duration=op_duration)
```