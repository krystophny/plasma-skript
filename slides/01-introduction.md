# Introduction

LOOK deck; THINK work takes place on blank Goodnotes notebook pages.
No writing pages in the deck. One idea per page.

Online deck: [present/01-introduction/](https://krystophny.github.io/plasma-skript/present/01-introduction/).
The site build exports the same pages as SVG and PDF, with inline animations and offline caching.

## Page sequence

| Page | Title | Kind | Script section label | Lecturer cue |
|---|---|---|---|---|
| 1 | Title | static | introduction | Course opener. |
| 2 | Solar flare | photo | intro-plasma-state | Magnetic structure. |
| 3 | Aurora | photo | intro-plasma-state | Energetic particles. |
| 4 | H II region | photo | intro-plasma-state | Photoionization. |
| 5 | Hall thruster | photo | intro-plasma-state | Laboratory discharge. |
| 6 | Collective response | animation | intro-plasma-state | Predict rearrangement. |
| 7 | Quasineutrality | static | intro-plasma-state | Large-scale balance. |
| 8 | Example plasmas | static | intro-plasma-state | Locate physical objects. |
| 9 | Thermal motion | static | intro-speed-energy-temperature | Heating versus acceleration. |
| 10 | Thermal speed | static | intro-speed-energy-temperature | Speed peak versus component variance. |
| 11 | Temperature scales | static | intro-speed-energy-temperature | Energy and kelvin. |
| 12 | Characteristic scales | static | intro-scales | Compare with system length. |
| 13 | Plasma phenomena | static | intro-plasma-state | Transport and radiation. |
| 14 | Microscopic dynamics | static | intro-model-hierarchy | Coupled ODEs and Maxwell fields. |
| 15 | Distribution function | static | intro-model-hierarchy | Count particles in a phase-space cell. |
| 16 | Particles to moments | animation | intro-model-hierarchy | Information loss. |
| 17 | Model hierarchy | static | intro-model-hierarchy | "The easy one": particles, kinetic, fluid, MHD; name what each averaging step loses. |
| 18 | Map of plasma models | figure | intro-model-hierarchy | "The fun one": full-slide map, course route highlighted, circles mark kin6d (implemented, partial, planned); the figure links to the interactive map (`map/index.html?course=plasma`). Point to the two first principles, the route of this course and what it leaves to Kinetic Theory (BBGKY, collision operators), Fusion Physics (drift kinetics, transport) and research (quantum, radiation, reacting plasmas); click one arrow, e.g. two-fluid → resistive MHD. |
| 19 | Source credits | static | introduction | Provenance and disclosure. |

## Evidence and assets

2025 filled Chapter 1–5 pages 8–42 supply the coverage checklist only.
All diagrams and plots are original; plots share the Skript derivation source.
Animations use media/animations.json and retain their PDF posters.
Photo provenance, where applicable, is in photos/credits.md.
The model hierarchy is `hierarchy()` in `slides/intro-drawings.typ`.
The map of plasma models is the chapter-1 script figure, drawn by
`src/map.typ` from `map/plasma-models.yaml` and scaled to the page.
