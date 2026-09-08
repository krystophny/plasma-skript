#import "../theme.typ": *
#import "../figures.typ": model-hierarchy, debye-profile
#import "@preview/physica:0.9.8": grad, div, curl, laplacian, pdv, vb

#let chapter = [
  #page-title[1. Introduction] <introduction>

  #lead[
    A plasma is a many-particle system whose long-range electromagnetic fields
    make the particles respond collectively. This chapter establishes the
    vocabulary, scales, and model choices used in the rest of the script.
  ]

  #section-title[Plasma as a collective state] <intro-plasma-state>

  #lead[
    Why is a plasma more than a hot gas? The useful answer is a test of
    response: a local charge or current must influence particles beyond the
    nearest collision partner, while the system still contains enough
    particles for a smooth field description.
  ]

  #objectives((
    [distinguish a plasma state from a temperature threshold],
    [identify collective electromagnetic phenomena in a physical example],
    [select a model level from the relevant length and time scales],
  ))

  #unit-ledger[
    The dimensional convention is Gaussian CGS. Number density $n_s$ is in
    #unit("cm^-3"), charge $q_s$ is in statcoulomb (esu), mass $m_s$ is in grams,
    time is in seconds, electric field $bold(E)$ is in statvolt per centimetre,
    magnetic field $bold(B)$ is in gauss, and energy is in #unit("erg"). The temperature
    $T_s$ below is a thermodynamic temperature in kelvin, so $k_B T_s$ is an
    energy in #unit("erg"). A symbol without a unit is explicitly marked dimensionless.
  ]

  #definition(
    [Working definition of a plasma],
    [A plasma is a collection of charged species whose collective
    electromagnetic response is important on the scale of interest. It need
    not be fully ionized, and there is no universal temperature at which matter
    abruptly becomes a plasma. Ionization, collisionality, boundaries, and the
    observation scale all matter.]
  )

  The charge density is the species sum

  $ rho_q = sum_s q_s n_s $ <intro-charge-density>

  #equation-note[
    Gaussian CGS. The charge density $rho_q$ is in statcoulomb $upright("cm")^(-3)$.
    The sum runs over all charged species.
  ]

  Maxwell's equations couple this source to the fields. Two source-free
  identities used repeatedly later are

  $ div bold(B) = 0, quad curl bold(E) = -1/c pdv(bold(B), t) $ <intro-maxwell-identities>

  #equation-note[
    Gaussian CGS. $c$ is the speed of light in $upright("cm") dot upright("s")^(-1)$.
    The divergence and curl equations are exact Maxwell equations, not a
    plasma approximation.
  ]

  The important distinction from a neutral gas is not simply the presence of
  charged particles. It is the range of the response. A charge imbalance can
  launch an electric field, a current can launch a magnetic perturbation, and
  the resulting fields can move many particles before local collisions erase
  the correlation.

  Representative plasmas include the solar corona, the solar wind, planetary
  magnetospheres, lightning, fluorescent discharges, arcs, fusion devices, and
  processing plasmas. Their temperatures and densities span many orders of
  magnitude, so the collective criterion must be stated at the scale of the
  observation rather than replaced by a temperature label.

  The characteristic responses introduced by this script are Debye shielding,
  electron plasma oscillations, collective waves, gyromotion and guiding-center
  drifts, instabilities, and boundary sheaths. These are different limits of
  the same coupled particle--field system, not independent definitions of a
  plasma.

  #definition(
    [Ideal-plasma convention used here],
    [For the purposes of this script, an ideal plasma is weakly coupled and
    sufficiently populated that collective fields can be treated smoothly.
    A useful weak-coupling parameter is $Gamma_s = q_s^2 / (a_s k_B T_s)$,
    where $a_s = (3 / (4 pi n_s))^(1/3)$ is the mean-spacing scale. The
    classical collective ordering also requires many particles in a Debye
    sphere and, when quasineutral fluid behavior is invoked, a system scale
    $L$ much larger than $lambda_D$. “Ideal” therefore does not mean cold,
    uniform, or exactly neutral at every point.]
  )

  #equation-note[
    Gaussian CGS. $a_s$ is in #unit("cm"), $q_s^2 / (a_s k_B T_s)$ is
    dimensionless, and the weak-coupling condition is $Gamma_s << 1$.
  ]

  Classical statistics also have a validity boundary. For electrons, define
  the degeneracy parameter $theta_e = k_B T_e / E_(F,e)$, with the
  nonrelativistic Fermi energy

  $ E_(F,e) = (ℏ^2 / (2 m_e)) (3 pi^2 n_e)^(2/3) $

  #equation-note[
    Gaussian CGS. $E_(F,e)$ and $k_B T_e$ are energies in #unit("erg"),
    and $theta_e$ is dimensionless. The classical limit has $theta_e >> 1$;
    $theta_e <= 1$ signals quantum degeneracy. White-dwarf interiors and
    dense laser-compressed matter are representative settings.
  ]

  #model-hierarchy

  #interpretation(
    [Reading the hierarchy],
    [The full particle--field model keeps every particle and the
    electromagnetic fields. Kinetic theory keeps a distribution function in
    phase space. Fluid models retain velocity moments and add closure
    assumptions. Magnetohydrodynamics combines species into a single fluid.
    Moving downward is a controlled loss of information, not a claim that a
    reduced model is always better or worse.]
  )

  #summary[
    A plasma is identified by scale-dependent collective electromagnetic
    response, not by a universal temperature threshold. Ideal-plasma and
    classical-statistics orderings must be stated separately from the
    collective criterion, and the particle--field hierarchy makes the model
    reduction explicit.
  ]

  #exam-prompts(
    (
      [1(a) At which temperature does matter enter the plasma state?],
      [1(b) Describe some typical plasmas in nature and technology (Fig. 1.3).],
      [1(c) What are characteristic phenomena in plasmas?],
      [1(g) List features of an ideal plasma.],
      [1(h) What is a quantum degenerate plasma and where does it appear?],
    ),
    [Plasma Physics Exam.pdf, p. 1],
  )

  #knowledge-check((
    (
      question: [Why is a temperature alone insufficient to identify a plasma?],
      answer: [The relevant test is whether collective electromagnetic response matters on the chosen length and time scales. Ionization, collisionality, boundaries, and observation scale also enter.],
    ),
    (
      question: [What does weak coupling mean for the parameter $Gamma_s$?],
      answer: [It means $Gamma_s = q_s^2 / (a_s k_B T_s)$ is much smaller than one, so typical thermal energy exceeds the electrostatic interaction energy at the mean spacing.],
    ),
    (
      question: [Which ordering distinguishes quantum degeneracy from classical statistics?],
      answer: [The ratio $theta_e = k_B T_e / E_(F,e)$ is the indicator: $theta_e >> 1$ is classical, while $theta_e <= 1$ requires quantum statistics.],
    ),
    (
      question: [What is lost when moving from the particle--field model to a fluid model?],
      answer: [Velocity-space and particle-level detail are averaged into moments, and a closure assumption supplies the unresolved higher moments.],
    ),
  ))

  #section-title[Characteristic scales and ordering] <intro-scales>

  #lead[
    Which scale decides whether a field perturbation is local or collective?
    Plasma physics answers by comparing natural particle, field, collision,
    and system scales before choosing equations.
  ]

  #objectives((
    [define the electron plasma frequency, gyrofrequency, Debye length, and gyroradius],
    [compare dimensionless orderings without hiding their reference scales],
    [estimate whether a stated model can resolve the relevant physics],
  ))

  #unit-ledger[
    All quantities in this section are dimensional Gaussian-CGS quantities
    unless a ratio is explicitly marked dimensionless. For a species $s$,
    $q_s$ is in statcoulomb, $m_s$ in grams, $n_s$ in $upright("cm")^(-3)$, $T_s$ in
    kelvin, and $B$ in gauss.
  ]

  The electron plasma frequency is the natural electrostatic response rate of
  a homogeneous electron population. For any species it is

  $ omega_(p,s) = sqrt((4 pi n_s q_s^2) / m_s) $ <intro-plasma-frequency>

  #equation-note[
    Gaussian CGS. $omega_(p,s)$ is in $upright("s")^(-1)$ as an angular frequency.
    The corresponding ordinary frequency is $f_(p,s) = omega_(p,s)/(2 pi)$
    in hertz.
  ]

  A magnetic field introduces the signed gyrofrequency

  $ Omega_s = q_s B / (m_s c), quad omega_(c,s) = abs(Omega_s) $ <intro-gyrofrequency>

  #equation-note[
    Gaussian CGS. $Omega_s$ and $omega_(c,s)$ are in $upright("s")^(-1)$. The sign of
    $Omega_s$ carries the charge-sign convention, while $omega_(c,s)$ is a
    positive rate.
  ]

  Taking the thermal speed convention

  $ v_("th,s") = sqrt((2 k_B T_s) / m_s), quad rho_s = v_("perp,s") / omega_(c,s) $ <intro-thermal-scales>

  gives a thermal gyroradius $rho_s$ in centimetres. The electron Debye length
  in an electron--ion plasma is

  $ lambda_D = sqrt((k_B T_e) / (4 pi n_e e^2)) $ <intro-debye-length>

  #equation-note[
    Gaussian CGS. $v_("th,s")$ is in $upright("cm") dot upright("s")^(-1)$, $rho_s$ and $lambda_D$
    are in cm, and $e$ is the positive elementary charge in statcoulomb. The
    chosen factor of $2$ defines this thermal-speed convention.
  ]

  A common collective ordering is the Debye number

  $ N_D = (4 pi)/(3) n_e lambda_D^3 >> 1 $ <intro-debye-number>

  #equation-note[
    Dimensionless. $N_D$ counts electrons inside a Debye sphere. The symbol
    $>> 1$ states an ordering assumption, not an exact numerical boundary.
  ]

  #rechenbeispiel[
    Context: use a hydrogen plasma with $n_e = qty("1e14", "cm^-3")$,
    $T_e = qty("1e6", "K")$, $T_i = qty("1e6", "K")$, and
    $B = qty("1e4", "G")$. Assume singly charged ions, $n_i = n_e$, and use
    $m_e = qty("9.109e-28", "g")$,
    $m_i = qty("1.673e-24", "g")$, $e = 4.803 dot 10^(-10)$ statcoulomb,
    $k_B = qty("1.381e-16", "erg/K")$, and
    $c = qty("2.998e10", "cm/s")$.

    Target: report $lambda_D$, $omega_(p,e)$, $rho_e$, and $rho_i$.

    Numerical result: $lambda_D = qty("6.9e-4", "cm")$,
    $omega_(p,e) = qty("5.6e11", "s^-1")$,
    $rho_e = qty("3.1e-3", "cm")$, and $rho_i = qty("1.3e-1", "cm")$.
    These values are dimensional Gaussian-CGS results.
  ]

  #debye-profile

  #details(
    [Why scale ratios come first],
    [A model is selected by comparing its smallest resolved length with
    $lambda_D$ and $rho_s$, and its fastest resolved time with
    $omega_(p,s)^(-1)$ and $omega_(c,s)^(-1)$. A fluid model can be useful
    even when it does not resolve every orbit, but only after the unresolved
    motion has been averaged or closed. The ratios $lambda_D/L$,
    $rho_s/L$, and $omega/omega_(c,s)$ are dimensionless only after the
    system length $L$ and observation frequency $omega$ are stated.]
  )

  #summary[
    The plasma frequency, gyrofrequency, Debye length, gyroradius, and Debye
    number provide a first ordering language. State the unit system and the
    reference scales before interpreting any ratio.
  ]

  #exam-prompts(
    (
      [1(i) Estimate the plasma frequency $omega_p$ from thermal velocity $v_t$ and Debye length $lambda_D$.],
      [1(j) Give rough values of particle density, temperature, plasma frequency, gyrofrequency (electrons, ions) and Debye length and gyroradius (thermal electrons, ion) in a thermonuclear plasma.],
    ),
    [Plasma Physics Exam.pdf, p. 1],
  )

  #knowledge-check((
    (
      question: [Which of $omega_(p,e)$ and $omega_(c,e)$ changes sign when the electron charge convention is reversed?],
      answer: [$omega_(p,e)$ is unchanged because it contains $q_e^2$. The signed $Omega_e$ changes sign, while its magnitude $omega_(c,e)$ does not.],
    ),
    (
      question: [What does $N_D >> 1$ say physically, and why is it dimensionless?],
      answer: [It says that many electrons occupy a Debye sphere. Density contributes $upright("cm")^(-3)$ and $lambda_D^3$ contributes $upright("cm")^3$, so the product has no unit.],
    ),
    (
      question: [If $B$ doubles while $T_s$ and $m_s$ remain fixed, how does the thermal gyroradius scale?],
      answer: [$rho_s$ halves because $omega_(c,s)$ is proportional to $B$ and the thermal speed is unchanged.],
    ),
    (
      question: [Name one reason a fluid model can remain useful when $rho_s$ is not resolved.],
      answer: [The rapid gyromotion can be averaged into a guiding-center or pressure response, provided the fields vary slowly over an orbit and the closure remains valid.],
    ),
  ))

  #section-title[Debye shielding] <intro-debye-shielding>

  #lead[
    A test charge disturbs the surrounding plasma. How far does its
    electrostatic influence extend once mobile electrons rearrange? Debye
    shielding answers this question in the weak-potential, equilibrium limit.
  ]

  #objectives((
    [state the equilibrium and ordering assumptions behind Debye shielding],
    [connect the Boltzmann response to the screened Poisson equation],
    [interpret the Debye length as a collective response scale],
  ))

  #unit-ledger[
    Gaussian CGS is active. The electrostatic potential $phi$ is in statvolt,
    charge density $rho_q$ in statcoulomb $upright("cm")^(-3)$, and the electron
    temperature $T_e$ is in kelvin. The screening length $lambda_D$ is in cm.
  ]

  #assumption(
    [Linearized Boltzmann response],
    [Take a uniform, stationary ion background with $n_i = n_0$, mobile
    electrons at temperature $T_e$, no magnetic force in the equilibrium
    response, and a weak potential satisfying $abs(e phi) << k_B T_e$. The
    ions are treated as fixed on the electron response time.]
  )

  The electron equilibrium density follows from the electrostatic potential
  energy $-e phi$:

  $ n_e = n_0 exp(e phi / (k_B T_e)) approx n_0 (1 + e phi / (k_B T_e)) $ <debye-boltzmann-response>

  #equation-note[
    Gaussian CGS. $n_e$ and $n_0$ are in $upright("cm")^(-3)$, and $e phi$ and $k_B T_e$
    are energies in erg. The approximation is dimensionless and requires
    $abs(e phi)/(k_B T_e) << 1$.
  ]

  The net charge density is therefore

  $ rho_q = e n_i - e n_e approx - (e^2 n_0)/(k_B T_e) phi $ <debye-charge-response>

  #equation-note[
    Gaussian CGS. The sign expresses the restoring response of electrons to a
    positive potential perturbation.
  ]

  Poisson's equation in Gaussian CGS is

  $ laplacian phi = -4 pi rho_q $ <debye-poisson>

  #equation-note[
    Gaussian CGS. This equation defines the electrostatic field convention used
    here. It is not the SI form with $epsilon_0$.
  ]

  Substitution gives the screened equation

  $ laplacian phi - phi / lambda_D^2 = 0, quad lambda_D = sqrt((k_B T_e) / (4 pi n_0 e^2)) $ <debye-screened-equation>

  #equation-note[
    Gaussian CGS. $lambda_D$ is in cm. The equation is valid outside the
    localized source and within the linearized, static response model.
  ]

  #details(
    [Derivation: from particle response to shielding],
    [For a positive test potential, the electron potential energy is $-e phi$.
    The equilibrium Boltzmann factor is therefore
    $exp(-(-e phi)/(k_B T_e)) = exp(e phi/(k_B T_e))$. Expand the exponential
    to first order because $abs(e phi)/(k_B T_e) << 1$. With immobile ions,
    $rho_q = e n_0 - e n_e$ becomes
    $rho_q approx -e^2 n_0 phi/(k_B T_e)$. Insert this response into the
    Gaussian-CGS Poisson equation. Defining the coefficient of $phi$ as
    $lambda_D^(-2) = 4 pi n_0 e^2/(k_B T_e)$ yields
    $laplacian phi - phi/lambda_D^2 = 0$. In spherical symmetry, the decaying
    source solution has the form $phi(r)$ proportional to
    $exp(-r/lambda_D)/r$.
    The exponential factor is the shielding result; the factor $1/r$ is the
    unscreened geometric spreading of a point source.]
  )

  #debye-profile

  #interpretation(
    [What the Debye length does not mean],
    [The Debye length is not a hard vacuum boundary and it does not make the
    plasma exactly neutral at every point. It is the distance over which this
    particular equilibrium response reduces a localized electrostatic field.
    Strong potentials, rapid time dependence, boundaries, insufficient Debye
    number, and kinetic non-equilibrium require a more complete model.]
  )

  #summary[
    Debye shielding is a linear equilibrium response: the Boltzmann electron
    density modifies Poisson's equation and introduces the length $lambda_D$.
    The derivation depends on weak potential, mobile electrons, and a stationary
    ion background.
  ]

  #exam-prompts(
    (
      [1(d) A spherical region of complete charge separation has a potential $Phi(r) = (N q_e / epsilon_0) r^2$ at its boundary. What size can such a region roughly have in a thermal plasma of temperature $T$ (potential energy = thermal energy)?],
      [1(e) Describe and give an overview of the derivation for Debye shielding.],
    ),
    [Plasma Physics Exam.pdf, p. 1],
  )

  #knowledge-check((
    (
      question: [Why does a positive electrostatic potential increase the equilibrium electron density in the Boltzmann response?],
      answer: [An electron has charge $-e$, so its potential energy is $-e phi$. A positive $phi$ lowers that energy and produces the factor $exp(e phi/(k_B T_e))$.],
    ),
    (
      question: [Which approximation turns the exponential Boltzmann response into a linear screening equation?],
      answer: [The weak-potential ordering $abs(e phi) << k_B T_e$ permits a first-order expansion of the exponential.],
    ),
    (
      question: [What happens to the screened potential at distances much larger than $lambda_D$ in this model?],
      answer: [The exponential factor suppresses it, so the localized electrostatic influence is small compared with the unscreened $1/r$ field.],
    ),
    (
      question: [Give one situation in which the linear Debye-shielding derivation should not be used without modification.],
      answer: [A potential comparable to or larger than $k_B T_e/e$, a time-dependent kinetic response, or a boundary within the shielding region violates the stated assumptions.],
    ),
  ))

  #section-title[Electron plasma oscillations] <intro-plasma-oscillations>

  #lead[
    Shielding is a static response. What happens when electrons are displaced
    faster than they can rearrange thermally? The restoring electric field then
    produces an electron plasma oscillation.
  ]

  #objectives((
    [derive the cold electron plasma frequency from a displacement model],
    [separate the restoring force from the equilibrium charge balance],
    [state how temperature, collisions, and magnetic fields change the model],
  ))

  #unit-ledger[
    Gaussian CGS is active. Let the equilibrium density be $n_0$ in
    $upright("cm")^(-3)$, the electron displacement $xi$ in cm, the electric field in
    statvolt per centimetre, and time in seconds. Ions are singly charged and
    initially stationary.
  ]

  #assumption(
    [Cold, unmagnetized, collisionless response],
    [Displace a uniform electron slab by a small amount $xi$ relative to fixed
    ions. Ignore pressure, collisions, magnetic fields, and density variation
    within the slab. The model isolates the electrostatic restoring force and
    describes small-amplitude motion about equilibrium.]
  )

  A displacement creates two oppositely charged boundary sheets. The sheet
  charge magnitude is $e n_0 xi$, so the electric field between them is

  $ bold(E) = 4 pi e n_0 xi bold(e)_xi $ <plasma-oscillation-field>

  #equation-note[
    Gaussian CGS. $bold(e)_xi$ points in the displacement direction. The field
    is in statvolt per centimetre when $n_0$ is in $upright("cm")^(-3)$ and $xi$ in $upright("cm")$.
  ]

  The electron force is opposite to the displacement:

  $ m_e (d^2 xi)/(d t^2) = -e E = -4 pi n_0 e^2 xi $ <plasma-oscillation-force>

  #equation-note[
    Gaussian CGS. The force is in dynes. The negative sign is the restoring
    sign for the electron charge $-e$.
  ]

  Dividing by $m_e$ gives the harmonic-oscillator equation

  $ (d^2 xi)/(d t^2) + omega_(p,e)^2 xi = 0, quad omega_(p,e) = sqrt((4 pi n_0 e^2)/m_e) $ <plasma-oscillation-frequency>

  #equation-note[
    Gaussian CGS. $omega_(p,e)$ is an angular frequency in $upright("s")^(-1)$.
    The cold model has no damping and no thermal dispersive correction.
  ]

  #details(
    [Derivation: the displacement oscillator],
    [At equilibrium the positive ion and negative electron charge densities
    cancel. Shift the electron slab by $xi$. The overlap region remains nearly
    neutral, while the two boundary layers carry sheet charges with magnitude
    $e n_0 xi$. Gauss's law for two infinite sheets gives the uniform internal
    field $E = 4 pi e n_0 xi$ in Gaussian CGS. An electron feels
    $F = -e E$, hence $m_e xi'' = -4 pi n_0 e^2 xi$. The coefficient of $xi$
    has units $upright("s")^(-2)$ and identifies the plasma-frequency square. The
    displacement is therefore sinusoidal, $xi(t) = xi_0 cos(omega_(p,e) t +
    delta)$, within the small-amplitude model.]
  )

  #animation(
    "../media/plasma-oscillation.mp4",
    "An illustrative one-dimensional electron slab oscillates against fixed positive ions. The electron slab moves as a group, the ion markers remain fixed, and a restoring-field arrow reverses with the displacement. Displacement and time are normalized.",
    caption: [
      Cold electron plasma oscillation: collective displacement and restoring
      field. The animation is a normalized illustration, not measured data.
    ],
    poster: "../media/plasma-oscillation.png",
  )

  #interpretation(
    [Limits and extensions],
    [Finite temperature adds pressure and produces a wavenumber-dependent
    Langmuir-wave frequency. Collisions damp the motion. A background magnetic
    field couples the displacement to gyromotion. Those effects belong to the
    kinetic and wave chapters, while the oscillator here provides the local
    response scale.]
  )

  #summary[
    A small collective electron displacement creates a restoring electric field.
    In the cold, collisionless, unmagnetized limit its natural angular
    frequency is $omega_(p,e)$. Pressure, collisions, and magnetic fields are
    controlled extensions of this baseline model.
  ]

  #exam-prompts(
    (
      [1(f) Describe and derive electron plasma oscillations.],
      [1(i) Estimate the plasma frequency $omega_p$ from thermal velocity $v_t$ and Debye length $lambda_D$.],
    ),
    [Plasma Physics Exam.pdf, p. 1],
  )

  #knowledge-check((
    (
      question: [What supplies the restoring force in the cold plasma oscillator?],
      answer: [The charge separation between displaced electrons and stationary ions creates an electric field, and the electron charge makes the force oppose the displacement.],
    ),
    (
      question: [Why does the cold model produce a single local frequency rather than a dispersive frequency?],
      answer: [Pressure and spatial gradients were omitted, so the restoring coefficient contains density and particle constants but no wavenumber.],
    ),
    (
      question: [How would electron collisions change the oscillator qualitatively?],
      answer: [They introduce momentum loss and therefore damp the oscillation. The undamped harmonic equation is no longer complete.],
    ),
    (
      question: [What is the dimensional status of $t omega_(p,e)$ in the animation?],
      answer: [It is dimensionless because time in seconds is multiplied by an angular frequency in $upright("s")^(-1)$.],
    ),
  ))

  #section-title[From microscopic particles to a model] <intro-model-hierarchy>

  #lead[
    Which description should be used for a given plasma problem? The answer is
    a model-selection argument. Keep the variables needed by the observable,
    then justify every average, closure, and ordering that removes detail.
  ]

  #objectives((
    [map particle, kinetic, multiple-fluid, and MHD descriptions to retained variables],
    [explain what is lost when taking moments or combining species],
    [connect equilibrium distributions to the next kinetic description],
  ))

  #unit-ledger[
    Gaussian CGS remains the dimensional convention. The distribution function
    $f_(s)(t, bold(r), bold(v))$ is defined so that its velocity integral gives
    number density in $upright("cm")^(-3)$. The velocity variable is in
    $upright("cm") dot upright("s")^(-1)$, and phase-space integrals carry the
    corresponding powers of cm and seconds.
  ]

  #definition(
    [Distribution function],
    [For species $s$, $f_(s)(t, bold(r), bold(v))$ gives the density of particles
    near position $bold(r)$ and velocity $bold(v)$. Its normalization is
    $n_s = integral f_s dif bold(v)$. A fluid variable is a velocity moment of
    this distribution.]
  )

  The collisionless phase-space balance has the conservative form

  $ pdv(f_s, t) + div(f_s bold(v)) + grad_(bold(v)) dot (f_s bold(a)_s) = 0 $ <intro-kinetic-balance>

  #equation-note[
    Gaussian CGS. This is a schematic collisionless kinetic equation. The
    acceleration $bold(a)_s$ is in $upright("cm") dot upright("s")^(-2)$, and the divergence in
    velocity space is distinct from the spatial divergence. Collisions add a
    right-hand-side operator $C_(s)[f]$.
  ]

  For electromagnetic acceleration,

  $ bold(a)_s = q_s/m_s (bold(E) + bold(v) times bold(B) / c) $ <intro-electromagnetic-acceleration>

  #equation-note[
    Gaussian CGS. The factor $1/c$ belongs to the magnetic part of the Lorentz
    force in this convention. The acceleration has units $upright("cm") dot upright("s")^(-2)$.
  ]

  Taking the zeroth spatial moment illustrates the route to fluid theory:

  $ pdv(n_s, t) + div(n_s bold(u)_s) = 0 $ <intro-continuity-preview>

  #equation-note[
    Gaussian CGS. This continuity equation is dimensional: $n_s$ is in
    $upright("cm")^(-3)$ and $bold(u)_s$ in $upright("cm") dot upright("s")^(-1)$. The velocity moment is
    $bold(u)_s = (1/n_s) integral bold(v) f_s dif bold(v)$.
  ]

  #details(
    [What a closure assumption does],
    [The kinetic equation evolves a function of three position and three
    velocity coordinates. A zeroth moment gives density, a first moment gives
    bulk velocity, and a second central moment gives the pressure tensor. The
    moment equations form a hierarchy because the equation for one moment
    contains the next one. A fluid model closes that hierarchy by prescribing,
    for example, an isotropic pressure, an equation of state, or a heat-flux
    model. Each choice has a validity range that must be stated rather than
    hidden in notation.]
  )

  #model-hierarchy

  #interpretation(
    [Equilibrium is a model statement],
    [A Maxwell--Boltzmann distribution is an equilibrium candidate when the
    relevant collisions establish a thermal state. A collisionless plasma can
    retain non-Maxwellian structure, beams, or anisotropy. Calling a state
    equilibrium therefore requires specifying which dynamics and time scale
    have equilibrated.]
  )

  #summary[
    Model reduction is an ordered argument about retained variables, averaging,
    and closure. The distribution function connects the full particle picture
    to moments and fluid equations, while equilibrium is always relative to a
    specified equilibration process.
  ]

  #exam-prompts(
    (
      [1(k) Describe the most complete plasma model? (All particles interacting with electromagnetic forces)],
      [1(l) What kind of models can be used for plasma and how are they related?],
      [1(m) What is a Boltzmann distribution and how is it related to equilibrium states?],
    ),
    [Plasma Physics Exam.pdf, p. 1],
  )

  #knowledge-check((
    (
      question: [What variable is removed when passing from a kinetic description to a fluid density?],
      answer: [Velocity dependence is integrated out. The density is the zeroth velocity moment, while information about distribution shape is no longer retained directly.],
    ),
    (
      question: [Why can a collisionless plasma be non-Maxwellian?],
      answer: [Without collisions that efficiently mix phase space, beams, anisotropy, and other structures can persist on the observation time.],
    ),
    (
      question: [Which new quantity appears when the first moment is taken?],
      answer: [The bulk velocity $bold(u)_s$ appears, together with a momentum equation whose next unresolved moment is the pressure tensor.],
    ),
    (
      question: [State a model-selection question that must be answered before using MHD.],
      answer: [One must justify combining species into one fluid and closing the pressure or energy response at the length and time scales of interest.],
    ),
  ))

  #chapter-nav(
    next: (href: "02-single-particle-motion.html", title: [Single-particle motion]),
  )
]
