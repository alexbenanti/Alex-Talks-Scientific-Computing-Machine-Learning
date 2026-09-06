"""Regenerate a figure with: py plot_eigenmodes.py --n 8 (or --n 4)."""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--n", type=int, choices=(4, 8), default=8)
n = parser.parse_args().n
x_nodes = np.arange(n + 1) / n
x_smooth = np.linspace(0, 1, n * 200 + 1)

# Verify the nonzero modes against the interior Dirichlet matrix.
T = 2 * np.eye(n - 1) - np.eye(n - 1, k=1) - np.eye(n - 1, k=-1)
for j in range(1, n):
    v = np.sin(np.pi * j * x_nodes[1:-1])
    eigenvalue = 4 * np.sin(np.pi * j / (2 * n)) ** 2
    np.testing.assert_allclose(T @ v, eigenvalue * v, atol=1e-14)

rows = n // 2
fig, axes = plt.subplots(rows, 2, figsize=(10, 2.5 * rows + (1 if n == 4 else 0)),
                         sharex=True, sharey=True)
for j, ax in enumerate(axes.flat[:n - 1], start=1):
    values = np.sin(np.pi * j * x_nodes)
    values[np.abs(values) < 1e-14] = 0
    color = "#235789"
    ax.plot(x_smooth, np.sin(np.pi * j * x_smooth), color=color,
            linewidth=1.8, label="Sine curve (visual guide)")
    ax.plot(x_nodes, values, "o", color=color, markersize=5,
            label="Discrete grid samples", zorder=3)
    ax.axhline(0, color="#777777", linewidth=0.7, zorder=0)
    ax.set_title(fr"$j={j}$", fontsize=11)
    ax.set_xlim(0, 1)
    ax.set_ylim(-1.15, 1.15)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1])
    ax.set_yticks([-1, 0, 1])
    ax.spines[["top", "right"]].set_visible(False)

axes.flat[-1].set_visible(False)
axes[rows - 2, 1].tick_params(labelbottom=True)

fig.suptitle(r"Eigenmodes $v_\ell^{(j)}=\sin(\pi j\ell/n)$ for " + fr"$n={n}$", fontsize=15)
fig.supxlabel(r"$x_\ell=\ell/n$")
fig.supylabel(r"$v^{(j)}(x)$")
fig.legend(*axes.flat[0].get_legend_handles_labels(), loc="lower center",
           bbox_to_anchor=(0.5, 0.025), ncol=2, frameon=False)
fig.tight_layout(rect=(0.02, 0.12 if n == 4 else 0.065, 1, 0.94 if n == 4 else 0.96))
# Let the website background show through the figure and each panel.
fig.savefig(Path(__file__).with_name(f"eigenmodes-n{n}.png"), dpi=180,
            transparent=True, bbox_inches="tight")
plt.close(fig)
