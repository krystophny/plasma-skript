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

## New visuals (2026-10-26)

Three Manim scenes (dark animation style, MP4 and poster registered in
`media/animations.json`, posters in `media/posters/`), all for the script
section `motion-nonuniform-fields`. The orbits are full Lorentz-force orbits
from a Boris push (`animations/drift_models.py`, numpy only), not drawn
paths. Conventions of the gyration scenes: ion Larmor radius $r_{Li}=1$,
reduced mass ratio $m_i/m_e=16$, $T_i=T_e$ (so $v_{\perp e}=4v_{\perp i}$ and
$r_{Le}=r_{Li}/4$), lengths in $r_{Li}$ [1], time $\Omega_it$ [1]. The drift
speeds on screen are the least-squares slope of the guiding centre
$\mathbf R=\mathbf x+(m/q)\,\mathbf v\times\mathbf B/B^2$; an independent RK4
integration in `scripts/check-physics.py` (`DriftOrbitPhysics`) gives the
same numbers.

**`grad-b-drift`** (`animations/grad_b_drift.py`, 20 s, plays once; after
the static grad-B page 15).
- Computed: ion and electron in $\mathbf B=B_0(1+y/L)\,\hat{\mathbf z}$,
  $L=10\,r_{Li}$, guiding centres start at the origin, 10 ion periods.
- Shown: $x/r_{Li}$, $y/r_{Li}$ [1]; B out of the page, symbols grow with $B$;
  $\nabla B$ arrow; ion loops step to $-x$ (smaller radius where $B$ is larger),
  electron band moves to $+x$; white dots and dashed lines are the guiding
  centres.
- Numbers on screen, $v_x/(r_{Li}\Omega_i)$ [1], orbit against
  $-\mu\,\partial_yB/(qB^2)$: ion $-0.0506$ against $-0.0500$ (+1.3 %),
  electron $+0.0501$ against $+0.0500$ (+0.1 %). The deviation is the
  second-order finite-Larmor-radius correction: it scales as $(r_L/L)^2$
  (ion and electron differ by $4^2$). At equal $T$ the speed does not depend
  on mass; the sign of $q$ sets the direction.

**`curvature-drift`** (`animations/curvature_drift.py`, 20 s; after the static
curvature page 16).
- Computed: both species in the toroidal vacuum field
  $\mathbf B=B_0R_0/R\,\hat{\boldsymbol\varphi}$, $R_0=40\,r_{Li}$, start on the
  midplane with $v_\parallel=v_\perp$, run for the time in which the ion goes
  half-way round the torus (the electron, with $v_{\parallel e}=4v_{\parallel i}$,
  goes round twice).
- Shown: poloidal plane, $(R-R_0)/r_{Li}$ and $Z/r_{Li}$ [1]; clock: toroidal
  angle of the ion $\varphi$ [1]. The ion drifts up, the electron down, with no
  radial displacement: charge separation that a purely toroidal field cannot
  hold, the motivation for the rotational transform.
- Numbers on screen, $v_Z/(r_{Li}\Omega_i)$ [1], orbit against
  $(m/qBR)(v_\parallel^2+\tfrac12v_\perp^2)$: ion $+0.0381$ against $+0.0375$
  (+1.6 %), electron $-0.0373$ against $-0.0375$ ($-0.4$ %). The deviation is
  first order in $r_L/R_0$ (it halves when $R_0$ doubles and does not change
  with the time step).

**`magnetic-mirror`** (`animations/magnetic_mirror.py`, 24 s; after the
loss-cone page 18).
- Computed: six ions of equal speed $v$, midplane pitch angles
  $18^\circ,26^\circ,29^\circ,31^\circ,45^\circ,70^\circ$, in
  $B_z=B_0[1+(R_m-1)(z/L)^2]$, $B_r=-\tfrac r2\,\partial_zB_z$ (divergence
  free), $R_m=4$, $L=30\,r_{L0}$ with $r_{L0}=v/\Omega_0$, each on its own field
  line; an ion counts as lost when it passes the field maximum $|z|=L$.
- Shown: $x/L$ against $z/L$ [1] at equal scale with the field lines; filled dot
  reflected, open ring lost at the throat. Critical angle from
  $\sin^2\alpha_c=1/R_m$: $30^\circ$; the $29^\circ$ and $31^\circ$ ions sit on
  either side and behave accordingly. Lower left $B/B_0$ [1] against $z/L$ [1];
  lower right the gyro-averaged $\mu/\mu_{\rm start}$ [1] against $vt/L$ [1].
- Numbers: $\mu$ stays constant within 0.3 % for the reflected ions over
  $vt/L=6$ and within 1.6 % for the escaping ones; the reflection points lie
  at 0.97 to 0.99 of the guiding-centre value
  $z_b=L\sqrt{(1/\sin^2\alpha-1)/(R_m-1)}$.
