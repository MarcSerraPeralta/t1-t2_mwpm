from typing import Tuple
from warnings import warn
from math import exp, inf

def idle_error_probs(
    relax_time: float, deph_time: float, duration: float
) -> Tuple[float, float, float]:
    """
    idle_error_probs Returns the probabilities of X, Y, and Z errors
    for a Pauli-twirled amplitude and phase damping channel.

    References:
    arXiv:1210.5799
    arXiv:1305.2021

    Parameters
    ----------
    relax_time : float
        The relaxation time (T1) of the qubit.
    deph_time : float
        The dephasing time (T2) of the qubit.
    duration : float
        The duration of the amplitude-phase damping period.

    Returns
    -------
    Tuple[float, float, float]
        The probabilities of X, Y, and Z errors
    """
    # Check for invalid inputs
    # If either the duration, relaxation time, or dephasing time is negative, you get negative probabilities
    # If the relaxation time or dephasing time is zero, you get a divide by zero error.
    # If the duration is zero, you don't get any errors, but it is likely a bug in the code for the user to have a zero duration.
    if relax_time <= 0:
        raise ValueError("The relaxation time ('relax_time') must be positive")
    if deph_time <= 0:
        raise ValueError("The dephasing time ('deph_time') must be positive")
    if duration <= 0: 
        raise ValueError("The idling duration ('duration') must be positive")

    relax_prob = 1 - exp(-duration / relax_time)
    deph_prob = 1 - exp(-duration / deph_time)

    x_prob = y_prob = 0.25 * relax_prob
    z_prob = 0.5 * deph_prob - 0.25 * relax_prob

    return x_prob, y_prob, z_prob
