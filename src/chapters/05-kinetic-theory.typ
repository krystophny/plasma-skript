#import "../theme.typ": *
#import "../figures.typ": collision-paths, maxwellian-profile
#import "@preview/physica:0.9.8": div, grad, curl, pdv, dv
#import "@preview/unify:0.8.1": qty, unit

#let chapter = [
  #page-title[5. Kinetic theory of plasmas] <kinetic-theory>

  #lead[
    Single-particle theory follows individual orbits. Kinetic theory instead
    describes how many particles of each species occupy each range of
    positions and velocities. One distribution function per species retains
    velocity-space structure, such as beams and unequal spreads in different
    directions, that a few fluid variables cannot fully describe.
  ]

  #callout(
    [The central object],
    [The species distribution $f_(s)(t, bold(r), bold(v))$ is a density in
    phase space. Its velocity moments give density, bulk velocity, pressure,
    and higher transport variables. The kinetic equation tells this density
    how streaming, electromagnetic forces, and collisions change it.]
  )

  #section-title[Collisions in gases and plasmas] <kinetic-collisions>

  #lead[
    When does a particle retain the memory of its previous flight? The answer
    is set by the distance between effective collisions and by the time over
    which the plasma is being observed.
  ]

  #objectives((
    [define mean free path and collision frequency from a collision probability],
    [distinguish short-range neutral collisions from long-range Coulomb scattering],
    [explain the Coulomb logarithm and identify the limits of a collisional model],
  ))

  #unit-ledger[
    Gaussian CGS is active. Number density $n_s$ is in #unit("cm^-3"), a
    neutral collision cross section $sigma$ is in #unit("cm^2"), speed is in
    #unit("cm/s"), mean free path is in #unit("cm"), and collision frequency
    is in #unit("s^-1"). Charge is in statcoulomb and energy is in
    #unit("erg"). The dimensionless parameters $K_"n"$ and $ln Lambda$ are
    explicitly marked as such.
  ]

  #definition(
    [Binary collision picture],
    [For a projectile of species $a$ moving through a background of species
    $b$, let $sigma_(a b)$ be the effective cross section for the chosen
    collision criterion. In a distance $d ell$, the probability of a collision
    is $d P_(a b) = n_b sigma_(a b) d ell$. This local statement assumes an
    uncorrelated background and a cross section that is defined for the
    relative velocity under consideration.]
  )

  If the background is uniform, the survival probability $S(ell)$ after a
  flight of length $ell$ obeys

  $ dv(S,ell) = -n_b sigma_(a b) S, quad S(0)=1 $ <kinetic-survival>

  #equation-note[
    The coefficient $n_b sigma_(a b)$ has units #unit("cm^-1") in Gaussian
    CGS. The equation describes loss from the uncollided population, not loss
    of particles from the plasma.
  ]

  Therefore the mean free path and collision frequency are

  $ lambda_("mfp", a b) = 1/(n_b sigma_(a b)), quad
    nu_(a b) = n_b sigma_(a b) v_"rel", quad
    lambda_("mfp", a b) = v_"rel" / nu_(a b) $ <kinetic-mfp>

  #equation-note[
    The mean free path is in #unit("cm") and the collision frequency is in
    #unit("s^-1"). The relation uses the same relative speed in both
    quantities.
  ]

  #details(
    [Derivation: exponential flights and the mean free path],
    [#derivation-step[Write the survival equation]
    During a path segment $d ell$, the probability $S$ of having no collision
    changes by

    $ d S=-S n_b sigma_(a b) d ell .$

    Dividing by $d ell$ gives the differential equation for survival.

    #derivation-step[Find the first-collision distribution]
    Integrating from $0$ to $ell$ gives

    $ S(ell)=exp(-n_b sigma_(a b)ell) .$

    The probability density for the first collision is the loss of survival
    probability per unit length:

    $ p(ell)=n_b sigma_(a b) exp(-n_b sigma_(a b)ell) .$

    #derivation-step[Calculate the mean free path and collision rate]
    The mean path length is

    $ integral_0^infinity ell p(ell) dif ell=1/(n_b sigma_(a b)) .$

    A particle traveling at $v_"rel"$ samples this length in a mean time
    $lambda_"mfp"/v_"rel"$. The inverse time is therefore

    $ nu_(a b)=v_"rel"/lambda_"mfp" .$

    The exponential model is valid when successive encounters can be treated
    as independent and the background properties are approximately constant
    over one mean free path.]
  )

  In a neutral gas, the interaction range is often short compared with the
  macroscopic system size. A geometric cross section can then summarize the
  encounter. A plasma has a different collision geometry. Two charged
  particles interact through a Coulomb field, so many weak deflections can
  accumulate even when no single encounter is a large-angle event.

  #collision-paths

  #assumption(
    [Small-angle Coulomb scattering],
    [For a weakly coupled, fully ionized plasma, treat the dominant encounters
    as many small deflections. The distant part of the interaction is limited
    by collective screening, while the close part is limited by strong
    deflection or quantum diffraction. The resulting collision estimate is a
    transport frequency, not a literal hard-sphere collision count.]
  )

  The impact parameter $b$ is the perpendicular separation of the incoming,
  undeflected relative trajectory from the scattering center. For relative
  speed $v_"rel"$ and reduced mass $m_r$, the classical impact parameter for
  a ninety-degree deflection is

  $ m_r v_"rel"^2 b_90 = abs(q_a q_b), quad
    b_90 = abs(q_a q_b)/(m_r v_"rel"^2), quad
    m_r = (m_a m_b)/(m_a+m_b) $ <kinetic-b90>

  #equation-note[
    Gaussian CGS is used in the electrostatic relation. The potential energy
    of two charges is $(q_a q_b)/r$ in #unit("erg"), so $b_90$ is in
    #unit("cm").]

  The small-angle contributions add a logarithmic weight over impact
  parameters. With $b_"max"$ set by collective screening and
  $b_"min"$ set by the larger of strong deflection and quantum diffraction,

  $ b_"max" approx lambda_D, quad
    b_"min" approx max(b_90, b_"qm"), quad
    ln Lambda = ln(b_"max"/b_"min") $ <kinetic-coulomb-log>

  #equation-note[
    $ln Lambda$ is dimensionless. In a classical plasma, $b_"qm"$ may be
    omitted when the de Broglie wavelength is much smaller than $b_90$. The
    precise cutoffs depend on the collision operator and velocity average.
    This is the cutoff-logarithm convention, denoted $ln Lambda_"cut"$ in
    Chapter 9; that chapter separately defines the plasma parameter
    $Lambda=n_e lambda_D^3$ for its cited approximate collision rate.
  ]

  A representative scaling for the deflection frequency of a test species
  $a$ in a background $b$ is

  $ nu_(a b) "scales as"
    (n_b q_a^2 q_b^2 ln Lambda)/(m_a^2 v_a^3) $ <kinetic-coulomb-frequency>

  #equation-note[
    This is a scaling relation. Numerical coefficients and the replacement of
    $v_a$ by a relative-velocity average depend on the selected collision
    operator. The $v_a^(-3)$ dependence makes slow particles especially
    sensitive to Coulomb scattering.
  ]

  #interpretation(
    [What makes a plasma different from a gas?],
    [The important distinction is the interaction range. Neutral collisions
    are often summarized by a finite cross section. Coulomb interactions are
    long range, and collective screening plus cumulative small-angle
    deflections determine the transport rate. A plasma can therefore be
    collisionless on a chosen time scale even though every charged particle
    feels electromagnetic forces continuously.]
  )

  The comparison with a macroscopic length $L$ is summarized by the Knudsen
  number and, for a process with time scale $tau$, by a collisionality
  parameter:

  $ K_"n" = lambda_"mfp"/L, quad nu tau $ <kinetic-collisionality>

  #equation-note[
    Both $K_"n"$ and $nu tau$ are dimensionless. $K_"n" << 1$ means many collisions
    occur over a macroscopic flight, while $nu tau << 1$ means the process is
    effectively collisionless over the time $tau$.]

  #rechenbeispiel[
    Consider a weakly ionized gas with $n_b = qty("1e12", "cm^-3")$,
    $sigma_(a b) = qty("1e-15", "cm^2")$, and
    $v_"rel" = qty("1e8", "cm/s")$. Use the neutral-collision model above.
    Determine the mean free path and collision frequency.

    Numerical result: $lambda_"mfp" = qty("1e3", "cm")$ and
    $nu_(a b) = qty("1e5", "s^-1")$.
  ]

  #summary[
    A mean free path follows from the survival probability of an uncollided
    particle. In a gas, a finite cross section often controls it directly. In
    a plasma, long-range Coulomb deflections produce a Coulomb logarithm and a
    velocity-dependent transport frequency. The ratios $K_"n"$ and $nu tau$
    decide whether collisions must be retained for a particular process.
  ]

  #exam-prompts(
    (
      [(a) What’s the difference between a gas and a plasma in terms of collisions?],
      [(b) What’s the mean free path and how is it related to the collision frequency?],
    ),
    [Plasma Physics Exam.pdf, p. 2],
  )

  #knowledge-check((
    (
      question: [What probability law gives the mean free path in a uniform background?],
      answer: [The first-collision distance is exponentially distributed,
      $p(ell)=n_b sigma exp(-n_b sigma ell)$, with mean
      $lambda_"mfp"=1/(n_b sigma)$.],
    ),
    (
      question: [Why is the Coulomb logarithm dimensionless?],
      answer: [It is the logarithm of the ratio of two impact-parameter
      lengths, $ln Lambda=ln(b_"max"/b_"min")$.],
    ),
    (
      question: [What does $K_"n" approx 1$ indicate?],
      answer: [The mean free path and the macroscopic scale are comparable.
      A local fluid closure is then questionable and kinetic information is
      generally needed.],
    ),
    (
      question: [Why can a plasma be collisionless while particles still interact?],
      answer: [Collisionless means $nu tau << 1$ for the process under study.
      Electromagnetic forces can remain strong even when discrete collisional
      deflections are too infrequent to affect that process.],
    ),
  ))

  #section-title[Distribution functions and phase space] <kinetic-distribution>

  #lead[
    A single particle has a position and a velocity. How can an ensemble with
    an enormous number of particles be represented without storing every
    trajectory? A distribution function assigns density to the corresponding
    phase-space cells.
  ]

  #objectives((
    [define a species distribution and its normalization],
    [distinguish phase-space density from a normalized probability density],
    [compute density, bulk velocity, and pressure as velocity moments],
    [identify the parameters and meaning of a shifted Maxwellian],
  ))

  #unit-ledger[
    Gaussian CGS is active. Position is in #unit("cm"), velocity in
    #unit("cm/s"), and the phase-space measure
    $dif^3 bold(r) dif^3 bold(v)$ has units #unit("cm^6 s^-3"). The
    distribution $f_s$ therefore has units #unit("s^3 cm^-6") so that its
    integral over a phase-space cell gives a particle count. The moments $n_s$
    and $bold(u)_s$ are in #unit("cm^-3") and #unit("cm/s"), respectively.
  ]

  #definition(
    [Species distribution function],
    [For species $s$, $f_(s)(t,bold(r),bold(v))$ is defined by
    $d N_s = f_s dif^3 bold(r) dif^3 bold(v)$. It is the number density in
    six-dimensional phase space: three position coordinates and three
    velocity coordinates. Dividing $f_s$ by the total species particle number
    in a chosen domain gives a probability density on that domain; its
    integral over the domain is one. At a fixed position, a different
    normalization, $f_s/n_s$, gives the local velocity probability density.]
  )

  For any single-particle property $g(t,bold(r),bold(v))$, the local velocity
  average is

  $ ⟨g⟩_s = (1)/(n_s) integral_(RR^3)
    g(t,bold(r),bold(v)) f_(s)(t,bold(r),bold(v)) dif^3 bold(v) $
  <kinetic-local-average>

  #equation-note[
    The average is local in position. Setting $g=1$ gives one, while setting
    $g=bold(v)$ gives the bulk velocity $bold(u)_s$. The factor
    $(f_s)/(n_s)$ is a velocity-space probability density with units
    #unit("s^3 cm^-3").]

  At a fixed position, the velocity integral gives the number density:

  $ n_(s)(t,bold(r)) = integral f_(s)(t,bold(r),bold(v)) dif^3 bold(v) $ <kinetic-density>

  #equation-note[
    The velocity integral is over all of $RR^3$. The result is a number
    density in #unit("cm^-3"). The position dependence remains because the
    integration removes velocity information only.
  ]

  The first two useful velocity moments are the bulk velocity and the central
  pressure tensor:

  $ bold(u)_s = 1/n_s integral bold(v) f_s dif^3 bold(v), quad
    bold(w) = bold(v) - bold(u)_s, quad
    bold(P)_s = m_s integral bold(w) bold(w) f_s dif^3 bold(v) $ <kinetic-moments-preview>

  #equation-note[
    $bold(w)$ is the random velocity measured in the local bulk frame. The
    dyadic product $bold(w) bold(w)$ has components $w_i w_j$: each pairs two
    components of the random velocity. In Gaussian CGS,
    $bold(P)_s$ is a momentum-flux or pressure tensor with force-per-area
    units. Its scalar isotropic part is introduced in the moments chapter.
  ]

  A local equilibrium distribution with uniform temperature $T_s$ and drift
  velocity $bold(u)_s$ is the shifted Maxwellian

  $ f_(M,s) = n_s (m_s/(2 pi k_B T_s))^(3/2)
    exp(-(m_s abs(bold(v)-bold(u)_s)^2)/(2 k_B T_s)) $ <kinetic-maxwellian>

  #equation-note[
    Temperature is expressed through the thermal energy $k_B T_s$ in
    #unit("erg"). The one-dimensional standard deviation is
    $sqrt((k_B T_s)/m_s)$, while the parameter
    $v_"th,s"=sqrt((2 k_B T_s)/m_s)$ is the thermal-speed convention from
    Chapter 1. The plot below shows a one-component velocity distribution,
    whose centered peak is at zero velocity. It is not the distribution of
    speed magnitudes, which includes a velocity-space volume factor.]

  #details(
    [Derivation: normalization and central moments of a Maxwellian],
    [#derivation-step[Shift to random velocity]
    Set

    $ bold(c)=bold(v)-bold(u)_s, quad
      a=m_s/(2 k_B T_s) .$

    In these variables the three-dimensional Gaussian factorizes:

    $ integral exp(-a abs(bold(c))^2) dif^3 bold(c)
        = (integral exp(-a c_x^2) dif c_x)^3
        = (sqrt(pi/a))^3 .$

    #derivation-step[Normalize the distribution]
    The prefactor in $f_(M,s)$ is chosen so that the velocity integral is

    $ integral f_(M,s) dif^3 bold(v)=n_s .$

    Thus $n_s$ is the zeroth moment, independent of the choice of bulk
    velocity.

    #derivation-step[Evaluate the first and second central moments]
    Symmetry gives

    $ integral bold(c) f_(M,s) dif^3 bold(v)=bold(0) ,$

    so the first raw moment is $n_s bold(u)_s$. Each Cartesian component has
    variance

    $ 1/(2a)=(k_B T_s)/m_s .$

    Therefore the pressure tensor is isotropic:

    $ bold(P)_s=m_s n_s ((k_B T_s)/m_s) bold(I)
        =n_s k_B T_s bold(I) .$

    The derivation assumes a smooth Maxwellian with finite temperature; a
    cold delta distribution has the same density and flow moments but zero
    central pressure.]
  )

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

  Thermodynamic temperature characterizes equilibrium. Away from equilibrium,
  a kinetic temperature can still be defined by the second central velocity
  moment, $3 k_B T_s=m_s lr(⟨ abs(bold(v)-bold(u)_s)^2 ⟩)$.
  It measures random kinetic energy but does not specify the whole
  distribution. If the velocity spread depends on direction, a single scalar
  temperature does not capture that anisotropy; a pressure tensor is needed.
  A species that has reached thermal equilibrium through collisions can be
  described by the Maxwellian above, whereas a collisionless species may
  retain beams or other non-Maxwellian structure.

  #maxwellian-profile

  #interpretation(
    [What information is lost by taking a moment?],
    [The density keeps the total number at a position. The bulk velocity keeps
    the first velocity average. The pressure tensor keeps the covariance of
    random velocities. Distinct distributions can share these moments, so a
    finite set of fluid variables cannot reproduce every kinetic feature.
    Closure assumptions enter when the retained moments are evolved.]
  )

  #summary[
    The distribution function is a phase-space density, not merely a curve of
    particle speeds. Integrating it over velocity gives density, weighting it
    once gives bulk flow, and weighting it twice about the bulk flow gives
    pressure. The Maxwellian is the normalized equilibrium reference state for
    elastic collisions at fixed density, flow velocity, and temperature.
  ]

  #exam-prompts(
    (
      [(c) What’s the meaning of the distribution function?],
    ),
    [Plasma Physics Exam.pdf, p. 2],
  )

  #knowledge-check((
    (
      question: [What does $f_s dif^3 bold(r) dif^3 bold(v)$ count?],
      answer: [It gives the number of species-$s$ particles in the specified
      six-dimensional phase-space cell.],
    ),
    (
      question: [Why does a shifted Maxwellian have zero first central moment?],
      answer: [After shifting to $bold(w)=bold(v)-bold(u)_s$, the Gaussian is
      even in every velocity component, so the integral of the odd vector
      $bold(w)$ vanishes.],
    ),
    (
      question: [Which moment distinguishes a hot isotropic plasma from a cold fluid?],
      answer: [The second central moment, or pressure tensor, is nonzero for a
      finite-temperature plasma and vanishes in the cold-fluid idealization.],
    ),
    (
      question: [Can two different distributions have the same density and bulk velocity?],
      answer: [Yes. Density and bulk velocity are only the zeroth and first
      moments. The distributions may differ in temperature, anisotropy, or
      non-Maxwellian tails.],
    ),
  ))

  #section-title[Convective derivatives and phase-space transport] <kinetic-derivatives>

  #lead[
    A distribution changes because particles cross phase-space cell faces and
    because collisions redistribute them. The Eulerian description measures
    this change at a fixed point. The Lagrangian description follows a moving
    phase-space trajectory.
  ]

  #objectives((
    [write the chain rule along a phase-space characteristic],
    [interpret Eulerian and Lagrangian views of the same evolution],
    [identify phase-space fluxes in position and velocity],
    [explain why collisionless Hamiltonian flow preserves phase-space volume],
  ))

  #unit-ledger[
    The dimensional variables are $bold(r)$ in #unit("cm"), $bold(v)$ in
    #unit("cm/s"), and $bold(a)$ in #unit("cm/s^2"). For the phase-space
    characteristic $bold(z)=(bold(r),bold(v))$, the two blocks of its velocity
    are $bold(V)_z=(bold(v),bold(a))$. We also use the normalized variables
    $xi=bold(r)/L_0$, $eta=bold(v)/v_0$, and
    $tau=(t v_0)/L_0$, all explicitly dimensionless.
  ]

  #definition(
    [Convective derivative],
    [For a scalar $g(t,bold(r),bold(v))$, the derivative along a particle
    trajectory is
    $ dv(g_(s),t,d:upright(D)) = pdv(g_(s),t) + bold(v) dot grad(g_(s))
    + bold(a)_s dot pdv(g_(s),bold(v))$. It follows the particle through both
    real space and velocity space.]
  )

  A characteristic is the phase-space curve defined by

  $ dv(bold(r),t) = bold(v), quad dv(bold(v),t) = bold(a)_s,
    quad bold(z)=(bold(r),bold(v)) $ <kinetic-characteristic>

  #equation-note[
    Position has units #unit("cm"), velocity has units #unit("cm/s"), and
    acceleration has units #unit("cm/s^2"). The phase-space coordinate is a
    bookkeeping pair with mixed units, so its normalized version is useful for
    visualizations.
  ]

  For any phase-space density, the conservative balance has the form

  $ pdv(f,t) + div(f bold(V)_z) = S $ <kinetic-phase-space-balance>

  #equation-note[
    Here $div$ is the divergence in the full phase space and $S$ is a source
    density. Expanding the flux gives separate spatial and velocity-space
    contributions. A collision operator is one possible source term in this
    balance.
  ]

  The normalized free-streaming equation used in the animation is

  $ pdv(f,tau) + bold(eta) dot grad(f) = 0 $ <kinetic-normalized-streaming>

  #equation-note[
    Both $bold(xi)=bold(r)/L_0$ and $bold(eta)=bold(v)/v_0$ are dimensionless.
    The time coordinate is $tau=t/tau_0$ with $tau_0=L_0/v_0$;
    restore positions, velocities, and times with $L_0$, $v_0$, and $tau_0$.
    In the one-dimensional visualization, the vector equation reduces to
    $pdv(f,tau)+eta pdv(f,xi)=0$ with $xi=x/L_0$ and $eta=v/v_0$. The physical
    kinetic equation is three-dimensional in both position and velocity.
  ]

  #details(
    [Derivation: the Eulerian chain rule],
    [#derivation-step[Apply the multivariable chain rule]
    Let $g(t,bold(r),bold(v))$ be evaluated on a trajectory
    $bold(r)=bold(r)(t)$ and $bold(v)=bold(v)(t)$. A small time step gives

    $ d g=pdv(g,t) d t+grad(g) dot d bold(r)
        +pdv(g,bold(v)) dot d bold(v) .$

    #derivation-step[Insert the characteristic velocities]
    Divide by $d t$ and use

    $ dv(bold(r),t)=bold(v), quad
      dv(bold(v),t)=bold(a)_s .$

    The derivative along the characteristic is then

    $ dv(g,t)=pdv(g,t)+bold(v) dot grad(g)
        +bold(a)_s dot pdv(g,bold(v)) .$

    #derivation-step[Distinguish the two viewpoints]
    At a fixed phase-space point, only the partial derivative $pdv(g,t)$ is
    measured. Along a characteristic, the spatial and velocity-space
    advection terms contribute as well. The two descriptions are equivalent
    because they evaluate the same scalar field in different ways.]
  )

  #details(
    [Derivation: phase-space flux balance],
    [#derivation-step[Account for the four phase-space contributions]
    Take a small cell $d^3 bold(r) d^3 bold(v)$. Its particle count changes by
    temporal accumulation, spatial flux through the position faces,
    velocity-space flux through the velocity faces, and collisions.

    #derivation-step[Write the two fluxes]
    The spatial flux is $f bold(v)$ and the velocity-space flux is
    $f bold(a)_s$. Dividing the cell balance by its volume and taking the
    cell-size limit gives

    $ pdv(f,t)+div(f bold(v))+div(f bold(a)_s)=S .$

    #derivation-step[Combine position and velocity space]
    Define the phase-space velocity

    $ bold(V)_z=(bold(v),bold(a)_s) .$

    The two divergence terms are then the compact conservative flux of
    particles through phase space. This form is valid provided the source
    $S$ represents all collisions, sources, and sinks not included in the
    characteristic flow.]
  )

  #animation(
    "../media/phase-space-advection.mp4",
    "A localized cloud of phase-space samples stretches and shifts to the right. The horizontal axis is position divided by L0 and the vertical axis is velocity divided by v0; time is normalized by L0/v0. Each sample keeps its velocity while its position advances, so faster samples move farther and the cloud shears. Horizontal characteristic arrows have lengths proportional to velocity.",
    caption: [
      Free streaming in one spatial and one velocity dimension. The
      visualization uses normalized variables and a deterministic sample of a
      distribution, not a particle simulation or measured data.
      Arrow lengths are proportional to $eta=v/v_0$ and represent displacement
      over the same normalized time interval.
    ],
    poster: "../media/phase-space-advection.png",
  )

  #interpretation(
    [Eulerian and Lagrangian pictures],
    [The Eulerian picture asks how the distribution at one fixed phase-space
    location changes. The Lagrangian picture follows a characteristic through
    phase space. In the free-streaming example, a particle keeps its velocity
    and moves horizontally in the position--velocity plane. The distribution
    at a fixed point can change as particles pass, even while its value along
    each characteristic remains constant.]
  )

  #summary[
    A convective derivative follows a particle through position and velocity.
    A conservative balance counts particles entering and leaving phase-space
    cells. Relating the two forms requires accounting for any compression of
    the characteristic flow. The free-streaming animation isolates spatial
    transport: velocities stay fixed and the cloud shears because faster
    particles travel farther. Acceleration would also move particles through
    velocity-space cell faces.
  ]

  #exam-prompts(
    (
      [(d) Sketch how the distribution function changes over time due to fluxes in phase-space (also collisions, see Fig. 3.3)],
      [(e) What is a convective derivative in terms of Euler and Lagrange picture?],
    ),
    [Plasma Physics Exam.pdf, p. 2],
  )

  #knowledge-check((
    (
      question: [What does the spatial part of a phase-space flux transport?],
      answer: [The flux $f bold(v)$ transports particles across position-space
      cell faces at their physical velocity.],
    ),
    (
      question: [What does the velocity-space flux transport?],
      answer: [The flux $f bold(a)$ transports particles across velocity-space
      cell faces as forces change their velocities.],
    ),
    (
      question: [When is the convective derivative of a distribution zero?],
      answer: [It is zero without collisions or sources when the phase-space
      flow is incompressible, as for Lorentz motion. In general,
      $dv(f,t,d: upright(D))=-f (div_(bold(r))(bold(v))
      +div_(bold(v))(bold(a)))$ along a source-free characteristic;
      velocity-dependent drag can compress phase space.],
    ),
    (
      question: [Why does free streaming shear a phase-space cloud?],
      answer: [Each sample keeps its velocity but advances by a distance
      proportional to that velocity. The faster part therefore moves farther
      in position during the same normalized time.],
    ),
  ))

  #section-title[The Boltzmann and Vlasov equations] <kinetic-boltzmann>

  #lead[
    The phase-space balance becomes a plasma kinetic equation after the force
    and collision terms are specified. The conservative and convective forms
    carry the same particle balance when the phase-space flow is
    incompressible.
  ]

  #objectives((
    [write the Boltzmann equation for a species in Gaussian CGS],
    [transform its conservative form into convective form],
    [state the phase-space incompressibility condition for Lorentz motion],
    [distinguish the collisional Boltzmann equation from the collisionless Vlasov equation],
  ))

  #unit-ledger[
    Gaussian CGS is active. For species $s$, $q_s$ is in statcoulomb, $m_s$ is
    in grams, $bold(E)$ is in statvolt per centimetre, $bold(B)$ is in gauss,
    and $bold(a)_s$ is in #unit("cm/s^2"). The collision operator has units
    of $f_s$ per second, so it is written as #unit("s^-1") times a
    distribution density.
  ]

  #strong[From discrete particles to a distribution] <kinetic-particle-model>

  #details(
    [Complete classical particle--field model],
    [At the most complete classical level, every particle trajectory and both
    electromagnetic fields are evolved self-consistently. In each particle's
    force, its singular self-field is excluded or regularized; radiation
    reaction is neglected in this nonrelativistic model:

    $ dv(bold(r)_(a)(t), t) = bold(v)_(a)(t) $

    $ m_a dv(bold(v)_(a)(t), t) = q_a [bold(E)(bold(r)_(a)(t), t)
      + (bold(v)_(a)(t) times bold(B)(bold(r)_(a)(t), t))/c] $

    $ rho_q (bold(r), t) = sum_a q_a delta(bold(r) - bold(r)_(a)(t)),
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

  The electromagnetic acceleration follows from the Gaussian-CGS Lorentz
  force:

  $ bold(a)_s = q_s/m_s (bold(E) + (bold(v) times bold(B))/c) $ <kinetic-acceleration>

  #equation-note[
    The speed of light $c$ is in #unit("cm/s"). The acceleration is in
    #unit("cm/s^2"). The magnetic term changes the direction of velocity and
    the electric term can change its magnitude.
  ]

  Let $C_(s)[f]$ denote the velocity-space redistribution caused by collisions.
  The conservative kinetic equation is

  $ pdv(f_s,t) + div(f_s bold(v))
    + div(f_s bold(a)_s) = C_(s)[f] $ <kinetic-conservative>

  #equation-note[
    The first divergence acts on position at fixed velocity; the second acts
    on velocity at fixed position. This convention also applies to the
    expanded fluxes below. The equation is a number balance in phase space.
    The source $C_(s)[f]$ conserves the particle number of species $s$ for
    ordinary binary collisions.
  ]

  Expanding the two fluxes gives

  $ div(f_s bold(v)) = bold(v) dot grad(f_s)
    + f_s div(bold(v)), $ \
  $ div(f_s bold(a)_s)
    = bold(a)_s dot pdv(f_s,bold(v))
    + f_s div(bold(a)_s). $ <kinetic-product-rules>

  Position and velocity are independent phase-space coordinates, so the
  spatial divergence of $bold(v)$ vanishes. The Lorentz acceleration does
  depend on velocity, but its velocity-space divergence vanishes: the
  electric part translates velocities and the magnetic part rotates them
  without compressing velocity-space volume. Thus

  $ div(bold(v)) = 0, quad div(bold(a)_s) = 0. $ <kinetic-liouville>

  #equation-note[
    These are the incompressibility conditions for the six-dimensional
    characteristic flow. They are statements about phase-space volume, not
    about the spatial compression of a fluid density.
  ]

  The convective form is therefore

  $ dv(f_(s),t,d:upright(D)) = pdv(f_(s),t) + bold(v) dot grad(f_(s))
    + bold(a)_s dot pdv(f_(s),bold(v)) = C_(s)[f] $ <kinetic-convective>

  When the collision operator is neglected, this becomes the Vlasov equation:

  $ pdv(f_s,t) + bold(v) dot grad(f_s)
    + q_s/m_s (bold(E) + (bold(v) times bold(B))/c)
      dot pdv(f_s,bold(v)) = 0 $ <kinetic-vlasov>

  #equation-note[
    The Vlasov equation is collisionless, not force-free. Self-consistent
    electromagnetic fields can still accelerate particles and bend their
    trajectories. The omitted collisions must be small on the process time
    scale.
  ]

  #details(
    [Derivation: conservative form to convective form],
    [#derivation-step[Start from the conservative equation]
    Use

    $ pdv(f_s,t)+div(f_s bold(v))+div(f_s bold(a)_s)=C_(s)[f] .$

    #derivation-step[Apply the product rule]
    Expanding both flux divergences gives

    $ pdv(f_s,t)+bold(v) dot grad(f_s)
        +bold(a)_s dot pdv(f_s,bold(v))
        +f_s dot [div(bold(v))+div(bold(a)_s)]=C_(s)[f] .$

    #derivation-step[Use incompressibility of Lorentz characteristics]
    For Lorentz motion, $div(bold(v))=0$ because $bold(v)$ is an independent
    velocity coordinate in the spatial divergence. Also
    $div(bold(a)_s)=0$: the electric acceleration is velocity independent,
    while the magnetic acceleration is linear in $bold(v)$ with an
    antisymmetric cross-product matrix of zero trace.

    Removing the vanishing bracket gives the convective form. The equivalence
    relies on the zero divergence of the phase-space characteristic flow.]
  )

  #details(
    [Derivation: particle-number conservation],
    [#derivation-step[Integrate over velocity space]
    Integrate the conservative equation over all velocity space. Assume
    $f_s$ and the velocity-space flux vanish as $abs(bold(v))$ tends to
    infinity. The velocity-space divergence becomes a boundary term and
    vanishes.

    #derivation-step[Use the collision invariant]
    Number-conserving binary collisions obey

    $ integral C_(s)[f] dif^3 bold(v)=0 .$

    #derivation-step[Identify the fluid density and flux]
    The remaining velocity integrals are

    $ integral f_s dif^3 bold(v)=n_s, quad
      integral bold(v)f_s dif^3 bold(v)=n_s bold(u)_s .$

    Therefore

    $ pdv(n_s,t)+div(n_s bold(u)_s)=0 .$

    This species continuity equation is the first bridge from kinetic theory
    to fluid theory. It assumes that no particles are created or removed by
    the selected collision model.]
  )

  #interpretation(
    [What does the collision operator change?],
    [Binary elastic collisions redistribute particles in velocity space. They
    can relax a non-equilibrium distribution toward a Maxwellian while
    conserving species particle number. Momentum and energy conservation are
    imposed on the combined interacting species, not necessarily on each
    species separately.]
  )

  #summary[
    The Boltzmann equation is a phase-space conservation law with a collision
    operator. Lorentz characteristics are incompressible in phase space, so
    the conservative equation and the convective equation are equivalent. The
    Vlasov equation is the collisionless limit and still contains the full
    electromagnetic acceleration.
  ]

  #exam-prompts(
    (
      [(f) Write down and explain the convective and conservative variant of the plasma kinetic (Boltzmann) equation. Why can one transform one into the other?],
    ),
    [Plasma Physics Exam.pdf, p. 2],
  )

  #knowledge-check((
    (
      question: [What condition makes the two kinetic forms equivalent?],
      answer: [The phase-space characteristic flow must have zero divergence,
      $div(bold(v))+div(bold(a))=0$. Lorentz motion satisfies
      this condition.],
    ),
    (
      question: [What is the Vlasov approximation?],
      answer: [It neglects the collisional redistribution term on the chosen
      time and length scales while retaining self-consistent electromagnetic
      forces.],
    ),
    (
      question: [Why must $C_(s)[f]$ integrate to zero over velocity for ordinary collisions?],
      answer: [Collisions rearrange the velocities of species-$s$ particles,
      so they do not create or destroy the number of particles of that species.],
    ),
    (
      question: [What is the first fluid equation obtained by integrating the kinetic equation?],
      answer: [The species continuity equation,
      $pdv(n_s,t)+div(n_s bold(u)_s)=0$, provided the velocity-space boundary
      flux vanishes and collisions conserve particle number.],
    ),
  ))

  #section-title[Maxwellian equilibrium and kinetic model limits] <kinetic-equilibrium>

  #lead[
    The Maxwellian is a reference state, not a universal shape. Its use is
    justified by collisional relaxation and the absence of unresolved sources
    that sustain non-equilibrium structure.
  ]

  #objectives((
    [state the conditions under which a Maxwellian is a collisional equilibrium],
    [derive the density response to a static electrostatic potential],
    [select between kinetic and fluid descriptions using scale orderings],
    [connect the kinetic description to the moment hierarchy of the next chapter],
  ))

  #unit-ledger[
    Gaussian CGS is active. The electrostatic potential $Phi$ is in statvolt,
    so $q_s Phi$ is an energy in #unit("erg"). Temperature enters through
    $k_B T_s$ in #unit("erg"). The ratios $nu tau$, $K_"n"$, and
    $lambda_D/L$ are dimensionless and must not be read as dimensional
    frequencies or lengths.
  ]

  #assumption(
    [Static isothermal equilibrium],
    [Take a time-independent electrostatic potential, uniform temperature, no
    bulk flow, and a collision operator whose stationary state is the
    Maxwellian. For full multispecies collisional equilibrium the temperature
    is common to all species; distinct species temperatures describe only
    self-collision equilibrium or an approximation neglecting interspecies
    energy exchange. The equilibrium is local in position and isotropic in
    the local rest frame.]
  )

  Let $n_(0,s)$ be the species density where the reference potential is
  $Phi=0$. A species in this equilibrium has the energy-dependent distribution

  $ f_("eq,s")(bold(r),bold(v)) = n_(0,s)
    (m_s/(2 pi k_B T_s))^(3/2)
    exp(-((m_s v^2)/2 + q_s Phi(bold(r)))/(k_B T_s)) $ <kinetic-equilibrium-distribution>

  Integrating over velocity gives the Boltzmann density response:

  $ n_(s)(bold(r)) = n_(0,s) exp(-(q_s Phi(bold(r)))/(k_B T_s)) $ <kinetic-boltzmann-response>

  #equation-note[
    The exponent is dimensionless because both $q_s Phi$ and $k_B T_s$ are
    energies in #unit("erg"). For electrons, $q_e<0$, so a positive
    potential increases the electron density in this convention.
  ]

  #details(
    [Derivation: Maxwellian equilibrium in a potential],
    [#derivation-step[Use the single-particle invariant]
    In a static electrostatic field, the single-particle energy is

    $ H_s=(m_s v^2)/2+q_s Phi(bold(r)) .$

    A stationary collisional equilibrium depends on velocity through this
    invariant and has the Maxwellian form

    $ f_("eq,s")=A_s exp(-(H_s)/(k_B T_s)) .$

    #derivation-step[Choose the normalization]
    Choose

    $ A_s=n_(0,s)(m_s/(2 pi k_B T_s))^(3/2) .$

    At $Phi=0$, the velocity integral is then $n_(0,s)$.

    #derivation-step[Separate velocity and position]
    Factor the exponential into a velocity part and a position part. The
    normalized Gaussian integrates to one, leaving

    $ n_(s)(bold(r))=n_(0,s) exp(-(q_s Phi)/(k_B T_s)) .$

    The result assumes a static potential, a spatially uniform temperature,
    and an equilibrium that is Maxwellian in the conserved single-particle
    energy.]
  )

  #callout(
    [Collision frequency is a model selector],
    [For a process with characteristic time $tau$ and length $L$, use
    $nu tau$ and $K_"n"=lambda_"mfp"/L$ together. A small $nu tau$ permits
    collisionless kinetic behavior. A small $K_"n"$ supports local fluid moments.
    These criteria answer different questions and can select hybrid models in
    which some directions or species are collisional while others are kinetic.]
  )

  The kinetic description remains necessary when the distribution contains
  velocity-space beams, anisotropic tails, resonant structure, or boundary
  layers whose width is comparable to a mean free path. A fluid model becomes
  efficient when a small set of moments evolves slowly and a closure can
  represent the discarded velocity dependence. The next chapter performs the
  first velocity moments and makes the closure issue explicit.

  #interpretation(
    [Why does equilibrium not erase kinetic theory?],
    [Equilibrium gives a useful reference distribution and a way to test a
    collision model. Perturbations, boundaries, waves, and weakly collisional
    transport can carry information in the parts of $f_s$ that a Maxwellian
    does not contain. Kinetic theory is the framework that tracks both the
    reference state and those departures.]
  )

  #strong[Classical statistics and quantum degeneracy] <kinetic-degeneracy>

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

  #summary[
    Collisions drive elastic systems toward Maxwellian velocity distributions
    when sources and boundaries do not sustain non-equilibrium structure. A
    static electrostatic potential changes the density through the Boltzmann
    factor. The ratios $nu tau$ and $K_"n"$ determine which kinetic information a
    reduced model may safely discard.]

  #exam-prompts(
    (
      [(h) What is a quantum degenerate plasma and where does it appear?],
      [(m) What is a Boltzmann distribution and how is it related to equilibrium states?],
    ),
    [Plasma Physics Exam.pdf, p. 1],
  )

  #knowledge-check((
    (
      question: [What makes the Maxwellian a stationary collisional state?],
      answer: [The elastic self-collision operator vanishes on a local
      Maxwellian. Full multispecies collisional equilibrium also requires
      common mean flow and temperature; otherwise interspecies collisions
      exchange momentum or energy even between Maxwellian species.],
    ),
    (
      question: [Why is $(q_s Phi)/(k_B T_s)$ dimensionless?],
      answer: [Both the numerator and denominator are energies in Gaussian
      CGS, so their ratio has no units.],
    ),
    (
      question: [Which ordering supports a local fluid closure?],
      answer: [A small Knudsen number, $K_"n"=lambda_"mfp"/L << 1$, supports
      frequent local collisions over the macroscopic scale. A closure is
      still required for the moment hierarchy.],
    ),
    (
      question: [Give one example of kinetic information a Maxwellian cannot represent.],
      answer: [A beam, loss-cone, anisotropic tail, or resonant velocity-space
      structure requires information beyond density, flow, and temperature.],
    ),
  ))

  #chapter-nav(
    previous: (href: "04-single-particle-motion.html", title: [Single-particle motion]),
    next: (href: "06-moments.html", title: [Moments]),
  )
]
