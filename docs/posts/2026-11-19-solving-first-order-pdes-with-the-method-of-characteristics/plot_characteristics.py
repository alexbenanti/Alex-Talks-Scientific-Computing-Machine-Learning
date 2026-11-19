"""Generate the post's figures from analytical characteristic formulas.

Run from any directory with NumPy and Matplotlib installed:
    python path/to/plot_characteristics.py

No PDE time stepping or numerical inversion is used. Burgers profiles are
sampled parametrically only before the first loss of smoothness at t = 1.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_DIR = Path(__file__).resolve().parent / "images"
BLUE = "#2463a6"
TEAL = "#008577"
ORANGE = "#d76b26"
RUST = "#934012"
TRAJECTORY = "#6697b7"
TEXT = "#253442"
TIMES = (0.0, 0.75, 1.5)
COLORS = (BLUE, TEAL, ORANGE)


def configure_style():
    """Use explicit settings so repeated runs have the same appearance."""
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "text.color": TEXT,
            "axes.labelcolor": TEXT,
            "axes.titlecolor": TEXT,
            "axes.titlesize": 13,
            "axes.titleweight": "bold",
            "axes.edgecolor": "#a4b1bc",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.facecolor": "none",
            "figure.facecolor": "none",
            "xtick.color": TEXT,
            "ytick.color": TEXT,
            "grid.color": "#e6ebef",
            "grid.linewidth": 0.7,
            "legend.frameon": False,
            "savefig.dpi": 180,
            "savefig.transparent": True,
        }
    )


def panel_pair():
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), layout="constrained")
    for ax in axes:
        ax.set_xlabel("Position $x$")
        ax.grid(True)
        ax.set_axisbelow(True)
    axes[0].set_ylabel("Time $t$")
    axes[1].set_ylabel("Solution $u(x,t)$")
    return fig, axes


def show_sample_times(ax):
    for time, color in zip(TIMES, COLORS):
        ax.axhline(time, color=color, linewidth=1.2, linestyle="--", alpha=0.7)
    ax.set_yticks(TIMES)
    ax.set_ylim(-0.04, 1.57)


def save_figure(fig, filename):
    destination = OUTPUT_DIR / filename
    fig.savefig(destination, metadata={"Software": "Matplotlib"})
    plt.close(fig)
    print(f"Saved {destination}")


def plot_transport():
    fig, (geometry, profiles) = panel_pair()
    time = np.linspace(0, 1.5, 200)
    for xi in np.linspace(-3, 3, 13):
        geometry.plot(xi + time, time, color=TRAJECTORY, linewidth=1.4)
    show_sample_times(geometry)
    geometry.set_xlim(-3.3, 4.8)
    geometry.set_title(r"Parallel characteristics: $x=\xi+t$")

    x = np.linspace(-3.3, 4.8, 1000)
    for sample_time, color in zip(TIMES, COLORS):
        profiles.plot(
            x,
            np.exp(-((x - sample_time) ** 2)),
            color=color,
            linewidth=2.3,
            label=f"$t={sample_time:g}$",
        )
    profiles.set_xlim(-3.3, 4.8)
    profiles.set_ylim(-0.03, 1.08)
    profiles.set_title(r"Translation: $u=e^{-(x-t)^2}$")
    profiles.legend(loc="upper right")
    save_figure(fig, "transport.png")


def plot_variable_transport():
    fig, (geometry, profiles) = panel_pair()
    time = np.linspace(0, 1.5, 200)
    for xi in np.linspace(-1.5, 1.5, 13):
        geometry.plot(xi * np.exp(time), time, color=TRAJECTORY, linewidth=1.4)
    show_sample_times(geometry)
    geometry.set_xlim(-7, 7)
    geometry.set_title(r"Curved characteristics: $x=\xi e^t$")

    x = np.linspace(-7, 7, 1600)
    for sample_time, color in zip(TIMES, COLORS):
        u = np.exp(-sample_time) * np.exp(-((x * np.exp(-sample_time)) ** 2))
        profiles.plot(
            x, u, color=color, linewidth=2.3, label=f"$t={sample_time:g}$"
        )
    profiles.set_xlim(-7, 7)
    profiles.set_ylim(-0.03, 1.08)
    profiles.set_title(r"Stretching and decay: $u=e^{-t}e^{-(xe^{-t})^2}$")
    profiles.legend(loc="upper right")
    save_figure(fig, "variable-transport.png")


def plot_burgers():
    fig, (geometry, profiles) = panel_pair()
    time = np.linspace(0, 1, 300)
    for xi in np.linspace(-np.pi, np.pi, 21):
        geometry.plot(
            xi - time * np.sin(xi), time, color=TRAJECTORY, linewidth=1.3
        )
    geometry.axhline(1, color=RUST, linewidth=1.6, linestyle="--")
    geometry.annotate(
        "First loss of smoothness: $t=1$",
        xy=(0, 1),
        xytext=(0, 1.06),
        ha="center",
        va="bottom",
        color=RUST,
        fontsize=10,
    )
    geometry.set_xlim(-np.pi - 0.1, np.pi + 0.1)
    geometry.set_ylim(-0.025, 1.17)
    geometry.set_yticks((0, 0.25, 0.5, 0.75, 1))
    geometry.set_title(r"Converging characteristics: $x=\xi-t\sin\xi$")

    # These are exact parameterizations of smooth solution profiles.
    # For t < 1, dx/dxi = 1 - t*cos(xi) > 0, so every x has one value of u.
    xi = np.linspace(-np.pi, np.pi, 6001)
    u = -np.sin(xi)
    for sample_time, color in zip((0.0, 0.5, 0.9, 0.99), (*COLORS, RUST)):
        x = xi - sample_time * np.sin(xi)
        profiles.plot(
            x, u, color=color, linewidth=2.1, label=f"$t={sample_time:g}$"
        )
    profiles.set_xlim(-np.pi - 0.1, np.pi + 0.1)
    profiles.set_ylim(-1.1, 1.1)
    profiles.set_title("Bounded values, increasingly steep slope")
    profiles.legend(loc="lower left", fontsize=10)
    save_figure(fig, "burgers.png")


def main():
    configure_style()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    plot_transport()
    plot_variable_transport()
    plot_burgers()


if __name__ == "__main__":
    main()
