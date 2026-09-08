#import "../theme.typ": *
#import "../figures.typ": wave-linearization, wave-dispersion, warm-kinetic-limits
#import "@preview/physica:0.9.8": div, grad, pdv, dv, curl
#import "@preview/unify:0.8.1": qty, unit

#let chapter = [
  #page-title[9. Introduction to waves in plasmas] <introduction-waves>

  #lead[
    A plasma wave is a collective perturbation whose restoring force and
    inertia are distributed among charged particles and fields. This chapter
    establishes the common language for the later wave chapters: equilibria,
    linearization, plane-wave response, dispersion, and controlled limits.
  ]

  #callout(
    [A wave is a model plus an ordering],
    [The same plasma can support an electrostatic oscillation, a transverse
    electromagnetic wave, or an ion-acoustic response. The branch is selected
    by the equilibrium, polarization, frequency, wavelength, and closure—not
    by the word “wave” alone.]
  )

  #section-title[Equilibrium, perturbation, and linearization] <wave-linearization>

  #lead[
    How do we turn a nonlinear plasma model into a wave problem? Choose an
    equilibrium, assign a small parameter to every perturbation, discard only
    terms of second order in that parameter, and then test sinusoidal
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
    Gaussian CGS is active. Number density $n_s$ is in #unit("cm^-3"),
    position and wavelength are in #unit("cm"), time and frequency are in
    #unit("s") and #unit("s^-1"), velocity is in #unit("cm/s"), mass is in
    #unit("g"), pressure is in #unit("dyn/cm^2"), $bold(E)$ is in statvolt per
    #unit("cm"), $bold(B)$ is in #unit("G"), and current density is in
    statcoulomb per #unit("cm^2") per #unit("s"). The speed of light $c$ is
    in #unit("cm/s"). The phase $bold(k) dot bold(r)-omega t$ and normalized
    variables such as $omega/omega_(p,e)$ are dimensionless.
  ]

  #assumption(
    [Uniform, stationary, neutral equilibrium],
    [Use $n_s=n_(s,0)$, $bold(u)_(s,0)=bold(0)$, constant $p_(s,0)$, and
    $bold(E)_0=bold(0)$. The background magnetic field $bold(B)_0$ may be
    retained for the general linear equation, but the unmagnetized chapters
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
    The wave number $k=abs(bold(k))$ is in #unit("cm^-1") and the
    frequency $omega$ is in #unit("s^-1").]
  )

  #wave-linearization

  The species equations and Maxwell equations that are linearized are

  $ pdv(n_s,t)+div_(bold(r))(n_s bold(u)_s)=0 $

  $ m_s n_s (pdv(bold(u)_s,t)+bold(u)_s dot grad_(bold(r)) bold(u)_s)
    =q_s n_s (bold(E)+(bold(u)_s times bold(B))/c)-grad_(bold(r))(p_s) $

  $ curl_(bold(r))(bold(E))=-(pdv(bold(B),t))/c, quad
    curl_(bold(r))(bold(B))=((4 pi)/c) bold(j)+(pdv(bold(E),t))/c $

  $ div_(bold(r))(bold(E))=4 pi rho_q, quad
    div_(bold(r))(bold(B))=0 $

  where $rho_q=sum_s q_s n_s$ and
  $bold(j)=sum_s q_s n_s bold(u)_s$. For an adiabatic or isothermal closure,
  the pressure perturbation is written
  $p_(s,1)=gamma_s k_B T_s n_(s,1)$, with the appropriate temperature
  ordering stated explicitly.

  #details(
    [Derivation: linearized Fourier system],
    [Insert the perturbation expansion into continuity. The equilibrium has
    no flow, so the product of two first-order quantities is second order:
    $pdv(n_(s,1),t)+n_(s,0) div_(bold(r))(bold(u)_(s,1))=0$.
    The same expansion of momentum removes the convective product
    $bold(u)_(s,1) dot grad bold(u)_(s,1)$ and the perturbed magnetic product
    $bold(u)_(s,1) times bold(B)_1$. The first-order momentum equation is
    $m_s n_(s,0) pdv(bold(u)_(s,1),t)
      =q_s n_(s,0)(bold(E)_1+
      (bold(u)_(s,1) times bold(B)_0)/c)-grad_(bold(r))(p_(s,1))$.

    Apply the plane-wave replacements
    $pdv(,t) -> -i omega$, $grad_(bold(r)) -> i bold(k)$,
    $div_(bold(r)) -> i bold(k) dot$, and
    $curl_(bold(r)) -> i bold(k) times$. This gives
    $-i omega n_(s,1)+i n_(s,0) bold(k) dot bold(u)_(s,1)=0$
    and
    $-i omega m_s n_(s,0) bold(u)_(s,1)
      =q_s n_(s,0)(bold(E)_1+
      (bold(u)_(s,1) times bold(B)_0)/c)-i bold(k) p_(s,1)$.
    Maxwell's equations become algebraic relations between the field
    amplitudes, while the equilibrium neutrality removes the zeroth-order
    charge density. A nontrivial amplitude exists only when the resulting
    linear coefficient matrix is singular; that determinant is the
    dispersion relation.]
  )

  #interpretation(
    [Linearization is an ordering, not a slogan],
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
      $pdv(,t)$ becomes $-i omega$ and $grad$ becomes $i bold(k)$ when acting
      on the amplitude.]
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
    oscillation frequency is set by density and charge rather than by a
    spatial wavelength.
  ]

  #objectives((
    [derive the electron plasma frequency from continuity, momentum, and Poisson],
    [identify the restoring force in a cold electrostatic oscillation],
    [state the correction when both electron and ion inertia are retained],
    [separate a localized plasma oscillation from a propagating wave],
  ))

  #unit-ledger[
    The electron density $n_0$ is in #unit("cm^-3"), charge $e$ is in
    statcoulomb, electron mass $m_e$ is in #unit("g"), electric field is in
    statvolt per #unit("cm"), and the plasma frequency
    $omega_(p,e)$ is in #unit("s^-1"). The normalized displacement
    $xi/xi_0$ and time $omega_(p,e) t$ are dimensionless.
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
    [The electron plasma frequency in Gaussian CGS is
    $omega_(p,e)=sqrt((4 pi n_0 e^2)/m_e)$.
    It is a local collective frequency. Since the cold longitudinal
    dispersion relation contains no $k$, this idealized oscillation has no
    group propagation.]
  )

  #governing-law(
    [Cold electrostatic plasma oscillation],
    [For a longitudinal perturbation with fixed ions,
    $omega^2=omega_(p,e)^2=(4 pi n_0 e^2)/m_e$.
    If every species is allowed to move coherently, the restoring frequency
    becomes $omega_p^2=sum_s ((4 pi n_(s,0) q_s^2)/m_s)$.]
  )

  #rechenbeispiel[
    For a cold hydrogen plasma use
    $n_0=qty("1.0e10", "cm^-3")$,
    $e=qty("4.803e-10", "statC")$, and
    $m_e=qty("9.109e-28", "g")$.
    Determine the electron plasma frequency and its ordinary frequency
    $f_p=omega_(p,e)/(2 pi)$.

    Numerical result:
    $omega_(p,e)=qty("5.64e9", "s^-1")$ and
    $f_p=qty("8.98e8", "Hz")$.
  ]

  #details(
    [Derivation: charge separation supplies the restoring force],
    [For the electron charge $q_e=-e$, the cold linearized momentum equation
    is $-i omega m_e bold(u)_(e,1)=-e bold(E)_1$.
    The longitudinal continuity equation gives
    $n_(e,1)=(n_0 (bold(k) dot bold(u)_(e,1)))/omega$.
    For a parallel electric field, this is
    $n_(e,1)=(n_0 k u_(e,1))/omega$.

    Poisson's equation contains only the perturbed electron charge because
    the ion background is fixed:
    $i k E_1=4 pi rho_(q,1)=-4 pi e n_(e,1)$.
    Solving the momentum equation gives
    $u_(e,1)=(-i e E_1)/(m_e omega)$.
    Insert it into continuity and then Poisson:
    $i k E_1=-4 pi e ((-i n_0 e k E_1)/(m_e omega^2))$.
    Cancel the nonzero amplitude and the common factor $i k$:
    $omega^2=(4 pi n_0 e^2)/m_e$.

    The wave number disappeared because the cold model has no pressure
    gradient and therefore no spatial restoring scale. If the ions also move,
    repeat the same force-balance calculation for each species and sum their
    charge responses. The result is
    $omega_p^2=sum_s ((4 pi n_(s,0)q_s^2)/m_s)$; for hydrogen the ion term is
    smaller by $m_e/m_i$.]
  )

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
    In Gaussian CGS this gives $omega_(p,e)^2=(4 pi n_0 e^2)/m_e$.
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
      $(4 pi n_(s,0)q_s^2)/m_s$ to the
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
    The wave number $k$ is in #unit("cm^-1"), frequency $omega$ is in
    #unit("s^-1"), and $c$ is in #unit("cm/s"). The velocities
    $v_"phi"$ and $v_"g"$ are in #unit("cm/s"). The dielectric factor
    $epsilon_(r)$, $(k c)/omega_(p,e)$, and $omega/omega_(p,e)$ are
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

  #animation(
    "../media/wave-packet.mp4",
    "A Gaussian wave packet with a visible carrier oscillation travels to the right. The slowly moving envelope is marked as the group-velocity scale, while a separate crest marker shows the faster phase motion. The normalized horizontal coordinate is position divided by a reference length, and the vertical field amplitude is dimensionless.",
    caption: [
      A carrier and its envelope separate because the cold plasma branch is
      dispersive. The animation is a deterministic normalized illustration,
      not a measurement or a live parameter solver.
    ],
    poster: "../media/wave-packet.png",
  )

  #details(
    [Derivation: current response and the transverse wave equation],
    [The cold electron momentum response is again
    $-i omega m_e bold(u)_(e,1)=-e bold(E)_1$,
    so $bold(u)_(e,1)=(-i e bold(E)_1)/(m_e omega)$.
    The perturbed current is therefore
    $bold(j)_1=-e n_0 bold(u)_(e,1)
      =(i n_0 e^2 bold(E)_1)/(m_e omega)$.

    For a transverse plane wave, Faraday's and Ampere's equations become
    $bold(k) times bold(E)_1=(omega bold(B)_1)/c$
    and
    $bold(k) times bold(B)_1=-(omega bold(E)_1)/c
      -(4 pi i bold(j)_1)/c$.
    Substitute the first into the second and use
    $bold(k) times (bold(k) times bold(E)_1)=-k^2 bold(E)_1$.
    The result is
    $(omega^2-c^2 k^2) bold(E)_1
      =-4 pi i omega bold(j)_1$.
    Inserting the current response on the right gives
    $(omega^2-c^2 k^2) bold(E)_1
      =omega_(p,e)^2 bold(E)_1$,
    with $omega_(p,e)^2=(4 pi n_0e^2)/m_e$. A nonzero field amplitude then
    requires $omega^2=omega_(p,e)^2+c^2 k^2$.

    Dividing by $omega^2$ gives
    $(k^2 c^2)/(omega^2)=1-omega_(p,e)^2/omega^2$,
    which identifies the relative dielectric factor. Real $k$ requires
    $omega>omega_(p,e)$. Below the cutoff, $k$ is imaginary and the field
    is evanescent rather than a propagating bulk wave.]
  )

  #rechenbeispiel[
    A cold electromagnetic wave has $omega=2 omega_(p,e)$ in a plasma with
    $omega_(p,e)=qty("5.64e9", "s^-1")$ and
    $c=qty("2.998e10", "cm/s")$.
    Determine $k$, the phase velocity, the group velocity, and the wavelength.

    Numerical result:
    $(k c)/omega_(p,e)=1.732$,
    $v_"phi"/c=1.155$,
    $v_"g"/c=0.866$,
    $k=qty("0.326", "cm^-1")$, and
    $lambda=qty("19.3", "cm")$.
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
      answer: [When $omega >> omega_(p,e)$, the electron response changes too
      slowly to modify the field strongly. The dielectric factor approaches
      one and $omega approx c k$.]
    ),
    (
      question: [Why can the phase velocity exceed the speed of light in this model?],
      answer: [The phase surface is not a causal signal. For the branch,
      $v_"phi">c$ is accompanied by $v_"g"<c$; signal propagation is governed
      by the causal packet and medium response.]
    ),
  ))

  #section-title[Cold-fluid wave equations and kinetic limits] <wave-kinetic-limits>

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
    Species temperature energy $k_B T_s$ is in #unit("erg"), mass is in
    #unit("g"), thermal speed and ion-acoustic speed are in #unit("cm/s"),
    $k$ is in #unit("cm^-1"), $omega$ is in #unit("s^-1"), and
    $lambda_D$ is in #unit("cm"). The phase parameters
    $k lambda_D$ and $omega/(k v_"th,s")$ are dimensionless.
  ]

  #assumption(
    [Unmagnetized, electrostatic, warm-fluid closure],
    [Use $bold(B)_0=bold(0)$, a longitudinal electric field, collisionless
    perturbations, and a local pressure closure
    $p_(s,1)=gamma_s k_B T_s n_(s,1)$. The equilibrium is quasi-neutral
    with equal electron and ion densities. Kinetic corrections are discussed
    as a limit comparison, not hidden inside $gamma_s$.]
  )

  #definition(
    [Warm-fluid scales],
    [Define
    $c_s^2=(gamma_s k_B T_s)/m_s$ and
    $omega_(p,s)^2=(4 pi n_(s,0)q_s^2)/m_s$.
    Here $c_s$ is a pressure-response speed, not necessarily the phase
    velocity of a branch. The thermal-speed convention used for kinetic
    comparisons is $v_"th,s"=sqrt((2 k_B T_s)/m_s)$.]
  )

  #warm-kinetic-limits

  #governing-law(
    [Warm electrostatic fluid dispersion],
    [The longitudinal two-species warm-fluid dispersion relation is
    $1-sum_s omega_(p,s)^2/(omega^2-k^2 c_s^2)=0$.
    With fixed ions this gives
    $omega^2=omega_(p,e)^2+k^2 c_e^2$.
    In the low-frequency quasi-neutral hydrogen limit,
    $omega^2 approx (k^2 (gamma_e k_B T_e+gamma_i k_B T_i))/m_i$.]
  )
  #details(
    [Derivation: warm-fluid susceptibility and ion sound],
    [For one species in one dimension, the Fourier continuity equation is
    $-i omega n_(s,1)+i k n_(s,0)u_(s,1)=0$,
    hence $n_(s,1)=(k n_(s,0)u_(s,1))/omega$.
    The longitudinal momentum equation with the pressure closure is
    $-i omega m_s u_(s,1)=q_s E_1
      -(i k gamma_s k_B T_s n_(s,1))/n_(s,0)$.
    Substituting continuity and solving for the velocity gives
    $u_(s,1)=(i q_s omega E_1)/
      (m_(s)(omega^2-k^2 c_s^2))$.
    Therefore
    $n_(s,1)=(i n_(s,0)q_s k E_1)/
      (m_(s)(omega^2-k^2 c_s^2))$.
    Poisson's equation is
    $i k E_1=4 pi sum_s q_s n_(s,1)$.
    Canceling $i k E_1$ and inserting the species response produces
    $1=sum_s (4 pi n_(s,0)q_s^2)/
      (m_(s)(omega^2-k^2 c_s^2))$,
    which is the displayed dispersion relation.
    For a high-frequency electron branch with fixed ions, the ion term is
    omitted and the result is
    $omega^2=omega_(p,e)^2+k^2 c_e^2$. For a low-frequency ion-acoustic
    branch, neglect electron inertia in the electron momentum equation and
    impose $n_(e,1)=n_(i,1)$ from quasi-neutrality. The electron pressure
    supplies the electric field, while the ion inertia carries the wave.
    Combining the two pressure responses yields
    $omega^2=(k^2 (gamma_e k_B T_e+gamma_i k_B T_i))/m_i$.
    The reduction requires $omega << omega_(p,e)$ and $k lambda_D << 1$;
    otherwise charge separation or electron inertia cannot be discarded.
    Kinetic theory replaces the fluid closure by a velocity-space response.
    A standard unmagnetized electrostatic form is
    $1+sum_s chi_(s)(omega,k)=0$ with
    $chi_s=omega_(p,s)^2/(k^2 v_"th,s"^2)
      (1+zeta_s Z(zeta_s))$ and
    $zeta_s=omega/(k v_"th,s")$.
    The analytically continued plasma-dispersion function $Z$ accounts for
    resonant particles; its imaginary contribution gives collisionless
    damping or growth. A warm-fluid $gamma_s$ can reproduce selected
    long-wavelength real-frequency limits, but it cannot reproduce this
    resonant phase mixing.]
  )
  #rechenbeispiel[
    For cold ions and an isothermal electron response use
    $k_B T_e=qty("1.602e-11", "erg")$,
    $m_i=qty("1.673e-24", "g")$, and
    $k=qty("1.0e-2", "cm^-1")$.
    Determine the ion-acoustic speed, frequency, and the ratio
    $k lambda_D$ for $n_0=qty("1.0e10", "cm^-3")$.
    Numerical result:
    $c_s=qty("3.09e6", "cm/s")$,
    $omega=qty("3.09e4", "s^-1")$,
    $lambda_D=qty("2.35e-2", "cm")$, and
    $k lambda_D=2.35 dot 10^(-4)$.
  ]
  #interpretation(
    [Fluid and kinetic limits answer different questions],
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
      $omega << omega_(p,e)$ and $k lambda_D << 1$.]
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
    slopes, cutoffs, and asymptotic branches. A limiting-case check is a
    physical test of the derivation, not merely a cosmetic algebra check.
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
    is in #unit("cm^-1"), frequency in #unit("s^-1"), and velocities in
    #unit("cm/s"). For warm electrostatic checks, $K_D=k lambda_D$ is also
    dimensionless.
  ]
  #assumption(
    [A branch is interpreted with its model attached],
    [Read the cold electromagnetic curve only for a homogeneous,
    unmagnetized, collisionless, fixed-ion plasma. The vacuum line is a
    reference, not a second plasma mode. If a branch leaves the assumptions,
    switch model before extrapolating the curve.]
  )
  #definition(
    [Dimensionless dispersion coordinates],
    [Use $K=(k c)/omega_(p,e)$ and $W=omega/omega_(p,e)$ for the cold
    electromagnetic branch. Then $W^2=1+K^2$,
    $v_"phi"/c=W/K$, and $v_"g"/c=K/W$.
    The cutoff is the intercept $W=1$ at $K=0$. A vertical or horizontal
    tangent has a direct velocity interpretation through these slopes.]
  )
  #wave-dispersion
  #details(
    [Derivation: limiting-case checks],
    [Start from the normalized transverse relation
    $W^2=1+K^2$. In the long-wavelength limit $K -> 0$,
    $W -> 1$, so $omega -> omega_(p,e)$ and
    $v_"g"/c=K/W -> 0$. The formal phase velocity diverges because a
    nearly spatially uniform oscillation has a finite frequency.
    In the short-wavelength or high-frequency limit $K -> infinity$,
    $W=sqrt(1+K^2) -> K$. Therefore
    $v_"phi"/c=W/K -> 1$ and $v_"g"/c=K/W -> 1$; the plasma becomes
    transparent and the branch approaches the vacuum line.
    If the density tends to zero, $omega_(p,e) -> 0$ and the dimensional
    relation becomes $omega=c k$. If the frequency is below the cutoff,
    $omega<omega_(p,e)$, rearrangement gives
    $k^2=(omega^2-omega_(p,e)^2)/c^2<0$. Write
    $k=i alpha$ with
    $alpha=sqrt(omega_(p,e)^2-omega^2)/c$; the spatial factor is
    $exp(-alpha x)$ after choosing the decaying boundary solution. This is
    an evanescent field, not a propagating bulk wave.
    The cold electrostatic fixed-ion branch provides a second check:
    $omega=omega_(p,e)$ for every $k$, so its group velocity vanishes.
    Adding pressure changes this to
    $omega^2=omega_(p,e)^2+k^2 c_e^2$ and therefore supplies spatial
    propagation. Every plotted branch should be read together with the
    approximation that produced it.]
  )
  #rechenbeispiel[
    A radio source drives a homogeneous cold plasma with
    $n_0=qty("1.0e10", "cm^-3")$ and
    $c=qty("2.998e10", "cm/s")$. Classify a drive at
    $omega=qty("4.0e9", "s^-1")$ and another at
    $omega=qty("1.13e10", "s^-1")$ as propagating or evanescent. For the
    propagating drive, report $k$ and the normalized phase and group speeds.
    Numerical result:
    $omega_(p,e)=qty("5.64e9", "s^-1")$; the lower-frequency drive is
    evanescent with $alpha=qty("3.98e-1", "cm^-1")$. The higher-frequency
    drive is propagating with $k=qty("2.94e-1", "cm^-1")$,
    $v_"phi"/c=1.31$, and $v_"g"/c=0.763$.
  ]
  #interpretation(
    [A good plot is a compact argument],
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
    previous: (href: "08-diffusion.html", title: [Diffusion]),
    next: (href: "10-cold-magnetized-waves.html", title: [Cold magnetized waves]),
  )
]
