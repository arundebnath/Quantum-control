import pytest
from qutip import identity, sigmax, sprepost

from openqctrl import optimize_grape, lindblad_generator


def test_optimizer_rejects_empty_controls():
    op = sprepost(identity(2), identity(2))
    with pytest.raises(ValueError, match="at least one control"):
        optimize_grape(
            lindblad_generator(0.5 * sigmax()), [], op, op,
            n_ts=5, evo_time=1.0,
        )
