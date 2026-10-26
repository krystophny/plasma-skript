# Single-particle motion

LOOK deck; THINK work takes place on blank Goodnotes notebook pages.
No writing pages in the deck. One idea per page.

Online deck: [present/05-single-particle-motion/](https://krystophny.github.io/plasma-skript/present/05-single-particle-motion/).
The site build exports the same pages as SVG and PDF, with inline animations and offline caching.

## Page sequence

Route (rebuilt 2026-10-26): one derivation-overview page per topic, in the
lecturer's notation of 2024/25 (species index $\alpha$, signed
$\omega_c = q_\alpha B/m_\alpha$, Larmor radius $\rho_L = v_\perp/|\omega_c|$,
gyrophase $\varphi$, $\mathbf b = \mathbf B/B$, drifts $\mathbf v_D$,
curvature with $R_c$ and $\mathbf e_R$ pointing away from the centre of
curvature, $(\mathbf b\cdot\nabla)\mathbf b = -\mathbf e_R/R_c$), each next to
its animation. Corrected against his notes: $v_y = -v_\perp\sin(\omega_c t + \varphi)$
with signed $\omega_c$; ions rotate clockwise for $\mathbf B$ out of the page.
Section numbers follow the script; the topic order makes them alternate
between 5.3 and 5.4 (guiding centre, curvature, moment, mirror force, the
three $\mu$ pages and the Hamiltonian page, mirror).

