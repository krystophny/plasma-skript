# Single-particle motion

LOOK deck; THINK work takes place on blank Goodnotes notebook pages.
No writing pages in the deck. One idea per page.

Online deck: [present/05-single-particle-motion/](https://krystophny.github.io/plasma-skript/present/05-single-particle-motion/).
The site build exports the same pages as SVG and PDF, with inline animations and offline caching.

## Page sequence

Route (rebuilt 2026-10-26): one derivation-overview page per topic, in the
lecturer's notation of 2024/25 (species index $\alpha$, signed
$\omega_c = q_\alpha B/m_\alpha$, Larmor radius $\rho_L = v_\perp/|\omega_c|$,
gyrophase $\phi$, $\mathbf b = \mathbf B/B$, drifts $\mathbf v_D$,
curvature with $R_c$ and $\mathbf e_R$ pointing away from the centre of
curvature, $(\mathbf b\cdot\nabla)\mathbf b = -\mathbf e_R/R_c$), each next to
its animation. Corrected against his notes: $v_y = -v_\perp\sin(\omega_c t + \phi)$
with signed $\omega_c$; ions rotate clockwise for $\mathbf B$ out of the page.
Section numbers follow the script: 5.3 from the guiding centre to the
Hamiltonian page (field-line following, moment, mirror force, energy and
$\mu$, the time-varying field), 5.4 for the mirror, the loss cone and the
grad-$B$ and curvature drifts (rebuilt 2026-10-27). Pages 15-30 are LOOK
pages: picture, at most three formula rows and one result; the derivation
route between start and result is in the THINK list below. Symbols added
2026-10-27 to avoid clashes: pitch angle $\vartheta$ (not $\alpha$, the species
index; the Skript uses $\vartheta$ as well), mirror half-length $L_m$ (not $L$, the
field-variation length), ramp time $\tau_B$ (not $\tau$, the collision time),
initial value $\mu_i$ (not $\mu_0$), magnetic flux $\psi$ (not $\Phi$), pass length
$\ell$; italic $R$ is the major radius, bold $\mathbf R$ the guiding centre.

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
| 14 | Gravity drift | animation | motion-exb | F = m g in the force drift: ion and electron drift opposite, the electron 16 times slower (reduced mass ratio m_i/m_e = 16, spoken); formula v_D = (m_alpha/q_alpha)(g x B)/B^2 on screen. |
| 15 | Guiding centre | static | motion-guiding-center | Side view: ion helix about the field line through R (axis b); R from O to the guiding centre on the axis, r from O to the particle, rho = r - R from R to the particle, perpendicular to b. r = R + rho with rho = (b x v)/omega_c; uniform B: rho-dot = v_perp, so R-dot = v_par b exactly; ordering eps = rho_L/L << 1, omega/abs(omega_c) << 1. See "THINK route, pages 15-30" below. |
| 16 | Staying on a field line | derivation | motion-guiding-center | Helix centred on a curved field line, kappa to the centre of curvature, ion v_D^curv into the page, one pass of arc length ell (L stays the field-variation length). d(v_par b)/dt = (dv_par/dt) b + v_par^2 kappa; supplied by the drift, q v_D^curv x B = m v_par^2 kappa, so v_D^curv = (m v_par^2/(q B)) b x kappa. Result: R-dot = v_par b + v_D^curv, offset per pass Delta_perp ~ abs(v_D^curv) ell/abs(v_par) = (ell/R_c) abs(v_par/omega_c). Rotational transform only in THINK. See "THINK route, pages 15-30" below. |
| 17 | Magnetic moment | derivation | motion-guiding-center | I = abs(q) abs(omega_c)/(2 pi), S = pi rho_L^2: mu = I S = m v_perp^2/(2B), mu-vector = -mu b (diamagnetic). Field symbols on a regular grid. See "THINK route, pages 15-30" below. |
| 18 | Mirror force | derivation | motion-guiding-center | div B = 0: B_r = -(r/2) dB/dz; <F_par> = abs(q) v_perp B_r(rho_L) = -mu dB/dz; parallel equation m dv_par/dt = -mu dB/ds - q dPhi/ds, s = z on the axis (the figure's axis is z). See "THINK route, pages 15-30" below. |
| 19 | Energy and mu | derivation | motion-guiding-center | W = m v_par^2/2 + mu B + q Phi = const.; <F_par> v_par with W-dot = 0 gives mu-dot = 0 to leading order in eps, static fields (the mirror force is itself leading order); flux through the orbit psi = pi rho_L^2 B = (2 pi m/q^2) mu = const. (psi, as Phi is the potential); mirror point v_par = 0 where B = (W - q Phi)/mu. See "THINK route, pages 15-30" below. |
| 20 | mu from Faraday's law | derivation | motion-guiding-center | One gyration: delta(m v_perp^2/2) = q oint E.dl; Faraday along the orbit: oint E.dl = +- pi rho_L^2 dB/dt (+ ions, clockwise for B out of the page; - electrons), so q oint E.dl = abs(q) pi rho_L^2 dB/dt; per turn delta B = 2 pi (dB/dt)/abs(omega_c): delta(m v_perp^2/2) = mu delta B, so delta mu ~ 0. B symbols everywhere. See "THINK route, pages 15-30" below. |
| 21 | mu in a slowly growing field | animation | motion-guiding-center | B ramps from B_0 to 2B_0 over about 20 turns (ramp time tau_B, omega_c0 = q B_0/m defined on screen), induced E clockwise: orbit shrinks as B^-1/2; flux psi = pi rho_L^2 B and mu stay constant (numbers against psi_i, mu_i). Faraday route of page 20 in motion; numerics of the plot on page 22. |
| 22 | Adiabatic invariance | plot | motion-guiding-center | Boris orbit in B_0 -> 2B_0 with the induced E: abs(mu_f/mu_i - 1) against abs(omega_c0) tau_B; smooth (tanh) ramp exponentially small, linear ramp with kinks only a power law in 1/(omega_c0 tau_B) (peak envelope about tau_B^-1.8, two kinks interfere). |
| 23 | mu in the Hamiltonian picture | derivation | motion-guiding-center | J = oint (m v_perp + q A).dl = 2 pi m v_perp rho_L - pi abs(q) B rho_L^2 = (2 pi m/abs(q)) mu; guiding-centre H = m v_par^2/2 + mu B(R) + q Phi(R); J is an adiabatic invariant, hence mu; mu B acts as a potential: mirror force and grad-B drift (the grad-B force itself on page 27). See "THINK route, pages 15-30" below. |
| 24 | Mirror ratio and loss cone | derivation | motion-nonuniform-fields | Pitch angle theta (theta.alt; alpha is the species index): sin theta = v_perp/v; with mu const. and Phi = 0 (speed constant) sin^2 theta/B = const.; trapped if B_0/sin^2 theta_0 < B_max: sin^2 theta_c = 1/R_m. Cone drawn at theta_c = 30 deg (R_m = 4), both lost sectors labelled. See "THINK route, pages 15-30" below. |
| 25 | Magnetic mirror | animation | motion-nonuniform-fields | After the loss-cone page, which defines theta, theta_c and R_m. Six pitch angles; 29 deg lost, 31 deg reflected for R_m = 4; mirror half-length L_m. |
| 26 | Loss cone in velocity space | plot | motion-nonuniform-fields | Isotropic sample at the midplane, R_m = 4: lost particles fill the cone sin^2 theta < 1/R_m around v_par; lost fraction 1 - cos theta_c = 1 - sqrt(1 - 1/R_m), the solid angle of the two cones over 4 pi, 13 % at R_m = 4; formula shown once, on the page. |
| 27 | Grad-B drift | derivation | motion-nonuniform-fields | F_perp = -mu grad_perp B in the force drift: v_D = (mu/q) B x grad B/B^2, opposite for ions and electrons. Sketch: smaller orbits where B is stronger, ion drift arrow to the left, small symbols labelled "weaker B". See "THINK route, pages 15-30" below. |
| 28 | Grad-B drift | animation | motion-nonuniform-fields | Smaller orbit where B is stronger; opposite drifts. Framed axes x/rho_Li, y/rho_Li [1]; B = B_0 [1 + y/(10 rho_Li)]. |
| 29 | Curvature drift | static | motion-nonuniform-fields | Merges the former pages "Field-line curvature" and "Curvature drift": picture with b, kappa, R_c e_R and the ion (into the page) and electron drifts; kappa = (b.grad) b = -e_R/R_c; result v_D^curv = m v_par^2 e_R x b/(q B R_c), not re-derived: the drift of "Staying on a field line". Symbols line: torus R_c = R, R major radius. See "THINK route, pages 15-30" below. |
| 30 | Curvature drift | animation | motion-nonuniform-fields | Ion up, electron down in a purely toroidal field; B = B_phi e_phi into the page (cross) in the right-handed (R, phi, Z) view; R major radius on screen. |
| 31 | Polarization drift | static | motion-polarization | Slowly varying E_perp; polarization current carried by ions. |
| 32 | Polarization drift | animation | motion-polarization | E_perp switched on over three ion turns; view with the common E x B displacement removed: ion guiding centre moves along E by m E_1/(q B^2), electron 16 times less and opposite. |
| 33 | Drifts | static | (none) | Table: charge and mass dependence of every drift; vacuum-field sum of curvature and grad-B. |
| 34 | Cyclotron resonance | derivation | motion-cyclotron-resonance | Rotating field E_cw = E_0 e^(-i s omega t); v_cw = v_x + i v_y obeys dv_cw/dt = -i omega_c v_cw + (q/m) E_cw (the script's equation); from rest the modulus 2 abs(sin(Delta t/2)/Delta), Delta = omega_c - s omega; Delta = 0: v_perp grows linearly, W quadratically. Ions take the clockwise, electrons the counterclockwise field (signed omega_c). |
| 35 | Cyclotron resonance | animation | motion-cyclotron-resonance | Predict each run before it starts: ion with the clockwise field at omega_ci (spiral, straight line in v_perp), at 0.8 omega_ci (beat, peak 10 E_0/B), with the counterclockwise field (nothing), electron with the counterclockwise field (resonance again). Measured slope 0.9999 abs(q) E_0/m against 1. |


## THINK route, pages 15-30

The LOOK pages carry the start and the result; the steps below are for the
Goodnotes board and for speaking. Nothing removed from the slides is lost.

**15 Guiding centre.**
- THINK: velocity split: $d\mathbf R/dt = v_\parallel\mathbf b + \mathbf v_D$, $d\boldsymbol\rho/dt\approx\mathbf v_\perp$, so $\mathbf v=v_\parallel\mathbf b+\mathbf v_\perp+\mathbf v_D$ (script equation `motion-velocity-split`); the gyration velocity averages to zero over one turn.
- THINK: $\rho=(\mathbf b\times\mathbf v)/\omega_c$ agrees with the board solution of page 3: for $\mathbf b=\mathbf e_z$, $(\mathbf b\times\mathbf v)/\omega_c=((v_\perp/\omega_c)\sin(\omega_ct+\phi),(v_\perp/\omega_c)\cos(\omega_ct+\phi))=(x-x_0,y-y_0)$.
- THINK: uniform $\mathbf B$: $\dot{\mathbf v}=\omega_c\mathbf v\times\mathbf b$ gives $\dot{\boldsymbol\rho}=\mathbf b\times\dot{\mathbf v}/\omega_c=\mathbf b\times(\mathbf v\times\mathbf b)=\mathbf v_\perp$. The gyration velocity is exactly $\dot{\boldsymbol\rho}$, which is why it drops out of $\dot{\mathbf R}=\mathbf v-\dot{\boldsymbol\rho}=v_\parallel\mathbf b$, exactly. Across $\mathbf B$ the orbit is a circle of radius $\rho_L$ about $\mathbf R$: bounded.
- THINK: numerical check (Boris push, uniform $\mathbf B=\mathbf e_z$, $q/m=\pm1$, 2000 steps per turn, time-centred velocity): $\mathbf R=\mathbf r-(\mathbf b\times\mathbf v)/\omega_c$ is the fitted circle centre for ion and electron; $\mathbf R_\perp$ constant to $5\times10^{-6}\rho_L$, $|d\boldsymbol\rho/dt-\mathbf v_\perp|\le2.5\times10^{-6}v$, $dR_z/dt=v_\parallel$; ion clockwise, electron counterclockwise.
- THINK: nearly uniform field during one gyration: $\rho_L/L\ll1$ in space, $\omega/|\omega_c|\ll1$ in time; $\omega$ is the rate of change of the fields.
- THINK: the sketch is a side view: the ion helix about the field line through $\mathbf R$ (front half solid, back half faint); the particle is drawn at the top of a turn, where $\boldsymbol\rho=\mathbf r-\mathbf R$ is perpendicular to $\mathbf b$ and in the page.

**16 Staying on a field line.**
- THINK: $q_\alpha\mathbf v\times\mathbf B\perp\mathbf B$: no magnetic force along $\mathbf b$, so $v_\parallel$ changes only through slow forces (mirror force, $q_\alpha E_\parallel$).
- THINK: a particle moving with $v_\parallel\mathbf b$ along a curved line must be accelerated: $d(v_\parallel\mathbf b)/dt=(dv_\parallel/dt)\,\mathbf b+v_\parallel\,d\mathbf b/dt$, and along the path in a static field $d\mathbf b/dt=v_\parallel(\mathbf b\cdot\nabla)\mathbf b=v_\parallel\boldsymbol\kappa$ (the drift and gyration contributions to $d\mathbf b/dt$ are of higher order in $\epsilon$, which is why the slide writes "=" for the guiding centre moving with $v_\parallel\mathbf b$); $\boldsymbol\kappa=-\mathbf e_R/R_c$ points to the centre of curvature. The only force across $\mathbf B$ is magnetic, so the guiding centre must drift with $q_\alpha\mathbf v_D\times\mathbf B=m_\alpha v_\parallel^2\boldsymbol\kappa$; crossing with $\mathbf B$: $\mathbf v_D=(m_\alpha v_\parallel^2/(q_\alpha B))\,\mathbf b\times\boldsymbol\kappa=(m_\alpha v_\parallel^2/(q_\alpha BR_c))\,\mathbf e_R\times\mathbf b$, the curvature drift of page 29 (sign checked with SymPy).
- THINK: size: $|\mathbf v_D|=\rho_\parallel v_\parallel/R_c\sim\epsilon v$. Slowly varying $\mathbf B$ in general: $\dot{\boldsymbol\rho}$ gains $(d(\mathbf b/\omega_c)/dt)\times\mathbf v$, with $d(\mathbf b/\omega_c)/dt\sim v/(|\omega_c|L)$, of size $\epsilon v$; a weak force adds $\mathbf F\times\mathbf B/(q_\alpha B^2)$ (page 13).
- THINK: pass of arc length $\ell$ (not $L$, which is the field-variation length): in the time $\ell/|v_\parallel|$ the guiding centre moves $\ell$ along $\mathbf b$ and $\Delta_\perp=|\mathbf v_D^{\rm curv}|\,\ell/|v_\parallel|=(\ell/R_c)\,|v_\parallel/\omega_c|$ across it (SymPy), about one Larmor radius for $\ell\sim R_c$ and $v_\parallel\sim v_\perp$: it follows the field line to $O(\epsilon)$. The generic estimate $|\mathbf v_D|\sim\epsilon v$ gives $\Delta_\perp\sim\rho_Lv/|v_\parallel|$, which grows as $v_\parallel\to0$; that is the grad-$B$ drift, not the curvature drift, which vanishes with $v_\parallel$.
- THINK: caveat: near $v_\parallel=0$ (mirror points, trapped particles) the grad-$B$ drift dominates; over many passes the drifts add up to orbit widths (banana orbits) and, in a purely toroidal field, to charge separation; the cure, the rotational transform, comes later (said, no longer on the slide).
- THINK: converging field lines are the third mechanism: the orbit keeps enclosing the same flux $\psi$ (page 19), so the guiding centre stays on the lines that the orbit encloses.

**17 Magnetic moment.**
- THINK: orbit current $I=|q_\alpha|/T_c$ with $T_c=2\pi/|\omega_c|$; $\mu=IS=|q_\alpha||\omega_c|\rho_L^2/2=m_\alpha v_\perp^2/(2B)$: perpendicular kinetic energy per $B$.
- THINK: orbit current left-handed about $\mathbf B$ for ions and electrons, so $\boldsymbol\mu$ points against $\mathbf B$: diamagnetic.

**18 Mirror force.**
- THINK: cylinder coordinates $r,\theta,z$ about the orbit axis (the figure's axis), $B_z(z)>0$, so $s=z$ on the axis; the rows use $z$, the result the arc length $s$. Near the axis $\nabla\cdot\mathbf B=0$ reads $(1/r)\,\partial(rB_r)/\partial r=-\partial B_z/\partial z$, so $B_r=-(r/2)\,\partial B_z/\partial z$; where the lines converge $B_r$ points to the axis.
- THINK: orbit on the axis, $r=\rho_L$, $B_\theta=0$, $v_r=0$: $q_\alpha(\mathbf v\times\mathbf B)_z=-q_\alpha v_\theta B_r$. Ions circle $\mathbf B$ left-handed, $v_\theta=-v_\perp$; electrons right-handed, $v_\theta=+v_\perp$; so $v_\theta=-\mathrm{sgn}(q_\alpha)v_\perp$ and $q_\alpha(\mathbf v\times\mathbf B)_z=|q_\alpha|v_\perp B_r$ for both signs (sign checked, unchanged from before; SymPy check "Deck: mirror force from div B = 0").
- THINK: the same at every gyrophase, so it is the gyroaverage, with $B_r$ evaluated at $r=\rho_L$: $\langle F_\parallel\rangle=-|q_\alpha|v_\perp(\rho_L/2)\,\partial B/\partial z$ and $|q_\alpha|v_\perp\rho_L/2=m_\alpha v_\perp^2/(2B)=\mu$. This is a leading-order result in $\epsilon$ (linear $B_r$, $\partial B/\partial z$ constant across the orbit).
- THINK: add $q_\alpha E_\parallel=-q_\alpha\partial\Phi/\partial s$ for the parallel equation of motion.

**19 Energy and mu.**
- THINK: magnetic force does no work, $q_\alpha(\mathbf v\times\mathbf B)\cdot\mathbf v=0$; static $\mathbf E=-\nabla\Phi$: $d(m_\alpha v^2/2+q_\alpha\Phi)/dt=0$; with $v^2=v_\parallel^2+v_\perp^2$ and $m_\alpha v_\perp^2/2=\mu B$, $W=m_\alpha v_\parallel^2/2+\mu B+q_\alpha\Phi$. Exact in static fields, $\mu$ and $B$ at the particle.
- THINK: not circular: $\mu\equiv m_\alpha v_\perp^2/(2B)$ at each instant, allowed to vary. Multiply page 18 by $v_\parallel$, $ds/dt=v_\parallel$: $d(m_\alpha v_\parallel^2/2)/dt=-\mu\,dB/dt-q_\alpha\,d\Phi/dt$. Energy: $d(m_\alpha v_\parallel^2/2+\mu B+q_\alpha\Phi)/dt=0$. Subtract: $B\,d\mu/dt=0$.
- THINK: the slide says $\dot\mu=0$ to leading order in $\epsilon$, static fields, because the mirror force used here is itself the leading-order result of page 18; adiabatic invariant: constant to leading order in $\epsilon=\rho_L/L$ or $1/(|\omega_c|\tau_B)$, $\tau_B$ time of change; in uniform fields, also with uniform $\mathbf E\perp\mathbf B$ and $\mu$ taken in the drift frame, exactly constant.
- THINK: consequence for converging fields: $\psi=\pi\rho_L^2B=\pi m_\alpha^2v_\perp^2/(q_\alpha^2B)=(2\pi m_\alpha/q_\alpha^2)\mu=$ const. ($\psi$ magnetic flux; $\Phi$ is the electrostatic potential): the orbit keeps enclosing the same field lines; the guiding centre follows them as they converge.
- THINK: mirror point where $\mu B+q_\alpha\Phi=W$; with $\Phi=0$, $B=W/\mu$.

**20 mu from Faraday's law.**
- THINK: one turn: $\delta(m_\alpha v_\perp^2/2)=q_\alpha\oint\mathbf E\cdot d\mathbf l$, $\oint$ along the orbit, left-handed about $\mathbf B$ for $q_\alpha>0$.
- THINK: Stokes along the orbit in the direction of motion: $\oint\mathbf E\cdot d\mathbf l=\pm\pi\rho_L^2\,\partial B/\partial t$, upper sign for ions (clockwise for $\mathbf B$ out of the page, so the right-hand normal points against $\mathbf B$), lower sign for electrons (SymPy with $\mathbf E=-\tfrac12\dot B\,\mathbf e_z\times\mathbf r$); hence $q_\alpha\oint\mathbf E\cdot d\mathbf l=|q_\alpha|\pi\rho_L^2\,\partial B/\partial t$ for both signs; per turn $\delta B=(2\pi/|\omega_c|)\,\partial B/\partial t$; so $\delta(m_\alpha v_\perp^2/2)=\mu\,\delta B$ and $\delta\mu=\delta(m_\alpha v_\perp^2/2)/B-\mu\,\delta B/B=0$.
- THINK: assumptions: slow change $|\partial B/\partial t|\ll|\omega_c|B$, $E_\parallel=0$, no $E\times B$ drift of the guiding centre; the box says $\delta\mu\approx0$ because $\rho_L$, $v_\perp$ and $B$ are held fixed over the turn (first order in $\delta B$).

**22 Adiabatic invariance.**
- THINK: $B:B_0\to2B_0$ with the induced $\mathbf E=-(1/2)(\partial B/\partial t)\,\mathbf e_z\times\mathbf r$, $\mathbf r$ from the axis; Boris integration (details in "Adiabatic-invariance plot" below). Ramp time $\tau_B$ ($\tau$ is the collision time of page 9), initial and final $\mu_i$, $\mu_f$ ($\mu_0$ is the vacuum permeability).
- THINK: the slide line "smooth ramp: exponentially small; kinks: power law in $1/(|\omega_{c0}|\tau_B)$" is checked against the plotted data: tanh, $\ln|\mu_f/\mu_i-1|$ linear in $\tau_B$ for $|\omega_{c0}|\tau_B\ge2$ (slope $-3.1$ per unit, rms residual 0.04); linear ramp, oscillating, peaks $9.4\times10^{-3}$, $3.5\times10^{-3}$, $1.8\times10^{-3}$ at 2.9, 5.1, 7.3 on a power law of slope $-1.8$ in log-log.

**23 mu in the Hamiltonian picture.**
- THINK: $J=\oint(m_\alpha\mathbf v_\perp+q_\alpha\mathbf A)\cdot d\mathbf l$ with $\mathbf A=\mathbf B\times\boldsymbol\rho/2$ ($\nabla\times\mathbf A=\mathbf B$): the kinetic part is $m_\alpha v_\perp\cdot2\pi\rho_L$; $\oint\mathbf A\cdot d\mathbf l$ is the flux counted with the sense of motion, $-B\pi\rho_L^2$ for ions (left-handed about $\mathbf B$) and $+B\pi\rho_L^2$ for electrons, so $q_\alpha\oint\mathbf A\cdot d\mathbf l=-|q_\alpha|\pi B\rho_L^2$ for both. With $|q_\alpha|B\rho_L=m_\alpha v_\perp$: $J=2\pi m_\alpha v_\perp\rho_L-\pi|q_\alpha|B\rho_L^2=\pi m_\alpha v_\perp\rho_L=(2\pi m_\alpha/|q_\alpha|)\mu=|q_\alpha|\pi\rho_L^2B$, $|q_\alpha|$ times the flux through the orbit (SymPy). Both rows are on the slide.
- THINK: actions of periodic motions are adiabatic invariants: slowly shortened pendulum, Einstein and Lorentz, Solvay 1911. $J\propto\mu$, so $\mu$ is one too (the result box).
- THINK: gyrophase $\phi$ ignorable: $p_\phi=(m_\alpha/q_\alpha)\mu=$ const. (Noether); his 2024 slides (Chapter 1-5, pp. 61-66) and the 2021 recording "#9 Guiding-Center Lagrangian"; $H$ as on his 2025 slides (pp. 15-16).
- THINK: $-\partial H/\partial s$ gives $m_\alpha dv_\parallel/dt=-\mu\,\partial B/\partial s-q_\alpha\partial\Phi/\partial s$ (page 18); $\mathbf F_\perp=-\nabla_\perp(\mu B)$ gives the grad-$B$ drift, shown on page 27 and not repeated here.
- THINK: exact for the guiding centre, which is an expansion in $\epsilon=\rho_L/L$; for the particle $\mu$ is an adiabatic invariant.

**24 Mirror ratio and loss cone.**
- THINK: pitch angle $\vartheta$ (Typst `theta.alt`; $\alpha$ is the species index): $\mu=m_\alpha v^2\sin^2\vartheta/(2B)$; with $\Phi=0$ the energy $W=m_\alpha v^2/2$ fixes $v$, so $\sin^2\vartheta/B=$ const.; mirror point $\vartheta=90^\circ$ at $B=B_0/\sin^2\vartheta_0$; trapped if this is below $B_{\max}$.
- THINK: the mirror animation (page 25) follows here, after $\vartheta$, $\vartheta_c$ and $R_m$ are defined; the cone in the sketch is drawn at $\vartheta_c=30^\circ$, the $R_m=4$ of the animation and the plot.

**26 Loss cone in velocity space.**
- THINK: isotropic Maxwellian at the midplane, $v_{\rm th}=\sqrt{2k_BT/m_\alpha}$; trapped if $v_\parallel^2(z)$ reaches 0 before the throat $z=L_m$ (mirror half-length; $L$ stays the field-variation length).
- THINK: lost fraction: an isotropic distribution fills the solid angle uniformly; each cone of half-angle $\vartheta_c$ has solid angle $2\pi(1-\cos\vartheta_c)$, two cones over $4\pi$ give $1-\cos\vartheta_c=1-\sqrt{1-1/R_m}$ (SymPy).

**27 Grad-B drift.**
- THINK: gyroaveraged force $\mathbf F=-\mu\nabla B=-\nabla(\mu B)$, $\mu$ constant; the parallel part is the mirror force of page 18; the perpendicular part into $\mathbf v_D=(\mathbf F_\perp/q_\alpha)\times\mathbf B/B^2$ with $-\nabla B\times\mathbf B=\mathbf B\times\nabla B$.
- THINK: $\mathbf B$ out of the page, stronger at the top (larger symbols; the smaller ones are labelled "weaker $B$"): smaller orbits there; $\mathbf B\times\nabla B$ points to the left, so the ion drifts left (arrow), the electron right.

**29 Curvature drift** (former pages "Field-line curvature" and "Curvature drift").
- THINK: $s$ arc length, $d\mathbf x/ds=\mathbf b$; chain rule $\boldsymbol\kappa=d\mathbf b/ds=\sum_i(\partial\mathbf b/\partial x_i)(dx_i/ds)=(\mathbf b\cdot\nabla)\mathbf b$, the change of the unit tangent per unit arc length; $R_c=1/|\boldsymbol\kappa|$, $R_c=\infty$ where $\boldsymbol\kappa=0$.
- THINK: circle of radius $a$: $\mathbf b=\mathbf e_\varphi$, $ds=a\,d\varphi$, $\boldsymbol\kappa=(1/a)\,\partial\mathbf e_\varphi/\partial\varphi=-\mathbf e_R/a$; $\mathbf e_R$ outward.
- THINK: torus: $R_c=R$, the major radius (symbols line), the $R$ of the animation on page 30; $\mathbf R$ bold stays the guiding centre.
- THINK: not re-derived on the slide; same drift as "Staying on a field line" (page 16), here in the centrifugal picture: guiding-centre acceleration $\mathbf a=-(v_\parallel^2/R_c)\mathbf e_R$; centrifugal force $m_\alpha v_\parallel^2\mathbf e_R/R_c$ into $\mathbf v_D=\mathbf F\times\mathbf B/(q_\alpha B^2)$; with $\mathbf b\times\boldsymbol\kappa=\mathbf e_R\times\mathbf b/R_c$ it is that result.
- THINK: mnemonic $\mathbf v_D^{\rm curv}=\rho_\parallel\Omega_\parallel\,\mathbf e_R\times\mathbf b$ with $\rho_\parallel=v_\parallel/\omega_c$, $\Omega_\parallel=v_\parallel/R_c$.

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
$x = x_0 + (v_\perp/\omega_c) \sin(\omega_c t + \phi)$,
$y = y_0 + (v_\perp/\omega_c) \cos(\omega_c t + \phi)$:
`gyration-top-view` (ion and electron, B out of the page, $m_i/m_e = 16$
stated on screen with the hydrogen value 1836, $T_i = T_e$, clock
$\omega_{ci} t$ [1]), `gyration-components` (ion circle beside $v_x/v_\perp$
and $(x - x_0)/\rho_L$ against $\omega_c t$ [1]) and `gyration-helix` (oblique
projection, pitch $1.1\,\rho_L$). The script shows all three in §5.1. All
chapter-5 scenes were re-rendered on 2026-10-26 in the deck notation
($\rho_L$, $\rho_{Li}$, $\omega_{ci}$, $\mathbf v_D$, $q_\alpha$, $m_\alpha$);
only labels changed, not the physics, parameters or layout.

## Adiabatic-invariance plot (2026-10-26)

`derivations/plot_mu_ramp.py` writes `build/fig/mu_ramp.svg` (page 22).
Normalized $q_\alpha = m_\alpha = 1$, $B_0 = 1$: time $\omega_{c0}t$ [1],
lengths $\rho_{L0}$ [1]. Uniform $B(t)$ from $B_0$ to $2B_0$ with the induced
field $\mathbf E = -\tfrac12\dot B\,\mathbf e_z\times\mathbf r$; orbit centred on
the axis (gyrophase-independent). Smooth ramp $B/B_0 = 3/2 + \tanh(t/\tau_B)/2$,
linear ramp with kinks at $t = \pm\tau_B$, same largest slope. Boris push,
1600 steps per turn, exact discrete start circle, $\mathbf E$ from the field
increment over each step. Plotted $|\mu_f/\mu_i-1|$ [1] against $|\omega_{c0}|\tau_B$ [1]
($\mu_i$, $\mu_f$ initial and final, $\tau_B$ ramp time; the values are
non-negative anyway: on the axis a non-adiabatic change only shifts the
guiding centre off the axis). Values: tanh $1.1\times10^{-1}$, $3.0\times10^{-2}$,
$2.0\times10^{-3}$, $5.0\times10^{-6}$, $1.0\times10^{-8}$, $2.0\times10^{-11}$
at $\omega_{c0}\tau_B = 0.25, 1, 2, 4, 6, 8$; linear $1.2\times10^{-1}$,
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
the grad-B page 27).
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

**`curvature-drift`** (`animations/curvature_drift.py`, 20 s; page 30, after the
curvature-drift page 29).
- Computed: both species in the toroidal vacuum field
  $\mathbf B=B_0R_0/R\,\hat{\boldsymbol\varphi}$, $R_0=40\,\rho_{Li}$, start on the
  midplane with $v_\parallel=v_\perp$, run for the time in which the ion goes
  half-way round the torus (the electron, with $v_{\parallel e}=4v_{\parallel i}$,
  goes round twice).
- Shown: poloidal plane, $(R-R_0)/\rho_{Li}$ and $Z/\rho_{Li}$ [1]; clock: toroidal
  angle of the ion $\varphi$ [1]. The ion drifts up, the electron down, with no
  radial displacement: charge separation that a purely toroidal field cannot
  hold, the motivation for the rotational transform.
- Orientation (2026-10-27): $(R,\varphi,Z)$ right-handed, $\mathbf e_R\times\mathbf e_\varphi=\mathbf e_Z$;
  with $R$ to the right and $Z$ up, $\mathbf e_\varphi$ points into the page, so the
  field symbols and the key are crosses ($\otimes$; they were dots before). The
  model has $\mathbf b=+\mathbf e_\varphi$ and the ion drifts $+Z$, consistent with
  "ion $\uparrow$"; only the symbol was wrong.
- On screen only the field key $\mathbf B=B_0(R_0/R)\,\mathbf e_\varphi$, "$R$ major radius", the species
  labels, the axes, the clock and the vacuum-field drift
  $\mathbf v_D=(m_\alpha/q_\alpha BR)(v_\parallel^2+\tfrac12v_\perp^2)\,\mathbf e_R\times\mathbf b$
  (curvature plus grad-$B$, $R_c=R$). Spoken: $R_0=40\,\rho_{Li}$,
  $v_\parallel=v_\perp$, $m_i/m_e=16$, $T_i=T_e$; the drift is about
  $0.04\,\rho_{Li}\omega_{ci}$, so the ion rises about $5\,\rho_{Li}$ in half a
  toroidal turn.
- Checked off screen (`scripts/check-physics.py`), $v_{D,Z}/(\rho_{Li}\omega_{ci})$ [1], orbit against
  $(m_\alpha/q_\alpha BR)(v_\parallel^2+\tfrac12v_\perp^2)$: ion $+0.0381$ against $+0.0375$
  (+1.6 %), electron $-0.0373$ against $-0.0375$ ($-0.4$ %). The deviation is
  first order in $\rho_L/R_0$ (it halves when $R_0$ doubles and does not change
  with the time step).

**`magnetic-mirror`** (`animations/magnetic_mirror.py`, 24 s; page 25,
after the mirror-ratio and loss-cone page 24, which defines $\vartheta$,
$\vartheta_c$ and $R_m$).
- Computed: six ions of equal speed $v$, midplane pitch angles
  $18^\circ,26^\circ,29^\circ,31^\circ,45^\circ,70^\circ$, in
  $B_z=B_0[1+(R_m-1)(z/L_m)^2]$, $B_r=-\tfrac r2\,\partial_zB_z$ (divergence
  free), $R_m=4$, mirror half-length $L_m=30\,\rho_{L0}$ with $\rho_{L0}=v/\omega_{c0}$, each on its own field
  line; an ion counts as lost when it passes the field maximum $|z|=L_m$.
- Shown: $x/L_m$ against $z/L_m$ [1] at equal scale with the field lines; filled dot
  reflected, open ring lost at the throat. Critical angle from
  $\sin^2\vartheta_c=1/R_m$: $30^\circ$; the $29^\circ$ and $31^\circ$ ions sit on
  either side and behave accordingly. Lower left $B/B_0$ [1] (axis label above)
  against $z/L_m$ [1] (below); lower right the gyro-averaged $\mu/\mu_i$ [1] against
  $vt/L_m$ [1], $\mu_i$ the initial value. Pitch angle $\vartheta$, as $\alpha$ is the species index.
- Numbers: $\mu$ stays constant within 0.3 % for the reflected ions over
  $vt/L=6$ and within 1.6 % for the escaping ones; the reflection points lie
  at 0.97 to 0.99 of the guiding-centre value
  $z_b=L_m\sqrt{(1/\sin^2\vartheta-1)/(R_m-1)}$.

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
  $E/B=0.4\,v_\perp$ with $v_\perp$ the gyration speed in the drift frame; $\rho_L=v_\perp/|\omega_c|$;
  three turns, 400 steps per turn.
- Shown, one after the other in the same axes ($x/\rho_L$, $y/\rho_L$ [1]):
  the lab frame, a looped trochoid drifting along $+x$ with the $\mathbf v_D$
  arrow; then $(x-v_Dt)/\rho_L$ [1], the frame moving with
  $\mathbf v_D=\mathbf E\times\mathbf B/B^2$, labelled
  $\mathbf E'=\mathbf E+\mathbf v_D\times\mathbf B=0$, where the orbit is a circle.
- A green velocity arrow on the particle, drawn as $\mathbf v/\omega_c$ in $\rho_L$:
  in the lab $\mathbf v=\mathbf v_D+\mathbf v_\perp$ grows and shrinks,
  $v_\perp-v_D\le|\mathbf v|\le v_\perp+v_D$ (E speeds the ion up on one side, slows it
  on the other); in the drift frame $|\mathbf v_\perp|=v_\perp$, one $\rho_L$ long, with
  $\rho_L=v_\perp/|\omega_c|$ on screen.
- Otherwise only frame titles, field keys, the $\mathbf v_D$ arrow, axes and the
  clock $\omega_c t$ [1]; ion ($q_\alpha>0$) is spoken.
- Checked off screen (`scripts/check-physics.py`): drift from a least-squares fit
  $c+vt+a\cos\omega t+b\sin\omega t$ of the lab orbit, $v_{D,x}/(\rho_L\omega_c)=0.400000$
  against $E/(B\rho_L\omega_c)=0.400000$ (agree to $10^{-12}$); drift-frame radius
  constant to $3\times10^{-14}$ (round-off; the mean radius is $v_\perp/|\omega_c|$ to
  $3\times10^{-5}$, the $O(\Delta t^2)$ radius of the discrete circle).

**`gravity-drift`** (`animations/gravity_drift.py`, 14 s; page 14, after the
general-force-drift page 13).
- Computed: ion and electron in uniform $\mathbf B$ out of the page with
  $\mathbf g=-g\,\mathbf e_y$, $g=0.2\,\rho_{Li}\omega_{ci}^2$, six ion periods.
- Shown: both orbits in $x/\rho_{Li}$ [1]; the ion loops drift to $-x$, the
  electron band 16 times slower to $+x$.
- On screen only the $\mathbf B$ and $\mathbf g$ keys, the species labels, the
  $x/\rho_{Li}$ [1] axis, the formula
  $\mathbf v_D=(m_\alpha/q_\alpha)(\mathbf g\times\mathbf B)/B^2$ and the clock
  $\omega_{ci}t$ [1].
- Spoken: reduced mass ratio $m_i/m_e=16$ at $T_i=T_e$ (hydrogen: 1836), so the
  electron drift is 16 times slower here and 1836 times slower in hydrogen;
  $g=0.2\,\rho_{Li}\omega_{ci}^2$ is exaggerated to make the drift visible
  within six turns. The force $m_\alpha\mathbf g$ does not depend on the charge:
  opposite drifts, ratio $m_i/m_e$, a current carried by the ions.
- Checked off screen (`scripts/check-physics.py`), $v_{D,x}/(\rho_{Li}\omega_{ci})$ [1],
  orbit (slope of the gyro-period average) against
  $(m_\alpha/q_\alpha)(\mathbf g\times\mathbf B)_x/B^2$: ion $-0.20000$ against
  $-0.20000$, electron $+0.01250$ against $+0.01250$ (agree to $10^{-5}$ relative).

**`mu-ramp`** (`animations/mu_ramp.py`, 23 s; page 21, after the Faraday page 20).
- Computed: the scheme of `derivations/plot_mu_ramp.py` (page 22) with the
  trajectory kept: one ion centred on the axis of a uniform
  $B/B_0=\tfrac32+\tfrac12\tanh(t/\tau)$, $\omega_{c0}\tau=20$, shown from
  $t=-4\tau$ to $4\tau$ (38 gyrations), induced
  $\mathbf E=-\tfrac12\dot B\,\mathbf e_z\times\mathbf r$, 1600 steps per turn.
  $B_0$ is the field at the start of the window, $\rho_{L0}$ the starting radius.
- Shown: top view with dashed circles $\rho_{L0}$ and $\rho_{L0}/\sqrt2$, field
  symbols growing with $B$, the clockwise induced $\mathbf E$ (arrow length
  $\propto\dot B$); one full-width trace against $\omega_{c0}t$ [1] (ticks 0 to 160):
  $B/B_0$ and the orbit radius $\rho_L/\rho_{L0}$ with $(B/B_0)^{-1/2}$ dashed, the
  dashed-curve label clear of the curves. Setup: $\omega_{c0}\tau_B=20$, $\omega_{c0}=q_\alpha B_0/m_\alpha$.
  The former right panel ($\mu/\mu_0$ and the flux on a $\pm1\,\%$ scale) was flat and
  is dropped (2026-10-27); the invariants are the end numbers $|\mu/\mu_i-1|$ and
  $|\psi/\psi_i-1|$, $\psi=\pi\rho_L^2B$ the flux ($\Phi$ is the potential, $\mu_0$ the
  vacuum permeability, $\tau$ the collision time).
- Numbers: end $B/B_0=1.999$, $\rho_L/\rho_{L0}=0.7073=(B/B_0)^{-1/2}$ to
  $1.5\times10^{-5}$; $\max|\mu/\mu_i-1|=7.2\times10^{-5}$ (on screen $\le8\times10^{-5}$) and
  $\max|\psi/\psi_i-1|=5\times10^{-4}$ during the ramp (a
  reversible breathing of the orbit), $3\times10^{-8}$ and $3\times10^{-5}$ at
  the end. The flux uses the measured orbit radius, $\mu$ the measured speed.
  At $\omega_{c0}\tau=1,2$ the final $\mu$ equals `plot_mu_ramp.boris` to $10^{-13}$.

**`loss_cone`** plot (`derivations/plot_loss_cone.py`, page 26 "Loss cone in
velocity space", after the loss-cone derivation page 24 and the mirror animation page 25).
- Computed: 1500 particles of an isotropic Maxwellian at the midplane (seeded),
  $v_\parallel$, $v_\perp$ in $v_\mathrm{th}=(2k_BT/m_\alpha)^{1/2}$ [1]; field
  $B(z)/B_0=1+(R_m-1)(z/L_m)^2$, $R_m=4$. Trapped if
  $v_\parallel^2(z)=v^2-v_{\perp0}^2B(z)/B_0$ (from $\mu$ and $W$) reaches zero for
  $|z|\le L_m$, tested on a grid of $z$, without the cone formula.
- Shown: left, trapped (blue circles) and lost (vermilion triangles) in the
  $(v_\parallel, v_\perp)$ plane with the cone lines $\sin^2\vartheta_c=1/R_m$ (labelled
  "loss cone"); right, lost fraction against $R_m$ [1] from $2\times10^5$ particles per
  point, with $1-\sqrt{1-1/R_m}$ dashed (labelled "solid angle"). The formulas are
  on the page only, once; limits $|v_\parallel|\le2.9\,v_{\rm th}$ and $R_m\le21$ so no
  point is clipped (largest sample $|v_\parallel|=2.65\,v_{\rm th}$).
- Numbers: at $R_m=4$, 14.3 % of the 1500 shown are lost (formula 13.4 %);
  the large samples agree with the formula to $\le1.2\times10^{-3}$ (one binomial
  standard deviation) for $R_m=1.25\dots20$. `derivations/test_chapters.py`
  (`test_loss_cone_sample_against_pitch_angle`) checks the test particle by
  particle against $\sin^2\vartheta\ge1/R_m$.

**`polarization-drift`** (`animations/polarization_drift.py`, 17 s; page 32,
after the polarization page 31).
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

`animations/cyclotron_resonance.py` (`cyclotron-resonance`, 31 s; page 35,
after the derivation page 34): uniform B out of the page, uniform field
rotating clockwise (s = +1) or counterclockwise (s = -1), particle from rest,
Boris push (`drift_models.boris_em`), 400 steps per gyration, 6 gyrations
per run; each species normalized with its own abs(omega_c) (speed v B/E_0,
time abs(omega_c) t, all [1]), so the electron run is the mirror image of the
ion run. Dashed: the closed form 2 abs(sin(Delta t/2)/Delta).
Checks (`CyclotronResonancePhysics`): orbit speed equals the closed form to
0.6 dt (half-step start); RK4 of the complex equation equals it to 1e-8;
growth rate 0.99994 abs(q) E_0/m (ion and electron), W proportional to t^2
(log-log slope 2 within 0.01); detuned peak 10.0005 (formula 10); counter-rotating
peak 1.0000 for both species (formula 1). The page-34 closed form was also
checked with SymPy (ODE residual 0, v_cw(0) = 0, modulus, Delta -> 0 limit).
Note: from rest the speed grows linearly and the energy quadratically in time;
the absorbed power, not the energy, grows linearly.

