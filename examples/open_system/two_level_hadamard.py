"""Two-level open-system gate-control example based on the supplied notebook."""

from pathlib import Path

import numpy as np
from qutip import gates, identity, sigmax, sigmam, sigmaz, sprepost

from openqctrl import lindblad_generator, optimize_grape, plot_pulses


def main():
    # Dimensionless model parameters; hbar = 1.
    delta = 0.25
    omega_q = 1.0
    gamma = 0.01

    H0 = 0.5 * omega_q * sigmaz() + 0.5 * delta * sigmax()
    collapse_ops = [np.sqrt(gamma) * sigmam()]

    drift = lindblad_generator(H0, collapse_ops)
    controls = [
        lindblad_generator(sigmaz()),
        lindblad_generator(sigmax()),
    ]

    initial_map = sprepost(identity(2), identity(2))
    hadamard = gates.hadamard_transform(1)
    target_map = sprepost(hadamard, hadamard)

    result = optimize_grape(
        drift,
        controls,
        initial_map,
        target_map,
        n_ts=10,
        evo_time=2.0,
        fid_err_targ=1e-3,
        max_iter=200,
        max_wall_time=30.0,
        min_grad=1e-20,
        init_pulse_type="SINE",
        out_file_ext=None,
        gen_stats=True,
    )

    print("Initial fidelity error:", result.initial_fid_err)
    print("Final fidelity error:", result.fid_err)
    print("Final gradient norm:", result.grad_norm_final)
    print("Termination:", result.termination_reason)
    print("Iterations:", result.num_iter)
    print("Wall time (s):", result.wall_time)

    plot_pulses(
        result,
        labels=[r"$u_z(t)$", r"$u_x(t)$"],
        savepath=Path("two_level_hadamard_pulses.pdf"),
        show=True,
    )


if __name__ == "__main__":
    main()
