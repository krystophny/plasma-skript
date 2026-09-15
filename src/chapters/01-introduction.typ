#import "../theme.typ": *
#import "../figures.typ": model-hierarchy, debye-profile, maxwellian-profile
#import "@preview/physica:0.9.8": grad, div, curl, laplacian, pdv, dv, vb

#let chapter = [
  #page-title[1. Introduction] <introduction>

  #lead[
    A plasma is a many-particle system whose long-range electromagnetic fields
    make the particles respond collectively. This chapter establishes the
    vocabulary, scales, and model choices used in the rest of the script. The
    scale hierarchy follows standard graduate plasma-physics treatments
    @chen2016 @bittencourt2004.
  ]

  #section-title[Speed, energy, and temperature] <intro-speed-energy-temperature>

  #lead[
    What does temperature measure for a plasma particle, and why is it not a
    universal switch into the plasma state? Start with the kinetic-energy
    scale, then keep the equilibrium and non-equilibrium meanings of
    temperature distinct.
  ]

  #objectives((
    [relate particle speed, kinetic energy, and the thermal energy $k_B T_s$],
    [use one stated thermal-speed convention consistently],
    [explain why different species can have different temperatures],
  ))

  #unit-ledger[
    Gaussian CGS is active. Mass $m_s$ is in grams, speed $v$ in
    #unit("cm/s"), and kinetic energy and $k_B T_s$ are in #unit("erg").
    Temperature $T_s$ itself is in kelvin. When temperature is quoted in
    electron-volts, the intended quantity is the energy $k_B T_s$, not the
    thermodynamic temperature symbol by itself.
  ]

  For a particle of species $s$, the kinetic energy associated with speed $v$
  is

  $ epsilon_("kin,s") = (m_s v^2)/2, quad epsilon_("th,s") = k_B T_s $
  <intro-thermal-energy>

  #equation-note[
    The first quantity depends on the individual particle speed. The second
    is the thermal energy scale of an equilibrium population; both are in
    #unit("erg"). The factor $1/2$ belongs to the complete numerator
    $(m_s v^2)$.
  ]

  In a three-dimensional Maxwell--Boltzmann equilibrium with bulk velocity
  $bold(u)_s$, the velocity distribution is

  $ f_(s)^({"M"})(bold(v)) = n_s (m_s/(2 pi k_B T_s))^(3/2)
    exp(-(m_s (bold(v) - bold(u)_s)^2)/(2 k_B T_s)) $
  <intro-maxwellian>

  #equation-note[
    $f_(s)^({"M"})$ is normalized so that $integral f_(s)^({"M"})(bold(v))
    dif bold(v) = n_s$. The density is in #unit("cm^-3"), and the velocity
    integral supplies the corresponding phase-space units.
  ]

  The width of this distribution is set by the temperature. With the
  convention used throughout this script,

  $ v_("th,s") = sqrt((2 k_B T_s)/m_s), quad
    ⟨(m_s (bold(v) - bold(u)_s)^2)/2⟩ = (3 k_B T_s)/2 $
  <intro-thermal-speed>

  #details(
    [Why the three-dimensional average is $(3 k_B T_s)/2$],
    [#derivation-step[Sum the independent velocity components]
    Each Cartesian component of a Maxwellian has variance

    $ ⟨(v_j-u_(s,j))^2⟩=(k_B T_s)/m_s .$

    The three components are independent, so their kinetic-energy average is

    $ ⟨(m_s (bold(v)-bold(u)_s)^2)/2⟩
      =(m_s)/2 sum_j ⟨(v_j-u_(s,j))^2⟩
      =(3 k_B T_s)/2 .$

    #derivation-step[Interpret the thermal-speed convention]
    The convention

    $ v_("th,s")=sqrt((2 k_B T_s)/m_s) $

    defines a width parameter of the distribution. It is not the mean particle
    speed.]
  )

  #maxwellian-profile

  The conversion $1 #unit("eV") = 1.602176634 dot 10^(-12) #unit("erg")$
  corresponds to $(1 #unit("eV"))/k_B approx 1.1605 dot 10^4$ K. Thus a
  statement such as $k_B T_e = 10 #unit("eV")$ identifies an energy scale of
  roughly $1.16 dot 10^5$ K, while the electron and ion temperatures may still
  differ. A temperature also does not specify the total heat content: that
  depends on the number of particles and the volume.

  Temperature is an equilibrium concept. A collisionally equilibrated species
  can be described by the Maxwellian above, whereas a collisionless species
  may retain beams, anisotropy, or other non-Maxwellian structure. There is
  consequently no universal temperature at which matter abruptly enters the
  plasma state. Ionization, the energy source, collisionality, and the scale of
  the electromagnetic response decide whether an ionized gas behaves as a
  plasma.

  #summary[
    Speed sets the single-particle kinetic energy, while temperature sets the
    width and average energy of an equilibrium distribution. The script uses
    $v_("th,s")=sqrt((2 k_B T_s)/m_s)$ and treats electron and ion temperatures
    as separate quantities unless an equilibration assumption is stated.
  ]

  #exam-prompts(
    (
      [(a) At which temperature does matter enter the plasma state?],
      [(m) What is a Boltzmann distribution and how is it related to equilibrium states?],
    ),
    [Plasma Physics Exam.pdf, p. 1],
  )

  #knowledge-check((
    (
      question: [What quantity does a quoted plasma temperature in electron-volts represent?],
      answer: [It represents the thermal energy $k_B T_s$ expressed in electron-volts. The thermodynamic temperature $T_s$ can be recovered using the conversion to kelvin.],
    ),
    (
      question: [How does the chosen thermal-speed convention relate to $k_B T_s$?],
      answer: [$v_("th,s")=sqrt((2 k_B T_s)/m_s)$, so the one-dimensional Gaussian width is set by $(k_B T_s)/m_s$ and the three-dimensional mean kinetic energy is $(3 k_B T_s)/2$.],
    ),
    (
      question: [Why can a plasma have separate electron and ion temperatures?],
      answer: [Interspecies energy exchange can be slower than equilibration within each species, so each species can have its own approximately Maxwellian distribution for the time scale being considered.],
    ),
    (
      question: [Why is there no universal temperature threshold for the plasma state?],
      answer: [Plasma behavior depends on ionization, collisionality, boundaries, and whether collective electromagnetic response matters on the chosen scales, not on temperature alone.],
    ),
  ))

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

  $ div(bold(B)) = 0, quad curl(bold(E)) = -1/c pdv(bold(B), t) $ <intro-maxwell-identities>

  #equation-note[
    Gaussian CGS. $c$ is the speed of light in $upright("cm") dot upright("s")^(-1)$.
    The divergence and curl equations are exact Maxwell equations, not a
    plasma approximation.
  ]

  #definition(
    [Quasineutrality],
    [On a macroscopic scale, a simple electron--positive-ion plasma is
    quasineutral when its net charge density is small compared with the
    individual species charge densities. This is an ordering statement, not
    an exact pointwise identity.]
  )

  $ rho_q = e (sum_i Z_i n_i - n_e) approx 0,
    quad n_e approx sum_i Z_i n_i $ <intro-quasineutrality>

  #equation-note[
    Gaussian CGS. $e$ is the positive elementary charge in statcoulomb and
    $Z_i$ is the integer ion charge state. For a singly ionized hydrogen
    plasma, the condition reduces to $n_e approx n_i$. Charge-separated
    regions of Debye-scale thickness and boundary sheaths are controlled
    departures from this bulk ordering.
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

  #details(
    [Order-of-magnitude examples],
    [The following ranges are orientation values rather than a phase diagram.
    The density column is $n_e$ in #unit("cm^-3"), and the energy column is
    $k_B T_e$ in electron-volts. A single named object can occupy more than one
    row as its local state changes.

    #table(
      columns: (2.6cm, 2.4cm, 2.6cm, 4.2cm),
      stroke: 0.5pt + muted,
      inset: 0.35em,
      table.header(
        [Setting],
        [$n_e$],
        [$k_B T_e$],
        [Characteristic emphasis],
      ),
      [Solar wind], [$1$--$10$], [$1$--$100$], [dilute, weakly collisional, magnetized],
      [Ionosphere], [$10^4$--$10^6$], [$0.1$--$1$], [partially ionized and collisional],
      [Glow discharge], [$10^9$--$10^12$], [$1$--$10$], [weak ionization and boundaries],
      [Solar corona], [$10^8$--$10^10$], [$10^2$--$10^3$], [hot, magnetized, nearly fully ionized],
      [Fusion plasma], [$10^13$--$10^15$], [$10^3$--$2 dot 10^4$], [hot, confined, collective],
    )
  ])

  The characteristic responses introduced by this script are Debye shielding,
  electron plasma oscillations, collective waves, gyromotion and guiding-center
  drifts, instabilities, and boundary sheaths. These are different limits of
  the same coupled particle--field system, not independent definitions of a
  plasma.

  #definition(
    [Ideal-plasma convention used here],
    [For the purposes of this script, an ideal plasma is weakly coupled and
    sufficiently populated that collective fields can be treated smoothly.
    A useful weak-coupling parameter is $Gamma_s = (q_s^2) / (a_s k_B T_s)$,
    where $a_s = (3 / (4 pi n_s))^(1/3)$ is the mean-spacing scale. The
    classical collective ordering also requires many particles in a Debye
    sphere and, when quasineutral fluid behavior is invoked, a system scale
    $L$ much larger than $lambda_D$. “Ideal” therefore does not mean cold,
    uniform, or exactly neutral at every point.]
  )

  #equation-note[
    Gaussian CGS. $a_s$ is in #unit("cm"), $(q_s^2) / (a_s k_B T_s)$ is
    dimensionless, and the weak-coupling condition is $Gamma_s << 1$.
  ]

  Classical statistics also have a validity boundary. For electrons, define
  the degeneracy parameter $theta_e = (k_B T_e) / E_(F,e)$, with the
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
      [(b) Describe some typical plasmas in nature and technology (Fig. 1.3).],
      [(c) What are characteristic phenomena in plasmas?],
      [(g) List features of an ideal plasma.],
      [(h) What is a quantum degenerate plasma and where does it appear?],
    ),
    [Plasma Physics Exam.pdf, p. 1],
  )

  #knowledge-check((
    (
      question: [What is the bulk meaning of quasineutrality?],
      answer: [On scales large compared with the charge-separation layer, the signed species charge densities nearly cancel: $rho_q approx 0$. This does not forbid Debye-scale charge separation or a sheath.],
    ),
    (
      question: [What do weak coupling and quasineutrality assert, respectively?],
      answer: [Weak coupling compares interaction and thermal energies through $Gamma_s << 1$. Quasineutrality compares the net charge density with the individual species charge densities on a stated macroscopic scale.],
    ),
    (
      question: [Which ordering distinguishes quantum degeneracy from classical statistics?],
      answer: [The ratio $theta_e = (k_B T_e) / E_(F,e)$ is the indicator: $theta_e >> 1$ is classical, while $theta_e <= 1$ requires quantum statistics.],
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

  $ Omega_s = (q_s B) / (m_s c), quad omega_(c,s) = abs(Omega_s) $ <intro-gyrofrequency>

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

  Combining the definitions gives the useful estimate requested whenever a
  thermal speed and a Debye length are known:

  $ lambda_D = v_("th,e")/(sqrt(2) omega_(p,e)),
    quad omega_(p,e) = v_("th,e")/(sqrt(2) lambda_D) $ <intro-plasma-frequency-debye-relation>

  #equation-note[
    Gaussian CGS. The factor $sqrt(2)$ follows from the convention
    $v_("th,e")=sqrt((2 k_B T_e)/m_e)$. If a source defines thermal speed as
    $sqrt((k_B T_e)/m_e)$, the same relation is written without that factor.
  ]

  A common collective ordering is the Debye number

  $ N_D = (4 pi)/(3) n_e lambda_D^3 >> 1 $ <intro-debye-number>

  #equation-note[
    Dimensionless. $N_D$ counts electrons inside a Debye sphere. The symbol
    $>> 1$ states an ordering assumption, not an exact numerical boundary.
  ]

  #details(
    [Why scale ratios come first],
    [#derivation-step[Compare resolved scales with kinetic scales]
    Select a model by comparing its smallest resolved length with

    $ lambda_D, quad rho_s .$

    Compare its fastest resolved time with

    $ omega_(p,s)^(-1), quad omega_(c,s)^(-1) .$

    A fluid model can still be useful when it does not resolve every orbit,
    but only after the unresolved motion has been averaged or closed.

    #derivation-step[State the reference scales]
    The ratios

    $ lambda_D/L, quad rho_s/L, quad omega/omega_(c,s) $

    are normalized quantities only after the system length $L$ and observation
    frequency $omega$ have been specified.]
  )

  #debye-profile

  #rechenbeispiel[
    Context: use a hydrogen plasma with $n_e = qty("1e14", "cm^-3")$,
    $T_e = qty("1e6", "K")$, $T_i = qty("1e6", "K")$, and
    $B = qty("1e4", "G")$. Assume singly charged ions, $n_i = n_e$, and use
    $m_e = qty("9.109e-28", "g")$,
    $m_i = qty("1.673e-24", "g")$, $e = 4.803 dot 10^(-10)$ statcoulomb,
    $k_B = qty("1.381e-16", "erg/K")$, and
    $c = qty("2.998e10", "cm/s")$. Take the perpendicular speed to be the
    thermal speed, $v_("perp,s") = v_("th,s") = sqrt((2 k_B T_s)/m_s)$, for each
    species.

    Target: report $lambda_D$, $omega_(p,e)$, $rho_e$, and $rho_i$.

    Numerical result: $lambda_D = qty("6.9e-4", "cm")$,
    $omega_(p,e) = qty("5.6e11", "s^-1")$,
    $rho_e = qty("3.1e-3", "cm")$, and $rho_i = qty("1.3e-1", "cm")$.
    These values are dimensional Gaussian-CGS results.
  ]

  #rechenbeispiel[
    Context: use a representative thermonuclear hydrogen plasma with
    $n_e = qty("1e14", "cm^-3")$, $T_e = qty("1e8", "K")$,
    $T_i = qty("1e8", "K")$, and $B = qty("5e4", "G")$. Assume
    singly charged ions, $n_i = n_e$. Use
    $m_e = qty("9.109e-28", "g")$,
    $m_i = qty("1.673e-24", "g")$, $e = 4.803 dot 10^(-10)$ statcoulomb,
    $k_B = qty("1.381e-16", "erg/K")$, and
    $c = qty("2.998e10", "cm/s")$. Take the perpendicular speed to be the
    thermal speed, $v_("perp,s") = v_("th,s") = sqrt((2 k_B T_s)/m_s)$, for each
    species.

    Target: report $lambda_D$, $omega_(p,e)$, $omega_(c,e)$,
    $omega_(c,i)$, $rho_e$, and $rho_i$.

    Numerical result: $k_B T_e approx qty("8.62", "keV")$,
    $lambda_D = qty("6.9e-3", "cm")$,
    $omega_(p,e) = qty("5.6e11", "s^-1")$,
    $omega_(c,e) = qty("8.8e11", "s^-1")$,
    $omega_(c,i) = qty("4.8e8", "s^-1")$,
    $rho_e = qty("6.3e-3", "cm")$, and
    $rho_i = qty("2.7e-1", "cm")$. These are rough dimensional
    Gaussian-CGS values for a hot confined plasma.
  ]

  #summary[
    The plasma frequency, gyrofrequency, Debye length, gyroradius, and Debye
    number provide a first ordering language. State the unit system and the
    reference scales before interpreting any ratio.
  ]

  #exam-prompts(
    (
      [(i) Estimate the plasma frequency $omega_p$ from thermal velocity $v_t$ and Debye length $lambda_D$.],
      [(j) Give rough values of particle density, temperature, plasma frequency, gyrofrequency (electrons, ions) and Debye length and gyroradius (thermal electrons, ion) in a thermonuclear plasma.],
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

  A first estimate of the size of a charge-separated region can be obtained
  before solving the shielding profile. Let $N$ denote a number density in a
  uniformly charged spherical region of radius $R$, with charge magnitude
  $e$ per particle. Gaussian Gauss's law gives the boundary potential scale

  $ phi(R) = (4 pi N e R^2)/3,
    quad abs(e phi(R)) approx k_B T_e
    => R approx sqrt((3 k_B T_e)/(4 pi N e^2)) $ <debye-charge-separation-scale>

  #equation-note[
    Gaussian CGS. $N$ is a number density in #unit("cm^-3"), $R$ is in cm,
    and $phi$ is in statvolt. The numerical factor depends on the assumed
    charge profile; the robust result is the scaling
    $R$ proportional to $sqrt((k_B T_e)/(N e^2))$.
  ]

  #details(
    [Derivation: potential scale of a uniformly charge-separated sphere],
    [#derivation-step[Compute the enclosed charge and field]
    The enclosed charge at radius $r$ is

    $ Q(r)=(4 pi)/3 N e r^3 .$

    Applying the Gaussian flux law to a sphere gives

    $ E(r) 4 pi r^2=4 pi Q(r) ,$

    and hence

    $ E(r)=(4 pi)/3 N e r .$

    #derivation-step[Estimate the boundary potential]
    Measured relative to infinity, the potential at the boundary of the
    uniformly charged sphere is

    $ phi(R)=Q(R)/R=(4 pi)/3 N e R^2 .$

    A thermal particle can cross or substantially rearrange the region when
    $abs(e phi(R))$ is comparable to $k_B T_e$. Solving that balance gives the
    displayed estimate. If $N=n_0$, then

    $ R approx sqrt(3) lambda_D .$

    The order-one factor depends on the charge geometry, so this is a
    charge-separation estimate rather than a new hard boundary.]
  )

  #assumption(
    [Linearized Boltzmann response],
    [Take a uniform, stationary ion background with $n_i = n_0$, mobile
    electrons at temperature $T_e$, no magnetic force in the equilibrium
    response, and a weak potential satisfying $abs(e phi) << k_B T_e$. The
    ions are treated as fixed on the electron response time.]
  )

  The electron equilibrium density follows from the electrostatic potential
  energy $-e phi$:

  $ n_e = n_0 exp((e phi) / (k_B T_e)) approx n_0 (1 + (e phi) / (k_B T_e)) $ <debye-boltzmann-response>

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
    [#derivation-step[Linearize the electron response]
    For a positive test potential, the electron potential energy is $-e phi$.
    The equilibrium Boltzmann factor is therefore

    $ exp((-(-e phi))/(k_B T_e))=exp((e phi)/(k_B T_e)) .$

    When $abs(e phi)/(k_B T_e) << 1$, expand it to first order:

    $ n_e approx n_0 (1+(e phi)/(k_B T_e)) .$

    With immobile ions, the charge density becomes

    $ rho_q=e n_0-e n_e approx -(e^2 n_0 phi)/(k_B T_e) .$

    #derivation-step[Insert the response into Poisson's equation]
    Define the Debye coefficient by

    $ lambda_D^(-2)=(4 pi n_0 e^2)/(k_B T_e) .$

    Inserting the charge response into the Gaussian-CGS Poisson equation gives

    $ laplacian phi-phi/lambda_D^2=0 .$

    In spherical symmetry, the decaying source solution has the form

    $ phi(r) "proportional to" exp(-r/lambda_D)/r .$

    The exponential factor is the shielding; $1/r$ is the unscreened geometric
    spreading of a point source.]
  )

  #debye-profile

  #animation(
    "../media/debye-shielding.mp4",
    "A movement-based normalized 1D slab model shows blue circular electron markers starting uniformly, drifting toward a localized positive test charge, and gathering into a negative screening cloud while orange triangular ion markers remain fixed. The right-hand plots update with the markers: electron density develops a central excess and the electrostatic potential contracts from a broad initial profile to a localized screened profile. Position is shown as x divided by the Debye length with unit [1], and time as t divided by the relaxation time with unit [1]. The animation is a deterministic pedagogical relaxation model, not a full 3D particle-in-cell calculation.",
    caption: [
      Debye shielding through motion: mobile electrons rearrange around a
      localized positive charge, and the self-consistent potential becomes
      short-ranged. The markers and profiles use the same normalized 1D slab
      model; the fixed ion background and the compensating box background are
      part of the stated reduction.
    ],
    poster: "../media/debye-shielding.png",
  )

  The animation has a direct static reading. At the start, the electron
  markers are uniformly distributed and the positive test charge produces a
  broad electrostatic response. As the markers move toward the charge, their
  negative density perturbation cancels the source field outside the central
  region. The density excess and the shrinking potential profile are plotted
  from the same evolving state, so the screening is caused by charge motion
  rather than by a pre-drawn screened curve.

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
      [(d) A spherical region of complete charge separation has a potential $Phi(r) = (N q_e / epsilon_0) r^2$ at its boundary. What size can such a region roughly have in a thermal plasma of temperature $T$ (potential energy = thermal energy)?],
      [(e) Describe and give an overview of the derivation for Debye shielding.],
    ),
    [Plasma Physics Exam.pdf, p. 1],
  )

  #knowledge-check((
    (
      question: [Why does a positive electrostatic potential increase the equilibrium electron density in the Boltzmann response?],
      answer: [An electron has charge $-e$, so its potential energy is $-e phi$. A positive $phi$ lowers that energy and produces the factor $exp((e phi) / (k_B T_e))$.],
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
      answer: [A potential comparable to or larger than $(k_B T_e)/e$, a time-dependent kinetic response, or a boundary within the shielding region violates the stated assumptions.],
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

  $ m_e dv(xi,t,2) = -e E = -4 pi n_0 e^2 xi $ <plasma-oscillation-force>

  #equation-note[
    Gaussian CGS. The force is in dynes. The negative sign is the restoring
    sign for the electron charge $-e$.
  ]

  Dividing by $m_e$ gives the harmonic-oscillator equation

  $ dv(xi,t,2) + omega_(p,e)^2 xi = 0, quad omega_(p,e) = sqrt((4 pi n_0 e^2)/m_e) $ <plasma-oscillation-frequency>

  #equation-note[
    Gaussian CGS. $omega_(p,e)$ is an angular frequency in $upright("s")^(-1)$.
    The cold model has no damping and no thermal dispersive correction.
  ]

  #details(
    [Derivation: the displacement oscillator],
    [#derivation-step[Create the charge-separation field]
    At equilibrium, positive ion and negative electron charge densities
    cancel. Shift the electron slab by $xi$. The overlap region remains nearly
    neutral, while the two boundary layers carry sheet charges of magnitude
    $e n_0 xi.$

    Gauss's law for two infinite sheets gives the uniform internal field

    $ E=4 pi e n_0 xi .$

    #derivation-step[Identify the oscillator]
    An electron feels $F=-e E$, so

    $ m_e dv(xi,t,2)=-4 pi n_0 e^2 xi .$

    The coefficient of $xi$ has units of $upright("s")^(-2)$ and identifies the
    square of the plasma frequency. Within the small-amplitude model,

    $ xi(t)=xi_0 cos(omega_(p,e) t+delta) .$
    ]
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
      [(f) Describe and derive electron plasma oscillations.],
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

  #details(
    [Complete classical particle--field model],
    [At the most complete classical level, every particle trajectory and both
    electromagnetic fields are evolved self-consistently:

    $ dv(bold(r)_(a)(t), t) = bold(v)_(a)(t) $

    $ m_a dv(bold(v)_(a)(t), t) = q_a [bold(E)(bold(r)_(a)(t), t)
      + (bold(v)_(a)(t) times bold(B)(bold(r)_(a)(t), t))/c] $

    $ rho_q(bold(r), t) = sum_a q_a delta(bold(r) - bold(r)_(a)(t)),
      quad bold(j)(bold(r), t) = sum_a q_a bold(v)_(a)(t)
        delta(bold(r) - bold(r)_(a)(t)) $

    $ div(bold(E)) = 4 pi rho_q, quad div(bold(B)) = 0 $

    $ curl(bold(E)) = -1/c pdv(bold(B), t),
      quad curl(bold(B)) = (4 pi)/c bold(j) + 1/c pdv(bold(E), t) $

    The discrete particle sources are coarse-grained when one passes to a
    kinetic distribution or to fluid moments. This is the sense in which the
    model is complete: all charged particles interact through the shared
    electromagnetic fields, subject to the classical and nonrelativistic
    assumptions stated here.]
  )

  #definition(
    [Distribution function],
    [For species $s$, $f_(s)(t, bold(r), bold(v))$ gives the density of particles
    near position $bold(r)$ and velocity $bold(v)$. Its normalization is
    $n_s = integral f_s dif bold(v)$. A fluid variable is a velocity moment of
    this distribution.]
  )

  The collisionless phase-space balance has the conservative form

  $ pdv(f_s, t) + div(f_s bold(v)) + div(f_s bold(a)_s) = 0 $ <intro-kinetic-balance>

  #equation-note[
    Gaussian CGS. This is a schematic collisionless kinetic equation. The
    acceleration $bold(a)_s$ is in $upright("cm") dot upright("s")^(-2)$, and the divergence in
    velocity space is distinct from the spatial divergence. Collisions add a
    right-hand-side operator $C_(s)[f]$.
  ]

  For electromagnetic acceleration,

  $ bold(a)_s = q_s/m_s (bold(E) + (bold(v) times bold(B)) / c) $ <intro-electromagnetic-acceleration>

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
    [#derivation-step[Identify the hierarchy]
    The kinetic equation evolves a function of three position and three
    velocity coordinates. Its zeroth moment gives density, its first moment
    gives bulk velocity, and its second central moment gives the pressure
    tensor.

    #derivation-step[Choose a closure]
    The moment equations form a hierarchy because the equation for one moment
    contains the next one. A fluid model closes that hierarchy by prescribing,
    for example, isotropic pressure, an equation of state, or a heat-flux
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
      [(k) Describe the most complete plasma model? (All particles interacting with electromagnetic forces)],
      [(l) What kind of models can be used for plasma and how are they related?],
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
