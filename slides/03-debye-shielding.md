# Debye shielding

LOOK deck; THINK work takes place on blank Goodnotes notebook pages.
No writing pages in the deck. One idea per page.

Online deck: [present/03-debye-shielding/](https://krystophny.github.io/plasma-skript/present/03-debye-shielding/).
The site build exports the same pages as SVG and PDF, with inline animations and offline caching.

## Page sequence

| Page | Title | Kind | Script section label | Lecturer cue |
|---|---|---|---|---|
| 1 | Title | static | debye-shielding | Screening opener. |
| 2 | Debye shielding | animation | intro-debye-shielding | Mobile electron rearrangement. |
| 3 | Boltzmann electrons | static | intro-debye-shielding | Potential energy has a minus sign. |
| 4 | Linear response | static | intro-debye-shielding | Weak potential expansion. |
| 5 | Screened Poisson equation | static | intro-debye-shielding | Close the field-response loop. |
| 6 | Yukawa potential | static | intro-debye-shielding | Boundary condition at infinity. |
| 7 | Charge separation scale | static | intro-debye-shielding | Thermal energy versus electrostatic cost. |
| 8 | Finite charge source | static | debye-finite-source | Geometry versus screening. |
| 9 | Finite source response | static | debye-finite-source | Match potential and radial field. |
| 10 | Debye sphere count | static | debye-collective-validity | Few versus many. |
| 11 | Weak coupling | static | debye-collective-validity | Nearest-neighbor energy. |
| 12 | Plasma regime map | static | debye-collective-validity | Both orderings are required. |
| 13 | Source credits | static | debye-shielding | Original figures. |

## Evidence and assets

2025 filled Chapter 1–5 pages 8–42 supply the coverage checklist only.
All diagrams and plots are original; plots share the Skript derivation source.
Animations use media/animations.json and retain their PDF posters.
Photo provenance, where applicable, is in photos/credits.md.

## Proposed particle animation

The incoming kin6d `debye-shielding-particles` scene reads case C4 data from
`animations/data/kin6d/debye-shielding-particles/`. It shows 6400 electrons in
a periodic one-component plasma, with $\Lambda=n\lambda_D^3=100$, around a
fixed repulsive charge. The normalized deficit $-\delta n_e/(\kappa n_0)$ [1]
approaches the periodic Debye response after time and ensemble averaging;
one snapshot does not reveal the screening cloud. The lecturer's pending
choice is to add this evidence after the point-charge derivation or replace
the opening schematic animation. The current LOOK deck keeps its selected
registered animations; this proposal changes no deck pages.
