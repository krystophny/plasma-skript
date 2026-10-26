# Visuals for chapters 7 to 12

These chapters have no decks yet. The visuals below are ready for the script
and for later decks: Manim scenes in the dark animation style (MP4 and poster
registered in `media/animations.json` with a supplementary description that
places each on its chapter page, posters in `media/posters/`) and plots in
`derivations/build/fig/`. Each is computed from first principles and checked
against an analytic result; `scripts/check-physics.py` (animations) and
`derivations/test_chapters.py` (plots) repeat the checks independently.
Notation: $q_\alpha$, $m_\alpha$, signed $\omega_{c\alpha}=q_\alpha B/m_\alpha$,
$\rho_L$, $v_D$; normalized quantities carry [1].

### Chapter 7 · Moments

**`moment-weights`** (plot, `derivations/plot_moment_weights.py`,
`build/fig/moment-weights.{svg,pdf}`; script section `moments-definitions`,
equations `moments-number-density`, `moments-fluid-velocity`,
`moments-pressure-tensor`, `moments-heat-flux`).
- Computed: a one-dimensional $f(v)$ of species $\alpha$, core Maxwellian
  plus warm beam, $(n_j/n_0,\,u_j/v_t,\,v_j/v_t)=(0.8,0,1)$ and $(0.2,2.5,0.6)$:
  shifted, heated and skewed. Four panels show the integrands $f$, $vf$,
  $w^2f$ and $w^3f$ with $w=v-u$; each area is a trapezoidal quadrature.
- Shown: positive area filled, negative area hatched (not colour alone), $f$
  dotted for reference, dashed line at the flow $u$; the area is printed in
  each panel.
- Units: $v/v_t$ [1] with $v_t=(k_BT_c/m_\alpha)^{1/2}$ of the core;
  integrands in $n_0v_t^{k-1}$, labelled with [1].
- Numbers: $n=1.000\,n_0$, $nu=0.500\,n_0v_t$, $nk_BT/m_\alpha=1.872\,n_0v_t^2$,
  $2q/m_\alpha=0.732\,n_0v_t^3$; the closed form for a sum of drifting
  Maxwellians agrees to $\le 6\times10^{-10}$. The heat flux is a small
  difference of two large lobes: the beam carries energy forward, the core
  returns it more slowly.

### Chapter 8 · Multiple-fluid theory

**`diamagnetic-drift`** (`animations/diamagnetic_drift.py`, 21 s, plays once;
chapter 8, section `multiple-diamagnetic-current`).
- Computed: about 690 ions on exact Lorentz-force circles in uniform
  $\mathbf B=B\,\hat{\mathbf z}$ (out of the page), $E=0$, signed
  $\omega_{c\alpha}=q_\alpha B/m_\alpha>0$ (clockwise), one $v_\perp$, so one $\rho_L$.
  The guiding centres $\mathbf R=\mathbf x+(m_\alpha/q_\alpha)\,\mathbf v\times\mathbf B/B^2$ are fixed on a
  deterministic Fibonacci lattice with $n(y)=n_0(1+y/L)$, $L=5\,\rho_L$,
  $n_0=12\,\rho_L^{-2}$; gyrophases from a second irrational sequence.
- Measured: six lines $x=-2.5,\dots,2.5\,\rho_L$, bins of height $\rho_L$; each sign
  change of $x(t)-x_{\rm line}$ (400 steps per gyration) counts $\pm1$. One
  uncounted gyration, then two counted ones.
- Shown: ion triangles, four highlighted circles with their fixed guiding
  centres (crosses), $\nabla n$ arrow, the counting lines; right: net crossings
  per line and bin against the same $y$, with the growing expectation
  $-\pi\rho_L^2\,\partial_y n\,\Delta y\,\omega_c t/2\pi$ dashed. Each ion crosses
  rightward at the top of its circle and leftward at the bottom; more ions above
  than below, so leftward wins although nothing drifts.
