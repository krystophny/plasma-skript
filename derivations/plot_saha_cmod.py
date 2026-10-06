#!/usr/bin/env python3
"""Replot the Alcator C-Mod Fig. 7b deuterium populations and Saha-Boltzmann values."""
from __future__ import annotations

import csv
import math
import runpy
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

HERE = Path(__file__).resolve().parent
DATA = HERE / "data/saha-cmod/data.csv"
OUTPUT = HERE / "build/fig"
FONT_DIR = HERE.parent / "fonts"
if not FONT_DIR.is_dir():
    FONT_DIR = HERE.parent / "animation-sources/fonts"
FONT_TEXT = FONT_DIR / "STIXTwoText-Regular.otf"
FONT_MATH = FONT_DIR / "STIXTwoMath-Regular.otf"

# Exact SI constants (2019 SI); temperatures in the plotted model are k_B T in eV.
M_E = 9.1093837015e-31       # kg
K_B = 1.380649e-23           # J K^-1
H = 6.62607015e-34           # J s
E_CHARGE = 1.602176634e-19   # J eV^-1
CHI_H_EV = 13.6
DATA_COLOR = "#0072B2"
SAHA_COLOR = "#B55000"


def configure_fonts() -> None:
    font_manager.fontManager.addfont(str(FONT_DIR / "STIXTwoText-Italic.otf"))
    for path in (FONT_TEXT, FONT_MATH):
        if not path.is_file():
            raise FileNotFoundError(f"Required lecture font not found: {path}")
        font_manager.fontManager.addfont(str(path))
    text_family = font_manager.FontProperties(fname=str(FONT_TEXT)).get_name()
    plt.rcParams.update({
        "font.family": text_family,
        "mathtext.fontset": "custom",
        "mathtext.rm": "STIX Two Text",
        "mathtext.it": "STIX Two Text:italic",
        "mathtext.bf": "STIX Two Math",
        "mathtext.cal": "STIX Two Math",
        "mathtext.sf": "STIX Two Text",
        "mathtext.tt": "STIX Two Text",
        "font.size": 18,
        "axes.labelsize": 18,
        "axes.labelweight": "regular",
        "xtick.labelsize": 18,
        "ytick.labelsize": 18,
        "legend.fontsize": 11,
        "axes.linewidth": 0.65,
        "xtick.major.width": 0.65,
        "ytick.major.width": 0.65,
        "xtick.minor.width": 0.5,
        "ytick.minor.width": 0.5,
        "svg.fonttype": "path",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
    })


def saha_ground_rhs(kt_eV: float) -> float:
    """Lecture convention g_i=g_n=1: n_e n_i/n_0, in m^-3."""
    kt_j = kt_eV * E_CHARGE
    q_e = (2.0 * math.pi * M_E * kt_j / H**2) ** 1.5
    return 2.0 * q_e * math.exp(-CHI_H_EV / kt_eV)


def half_ionization_temperature(total_nuclei_m3: float, rhs) -> float:
    """Solve Saha at x=1/2, where n_e=n_i=n_0=total_density/2."""
    target = total_nuclei_m3 / 2.0
    lo, hi = 0.05, 20.0  # eV
    for _ in range(160):
        mid = 0.5 * (lo + hi)
        if rhs(mid) < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def saha_level_population(n, kt_eV, ne_m3, ni_m3):
    """Ideal Saha-Boltzmann population for a resolved hydrogenic level n.

    The free-electron spin factor is the explicit 2 in Saha; the excited
    neutral level has g_n=2 n^2 and the singly charged ion has g_i=1.
    Therefore g_n/(2 g_i)=n^2. No continuum lowering is applied.
    """
    n = np.asarray(n, dtype=float)
    kt_j = kt_eV * E_CHARGE
    q_e = (2.0 * np.pi * M_E * kt_j / H**2) ** 1.5
    binding_eV = CHI_H_EV / n**2
    return ne_m3 * ni_m3 * n**2 / q_e * np.exp(binding_eV / kt_eV)


def load_data():
    with DATA.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    n = np.array([int(row["upper_level_n"]) for row in rows], dtype=float)
    measured = np.array([float(row["population_m-3"]) for row in rows])
    err_low = np.array([float(row["population_err_low_m-3"]) for row in rows])
    err_high = np.array([float(row["population_err_high_m-3"]) for row in rows])
    first = rows[0]
    return rows, n, measured, np.vstack((err_low, err_high)), first


def verify_independent_sanity_check() -> tuple[float, float]:
    """Compare SI constants with the NRL 2019 approximate Saha coefficient."""
    density = 1.0e20  # total H nuclei m^-3; half ionization means RHS=density/2
    exact = half_ionization_temperature(density, saha_ground_rhs)

    # NRL Plasma Formulary (2019), Eq. 17: 6.0e21 T_eV^(3/2) exp(-13.6/T_eV)
    # cm^-3 for g_i/g_n=1. Convert cm^-3 to m^-3 before solving.
    def nrl_rhs(kt_eV: float) -> float:
        return 6.0e21 * kt_eV**1.5 * math.exp(-CHI_H_EV / kt_eV) * 1.0e6

    nrl = half_ionization_temperature(density, nrl_rhs)
    assert abs(exact - nrl) / nrl < 0.01
    return exact, nrl


