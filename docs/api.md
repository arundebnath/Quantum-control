# API reference

## `lindblad_generator(hamiltonian, collapse_ops=None)`

Builds a QuTiP Liouvillian from a Hamiltonian and a sequence of collapse
operators. With no collapse operators, it returns the coherent commutator
generator. Collapse operators use the standard Lindblad convention; e.g.
`np.sqrt(gamma) * sigmam()` gives amplitude damping at rate `gamma`.

## `optimize_grape(drift, controls, initial, target, *, ...)`

Thin wrapper around `qutip_qtrl.pulseoptim.optimize_pulse`.

Required arguments:

- `drift`: drift generator (`qutip.Qobj` superoperator).
- `controls`: nonempty sequence of control generators.
- `initial`: initial propagator/map.
- `target`: target propagator/map.
- `n_ts`: number of piecewise-constant control slots.
- `evo_time`: total evolution time.

Main options:

- `fid_err_targ=1e-3`
- `max_iter=200`
- `max_wall_time=30.0`
- `min_grad=1e-20`
- `init_pulse_type="SINE"`
- `out_file_ext=None`
- `gen_stats=True`

The wrapper fixes `dyn_type="GEN_MAT"`, `prop_type="FRECHET"`, and
`fid_type="TRACEDIFF"` explicitly. It returns the native QuTiP-Qtrl result,
including pulse arrays, fidelity-error fields, timing, and statistics.

## `plot_pulses(result, labels=None, *, savepath=None, show=True)`

Plots initial and optimized control amplitudes. Matplotlib is optional and can
be installed with `pip install openqctrl[plot]`. Returns `(figure, axes)`.

## Conventions and caveats

- Supply superoperators for `drift` and each entry in `controls`.
- The control generators must be consistent with the Hamiltonian-amplitude
  convention used to define the physical model.
- The API currently exposes map optimization through QuTiP-Qtrl; it does not
  yet provide a high-level system builder or a custom objective interface.