- Units: $x/\rho_L$, $y/\rho_L$ [1], $\omega_c t/2\pi$ [1], $j_x/(q_\alpha n_0 v_\perp)$ [1].
- Numbers: $j_x/(q_\alpha n_0 v_\perp)=-0.0999$ (mean over bins and lines) against
  $\mathbf j_{\rm dia}=\mathbf B\times\nabla p/B^2=-\rho_L/(2L)=-0.100$ with $p=n m_\alpha v_\perp^2/2$;
  single bins $-0.086\dots-0.111$ (finite ion number; the counts repeat
  exactly every period, so they do not average down in time). The current is
  uniform in $y$ although $n$ changes by a factor 9: it follows $\nabla p$, not $n$.

### Chapter 9 · Single-fluid theory and MHD

**`frozen-flux`** (`animations/frozen_flux.py`, 25 s, plays once; script
section `mhd-flux`, Chapter 9).
- Computed: the 2D resistive induction equation for the flux function,
  $\partial_tA_z+\mathbf u\cdot\nabla A_z=D_B\nabla^2A_z$ with
  $\mathbf B=\nabla A_z\times\hat{\mathbf z}$, pseudo-spectral on a periodic box of
  side $2\pi L$ (192², 2/3 dealiasing, RK4 advection, exact diffusion factor).
  Prescribed vortex $\mathbf u=\nabla\times(UL\sin(x/L)\sin(y/L)\,\hat{\mathbf z})$.
  Start: Gaussian $A_z=A_0e^{-r^2/2\sigma^2}$, $\sigma=0.35L$, centred $0.55L$
  right of the cell centre (a loop of closed field lines). 24 fluid elements
  on the line $A_z=A_0/2$, moved with $\mathbf u$ (RK4).
- Parameters: $R_m=UL/D_B=10^4$, then $R_m=10$ from the same state, each to
  $tU/L=8$.
- Shown: one vortex cell, $x/L$, $y/L$ [1]; solid field lines at
  $A_z/A_0=0.03,0.1,0.3,0.5,0.8$ (the traced line bold), dashed streamlines,
  triangles = fluid elements; readout $\max A_z/A_0$ [1]; right: mean $A_z$ at
  the elements over its start value [1] against $tU/L$ [1], solid for
  $R_m=10^4$, dashed for $R_m=10$.
- What to see: at $R_m=10^4$ the loop is wound into a spiral and the elements
  stay on their field line (flux between field lines moves with the fluid);
  at $R_m=10$ the elements are wound the same way but the field diffuses
  through them and the loop spreads over the cell.
- Numbers: $R_m=10^4$: $A_z$ at the elements within 2.6 % (mean 0.993) of the
  start value, $\max A_z/A_0=0.984$ at $tU/L=8$, against 0.987 for the pure
  diffusion of the Gaussian. $R_m=10$: 0.11 and 0.064. A single Fourier mode
  without flow decays with e-folding time $1/(D_Bk^2)$ to $10^{-12}$.

**`alfven-wave`** (`animations/alfven_wave.py`, 24 s; script section
`mhd-linearized`, Chapter 9 — the chapter does not yet derive the shear
Alfvén wave or define $v_A$).
- Computed: linearized ideal MHD on uniform $\mathbf B_0=B_0\hat{\mathbf x}$, shear
  polarization, $\rho\,\partial_t\delta u_y=(B_0/\mu_0)\partial_x\delta B_y$,
  $\partial_t\delta B_y=B_0\partial_x\delta u_y$, staggered leapfrog (800 cells,
  Courant 0.5), line tied at $x=0,L$; field line $y=\xi_y(x,t)$ with
  $\delta B_y=B_0\partial_x\xi_y$. Pluck: Gaussian $\xi_y$, centre $0.3L$, width
  $0.035L$, at rest.
- Parameters: $\rho=\rho_0$, then $\rho=4\rho_0$, each to $tv_{A0}/L=0.6$,
  $v_{A0}=B_0/\sqrt{\mu_0\rho_0}$.
