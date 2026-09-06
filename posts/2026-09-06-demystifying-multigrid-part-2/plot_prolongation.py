"""Generate the linear prolongation illustration: py plot_prolongation.py."""

from pathlib import Path
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


coarse_x = np.linspace(0, 1, 5)
coarse_v = np.array([0, 1, 0.5, 1.5, 0])
fine_x = np.linspace(0, 1, 9)
fine_v = np.interp(fine_x, coarse_x, coarse_v)
P = 0.5 * np.array([[1, 0, 0], [2, 0, 0], [1, 1, 0],
                    [0, 2, 0], [0, 1, 1], [0, 0, 2], [0, 0, 1]])
np.testing.assert_allclose(P @ coarse_v[1:-1], fine_v[1:-1])

blue, orange = "#235789", "#b65c20"
plt.rcParams.update({"font.size": 10, "mathtext.fontset": "stix"})
fig, axes = plt.subplots(1, 2, figsize=(10, 3.7), sharey=True)
fig.subplots_adjust(left=0.065, right=0.985, top=0.83, bottom=0.27, wspace=0.42)

for ax, nodes, title in zip(axes, (coarse_x, fine_x),
                          (r"Coarse grid $\Omega^{2h}$", r"Fine grid $\Omega^h$")):
    ax.set_title(title, loc="left", fontsize=13, pad=14)
    ax.plot(coarse_x, coarse_v, color=blue, alpha=0.65, linewidth=1.6,
            solid_joinstyle="round", solid_capstyle="round", zorder=1)
    ax.set_xlim(-0.035, 1.035)
    ax.set_ylim(-0.08, 1.72)
    ax.set_xticks([0, 0.5, 1], labels=["0", "0.5", "1"])
    ax.set_xticks(nodes, minor=True)
    ax.set_yticks([0, 0.5, 1, 1.5])
    ax.tick_params(axis="both", which="major", length=3, color="#8a8a8a", labelsize=9)
    ax.tick_params(axis="x", which="minor", length=3, color="#8a8a8a")
    ax.spines[["top", "right"]].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#8a8a8a")
        ax.spines[side].set_linewidth(0.6)
    ax.set_xlabel(r"$x$", labelpad=4)

axes[0].set_ylabel(r"$v(x)$", labelpad=8)
axes[0].scatter(coarse_x, coarse_v, color=blue, s=38, zorder=3)
axes[1].scatter(fine_x[::2], fine_v[::2], color=blue, s=38, zorder=3,
                label="Copied value")
axes[1].scatter(fine_x[1::2], fine_v[1::2], color=orange, marker="D", s=35,
                zorder=4, label="Midpoint average")
# Reserve the gap between panels for a single operator arrow.
axes[0].annotate("", xy=(0.57, 0.54), xytext=(0.47, 0.54),
                 xycoords=fig.transFigure, textcoords=fig.transFigure,
                 arrowprops=dict(arrowstyle="-|>", color=blue, lw=1.3, mutation_scale=13))
fig.text(0.52, 0.59, r"$\mathbf{P}_{2h}^{h}$", fontsize=17, ha="center", color=blue)
fig.legend(*axes[1].get_legend_handles_labels(), loc="lower center",
           bbox_to_anchor=(0.525, 0.035), ncol=2, frameon=False, fontsize=10,
           handletextpad=0.5, columnspacing=2.4)
fig.savefig(Path(__file__).with_name("prolongation.png"), dpi=220,
            transparent=True, bbox_inches="tight")
plt.close(fig)
