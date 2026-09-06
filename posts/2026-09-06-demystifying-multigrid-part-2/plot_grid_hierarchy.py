"""Generate the four-level 1D grid illustration: py plot_grid_hierarchy.py."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


fig, ax = plt.subplots(figsize=(10, 5.6))
color = "#235789"
labels = [r"$\Omega^h$", r"$\Omega^{2h}$", r"$\Omega^{4h}$",
          r"$\Omega^{h_0}=\Omega^{8h}$"]
spacings = [r"$h=1/16$", r"$2h=1/8$", r"$4h=1/4$", r"$h_0=8h=1/2$"]

# Vertical guides emphasize that all coarse-grid points are fine-grid points.
for x in np.linspace(0, 1, 17):
    ax.plot([x, x], [-0.08, 3.08], color="#888888", alpha=0.18,
            linewidth=0.7, linestyle=":", zorder=0)

for level, intervals in enumerate((16, 8, 4, 2)):
    y = 3 - level
    nodes = np.linspace(0, 1, intervals + 1)
    ax.hlines(y, 0, 1, color=color, linewidth=1.6)
    ax.vlines(nodes, y - 0.09, y + 0.09, color=color, linewidth=1.8)
    ax.text(-0.055, y, labels[level], ha="right", va="center", fontsize=15)
    ax.text(1.04, y, f"Level {level + 1}" +
            (" (finest)" if level == 0 else " (coarsest)" if level == 3 else ""),
            ha="left", va="center", fontsize=11)
    for x, label in ((0, "$0$"), (1, "$1$")):
        ax.text(x, y - 0.16, label, ha="center", va="top", fontsize=11)
    # Mark one interval on each grid to show the doubling of mesh spacing.
    ax.annotate("", xy=(0, y + 0.25), xytext=(1 / intervals, y + 0.25),
                arrowprops=dict(arrowstyle="|-|", color=color, linewidth=1))
    ax.text(0.5 / intervals, y + 0.35, spacings[level], ha="center",
            va="bottom", fontsize=12)

ax.set_xlim(-0.36, 1.30)
ax.set_ylim(-0.45, 3.85)
ax.axis("off")
fig.tight_layout(pad=0.5)
fig.savefig(Path(__file__).with_name("grid-hierarchy.png"), dpi=180,
            transparent=True, bbox_inches="tight")
plt.close(fig)
