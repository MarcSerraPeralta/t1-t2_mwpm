from stim import Circuit
from pymatching import Matching


def get_matching(
    circuit: Circuit,
    decompose_errors: bool = True,
    allow_gauge_detectors: bool = True,
    approximate_disjoint_errors: bool = False,
) -> Matching:

    error_model = circuit.detector_error_model(
        decompose_errors=decompose_errors,
        allow_gauge_detectors=allow_gauge_detectors,
        approximate_disjoint_errors=approximate_disjoint_errors
    )
    matching = Matching(error_model)
    return matching