"""QuTiP-Qtrl GRAPE integration."""

from collections.abc import Sequence
from numbers import Real

from qutip import Qobj
import qutip_qtrl.pulseoptim as pulseoptim


def optimize_grape(
    drift: Qobj,
    controls: Sequence[Qobj],
    initial: Qobj,
    target: Qobj,
    *,
    n_ts: int,
    evo_time: Real,
    fid_err_targ: float = 1e-3,
    max_iter: int = 200,
    max_wall_time: float = 30.0,
    min_grad: float = 1e-20,
    init_pulse_type: str = "SINE",
    out_file_ext: str | None = None,
    gen_stats: bool = True,
):
    """Optimize piecewise-constant controls using QuTiP-Qtrl GRAPE.

    The selected dynamics, propagator, and fidelity-error definitions are
    explicit to avoid silently relying on changing library defaults:
    ``GEN_MAT``, ``FRECHET``, and ``TRACEDIFF``.

    Returns the native QuTiP-Qtrl optimization result. In particular,
    ``result.fid_err`` follows QuTiP-Qtrl's selected ``TRACEDIFF`` convention;
    it is not relabelled as average gate infidelity.
    """
    if not isinstance(drift, Qobj):
        raise TypeError("drift must be a qutip.Qobj")
    if not controls:
        raise ValueError("at least one control generator is required")
    if any(not isinstance(control, Qobj) for control in controls):
        raise TypeError("every control generator must be a qutip.Qobj")
    if not isinstance(initial, Qobj) or not isinstance(target, Qobj):
        raise TypeError("initial and target must be qutip.Qobj instances")
    if not isinstance(n_ts, int) or n_ts < 1:
        raise ValueError("n_ts must be a positive integer")
    if not isinstance(evo_time, Real) or evo_time <= 0:
        raise ValueError("evo_time must be positive")
    if max_iter < 1:
        raise ValueError("max_iter must be positive")

    return pulseoptim.optimize_pulse(
        drift,
        list(controls),
        initial,
        target,
        n_ts,
        float(evo_time),
        fid_err_targ=fid_err_targ,
        min_grad=min_grad,
        max_iter=max_iter,
        max_wall_time=max_wall_time,
        out_file_ext=out_file_ext,
        init_pulse_type=init_pulse_type,
        gen_stats=gen_stats,
        dyn_type="GEN_MAT",
        prop_type="FRECHET",
        fid_type="TRACEDIFF",
    )