| Page | Title | Kind | Script section label | Lecturer cue |
|---|---|---|---|---|
| 1 | Title | static | single-particle-motion | Charged particles in prescribed fields. |
| 2 | Gyration: force balance | derivation | motion-lorentz | Centrifugal force m v_perp^2/rho_L against Lorentz force abs(q) v_perp B gives abs(omega_c) and rho_L; omega_c itself is signed. |
| 3 | Equations of motion | derivation | motion-lorentz | Components for B = B e_z, differentiate once more: harmonic oscillator; solution with signed omega_c (v_y has the minus sign); integrate to the circle, add v_par for the helix; ions clockwise. Chen (2016) ch. 2. |
| 4 | Ion and electron gyration | animation | motion-lorentz | Reduced mass ratio 16 at equal T: rho_Li/rho_Le = 4, 16 electron turns per ion turn. Loops. |
| 5 | Gyration components | animation | motion-lorentz | v_x = v_perp cos, x - x_0 = rho_L sin next to the ion circle. |
| 6 | Helix | animation | motion-lorentz | v_par != 0, pitch 2 pi v_par/omega_c = 1.1 rho_L. |
| 7 | Typical gyrofrequencies and Larmor radii | static | motion-lorentz | Electrons and protons at 1 and 5 T, 10 eV and 10 keV (derivations/build/gyration.json). |
| 8 | Thermonuclear scales | static | motion-lorentz | Exam (j): omega_ce, omega_pe, omega_ci; rho_Li, lambda_D, rho_Le at 5 T, 1e20 m^-3, 1e8 K. |
| 9 | Magnetized plasma | static | motion-lorentz | rho_L << L and abs(omega_c) tau >> 1. |
| 10 | E x B drift | derivation | motion-exb | His ansatz v = v_par b + v_perp(t) + v_D, "assume" pure gyration for v_perp, remainder 0 = E_perp + v_D x B, cross with B. Then: in the frame moving with v_D, E' = 0, so the ansatz is an exact Galilean transformation (E perp B, E/B << c); E_par accelerates freely. |
| 11 | E x B drift | animation | motion-exb | Same drift for both signs; larger radius on the half orbit where the ion gained energy. |
| 12 | E x B drift in the drift frame | animation | motion-exb | Same ion orbit twice: lab frame, looped trochoid drifting with v_D; then the frame moving with v_D = E x B/B^2, where E' = E + v_D x B = 0 and the orbit is a circle. The ansatz of page 10 is an exact frame change. |
| 13 | General force drift | derivation | motion-exb | Replace q E by F: v_D = (F/q) x B/B^2; F = q E is the special case without charge separation; gravity drift opposite for ions and electrons, current n (m_i + m_e) g x B/B^2. |
| 14 | Gravity drift | animation | motion-exb | F = m g in the force drift: ion and electron drift opposite, the electron 16 times slower (reduced mass ratio on screen); measured against (m/q) g x B/B^2. |
| 15 | Guiding centre | static | motion-guiding-center | r = R + rho; ordering rho_L/L << 1, omega/abs(omega_c) << 1. |
| 16 | Curvature drift | derivation | motion-nonuniform-fields | Guiding centre follows the curved line with v_par: centripetal acceleration v_par^2/R_c, centrifugal force m v_par^2 e_R/R_c into the force drift. Mnemonic v_D = rho_par Omega_par. |
| 17 | Curvature drift | animation | motion-nonuniform-fields | Ion up, electron down in a purely toroidal field. |
| 18 | Magnetic moment | derivation | motion-guiding-center | mu = I S = m v_perp^2/(2B); current left-handed about B for both species: diamagnetic. |
| 19 | Mirror force and grad-B drift | derivation | motion-nonuniform-fields | div B = 0 gives B_r = -(r/2) dB_z/dz near the axis; gyro-average q (v x B)_z gives F_par = -mu dB/ds; general F = -mu grad B; its perpendicular part in the force drift is the grad-B drift. |
| 20 | Grad-B drift | animation | motion-nonuniform-fields | Smaller orbit where B is stronger; opposite drifts. |
| 21 | Energy conservation | derivation | motion-guiding-center | Magnetic force does no work; with m v_perp^2/2 = mu B the energy reads m v_par^2/2 + mu B + q Phi = W, exact in static fields. |
| 22 | mu from Faraday's law | derivation | motion-guiding-center | Heyn's route in SI: work of the induced E over one turn, Stokes, delta(m v_perp^2/2) = mu delta B, so delta mu = 0. Assumptions on the page. |
| 23 | mu in a slowly growing field | animation | motion-guiding-center | B ramps from B_0 to 2B_0 over about 20 turns, induced E clockwise: orbit shrinks as B^-1/2, flux pi rho_L^2 B and mu stay constant. Faraday route of page 22 in motion; numerics of the plot on page 26. |
| 24 | mu from the mirror force | derivation | motion-guiding-center | Multiply the mirror force by v_par, compare with energy conservation: B dmu/dt = 0; mirror point where B = W/mu; "adiabatic invariant". |
| 25 | mu in the Hamiltonian picture | derivation | motion-guiding-center | Action of the gyration J = oint (m v_perp + q A).dl = 2 pi m v_perp rho_L - pi abs(q) B rho_L^2 = (2 pi m/abs(q)) mu, abs(q) times the flux through the orbit; actions of periodic motions are adiabatic invariants (slowly shortened pendulum, Einstein and Lorentz, Solvay 1911); guiding-centre H = m v_par^2/2 + mu B(R) + q Phi(R) as on his 2025 slides (pp. 15-16); gyrophase ignorable, p_phi = (m/q) mu conserved (Noether), as in his 2024 slides (Chapter 1-5, pp. 61-66, guiding-centre Lagrangian) and the 2021 recording "#9 Guiding-Center Lagrangian"; mu B is the potential for the mirror force and the grad-B drift. Exact in the guiding-centre model, which is an expansion in rho_L/L. |
| 26 | Adiabatic invariance | plot | motion-guiding-center | Boris orbit in B_0 -> 2B_0 with the induced E: smooth (tanh) ramp, change of mu falls exponentially with tau; linear ramp with kinks only algebraically (about tau^-2, two kinks interfere). |
| 27 | Magnetic mirror | animation | motion-nonuniform-fields | Six pitch angles; 29 deg lost, 31 deg reflected for R_m = 4. |
| 28 | Mirror ratio and loss cone | derivation | motion-nonuniform-fields | sin^2 alpha/B = const. from mu and energy; trapped if B_0/sin^2 alpha_0 < B_max: sin^2 alpha_c = 1/R_m (not in his notes; derived on the page). |
| 29 | Loss cone in velocity space | plot | motion-nonuniform-fields | Isotropic sample at the midplane, R_m = 4: lost particles fill the cone sin^2 alpha < 1/R_m around v_par; isotropic lost fraction 1 - sqrt(1 - 1/R_m), 13 % at R_m = 4. |
| 30 | Polarization drift | static | motion-polarization | Slowly varying E_perp; polarization current carried by ions. |
| 31 | Polarization drift | animation | motion-polarization | E_perp switched on over three ion turns; view with the common E x B displacement removed: ion guiding centre moves along E by m E_1/(q B^2), electron 16 times less and opposite. |
| 32 | Drifts | static | (none) | Table: charge and mass dependence of every drift; vacuum-field sum of curvature and grad-B. |
| 33 | Cyclotron resonance | derivation | motion-cyclotron-resonance | Rotating field E_cw = E_0 e^(-i s omega t); v_cw = v_x + i v_y obeys dv_cw/dt = -i omega_c v_cw + (q/m) E_cw (the script's equation); from rest the modulus 2 abs(sin(Delta t/2)/Delta), Delta = omega_c - s omega; Delta = 0: v_perp grows linearly, W quadratically. Ions take the clockwise, electrons the counterclockwise field (signed omega_c). |
| 34 | Cyclotron resonance | animation | motion-cyclotron-resonance | Predict each run before it starts: ion with the clockwise field at omega_ci (spiral, straight line in v_perp), at 0.8 omega_ci (beat, peak 10 E_0/B), with the counterclockwise field (nothing), electron with the counterclockwise field (resonance again). Measured slope 0.9999 abs(q) E_0/m against 1. |

## Evidence and assets

Notation and routes follow the lecturer's 2024/25 slides (Chapter 1-5) and
his lecture notes on particle dynamics and drift orbits; the Faraday route
for mu is from the notes, rewritten in SI. All sketches are original
(`slides/motion-drawings.typ`). Every formula of the derivation pages is
checked in `derivations/chapters/ch05_single_particle_motion.py` (sections
"Deck: ..."). The scale tables are computed by the same file into
`derivations/build/gyration.json` and checked independently, against a
Boris integration of the Lorentz force, in `scripts/check-physics.py`
(`GyrationPhysics`). Reference: F. F. Chen, Introduction to Plasma Physics
and Controlled Fusion, 3rd ed., Springer (2016), doi:10.1007/978-3-319-22309-4.

## Gyration animations

`animations/gyration.py` holds three scenes on the board solution
$x = x_0 + (v_\perp/\omega_c) \sin(\omega_c t + \varphi)$,
$y = y_0 + (v_\perp/\omega_c) \cos(\omega_c t + \varphi)$:
`gyration-top-view` (ion and electron, B out of the page, $m_i/m_e = 16$
stated on screen with the hydrogen value 1836, $T_i = T_e$, clock
$\omega_{ci} t$ [1]), `gyration-components` (ion circle beside $v_x/v_\perp$
and $(x - x_0)/\rho_L$ against $\omega_c t$ [1]) and `gyration-helix` (oblique
projection, pitch $1.1\,\rho_L$). The script shows all three in §5.1. All
chapter-5 scenes were re-rendered on 2026-10-26 in the deck notation
($\rho_L$, $\rho_{Li}$, $\omega_{ci}$, $\mathbf v_D$, $q_\alpha$, $m_\alpha$);
only labels changed, not the physics, parameters or layout.

## Adiabatic-invariance plot (2026-10-26)

`derivations/plot_mu_ramp.py` writes `build/fig/mu_ramp.svg` (page 26).
Normalized $q_\alpha = m_\alpha = 1$, $B_0 = 1$: time $\omega_{c0}t$ [1],
lengths $\rho_{L0}$ [1]. Uniform $B(t)$ from $B_0$ to $2B_0$ with the induced
field $\mathbf E = -\tfrac12\dot B\,\mathbf e_z\times\mathbf r$; orbit centred on
the axis (gyrophase-independent). Smooth ramp $B/B_0 = 3/2 + \tanh(t/\tau)/2$,
linear ramp with kinks at $t = \pm\tau$, same largest slope. Boris push,
1600 steps per turn, exact discrete start circle, $\mathbf E$ from the field
increment over each step. Plotted $\mu_\mathrm{final}/\mu_\mathrm{initial}-1$ [1]
(non-negative: on the axis a non-adiabatic change only shifts the guiding
centre off the axis). Values: tanh $1.1\times10^{-1}$, $3.0\times10^{-2}$,
$2.0\times10^{-3}$, $5.0\times10^{-6}$, $1.0\times10^{-8}$, $2.0\times10^{-11}$
at $\omega_{c0}\tau = 0.25, 1, 2, 4, 6, 8$; linear $1.2\times10^{-1}$,
$5.8\times10^{-2}$, $5.9\times10^{-3}$, $2.0\times10^{-3}$,
$1.1\times10^{-3}$, $7.7\times10^{-4}$. Checked against DOP853 in
`derivations/test_chapters.py` (`test_mu_ramp_boris_against_dop853`).

## New visuals (2026-10-26)

Three Manim scenes (dark animation style, MP4 and poster registered in
`media/animations.json`, posters in `media/posters/`), all for the script
section `motion-nonuniform-fields`; four further scenes and a plot follow
below ("Field-change visuals"). Labels re-rendered in the deck notation. The orbits are full Lorentz-force orbits
from a Boris push (`animations/drift_models.py`, numpy only), not drawn
paths. Conventions of the gyration scenes: ion Larmor radius $\rho_{Li}=1$,
reduced mass ratio $m_i/m_e=16$, $T_i=T_e$ (so $v_{\perp e}=4v_{\perp i}$ and
$\rho_{Le}=\rho_{Li}/4$), lengths in $\rho_{Li}$ [1], time $\omega_{ci}t$ [1]. The drift
speeds on screen are the least-squares slope of the guiding centre
$\mathbf R=\mathbf x+(m_\alpha/q_\alpha)\,\mathbf v\times\mathbf B/B^2$; an independent RK4
integration in `scripts/check-physics.py` (`DriftOrbitPhysics`) gives the
same numbers.

**`grad-b-drift`** (`animations/grad_b_drift.py`, 20 s, plays once; after
the mirror-force page 19).
- Computed: ion and electron in $\mathbf B=B_0(1+y/L)\,\hat{\mathbf z}$,
  $L=10\,\rho_{Li}$, guiding centres start at the origin, 10 ion periods.
- Shown: $x/\rho_{Li}$, $y/\rho_{Li}$ [1]; B out of the page, symbols grow with $B$;
  $\nabla B$ arrow; ion loops step to $-x$ (smaller radius where $B$ is larger),
  electron band moves to $+x$; white dots and dashed lines are the guiding
  centres.
- Numbers on screen, $v^{\nabla B}_{D,x}/(\rho_{Li}\omega_{ci})$ [1], orbit against
  $-\mu\,\partial_yB/(q_\alpha B)$: ion $-0.0506$ against $-0.0500$ (+1.3 %),
  electron $+0.0501$ against $+0.0500$ (+0.1 %). The deviation is the
  second-order finite-Larmor-radius correction: it scales as $(\rho_L/L)^2$
  (ion and electron differ by $4^2$). At equal $T$ the speed does not depend
  on mass; the sign of $q_\alpha$ sets the direction.

**`curvature-drift`** (`animations/curvature_drift.py`, 20 s; after the
curvature page 16).
- Computed: both species in the toroidal vacuum field
  $\mathbf B=B_0R_0/R\,\hat{\boldsymbol\varphi}$, $R_0=40\,\rho_{Li}$, start on the
  midplane with $v_\parallel=v_\perp$, run for the time in which the ion goes
  half-way round the torus (the electron, with $v_{\parallel e}=4v_{\parallel i}$,
  goes round twice).
- Shown: poloidal plane, $(R-R_0)/\rho_{Li}$ and $Z/\rho_{Li}$ [1]; clock: toroidal
  angle of the ion $\varphi$ [1]. The ion drifts up, the electron down, with no
  radial displacement: charge separation that a purely toroidal field cannot
  hold, the motivation for the rotational transform.
- Numbers on screen, $v_{D,Z}/(\rho_{Li}\omega_{ci})$ [1], orbit against
  $(m_\alpha/q_\alpha BR)(v_\parallel^2+\tfrac12v_\perp^2)$: ion $+0.0381$ against $+0.0375$
  (+1.6 %), electron $-0.0373$ against $-0.0375$ ($-0.4$ %). The deviation is
  first order in $\rho_L/R_0$ (it halves when $R_0$ doubles and does not change
  with the time step).

**`magnetic-mirror`** (`animations/magnetic_mirror.py`, 24 s; page 27,
before the loss-cone page 28).
- Computed: six ions of equal speed $v$, midplane pitch angles
  $18^\circ,26^\circ,29^\circ,31^\circ,45^\circ,70^\circ$, in
  $B_z=B_0[1+(R_m-1)(z/L)^2]$, $B_r=-\tfrac r2\,\partial_zB_z$ (divergence
  free), $R_m=4$, $L=30\,\rho_{L0}$ with $\rho_{L0}=v/\omega_{c0}$, each on its own field
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

## Field-change visuals (2026-10-26)

Four further Manim scenes and one plot. The scenes use a Boris push with
time-dependent fields (`animations/drift_models.py`, `boris_em`), started on
the exact discrete gyro-circle of the scheme so that the guiding centre is
known at $t=0$. Ion and electron have $|q_\alpha|=1$, the reduced mass ratio
$m_i/m_e=16$ (stated on screen with the hydrogen value) and $T_i=T_e$.
`scripts/check-physics.py` (`FieldChangePhysics`) repeats every number with
an independent RK4 integration and gyro-period averages.

**`exb-frame-change`** (`animations/exb_frame.py`, 25 s; page 12, after the
E x B derivation page 10 and the `exb-drift` scene).
- Computed: one ion in $\mathbf B=B\,\mathbf e_z$, $\mathbf E=E\,\mathbf e_y$,
  $E/B=0.4\,u$ with $u$ the gyration speed in the drift frame; $\rho_L=u/\omega_c$;
  three turns, 400 steps per turn.
- Shown, one after the other in the same axes ($x/\rho_L$, $y/\rho_L$ [1]):
  the lab frame, a looped trochoid drifting along $+x$ with the $\mathbf v_D$
  arrow; then $(x-v_Dt)/\rho_L$ [1], the frame moving with
  $\mathbf v_D=\mathbf E\times\mathbf B/B^2$, labelled
  $\mathbf E'=\mathbf E+\mathbf v_D\times\mathbf B=0$, where the orbit is a circle.
- Numbers on screen: drift from a least-squares fit
  $c+vt+a\cos\omega t+b\sin\omega t$ of the lab orbit, $v_{D,x}/(\rho_L\omega_c)=0.400000$
  against $E/(B\rho_L\omega_c)=0.400000$ (agree to $10^{-12}$); drift-frame radius
  constant to $3\times10^{-14}$ (round-off; the mean radius is $u/\omega_c$ to
  $3\times10^{-5}$, the $O(\Delta t^2)$ radius of the discrete circle).

**`gravity-drift`** (`animations/gravity_drift.py`, 14 s; page 14, after the
general-force-drift page 13).
- Computed: ion and electron in uniform $\mathbf B$ out of the page with
  $\mathbf g=-g\,\mathbf e_y$, $g=0.2\,\rho_{Li}\omega_{ci}^2$, six ion periods.
- Shown: both orbits in $x/\rho_{Li}$ [1]; the ion loops drift to $-x$, the
  electron band 16 times slower to $+x$.
- Numbers on screen, $v_{D,x}/(\rho_{Li}\omega_{ci})$ [1], orbit (slope of the
  gyro-period average) against $(m_\alpha/q_\alpha)(\mathbf g\times\mathbf B)_x/B^2$:
  ion $-0.20000$ against $-0.20000$, electron $+0.01250$ against $+0.01250$
  (agree to $10^{-5}$ relative). The force $m_\alpha\mathbf g$ does not depend on
  the charge: opposite drifts, ratio $m_i/m_e$, a current carried by the ions.

**`mu-ramp`** (`animations/mu_ramp.py`, 23 s; page 23, after the Faraday page 22).
- Computed: the scheme of `derivations/plot_mu_ramp.py` (page 26) with the
  trajectory kept: one ion centred on the axis of a uniform
  $B/B_0=\tfrac32+\tfrac12\tanh(t/\tau)$, $\omega_{c0}\tau=20$, shown from
  $t=-4\tau$ to $4\tau$ (38 gyrations), induced
  $\mathbf E=-\tfrac12\dot B\,\mathbf e_z\times\mathbf r$, 1600 steps per turn.
  $B_0$ is the field at the start of the window, $\rho_{L0}$ the starting radius.
- Shown: top view with dashed circles $\rho_{L0}$ and $\rho_{L0}/\sqrt2$, field
  symbols growing with $B$, the clockwise induced $\mathbf E$ (arrow length
  $\propto\dot B$); traces against $\omega_{c0}t$ [1]: left $B/B_0$ and the orbit
  radius $\rho_L/\rho_{L0}$ with $(B/B_0)^{-1/2}$ dashed, right $\mu/\mu_0$ and the
  flux $\pi\rho_L^2B$ relative to its start on a $\pm1\,\%$ scale.
- Numbers: end $B/B_0=1.999$, $\rho_L/\rho_{L0}=0.7073=(B/B_0)^{-1/2}$ to
  $1.5\times10^{-5}$; $\max|\mu/\mu_0-1|=7.2\times10^{-5}$ (on screen $\le8\times10^{-5}$) and
  $\max|\pi\rho_L^2B\ \mathrm{rel.}-1|=5\times10^{-4}$ during the ramp (a
  reversible breathing of the orbit), $3\times10^{-8}$ and $3\times10^{-5}$ at
  the end. The flux uses the measured orbit radius, $\mu$ the measured speed.
  At $\omega_{c0}\tau=1,2$ the final $\mu$ equals `plot_mu_ramp.boris` to $10^{-13}$.

**`loss_cone`** plot (`derivations/plot_loss_cone.py`, page 29 "Loss cone in
velocity space", after the loss-cone derivation page 28).
- Computed: 1500 particles of an isotropic Maxwellian at the midplane (seeded),
  $v_\parallel$, $v_\perp$ in $v_\mathrm{th}=(2k_BT/m_\alpha)^{1/2}$ [1]; field
  $B(z)/B_0=1+(R_m-1)(z/L)^2$, $R_m=4$. Trapped if
  $v_\parallel^2(z)=v^2-v_{\perp0}^2B(z)/B_0$ (from $\mu$ and $W$) reaches zero for
  $|z|\le L$, tested on a grid of $z$, without the cone formula.
- Shown: left, trapped (blue circles) and lost (vermilion triangles) in the
  $(v_\parallel, v_\perp)$ plane with the lines $\sin^2\alpha_c=1/R_m$; right,
  lost fraction against $R_m$ [1] from $2\times10^5$ particles per point, with
  $1-\sqrt{1-1/R_m}$ dashed.
- Numbers: at $R_m=4$, 14.3 % of the 1500 shown are lost (formula 13.4 %);
  the large samples agree with the formula to $\le1.2\times10^{-3}$ (one binomial
  standard deviation) for $R_m=1.25\dots20$. `derivations/test_chapters.py`
  (`test_loss_cone_sample_against_pitch_angle`) checks the test particle by
  particle against $\sin^2\alpha\ge1/R_m$.

**`polarization-drift`** (`animations/polarization_drift.py`, 17 s; page 31,
after the polarization page 30).
- Computed: ion and electron in uniform $\mathbf B$ out of the page with
  $\mathbf E=E(t)\,\mathbf e_y$, $E/B=(E_1/B)(1-\cos(\pi t/T_r))/2$ up to
  $T_r$ = three ion periods ($\omega/\omega_{ci}\approx0.17$), then constant,
  $E_1/B=0.75\,v_{\perp i}$; five ion periods in all. Guiding centre
  $\mathbf R=\mathbf x+(m_\alpha/q_\alpha)(\mathbf v-\mathbf v_D)\times\mathbf B/B^2$
  with $\mathbf v_D=\mathbf E\times\mathbf B/B^2$.
- Shown: orbits with the common E x B displacement $x_D=\int_0^tE/B\,dt$
  removed, $(x-x_D)/\rho_{Li}$, $y/\rho_{Li}$ [1]; growing $\mathbf E(t)$ arrow;
  lower panel $R_y/\rho_{Li}$ [1] against $\omega_{ci}t$ [1] with
  $(m_\alpha/(q_\alpha B^2))E(t)$ dashed.
- Numbers on screen, $\Delta R_y/\rho_{Li}$ [1] (mean over the last two ion turns)
  against $m_\alpha E_1/(q_\alpha B^2)$: ion $+0.7500$ against $+0.7500$, electron
  $-0.0469$ against $-0.0469$. The ion shifts along $\mathbf E$, the electron
  16 times less against it: the polarization current is carried by the ions.

`animations/magnetized_polarization.py` shows Faraday rotation of a wave, not
the polarization drift of particles, so the drift got its own scene.

## Cyclotron resonance (2026-10-26)

`animations/cyclotron_resonance.py` (`cyclotron-resonance`, 31 s; page 34,
after the derivation page 33): uniform B out of the page, uniform field
rotating clockwise (s = +1) or counterclockwise (s = -1), particle from rest,
Boris push (`drift_models.boris_em`), 400 steps per gyration, 6 gyrations
per run; each species normalized with its own abs(omega_c) (speed v B/E_0,
time abs(omega_c) t, all [1]), so the electron run is the mirror image of the
ion run. Dashed: the closed form 2 abs(sin(Delta t/2)/Delta).
Checks (`CyclotronResonancePhysics`): orbit speed equals the closed form to
0.6 dt (half-step start); RK4 of the complex equation equals it to 1e-8;
growth rate 0.99994 abs(q) E_0/m (ion and electron), W proportional to t^2
(log-log slope 2 within 0.01); detuned peak 10.0005 (formula 10); counter-rotating
peak 1.0000 for both species (formula 1). The page-33 closed form was also
checked with SymPy (ODE residual 0, v_cw(0) = 0, modulus, Delta -> 0 limit).
Note: from rest the speed grows linearly and the energy quadratically in time;
the absorbed power, not the energy, grows linearly.

