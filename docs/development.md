# Development notes

## Initial code extraction

The original notebook is retained as the scientific reference. Its model
construction, optimizer call, and pulse plotting are separated into package
modules and a script example. Notebook-only IPython magic and implicit output
file generation are removed.

## Before tagging a release

1. Test against a clean environment and record exact Python, QuTiP, and
   QuTiP-Qtrl versions.
2. Verify the `sprepost` map convention against the intended channel action.
3. Derive and document the `TRACEDIFF` objective used by the installed
   QuTiP-Qtrl release.
4. Compare analytic/optimizer gradients against finite differences.
5. Add tests for trace preservation, Hermiticity, positivity/complete
   positivity where numerically appropriate, and time-grid convergence.
6. Add bounded-amplitude and slew-rate constraints only after specifying
   their physical interpretation.
7. Add state-transfer and channel/process objectives as distinct problem
   types rather than overloading the current wrapper.

## Scope

The alpha release is a QuTiP/QuTiP-Qtrl adapter, not an independent dynamics
or optimization engine. Keep physical model construction separate from
optimization backends as the package grows.
