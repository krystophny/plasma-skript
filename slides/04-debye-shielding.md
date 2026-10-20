# Debye shielding

LOOK deck; THINK work takes place on blank Goodnotes notebook pages.
No writing pages in the deck. One idea per page.

Online deck: [present/04-debye-shielding/](https://krystophny.github.io/plasma-skript/present/04-debye-shielding/).
The site build exports the same pages as SVG and PDF, with inline animations and offline caching.

## Page sequence

Delivery: title, whiteboard rigid sphere, charge-separation page, thermal
fluctuation animation, coupling-regions animation, whiteboard coupling (neighbour
energy versus k_B T), coupling page, Debye number, regime map, ideal plasma, point-charge
animation, whiteboard Boltzmann derivation,
derivation overview, comparison page, Debye-circle animation, Debye length and
plasma frequency. The board plan is
`~/Nextcloud/lv/lecturer/plasma/board/04-debye-shielding.typ`.

| Page | Title | Kind | Script section label | Lecturer cue |
|---|---|---|---|---|
| 1 | Title | static | debye-shielding | Screening opener. |
| 2 | Charge separation | static | debye-collective-validity | Before the animation: electron-free sphere, last electron out, R of order lambda_D (2025 pp. 21-22). |
| 3 | Thermal charge fluctuations | animation | debye-collective-validity | After the rigid sphere: no test charge; thermal motion alone opens red/blue regions of size lambda_D (kin6d). |
| 4 | Coupling regions | animation | debye-collective-validity | Same density, T_0 versus 9 T_0 (kin6d): red/blue regions of size lambda_D = a with one or a few electrons versus lambda_D = 3a with many; freeze; one electron runs through, strongly deflected versus nearly straight. No Debye circle. |
| 5 | Weak and strong coupling | static | debye-collective-validity | After the whiteboard coupling: the frozen frame of page 4 (same electrons, colours, scale), Gamma_e = a^2/(4 pi lambda_D^2) from the neighbour energy. |
| 6 | Debye number | static | debye-collective-validity | Rewrite weak coupling as N_D >> 1 (2025 pp. 39-40). |
| 7 | Plasma regime map | static | debye-collective-validity | Typical lambda_D and plasmas; N_D = 1 line. |
| 8 | Ideal plasma | static | debye-collective-validity | Exam question (g): N_D >> 1 and lambda_D << L (2025 pp. 41, 43). |
| 9 | Debye shielding from particles | animation | intro-debye-shielding | After the whiteboard physics; the cloud is an average, no hole in one snapshot. |
| 10 | Debye shielding | static | intro-debye-shielding | Read after the whiteboard derivation (2025 pp. 31-37): force balance, Poisson, linearize, a(r)/r, Debye-Hückel potential. |
| 11 | Charge separation and screening | static | intro-debye-shielding | Rigid sphere next to the point-charge response (2025 p. 38), Debye length. |
| 12 | Coupling test particles | animation | intro-debye-shielding | After the shielded point charge: same frozen electrons at Gamma_e = 0.08 (lambda_D = a) and 0.009 (lambda_D = 3a); the Debye circle moves with the test electron; few versus many electrons inside. |
| 13 | Debye length and plasma frequency | static | intro-debye-shielding | Knowing v_th and omega_pe gives lambda_D (2025 p. 22); fusion example 10 keV, 1e20 m^-3. |

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

## Thermal fluctuation animation

The kin6d `thermal-charge-fluctuations` scene
(`animations/thermal_charge_fluctuations.py`) reads
`animations/data/kin6d/thermal-charge-fluctuations/`: 6480 electrons in a
periodic one-component plasma of edge $6\lambda_D$, $n\lambda_D^3=30$, in
equilibrium and without a test charge. The colour field is the net charge
density $\rho/(e n_0)$ [1] in the plane $z=0$, from the same electrons
smoothed with a Gaussian of width $\sigma=0.4\lambda_D$: red where electrons
are missing ($\rho>0$), blue where they crowd ($\rho<0$). The dots are the
electrons of the slab $|z|<0.4\lambda_D$; a bar shows $\lambda_D$. Patches
of size $\sim\lambda_D$ and amplitude $\sim 0.1\,e n_0$ appear and dissolve
within a few $1/\omega_p$. Page 3, after the rigid-sphere estimate. It loops.
The script shows it in §4.1.

## Coupling-regions animation

The kin6d `coupling-regions` scene (`animations/coupling_regions.py`) reads
`animations/data/kin6d/coupling-regions/{strong,weak}/`: two periodic
one-component plasmas of 5832 electrons in the same cube of edge $18a$, so
the same $n_0$ and $\omega_p$, at $T_e=T_0$ ($n\lambda_D^3=1$, $\lambda_D=a$,
$\Gamma_e=0.08$) and $T_e=9T_0$ ($n\lambda_D^3=27$, $\lambda_D=3a$,
$\Gamma_e=0.009$), with $\lambda_D/a=(4\pi\Gamma_e)^{-1/2}$. Colour: net
charge density in $z=0$ smoothed with a Gaussian of width $\lambda_D/2$
(colour map of the thermal-fluctuation scene, each panel scaled to its own
rms), dots the electrons of $|z|<a/2$. The electrons move for
$12/\omega_p$, the picture freezes, and one electron per panel runs through
the frozen charges at $v_{th}=\sqrt{2k_BT_e/m_e}$ for $8/\omega_p$: deflected
by about $1$ rad at strong coupling, nearly straight (and out of the panel
after $4/\omega_p$) at weak coupling. Page 5 shows the frozen frame from
`slides/coupling-regions.json` and `slides/coupling-regions-{0,1}.png`
(`scripts/export-coupling-still.py`). Page 4, before the whiteboard
coupling. The script shows it in §4.1.

## Debye-circle animation

The `coupling-test-particle` scene (`animations/coupling_test_particle.py`)
sends a test electron at the thermal speed through the same frozen electrons
on a uniform positive background, side by side at $\Gamma_e=0.08$
($\lambda_D\approx a$) and $\Gamma_e=0.009$ ($\lambda_D\approx 3a$). A circle
of radius $\lambda_D$ moves with the test electron; drawn electrons inside it
are blue (about 3 versus 28), the others grey. Lengths are in units of the
mean spacing $a$ [1], time is $t v_{th}/a$ [1]. Page 12, after the shielded
point charge and $\lambda_D$. The script shows it after the screened point
charge in §4.2.

## Particle animation

The kin6d `debye-shielding-particles` scene reads case C4 data from
`animations/data/kin6d/debye-shielding-particles/`. It shows 6400 electrons in
a periodic one-component plasma, with $n\lambda_D^3=100$ ($N_D\approx 420$),
around a fixed repulsive charge. The normalized deficit
$-\delta n_e/(\kappa n_0)$ [1] approaches the periodic Debye response after
time and ensemble averaging; one snapshot does not reveal the screening
cloud. Page 9, after the plasma-parameter pages. It plays once, because
the average converges to its final state. The script shows it in §4.1.
