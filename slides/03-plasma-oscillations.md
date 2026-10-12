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
| 4 | Plasma frequency | static | intro-plasma-oscillations | Metal versus fusion; fastest electrostatic time scale. |
| 5 | EM wave at a plasma edge | animation | intro-plasma-oscillations | kin6d Maxwell-Lorentz run: omega = 0.5 omega_pe reflected (electrons follow), omega = 2 omega_pe transmitted. |
| 6 | Electromagnetic waves | static | intro-plasma-oscillations | Teaser: reflected below, transmitted above the plasma frequency. |
| 7 | Frequency and length scales | static | intro-plasma-oscillations | Closing reminder: any species, ions, inertial length, effective mass when ions move. |

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
