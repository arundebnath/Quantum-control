# OpenQCtrl

**Open-system quantum optimal control in Python.**

OpenQCtrl is a research-oriented starting point for modelling finite-dimensional open quantum systems and optimizing control pulses for quantum-state and quantum-operation objectives. The first implementation wraps the GRAPE pulse optimizer in [QuTiP-Qtrl](https://qutip-qtrl.readthedocs.io/) and uses QuTiP objects for Hamiltonians, Lindblad generators, and quantum maps.

> **Status:** experimental alpha. The initial example reproduces the structure of the supplied two-level Lindblad-control notebook. The package is deliberately small; its API may change before a stable release.

## Capabilities in this release

- Construct Lindblad generators from a drift Hamiltonian and collapse operators.
- Represent control Hamiltonians as Liouville-space generators.
- Run GRAPE through QuTiP-Qtrl with explicit optimizer settings.
- Return the native optimizer result for diagnostics and pulse analysis.
- Plot initial and optimized control amplitudes.

## Physical model

The dynamics follow

\[
\dot{\rho}(t)=-i[H(t),\rho(t)]+\sum_j\mathcal{D}[C_j]\rho(t),
\qquad
H(t)=H_0+\sum_k u_k(t)H_k,
\]

where

\[
\mathcal{D}[C]\rho=C\rho C^\dagger-\frac12\{C^\dagger C,\rho\}.
\]

The example uses a two-level system,

\[
H_0=\frac{\omega_q}{2}\sigma_z+\frac{\Delta}{2}\sigma_x,
\qquad C=\sqrt{\gamma}\,\sigma_-,
\]

with two control Hamiltonians \(H_{c,1}=\sigma_z\) and \(H_{c,2}=\sigma_x\). The initial and target maps are built from the identity and Hadamard operators, respectively, using QuTiP's `sprepost`.

**Unit convention:** the example uses dimensionless numerical parameters with \(\hbar=1\). Consequently, time and Hamiltonian parameters are mutually inverse units. The original notebook's `ns` and `MHz` plot labels are not physically established by its parameter definitions and are not retained as default labels.

## Install

Python 3.10–3.12 is recommended.

```bash
git clone https://github.com/<your-account>/OpenQCtrl.git
cd OpenQCtrl
python -m pip install -e ".[dev]"
```

The optimizer integration requires both QuTiP and QuTiP-Qtrl. See `pyproject.toml` for dependency declarations.

## Run the example

```bash
python examples/open_system/two_level_hadamard.py
```

The script prints optimizer diagnostics and saves pulse plots in the current directory. The optimization outcome depends on software versions and numerical settings; no particular fidelity or iteration count is guaranteed.

## Minimal API

```python
from qutip import sigmax, sigmaz, sigmam, gates, identity, sprepost
from openqctrl import lindblad_generator, optimize_grape

H0 = 0.5 * sigmaz() + 0.125 * sigmax()
collapse_ops = [gamma**0.5 * sigmam()]
drift = lindblad_generator(H0, collapse_ops)
controls = [lindblad_generator(sigmaz()), lindblad_generator(sigmax())]

initial_map = sprepost(identity(2), identity(2))
target_map = sprepost(gates.hadamard_transform(1), gates.hadamard_transform(1))

result = optimize_grape(
    drift, controls, initial_map, target_map,
    n_ts=10, evo_time=2.0,
    fid_err_targ=1e-3, max_iter=200,
)
```

See [`docs/api.md`](docs/api.md) and the runnable example for the complete interface.

## Scientific interpretation and limitations

- The example optimizes a **quantum map** in the presence of amplitude damping. The dissipative evolution is generally non-unitary, even when the target map is generated from a unitary Hadamard operator.
- The example explicitly selects QuTiP-Qtrl's `TRACEDIFF` fidelity-error convention. Do not interpret its reported error as average gate infidelity or process infidelity without a separate derivation and validation.
- GRAPE discretizes the control into `n_ts` piecewise-constant time slots.
- This initial interface delegates propagation and gradient evaluation to QuTiP-Qtrl. It does not yet provide independent propagators, custom objective functions, robust ensemble optimization, or Krotov optimization.
- The package does not claim complete positivity or positivity preservation for arbitrary numerical settings. Validate physical constraints for each chosen propagation method and tolerance.

## Repository map

```text
src/openqctrl/       package implementation
examples/            runnable research examples
tests/               automated tests
docs/                theory and API notes
```

## Development and tests

```bash
python -m pip install -e ".[dev]"
pytest
```

The test suite checks generator construction and API validation. Integration tests requiring QuTiP-Qtrl are marked by their imports and should be run in the declared environment.

## Citation

Please cite the repository using the metadata in [`CITATION.cff`](CITATION.cff). No software paper is currently associated with this project.

## License

MIT. See [`LICENSE`](LICENSE).
