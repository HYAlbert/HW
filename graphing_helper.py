"""
Draw stability circles with the unit circle (|Γ| = 1).

Figures:
- stability_circles.png: original device input/output stability circles (Problem 1).
- loss_circle.png: composite device (after output loss) stability circles (Problem 2).
"""

import numpy as np
import matplotlib.pyplot as plt

from problem_calc import C_L, r_L, C_S, r_S, C_L_p, r_L_p, C_S_p, r_S_p


def circle_points(center_real, center_imag, radius, n=500):
    """Return (x, y) points for a circle in the complex plane."""
    theta = np.linspace(0, 2 * np.pi, n)
    x = center_real + radius * np.cos(theta)
    y = center_imag + radius * np.sin(theta)
    return x, y


def plot_stability_circle(ax, center_real, center_imag, radius, title, gamma_label):
    """Plot unit circle and one stability circle on given axes."""
    # Unit circle (|Γ| = 1)
    ux, uy = circle_points(0, 0, 1)
    ax.plot(ux, uy, "b-", linewidth=1.5, label="Unit circle (|Γ| = 1)")

    # Stability circle
    sx, sy = circle_points(center_real, center_imag, radius)
    ax.plot(sx, sy, "r-", linewidth=1.5, label="Stability circle")

    ax.set_xlabel(f"Re({gamma_label})")
    ax.set_ylabel(f"Im({gamma_label})")
    ax.set_title(title)
    ax.set_aspect("equal")
    ax.axhline(0, color="k", linewidth=0.5)
    ax.axvline(0, color="k", linewidth=0.5)
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, alpha=0.3)


def main():
    # Original device stability circles (Problem 1)
    fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    plot_stability_circle(
        ax1,
        C_L.real,
        C_L.imag,
        r_L,
        title="Input Stability Circle (Load Plane)",
        gamma_label="Γ_L",
    )

    plot_stability_circle(
        ax2,
        C_S.real,
        C_S.imag,
        r_S,
        title="Output Stability Circle (Source Plane)",
        gamma_label="Γ_S",
    )

    fig1.tight_layout()
    fig1.savefig("stability_circles.png", dpi=150, bbox_inches="tight")

    # Composite device stability circles after adding minimum-loss resistor (Problem 2)
    fig2, (bx1, bx2) = plt.subplots(1, 2, figsize=(10, 5))

    plot_stability_circle(
        bx1,
        C_L_p.real,
        C_L_p.imag,
        r_L_p,
        title="Composite Input Stability Circle (Load Plane)",
        gamma_label="Γ_L",
    )

    plot_stability_circle(
        bx2,
        C_S_p.real,
        C_S_p.imag,
        r_S_p,
        title="Composite Output Stability Circle (Source Plane)",
        gamma_label="Γ_S",
    )

    fig2.tight_layout()
    fig2.savefig("loss_circle.png", dpi=150, bbox_inches="tight")

    plt.show()


if __name__ == "__main__":
    main()
