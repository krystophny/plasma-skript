# Single-particle motion

LOOK deck; THINK work takes place on blank Goodnotes notebook pages.
No writing pages in the deck. One idea per page.

Online deck: [present/05-single-particle-motion/](https://krystophny.github.io/plasma-skript/present/05-single-particle-motion/).
The site build exports the same pages as SVG and PDF, with inline animations and offline caching.

## Page sequence

Delivery (2026-10-20): title, whiteboard force balance and equations of
motion (board plan pages 2-3, in the board notation $r_L$, $\omega_c$,
$\varphi$), gyration summary, the three gyration animations, the scale
tables, then the drifts, guiding centre, magnetic moment, mirror and
polarization summaries of the rest of chapter 5. The script writes the
Larmor radius as $\rho$ and the signed frequency as $\Omega = qB/m$.

| Page | Title | Kind | Script section label | Lecturer cue |
|---|---|---|---|---|
| 1 | Title | static | single-particle-motion | Charged particles in prescribed fields. |
| 2 | Gyration: force balance | board plan | motion-lorentz | Lorentz force, circular orbit, centrifugal balance gives omega_c and r_L. |
| 3 | Equations of motion | board plan | motion-lorentz | B along z, differentiate once more, harmonic oscillator, integrate to the circle, add v_par. |
| 4 | Gyration | static | motion-lorentz | Summary: frequency, radius, circle, helix; ions clockwise, electrons counterclockwise (B out of the page), diamagnetic. Chen (2016) ch. 2. |
| 5 | Ion and electron gyration | animation | motion-lorentz | Reduced mass ratio 16 at equal T: r_Li/r_Le = 4, 16 electron turns per ion turn. Loops. |
| 6 | Gyration components | animation | motion-lorentz | v_x = v_perp cos, x - x_0 = r_L sin next to the ion circle. |
| 7 | Helix | animation | motion-lorentz | v_par != 0, pitch 2 pi v_par/omega_c = 1.1 r_L. |
| 8 | Typical gyrofrequencies and Larmor radii | static | motion-lorentz | Electrons and protons at 1 and 5 T, 10 eV and 10 keV (derivations/build/gyration.json). |
| 9 | Thermonuclear scales | static | motion-lorentz | Exam (j): omega_ce, omega_pe, omega_ci; r_Li, lambda_D, r_Le at 5 T, 1e20 m^-3, 1e8 K. |
| 10 | Magnetized plasma | static | motion-lorentz | r_L << L and omega_c tau >> 1. |
| 11 | E x B drift | static | motion-exb | Same drift for both species; frame where E' = 0. |
| 12 | General force drift | static | motion-exb | F x B/(qB^2); gravity drift and its current. |
| 13 | Guiding centre | static | motion-guiding-center | r = R + rho; ordering r_L/L << 1, omega/omega_c << 1. |
| 14 | Magnetic moment | static | motion-guiding-center | mu = I S = m v_perp^2/(2B), adiabatic invariant; flux through the orbit. |
| 15 | Grad-B drift | static | motion-nonuniform-fields | Smaller orbit where B is stronger; opposite drifts. |
| 16 | Curvature drift | static | motion-nonuniform-fields | Centrifugal force; combined vacuum-field drift. |
| 17 | Magnetic mirror | static | motion-nonuniform-fields | Mirror force, energy, reflection point. |
| 18 | Mirror ratio and loss cone | static | motion-nonuniform-fields | sin^2 alpha_c = 1/R_m. |
| 19 | Polarization drift | static | motion-polarization | Slowly varying E_perp; polarization current carried by ions. |
| 20 | Drifts | static | (none) | Table: charge and mass dependence of every drift. |

## Evidence and assets

The 2025 filled notes (Chapter 1-5, pp. 43-48) supply the coverage checklist
and the board notation; no whiteboard export of 2026-10-20 was available in
the Goodnotes backup when the deck was built. All sketches are original
(`slides/motion-drawings.typ`). The scale tables are computed by
`derivations/chapters/ch05_single_particle_motion.py` into
`derivations/build/gyration.json` and checked independently, against a
Boris integration of the Lorentz force, in `scripts/check-physics.py`
(`GyrationPhysics`). Reference: F. F. Chen, Introduction to Plasma Physics
and Controlled Fusion, 3rd ed., Springer (2016), doi:10.1007/978-3-319-22309-4.

## Gyration animations

`animations/gyration.py` holds three scenes on the board solution
$x = x_0 + r_L \sin(\omega_c t + \varphi)$, $y = y_0 \pm r_L \cos(\omega_c t + \varphi)$:
`gyration-top-view` (ion and electron, B out of the page, $m_i/m_e = 16$
stated on screen with the hydrogen value 1836, $T_i = T_e$, clock
$\omega_{ci} t$ [1]), `gyration-components` (ion circle beside $v_x/v_\perp$
and $(x - x_0)/r_L$ against $\omega_c t$ [1]) and `gyration-helix` (oblique
projection, pitch $1.1\,r_L$). The script shows all three in §5.1.