def plot_saha_cmod() -> None:
    configure_fonts()
    rows, n, measured, yerr, first = load_data()
    kt = float(first["kBT_e_eV"])
    ne = float(first["n_e_m-3"])
    ni = float(first["n_i_m-3"])
    kt_min = float(first["kBT_joint_min_eV"])
    kt_max = float(first["kBT_joint_max_eV"])
    ne_rel = float(first["u_n_e_relative"])

    central = saha_level_population(n, kt, ne, ni)
    # The source constrains T_e to 0.8--1.5 eV jointly; its Stark n_e uncertainty
    # is ±20%. Quasineutrality makes n_i=n_e here, so the density scaling is squared.
    lower = saha_level_population(n, kt_max, ne * (1.0 - ne_rel), ni * (1.0 - ne_rel))
    upper = saha_level_population(n, kt_min, ne * (1.0 + ne_rel), ni * (1.0 + ne_rel))

    width_mm, height_mm = 257.0, 128.0
    fig, ax = plt.subplots(figsize=(width_mm / 25.4, height_mm / 25.4))
    ax.fill_between(n, lower, upper, color=SAHA_COLOR, alpha=0.13, linewidth=0, zorder=1)
    ax.plot(n, central, color=SAHA_COLOR, linewidth=1.8, zorder=2)
    ax.errorbar(
        n, measured, yerr=yerr, fmt="o", markersize=8,
        color=DATA_COLOR, markerfacecolor=DATA_COLOR, markeredgewidth=0,
        ecolor=DATA_COLOR, elinewidth=1.1, capsize=3.0, capthick=1.1,
        linestyle="none", zorder=3,
    )
    # Direct labels instead of a legend.
    ax.annotate("measured, Alcator C-Mod divertor", xy=(n[-3], measured[-3]),
                xytext=(6.15, 4.6e16), color=DATA_COLOR, fontsize=18,
                arrowprops=dict(arrowstyle="-", color=DATA_COLOR, lw=0.8, shrinkA=2, shrinkB=7))
    ax.text(8.6, 1.05e16, "Saha", color=SAHA_COLOR, fontsize=18, ha="left", va="top")
    ax.text(8.35, 5.6e15, r"measured $T_e,\,n_e$ range", color=SAHA_COLOR, fontsize=15,
            alpha=0.85, ha="left", va="top")
    ax.text(2.75, 7.0e16, r"$k_B T_e = 1.2$ eV $\approx 1.4\times10^4$ K" "\n"
            r"$n_e = 8.8\times10^{20}$ m$^{-3}$", fontsize=16, color="#526175",
            ha="left", va="top", linespacing=1.5)

    ax.set_xlim(2.6, 10.4)
    ax.set_ylim(1.0e15, 1.0e17)
    ax.set_yscale("log")
    ax.set_xticks(np.arange(3, 11, 1))
    ax.set_yticks([1.0e15, 1.0e16, 1.0e17])
    ax.set_yticklabels([r"$10^{15}$", r"$10^{16}$", r"$10^{17}$"])
    ax.set_xlabel(r"upper level $p$ [1]", labelpad=6)
    ax.set_ylabel(r"$n_\mathrm{D}(p)$ [m$^{-3}$]", labelpad=8)
    ax.grid(axis="y", which="major", color="#E3E6EA", linewidth=0.6, zorder=0)
    ax.tick_params(which="major", length=5.0, direction="out", color="#17202A")
    ax.tick_params(which="minor", length=2.6, direction="out", color="#526175")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#17202A")
        ax.spines[side].set_linewidth(0.8)
    fig.subplots_adjust(left=0.105, right=0.985, bottom=0.15, top=0.97)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for ext in ("svg", "png", "pdf"):
        fig.savefig(OUTPUT / f"saha_cmod.{ext}", dpi=300)
    # Reuse the site's paint conversion; the exported student copy still
    # produces all light outputs without the website's optional dark variant.
    theme = HERE.parent / "scripts/prepare-media.py"
    if theme.is_file():
        dark_svg = runpy.run_path(str(theme))["dark_svg"]
        svg = (OUTPUT / "saha_cmod.svg").read_text()
        (OUTPUT / "saha_cmod-dark.svg").write_text(dark_svg(svg))
    plt.close(fig)

    ratios = measured / central
    fit_rows = [(int(nn), float(rr)) for nn, rr in zip(n, ratios) if nn >= 5]
    exact_half, nrl_half = verify_independent_sanity_check()
    print(f"Figure: {width_mm:.0f} × {height_mm:.0f} mm; seven digitized levels n=3,5–10")
    print("Measured/Saha central ratios at n>=5: " + ", ".join(f"n={nn}: {rr:.2f}" for nn, rr in fit_rows))
    print(f"Median ratio n>=5: {np.median([r for _, r in fit_rows]):.3f}; maximum: {max(r for _, r in fit_rows):.3f}")
    ev_to_kelvin = E_CHARGE / K_B
    print(f"Half-ionization check, n_H=1e20 m^-3: exact SI {exact_half * ev_to_kelvin:.0f} K; NRL 2019 {nrl_half * ev_to_kelvin:.0f} K")


if __name__ == "__main__":
    plot_saha_cmod()
