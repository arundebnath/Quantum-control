"""Plotting helpers (Matplotlib is an optional dependency)."""

def plot_pulses(result, labels=None, *, savepath=None, show=True):
    """Plot initial and optimized piecewise-constant control amplitudes.

    Parameters
    ----------
    result:
        Native result returned by :func:`openqctrl.optimize_grape`.
    labels:
        Optional sequence of control labels.
    savepath:
        Optional output filename. The file format is inferred by Matplotlib.
    show:
        Whether to call ``plt.show()``.

    Returns
    -------
    tuple
        Matplotlib figure and axes.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise ImportError("Install plotting support with `pip install openqctrl[plot]`.") from exc

    n_ctrls = result.initial_amps.shape[1]
    labels = list(labels) if labels is not None else [f"u{j + 1}(t)" for j in range(n_ctrls)]
    if len(labels) != n_ctrls:
        raise ValueError("labels must have one entry per control channel")

    fig, axes = plt.subplots(2, 1, sharex=True, sharey=True, constrained_layout=True)
    for ax, amplitudes, title in zip(
        axes,
        (result.initial_amps, result.final_amps),
        ("Initial controls", "Optimized controls"),
    ):
        for j in range(n_ctrls):
            step = list(amplitudes[:, j]) + [amplitudes[-1, j]]
            ax.step(result.time, step, where="post", label=labels[j])
        ax.axhline(0.0, color="0.5", linestyle=":", linewidth=0.7)
        ax.set_ylabel("Amplitude")
        ax.set_title(title)
        ax.legend(frameon=False)
    axes[-1].set_xlabel("Time (model units)")
    if savepath is not None:
        fig.savefig(savepath, bbox_inches="tight")
    if show:
        plt.show()
    return fig, axes
