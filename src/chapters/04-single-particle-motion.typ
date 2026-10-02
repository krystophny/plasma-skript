#import "../theme.typ": *
#import "../figures.typ": gyroradius-geometry
#import "@preview/physica:0.9.8": grad, pdv, dv

#let chapter = [
  #page-title(number: 4)[Single-particle motion] <single-particle-motion>

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

  $ m dv(bold(v),t) = q (bold(E) + bold(v) times bold(B)) $ <motion-lorentz-force>

  #equation-note[
    Multiplying each field term by $q$ gives its contribution
    to the force, in #unit("N"). Dividing the total force by $m$ gives the
    particle acceleration.
  ]

  The instantaneous power supplied by the fields is

  $ dv((m v^2)/2,t) = q bold(E) dot bold(v) $ <motion-energy>

  #equation-note[
    The kinetic energy is in #unit("J"). The magnetic term does no work
    because $bold(v) dot (bold(v) times bold(B)) = 0$.
  ]

  In a uniform magnetic field with $bold(E)=0$, choose
  $bold(B) = B bold(e)_z$. The perpendicular velocity components satisfy

  $ dv(v_x,t) = Omega v_y, quad dv(v_y,t) = -Omega v_x, quad Omega = (q B)/m $ <motion-cyclotron-components>

  #equation-note[
    $Omega$ is a signed angular frequency in $upright("s")^(-1)$. The
    parallel velocity is constant, so the full orbit is a helix unless
    $v_parallel = 0$.
  ]

  #details(
    [Derivation: circular motion and the gyroradius],
    [#derivation-step[Balance magnetic bending and inertia]
    The magnetic force is perpendicular to $bold(v)_perp$, so it supplies
    centripetal acceleration without changing $v_perp$. Equating magnitudes,

    $ (m v_perp^2)/rho=abs(q) v_perp B , $

    gives

    $ rho=(m v_perp)/(abs(q) B)=v_perp/omega_c, quad
      omega_c=(abs(q) B)/m . $

    #derivation-step[Integrate the component motion]
    Solving the perpendicular component equations gives, for the chosen
    coordinate orientation,

    $ v_x=v_perp cos(Omega t+delta), quad
      v_y=-v_perp sin(Omega t+delta) . $

    Integrating once gives a circle in the perpendicular plane plus a constant
    guiding-center position. Reversing $q$ reverses the sign of $Omega$ and
    therefore reverses the sense of rotation, while the radius is unchanged.]
  )

  The guiding center is the center of the circular orbit in the perpendicular
  plane. Its radius is $rho=v_perp/omega_c$, where $omega_c=abs(Omega)$ is
  the positive gyrofrequency. Thus a faster perpendicular particle has a
  larger orbit, while a stronger field bends the same particle more tightly.

  For species $s$, write the signed frequency as $Omega_s=(q_s B)/m_s$
  and its positive magnitude as $omega_(c,s)=abs(Omega_s)$. Both are angular
  frequencies in #unit("s^-1"). A thermal orbit estimate uses
  $v_(perp,s)=v_("th,s")=sqrt((2 k_B T_s)/m_s)$ in #unit("m/s"),
  giving $rho_s=v_("th,s")/omega_(c,s)$ in #unit("m").

  #gyroradius-geometry

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
    thermal speed, $v_(perp,s) = v_("th,s") = sqrt((2 k_B T_s)/m_s)$, for each
    species.

    Target: report $lambda_D$, $omega_(p,e)$, $rho_e$, and $rho_i$.

    Numerical result: $lambda_D = qty("6.9e-6", "m")$,
    $omega_(p,e) = qty("5.6e11", "s^-1")$,
    $rho_e = qty("3.1e-5", "m")$, and $rho_i = qty("1.3e-3", "m")$.
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
    thermal speed, $v_(perp,s) = v_("th,s") = sqrt((2 k_B T_s)/m_s)$, for each
    species.

    Target: report $lambda_D$, $omega_(p,e)$, $omega_(c,e)$,
    $omega_(c,i)$, $rho_e$, and $rho_i$.

    Numerical result: $k_B T_e approx qty("8.62", "keV")$,
    $lambda_D = qty("6.9e-5", "m")$,
    $omega_(p,e) = qty("5.6e11", "s^-1")$,
    $omega_(c,e) = qty("8.8e11", "s^-1")$,
    $omega_(c,i) = qty("4.8e8", "s^-1")$,
    $rho_e = qty("6.3e-5", "m")$, and
    $rho_i = qty("2.7e-3", "m")$. These are rough dimensional
    values for a hot confined plasma.
  ]

  #summary[
    The Lorentz force separates energy transfer by $bold(E)$ from magnetic
    bending. In a uniform $bold(B)$ field the perpendicular motion is circular
    with radius $rho = v_perp/omega_c$, while the parallel motion is uniform.
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
      answer: [Only $q bold(E)$ can do work. The magnetic force is perpendicular to the instantaneous velocity and has zero power.],
    ),
    (
      question: [How does the gyroradius scale with particle mass at fixed $v_perp$ and $B$?],
      answer: [It is proportional to $m$, because $rho = (m v_perp)/(abs(q)B)$.],
    ),
    (
      question: [What changes when the sign of $q$ changes in a uniform magnetic field?],
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
    [derive the drift velocity for a homogeneous force perpendicular to $bold(B)$],
    [specialize the result to the electric $E times B$ drift],
    [identify which particle properties cancel from the common drift],
  ))

  #unit-ledger[
    A drift ratio such as $v_D/v_perp$ is dimensionless only after both speeds
    use the same reference state.
  ]

  Resolve the electric field into components parallel and perpendicular to the
  magnetic field, with $bold(b) = bold(B)/B$:

  $ bold(E) = E_parallel bold(b) + bold(E)_perp, quad
    m dv(v_parallel,t) = q E_parallel $ <motion-electric-decomposition>

  #equation-note[
    $E_parallel$ is the scalar component along $bold(B)$. It accelerates a
    particle along the field. The perpendicular component participates in
    gyromotion and, when static and homogeneous, in the common $E times B$
    drift derived below.
  ]

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

  The force balance for a constant orbit-center velocity is

  $ bold(F) + q (bold(v)_D times bold(B)) = 0 $ <motion-force-balance>

  #equation-note[
    This is a vector force balance in #unit("N"). The drift has no
    acceleration because it describes the constant orbit-center translation.
  ]

  Crossing with $bold(B)$ and using $bold(F) dot bold(B)=0$ gives

  $ bold(v)_D = (bold(F) times bold(B))/(q B^2) $ <motion-general-drift>

  #equation-note[
    The result has velocity units, #unit("m/s"). It is valid for a homogeneous
    perpendicular force and a uniform magnetic field.
  ]

  For $bold(F)=q bold(E)$, the charge cancels:

  $ bold(v)_(E times B) = (bold(E) times bold(B))/(B^2) $ <motion-exb-drift>

  #equation-note[
    With $E$ in #unit("V/m") and $B$ in #unit("T"), $E/B$ is directly a
    speed in #unit("m/s"). The common $E times B$ drift is independent of species mass and charge sign.
  ]

  #details(
    [Derivation: the force drift as a cross product],
    [#derivation-step[Start from the orbit-center force balance]
    A constant drift velocity satisfies

    $ bold(F)+q (bold(v)_D times bold(B))=bold(0) . $

    The drift is perpendicular to $bold(B)$, so crossing the equation with
    $bold(B)$ uses

    $ (bold(v)_D times bold(B)) times bold(B)=-bold(v)_D B^2 . $

    #derivation-step[Solve for the drift]
    The cross-product equation becomes

    $ bold(v)_D=(bold(F) times bold(B))/(q B^2) . $

    For an electric force, $bold(F)=q bold(E)$, so both the charge magnitude
    and its sign cancel. Direct substitution into the original force balance
    checks the sign of the resulting $E times B$ drift.]
  )

  #animation(
    "../media/exb-drift.mp4",
    "A positive charge gyrates clockwise around a guiding center translating rightward. Position axes are x/L0 and y/L0 [1]. The electric field points upward and the magnetic field out of the page; the drift is E cross B.",
    caption: [
      Gyromotion plus the $E times B$ drift. With reference
      length $L_0$ and time $t_0$, the trajectory uses $Omega t_0=2$,
      $rho/L_0=0.65$, and $v_D t_0/L_0=0.55$, all dimensionless.
    ],
    poster: "../media/exb-drift.png",
  )

  #summary[
    A homogeneous perpendicular force produces a drift
    $bold(v)_D = (bold(F) times bold(B))/(q B^2)$. For an electric force the
    charge cancels, so all magnetized species share the same $E times B$ drift.
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
      answer: [The electric force is $q bold(E)$, and the $q$ cancels the $1/q$ in the general force-drift expression.],
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
    $omega_c^(-1)$ the characteristic gyration time in seconds; the gyroperiod
    is $(2 pi)/omega_c$. The ordering parameters $rho/L_B$ and
    $omega_"slow"/omega_c$ are dimensionless. The magnetic moment defined
    below is in #unit("J/T"), equivalently #unit("A m^2").
  ]

  #assumption(
    [Slowly varying fields],
    [Assume $rho/L_B << 1$, field variation during one gyroperiod is small,
    and the fields are smooth enough for a local orbit expansion. Collisions,
    wave-particle resonances, and abrupt boundaries can invalidate the
    averaging.
  ]
  )

  Write the particle position as

  $ bold(r)(t) = bold(R)(t) + bold(rho)(t), quad abs(bold(rho)) approx rho $ <motion-position-split>

  #equation-note[
    $bold(R)$ is the guiding-center position and
    $bold(rho)$ is the fast gyroradius vector. Both positions and $rho$ are in
    #unit("m").
  ]

  The velocity has the corresponding decomposition

  $ bold(v) = dv(bold(r),t)
    = dv(bold(R),t) + dv(bold(rho),t), quad
    bold(v) = bold(v)_parallel + bold(v)_perp $ <motion-velocity-split>

  #equation-note[
    Every velocity is in #unit("m/s"). The first equality
    follows from the position split; the second is the local decomposition
    relative to $bold(B)$. The guiding-center derivative includes parallel
    motion and slow drifts, so it is not generally identical to
    $bold(v)_parallel$.
  ]

  For perpendicular gyromotion, define the magnetic moment

  $ mu = (m v_perp^2)/(2 B) $ <motion-magnetic-moment>

  #equation-note[
    $mu$ is an energy divided by magnetic field, in #unit("J/T"). It is an
    adiabatic invariant under the stated slow-variation ordering: it remains
    approximately constant as the particle samples a slowly changing field.
    Here “adiabatic” refers to the separation of orbit and field-variation
    scales, not to thermodynamic heat exchange.
  ]

  #details(
    [Derivation: magnetic moment and adiabatic invariance],
    [For this energy argument, take a static magnetic configuration with no
    electric work at the retained order. Keep leading parallel motion along
    the field when evaluating the sampled change in $B$.

    #derivation-step[Compute the magnetic moment of one orbit]
    For one circular orbit, the gyroperiod and orbit area are

    $ T_"c"=(2 pi)/omega_c, quad S=pi rho^2 . $

    The magnitude of the orbit current is

    $ I_"gyro"=abs(q)/T_"c"=(abs(q) omega_c)/(2 pi) . $

    The magnetic dipole moment is current times area:

    $ mu=I_"gyro" S
      =(abs(q) omega_c rho^2)/2
      =(m v_perp^2)/(2 B) . $

    Here $mu$ is the positive scalar magnitude; the gyration produces a
    diamagnetic vector dipole.

    #derivation-step[Use the averaged mirror force]
    Let $s$ measure distance along a field line. The averaged mirror force is

    $ F_parallel=-mu pdv(B,s), quad
      m dv(v_parallel,t)=-mu pdv(B,s) . $

    Since $dv(s,t)=v_parallel$, the particle samples the field according to

    $ dv(B,t)=v_parallel pdv(B,s) . $

    Therefore the parallel kinetic energy changes as

    $ dv((m v_parallel^2)/2,t)
      =-mu v_parallel pdv(B,s) . $

    #derivation-step[Show adiabatic conservation]
    The magnetic part changes according to

    $ dv(mu B,t)=B dv(mu,t)+mu v_parallel pdv(B,s) . $

    Adding the two balances gives

    $ dv((m v_parallel^2)/2+mu B,t)=B dv(mu,t) . $

    In this static, leading-order guiding-center approximation, the total
    guiding-center energy is conserved, so $dv(mu,t) approx 0$. The ordering
    requires the field to vary little over one gyroperiod and one gyroradius.]
  )

  This static mirror argument transfers energy between parallel and
  perpendicular motion. In a slowly time-varying magnetic field, $mu$ can
  remain invariant while an induced electric field supplies energy: the
  increase of $mu B$ is then betatron acceleration, and total kinetic energy
  need not be conserved.

  #rechenbeispiel[
    A proton has $m_i=qty("1.673e-27", "kg")$ and charge
    $q_i=e=qty("1.602e-19", "C")$. Use an initial field
    $B_0=qty("0.0100", "T")$, a final field $B_1=qty("0.0400", "T")$, and
    $v_(perp,0)=qty("1.00e5", "m/s")$. Assume that the field changes
    adiabatically, $mu$ is conserved, and there is no electrostatic energy
    exchange.

    Target: report $v_(perp,1)$, $rho_0$, and $rho_1$.

    Numerical result: $v_(perp,1)=qty("2.00e5", "m/s")$,
    $rho_0=qty("0.104", "m")$, and $rho_1=qty("0.0522", "m")$.
  ]

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
    center motion, and $mu=(m v_perp^2)/(2B)$ is conserved approximately in the
    adiabatic regime.
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
      answer: [ $rho/L_B$. Guiding-center averaging requires this dimensionless ratio to be much smaller than one.],
    ),
    (
      question: [Which part of the orbit is averaged out in guiding-center theory?],
      answer: [The fast gyrophase dependence of $bold(rho)$ is averaged, while the guiding-center position and slow invariants are retained.],
    ),
    (
      question: [What happens to $mu$ if $B$ increases adiabatically while it remains invariant?],
      answer: [The perpendicular kinetic energy $(m v_perp^2)/2 = mu B$ increases in proportion to $B$, so $v_perp$ increases as $sqrt(B)$.],
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
    [Use the same $rho/L_B << 1$ ordering and neglect rapid changes of $mu$.
    The magnetic-moment force is the effective guiding-center force]
  )

  $ bold(F)_mu = -mu grad(B) $ <motion-mu-force>

  #equation-note[
    $bold(F)_mu$ is in #unit("N") when $mu$ is in #unit("J/T") and
    $grad(B)$ in #unit("T/m").
  ]

  Because the field varies little across an orbit, the local perpendicular
  part of this force can be inserted into the homogeneous-force drift:

  $ bold(v)_(grad B) = (bold(F)_mu times bold(B))/(q B^2) = (mu (bold(B) times grad(B)))/(q B^2) $ <motion-gradb-drift>

  #equation-note[
    The drift is perpendicular to both $bold(B)$ and the field
    gradient. Its direction changes with the sign of $q$.
  ]

  A curved field line produces a centrifugal response from parallel motion.
  Denote the local radius-of-curvature vector by $bold(R)_c$ and its magnitude
  by $R_c$. The effective centrifugal force is

  $ bold(F)_"curv" = -(m v_parallel^2 bold(R)_c)/(R_c^2) $ <motion-curvature-force>

  #equation-note[
    The effective centrifugal force is in #unit("N"). The vector
    convention for $bold(R)_c$ points from the particle toward the centre of
    curvature, so the minus sign points outward from that centre.
  ]

  Define the curvature vector $bold(kappa) = bold(R)_c/R_c^2$ and the field
  unit vector $bold(b) = bold(B)/B$. Applying the same force-drift map gives

  $ bold(v)_"curv" = (bold(F)_"curv" times bold(B))/(q B^2) = (m v_parallel^2)/(q B) (bold(b) times bold(kappa)) $ <motion-curvature-drift>

  #equation-note[
    The curvature drift is in #unit("m/s"). The sign of $q$
    determines its direction; the expression uses the stated convention for
    $bold(R)_c$ and assumes the same adiabatic ordering as the grad- $B$ drift.
  ]

  #details(
    [Derivation: grad- $B$ drift],
    [#derivation-step[Identify the magnetic-moment force]
    The guiding-center force from the adiabatic magnetic moment is

    $ bold(F)_mu=-mu grad(B) . $

    #derivation-step[Apply the general force-drift formula]
    A perpendicular homogeneous force drifts at

    $ bold(v)_D=(bold(F) times bold(B))/(q B^2) . $

    Substitute the magnetic-moment force and use

    $ -grad(B) times bold(B)=bold(B) times grad(B) . $

    The grad-$B$ drift is therefore

    $ bold(v)_(grad B)=(mu (bold(B) times grad(B)))/(q B^2) . $

    Reversing $q$ while holding $bold(B)$ fixed checks the direction of the
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

  $ m dv(v_parallel,t) = F_parallel = -mu pdv(B,s) $ <motion-mirror-force>

  #equation-note[
    The derivative $pdv(B,s)$ is taken along the field-line coordinate $s$.
    A positive field gradient therefore opposes motion into the stronger-field
    region. This is the one-dimensional mirror force in the adiabatic model.
  ]

  In a static magnetic field with no electrostatic potential, the effective
  parallel energy is

  $ K = (m v_parallel^2)/2 + mu B(s) = "const." $ <motion-mirror-energy>

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

    $ dv((m v_parallel^2)/2,t)
      =m v_parallel dv(v_parallel,t)
      =-mu v_parallel pdv(B,s) . $

    If $dv(mu,t)=0$, the magnetic energy changes as

    $ dv(mu B,t)=mu v_parallel pdv(B,s) . $

    The two terms cancel, proving conservation of

    $ K=(m v_parallel^2)/2+mu B . $

    #derivation-step[Find the mirror point]
    At the initial point, use

    $ v_(perp,0)=v_0 sin alpha_0, quad
      v_(parallel,0)=v_0 cos alpha_0 . $

    At the mirror point $B_m$, $v_parallel$ is zero. Conservation of $K$
    and $mu$ gives

    $ mu B_m=(m v_0^2)/2, quad
      mu B_0=(m v_0^2 sin^2 alpha_0)/2 . $

    Hence

    $ B_m/B_0=1/(sin^2 alpha_0) . $

    If the largest available field is $B_"max"$, reflection occurs when

    $ sin^2 alpha_0 >= B_0/B_"max" . $

    The complementary range is the loss cone: particles with
    $sin^2 alpha_0 < B_0/B_"max"$ pass through the mirror and escape.]
  )

  #rechenbeispiel[
    A particle starts in a minimum field $B_0 = qty("0.0100", "T")$ and sees a
    maximum field $B_"max" = qty("0.0500", "T")$. Determine the critical pitch
    angle $alpha_"c"$ separating reflected particles from the loss cone.
    Here $0 <= alpha_0 <= pi/2$ is the acute pitch angle to the direction of
    approach, in a static field with no electric work.

    Numerical result: $alpha_"c" = 26.6 degree$. Particles with
    $alpha_0 >= alpha_"c"$ reflect in this ideal adiabatic model.
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
      answer: [The magnetic-moment force does not contain a factor of $q$, so the force-drift formula retains $1/q$. The electric force contains $q$ and cancels it.],
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
    The drive frequency $omega_"d"$ and $Omega$ are in #unit("s^-1"). The
    ordering ratio $omega_"d"/abs(Omega)$ is normalized and therefore carries
    unit [1].
  ]

  #assumption(
    [Slowly varying perpendicular electric field],
    [Take a uniform, time-independent $bold(B)=B bold(b)$ and a spatially
    uniform perpendicular electric field whose characteristic drive
    frequency satisfies $omega_"d"/abs(Omega) << 1$. The field changes slowly
    compared with one gyroperiod, and the correction to the $E times B$ drift
    remains small.]
  )

  For the perpendicular motion, separate the leading drift from the fast
  gyromotion and its inertial correction:

  $ bold(v)_perp = bold(v)_(E times B) + bold(v)_"pol" + bold(v)_"gyro" $ <motion-polarization-split>

  The leading force balance is the familiar common drift

  $ bold(v)_(E times B) = (bold(E)_perp times bold(B))/(B^2) $ <motion-polarization-exb>

  #equation-note[
    The leading drift is in #unit("m/s") and follows the
    instantaneous electric field. The notation $bold(v)_"gyro"$ denotes the
    rapidly rotating residual motion.
  ]

  The next-order orbit-center response is the polarization drift:

  $ bold(v)_"pol" = m/(q B^2) pdv(bold(E)_perp,t) $ <motion-polarization-drift>

  #equation-note[
    The factor $1/q$ makes the polarization drift point in
    opposite directions for positive and negative charges. Unlike the
    $E times B$ drift, it depends on particle mass.
  ]

  #details(
    [Derivation: inertial correction to the $E times B$ drift],
    [#derivation-step[Separate the leading drift]
    For a uniform magnetic field, the perpendicular Lorentz equation is

    $ m pdv(bold(v)_perp,t)=q (bold(E)_perp+
      bold(v)_perp times bold(B)) . $

    Define $bold(v)_E=bold(v)_(E times B)$ by

    $ bold(E)_perp+bold(v)_E times bold(B)=bold(0) . $

    Write the remaining slow correction as $bold(delta v)$. Keeping the
    leading inertial term gives

    $ m pdv(bold(v)_E,t)=q (bold(delta v) times bold(B)) . $

    #derivation-step[Invert the magnetic operator]
    Cross with $bold(B)$. Because the correction is perpendicular to the
    field,

    $ (bold(delta v) times bold(B)) times bold(B)
      =-B^2 bold(delta v) . $

    Thus

    $ bold(delta v)=m/(q B^2)
      (bold(B) times pdv(bold(v)_E,t)) . $

    Since $bold(B)$ is constant,

    $ pdv(bold(v)_E,t)=
      (pdv(bold(E)_perp,t) times bold(B))/(B^2) . $

    Use $bold(B) times (bold(A) times bold(B))=B^2 bold(A)$ for
    $bold(A) dot bold(B)=0$. The correction is therefore

    $ bold(delta v)=m/(q B^2) pdv(bold(E)_perp,t) . $

    #derivation-step[State the ordering]
    The discarded term $m pdv(bold(delta v),t)$ is smaller by
    $omega_"d"/abs(Omega)$. The polarization drift is therefore valid when
    the electric field varies slowly compared with the gyrofrequency.]
  )

  Summing over species gives a polarization current density

  $ bold(j)_"pol" = sum_s n_(s,0) q_s bold(v)_"pol,s"
    = 1/(B^2) (sum_s n_(s,0) m_s)
      pdv(bold(E)_perp,t) $ <motion-polarization-current>

  #equation-note[
    The current density is in #unit("A/m^2"). The charge signs cancel in the species sum, so the mass
    density weights the polarization current; in an electron--ion plasma the
    ion contribution is usually larger.
  ]

  #rechenbeispiel[
    Consider an electron in a uniform field $B=qty("0.0100", "T")$. Use
    $m_e=qty("9.109e-31", "kg")$, $q_e=-qty("1.602e-19", "C")$,
    and a perpendicular drive
    $bold(E)_perp (t)=qty("3.00e4", "V/m") cos(omega_"d" t) bold(e)_x$
    with $omega_"d"=qty("1.00e5", "s^-1")$. Evaluate the polarization-drift
    amplitude and the ordering ratio $omega_"d"/abs(Omega_e)$.

    Assumptions: uniform fields, collisionless motion, and the
    slowly varying-field approximation.

    Numerical result: $abs(v_"pol,e")=qty("171", "m/s")$ and
    #normalized-label[ $omega_"d"/abs(Omega_e)=qty("5.69e-5", "1")$].
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
    For $omega_"d" << abs(Omega)$, a changing perpendicular electric field
    adds $bold(v)_"pol"=m/(q B^2) pdv(bold(E)_perp,t)$ to the common
    $E times B$ drift. This correction is mass dependent and reverses with
    charge, so it contributes to the polarization current.
  ]

  #knowledge-check((
    (
      question: [Which ordering makes the polarization-drift expansion valid?],
      answer: [The electric-field drive must be slow compared with gyromotion:
      $omega_"d"/abs(Omega) << 1$, with a uniform field over the orbit and a
      small inertial correction.]
    ),
    (
      question: [Why does the polarization drift depend on mass while the $E times B$ drift does not?],
      answer: [The $E times B$ drift is an instantaneous electric--magnetic
      force balance. The polarization drift is the velocity needed to supply
      the inertia $m pdv(bold(v)_(E times B),t)$, so its coefficient contains
      $m/q$.]
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
    The angular frequency $omega$, signed gyrofrequency $Omega=(q B)/m$, and
    detuning are in #unit("s^-1"). The resonance condition
    $omega/abs(Omega)=1$ is normalized and carries unit [1].
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
    combinations $v_"ccw"=v_x-i v_y$ and $E_"ccw"=E_x-i E_y$. For $q B>0$,
    free gyromotion has $v_"cw"$ proportional to $exp(-i Omega t)$, so the
    clockwise field is the resonant polarization.]
  )

  #governing-law(
    [Circular cyclotron response],
    [The perpendicular Lorentz equation becomes]
  )

  $ pdv(v_"cw",t) + i Omega v_"cw" = (q/m) E_"cw" $ <motion-cyclotron-response>

  #equation-note[
    For a harmonic drive
    $E_"cw"=tilde(E)_"cw" exp(-i omega t)$, the response amplitude is
    $tilde(v)_"cw"=(q tilde(E)_"cw")/(i m (Omega-omega))$. The denominator
    becomes small when the drive rotation matches the signed gyrofrequency.
  ]

  #details(
    [Derivation: the resonant circular response],
    [#derivation-step[Combine the transverse equations]
    With $bold(B)=B bold(e)_z$, the component equations are

    $ pdv(v_x,t)=(q/m) E_x+Omega v_y, quad
      pdv(v_y,t)=(q/m) E_y-Omega v_x . $

    Define $v_"cw"=v_x+i v_y$ and $E_"cw"=E_x+i E_y$. Adding $i$ times
    the second equation to the first gives

    $ pdv(v_"cw",t)+i Omega v_"cw"=(q/m)E_"cw" . $

    #derivation-step[Insert a harmonic drive]
    Use

    $ E_"cw" (t)=tilde(E)_"cw" exp(-i omega t), quad
      v_"cw" (t)=tilde(v)_"cw" exp(-i omega t) . $

    The forced amplitude satisfies

    $ -i omega tilde(v)_"cw"+i Omega tilde(v)_"cw"
      =(q/m) tilde(E)_"cw" , $

    so

    $ tilde(v)_"cw"=(q tilde(E)_"cw")/(i m (Omega-omega)) . $

    The homogeneous solution is $v_("cw",0) exp(-i Omega t)$. The forced
    response therefore resonates at $omega=Omega$ for this polarization.

    #derivation-step[Reverse the circular polarization]
    With $v_"ccw"=v_x-i v_y$ and $E_"ccw"=E_x-i E_y$,

    $ pdv(v_"ccw",t)-i Omega v_"ccw"=(q/m)E_"ccw" . $

    Its denominator is proportional to $omega+Omega$. For positive drive
    frequency, one circular polarization resonates at $omega=abs(Omega)$;
    the matching handedness is determined by the sign of $q B$.]
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
    $omega=abs(Omega)$, that ordering fails: the drive remains phase coherent
    with the orbit and transfers energy over many gyroperiods. A finite
    collision rate or a finite interaction time must then be included before
    predicting an amplitude or absorbed power.]
  )

  #summary[
    Circular decomposition exposes the cyclotron denominator. A positive
    frequency resonates with the circular polarization matching the free
    gyromotion, at $omega=abs(Omega)$. The collisionless singularity marks the
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
      question: [How does changing the sign of $q$ affect the resonant polarization?],
      answer: [It reverses the signed gyrofrequency and therefore selects the
      opposite circular handedness for a positive-frequency drive; the
      positive resonance remains at $abs(Omega)$.]
    ),
    (
      question: [What does the factor $1/(Omega-omega)$ predict as the drive approaches resonance?],
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
    previous: (href: "03-plasma-oscillations.html", title: [Plasma oscillations]),
    next: (href: "05-kinetic-theory.html", title: [Kinetic theory]),
  )
]