- Shown: $\xi_y/\xi_0$ [1] against $x/L$ [1]; field line, white fluid elements
  (move only along $y$), dashed markers at $x_0\pm v_At$; measured speed after
  each run.
- What to see: the pluck splits into two pulses at $\pm v_A$, the left one
  reflects inverted at the tied end; four times the density halves the
  speed.
- Numbers: pulse-peak speed $0.99988\,v_{A0}$ against $v_A=v_{A0}$, and
  $0.49994\,v_{A0}$ against $0.5\,v_{A0}$ ($-1.2\times10^{-4}$, second order
  in the grid spacing: $-4.8\times10^{-4}$ at 400 cells, $-3\times10^{-5}$ at
  1600). Before reflection the solution agrees with d'Alembert's within
  $5\times10^{-3}\,\xi_0$.

### Chapter 10 · Collisions and conductivity

**`spitzer-resistivity`** (plot, `derivations/plot_spitzer_resistivity.py`,
`build/fig/spitzer-resistivity.{svg,pdf}`; script section
`specific-resistivity`).
- Computed: NRL Plasma Formulary (`nrl2019`) transverse Spitzer resistivity
  $\eta_\perp=1.03\times10^{-4}\,Z\ln\Lambda\,(k_BT_e/\mathrm{eV})^{-3/2}\,\Omega\,$m and,
  for $Z=1$, $\eta_\parallel=0.51\,\eta_\perp$; $\ln\Lambda$ is the formulary's
  electron–ion $\lambda_{ei}(n_e,T_e)$.
- Parameters: curves at $n_e=10^{20}\,$m$^{-3}$, $Z=1$, $0.5\,$eV to $30\,$keV;
  dots are $\eta_\parallel$ of four example plasmas (`si.EXAMPLE_PLASMAS`) at their
  own $n_e$: H II region ($\ln\Lambda=19.5$, $1.0\times10^{-3}\,\Omega\,$m),
  Hall thruster (13.2, $7.7\times10^{-6}$), solar corona (18.2,
  $9.6\times10^{-7}$), tokamak core (17.1, $9.0\times10^{-10}$).
- Copper at 293 K, $1.68\times10^{-8}\,\Omega\,$m (Matula 1979,
  doi:10.1063/1.555614), dotted: plasmas cross it near 1–2 keV; a 10 keV
  core conducts about 20 times better than copper.
- Units: $k_BT_e$ in eV, $\eta$ in $\Omega\,$m, log–log.
- Check: the formulary coefficient equals $m_e/(ne^2\tau_e)$ with its
  $\tau_e$ to 0.13 %, and its Gaussian form $1.15\times10^{-14}\,$s gives the same.

