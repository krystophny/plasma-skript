#import "../theme.typ": *
#import "../figures.typ": wave-linearization, wave-dispersion, warm-kinetic-limits
#import "@preview/physica:0.9.8": div, grad, pdv, dv, curl
#import "@preview/unify:0.8.1": qty, unit

#let chapter = [
  #page-title[11. Introduction to waves in plasmas] <introduction-waves>

  #lead[
    A plasma wave is a collective perturbation whose restoring force and
    inertia are distributed among charged particles and fields. This chapter
    establishes the common language for the later wave chapters: equilibria,
    linearization, plane-wave response, dispersion, and controlled limits.
    The chapter follows the standard progression from small-amplitude wave
    properties to non-magnetized plasma modes in @bittencourt2004.
  ]

  #callout(
    [Selecting a wave branch],
    [The same plasma can support an electrostatic oscillation, a transverse
    electromagnetic wave, or an ion-acoustic response. The equilibrium,
    polarization, frequency, wavelength, and closure select the branch.]
  )

  #section-title[Equilibrium, perturbation, and linearization] <wave-linearization>

  #lead[
    How do we turn a nonlinear plasma model into a wave problem? Choose an
    equilibrium, assign a small parameter to every perturbation, retain terms
    through first order in that parameter, and then test sinusoidal
    solutions. The discarded products are precisely where finite-amplitude
    wave coupling would enter.
  ]

  #objectives((
    [state the homogeneous equilibrium and its ordering assumptions],
    [linearize continuity, momentum, and Maxwell equations consistently],
    [use a plane-wave ansatz to replace derivatives by algebraic operators],
    [distinguish longitudinal, transverse, electrostatic, and electromagnetic response],
  ))

  #unit-ledger[
    The phase $bold(k) dot bold(r)-omega t$ and normalized variables such as
    $omega/omega_(p,e)$ are dimensionless.
  ]

  #assumption(
    [Uniform, stationary, neutral equilibrium],
    [Use $n_s=n_(s,0)$, $bold(u)_(s,0)=bold(0)$, constant $p_(s,0)$, and
    $bold(E)_0=bold(0)$. The background magnetic field $bold(B)_0$ may be
    retained for the general linear equation, but the unmagnetized examples
    below set $bold(B)_0=bold(0)$. Macroscopic charge neutrality means
    $sum_s q_s n_(s,0)=0$.]
  )

  #definition(
    [Perturbation and plane-wave convention],
    [Introduce a bookkeeping parameter $epsilon << 1$ and write
    $n_s=n_(s,0)+epsilon n_(s,1)$,
    $bold(u)_s=epsilon bold(u)_(s,1)$,
    $bold(E)=epsilon bold(E)_1$, and
    $bold(B)=bold(B)_0+epsilon bold(B)_1$.
    A complex amplitude represents the real field through
    $bold(A)_1(bold(r),t)=Re{tilde(bold(A))_1
    exp(i (bold(k) dot bold(r)-omega t))}$.
    The wave number $k=abs(bold(k))$ is in #unit("m^-1") and the
    angular frequency $omega$ is in #unit("s^-1").]
  )

  Polarization describes the direction and time evolution of the electric
  perturbation. A longitudinal electric field is parallel to $bold(k)$;
  a transverse one is perpendicular to it. For a plane wave at nonzero
  frequency, a purely longitudinal field has no magnetic perturbation by
  Faraday's law and is electrostatic in this sense. A transverse electric
  wave has an accompanying magnetic perturbation even when the equilibrium
  field is zero.

  Acting on the complex plane wave, a time derivative multiplies its
  amplitude by $-i omega$, and a spatial gradient multiplies it by
  $i bold(k)$. These replacements turn the differential equations into
  algebraic equations for the amplitudes. A dispersion relation specifies
  which frequencies and wave vectors allow a nonzero solution.

  The species equations and Maxwell equations that are linearized are

  $ pdv(n_s,t)+div(n_s bold(u)_s)=0 $

  $ m_s n_s (pdv(bold(u)_s,t)+bold(u)_s dot grad(bold(u)_s))
    =q_s n_s (bold(E)+bold(u)_s times bold(B))-grad(p_s) $

  $ curl(bold(E))=-pdv(bold(B),t), quad
    curl(bold(B))=mu_0 bold(j)+mu_0 epsilon_0 pdv(bold(E),t) $

  $ div(bold(E))=rho_q/epsilon_0, quad
    div(bold(B))=0 $

  where $rho_q=sum_s q_s n_s$ and
  $bold(j)=sum_s q_s n_s bold(u)_s$. For an adiabatic or isothermal closure,
  the pressure perturbation is written
  $p_(s,1)=gamma_s k_B T_s n_(s,1)$, with the appropriate temperature
  ordering stated explicitly. The dimensionless coefficient $gamma_s$
  specifies the pressure response; $gamma_s=1$ gives an isothermal response.
  It must be chosen for the process being modeled, not inferred from small
  amplitude alone.

  #details(
    [Derivation: linearized Fourier system],
    [#derivation-step[Classify the perturbation order]
    The equilibrium has no flow. Consequently, products of two first-order
    quantities are second order and do not appear in the linear problem. In
    particular, the convective term and the perturbed magnetic force are
    omitted at first order.

    #derivation-step[Linearize continuity and momentum]
    The continuity equation becomes

    $ pdv(n_(s,1),t)+n_(s,0) div(bold(u)_(s,1))=0 .$

    The first-order momentum equation retains the equilibrium magnetic field
    but not the product of two perturbations:

    $ m_s n_(s,0) pdv(bold(u)_(s,1),t)
      =q_s n_(s,0)(bold(E)_1+
      bold(u)_(s,1) times bold(B)_0)-grad(p_(s,1)) .$

    #derivation-step[Apply the plane-wave replacement]
    For the convention
    $exp(i (bold(k) dot bold(r)-omega t))$, replace derivatives by
    algebraic operators:

    $ pdv(f,t) -> -i omega f, quad
      grad(f) -> i bold(k) f, quad
      div(bold(A)) -> i bold(k) dot bold(A), quad
      curl(bold(A)) -> i bold(k) times bold(A) .$

    Thus continuity and momentum become

    $ -i omega n_(s,1)+i n_(s,0) bold(k) dot bold(u)_(s,1)=0 $

    and

    $ -i omega m_s n_(s,0) bold(u)_(s,1)
      =q_s n_(s,0)(bold(E)_1+
      bold(u)_(s,1) times bold(B)_0)-i bold(k) p_(s,1) .$

    #derivation-step[Form the dispersion condition]
    Maxwell's equations receive the same algebraic replacement. Equilibrium
    neutrality removes the zeroth-order charge density. The remaining linear
    equations form a coefficient matrix for the field and fluid amplitudes.
    A nonzero wave exists only when this matrix is singular; its determinant
    is the dispersion relation.]
  )

  #wave-linearization

  #rechenbeispiel[
    A homogeneous hydrogen plasma has equilibrium density
    $n_(e,0)=n_(i,0)=qty("1.0e16", "m^-3")$, electron temperature energy
    $k_B T_e=qty("1.0", "eV")=qty("1.602e-19", "J")$, and a density perturbation with
    relative amplitude #normalized-label[$(delta n_e)/n_(e,0)=qty("2.0e-2", "1")$]. Use
    $e=qty("1.602e-19", "C")$, $m_e=qty("9.109e-31", "kg")$,
    $epsilon_0=qty("8.854e-12", "F/m")$, and a
    wavelength $lambda=qty("0.10", "m")$ at angular frequency
    $omega=qty("1.0e10", "s^-1")$, with $k=(2 pi)/lambda$.

    Assumptions: cold fixed-ion ordering for the plasma-frequency estimate
    and small-amplitude perturbation.

    Target: report the perturbation parameter, Debye-scale ordering
    $k lambda_D$, and frequency ordering $omega/omega_(p,e)$.

    Numerical result: #normalized-label[$epsilon=qty("2.0e-2", "1")$],
    $lambda_D=qty("7.43e-5", "m")$,
    #normalized-label[$k lambda_D=qty("4.67e-3", "1")$],
    $omega_(p,e)=qty("5.64e9", "s^-1")$, and
    #normalized-label[$omega/omega_(p,e)=qty("1.77", "1")$].
  ]

  #interpretation(
    [Amplitude ordering and regime ratios],
    [The small parameter controls amplitudes, while the ratios
    $omega/(k v_"th")$, $omega/omega_(p,e)$, and
    $k lambda_D$ control the physical regime. A perturbation can be small
    and still be kinetic, magnetized, or strongly dispersive.]
  )

  #summary[
    A homogeneous equilibrium plus a first-order expansion turns the fluid
    and Maxwell system into a linear algebra problem. The plane-wave
    replacement gives an algebraic response, and the determinant condition
    selects the allowed wave branches.
  ]

  #knowledge-check((
    (
      question: [Why must the equilibrium be specified before linearizing a plasma model?],
      answer: [The equilibrium determines which zeroth-order forces cancel and
      which products are first or second order. Without it, terms such as
      background flow, background magnetic force, and charge density cannot be
      classified consistently.]
    ),
    (
      question: [What does the plane-wave ansatz do to a time derivative and a spatial gradient?],
      answer: [For the convention $exp(i (bold(k) dot bold(r)-omega t))$,
      $pdv(f,t)$ becomes $-i omega f$ and
      $grad(f)$ becomes $i bold(k) f$ when acting on the amplitude.]
    ),
    (
      question: [What is the difference between longitudinal and transverse polarization?],
      answer: [Longitudinal fields are parallel to $bold(k)$ and can create a
      charge-density perturbation. Transverse fields are perpendicular to
      $bold(k)$ and, in the plane-wave Maxwell system, have vanishing
      divergence of the electric field.]
    ),
    (
      question: [Why is a dispersion relation a determinant condition?],
      answer: [The linearized equations form a homogeneous matrix equation for
      the wave amplitudes. A nonzero solution exists only when the matrix is
      singular, so its determinant must vanish.]
    ),
  ))

  #section-title[Nonmagnetized response and plasma oscillations] <plasma-oscillations>

  #lead[
    What oscillates when a cold, unmagnetized plasma is displaced? In the
    high-frequency limit the electrons move against an almost fixed ion
    background. Charge separation creates an electric restoring force, so the
    oscillation frequency is set by density and charge, not by a spatial
    wavelength.
  ]

  #objectives((
    [derive the electron plasma frequency from continuity, momentum, and Poisson],
    [identify the restoring force in a cold electrostatic oscillation],
    [state the correction when both electron and ion inertia are retained],
    [separate a localized plasma oscillation from a propagating wave],
  ))

  #unit-ledger[
    The plasma frequency $omega_(p,e)$ is in #unit("s^-1"). The normalized
    displacement $xi/xi_0$ and time $omega_(p,e) t$ are dimensionless.
  ]

  #assumption(
    [Cold, unmagnetized, collisionless electron response],
    [Use $bold(B)_0=bold(0)$, negligible pressure, negligible collisions,
    fixed singly charged ions, and a small longitudinal electric perturbation.
    The electron equilibrium density equals the ion equilibrium density
    $n_(e,0)=n_(i,0)=n_0$. Ion motion is added only as a stated extension.]
  )

  #definition(
    [Electron plasma frequency],
    [The electron plasma frequency is
    $omega_(p,e)=sqrt((n_0 e^2)/(epsilon_0 m_e))$.
    It is a local collective frequency. Since the cold longitudinal
    dispersion relation contains no $k$, this idealized oscillation has no
    group propagation.]
  )

  #governing-law(
    [Cold electrostatic plasma oscillation],
    [For a longitudinal perturbation with fixed ions,
    $omega^2=omega_(p,e)^2=(n_0 e^2)/(epsilon_0 m_e)$.
    If every species is allowed to move coherently, the restoring frequency
    becomes $omega_p^2=sum_s ((n_(s,0) q_s^2)/(epsilon_0 m_s))$.]
  )

  #details(
    [Derivation: charge separation supplies the restoring force],
    [#derivation-step[Write the electron response]
    For the electron charge $q_e=-e$, the cold linearized momentum equation is

    $ -i omega m_e bold(u)_(e,1)=-e bold(E)_1 .$

    Longitudinal continuity gives

    $ n_(e,1)=(n_0 (bold(k) dot bold(u)_(e,1)))/omega .$

    For a field parallel to $bold(k)$, this reduces to

    $ n_(e,1)=(n_0 k u_(e,1))/omega .$

    #derivation-step[Close the charge--field loop]
    The fixed ions do not contribute a perturbed charge. Poisson's equation
    is therefore

    $ i k E_1=rho_(q,1)/epsilon_0=-(e n_(e,1))/epsilon_0 .$

    Solving the momentum equation gives

    $ u_(e,1)=(-i e E_1)/(m_e omega) .$

    Inserting this response into continuity and then Poisson gives

    $ i k E_1=-e/epsilon_0 ((-i n_0 e k E_1)/(m_e omega^2)) .$

    #derivation-step[Identify the collective frequency]
    Cancel the nonzero field amplitude and the common factor $i k$:

    $ omega^2=(n_0 e^2)/(epsilon_0 m_e) .$

    The wave number disappears because the cold model has no pressure
    gradient and hence no spatial restoring scale. If the ions also move,
    repeat the response calculation for every species and add their charge
    responses. The result is

    $ omega_p^2=sum_s ((n_(s,0)q_s^2)/(epsilon_0 m_s)) .$

    For hydrogen, the ion contribution is smaller than the electron term by
    $m_e/m_i$.]
  )

  #rechenbeispiel[
    Assume a homogeneous, cold, collisionless, longitudinal electrostatic
    perturbation with fixed ions. For a cold
    hydrogen plasma use
    $n_0=qty("1.0e16", "m^-3")$,
    $e=qty("1.602e-19", "C")$,
    $m_e=qty("9.109e-31", "kg")$, and
    $epsilon_0=qty("8.854e-12", "F/m")$.
    Determine the electron plasma frequency and its ordinary frequency
    $f_p=omega_(p,e)/(2 pi)$.

    Numerical result:
    $omega_(p,e)=qty("5.64e9", "s^-1")$ and
    $f_p=qty("8.98e8", "s^-1")$.
  ]

  #interpretation(
    [A plasma oscillation can be local],
    [The electron slab can oscillate at every location without transporting
    information from one location to another in the cold fixed-ion limit.
    Pressure, magnetic coupling, boundaries, or kinetic phase mixing add the
    spatial dependence that turns the local oscillation into a propagating or
    damped mode.]
  )

  #summary[
    A displaced cold electron population creates a charge-separation field.
    This gives $omega_(p,e)^2=(n_0 e^2)/(epsilon_0 m_e)$.
    The frequency is collective and local in the cold fixed-ion limit; ion
    inertia adds the corresponding ion plasma-frequency contribution.
  ]

  #knowledge-check((
    (
      question: [What provides the restoring force for a cold electron plasma oscillation?],
      answer: [The electron displacement leaves a small charge imbalance.
      Poisson's equation turns that imbalance into an electric field that
      accelerates the electrons back toward neutrality.]
    ),
    (
      question: [Why does the cold fixed-ion plasma-oscillation frequency not contain the wave number?],
      answer: [The cold model has no pressure or other spatial restoring term.
      The charge-separation balance is local, so the frequency is independent
      of $k$ in this limit.]
    ),
    (
      question: [How does allowing the ions to move change the collective frequency?],
      answer: [Each mobile species contributes
      $(n_(s,0)q_s^2)/(epsilon_0 m_s)$ to the
      squared collective frequency. The ion contribution is usually small
      because the ion mass is large.]
    ),
    (
      question: [When does the cold plasma oscillation cease to be an adequate model?],
      answer: [Finite pressure, collisions, magnetic fields, finite amplitude,
      boundaries, or kinetic resonances can alter the response. The relevant
      ordering must be checked before using the cold local result.]
    ),
  ))

  #section-title[Phase velocity, group velocity, and electromagnetic dispersion] <wave-dispersion>

  #lead[
    How does a transverse electromagnetic disturbance differ from a local
    plasma oscillation? The fields must satisfy both Maxwell's equations and
    the current response of the electrons. The resulting branch has a cutoff
    and a wavelength-dependent phase and group velocity.
  ]

  #objectives((
    [define phase and group velocity for a one-dimensional branch],
    [derive the cold unmagnetized electromagnetic dispersion relation],
    [interpret the plasma cutoff and the evanescent regime],
    [explain why a phase velocity larger than $c$ does not transmit information],
  ))

  #unit-ledger[
    The velocities $v_"phi"$ and $v_"g"$ are in #unit("m/s"). The dielectric
    factor $epsilon_(r)$, $(k c)/omega_(p,e)$, and $omega/omega_(p,e)$ are
    dimensionless.
  ]

  #assumption(
    [Cold transverse response in an unmagnetized plasma],
    [Use a homogeneous, collisionless electron fluid with fixed ions,
    $bold(B)_0=bold(0)$, and $bold(k) dot bold(E)_1=0$. Retain the
    displacement current in Maxwell's equations. The current response is
    linear and isotropic.]
  )

  #definition(
    [Phase and group velocity],
    [For a branch $omega(k)$ with $k>0$, define
    $v_"phi"=omega/k$ and $v_"g"=dv(omega,k)$.
    Phase velocity tracks a constant phase surface. For a narrow-band packet
    in a weakly dispersive medium, group velocity describes the motion of its
    envelope; energy and information transport require the full causal
    medium and boundary conditions.]
  )

  #governing-law(
    [Cold electromagnetic branch],
    [The electron current produces
    $epsilon_(r)(omega)=1-omega_(p,e)^2/omega^2$ and
    $k^2 c^2=omega^2 epsilon_(r)$.
    Equivalently,
    $omega^2=omega_(p,e)^2+c^2 k^2$,
    $v_"phi"=c sqrt(1+omega_(p,e)^2/(c^2 k^2))$, and
    $v_"g"=(c^2 k)/omega$.]
  )

  The relative dielectric factor $epsilon_(r)$ summarizes how the induced
  electron current changes the electromagnetic response; vacuum has
  $epsilon_(r)=1$. It is distinct from the small perturbation parameter
  $epsilon$ used earlier. For a real drive frequency below the plasma
  frequency, this factor is negative, so $k$ is imaginary. A boundary-driven
  field then decays into the plasma instead of propagating as a bulk wave.

  #details(
    [Derivation: current response and the transverse wave equation],
    [#derivation-step[Compute the cold current response]
    The cold electron momentum equation gives

    $ -i omega m_e bold(u)_(e,1)=-e bold(E)_1 ,$

    and hence

    $ bold(u)_(e,1)=(-i e bold(E)_1)/(m_e omega) .$

    The perturbed current is

    $ bold(j)_1=-e n_0 bold(u)_(e,1)
      =(i n_0 e^2 bold(E)_1)/(m_e omega) .$

    #derivation-step[Eliminate the magnetic amplitude]
    For a transverse plane wave, Faraday's and Ampere's equations are

    $ bold(k) times bold(E)_1=omega bold(B)_1 $

    and

    $ bold(k) times bold(B)_1=-(omega bold(E)_1)/c^2
      -i mu_0 bold(j)_1 ,$

    with $c^2=1/(mu_0 epsilon_0)$.

    Substitute the first relation into the second and use

    $ bold(k) times (bold(k) times bold(E)_1)=-k^2 bold(E)_1 .$

    The resulting electric-field equation is

    $ (omega^2-c^2 k^2) bold(E)_1=-(i omega bold(j)_1)/epsilon_0 .$

    #derivation-step[Read off the electromagnetic branch]
    Insert the current response and define
    $omega_(p,e)^2=(n_0 e^2)/(epsilon_0 m_e):$

    $ (omega^2-c^2 k^2) bold(E)_1
      =omega_(p,e)^2 bold(E)_1 .$

    A nonzero field amplitude therefore requires

    $ omega^2=omega_(p,e)^2+c^2 k^2 .$

    Dividing by $omega^2$ identifies the relative dielectric factor:

    $ (k^2 c^2)/(omega^2)=1-omega_(p,e)^2/omega^2 .$

    Real $k$ requires $omega>omega_(p,e)$. Below the cutoff, $k$ is
    imaginary and the field is evanescent rather than a propagating bulk
    wave.]
  )

  #callout(
    [Pause and predict],
    [Before playing the animation, identify which marker should move faster:
    the carrier phase or the packet envelope. The answer follows from the
    two velocities in the governing law.]
  )

  #animation(
    "../media/wave-packet.mp4",
    "A prescribed Gaussian envelope and cosine carrier travel rightward in normalized coordinates. A stationary key identifies the slower dashed envelope marker and faster solid carrier-phase marker. Position is x/L0 [1] and field amplitude is E/E0 [1].",
    caption: [
      The prescribed carrier and envelope illustrate different phase and
      group speeds. With $X=x/L_0$, $tau=t/t_0$, and $A=E/E_0$, the ansatz is
      $A=exp(-(X-0.42 tau)^2/(2 (1.15)^2))
        cos(5.2 (X-0.90 tau))$.
      Here $L_0$, $t_0$, and $E_0$ are arbitrary reference length, time,
      and field scales; velocities are in units $L_0/t_0$.
      Thus $sigma/L_0=1.15$, $k L_0=5.2$,
      $(v_"g" t_0)/L_0=0.42$, and $(v_"phi" t_0)/L_0=0.90$ are
      prescribed dimensionless parameters. This ansatz is not an exact
      solution of the cold-plasma dispersion relation. The phase marker
      follows a cosine maximum; the varying envelope shifts the maxima of
      the total field.
    ],
    poster: "../media/wave-packet.png",
  )

  #rechenbeispiel[
    Assume the homogeneous, cold, collisionless, unmagnetized, fixed-ion
    transverse electromagnetic model. A cold electromagnetic
    wave has #normalized-label[$omega/omega_(p,e)=2$] in a plasma with
    $omega_(p,e)=qty("5.64e9", "s^-1")$ and
    $c=qty("2.998e8", "m/s")$.
    Determine $k$, the phase velocity, the group velocity, and the wavelength.

    Numerical result:
    #normalized-label[$(k c)/omega_(p,e)=qty("1.732", "1")$],
    #normalized-label[$v_"phi"/c=qty("1.155", "1")$],
    #normalized-label[$v_"g"/c=qty("0.866", "1")$],
    $k=qty("32.6", "m^-1")$, and
    $lambda=qty("0.193", "m")$.
  ]

  #interpretation(
    [Superluminal phase is not superluminal signalling],
    [For the cold branch $v_"phi" v_"g"=c^2$. A phase crest can move faster
    than $c$ because it is not a localized signal. The packet envelope,
    causal turn-on, and energy flow carry the physically relevant information
    and approach the vacuum limit consistently.]
  )

  #summary[
    The cold unmagnetized electromagnetic branch obeys
    $omega^2=omega_(p,e)^2+c^2 k^2$. It has a cutoff at $omega_(p,e)$,
    $v_"phi">c$, $v_"g"<c$, and the product
    $v_"phi"v_"g"=c^2$ in the propagating regime.
  ]

  #knowledge-check((
    (
      question: [What is the physical meaning of the phase velocity?],
      answer: [It is $v_"phi"=omega/k$, the speed of a constant phase surface.
      It need not equal the speed of a localized pulse or of information.]
    ),
    (
      question: [What condition allows the cold electromagnetic branch to propagate in the bulk plasma?],
      answer: [The wave number must be real, which requires
      $omega>omega_(p,e)$ in the fixed-ion cold model. Below the cutoff the
      solution is evanescent.]
    ),
    (
      question: [Why does the cold electromagnetic branch approach the vacuum branch at high frequency?],
      answer: [When $omega >> omega_(p,e)$, electron inertia makes the current
      response small relative to the displacement current. The dielectric factor approaches
      one and $omega approx c k$.]
    ),
    (
      question: [Why can the phase velocity exceed the speed of light in this model?],
      answer: [The phase surface is not a causal signal. For the branch,
      $v_"phi">c$ is accompanied by $v_"g"<c$; signal propagation is governed
      by the causal packet and medium response.]
    ),
  ))

  #section-title[Warm-fluid wave equations and kinetic limits] <wave-kinetic-limits>

  #lead[
    What changes when pressure and particle velocity spread are restored?
    A warm-fluid closure makes the restoring force depend on wavelength.
    The resulting branches include warm Langmuir and ion-acoustic limits,
    while kinetic theory adds resonant particles and phase mixing that no
    finite set of fluid moments can represent exactly.
  ]

  #objectives((
    [derive the warm electrostatic fluid susceptibility],
    [identify the warm Langmuir and ion-acoustic limits],
    [state the ordering behind the quasi-neutral ion-acoustic approximation],
    [explain what kinetic response adds beyond a fluid pressure closure],
  ))

  #unit-ledger[
    Thermal speed and ion-acoustic speed are in #unit("m/s"), and
    $lambda_D=sqrt((epsilon_0 k_B T_e)/(n_0 e^2))$ is in #unit("m"). The phase
    parameters $k lambda_D$ and $omega/(k v_"th,s")$ are dimensionless.
  ]

  #assumption(
    [Unmagnetized, electrostatic, warm-fluid closure],
    [Use $bold(B)_0=bold(0)$, a longitudinal electric field, collisionless
    perturbations, and a local pressure closure
    $p_(s,1)=gamma_s k_B T_s n_(s,1)$. The equilibrium is quasi-neutral
    with equal electron and ion densities. Kinetic corrections are discussed
    separately as a limit comparison.]
  )

  #definition(
    [Warm-fluid scales],
    [Define
    $c_s^2=(gamma_s k_B T_s)/m_s$ and
    $omega_(p,s)^2=(n_(s,0)q_s^2)/(epsilon_0 m_s)$.
    Here the index $s$ labels a species: $c_e$ and $c_i$ are its electron
    and ion pressure-response speeds. Neither is necessarily the phase
    velocity of a collective branch. The thermal-speed convention used for kinetic
    comparisons is $v_"th,s"=sqrt((2 k_B T_s)/m_s)$.]
  )

  #definition(
    [Plasma-dispersion function convention],
    [For a Maxwellian, the velocity integral in the kinetic response can be
    expressed using the dimensionless Fried--Conte function
    $Z(zeta)=1/sqrt(pi) integral_(-infinity)^infinity
      exp(-x^2)/(x-zeta) dif x$,
    initially defined for $Im(zeta)>0$ and continued causally to real and
    lower-half-plane frequencies. Here $x$ is a dimensionless integration
    variable for velocity, not position. The argument $zeta$ compares phase
    speed with thermal speed, as specified for each species below. For
    $k>0$ and $exp(-i omega t)$, deform
    the velocity contour below the pole as it crosses the real axis.
    The factor of two in the susceptibility below follows from the stated
    convention $v_"th,s"=sqrt((2 k_B T_s)/m_s)$.]
  )

  #governing-law(
    [Warm electrostatic fluid dispersion],
    [The longitudinal two-species warm-fluid dispersion relation is
    $1-sum_s omega_(p,s)^2/(omega^2-k^2 c_s^2)=0$.
    With fixed ions this gives
    $omega^2=omega_(p,e)^2+k^2 c_e^2$.
    In the low-frequency quasi-neutral hydrogen limit, requiring
    $omega << omega_(p,e)$, $k lambda_D << 1$, and
    $abs(omega/(k c_e)) << 1$ to neglect electron inertia relative to
    electron pressure,
    $omega^2 approx (k^2 (gamma_e k_B T_e+gamma_i k_B T_i))/m_i$.]
  )
  #details(
    [Derivation: warm-fluid susceptibility and ion sound],
    [#derivation-step[Obtain the response of one warm species]
    For one species in one dimension, Fourier continuity gives

    $ -i omega n_(s,1)+i k n_(s,0)u_(s,1)=0 .$

    Therefore

    $ n_(s,1)=(k n_(s,0)u_(s,1))/omega .$

    With the pressure closure, the longitudinal momentum equation is

    $ -i omega m_s u_(s,1)=q_s E_1
      -(i k gamma_s k_B T_s n_(s,1))/n_(s,0) .$

    Define $c_s^2=(gamma_s k_B T_s)/m_s$. Substitution of continuity and
    solution for the velocity gives

    $ u_(s,1)=(i q_s omega E_1)/
      (m_s (omega^2-k^2 c_s^2)) .$

    The density response is consequently

    $ n_(s,1)=(i n_(s,0)q_s k E_1)/
      (m_s (omega^2-k^2 c_s^2)) .$

    #derivation-step[Sum the species in Poisson's equation]
    The longitudinal field obeys

    $ i k E_1=1/epsilon_0 sum_s q_s n_(s,1) .$

    Cancel $i k E_1$ and insert the species response:

    $ 1=sum_s (n_(s,0)q_s^2)/
      (epsilon_0 m_s (omega^2-k^2 c_s^2)) .$

    This is the warm-fluid longitudinal dispersion relation.

    #derivation-step[Select the two-fluid limits]
    For a high-frequency electron branch with fixed ions, omit the ion term:

    $ omega^2=omega_(p,e)^2+k^2 c_e^2 .$

    For a low-frequency ion-acoustic branch, neglect electron inertia and
    impose $n_(e,1)=n_(i,1)$ through quasi-neutrality. Electron pressure then
    supplies the electric field and ion inertia carries the slow wave:

    $ omega^2=(k^2 (gamma_e k_B T_e+gamma_i k_B T_i))/m_i .$

    This reduction requires $omega << omega_(p,e)$,
    $k lambda_D << 1$, and $abs(omega/(k c_e)) << 1$.
    The last condition follows by comparing $omega^2$ with $k^2 c_e^2$
    in the electron susceptibility; it controls neglect of electron inertia
    relative to pressure. The Debye ordering controls charge separation.

    #derivation-step[Compare with kinetic response]
    Kinetic theory replaces the fluid closure by a velocity-space response.
    For isotropic, non-drifting Maxwellian equilibria of each responding
    species, with $v_"th,s"=sqrt((2 k_B T_s)/m_s)$, the unmagnetized
    electrostatic form is

    $ 1+sum_s chi_(s)(omega,k)=0 ,$

    where

    $ chi_s=(2 omega_(p,s)^2)/(k^2 v_"th,s"^2)
      (1+zeta_s Z(zeta_s)), quad
      zeta_s=omega/(k v_"th,s") .$

    The analytically continued plasma-dispersion function $Z$ accounts for
    resonant particles through causal continuation from $Im(omega)>0$.
    Other distributions require their own velocity-space integral. The imaginary contribution describes resonant
    energy exchange: the non-drifting Maxwellian response gives Landau
    damping, while suitable non-equilibrium distributions can drive growth.
    A warm-fluid $gamma_s$ can reproduce selected
    long-wavelength real-frequency limits, but it cannot reproduce resonant
    phase mixing.]
  )
  #warm-kinetic-limits

  In the following example, $c_s$ denotes the collective ion-acoustic speed,
  as is common in sound-wave notation. It is determined by electron pressure
  and ion inertia for the stated cold-ion limit, not by the ion
  pressure-response speed $c_i$ defined above.

  #rechenbeispiel[
    Assume an unmagnetized, electrostatic warm-fluid model with cold ions,
    an isothermal electron response, and quasi-neutral long-wavelength ordering.
    For cold ions and an isothermal electron response use
    $k_B T_e=qty("10", "eV")=qty("1.602e-18", "J")$,
    $m_i=qty("1.673e-27", "kg")$, and
    $k=qty("1.0", "m^-1")$.
    Determine the ion-acoustic speed, frequency, and the ratio
    $k lambda_D$ for $n_0=qty("1.0e16", "m^-3")$.
    Numerical result:
    $c_s=qty("3.09e4", "m/s")$,
    $omega=qty("3.09e4", "s^-1")$,
    $lambda_D=qty("2.35e-4", "m")$, and
    #normalized-label[$k lambda_D=qty("2.35e-4", "1")$].
  ]
  #interpretation(
    [Fluid and kinetic responses],
    [A warm-fluid dispersion relation is a controlled closure for selected
    moments and scales. A kinetic response resolves velocity-space structure,
    including resonant particles and Landau damping. Agreement of real
    frequencies in one limit does not make the models interchangeable.]
  )
  #summary[
    Pressure adds $k$-dependent restoring forces. The warm-fluid longitudinal
    response obeys
    $1-sum_s omega_(p,s)^2/(omega^2-k^2 c_s^2)=0$,
    whose limits include warm Langmuir and ion-acoustic waves. Kinetic
    response adds resonant velocity-space physics and collisionless damping.
  ]
  #knowledge-check((
    (
      question: [What new scale enters the warm-fluid electrostatic dispersion relation?],
      answer: [The pressure response introduces $k^2 c_s^2$, so the frequency
      depends on wavelength through the species pressure-response speed.]
    ),
    (
      question: [Why can an ion-acoustic wave be low frequency even though the electric field is produced by electrons?],
      answer: [Electrons establish the pressure-supported electric response
      quickly, while the large ion inertia carries the slow density motion.]
    ),
    (
      question: [Which ordering justifies the quasi-neutral ion-acoustic limit?],
      answer: [The mode must be slow compared with the electron plasma
      response and long compared with the Debye scale:
      $omega << omega_(p,e)$ and $k lambda_D << 1$. Neglecting electron
      inertia relative to pressure also requires $abs(omega/(k c_e)) << 1$.]
    ),
    (
      question: [What physical effect is absent from a finite warm-fluid closure?],
      answer: [A finite moment closure does not resolve resonant particles and
      their phase mixing. Kinetic response is needed for Landau damping or
      growth and for nonlocal velocity-space structure.]
    ),
  ))
  #section-title[Reading dispersion diagrams and checking limits] <dispersion-limits>
  #lead[
    How do we read a dispersion diagram without losing the assumptions?
    First normalize both axes, then identify real and imaginary wave numbers,
    slopes, cutoffs, and asymptotic branches.
  ]
  #objectives((
    [read cutoffs, slopes, and propagating regions from a dispersion plot],
    [use dimensionless variables to compare plasma and vacuum branches],
    [check long-wavelength, high-frequency, and weak-plasma limits],
    [identify when a branch is evanescent or when a fluid model has left its ordering],
  ))
  #unit-ledger[
    The normalized axes use $K=(k c)/omega_(p,e)$ and
    $W=omega/omega_(p,e)$, both dimensionless. The reconstructed wave number
    is in #unit("m^-1"), frequency in #unit("s^-1"), and velocities in
    #unit("m/s"). For warm electrostatic checks, $K_D=k lambda_D$ is also
    dimensionless.
  ]
  #assumption(
    [Validity range of the plotted branches],
    [Read the cold electromagnetic curve only for a homogeneous,
    unmagnetized, collisionless, fixed-ion plasma. The vacuum line is a
    reference. If a branch leaves the assumptions,
    switch model before extrapolating the curve.]
  )
  #definition(
    [Dimensionless dispersion coordinates],
    [Use $K=(k c)/omega_(p,e)$ and $W=omega/omega_(p,e)$ for the cold
    electromagnetic branch. Then $W^2=1+K^2$,
    $v_"phi"/c=W/K$, and $v_"g"/c=K/W$.
    The cutoff is the intercept $W=1$ at $K=0$. The tangent slope
    $dv(W,K)$ gives $v_"g"/c$; the slope of the line from the origin to a
    point on the branch gives $v_"phi"/c=W/K$. These are different
    geometric measurements of the same curve.]
  )
  #details(
    [Derivation: limiting-case checks],
    [#derivation-step[Long-wavelength limit]
    Start from the normalized transverse relation

    $ W^2=1+K^2 .$

    As $K -> 0$, $W -> 1$. Hence

    $ omega -> omega_(p,e), quad v_"g"/c=K/W -> 0 .$

    The phase velocity formally diverges because a nearly spatially uniform
    oscillation has a finite frequency while its wave number tends to zero.

    #derivation-step[Short-wavelength and vacuum limits]
    As $K -> infinity$,

    $ W=sqrt(1+K^2) -> K .$

    Therefore

    $ v_"phi"/c=W/K -> 1, quad v_"g"/c=K/W -> 1 .$

    The plasma becomes transparent and the branch approaches the vacuum line.
    The same result follows dimensionally when the density tends to zero,
    because $omega_(p,e) -> 0$ and $omega=c k$.

    #derivation-step[Below-cutoff behavior]
    If $omega<omega_(p,e)$, then

    $ k^2=(omega^2-omega_(p,e)^2)/c^2<0 .$

    Write

    $ k=i alpha, quad alpha=sqrt(omega_(p,e)^2-omega^2)/c .$

    Choosing the decaying boundary solution gives the spatial factor
    $exp(-alpha x)$. This is an evanescent field.

    #derivation-step[Compare with the cold electrostatic branch]
    The cold electrostatic fixed-ion branch has
    $omega=omega_(p,e)$ for every $k$, so its group velocity vanishes. Adding
    pressure changes the relation to

    $ omega^2=omega_(p,e)^2+k^2 c_e^2 .$

    Pressure therefore supplies spatial propagation.]
  )
  #wave-dispersion
  #rechenbeispiel[
    Assume a homogeneous, cold, collisionless, unmagnetized, fixed-ion
    electromagnetic model. A radio source drives a plasma with
    $n_0=qty("1.0e16", "m^-3")$ and
    $c=qty("2.998e8", "m/s")$. Classify a drive at
    $omega=qty("4.0e9", "s^-1")$ and another at
    $omega=qty("1.13e10", "s^-1")$ as propagating or evanescent. For the
    propagating drive, report $k$ and the normalized phase and group speeds.
    Numerical result:
    $omega_(p,e)=qty("5.64e9", "s^-1")$; the lower-frequency drive is
    evanescent with $alpha=qty("13.3", "m^-1")$. The higher-frequency
    drive is propagating with $k=qty("32.7", "m^-1")$,
    #normalized-label[$v_"phi"/c=qty("1.15", "1")$], and
    #normalized-label[$v_"g"/c=qty("0.866", "1")$].
  ]
  #interpretation(
    [Cutoff, slope, and asymptote checks],
    [The intercept identifies the cutoff, the slope gives group velocity,
    and the asymptote checks the vacuum limit. If a curve violates one of
    these tests, revisit signs, units, polarization, and the omitted physics
    before using it for a prediction.]
  )
  #summary[
    Normalize first, then read the branch: $W^2=1+K^2$ has a cutoff at
    $W=1$, approaches the vacuum line at large $K$, and becomes evanescent
    below the cutoff. Limiting cases expose missing factors, incorrect
    polarizations, and unjustified model extrapolations.
  ]
  #knowledge-check((
    (
      question: [What does the intercept of the cold electromagnetic branch represent?],
      answer: [The intercept $W=1$ at $K=0$ is the plasma cutoff
      $omega=omega_(p,e)$. Frequencies below it have an imaginary bulk wave
      number in this model.]
    ),
    (
      question: [How can the slope of a dispersion curve be used physically?],
      answer: [The local slope $dv(omega,k)$ is the group velocity for a
      narrow-band packet. It is distinct from the ratio $omega/k$, which is
      the phase velocity.]
    ),
    (
      question: [What is the vacuum limit of the cold electromagnetic branch?],
      answer: [As density tends to zero or frequency becomes much larger than
      the plasma frequency, $omega approx c k$, and both normalized phase
      and group speeds approach the speed of light.]
    ),
    (
      question: [What is the signature of an evanescent solution in the wave number?],
      answer: [A frequency below cutoff gives $k^2<0$, so one chooses
      $k=i alpha$ and obtains exponential spatial decay rather than a
      propagating oscillation.]
    ),
  ))
  #chapter-nav(
    previous: (href: "10-diffusion.html", title: [Diffusion]),
    next: (href: "12-cold-magnetized-waves.html", title: [Cold magnetized waves]),
  )
]
