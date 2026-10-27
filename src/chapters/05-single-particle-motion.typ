#import "../theme.typ": *
#import "../figures.typ": gyroradius-geometry, motion-mu-ramp, motion-loss-cone
#import "@preview/physica:0.9.8": grad, pdv, dv, curl, div

#let chapter = [
  #page-title(number: 5)[Single-particle motion] <single-particle-motion>

  #lead[
    The single-particle model prescribes electromagnetic fields and follows
    one charged particle through them. It supplies the orbit geometry that
    guiding-center, kinetic, and fluid descriptions later average or close.
  ]

  #section-title[The Lorentz force and uniform-field gyromotion] <motion-lorentz>

  #lead[
    What can an electric or magnetic field do to a charged particle? Splitting
    the Lorentz force into its electric and magnetic parts separates energy
    change from bending, before any approximation is introduced.
  ]

  #objectives((
    [separate the energy-changing and trajectory-bending parts of the force],
    [derive the circular orbit in a uniform magnetic field],
    [use the charge sign to determine the sense of gyration],
  ))

  #governing-law(
    [Lorentz force],
    [For prescribed fields, a particle obeys]
  )

  $ m_alpha dv(bold(v),t) = q_alpha (bold(E) + bold(v) times bold(B)) $ <motion-lorentz-force>

  #equation-note[
    $q_alpha$ and $m_alpha$ are the charge and mass of a particle of species
    $alpha$, for example $alpha = e$ for electrons and $alpha = i$ for ions.
    Multiplying each field term by $q_alpha$ gives its contribution
    to the force, in #unit("N"). Dividing the total force by $m_alpha$ gives the
    particle acceleration.
  ]

  The instantaneous power supplied by the fields is

  $ dv((m_alpha v^2)/2,t) = q_alpha bold(E) dot bold(v) $ <motion-energy>

  #equation-note[
    The kinetic energy is in #unit("J"). The magnetic term does no work
    because $bold(v) dot (bold(v) times bold(B)) = 0$.
  ]

  In a uniform magnetic field with $bold(E)=0$, choose
  $bold(B) = B bold(e)_z$. The perpendicular velocity components satisfy

  $ dv(v_x,t) = omega_c v_y, quad dv(v_y,t) = -omega_c v_x, quad omega_c = (q_alpha B)/m_alpha $ <motion-cyclotron-components>

  #equation-note[
    The gyrofrequency $omega_c$ is a signed angular frequency in
    $upright("s")^(-1)$: positive for ions, negative for electrons. The
    parallel velocity is constant, so the full orbit is a helix unless
    $v_parallel = 0$.
  ]

  #details(
    [Derivation: circular motion and the gyroradius],
    [#derivation-step[Balance magnetic bending and inertia]
    The magnetic force is perpendicular to $bold(v)_perp$, so it supplies
    centripetal acceleration without changing $v_perp$. Equating magnitudes,

    $ (m_alpha v_perp^2)/rho_L=abs(q_alpha) v_perp B , $

    gives the Larmor radius

    $ rho_L=(m_alpha v_perp)/(abs(q_alpha) B)=v_perp/abs(omega_c) . $

    #derivation-step[Decouple the component equations]
    Differentiating the first component equation once more and inserting the
    second gives

    $ dv(v_x,t,2)=omega_c dv(v_y,t)=-omega_c^2 v_x , $

    a harmonic oscillator at the angular frequency $abs(omega_c)$; $v_y$ obeys the same equation.

    #derivation-step[Integrate the component motion]
    Solving the perpendicular component equations gives, for the chosen
    coordinate orientation,

    $ v_x=v_perp cos(omega_c t+phi.alt), quad
      v_y=-v_perp sin(omega_c t+phi.alt) , $

    where the gyrophase $phi.alt$ at $t = 0$ is set by the initial velocity.
    Integrating once more gives

    $ x=x_0+v_perp/omega_c sin(omega_c t+phi.alt), quad
      y=y_0+v_perp/omega_c cos(omega_c t+phi.alt) , $

    a circle of radius $v_perp\/abs(omega_c)=rho_L$ about the constant
    guiding-center position $(x_0, y_0)$. Reversing $q_alpha$ reverses the sign of
    $omega_c$ and therefore reverses the sense of rotation, while the radius is
    unchanged. With $v_z=v_parallel$ constant, $z=z_0+v_parallel t$ and the
    orbit is a helix.]
  )

  The guiding center is the center of the circular orbit in the perpendicular
  plane. Its radius is the Larmor radius or gyroradius
  $rho_L=v_perp\/abs(omega_c)$, where $abs(omega_c)$ is
  the positive gyrofrequency. Thus a faster perpendicular particle has a
  larger orbit, while a stronger field bends the same particle more tightly.

  For species $alpha$, write the signed frequency as $omega_(c alpha)=q_alpha B\/m_alpha$,
  so that $omega_(c i) > 0$ and $omega_(c e) < 0$; both are angular
  frequencies in #unit("s^-1"). A thermal orbit estimate uses
  $v_(perp,alpha)=v_("th",alpha)=sqrt(2 k_B T_alpha\/m_alpha)$ in #unit("m/s"),
  giving $rho_(L alpha)=v_("th",alpha)\/abs(omega_(c alpha))$ in #unit("m").

  #gyroradius-geometry

  Viewed with $bold(B)$ pointing toward the reader, ions ($omega_c>0$) gyrate
  clockwise and electrons ($omega_c<0$) counterclockwise. In both cases the
  current of the orbiting charge produces a magnetic moment opposite to
  $bold(B)$: gyrating particles weaken the applied field, so a plasma is
  diamagnetic.

  #animation(
    "../media/gyration-top-view.mp4",
    "Top view of an ion and an electron gyrating in a uniform magnetic field that points out of the page. The ion circles clockwise on a large orbit, the electron counterclockwise on an orbit four times smaller, turning sixteen times while the ion turns once. Each particle is a small dot with a short fading trail; a bar marks each Larmor radius, and a clock shows the ion gyrophase.",
    caption: [
      Ion and electron gyration in a uniform $bold(B)$ out of the page, at
      equal temperature. A reduced mass ratio $m_i\/m_e=16$ (hydrogen: 1836)
      keeps both orbits visible: $rho_(L i)\/rho_(L e)=sqrt(m_i\/m_e)=4$ and
      $abs(omega_(c e))\/omega_(c i)=16$. Time is $omega_(c i) t$ [1].
    ],
    poster: "../media/gyration-top-view.png",
  )

  #animation(
    "../media/gyration-components.mp4",
    "An ion circles clockwise in a magnetic field pointing out of the page, with its perpendicular velocity drawn as an arrow. Beside it, two graphs trace the x component of the velocity, a cosine of amplitude v-perp, and the x position about the guiding center, a sine of amplitude rho_L, against the gyrophase over two turns.",
    caption: [
      Velocity and position components of a gyrating ion ($q_alpha>0$,
      gyrophase $phi.alt=0$): $v_x\/v_perp=cos omega_c t$ and
      $(x-x_0)\/rho_L=sin omega_c t$, both [1], over two gyroperiods.
    ],
    poster: "../media/gyration-components.png",
  )

  #animation(
    "../media/gyration-helix.mp4",
    "Oblique view of an ion moving on a helix around a vertical magnetic field line: it circles the dashed guiding-center line while advancing along the field at constant parallel speed. The projection of the orbit onto the base plane is a dashed circle of radius rho_L.",
    caption: [
      Helical orbit with $v_parallel != 0$ along $bold(B)=B bold(e)_z$: the
      pitch is $2 pi v_parallel\/omega_c=1.1 rho_L$; time is $omega_c t$ [1].
    ],
    poster: "../media/gyration-helix.png",
  )

  #interpretation(
    [Energy versus orbit geometry],
    [An electric field can change the particle's kinetic energy because it can
    have a component along the velocity. A magnetic field can change the
    direction of the velocity but not its speed in this single-particle model.
    This distinction remains useful when fields are later solved
    self-consistently.]
  )

  #strong[Comparing orbit and collective scales] <motion-scale-estimates>

  The following estimates compare orbit sizes with the
  #chapter-link("intro-debye-shielding")[Debye length]
  and #chapter-link("oscillation-scales")[plasma frequency].
  Each measures a different response; a small screening length alone does
  not justify averaging over a particle orbit.

  #rechenbeispiel[
    Context: use a hydrogen plasma with $n_e = qty("1e20", "m^-3")$,
    $T_e = qty("1e6", "K")$, $T_i = qty("1e6", "K")$, and
    $B = qty("1", "T")$. Assume singly charged ions, $n_i = n_e$, and use
    $m_e = qty("9.109e-31", "kg")$,
    $m_i = qty("1.673e-27", "kg")$, $e = qty("1.602e-19", "C")$,
    $epsilon_0 = qty("8.854e-12", "F/m")$, and
    $k_B = qty("1.381e-23", "J/K")$. Take the perpendicular speed to be the
    thermal speed, $v_(perp,alpha) = v_("th",alpha) = sqrt(2 k_B T_alpha\/m_alpha)$, for each
    species.

    Target: report $lambda_D$, $omega_(p,e)$, $rho_(L e)$, and $rho_(L i)$.

    Numerical result: $lambda_D = qty("6.9e-6", "m")$,
    $omega_(p,e) = qty("5.6e11", "s^-1")$,
    $rho_(L e) = qty("3.1e-5", "m")$, and $rho_(L i) = qty("1.3e-3", "m")$.
    These values are dimensional results.
  ]

  #rechenbeispiel[
    Context: use a representative thermonuclear hydrogen plasma with
    $n_e = qty("1e20", "m^-3")$, $T_e = qty("1e8", "K")$,
    $T_i = qty("1e8", "K")$, and $B = qty("5", "T")$. Assume
    singly charged ions, $n_i = n_e$. Use
    $m_e = qty("9.109e-31", "kg")$,
    $m_i = qty("1.673e-27", "kg")$, $e = qty("1.602e-19", "C")$,
    $epsilon_0 = qty("8.854e-12", "F/m")$, and
    $k_B = qty("1.381e-23", "J/K")$. Take the perpendicular speed to be the
    thermal speed, $v_(perp,alpha) = v_("th",alpha) = sqrt(2 k_B T_alpha\/m_alpha)$, for each
    species.

    Target: report $lambda_D$, $omega_(p,e)$, $abs(omega_(c e))$,
    $omega_(c i)$, $rho_(L e)$, and $rho_(L i)$.

    Numerical result: $k_B T_e approx qty("8.62", "keV")$,
    $lambda_D = qty("6.9e-5", "m")$,
    $omega_(p,e) = qty("5.6e11", "s^-1")$,
    $abs(omega_(c e)) = qty("8.8e11", "s^-1")$,
    $omega_(c i) = qty("4.8e8", "s^-1")$,
    $rho_(L e) = qty("6.3e-5", "m")$, and
    $rho_(L i) = qty("2.7e-3", "m")$. These are rough dimensional
    values for a hot confined plasma.
  ]

  #summary[
    The Lorentz force separates energy transfer by $bold(E)$ from magnetic
    bending. In a uniform $bold(B)$ field the perpendicular motion is circular
    with radius $rho_L = v_perp\/abs(omega_c)$, while the parallel motion is uniform.
  ]

  #exam-prompts(
    (
      [(a) What are the main differences between the electric and magnetic force acting on a charged particle? How does a background magnetic field $B$ change the effect of an electric field on particle orbits if it is parallel or perpendicular to $B$?],
      [(b) Compute the gyroradius by balancing centrifugal force and Lorentz force. Draw the direction of the gyration for ions/electrons if the $B$ field points inside the paper plane.],
    ),
    [Plasma Physics Exam.pdf, p. 2],
  )

  #exam-prompts(
    ([(j) Give rough values of particle density, temperature, plasma frequency, gyrofrequency (electrons, ions) and Debye length and gyroradius (thermal electrons, ion) in a thermonuclear plasma.],),
    [Plasma Physics Exam.pdf, p. 1],
  )

  #knowledge-check((
    (
      question: [Which part of the Lorentz force changes a particle's kinetic energy?],
      answer: [Only $q_alpha bold(E)$ can do work. The magnetic force is perpendicular to the instantaneous velocity and has zero power.],
    ),
    (
      question: [How does the gyroradius scale with particle mass at fixed $v_perp$ and $B$?],
      answer: [It is proportional to $m_alpha$, because $rho_L = m_alpha v_perp\/(abs(q_alpha)B)$.],
    ),
    (
      question: [What changes when the sign of $q_alpha$ changes in a uniform magnetic field?],
      answer: [The signed gyrofrequency and the sense of rotation change. The gyroradius magnitude and kinetic energy do not.],
    ),
    (
      question: [What limiting orbit results when $v_perp$ tends to zero?],
      answer: [The gyroradius tends to zero and only uniform motion parallel to the magnetic field remains in the ideal uniform-field model.],
    ),
  ))

  #section-title[Homogeneous-force drift and the $E times B$ drift] <motion-exb>

  #lead[
    A slowly moving orbit center can be found without solving the rapid
    gyromotion. What velocity makes a constant force balance the magnetic
    Lorentz force in a uniform field?
  ]

  #objectives((
    [derive the $E times B$ drift from a gyration-plus-drift ansatz],
    [generalize it to the drift velocity for a homogeneous force perpendicular to $bold(B)$],
    [identify which particle properties cancel from the common drift],
  ))

  #unit-ledger[
    A drift ratio such as $v_D\/v_perp$ is dimensionless only after both speeds
    use the same reference state.
  ]

  Resolve the electric field into components parallel and perpendicular to the
  magnetic field, with $bold(b) = bold(B)\/B$:

  $ bold(E) = E_parallel bold(b) + bold(E)_perp, quad
    m_alpha dv(v_parallel,t) = q_alpha E_parallel $ <motion-electric-decomposition>

  #equation-note[
    $E_parallel$ is the scalar component along $bold(B)$. It accelerates a
    particle along the field. The perpendicular component participates in
    gyromotion and, when static and homogeneous, in the common $E times B$
    drift derived below.
  ]

  For uniform, static $bold(E)$ and $bold(B)$, try a gyration carried along
  by a constant drift:

  $ bold(v) = v_parallel bold(b) + bold(v)_perp (t) + bold(v)_D $ <motion-exb-ansatz>

  #equation-note[
    All velocities are in #unit("m/s"). $bold(v)_perp (t)$ is the gyration of
    the previous section, $m_alpha dv(bold(v)_perp,t) = q_alpha bold(v)_perp times bold(B)$,
    and $bold(v)_D$ is a constant drift velocity perpendicular to $bold(B)$.
  ]

  Insert the ansatz into the Lorentz force. The gyration terms cancel on both
  sides, $dv(bold(v)_D,t, style: "horizontal") = 0$, and the parallel part was
  treated above, so the perpendicular remainder is

  $ bold(0) = bold(E)_perp + bold(v)_D times bold(B) . $

  Crossing with $bold(B)$ and using
  $(bold(v)_D times bold(B)) times bold(B) = -B^2 bold(v)_D$ gives

  $ bold(v)_D = (bold(E) times bold(B))/(B^2) $ <motion-exb-drift>

  #equation-note[
    With $E$ in #unit("V/m") and $B$ in #unit("T"), $E\/B$ is directly a
    speed in #unit("m/s"). The common $E times B$ drift is independent of species mass and charge sign.
  ]

  The remainder equation also states what the drift means. In a frame moving
  with $bold(v)_D$, the perpendicular electric field is
  $bold(E)'_perp = bold(E)_perp + bold(v)_D times bold(B) = bold(0)$, so there
  the particle only gyrates. In the laboratory the same circle is carried
  along at $bold(v)_D$. For $E\/B << c$ this split is exact, not an average
  over the orbit.

  #animation(
    "../media/exb-drift.mp4",
    "A positive charge gyrates clockwise around a guiding center translating rightward. Position axes are x/L0 and y/L0 [1]. The electric field points upward and the magnetic field out of the page; the drift v_D is E cross B.",
    caption: [
      Gyromotion plus the $E times B$ drift. With reference
      length $L_0$ and time $t_0$, the trajectory uses $omega_c t_0=2$,
      $rho_L\/L_0=0.65$, and $v_D t_0\/L_0=0.55$, all dimensionless.
    ],
    poster: "../media/exb-drift.png",
  )

  #animation(
    "../media/exb-frame-change.mp4",
    "An ion orbit in uniform crossed fields, drawn twice in the same axes. First, in the laboratory frame, the ion traces a looped trochoid that advances along E cross B. Second, in the frame moving with the drift velocity v_D, the electric field vanishes and the same ion moves on a fixed circle. Lengths in Larmor radii and time in inverse gyrofrequencies, with unit [1].",
    caption: [
      The $E times B$ drift as a change of frame, computed from the full
      Lorentz force for an ion with $E\/B = 0.4 v_perp$ over three turns.
      Laboratory frame: a trochoid whose fitted drift speed equals $E\/B$.
      Frame moving with $bold(v)_D$: $bold(E)' = bold(E) + bold(v)_D times bold(B) = 0$
      and the orbit is a circle of radius $rho_L$. Lengths in $rho_L$ and
      time $omega_c t$, both [1].
    ],
    poster: "../media/exb-frame-change.png",
  )

  #assumption(
    [Uniform crossed-field ordering],
    [Take uniform, time-independent $bold(B)$ and a constant force with
    $bold(F) dot bold(B) = 0$. The force may be electric, gravitational, or
    another prescribed force on the particle. Averaging over gyromotion
    leaves a constant orbit-center velocity. The pressure-gradient force
    used later in fluid theory acts on a population; it is not an additional
    microscopic force on an isolated particle.
  ]
  )

  The same argument holds with $q_alpha bold(E)_perp$ replaced by any such
  force. The force balance for a constant orbit-center velocity is

  $ bold(F) + q_alpha (bold(v)_D times bold(B)) = 0 $ <motion-force-balance>

  #equation-note[
    This is a vector force balance in #unit("N"). The drift has no
    acceleration because it describes the constant orbit-center translation.
  ]

  Crossing with $bold(B)$ and using $bold(v)_D dot bold(B)=0$ gives

  $ bold(v)_D = (bold(F) times bold(B))/(q_alpha B^2) $ <motion-general-drift>

  #equation-note[
    The result has velocity units, #unit("m/s"). It is valid for a homogeneous
    perpendicular force and a uniform magnetic field. For
    $bold(F)=q_alpha bold(E)$ the charge cancels and the $E times B$ drift is
    recovered.
  ]

  #details(
    [Derivation: the force drift as a cross product],
    [#derivation-step[Start from the orbit-center force balance]
    A constant drift velocity satisfies

    $ bold(F)+q_alpha (bold(v)_D times bold(B))=bold(0) . $

    The drift is perpendicular to $bold(B)$, so crossing the equation with
    $bold(B)$ uses

    $ (bold(v)_D times bold(B)) times bold(B)=-bold(v)_D B^2 . $

    #derivation-step[Solve for the drift]
    The cross-product equation becomes

    $ bold(v)_D=(bold(F) times bold(B))/(q_alpha B^2) . $

    For an electric force, $bold(F)=q_alpha bold(E)$, so both the charge magnitude
    and its sign cancel. Direct substitution into the original force balance
    checks the sign of the resulting $E times B$ drift.]
  )

  Gravity, $bold(F) = m_alpha bold(g)$ with the gravitational acceleration
  $bold(g)$ in #unit("m/s^2"), does not contain the charge:

  $ bold(v)_D = m_alpha/q_alpha (bold(g) times bold(B))/(B^2) $ <motion-gravity-drift>

  #equation-note[
    Ions and electrons drift in opposite directions, the electrons slower by
    $m_e\/m_i$. In a hydrogen plasma with $n_i = n_e = n$ in #unit("m^-3")
    the drifts carry the current density
    $bold(j) = sum_alpha n_alpha q_alpha bold(v)_D = n (m_i + m_e) (bold(g) times bold(B))\/B^2$
    in #unit("A/m^2").
  ]

  #animation(
    "../media/gravity-drift.mp4",
    "An ion and an electron gyrate in a uniform magnetic field with gravity pointing perpendicular to it. Their guiding centres drift sideways in opposite directions; the electron drift is sixteen times slower than the ion drift. Lengths in ion Larmor radii and time in inverse ion gyrofrequencies, with unit [1].",
    caption: [
      Gravity drift of an ion and an electron, computed from the full Lorentz
      force at a reduced mass ratio $m_i\/m_e = 16$ (hydrogen: 1836) and
      equal temperatures. The measured drifts agree with
      $(m_alpha\/q_alpha) (bold(g) times bold(B))\/B^2$ to better than
      $0.01$~%: opposite directions, electron drift 16 times smaller.
      Lengths in $rho_(L i)$ and time $omega_(c i) t$, both [1].
    ],
    poster: "../media/gravity-drift.png",
  )

  #summary[
    A homogeneous perpendicular force produces a drift
    $bold(v)_D = bold(F) times bold(B)\/(q_alpha B^2)$. For an electric force the
    charge cancels, so all magnetized species share the same $E times B$ drift;
    in the frame moving with it the electric field vanishes.
  ]

  #exam-prompts(
    (
      [(c) Derive the drift velocity in a magnetized plasma for a general homogeneous force.],
      [(d) What is the $E times B$ drift?],
    ),
    [Plasma Physics Exam.pdf, p. 2],
  )

  #knowledge-check((
    (
      question: [Why does the $E times B$ drift not depend on charge sign?],
      answer: [The electric force is $q_alpha bold(E)$, and the $q_alpha$ cancels the $1\/q_alpha$ in the general force-drift expression.],
    ),
    (
      question: [What component of a constant force is not represented by the perpendicular force drift?],
      answer: [A component parallel to $bold(B)$ accelerates the particle along the field and cannot be balanced by a magnetic force.],
    ),
    (
      question: [If $bold(E)$ is parallel to $bold(B)$, what happens to the $E times B$ drift?],
      answer: [The cross product vanishes. The electric field instead accelerates particles along the field, with a response that depends on charge and mass.],
    ),
    (
      question: [What is the physical meaning of averaging over gyromotion in the drift derivation?],
      answer: [It removes the rapid circular oscillation and retains the slower translation of the orbit center.],
    ),
  ))

  #section-title[Guiding-center approximation and magnetic moment] <motion-guiding-center>

  #lead[
    Real plasmas rarely have perfectly uniform fields. How can a circular
    orbit remain a useful local picture when the field changes across the
    orbit? The guiding-center approximation separates the fast gyration from
    the slow field variation.
  ]

  #objectives((
    [state the scale ordering behind guiding-center motion],
    [decompose position and velocity into guiding-center and gyromotion parts],
    [define the magnetic moment and identify its adiabatic character],
  ))

  #unit-ledger[
    Let $L_B$ denote the magnetic-field variation length in #unit("m") and
    $abs(omega_c)^(-1)$ the characteristic gyration time in seconds; the gyroperiod
    is $2 pi\/abs(omega_c)$. The ordering parameters $epsilon = rho_L\/L_B$ and
    $omega_"slow"\/abs(omega_c)$ are dimensionless. The magnetic moment defined
    below is in #unit("J/T"), equivalently #unit("A m^2").
  ]

  #assumption(
    [Slowly varying fields],
    [Assume $rho_L\/L_B << 1$, field variation during one gyroperiod is small,
    and the fields are smooth enough for a local orbit expansion. Collisions,
    wave-particle resonances, and abrupt boundaries can invalidate the
    averaging.
  ]
  )

  Write the particle position as

  $ bold(r)(t) = bold(R)(t) + bold(rho)(t), quad abs(bold(rho)) approx rho_L $ <motion-position-split>

  #equation-note[
    $bold(R)$ is the guiding-center position and
    $bold(rho)$ is the fast gyration vector. Both positions and $rho_L$ are in
    #unit("m").
  ]

  The velocity has the corresponding decomposition

  $ bold(v) = dv(bold(r),t)
    = dv(bold(R),t) + dv(bold(rho),t), quad
    dv(bold(R),t) = v_parallel bold(b) + bold(v)_D, quad
    dv(bold(rho),t) approx bold(v)_perp $ <motion-velocity-split>

  #equation-note[
    Every velocity is in #unit("m/s"). The first equality
    follows from the position split. The guiding center moves along the field
    at $v_parallel$ and across it at the slow drift $bold(v)_D$; the fast
    gyration velocity $bold(v)_perp$ averages to zero over one turn.
  ]

  For perpendicular gyromotion, define the magnetic moment

  $ mu = (m_alpha v_perp^2)/(2 B) $ <motion-magnetic-moment>

  #equation-note[
    $mu$ is an energy divided by magnetic field, in #unit("J/T"). It is an
    adiabatic invariant under the stated slow-variation ordering: it is
    constant to leading order in $epsilon$ as the particle samples a slowly
    changing field.
    Here “adiabatic” refers to the separation of orbit and field-variation
    scales, not to thermodynamic heat exchange.
  ]

  #details(
    [Derivation: magnetic moment, and its invariance from the mirror force],
    [For this energy argument, take a static magnetic configuration with no
    electric work at the retained order. Keep leading parallel motion along
    the field when evaluating the sampled change in $B$.

    #derivation-step[Compute the magnetic moment of one orbit]
    For one circular orbit, the gyroperiod and orbit area are

    $ T_"c"=(2 pi)/abs(omega_c), quad S=pi rho_L^2 . $

    The magnitude of the orbit current is

    $ I_"gyro"=abs(q_alpha)/T_"c"=(abs(q_alpha) abs(omega_c))/(2 pi) . $

    The magnetic dipole moment is current times area:

    $ mu=I_"gyro" S
      =(abs(q_alpha) abs(omega_c) rho_L^2)/2
      =(m_alpha v_perp^2)/(2 B) . $

    Here $mu$ is the positive scalar magnitude; the gyration produces a
    diamagnetic vector dipole.

    #derivation-step[Use the averaged mirror force]
    Let $s$ measure distance along a field line. The averaged mirror force is

    $ F_parallel=-mu pdv(B,s), quad
      m_alpha dv(v_parallel,t)=-mu pdv(B,s) . $

    Since $dv(s,t, style: "horizontal")=v_parallel$, the particle samples the field according to

    $ dv(B,t)=v_parallel pdv(B,s) . $

    Therefore the parallel kinetic energy changes as

    $ dv((m_alpha v_parallel^2)/2,t)
      =-mu v_parallel pdv(B,s) . $

    #derivation-step[Show adiabatic conservation]
    The magnetic part changes according to

    $ dv(mu B,t)=B dv(mu,t)+mu v_parallel pdv(B,s) . $

    Adding the two balances gives

    $ dv((m_alpha v_parallel^2)/2+mu B,t)=B dv(mu,t) . $

    In this static, leading-order guiding-center approximation, the total
    guiding-center energy is conserved, so $dv(mu,t, style: "horizontal") approx 0$. The ordering
    requires the field to vary little over one gyroperiod and one gyroradius.]
  )

  This static mirror argument transfers energy between parallel and
  perpendicular motion. In a slowly time-varying magnetic field, $mu$ can
  remain invariant while an induced electric field supplies energy: the
  increase of $mu B$ is then betatron acceleration, and total kinetic energy
  need not be conserved. Faraday's law gives this second route directly.

  #details(
    [Derivation: $mu$ from Faraday's law],
    [Take a uniform field $bold(B) = B(t) bold(e)_z$ that changes slowly,
    $abs(pdv(B,t, style: "horizontal")) << abs(omega_c) B$, with no parallel
    electric field and an orbit centred on the symmetry axis, so that the
    guiding center does not drift.

    #derivation-step[Work done in one turn]
    The induced electric field obeys $curl(bold(E)) = -pdv(bold(B),t, style: "horizontal")$.
    Over one turn it changes the perpendicular energy by

    $ delta((m_alpha v_perp^2)/2) = q_alpha integral.cont bold(E) dot dif bold(l) , $

    with the line integral taken along the orbit in the direction of motion.

    #derivation-step[Apply Stokes' theorem]
    Ions run around $bold(B)$ in the left-handed sense and electrons in the
    right-handed sense, so for both signs of the charge

    $ q_alpha integral.cont bold(E) dot dif bold(l) = abs(q_alpha) pi rho_L^2 pdv(B,t) . $

    #derivation-step[Compare with the field change]
    One turn lasts $2 pi\/abs(omega_c)$, during which the field changes by
    $delta B = pdv(B,t, style: "horizontal") 2 pi\/abs(omega_c)$. With
    $rho_L = m_alpha v_perp\/(abs(q_alpha) B)$ the energy gain becomes

    $ delta((m_alpha v_perp^2)/2) = (m_alpha v_perp^2)/(2 B) delta B = mu delta B . $

    To first order in $delta B$ the magnetic moment then changes by

    $ delta mu = (delta(m_alpha v_perp^2\/2))/B - mu (delta B)/B = 0 . $]
  )

  #animation(
    "../media/mu-ramp.mp4",
    "An ion circles the axis of a uniform magnetic field that grows smoothly from B0 to 2 B0 over about twenty gyrations. The orbit shrinks while readouts show the field, the magnetic moment and the flux through the orbit; the magnetic moment and the flux stay constant. Lengths in the initial Larmor radius and time in inverse initial gyrofrequencies, with unit [1].",
    caption: [
      An ion in a uniform field that grows smoothly from $B_0$ to $2 B_0$ over
      about twenty gyrations, computed from the full Lorentz force with the
      induced electric field of Faraday's law. The orbit shrinks as
      $rho_L prop B^(-1\/2)$, while $mu$ and the flux $pi rho_L^2 B$ through
      the orbit stay constant to better than $0.05$~%. Lengths in the
      initial $rho_L$ and time $omega_(c 0) t$, both [1], with
      $omega_(c 0) = q_alpha B_0\/m_alpha$.
    ],
    poster: "../media/mu-ramp.png",
  )

  "Constant to leading order" can be tested. The figure below doubles the
  field at different rates and records how much $mu$ has changed once the
  field is constant again.

  #motion-mu-ramp

  #rechenbeispiel[
    A proton has $m_i=qty("1.673e-27", "kg")$ and charge
    $q_i=e=qty("1.602e-19", "C")$. Use an initial field
    $B_0=qty("0.0100", "T")$, a final field $B_1=qty("0.0400", "T")$, and
    $v_(perp,0)=qty("1.00e5", "m/s")$. Assume that the field changes
    adiabatically, $mu$ is conserved, and there is no electrostatic energy
    exchange.

    Target: report $v_(perp,1)$, $rho_(L 0)$, and $rho_(L 1)$.

    Numerical result: $v_(perp,1)=qty("2.00e5", "m/s")$,
    $rho_(L 0)=qty("0.104", "m")$, and $rho_(L 1)=qty("0.0522", "m")$.
  ]

  The invariance has a Hamiltonian form. For a periodic motion whose
  parameters change slowly compared with its period, the action
  $J = integral.cont bold(p) dot dif bold(l)$ over one period is an adiabatic
  invariant. For the gyration, $J$ is proportional to $mu$, and the guiding
  center moves with the Hamiltonian

  $ H = (m_alpha v_parallel^2)/2 + mu B(bold(R)) + q_alpha Phi(bold(R)) $ <motion-gc-hamiltonian>

  #equation-note[
    $H$ is an energy in #unit("J") and $Phi$ the electrostatic potential in
    #unit("V"), both evaluated at the guiding center $bold(R)$. The term
    $mu B$ acts as a potential energy for the guiding center. Its parallel
    gradient gives the mirror force, its perpendicular gradient the
    grad-$B$ drift of the next section.
  ]

  #details(
    [Derivation: $mu$ as the action of the gyration],
    [#derivation-step[Canonical momentum on the orbit]
    With the vector potential $bold(A) = bold(B) times bold(r)\/2$ of the
    uniform field, $bold(r)$ measured from the orbit center, the canonical
    momentum across $bold(B)$ is
    $bold(p)_perp = m_alpha bold(v)_perp + q_alpha bold(A)$, in #unit("kg m s^-1").

    #derivation-step[Integrate over one turn]
    Along the orbit in the direction of motion, the kinetic part gives
    $2 pi m_alpha v_perp rho_L$. The vector-potential part is $q_alpha$
    times the magnetic flux through the orbit, counted with the sense of
    rotation; since ions circle $bold(B)$ left-handed and electrons
    right-handed, it is $-pi abs(q_alpha) B rho_L^2$ for both. Hence

    $ J = 2 pi m_alpha v_perp rho_L - pi abs(q_alpha) B rho_L^2
      = (2 pi m_alpha)/abs(q_alpha) mu = abs(q_alpha) pi rho_L^2 B . $

    The action is proportional to $mu$ and to the flux $pi rho_L^2 B$
    through the orbit.

    #derivation-step[Gyrophase as an ignorable coordinate]
    $H$ does not depend on the gyrophase $phi.alt$, so its conjugate momentum
    $p_phi.alt = (m_alpha\/q_alpha) mu$ is constant. Along the field line,
    $-pdv(H,s, style: "horizontal")$ gives

    $ m_alpha dv(v_parallel,t) = -mu pdv(B,s) - q_alpha pdv(Phi,s) . $

    Within the guiding-center model $mu$ is exactly conserved. The
    particle's $mu$ differs from the guiding-center value by terms of order
    $epsilon = rho_L\/L_B$, so for the particle it is constant to leading
    order in $epsilon$: an adiabatic invariant.]
  )

  #interpretation(
    [Fast and slow variables],
    [The particle position contains a rapidly rotating vector $bold(rho)$ and
    a slowly evolving center $bold(R)$. Guiding-center theory does not erase
    the physics of the fast orbit. It replaces its detailed phase by averaged
    quantities such as $mu$, parallel momentum, and drift velocities.]
  )

  #summary[
    Guiding-center theory requires small orbit size and slow field variation.
    The decomposition $bold(r)=bold(R)+bold(rho)$ separates gyromotion from
    center motion, and $mu=m_alpha v_perp^2\/(2B)$ is conserved to leading
    order in $epsilon = rho_L\/L_B$: by the mirror force and energy
    conservation, by Faraday's law, and as the action of the gyration.
  ]

  #exam-prompts(
    (
      [(e) How are particle orbits approximated in a magnetized plasma and how is the particle motion decomposed and averaged in a not fully homogeneous plasma? What are the conditions that such an approximation is applicable?],
    ),
    [Plasma Physics Exam.pdf, p. 2],
  )

  #knowledge-check((
    (
      question: [What is the small parameter that compares a gyroradius with magnetic-field structure?],
      answer: [ $epsilon = rho_L\/L_B$. Guiding-center averaging requires this dimensionless ratio to be much smaller than one.],
    ),
    (
      question: [Which part of the orbit is averaged out in guiding-center theory?],
      answer: [The fast gyrophase dependence of $bold(rho)$ is averaged, while the guiding-center position and slow invariants are retained.],
    ),
    (
      question: [What happens to $mu$ if $B$ increases adiabatically while it remains invariant?],
      answer: [The perpendicular kinetic energy $m_alpha v_perp^2\/2 = mu B$ increases in proportion to $B$, so $v_perp$ increases as $sqrt(B)$.],
    ),
    (
      question: [Give one process that can break magnetic-moment conservation.],
      answer: [A field variation on the gyroradius or gyroperiod scale, a collision, a sharp boundary, or a resonant wave can change the gyrophase coherently.],
    ),
  ))

  #section-title[Nonuniform fields: grad-$B$, curvature, and mirrors] <motion-nonuniform-fields>

  #lead[
    A nonuniform magnetic field exerts an averaged force on the guiding center.
    How do field gradients and curved field lines turn the local circular orbit
    into a drift or a mirror reflection?
  ]

  #objectives((
    [derive the grad-$B$ drift from the magnetic-moment force],
    [identify the curvature drift as a response to parallel inertia],
    [explain magnetic-mirror reflection using the adiabatic invariant],
  ))

  #assumption(
    [Adiabatic guiding-center force],
    [Use the same $rho_L\/L_B << 1$ ordering and neglect rapid changes of $mu$.
    The magnetic-moment force is the effective guiding-center force]
  )

  $ bold(F)_mu = -mu grad(B) $ <motion-mu-force>

  #equation-note[
    $bold(F)_mu$ is in #unit("N") when $mu$ is in #unit("J/T") and
    $grad(B)$ in #unit("T/m"). Its component along $bold(b)$ is the mirror
    force, derived below from $div(bold(B)) = 0$; its perpendicular part
    drives the grad-$B$ drift.
  ]

  Because the field varies little across an orbit, the local perpendicular
  part of this force, $bold(F)_(mu,perp) = -mu grad_perp B$, can be inserted
  into the homogeneous-force drift:

  $ bold(v)_D^(grad B) = (bold(F)_(mu,perp) times bold(B))/(q_alpha B^2) = mu/q_alpha (bold(B) times grad(B))/(B^2) $ <motion-gradb-drift>

  #equation-note[
    The drift is perpendicular to both $bold(B)$ and the field
    gradient. Its direction changes with the sign of $q_alpha$.
  ]

  #animation(
    "../media/grad-b-drift.mp4",
    "An ion and an electron gyrate in a magnetic field out of the page whose strength grows upward. Each orbit is tighter where the field is stronger, so the guiding centres drift sideways, the ion and the electron in opposite directions. Lengths in ion Larmor radii and time in inverse ion gyrofrequencies, with unit [1].",
    caption: [
      Grad-$B$ drift from the full Lorentz force in $bold(B) = B_0 (1 + y\/L) bold(e)_z$
      with $L = 10 rho_(L i)$, reduced mass ratio $m_i\/m_e = 16$ and equal
      temperatures. The orbit curves more tightly where $B$ is stronger, so
      ion and electron drift along $x$ in opposite directions. The measured
      drift speeds agree with $mu abs(grad B)\/(abs(q_alpha) B)$ within
      $1.3$~% (ion) and $0.1$~% (electron). Lengths in $rho_(L i)$ and time
      $omega_(c i) t$, both [1].
    ],
    poster: "../media/grad-b-drift.png",
  )

  A curved field line also pushes the guiding center sideways. Let $R_c$ be
  the local radius of curvature in #unit("m") and $bold(e)_R$ the unit vector
  normal to the field line, pointing away from the centre of curvature. Along
  the line, $bold(b) = bold(B)\/B$ turns as

  $ (bold(b) dot grad) bold(b) = -bold(e)_R/R_c $ <motion-field-line-curvature>

  #equation-note[
    $(bold(b) dot grad) bold(b)$ is the rate of change of $bold(b)$ per unit
    length along the field line, in #unit("m^-1"). It points toward the
    centre of curvature.
  ]

  A guiding center streaming at $v_parallel$ along the curved line therefore
  has the centripetal acceleration
  $v_parallel^2 (bold(b) dot grad) bold(b) = -(v_parallel^2\/R_c) bold(e)_R$.
  The magnetic force must supply it. In the frame of the guiding center this
  appears as the centrifugal force

  $ bold(F)_"curv" = (m_alpha v_parallel^2)/R_c bold(e)_R $ <motion-curvature-force>

  #equation-note[
    The effective centrifugal force is in #unit("N") and points away from
    the centre of curvature.
  ]

  Applying the same force-drift map gives

  $ bold(v)_D^"curv" = (bold(F)_"curv" times bold(B))/(q_alpha B^2) = (m_alpha v_parallel^2)/(q_alpha B R_c) bold(e)_R times bold(b) $ <motion-curvature-drift>

  #equation-note[
    The curvature drift is in #unit("m/s"). The sign of $q_alpha$
    determines its direction, and it assumes the same adiabatic ordering as
    the grad-$B$ drift. With the signed $rho_parallel = v_parallel\/omega_c$
    and the angular frequency $Omega_parallel = v_parallel\/R_c$ at which the
    guiding center circles the centre of curvature,
    $bold(v)_D^"curv" = rho_parallel Omega_parallel bold(e)_R times bold(b)$.
  ]

  #details(
    [Derivation: curvature drift from the guiding-center acceleration],
    [#derivation-step[Curvature of a circular field line]
    Take a field line that is a circle of radius $R_c$ about the $z$ axis.
    With $R = sqrt(x^2 + y^2)$, its unit vectors are
    $bold(b) = (-y bold(e)_x + x bold(e)_y)\/R$ and
    $bold(e)_R = (x bold(e)_x + y bold(e)_y)\/R$. Differentiating $bold(b)$
    along itself gives

    $ (bold(b) dot grad) bold(b) = -(x bold(e)_x + y bold(e)_y)/R^2 = -bold(e)_R/R_c $

    on the line $R = R_c$. A smooth field line is locally such a circle.

    #derivation-step[Acceleration of the guiding center]
    The guiding center moves with $v_parallel bold(b)$, and $bold(b)$ changes
    along its path at the rate $v_parallel (bold(b) dot grad) bold(b)$. For
    constant $v_parallel$ in a static field,

    $ dv(,t) (v_parallel bold(b)) = v_parallel^2 (bold(b) dot grad) bold(b)
      = -v_parallel^2/R_c bold(e)_R . $

    #derivation-step[Insert the centrifugal force into the force drift]
    The force $bold(F)_"curv" = (m_alpha v_parallel^2\/R_c) bold(e)_R$ in
    $bold(v)_D = (bold(F) times bold(B))\/(q_alpha B^2)$ gives
    $bold(v)_D^"curv" = m_alpha v_parallel^2 (bold(e)_R times bold(b))\/(q_alpha B R_c)$.
    At $(R_c, 0, 0)$, $bold(e)_R = bold(e)_x$ and $bold(b) = bold(e)_y$, so
    $bold(e)_R times bold(b) = bold(e)_z$: ions drift along $+z$, electrons
    along $-z$.]
  )

  In a vacuum toroidal field, $B prop 1\/R$, so
  $grad B = -(B\/R_c) bold(e)_R$ and the grad-$B$ drift points the same way.
  The two drifts add to

  $ bold(v)_D^"curv" + bold(v)_D^(grad B) = m_alpha/(q_alpha B R_c) (v_parallel^2 + v_perp^2/2) bold(e)_R times bold(b) $ <motion-vacuum-drift>

  #equation-note[
    In #unit("m/s"). Both terms are vertical in a torus and opposite for ions
    and electrons, so they separate charge.
  ]

  #animation(
    "../media/curvature-drift.mp4",
    "Poloidal cross-section of a purely toroidal magnetic field that points out of the page and weakens with the major radius R. An ion and an electron gyrate; the ion guiding centre drifts upward and the electron guiding centre downward. Lengths in ion Larmor radii, with unit [1].",
    caption: [
      Curvature and grad-$B$ drift from the full Lorentz force in the vacuum
      toroidal field $B prop 1\/R$, seen in the poloidal plane. The ion
      drifts up and the electron down, a charge separation that a purely
      toroidal field cannot hold. The measured vertical drift speeds agree
      with $(m_alpha\/(q_alpha B R_c))(v_parallel^2 + v_perp^2\/2)$ within
      $1.6$~% (ion) and $0.4$~% (electron). Lengths in $rho_(L i)$ [1].
    ],
    poster: "../media/curvature-drift.png",
  )

  #details(
    [Derivation: grad- $B$ drift],
    [#derivation-step[Identify the magnetic-moment force]
    The guiding-center force from the adiabatic magnetic moment is

    $ bold(F)_mu=-mu grad(B) = -grad(mu B) , $

    with $mu$ held constant. Its part along $bold(b)$ is the mirror force;
    only the perpendicular part enters the drift.

    #derivation-step[Apply the general force-drift formula]
    A perpendicular homogeneous force drifts at

    $ bold(v)_D=(bold(F) times bold(B))/(q_alpha B^2) . $

    Substitute the magnetic-moment force and use

    $ -grad(B) times bold(B)=bold(B) times grad(B) . $

    The grad-$B$ drift is therefore

    $ bold(v)_D^(grad B)=mu/q_alpha (bold(B) times grad(B))/(B^2) . $

    Reversing $q_alpha$ while holding $bold(B)$ fixed checks the direction of the
    drift.]
  )

  #interpretation(
    [Magnetic mirrors],
    [If a particle moves into a region of increasing $B$ while $mu$ is
    approximately conserved, its perpendicular energy $mu B$ increases. With
    nearly constant total kinetic energy, parallel energy decreases. The
    parallel velocity can reach zero, after which the particle reverses and is
    reflected without a collision. The pitch angle determines whether the
    particle reaches the high-field region. The pitch angle is the angle
    between the velocity and the local magnetic field.]
  )

  Let $s$ measure distance along a field line. The magnetic-moment force has a
  parallel component

  $ m_alpha dv(v_parallel,t) = F_parallel = -mu pdv(B,s) $ <motion-mirror-force>

  #equation-note[
    The derivative $pdv(B,s, style: "horizontal")$ is taken along the field-line coordinate $s$.
    A positive field gradient therefore opposes motion into the stronger-field
    region. This is the one-dimensional mirror force in the adiabatic model.
  ]

  #details(
    [Derivation: mirror force from $div(bold(B)) = 0$],
    [#derivation-step[Radial field of a converging field]
    Take an axisymmetric field whose axial component $B_z (z)$ varies slowly
    along the axis, in cylinder coordinates $r$, $theta$, $z$ about the
    axis. Near the axis, $div(bold(B)) = 0$ reads
    $(1\/r) pdv(,r) (r B_r) = -pdv(B_z,z, style: "horizontal")$, so

    $ B_r = -r/2 pdv(B_z,z) . $

    Where the field lines converge, $B_r$ points toward the axis.

    #derivation-step[Average the axial Lorentz force over one turn]
    Put the orbit on the axis at $r = rho_L$. With $B_theta = 0$, the
    axial force is $q_alpha (bold(v) times bold(B))_z = -q_alpha v_theta B_r$.
    Ions circle $bold(B)$ left-handed, $v_theta = -v_perp$; electrons
    right-handed, $v_theta = +v_perp$. For both signs of the charge,

    $ q_alpha (bold(v) times bold(B))_z = abs(q_alpha) v_perp B_r
      = -(abs(q_alpha) v_perp rho_L)/2 pdv(B_z,z) , $

    the same at every gyrophase, so it is also the gyro-average.

    #derivation-step[Identify the magnetic moment]
    With $rho_L = m_alpha v_perp\/(abs(q_alpha) B)$,
    $abs(q_alpha) v_perp rho_L\/2 = m_alpha v_perp^2\/(2 B) = mu$. On the
    axis $B = B_z$ and $s = z$, which gives the mirror force
    $F_parallel = -mu pdv(B,s, style: "horizontal")$. The same average in a
    field whose strength varies across the orbit gives the perpendicular
    part, so that $bold(F)_mu = -mu grad(B)$.]
  )

  In a static magnetic field with no electrostatic potential, the effective
  parallel energy is

  $ K = (m_alpha v_parallel^2)/2 + mu B(s) = "const." $ <motion-mirror-energy>

  In this one-dimensional description, $mu B(s)$ acts as a potential for
  parallel motion, although it is physically the perpendicular kinetic
  energy. A particle reflects when this term grows to equal $K$, leaving
  no parallel kinetic energy. Particles with too little perpendicular
  energy reach the maximum field without reflecting; they form the loss cone.

  #details(
    [Derivation: mirror reflection and the loss cone],
    [#derivation-step[Show conservation of parallel plus magnetic energy]
    Along a field line, the chain rule gives

    $ dv(B(s(t)),t)=dv(s,t) pdv(B,s)
      =v_parallel pdv(B,s) . $

    The parallel kinetic energy therefore obeys

    $ dv((m_alpha v_parallel^2)/2,t)
      =m_alpha v_parallel dv(v_parallel,t)
      =-mu v_parallel pdv(B,s) . $

    If $dv(mu,t, style: "horizontal")=0$, the magnetic energy changes as

    $ dv(mu B,t)=mu v_parallel pdv(B,s) . $

    The two terms cancel, proving conservation of

    $ K=(m_alpha v_parallel^2)/2+mu B . $

    #derivation-step[Find the mirror point]
    At the initial point, use

    $ v_(perp,0)=v_0 sin theta.alt_0, quad
      v_(parallel,0)=v_0 cos theta.alt_0 . $

    At the mirror point $B_m$, $v_parallel$ is zero. Conservation of $K$
    and $mu$ gives

    $ mu B_m=(m_alpha v_0^2)/2, quad
      mu B_0=(m_alpha v_0^2 sin^2 theta.alt_0)/2 . $

    Hence

    $ B_m/B_0=1/(sin^2 theta.alt_0) . $

    If the largest available field is $B_"max"$, reflection occurs when

    $ sin^2 theta.alt_0 >= B_0/B_"max" . $

    The complementary range is the loss cone: particles with
    $sin^2 theta.alt_0 < B_0\/B_"max"$ pass through the mirror and escape.]
  )

  The boundary of the loss cone depends only on the mirror ratio
  $R_m = B_"max"\/B_0$:

  $ sin^2 theta.alt_c = 1/R_m $ <motion-loss-cone>

  #equation-note[
    $theta.alt_c$ is the loss-cone angle and $R_m$ is dimensionless. Particles
    with $theta.alt_0 < theta.alt_c$, or $theta.alt_0 > pi - theta.alt_c$ when moving the
    other way, leave through the mirror throat. The angle does not depend on
    the particle's speed, charge or mass.
  ]

  #animation(
    "../media/magnetic-mirror.mp4",
    "Six ions of equal speed start at the midplane of a magnetic mirror with pitch angles of 18, 26, 29, 31, 45 and 70 degrees. The three below 30 degrees pass through the throat and leave; the other three slow down where the field lines converge, turn around and bounce between the two mirror points. Positions in units of the mirror half-length L_m, with unit [1].",
    caption: [
      Six ions of equal speed in a mirror with $R_m = 4$, computed from the
      full Lorentz force. Ions with $sin^2 theta.alt_0 < 1\/R_m$, inside the
      $30 degree$ loss cone, leave through the throat; the others are
      reflected. $mu$ stays constant within $0.3$~% for the reflected and
      $1.6$~% for the escaping ions. Positions in units of the mirror
      half-length $L_m$ [1].
    ],
    poster: "../media/magnetic-mirror.png",
  )

  #motion-loss-cone

  #rechenbeispiel[
    A particle starts in a minimum field $B_0 = qty("0.0100", "T")$ and sees a
    maximum field $B_"max" = qty("0.0500", "T")$. Determine the critical pitch
    angle $theta.alt_c$ separating reflected particles from the loss cone.
    Here $0 <= theta.alt_0 <= pi\/2$ is the acute pitch angle to the direction of
    approach, in a static field with no electric work.

    Numerical result: $theta.alt_c = 26.6 degree$. Particles with
    $theta.alt_0 >= theta.alt_c$ reflect in this ideal adiabatic model.
  ]

  #interpretation(
    [Drift inventory],
    [The single-particle drifts developed here are the common $E times B$
    drift, the general homogeneous-force drift, the grad-$B$ drift, and the
    curvature drift. The first is species independent; the latter two reverse
    direction with charge sign. A mirror reflection is not itself a transverse
    drift: it is parallel slowing and reversal caused by the effective
    potential $mu B$.]
  )

  #summary[
    Gradients and curvature create effective guiding-center forces. The force
    drift turns $-mu grad(B)$ into grad- $B$ drift, while parallel inertia in a
    curved field produces curvature drift. Magnetic mirrors follow from
    conserving $mu$ while the field strength changes.
  ]

  #exam-prompts(
    (
      [(f) How is the magnetic moment $mu$ defined and how does the grad-B-drift follow from $F = -mu grad(B)$?],
      [(g) Draw and explain a magnetic mirror.],
      [(h) What is the curvature drift?],
      [(i) What drifts do you know in magnetized plasmas?],
    ),
    [Plasma Physics Exam.pdf, p. 2],
  )

  #knowledge-check((
    (
      question: [Why is the grad-$B$ drift charge-sign dependent while the $E times B$ drift is not?],
      answer: [The magnetic-moment force does not contain a factor of $q_alpha$, so the force-drift formula retains $1\/q_alpha$. The electric force contains $q_alpha$ and cancels it.],
    ),
    (
      question: [What energy conversion occurs as a mirrored particle approaches stronger $B$?],
      answer: [Perpendicular energy $mu B$ increases while parallel kinetic energy decreases if total energy is conserved.],
    ),
    (
      question: [What is the common geometric direction of grad- $B$ drift?],
      answer: [It is perpendicular to the local field and to $grad(B)$, with its sign set by the charge.],
    ),
    (
      question: [What approximation must be checked before classifying a drift with guiding-center theory?],
      answer: [The field and force must vary slowly across a gyroradius and a gyroperiod, so the relevant dimensionless ordering parameters must be small.],
    ),
  ))

  #section-title[Polarization drift in a slowly varying electric field] <motion-polarization>

  #lead[
    The $E times B$ drift is an instantaneous force balance. What happens
    when the perpendicular electric field changes slowly in time? The orbit
    center acquires an inertial correction so that its drift can follow the
    changing field.
  ]

  #objectives((
    [state the temporal ordering for the polarization-drift approximation],
    [separate the static $E times B$ drift from the inertial correction],
    [derive the polarization drift in a uniform magnetic field],
    [interpret the species-summed polarization current],
  ))

  #unit-ledger[
    The drive frequency $omega_"d"$ and $omega_c$ are in #unit("s^-1"). The
    ordering ratio $omega_"d"\/abs(omega_c)$ is normalized and therefore carries
    unit [1].
  ]

  #assumption(
    [Slowly varying perpendicular electric field],
    [Take a uniform, time-independent $bold(B)=B bold(b)$ and a spatially
    uniform perpendicular electric field whose characteristic drive
    frequency satisfies $omega_"d"\/abs(omega_c) << 1$. The field changes slowly
    compared with one gyroperiod, and the correction to the $E times B$ drift
    remains small.]
  )

  Extend the $E times B$ ansatz by a slow inertial correction to the drift:

  $ bold(v) = v_parallel bold(b) + bold(v)_D + bold(v)_D^"pol" + bold(v)_perp $ <motion-polarization-split>

  The leading force balance is the familiar common drift

  $ bold(v)_D = (bold(E)_perp times bold(B))/(B^2) $ <motion-polarization-exb>

  #equation-note[
    The leading drift is in #unit("m/s") and follows the
    instantaneous electric field. As in the guiding-center split,
    $bold(v)_perp$ is the rapidly rotating gyration velocity.
  ]

  The next-order orbit-center response is the polarization drift:

  $ bold(v)_D^"pol" = m_alpha/(q_alpha B^2) pdv(bold(E)_perp,t) $ <motion-polarization-drift>

  #equation-note[
    The factor $1\/q_alpha$ makes the polarization drift point in
    opposite directions for positive and negative charges. Unlike the
    $E times B$ drift, it depends on particle mass.
  ]

  #details(
    [Derivation: inertial correction to the $E times B$ drift],
    [#derivation-step[Separate the leading drift]
    Insert the split into the Lorentz force for a uniform magnetic field. As
    for the $E times B$ ansatz, the gyration obeys
    $m_alpha dv(bold(v)_perp,t, style: "horizontal") = q_alpha bold(v)_perp times bold(B)$
    and cancels, leaving for the perpendicular drifts

    $ m_alpha pdv(,t) (bold(v)_D + bold(v)_D^"pol") = q_alpha (bold(E)_perp+
      (bold(v)_D + bold(v)_D^"pol") times bold(B)) . $

    The $E times B$ drift is defined by

    $ bold(E)_perp+bold(v)_D times bold(B)=bold(0) . $

    Keeping the leading inertial term gives

    $ m_alpha pdv(bold(v)_D,t)=q_alpha (bold(v)_D^"pol" times bold(B)) . $

    #derivation-step[Invert the magnetic operator]
    Cross with $bold(B)$. Because the correction is perpendicular to the
    field,

    $ (bold(v)_D^"pol" times bold(B)) times bold(B)
      =-B^2 bold(v)_D^"pol" . $

    Thus

    $ bold(v)_D^"pol"=m_alpha/(q_alpha B^2)
      (bold(B) times pdv(bold(v)_D,t)) . $

    Since $bold(B)$ is constant,

    $ pdv(bold(v)_D,t)=
      (pdv(bold(E)_perp,t) times bold(B))/(B^2) . $

    Use $bold(B) times (bold(A) times bold(B))=B^2 bold(A)$ for
    $bold(A) dot bold(B)=0$. The correction is therefore

    $ bold(v)_D^"pol"=m_alpha/(q_alpha B^2) pdv(bold(E)_perp,t) . $

    #derivation-step[State the ordering]
    The discarded term $m_alpha pdv(bold(v)_D^"pol",t, style: "horizontal")$ is smaller by
    $omega_"d"\/abs(omega_c)$. The polarization drift is therefore valid when
    the electric field varies slowly compared with the gyrofrequency.]
  )

  Summing over species gives a polarization current density

  $ bold(j)_"pol" = sum_alpha n_alpha q_alpha bold(v)_(D,alpha)^"pol"
    = 1/(B^2) (sum_alpha n_alpha m_alpha)
      pdv(bold(E)_perp,t) $ <motion-polarization-current>

  #equation-note[
    The current density is in #unit("A/m^2") and $n_alpha$ is the density
    of species $alpha$ in #unit("m^-3"). The charge signs cancel in the species sum, so the mass
    density weights the polarization current; in an electron--ion plasma the
    ion contribution is usually larger.
  ]

  #animation(
    "../media/polarization-drift.mp4",
    "An ion and an electron gyrate in a uniform magnetic field while a perpendicular electric field is switched on smoothly over three ion gyroperiods. The view moves with the common E cross B displacement. In this view the ion guiding centre shifts along the electric field and the electron guiding centre shifts a sixteenth as far the other way. Lengths in ion Larmor radii and time in inverse ion gyrofrequencies, with unit [1].",
    caption: [
      Polarization drift, computed from the full Lorentz force while
      $bold(E)_perp$ rises smoothly to $E_1$ over three ion gyroperiods, with
      $E_1\/B = 0.75 v_perp$ of the ion and $m_i\/m_e = 16$. With the common
      $E times B$ displacement removed, the ion guiding center moves along
      $bold(E)$ by $m_i E_1\/(e B^2)$ and the electron 16 times less the
      other way, the time integral of $bold(v)_D^"pol"$. Lengths in
      $rho_(L i)$ and time $omega_(c i) t$, both [1].
    ],
    poster: "../media/polarization-drift.png",
  )

  #rechenbeispiel[
    Consider an electron in a uniform field $B=qty("0.0100", "T")$. Use
    $m_e=qty("9.109e-31", "kg")$, $q_e=-qty("1.602e-19", "C")$,
    and a perpendicular drive
    $bold(E)_perp (t)=qty("3.00e4", "V/m") cos(omega_"d" t) bold(e)_x$
    with $omega_"d"=qty("1.00e5", "s^-1")$. Evaluate the polarization-drift
    amplitude and the ordering ratio $omega_"d"\/abs(omega_(c e))$.

    Assumptions: uniform fields, collisionless motion, and the
    slowly varying-field approximation.

    Numerical result: $abs(v_(D,e)^"pol")=qty("171", "m/s")$ and
    #normalized-label[ $omega_"d"\/abs(omega_(c e))=qty("5.69e-5", "1")$].
  ]

  #interpretation(
    [Polarization is an inertial response],
    [The $E times B$ drift transports both species together, whereas the
    polarization drift separates their orbit centers when the electric field
    changes. A growing electric field therefore produces a current even though
    the leading $E times B$ drift carries no net current in a quasineutral
    pair of species. The approximation fails when the field varies on the
    gyrofrequency scale, where the full cyclotron response is needed.]
  )

  #summary[
    For $omega_"d" << abs(omega_c)$, a changing perpendicular electric field
    adds $bold(v)_D^"pol"=(m_alpha\/(q_alpha B^2)) pdv(bold(E)_perp,t, style: "horizontal")$ to the common
    $E times B$ drift. This correction is mass dependent and reverses with
    charge, so it contributes to the polarization current.
  ]

  #knowledge-check((
    (
      question: [Which ordering makes the polarization-drift expansion valid?],
      answer: [The electric-field drive must be slow compared with gyromotion:
      $omega_"d"\/abs(omega_c) << 1$, with a uniform field over the orbit and a
      small inertial correction.]
    ),
    (
      question: [Why does the polarization drift depend on mass while the $E times B$ drift does not?],
      answer: [The $E times B$ drift is an instantaneous electric--magnetic
      force balance. The polarization drift is the velocity needed to supply
      the inertia $m_alpha pdv(bold(v)_D,t, style: "horizontal")$, so its coefficient contains
      $m_alpha\/q_alpha$.]
    ),
    (
      question: [What is the direction of the electron polarization drift when $bold(E)_perp$ grows in the $bold(e)_x$ direction?],
      answer: [It points in the negative $bold(e)_x$ direction because the
      electron charge is negative, while the positive-ion response points in
      the positive $bold(e)_x$ direction.]
    ),
    (
      question: [What physical effect is missed if only the $E times B$ drift is retained?],
      answer: [The model misses the species-opposite inertial response and the
      associated polarization current generated by a time-varying electric
      field.]
    ),
  ))

  #section-title[Cyclotron resonance and circular polarization] <motion-cyclotron-resonance>

  #lead[
    The slow polarization approximation has a sharp boundary. How does a
    rotating electric field exchange energy with a particle when its rotation
    matches the particle's gyrofrequency? This matching condition is
    cyclotron resonance.
  ]

  #objectives((
    [represent perpendicular motion with circular complex amplitudes],
    [identify the circular polarization that couples to a given charge sign],
    [locate the cyclotron-resonance denominator],
    [state why an ideal collisionless resonance cannot predict unlimited physical energy],
  ))

  #unit-ledger[
    The angular frequency $omega$, signed gyrofrequency $omega_c=q_alpha B\/m_alpha$, and
    detuning are in #unit("s^-1"). The resonance condition
    $omega\/abs(omega_c)=1$ is normalized and carries unit [1].
  ]

  #assumption(
    [Uniform harmonic drive],
    [Use a uniform, static $bold(B)=B bold(e)_z$ and a small transverse field
    with time dependence $exp(-i omega t)$. Neglect collisions, field
    gradients, radiation reaction, and relativistic corrections. The physical
    field is the real part of the complex representation.]
  )

  #definition(
    [Circular complex amplitudes],
    [In the perpendicular plane define the clockwise combinations
    $v_"cw"=v_x+i v_y$ and $E_"cw"=E_x+i E_y$, and the counterclockwise
    combinations $v_"ccw"=v_x-i v_y$ and $E_"ccw"=E_x-i E_y$. For $q_alpha>0$,
    free gyromotion has $v_"cw"$ proportional to $exp(-i omega_c t)$, so the
    clockwise field is the resonant polarization.]
  )

  #governing-law(
    [Circular cyclotron response],
    [The perpendicular Lorentz equation becomes]
  )

  $ pdv(v_"cw",t) + i omega_c v_"cw" = (q_alpha/m_alpha) E_"cw" $ <motion-cyclotron-response>

  #equation-note[
    For a harmonic drive
    $E_"cw"=tilde(E)_"cw" exp(-i omega t)$, the response amplitude is

    $ tilde(v)_"cw"=(q_alpha tilde(E)_"cw")/(i m_alpha (omega_c-omega)) . $

    The denominator
    becomes small when the drive rotation matches the signed gyrofrequency.
  ]

  #details(
    [Derivation: the resonant circular response],
    [#derivation-step[Combine the transverse equations]
    With $bold(B)=B bold(e)_z$, the component equations are

    $ pdv(v_x,t)=(q_alpha/m_alpha) E_x+omega_c v_y, quad
      pdv(v_y,t)=(q_alpha/m_alpha) E_y-omega_c v_x . $

    Define $v_"cw"=v_x+i v_y$ and $E_"cw"=E_x+i E_y$. Adding $i$ times
    the second equation to the first gives

    $ pdv(v_"cw",t)+i omega_c v_"cw"=(q_alpha/m_alpha)E_"cw" . $

    #derivation-step[Insert a harmonic drive]
    Use

    $ E_"cw" (t)=tilde(E)_"cw" exp(-i omega t), quad
      v_"cw" (t)=tilde(v)_"cw" exp(-i omega t) . $

    The forced amplitude satisfies

    $ -i omega tilde(v)_"cw"+i omega_c tilde(v)_"cw"
      =(q_alpha/m_alpha) tilde(E)_"cw" , $

    so

    $ tilde(v)_"cw"=(q_alpha tilde(E)_"cw")/(i m_alpha (omega_c-omega)) . $

    The homogeneous solution is $v_("cw",0) exp(-i omega_c t)$. The forced
    response therefore resonates at $omega=omega_c$ for this polarization.

    #derivation-step[Reverse the circular polarization]
    With $v_"ccw"=v_x-i v_y$ and $E_"ccw"=E_x-i E_y$,

    $ pdv(v_"ccw",t)-i omega_c v_"ccw"=(q_alpha/m_alpha)E_"ccw" . $

    Its denominator is proportional to $omega+omega_c$. For positive drive
    frequency, one circular polarization resonates at $omega=abs(omega_c)$;
    the matching handedness is determined by the sign of $q_alpha$.]
  )

  A linearly polarized field is the sum of two counter-rotating circular
  fields. Only the component with the matching handedness resonates, while
  the other component remains off resonance. In a real plasma, collisions,
  finite pulse duration, spatial inhomogeneity, and nonlinear effects limit
  the energy transfer and broaden or shift the ideal resonance.

  #rechenbeispiel[
    In a uniform field $B=qty("0.0100", "T")$, determine the
    positive resonant angular frequencies for an electron and a proton. Use
    $e=qty("1.602e-19", "C")$,
    $m_e=qty("9.109e-31", "kg")$, and $m_i=qty("1.673e-27", "kg")$. For each species, identify the circular
    polarization that couples to the positive-frequency drive.

    Assumptions: collisionless, nonrelativistic, uniform magnetic field and
    ideal harmonic forcing.

    Numerical result: $omega_"res,e"=qty("1.76e9", "s^-1")$ and
    $omega_"res,i"=qty("9.58e5", "s^-1")$. The resonant polarization has the
    handedness of the species' free gyromotion.
  ]

  #interpretation(
    [Resonance is a model boundary],
    [When the drive frequency is much smaller than the gyrofrequency, the
    response can be expanded into the common $E times B$ drift and the small
    polarization correction. Near
    $omega=abs(omega_c)$, that ordering fails: the drive remains phase coherent
    with the orbit and transfers energy over many gyroperiods. A finite
    collision rate or a finite interaction time must then be included before
    predicting an amplitude or absorbed power.]
  )

  #summary[
    Circular decomposition exposes the cyclotron denominator. A positive
    frequency resonates with the circular polarization matching the free
    gyromotion, at $omega=abs(omega_c)$. The collisionless singularity marks the
    limit of the slow-drift approximation.
  ]

  #knowledge-check((
    (
      question: [Why is circular polarization useful for diagnosing cyclotron resonance?],
      answer: [It separates a rotating field into the two handednesses. Only
      the component rotating with the free gyromotion has the small resonant
      denominator.]
    ),
    (
      question: [How does changing the sign of $q_alpha$ affect the resonant polarization?],
      answer: [It reverses the signed gyrofrequency and therefore selects the
      opposite circular handedness for a positive-frequency drive; the
      positive resonance remains at $abs(omega_c)$.]
    ),
    (
      question: [What does the factor $1\/(omega_c-omega)$ predict as the drive approaches resonance?],
      answer: [The ideal forced-response amplitude grows as the detuning tends
      to zero. The divergence signals missing broadening or saturation physics,
      such as collisions, finite pulse duration, or nonlinear motion.]
    ),
    (
      question: [Why can a linearly polarized wave still heat a charged particle at cyclotron resonance?],
      answer: [A linear polarization is the sum of two circular components. The
      component with matching handedness supplies the resonant rotating force,
      while the opposite component is nonresonant.]
    ),
  ))

  #chapter-nav(
    previous: (href: "04-debye-shielding.html", title: [Debye shielding]),
    next: (href: "06-kinetic-theory.html", title: [Kinetic theory]),
  )
]
