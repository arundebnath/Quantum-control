import numpy as np
from qutip import sigmam, sigmax, sigmaz

from openqctrl import lindblad_generator


def test_closed_system_generator_is_trace_preserving():
    H = 0.5 * sigmaz()
    generator = lindblad_generator(H)
    rho = (sigmax() + 0.2 * sigmaz()).unit()
    derivative = generator(rho)
    assert abs(derivative.tr()) < 1e-12


def test_amplitude_damping_generator_has_expected_dimensions():
    gamma = 0.03
    generator = lindblad_generator(0.5 * sigmaz(), [np.sqrt(gamma) * sigmam()])
    assert generator.issuper
    assert generator.shape == (4, 4)