**`small-angle-deflections`** (`animations/small_angle_deflections.py`, 20 s,
plays once; Chapter 10, section `coulomb-collisions`, after the definition
"Coulomb logarithm and electron--ion rate").
- Computed: 12 000 test electrons cross fixed singly charged ions (infinitely
  heavy) along straight paths; per path a Poisson number of encounters with
  impact parameter $b$ uniform in area on $[0,b_{\max}]$, each deflecting by the
  exact Rutherford angle $\tan(\theta/2)=b_{90}/b$,
  $b_{90}=|q_\alpha q_\beta|/(4\pi\varepsilon_0 m_\alpha v^2)$, in a random azimuth;
  the accumulated deflection is the vector sum of the kicks (small-angle
  accumulation, as in the script's derivation).
- Parameters: $b_{\max}=10^3\,b_{90}$ ($\ln\Lambda=\ln(b_{\max}/b_{90})=6.91$),
  path length up to $s=0.005\,\lambda_{90}$, $\lambda_{90}=1/(n\pi b_{90}^2)$, about
  5000 encounters per electron, about 60 strong ones ($b<b_{90}$) in the whole
  ensemble; seed 11.
- Shown: left, the deflection plane $\Delta\theta_x$, $\Delta\theta_y$ [rad] with 70
  electrons as dots and three trails; one ringed electron meets a strong
  encounter and jumps by about $90^\circ$. Upper right, $\langle\Delta\theta^2\rangle$ [rad²]
  against $s/\lambda_{90}$ [1] with the analytic line. Lower right, the
  contribution of each decade of $b/b_{90}$ [1] with the exact quadrature as a
  green tick: the three weak decades are almost equal (each $\to 8\ln 10$), the
  strong bar is small.
- Numbers: slope $59.2\pm0.9$ (standard error) against
  $8(\ln\Lambda+C)=57.4$ per $\lambda_{90}$, $C=0.266$ the strong-encounter constant
  of the exact Rutherford angle (+3.1 %, 1.9 standard errors); leading log
  $8\ln\Lambda=55.3$. Decades $1$–$10$, $10$–$10^2$, $10^2$–$10^3$: $16.10$, $18.41$,
  $18.41$ against $16.46$, $18.39$, $18.42$; $b<b_{90}$: $4.8$ against $4.12$
  (Poisson noise of about 60 events), i.e. 7 % of the total.
- Message: the many weak, distant encounters dominate; $\ln\Lambda$ counts the
  decades of $b$ between $b_{90}$ and the screening cutoff.

### Chapter 11 · Plasma diffusion

**`ambipolar-expansion`** (`animations/ambipolar_expansion.py`, 22 s, plays
once; Chapter 11, section `ambipolar-diffusion`, after the governing law
"Ambipolar field and diffusion coefficient").
- Computed: 1D drift-diffusion fluids,
  $\Gamma_i=\mu_i n_iE-D_i\partial_xn_i$, $\Gamma_e=-\mu_e n_eE-D_e\partial_xn_e$, with
  continuity and Poisson's equation $\partial_xE=e(n_i-n_e)/\varepsilon_0$, Einstein
  relations $D_\alpha=\mu_\alpha k_BT_\alpha/e$; finite volumes with
  Scharfetter–Gummel fluxes, explicit steps, closed box $|x|<10L$.
- Parameters: $\mu_e/\mu_i=50$, $T_e/T_i=2$ ($D_e=100\,D_i$), $L/\lambda_{De}=10$,
  initial $n_e=n_i=n_0$ on $|x|<L$ (edges smoothed over $0.05L$), $tD_i/L^2$ from
  $10^{-5}$ to $1.5$ on a logarithmic clock.
- Shown: $n_\alpha/n_0$ [1] (electrons solid with dots, ions dashed with
  triangles) and $eEL/(k_BT_e)$ [1] against $x/L$ [1]; right, log–log
  variance growth $(\sigma^2-\sigma_0^2)/L^2$ [1] against $tD_i/L^2$ [1] with the lines
  $2D_et$, $2D_at$, $2D_it$. The electrons start on $2D_et$ and run ahead, the
  edge field spikes ($|E|\approx 5.7\,k_BT_e/(eL)$ at $tD_i/L^2\approx10^{-3}$) pull
  them back and drag the ions, and both species then follow $2D_at$.
- Numbers: slab coefficient (ion variance slope, $tD_i/L^2\ge0.3$)
  $D=2.87\,D_i$ against $D_a=(\mu_iD_e+\mu_eD_i)/(\mu_i+\mu_e)=2.94\,D_i$
  ($\approx D_i(1+T_e/T_i)=3D_i$), −2.4 %. The gap is the finite Debye length: at
  $L/\lambda_{De}=20$ and $40$ it falls to −0.84 % and −0.28 %. The core field agrees
  with $E_a=[(D_i-D_e)/(\mu_i+\mu_e)]\,\partial_xn/n$ within 0.25 %. A small electron
  halo outside the slab (density ~$10^{-3}n_0$) keeps the electron variance
  above the ion variance by a constant.

**`magnetized-random-walk`** (`animations/magnetized_random_walk.py`, 23 s;
chapter 11, section `cross-field-diffusion`).
- Computed (event-driven, exact circles between collisions): ions with fixed
  $v_\perp$, Poisson collisions at rate $\nu=0.1\,\omega_{c0}$ that redraw the
  velocity direction isotropically in the perpendicular plane. Each collision
  moves the guiding centre by $\Delta\mathbf R=(m_\alpha/q_\alpha)\,\Delta\mathbf v\times\mathbf B/B^2$,
  $\langle|\Delta\mathbf R|^2\rangle=2\rho_L^2$.
- Part 1: one ion at $B_0$ for $\omega_{c0}t=120$ (14 collisions): orbit, collision
  stars, guiding-centre polyline jumping by about $\rho_L$.
- Part 2: 4000 ions each at $B/B_0=1,2,4$ (same collision sequence) to
  $\omega_{c0}t=400$ (about 40 collisions each); $\langle|\Delta\mathbf R|^2\rangle$ grows linearly,
  dashed $4D_\perp t$; then $D_\perp$ against $B$ on log axes with the line
  $\nu\rho_L^2/2\propto B^{-2}$.
- Units: $x/\rho_{L0}$, $y/\rho_{L0}$ [1], $\omega_{c0}t$ [1],
  $\langle|\Delta\mathbf R|^2\rangle/\rho_{L0}^2$ [1], $D_\perp/(\rho_{L0}^2\omega_{c0})$ [1],
  $\rho_{L0}=v_\perp/\omega_{c0}$.
- Numbers: $D_\perp$ (slope/4 of the mean square displacement over the last 3/4
  of the run) $0.0496$, $0.0127$, $0.00304$ against the exact
  $v_\perp^2\nu/[2(\nu^2+\omega_c^2)]=0.0495$, $0.0125$, $0.00312$ ($+0.2$, $+1.9$,
  $-2.6$ %, sampling error of 4000 ions); fitted exponent $-2.01$ (exact $-1.99$
  with the $\nu^2/\omega_c^2$ correction). The exact coefficient is the script's
  $D_\perp=D/(1+\omega_c^2/\nu^2)$ with the unmagnetized $D=v_\perp^2/(2\nu)$ of this
  2D model; along $\mathbf B$ nothing is slowed, $D_\parallel\sim v_{\rm th}^2/\nu$, so
  $D_\perp/D_\parallel\sim(\nu/\omega_c)^2$.

### Chapter 12 · Introduction to waves

**`em-wave-packet`** (`animations/em_wave_packet.py`, 21 s, plays once;
script section `wave-dispersion`).
- Computed: a Gaussian packet of transverse waves with
  $\omega^2=\omega_{pe}^2+c^2k^2$, $ck_0/\omega_{pe}=1$, spectral width
  $0.1\,\omega_{pe}/c$ (envelope width $10\,c/\omega_{pe}$), each Fourier mode
  advanced with its own $\omega(k)$ on a periodic grid of 4096 cells over
  $400\,c/\omega_{pe}$. Nothing is drawn at a prescribed speed: one crest is
  followed as a local maximum, the envelope as the maximum of $|E|$.
- Shown: top, $E/E_0$ [1] against $x\,\omega_{pe}/c$ [1] with the envelope dashed;
  dot = tracked crest, triangle = envelope peak, dashed vertical = light
  front $x_0+ct$. The crest starts behind the light front and overtakes it,
  the envelope falls behind. Bottom left, the dispersion curve with the light
  line, chord to $(k_0,\omega_0)$ (slope $v_\varphi$) and tangent (slope $v_g$).
- Units: $x\,\omega_{pe}/c$, $\omega_{pe}t$, $ck/\omega_{pe}$, $\omega/\omega_{pe}$, $E/E_0$, all [1].
- Numbers on screen: $v_\varphi/c=1.406$ (theory 1.414), $v_g/c=0.705$
  (0.707), $v_\varphi v_g/c^2=0.991$. The 1 % deficit is the finite spectral
  width (the crest crosses a chirped packet): with half the width the
  numbers become 1.413, 0.7064 and 0.998, and the local $\omega,k$ at the envelope centre satisfy the
  dispersion relation to 0.5 %.
