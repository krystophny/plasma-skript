# Debye shielding

LOOK deck; THINK work takes place on blank Goodnotes notebook pages.
No writing pages in the deck. One idea per page.

Online deck: [present/04-debye-shielding/](https://krystophny.github.io/plasma-skript/present/04-debye-shielding/).
The site build exports the same pages as SVG and PDF, with inline animations and offline caching.

## Page sequence

Delivery: title, whiteboard physics (rigid sphere, then Boltzmann response),
charge-separation page, animation, whiteboard derivation, derivation overview, comparison page.

| Page | Title | Kind | Script section label | Lecturer cue |
|---|---|---|---|---|
| 1 | Title | static | debye-shielding | Screening opener. |
| 2 | Charge separation | static | intro-debye-shielding | Before the animation: electron-free sphere, last electron out, R of order lambda_D (2025 pp. 21-22). |
| 3 | Debye shielding from particles | animation | intro-debye-shielding | After the whiteboard physics; the cloud is an average, no hole in one snapshot. |
| 4 | Debye shielding | static | intro-debye-shielding | Read after the whiteboard derivation (2025 pp. 31-37): force balance, Poisson, linearize, a(r)/r, Debye-Hückel potential. |
| 5 | Charge separation and screening | static | intro-debye-shielding | Rigid sphere next to the point-charge response (2025 p. 38), Debye length. |
| 6 | Debye length and plasma frequency | static | intro-debye-shielding | Knowing v_th and omega_pe gives lambda_D (2025 p. 22); fusion example 10 keV, 1e20 m^-3. |
| 7 | Plasma parameter | static | debye-collective-validity | From weak coupling (2025 pp. 39-40): mean spacing, e^2/(4 pi eps0 a) << kT, N_D >> 1. |
| 8 | Debye sphere count | static | debye-collective-validity | Few versus many. |
| 9 | Plasma regime map | static | debye-collective-validity | Typical lambda_D and plasmas; N_D = 1 line. |
| 10 | Ideal plasma | static | debye-collective-validity | Exam question (g): N_D >> 1 and lambda_D << L (2025 pp. 41, 43). |

Rebuilt from scratch on 2026-10-13. The 2025 fluid preliminaries (pp. 25-30:
conservation laws, Euler and Lagrange derivatives) are saved for the moments
chapter (chapter 7); this deck keeps the force balance that gives Boltzmann. Optional later kin6d job: net-charge
fluctuations in spheres of radius R from the same runs (sqrt(N) for R << lambda_D,
suppressed for R >~ lambda_D).

## Evidence and assets

2025 filled Chapter 1–5 pages 8–42 supply the coverage checklist only.
All diagrams and plots are original; plots share the Skript derivation source.
Animations use media/animations.json and retain their PDF posters.
Photo provenance, where applicable, is in photos/credits.md.

## Particle animation

The kin6d `debye-shielding-particles` scene reads case C4 data from
`animations/data/kin6d/debye-shielding-particles/`. It shows 6400 electrons in
a periodic one-component plasma, with $n\lambda_D^3=100$ ($N_D\approx 420$),
around a fixed repulsive charge. The normalized deficit
$-\delta n_e/(\kappa n_0)$ [1] approaches the periodic Debye response after
time and ensemble averaging; one snapshot does not reveal the screening
cloud. Page 3, after the charge-separation page. It plays once, because
the average converges to its final state. The script shows it in §4.1.
