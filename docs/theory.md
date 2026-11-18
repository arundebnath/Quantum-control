# Mathematical model

## Controlled Lindblad dynamics

OpenQCtrl's first backend represents the density operator as a vector in Liouville space. For a finite-dimensional system,

\[
\frac{d\rho}{dt}=-i[H(t),\rho]+\sum_{j=1}^{N_c}\left(
C_j\rho C_j^\dagger-\frac{1}{2}C_j^\dagger C_j\rho
-\frac{1}{2}\rho C_j^\dagger C_j
\right),
\]

with

\[
H(t)=H_0+\sum_{k=1}^{N_u}u_k(t)H_k.
\]

The generator is affine in the controls,

\[
\mathcal L(t)=\mathcal L_0+\sum_k u_k(t)\mathcal L_k,
\]

where

\[
\mathcal L_0=-i[H_0,\cdot]+\sum_j\mathcal D[C_j],
\qquad
\mathcal L_k=-i[H_k,\cdot].
\]

For a piecewise-constant pulse with \(N_t\) slots and slot duration
\(\Delta t=T/N_t\), the propagation is composed from slot propagators
\(\mathcal P_n=\exp[\mathcal L_n\Delta t]\). The optimizer backend computes
propagators and gradients using the Frechet method selected in the API.

## Notebook model

The supplied notebook specifies

\[
H_0=\frac{\omega_q}{2}\sigma_z+\frac{\Delta}{2}\sigma_x,
\qquad C_1=\sqrt{\gamma}\sigma_-,
\]

and control generators formed from \(H_{c,1}=\sigma_z\) and
\(H_{c,2}=\sigma_x\). Its initial and target maps are

\[
\mathcal E_0=\operatorname{sprepost}(I,I),\qquad
\mathcal E_{\mathrm{target}}=
\operatorname{sprepost}(H_{\mathrm{Had}},H_{\mathrm{Had}}).
\]

The package example retains these choices. In particular, the control
Hamiltonians are the Pauli operators themselves, not one-half Pauli
operators. That scaling is part of the model definition and changes the
meaning of the optimized amplitudes.

## Objective and interpretation

The initial example explicitly selects QuTiP-Qtrl's `TRACEDIFF` fidelity
error. The returned `fid_err` should be reported using that backend-specific
definition. It must not be casually renamed average gate infidelity,
entanglement infidelity, or process infidelity.

A unitary target map does not make the realized evolution unitary: nonzero
collapse operators generate a dissipative channel. A physically meaningful
assessment should separately inspect trace preservation, complete positivity,
and the chosen operational fidelity metric.

## Units

The notebook sets \(\omega_q=1\), \(\Delta=0.25\), \(\gamma=0.01\), and
\(T=2\), but does not define a dimensional conversion. The example therefore
uses dimensionless model units with \(\hbar=1\). If a dimensional convention is
chosen, Hamiltonian frequencies and inverse time must be converted consistently.
The previous plot's `ns` and `MHz` labels are intentionally replaced by
`model units` until that convention is supplied.
