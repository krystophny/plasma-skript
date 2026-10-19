# Debye shielding

LOOK deck; THINK work takes place on blank Goodnotes notebook pages.
No writing pages in the deck. One idea per page.

Online deck: [present/04-debye-shielding/](https://krystophny.github.io/plasma-skript/present/04-debye-shielding/).
The site build exports the same pages as SVG and PDF, with inline animations and offline caching.

## Page sequence

Delivery: title, whiteboard rigid sphere, charge-separation page, thermal
fluctuation animation, whiteboard coupling (neighbour energy versus k_B T),
coupling page, Debye number, regime map, ideal plasma, point-charge
animation, whiteboard Boltzmann derivation,
derivation overview, comparison page. The board plan is
`~/Nextcloud/lv/lecturer/plasma/board/04-debye-shielding.typ`.

| Page | Title | Kind | Script section label | Lecturer cue |
|---|---|---|---|---|
| 1 | Title | static | debye-shielding | Screening opener. |
| 2 | Charge separation | static | debye-collective-validity | Before the animation: electron-free sphere, last electron out, R of order lambda_D (2025 pp. 21-22). |
| 3 | Thermal charge fluctuations | animation | debye-collective-validity | After the rigid sphere: no test charge; thermal motion alone opens red/blue regions of size lambda_D (kin6d). |
| 4 | Weak and strong coupling | static | debye-collective-validity | After the whiteboard coupling: one particle versus many in the sphere; Gamma from the neighbour energy. |
| 5 | Debye number | static | debye-collective-validity | Rewrite weak coupling as N_D >> 1 (2025 pp. 39-40). |
| 6 | Plasma regime map | static | debye-collective-validity | Typical lambda_D and plasmas; N_D = 1 line. |
| 7 | Ideal plasma | static | debye-collective-validity | Exam question (g): N_D >> 1 and lambda_D << L (2025 pp. 41, 43). |
| 8 | Debye shielding from particles | animation | intro-debye-shielding | After the whiteboard physics; the cloud is an average, no hole in one snapshot. |
| 9 | Debye shielding | static | intro-debye-shielding | Read after the whiteboard derivation (2025 pp. 31-37): force balance, Poisson, linearize, a(r)/r, Debye-Hückel potential. |
| 10 | Charge separation and screening | static | intro-debye-shielding | Rigid sphere next to the point-charge response (2025 p. 38), Debye length. |
| 11 | Debye length and plasma frequency | static | intro-debye-shielding | Knowing v_th and omega_pe gives lambda_D (2025 p. 22); fusion example 10 keV, 1e20 m^-3. |

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
cloud. Page 8, after the plasma-parameter pages. It plays once, because
the average converges to its final state. The script shows it in §4.1.
