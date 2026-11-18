"""Liouville-space generators for finite-dimensional open systems."""

from collections.abc import Sequence

from qutip import Qobj, liouvillian


def lindblad_generator(hamiltonian: Qobj, collapse_ops: Sequence[Qobj] | None = None) -> Qobj:
    """Return the Lindblad superoperator for a Hamiltonian and collapse operators.

    Parameters
    ----------
    hamiltonian:
        System Hamiltonian :math:`H` (units of inverse time when hbar=1).
    collapse_ops:
        Collapse operators :math:`C_j`. Use, for example,
        ``sqrt(gamma) * sigmam()`` for amplitude damping.

    Returns
    -------
    qutip.Qobj
        Liouville-space generator ``-1j[H, .] + sum_j D[C_j]``.
    """
    if not isinstance(hamiltonian, Qobj):
        raise TypeError("hamiltonian must be a qutip.Qobj")
    collapse_ops = [] if collapse_ops is None else list(collapse_ops)
    if any(not isinstance(op, Qobj) for op in collapse_ops):
        raise TypeError("every collapse operator must be a qutip.Qobj")
    return liouvillian(hamiltonian, collapse_ops)
