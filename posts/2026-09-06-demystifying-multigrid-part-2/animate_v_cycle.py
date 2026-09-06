"""Generate the V-cycle traversal GIF: py animate_v_cycle.py."""

from pathlib import Path
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


blue, orange, gray = "#235789", "#b65c20", "#9b9b9b"
levels = list(range(6)) + list(range(4, -1, -1))
path_x = np.arange(11)
path_y = 5 - np.array(levels)
frames = []
plt.rcParams.update({"font.size": 11, "mathtext.fontset": "stix"})
for stage, level in enumerate(levels):
    fig = plt.figure(figsize=(9, 5.8), dpi=120)
    ax = fig.add_axes([0.15, 0.35, 0.76, 0.49])
    ax.plot(path_x, path_y, color=gray, alpha=0.4, linewidth=1.5)
    ax.plot(path_x[:stage + 1], path_y[:stage + 1], color=blue, linewidth=2)
    ax.scatter(path_x, path_y, s=40, color=gray, zorder=3)
    ax.scatter(path_x[stage], path_y[stage], s=160, color=orange, zorder=4)
    for row in range(6):
        ax.axhline(row, color=gray, alpha=0.12, linewidth=0.7, zorder=0)
    ax.set_yticks(range(6), labels=[r"$\Omega^{32h}$", r"$\Omega^{16h}$",
                                   r"$\Omega^{8h}$", r"$\Omega^{4h}$",
                                   r"$\Omega^{2h}$", r"$\Omega^h$"])
    ax.tick_params(axis="y", length=0, pad=12)
    ax.set(xticks=[], xlim=(-0.6, 10.6), ylim=(-0.5, 5.6))
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.text(0.5, 0.95, "One multigrid V-cycle", ha="center", fontsize=18)
    fig.text(0.30, 0.88, "Smooth → restrict residual", ha="center", color=blue)
    fig.text(0.75, 0.88, "Correct → smooth", ha="center", color=blue)

    if stage < 5:
        title = "Pre-smooth, then restrict the residual"
        detail = "Start the coarse error equation from zero."
    elif stage == 5:
        title = "Solve the coarsest error equation directly"
        detail = "One interior unknown remains."
    else:
        title = "Prolongate the correction, then post-smooth"
        detail = "Add the correction to this level's saved approximation."
    fig.text(0.5, 0.28, title, ha="center", fontsize=13, color=orange)
    fig.text(0.5, 0.235, detail, ha="center", fontsize=10)
    grid = fig.add_axes([0.18, 0.085, 0.70, 0.10])
    n = 64 // 2**level
    nodes = np.linspace(0, 1, n + 1)
    grid.hlines(0, 0, 1, color=blue, linewidth=1.2)
    grid.vlines(nodes, -0.1, 0.1, color=blue, linewidth=1)
    grid.text(0, -0.22, "0", ha="center", fontsize=9)
    grid.text(1, -0.22, "1", ha="center", fontsize=9)
    grid.set(xlim=(-0.02, 1.02), ylim=(-0.4, 0.45))
    grid.axis("off")
    fig.text(0.53, 0.19, f"Current grid: {n} intervals", ha="center", fontsize=10)
    fig.text(0.95, 0.035, f"{stage + 1} / {len(levels)}", ha="right",
             color=gray, fontsize=9)
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    fig.canvas.draw()
    rgba = np.asarray(fig.canvas.buffer_rgba()).copy()
    # Reserve one palette entry for transparency; disposal clears the old frame.
    frame = Image.fromarray(rgba[:, :, :3]).quantize(colors=255)
    palette = frame.getpalette()
    pixels = np.asarray(frame).copy()
    pixels[rgba[:, :, 3] < 128] = 255
    frame = Image.fromarray(pixels)
    frame.putpalette((palette + [0] * 768)[:765] + [255, 0, 255])
    frames.append(frame)
    plt.close(fig)

out = Path(__file__).parent
frames[0].save(out / "v-cycle.gif", save_all=True, append_images=frames[1:],
               duration=[1400] * 5 + [2000] + [1400] * 4 + [2400],
               loop=0, transparency=255, disposal=2, optimize=False)
frames[5].save(out / "v-cycle-still.png", transparency=255)
