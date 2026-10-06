#import "../theme.typ": *
#import "../figures.typ": model-hierarchy, intro-enclosed-charge, intro-heating-drift, intro-speed-distribution, intro-thermal-speed, intro-scale-ordering
#import "@preview/physica:0.9.8": grad, div, curl, laplacian, pdv, dv, vb
#import "../map.typ": model-map-figure, map-data, map-link

#let chapter = [
  #page-title(number: 1)[Introduction] <introduction>

  #lead[
    A plasma is a many-particle system whose long-range electromagnetic fields
    make the particles respond collectively. This chapter establishes the
    vocabulary through examples, characteristic lengths and times, and the
    models used to describe different observations. The next two chapters
    develop Debye shielding and plasma oscillations as separate physical
    responses. The scale hierarchy follows standard graduate treatments
    @inan2011 @chen2016 @bittencourt2004.
  ]

  #section-title[Plasma as a collective state] <intro-plasma-state>

  #lead[
    A plasma is recognized by its response: a local charge or current must
    influence particles beyond the
    nearest collision partner, while the system still contains enough
    particles for a smooth field description.
  ]

  #objectives((
    [distinguish a plasma state from a temperature threshold],
    [identify collective electromagnetic phenomena in a physical example],
    [select a model level from the relevant length and time scales],
  ))

  #unit-ledger[
    The temperature $T_s$ below is a thermodynamic temperature in kelvin, so
    $k_B T_s$ is an energy in #unit("J"). A symbol without a unit is
    explicitly marked dimensionless.
  ]

  #definition(
    [Working definition of a plasma],
    [A plasma is a collection of charged species whose collective
    electromagnetic response is important on the scale of interest. It need
    not be fully ionized, and there is no universal temperature at which matter
    abruptly becomes a plasma. Ionization, collisionality, boundaries, and the
    observation scale all matter.]
  )

  Three examples show why the observation matters as much as the name of the
  plasma:

  - In a glow discharge, energetic electrons sustain ionization while much of
    the gas remains neutral. Collisions with neutrals and particle collection
    at surfaces influence the electrical response.
  - In a magnetic fusion device, the field confines a hot plasma. Particle
    orbit sizes and collective fluid motion matter on different length and
    time scales, so one model need not describe both.
  - In the solar wind, a dilute plasma expands through a magnetic field.
    Infrequent collisions allow velocity distributions to retain structure
    that a density and a single temperature cannot specify.

  Other examples include the solar corona, planetary magnetospheres,
  lightning, arcs, and processing plasmas. These settings span many orders of
  magnitude in density and temperature; the table below lists typical
  values.

  The charge density is the species sum

  $ rho_q = sum_s q_s n_s $ <intro-charge-density>

  #equation-note[
    The charge density $rho_q$ is in #unit("C m^-3").
    The sum runs over all charged species.
  ]

  Charge and current generate electromagnetic fields, which in turn act on
  the particles. The self-consistent equations are given in
  #chapter-link("kinetic-particle-model")[the particle–field model].

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
    $e$ is the positive elementary charge in #unit("C") and
    $Z_i$ is the integer ion charge state. For a singly ionized hydrogen
    plasma, the condition reduces to $n_e approx n_i$. Charge-separated
    regions of Debye-scale thickness and boundary sheaths are controlled
    departures from this bulk ordering.
  ]

  #intro-enclosed-charge

  A plasma differs from a neutral gas in the range of its response. A charge imbalance can
  launch an electric field, a current can launch a magnetic perturbation, and
  the resulting fields can move many particles before local collisions erase
  the correlation.

  #animation(
    "../media/collective-response.mp4",
    "Two runs, one after the other, in the same panel with the same particle positions. First, neutral gas: a test particle flies straight and changes direction sharply at three contact collisions; only the struck neutrals start to move. Then, plasma: a positive test charge passes through resting electrons; arrows show an attractive force on every electron within about one to two Debye lengths of it at each moment, and its own path bends only slightly under the sum of many weak pulls. The video ends on a still of both final states side by side.",
    caption: [
      Range of the interaction. Neutral gas: hard spheres of equal mass
      that interact only at contact. Plasma: a positive test charge and
      resting electrons with the screened force derived from
      $-e^(-r\/lambda_D)\/r$; arrow length grows with the force and
      saturates near the charge. Lengths in units of $lambda_D$; the
      dashed circle has radius $lambda_D$. The screened force is prescribed.
    ],
    poster: "../media/collective-response.png",
  )

  #details(
    [Order-of-magnitude examples],
    [The density column is $n_e$ in #unit("m^-3"), and the energy column is
    $k_B T_e$ in electron-volts. A single named object can occupy more than one
    row as its local state changes.

    #table(
      columns: (2.6cm, 2.4cm, 2.6cm, 4.2cm),
      stroke: 0.5pt + muted,
      inset: 0.35em,
      table.header(
        [Setting],
        [ $n_e$],
        [$k_B T_e$],
        [Characteristic emphasis],
      ),
      [Solar wind], [$10^6$--$10^7$], [$1$--$100$], [dilute, weakly collisional, magnetized],
      [Ionosphere], [$10^10$--$10^12$], [$0.03$--$0.3$], [partially ionized and collisional],
      [Glow discharge], [$10^15$--$10^18$], [$1$--$10$], [weak ionization and boundaries],
      [Solar corona], [$10^14$--$10^16$], [$10^2$--$10^3$], [hot, magnetized, nearly fully ionized],
      [Fusion plasma], [$10^19$--$10^21$], [$10^3$--$2 dot 10^4$], [hot, confined, collective],
    )
  ])

  The characteristic responses introduced by this script are Debye shielding,
  electron plasma oscillations, collective waves, gyromotion and guiding-center
  drifts, instabilities, and boundary sheaths. These are different limits of
  the same coupled particle--field system.

  An ideal plasma, as used here, contains enough weakly interacting particles
  for smooth collective fields to be useful. Bulk quasineutrality also
  requires observing lengths larger than the charge-separation scale.
  #chapter-link("debye-collective-validity")[The collective validity criteria]
  quantify these conditions. Very dense plasmas can require quantum
  statistics; #chapter-link("kinetic-degeneracy")[the degeneracy criterion]
  distinguishes that regime from the classical description used in this course.

  #summary[
    A plasma is identified by its scale-dependent collective electromagnetic
    response. Bulk quasineutrality,
    weak coupling, and the validity of classical statistics are separate
    conditions, each checked at the scale of interest.
  ]

  #exam-prompts(
    (
      [(b) Describe some typical plasmas in nature and technology (Fig. 1.3).],
      [(c) What are characteristic phenomena in plasmas?],
      [(g) List features of an ideal plasma.],
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
      answer: [Weak coupling means that a typical pair interaction is small compared with thermal energy. Quasineutrality compares the net charge density with the individual species charge densities on a stated macroscopic scale.],
    ),
    (
      question: [Why can a weakly ionized gas still behave as a plasma?],
      answer: [Its charged component can sustain collective electromagnetic responses on the observation scale even when most particles are neutral.],
    ),
    (
      question: [What is lost when moving from the particle--field model to a fluid model?],
      answer: [Velocity-space and particle-level detail are averaged into moments, and a closure assumption supplies the unresolved higher moments.],
    ),
  ))

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
    When temperature is quoted in electron-volts, the intended quantity is the energy $k_B T_s$, not the
    thermodynamic temperature symbol by itself.
  ]

  For a particle of species $s$, the kinetic energy associated with speed $v$
  is

  $ epsilon_("kin,s") = (m_s v^2)/2, quad epsilon_("th,s") = k_B T_s $
  <intro-thermal-energy>

  #equation-note[
    The first quantity depends on the individual particle speed. The second
    is the thermal energy scale of an equilibrium population; both are in
    #unit("J"). A single particle need not have the population's average
    kinetic energy.
  ]

  Temperature measures the spread of random velocities around the bulk
  motion. Heating a population and accelerating it as a whole are therefore
  different changes. Throughout this course the thermal-speed convention is

  $ v_("th,s") = sqrt((2 k_B T_s)/m_s) $ <intro-thermal-speed>

  #equation-note[
    $v_("th,s")$ is in #unit("m/s"). It is a characteristic
    width, not the mean speed of the particles.
  ]

  #intro-heating-drift

  #intro-speed-distribution

  #chapter-link("kinetic-distribution")[Distribution functions and phase space]
  develops the Maxwellian, its normalization, and the connection between
  temperature and mean random kinetic energy.

  The conversion $1 #unit("eV") = 1.602176634 dot 10^(-19) #unit("J")$
  corresponds to $1 #unit("eV")\/k_B approx 1.1605 dot 10^4$ K. Thus a
  statement such as $k_B T_e = 10 #unit("eV")$ identifies an energy scale of
  roughly $1.16 dot 10^5$ K, while the electron and ion temperatures may still
  differ. A temperature also does not specify the total heat content: that
  depends on the number of particles and the volume.

  #intro-thermal-speed

  Electron and ion temperatures can differ when energy exchange between
  species is slow. Outside thermal equilibrium, one temperature does not
  describe beams or unequal velocity spreads in different directions.
  #chapter-link("kinetic-equilibrium")[Equilibrium and kinetic model limits]
  explains when a thermal description is adequate.

  There is consequently no universal temperature at which matter abruptly enters the
  plasma state. Ionization, the energy source, collisionality, and the scale of
  the electromagnetic response decide whether an ionized gas behaves as a
  plasma.

  #summary[
    Speed sets the single-particle kinetic energy, while temperature sets the
    width and average energy of an equilibrium distribution. The script uses
    $v_("th,s")=sqrt(2 k_B T_s\/m_s)$ and treats electron and ion temperatures
    as separate quantities unless an equilibration assumption is stated.
  ]

  #exam-prompts(
    (
      [(a) At which temperature does matter enter the plasma state?],
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
      answer: [$v_("th,s")=sqrt(2 k_B T_s\/m_s)$. At fixed mass, multiplying thermal energy by four doubles this characteristic speed.],
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

  #section-title[Characteristic scales and ordering] <intro-scales>

  #lead[
    A model must resolve the response being studied. Compare the size and
    duration of the observation with the distances and times over which
    particles and fields respond.
  ]

  #objectives((
    [distinguish screening, collective oscillation, and gyromotion],
    [explain why length and time scales affect model selection],
    [locate the quantitative treatment of a relevant response],
  ))

  #unit-ledger[
    Comparing two lengths or two times produces a dimensionless ratio; both
    must refer to the same physical problem.
  ]

  Screening describes how mobile charges rearrange around an electric
  disturbance. Far enough from a localized source, its influence is reduced.
  #chapter-link("intro-debye-shielding")[Debye shielding]
  derives the screening length and the assumptions behind bulk quasineutrality.

  A displaced electron population can also overshoot equilibrium because
  electrons have inertia. The charge separation then supplies a restoring
  force. #chapter-link("intro-plasma-oscillations")[Plasma oscillations]
  derives this motion and its natural response time.

  In a magnetic field, individual particles turn around field lines. Their
  orbit size and period determine whether this motion must be followed or
  can be averaged. #chapter-link("motion-lorentz")[Uniform-field gyromotion]
  defines these scales, with numerical examples in
  #chapter-link("motion-scale-estimates")[Comparing orbit and collective scales].

  Collisions introduce a further distance: how far a particle travels before
  its motion changes appreciably through scattering.
  #chapter-link("kinetic-collisions")[Collisions in gases and plasmas]
  relates this mean free path to the collision rate.

  #intro-scale-ordering

  For example, an instrument that averages over many tiny orbits may not
  need a model of each turn. An experiment that resolves a single orbit does.
  Likewise, bulk neutrality can be useful far from a wall while failing in
  the thin charge-separated layer next to it. Each approximation must match
  the observation; one small scale does not justify every simplification.

  #summary[
    Screening, oscillation, gyromotion, and collisions describe different
    responses. Comparing their scales with the observation tells us which
    processes to resolve and which might be averaged.
  ]

  #knowledge-check((
    (
      question: [How do shielding and plasma oscillations differ?],
      answer: [Shielding concerns an equilibrium rearrangement of charge; plasma oscillations concern the time-dependent restoring motion of displaced charges.],
    ),
    (
      question: [When might averaging over gyromotion be useful?],
      answer: [When observations and fields vary over distances and times much larger than an orbit and its period, and the omitted orbit detail does not control the response.],
    ),
    (
      question: [Why can bulk quasineutrality fail close to a wall?],
      answer: [The wall can create a thin charge-separated layer. Resolving that layer requires keeping the charge imbalance.],
    ),
    (
      question: [Does rapid screening imply frequent collisions?],
      answer: [No. Collective field response and collisional scattering have distinct scales that must be compared separately with the observation.],
    ),
  ))

  #section-title[From microscopic particles to a model] <intro-model-hierarchy>

  #lead[
    Which description should be used for a given plasma problem? Keep the
    variables needed by the observable,
    then justify every average, closure, and ordering that removes detail.
  ]

  #objectives((
    [map particle, kinetic, multiple-fluid, and MHD descriptions to retained variables],
    [explain what is lost when taking moments or combining species],
    [connect equilibrium distributions to the next kinetic description],
  ))

  The most complete classical description follows all charged particles
  together with the fields they generate. A single-particle approximation
  instead prescribes the fields; #chapter-link("motion-lorentz")[the Lorentz-force model]
  explains what can be learned from that approximation.

  Kinetic theory replaces the list of particles with a distribution over
  positions and velocities. It retains beams and directional structure that
  a density and temperature cannot describe.
  #chapter-link("kinetic-boltzmann")[The Boltzmann and Vlasov equations]
  evolve this distribution under forces and collisions.

  Fluid models keep averages such as density, bulk velocity, and pressure.
  #chapter-link("moments-continuity")[The continuity equation]
  illustrates how their conservation laws follow from kinetic theory.
  Discarding the rest of the distribution requires a
  #chapter-link("moments-closures")[closure assumption].
  Combining species into a single conducting fluid leads to
  #chapter-link("single-fluid-mhd")[magnetohydrodynamics], when its scale assumptions hold.

  #animation(
    "../media/particles-to-moments.mp4",
    "Top, about 700 particle points in the position-velocity plane: a dense band around zero velocity whose density varies along x, and a narrow beam near two and a half thermal speeds. The points are replaced by the smooth distribution f(x, v). Integrating over velocity gives, below, the density n(x), largest at the ends and smallest in the middle, and the bulk velocity u(x), largest where the density is smallest. Square markers from the particle sample lie on the exact curves; neither curve shows that some particles form a beam.",
    caption: [
      Particles, distribution function and moments in one dimension: a
      density-modulated Maxwellian at rest plus a uniform beam at
      $v = 2.5 v_"th"$. Integration over $v$ gives $n(x)$ and $u(x)$;
      squares are estimates from the plotted particles. Position in units
      of the period $L$, velocity in units of $v_"th"$, density in units of
      the mean background density $n_0$.
    ],
    poster: "../media/particles-to-moments.png",
  )

  #model-hierarchy

  #subsection-title[Map of plasma models] <intro-model-map>

  These four descriptions are a small part of a larger landscape. The map
  below places #map-data.nodes.len() plasma models between the first
  principles at the top, the classical Maxwell--Lorentz many-body system and
  the many-electron Schrödinger equation, and the fluid, wave and equilibrium
  models at the bottom; each arrow is a reduction with its own small
  parameters and assumptions.

  This course follows the highlighted route. It reaches the Vlasov equation
  by coarse graining instead of deriving it from the many-body dynamics, and
  it leaves the many-body hierarchy, the collision operators and drift
  kinetics to the Kinetic Theory course and the quantum branch to research.
  The #map-link[interactive map] shows the
  equations, assumptions and verification status of every model and
  reduction.

  #model-map-figure()

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
      question: [Why does a fluid description need a closure assumption?],
      answer: [It retains only a few averages. A closure supplies a model for the discarded distribution information that still affects their evolution.],
    ),
    (
      question: [State a model-selection question that must be answered before using MHD.],
      answer: [One must justify combining species into one fluid and closing the pressure or energy response at the length and time scales of interest.],
    ),
  ))

  #chapter-nav(
    next: (href: "02-thermal-equilibrium.html", title: [Temperature, entropy, and thermal ionization]),
  )
]
