# Plasma oscillations

LOOK deck; THINK work takes place on blank Goodnotes notebook pages.
No writing pages in the deck. One idea per page.

Online deck: [present/03-plasma-oscillations/](https://krystophny.github.io/plasma-skript/present/03-plasma-oscillations/).
The site build exports the same pages as SVG and PDF, with inline animations and offline caching.

## Page sequence

| Page | Title | Kind | Script section label | Lecturer cue |
|---|---|---|---|---|
| 1 | Title | static | plasma-oscillations | Dynamic response. |
| 2 | Electron slab oscillation | animation | intro-plasma-oscillations | After the whiteboard model; predict force reversal. Replay after the derivation. |
| 3 | Electron plasma oscillations | static | intro-plasma-oscillations | Recap of the whiteboard derivation: Gauss, Newton, oscillator, result. |
| 4 | Sheet model: plasma oscillation | animation | intro-plasma-oscillations | After the recap: the slab cut into 160 sheets (Dawson). Phase space, sheets, Gauss field; no sheet overtakes another, so every sheet oscillates at omega_pe whatever its amplitude; measured omega/omega_pe = 1.0000. |
| 5 | Sheet model: wave breaking | animation | intro-plasma-oscillations | Same model at k v_0/omega_pe = 1.5: predict when neighbours meet; first crossing at omega_pe t = 0.73 = arcsin(omega_pe/k v_0); phase space folds, several streams at one x, the oscillator picture ends. |
| 6 | Plasma frequency | static | intro-plasma-oscillations | Metal versus fusion; fastest electrostatic time scale. |
| 7 | EM wave at a plasma edge | animation | intro-plasma-oscillations | kin6d Maxwell-Lorentz run: omega = 0.5 omega_pe reflected (electrons follow), omega = 2 omega_pe transmitted. |
| 8 | Electromagnetic waves | static | intro-plasma-oscillations | Teaser: reflected below, transmitted above the plasma frequency. |
| 9 | Frequency and length scales | static | intro-plasma-oscillations | Closing reminder: any species, ions, inertial length, effective mass when ions move. |
| 10 | Ions move too | plot | intro-plasma-oscillations | After the closing reminder: ions and electrons in antiphase, xi_i = -(m_e/m_i) xi_e; measured omega against sqrt(1 + m_e/m_i) from m_i = m_e to hydrogen, agreement better than 2e-4. |

Rebuilt from scratch on 2026-10-13. Delivery: title, whiteboard model,
animation, whiteboard derivation, animation again, recap page.

## Evidence and assets

2025 filled Chapter 1–5 pages 8–42 supply the coverage checklist only.
All diagrams and plots are original; plots share the Skript derivation source.
Animations use media/animations.json and retain their PDF posters.
Photo provenance, where applicable, is in photos/credits.md.

The incoming kin6d source for `animations/plasma_oscillation.py` reads
`animations/data/kin6d/plasma-oscillation/`: an RK5 slab trajectory and its
certified band (half-width below 0.003), displayed with $\xi_0/a=0.1$ [1].
Published streams remain the exact revisions in `media/animations.json`
until a reviewed render updates that registry and the corresponding poster.

## Sheet and two-species visuals (2026-10-26)

`animations/sheet_oscillation.py` (`sheet-oscillation`, 16 s; `sheet-wave-breaking`,
19 s; pages 4 and 5): 160 cold electron sheets, periodic box of one wavelength,
fixed ion background, start at rest positions with v = v_0 sin(kx); exact
sheet-model field from the number of sheets to the left, leapfrog with
400 steps per plasma period. Checks (`SheetOscillationPhysics`): the field
equals the sheet-by-sheet Gauss sum; RK4 with that sum returns every sheet
after one period 2 pi/omega_pe to 2e-9; leapfrog omega/omega_pe = 1.0000103
at k v_0/omega_pe = 0.5; first crossing at omega_pe t = 0.72978 for 1.5
(discrete sheets 0.72979, continuum arcsin(2/3) = 0.72973).

`derivations/plot_two_species_oscillation.py` writes `two_species_oscillation`
(page 10): cold 1D particle-in-cell, 4096 particles per species, linear
weighting, k v_0/omega_pe = 0.005, no net momentum. Measured omega/omega_pe
against sqrt(1 + m_e/m_i): 1.41398/1.41421 (m_i = m_e), 1.11796/1.11803 (4),
1.00498/1.00499 (100), 1.000263/1.000272 (1836); xi_i/xi_e = -m_e/m_i to 1e-4
(`TwoSpeciesOscillationPhysics`). At k v_0/omega_pe = 0.05 the mode
phase-mixes within a few periods when ions move (nonlinear), so the plot
stays at small amplitude.

