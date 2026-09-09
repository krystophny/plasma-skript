#import "../theme.typ": *
#import "../figures.typ": gyroradius-geometry
#import "@preview/physica:0.9.8": grad, pdv, dv

#let chapter = [
  #page-title[2. Single-particle motion] <single-particle-motion>

  #lead[
    The single-particle model prescribes electromagnetic fields and follows
    one charged particle through them. It supplies the orbit geometry that
    guiding-center, kinetic, and fluid descriptions later average or close.
  ]

  #section-title[The Lorentz force and uniform-field gyromotion] <motion-lorentz>

  #lead[
    What can an electric or magnetic field do to a charged particle? The force
    decomposition answers this before any approximation is introduced.
  ]

  #objectives((
    [separate the energy-changing and trajectory-bending parts of the force],
    [derive the circular orbit in a uniform magnetic field],
    [use the charge sign to determine the sense of gyration],
  ))

  #unit-ledger[
    Gaussian CGS is active. The particle has mass $m$ in grams, charge $q$ in
    statcoulomb, velocity in #unit("cm/s"), electric field in statvolt per
    centimetre, magnetic field $B$ in gauss, and time in seconds. The magnetic
    part of the Lorentz force therefore carries $1/c$.
  ]

  #governing-law(
    [Lorentz force],
    [For prescribed fields, a particle obeys]
  )

  $ m dv(bold(v),t) = q (bold(E) + (bold(v) times bold(B)) / c) $ <motion-lorentz-force>

  #equation-note[
    Gaussian CGS. Both terms inside the parentheses are accelerative field
    contributions after multiplication by $q$. The force is in dynes.
  ]

  The instantaneous power supplied by the fields is

  $ dv((m v^2)/2,t) = q bold(E) dot bold(v) $ <motion-energy>

  #equation-note[
    Gaussian CGS. The kinetic energy is in erg. The magnetic term does no work
    because $bold(v) dot (bold(v) times bold(B)) = 0$.
  ]

  In a uniform magnetic field with $bold(E)=0$, choose
  $bold(B) = B bold(e)_z$. The perpendicular velocity components satisfy

  $ dv(v_x,t) = Omega v_y, quad dv(v_y,t) = -Omega v_x, quad Omega = (q B)/(m c) $ <motion-cyclotron-components>

  #equation-note[
    Gaussian CGS. $Omega$ is a signed angular frequency in $upright("s")^(-1)$. The
    parallel velocity is constant, so the full orbit is a helix unless
    $v_"parallel" = 0$.
  ]

  #details(
    [Derivation: circular motion and the gyroradius],
    [The magnetic force is perpendicular to $bold(v)_"perp"$, so it supplies the
    centripetal acceleration without changing $v_"perp"$. Equating magnitudes,
    $(m v_"perp"^2)/rho = (abs(q) v_"perp" B)/c$, gives
    $rho = (m c v_"perp")/(abs(q) B) = v_"perp"/omega_c$, where
    $omega_c = (abs(q)B)/(m c)$. Solving the component equations gives
    $v_x = v_"perp" cos(Omega t + delta)$ and
    $v_y = -v_"perp" sin(Omega t + delta)$ for this coordinate orientation.
    Integrating once gives a circle in the perpendicular plane plus a constant
    guiding-center position. Reversing $q$ reverses the sign of $Omega$ and
    therefore reverses the sense of rotation.]
  )

  #gyroradius-geometry

  #interpretation(
    [Energy versus orbit geometry],
    [An electric field can change the particle's kinetic energy because it can
    have a component along the velocity. A magnetic field can change the
    direction of the velocity but not its speed in this single-particle model.
    This distinction remains useful when fields are later solved
    self-consistently.]
  )

  #summary[
    The Lorentz force separates energy transfer by $bold(E)$ from magnetic
    bending. In a uniform $bold(B)$ field the perpendicular motion is circular
    with radius $rho = v_"perp"/omega_c$, while the parallel motion is uniform.
  ]

  #exam-prompts(
    (
      [(a) What are the main differences between the electric and magnetic force acting on a charged particle? How does a background magnetic field $B$ change the effect of an electric field on particle orbits if it is parallel or perpendicular to $B$?],
      [(b) Compute the gyroradius by balancing centrifugal force and Lorentz force. Draw the direction of the gyration for ions/electrons if the $B$ field points inside the paper plane.],
    ),
    [Plasma Physics Exam.pdf, p. 2],
  )

  #knowledge-check((
    (
      question: [Which part of the Lorentz force changes a particle's kinetic energy?],
      answer: [Only $q bold(E)$ can do work. The magnetic force is perpendicular to the instantaneous velocity and has zero power.],
    ),
    (
      question: [How does the gyroradius scale with particle mass at fixed $v_"perp"$ and $B$?],
      answer: [It is proportional to $m$, because $rho = (m c v_"perp")/(abs(q)B)$ in Gaussian CGS.],
    ),
    (
      question: [What changes when the sign of $q$ changes in a uniform magnetic field?],
      answer: [The signed gyrofrequency and the sense of rotation change. The gyroradius magnitude and kinetic energy do not.],
    ),
    (
      question: [What limiting orbit results when $v_"perp"$ tends to zero?],
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
    Gaussian CGS is active. The homogeneous force $bold(F)$ is in dynes,
    $bold(B)$ in gauss, $q$ in statcoulomb, and drift velocity in
    #unit("cm/s"). A drift ratio such as $v_D/v_"perp"$ is dimensionless
    only after both speeds use the same reference state.
  ]

  Resolve the electric field into components parallel and perpendicular to the
  magnetic field, with $bold(b) = bold(B)/B$:

  $ bold(E) = E_"parallel" bold(b) + bold(E)_"perp", quad
    m dv(v_"parallel",t) = q E_"parallel" $ <motion-electric-decomposition>

  #equation-note[
    $E_"parallel"$ is the scalar component along $bold(B)$. It accelerates a
    particle along the field. The perpendicular component participates in
    gyromotion and, when static and homogeneous, in the common $E times B$
    drift derived below.
  ]

  #assumption(
    [Uniform crossed-field ordering],
    [Take uniform, time-independent $bold(B)$ and a constant force with
    $bold(F) dot bold(B) = 0$. The force may be an electric force, pressure
    force, gravity-like force, or another prescribed homogeneous force. The
    drift is the slow orbit-center velocity after the fast gyromotion is
    averaged.
  ]
  )

  The force balance for a constant orbit-center velocity is

  $ bold(F) + (q/c) (bold(v)_D times bold(B)) = 0 $ <motion-force-balance>

  #equation-note[
    Gaussian CGS. This is a vector force balance in dynes. The drift has no
    acceleration because it describes the constant orbit-center translation.
  ]

  Crossing with $bold(B)$ and using $bold(F) dot bold(B)=0$ gives

  $ bold(v)_D = (c (bold(F) times bold(B)))/(q B^2) $ <motion-general-drift>

  #equation-note[
    Gaussian CGS. The result has velocity units. It is valid for a homogeneous
    perpendicular force and a uniform magnetic field.
  ]

  For $bold(F)=q bold(E)$, the charge cancels:

  $ bold(v)_(E times B) = (c (bold(E) times bold(B)))/(B^2) $ <motion-exb-drift>

  #equation-note[
    Gaussian CGS. The factor $c$ is required in this electromagnetic convention.
    The common $E times B$ drift is independent of species mass and charge sign.
  ]

  #details(
    [Derivation: why the force drift is a cross product],
    [Start from $bold(F) + (q/c) (bold(v)_D times bold(B))=0$. Cross the equation
    with $bold(B)$ and use
    $(bold(v)_D times bold(B)) times bold(B) = -bold(v)_D B^2$ because the
    drift is perpendicular to $bold(B)$. This yields
    $bold(v)_D = (c (bold(F) times bold(B)))/(q B^2)$. Substitution of
    $bold(F)=q bold(E)$ removes both the charge magnitude and its sign. A
    direct substitution into the original force balance is the sign check.]
  )

  #animation(
    "../media/exb-drift.mp4",
    "A positive charge follows a circular orbit while its guiding center translates to the right. The axes are normalized by the reference gyroradius. The electric field points upward, the magnetic field points out of the page, and the orbit-center translation is labelled E cross B drift.",
    caption: [
      Gyromotion plus the Gaussian-CGS $E times B$ drift. The trajectory is a
      deterministic normalized illustration, not measured data.
    ],
    poster: "../media/exb-drift.png",
  )

  #summary[
    A homogeneous perpendicular force produces a drift
    $bold(v)_D = (c (bold(F) times bold(B)))/(q B^2)$. For an electric force the
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
    orbit? The guiding-center approximation answers by separating fast and
    slow scales.
  ]

  #objectives((
    [state the scale ordering behind guiding-center motion],
    [decompose position and velocity into guiding-center and gyromotion parts],
    [define the magnetic moment and identify its adiabatic character],
  ))

  #unit-ledger[
    Gaussian CGS is active. Let $L_B$ denote the magnetic-field variation
    length in cm and $omega_c^(-1)$ the gyroperiod in seconds. The ordering
    parameters $rho/L_B$ and $omega_"slow"/omega_c$ are dimensionless.
    Magnetic moment is defined below in the corresponding Gaussian-CGS
    energy-per-field convention.
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
    Gaussian CGS geometry. $bold(R)$ is the guiding-center position and
    $bold(rho)$ is the fast gyroradius vector. Both positions and $rho$ are in
    cm.
  ]

  The velocity has the corresponding decomposition

  $ bold(v) = dv(bold(r),t)
    = dv(bold(R),t) + dv(bold(rho),t), quad
    bold(v) = bold(v)_"parallel" + bold(v)_"perp" $ <motion-velocity-split>

  #equation-note[
    Gaussian CGS. Every velocity is in #unit("cm/s"). The first equality
    follows from the position split; the second is the local decomposition
    relative to $bold(B)$. The guiding-center derivative includes parallel
    motion and slow drifts, so it is not generally identical to
    $bold(v)_"parallel"$.
  ]

  For perpendicular gyromotion, define the magnetic moment

  $ mu = (m v_"perp"^2)/(2 B) $ <motion-magnetic-moment>

  #equation-note[
    Gaussian CGS. $mu$ is an energy divided by magnetic field. It is an
    adiabatic invariant under the stated slow-variation ordering.
  ]

  #details(
    [Derivation: magnetic moment and adiabatic invariance],
    [For one circular orbit, the gyroperiod and orbit area are
    $T_"c" = 2 pi/omega_c$ and $S = pi rho^2$. The magnitude of the orbit
    current is $I_"gyro" = abs(q)/T_"c" = abs(q) omega_c/(2 pi)$. In
    Gaussian CGS the magnetic dipole moment is current times area divided by
    $c$, so
    $mu = (I_"gyro" S)/c
      = (abs(q) omega_c rho^2)/(2 c)
      = (m v_"perp"^2)/(2 B)$,
    after using $omega_c = abs(q) B/(m c)$ and
    $rho = (m c v_"perp")/(abs(q) B)$. The vector dipole generated by the
    gyration is diamagnetic; $mu$ here denotes its positive scalar magnitude.

    To see the adiabatic invariant, let $s$ measure distance along a field
    line. The averaged mirror force is
    $F_"parallel" = -mu pdv(B,s)$, so
    $m dv(v_"parallel",t) = -mu pdv(B,s)$.
    Since $dv(s,t)=v_"parallel"$, the field seen by the particle changes as
    $dv(B,t)=v_"parallel" pdv(B,s)$. Thus the parallel kinetic energy obeys
    $dv((m v_"parallel"^2)/2,t)
      = -mu v_"parallel" pdv(B,s)$, while
    $dv(mu B,t)=B dv(mu,t)+mu v_"parallel" pdv(B,s)$. Adding them gives
    $dv((m v_"parallel"^2)/2+mu B,t)=B dv(mu,t)$. The leading-order
    energy balance therefore gives $dv(mu,t) approx 0$ when the field varies
    slowly over a gyroperiod and a gyroradius.]
  )

  #rechenbeispiel[
    A proton has $m_i=qty("1.673e-24", "g")$ and charge
    $q_i=e=qty("4.803e-10", "statcoulomb")$. Use
    $c=qty("2.998e10", "cm/s")$, an initial field
    $B_0=qty("100", "G")$, a final field $B_1=qty("400", "G")$, and
    $v_(perp,0)=qty("1.00e7", "cm/s")$. Assume that the field changes
    adiabatically, $mu$ is conserved, and there is no electrostatic energy
    exchange.

    Target: report $v_(perp,1)$, $rho_0$, and $rho_1$.

    Numerical result: $v_(perp,1)=qty("2.00e7", "cm/s")$,
    $rho_0=qty("10.4", "cm")$, and $rho_1=qty("5.22", "cm")$.
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
    center motion, and $mu=(m v_"perp"^2)/(2B)$ is conserved approximately in the
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
      answer: [$rho/L_B$. Guiding-center averaging requires this dimensionless ratio to be much smaller than one.],
    ),
    (
      question: [Which part of the orbit is averaged out in guiding-center theory?],
      answer: [The fast gyrophase dependence of $bold(rho)$ is averaged, while the guiding-center position and slow invariants are retained.],
    ),
    (
      question: [What happens to $mu$ if $B$ increases adiabatically while it remains invariant?],
      answer: [The perpendicular kinetic energy $(m v_"perp"^2)/2 = mu B$ increases in proportion to $B$, so $v_"perp"$ increases as $sqrt(B)$.],
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

  #unit-ledger[
    Gaussian CGS is active. $grad B$ has gauss per centimetre, the effective
    force is in dynes, and all drift velocities are in #unit("cm/s").
    The symbols $mu$, $m$, $q$, $B$, and $c$ use the definitions of the prior
    section.
  ]

  #assumption(
    [Adiabatic guiding-center force],
    [Use the same $rho/L_B << 1$ ordering and neglect rapid changes of $mu$.
    The magnetic-moment force is the effective guiding-center force]
  )

  $ bold(F)_mu = -mu grad B $ <motion-mu-force>

  #equation-note[
    Gaussian CGS. $bold(F)_mu$ is in dynes when $mu$ is in energy per gauss and
    $grad B$ in gauss per centimetre.
  ]

  Inserting this force into the homogeneous-force drift gives

  $ bold(v)_(grad B) = (c (bold(F)_mu times bold(B)))/(q B^2) = (c mu (bold(B) times grad B))/(q B^2) $ <motion-gradb-drift>

  #equation-note[
    Gaussian CGS. The drift is perpendicular to both $bold(B)$ and the field
    gradient. Its direction changes with the sign of $q$.
  ]

  A curved field line produces a centrifugal response from parallel motion.
  Denote the local radius-of-curvature vector by $bold(R)_c$ and its magnitude
  by $R_c$. The effective centrifugal force is

  $ bold(F)_"curv" = -(m v_"parallel"^2 bold(R)_c)/(R_c^2) $ <motion-curvature-force>

  #equation-note[
    Gaussian CGS. The effective centrifugal force is in dynes. The vector
    convention for $bold(R)_c$ points from the particle toward the centre of
    curvature, so the minus sign points outward from that centre.
  ]

  Define the curvature vector $bold(kappa) = bold(R)_c/R_c^2$ and the field
  unit vector $bold(b) = bold(B)/B$. Applying the same force-drift map gives

  $ bold(v)_"curv" = (c (bold(F)_"curv" times bold(B)))/(q B^2) = (c m v_"parallel"^2)/(q B) (bold(b) times bold(kappa)) $ <motion-curvature-drift>

  #equation-note[
    Gaussian CGS. The curvature drift is in #unit("cm/s"). The sign of $q$
    determines its direction; the expression uses the stated convention for
    $bold(R)_c$ and assumes the same adiabatic ordering as the grad-$B$ drift.
  ]

  #details(
    [Derivation: grad-$B$ drift],
    [The guiding-center force from the adiabatic magnetic moment is
    $bold(F)_mu=-mu grad B$. A perpendicular homogeneous force drifts at
    $bold(v)_D=(c (bold(F) times bold(B)))/(q B^2)$. Substitute the magnetic-moment
    force and use $-grad B times bold(B)=bold(B) times grad B$ to obtain
    $bold(v)_(grad B)=(c mu (bold(B) times grad B))/(q B^2)$. The sign check follows
    from reversing $q$ while holding $bold(B)$ fixed.]
  )

  #interpretation(
    [Magnetic mirrors],
    [If a particle moves into a region of increasing $B$ while $mu$ is
    approximately conserved, its perpendicular energy $mu B$ increases. With
    nearly constant total kinetic energy, parallel energy decreases. The
    parallel velocity can reach zero, after which the particle reverses and is
    reflected without a collision. The pitch angle determines whether the
    particle reaches the high-field region.]
  )

  Let $s$ measure distance along a field line. The magnetic-moment force has a
  parallel component

  $ m dv(v_"parallel",t) = F_"parallel" = -mu pdv(B,s) $ <motion-mirror-force>

  #equation-note[
    The derivative $pdv(B,s)$ is taken along the field-line coordinate $s$.
    A positive field gradient therefore opposes motion into the stronger-field
    region. This is the one-dimensional mirror force in the adiabatic model.
  ]

  In a static magnetic field with no electrostatic potential, the effective
  parallel energy is

  $ K = (m v_"parallel"^2)/2 + mu B(s) = "const." $ <motion-mirror-energy>

  #details(
    [Derivation: mirror reflection and the loss cone],
    [Using the mirror force and the chain rule along the field line,
    $dv(B(s(t)),t) = dv(s,t) pdv(B,s)
      = v_"parallel" pdv(B,s)$. Therefore
    $dv((m v_"parallel"^2)/2,t)
      = m v_"parallel" dv(v_"parallel",t)
      = -mu v_"parallel" pdv(B,s)$, while
    $dv(mu B,t)=mu v_"parallel" pdv(B,s)$ when $dv(mu,t)=0$.
    The two terms cancel, proving that
    $K=(m v_"parallel"^2)/2+mu B$ is conserved.

    At an initial point with field $B_0$, speed $v_0$, and pitch angle
    $alpha_0$, use
    $v_"perp",0 = v_0 sin alpha_0$ and
    $v_"parallel",0 = v_0 cos alpha_0$. At the mirror point $B_m$, the
    parallel speed is zero. Conservation of $K$ and $mu$ gives
    $mu B_m = (m v_0^2)/2$ and
    $mu B_0 = (m v_0^2 sin^2 alpha_0)/2$, hence
    $B_m/B_0 = 1/(sin^2 alpha_0)$. If the largest field available is
    $B_"max"$, reflection occurs when
    $sin^2 alpha_0 >= B_0/B_"max"$. The complementary range is the loss
    cone: particles with $sin^2 alpha_0 < B_0/B_"max"$ pass through the
    mirror and escape.]
  )

  #rechenbeispiel[
    A particle starts in a minimum field $B_0 = qty("100", "G")$ and sees a
    maximum field $B_"max" = qty("500", "G")$. Determine the critical pitch
    angle $alpha_"c"$ separating reflected particles from the loss cone.

    Numerical result: $alpha_"c" = 26.6 degree$. Particles with
    $alpha_0 >= alpha_"c"$ reflect in this ideal adiabatic model.
  ]

  #interpretation(
    [A compact drift inventory],
    [The single-particle drifts developed here are the common $E times B$
    drift, the general homogeneous-force drift, the grad-$B$ drift, and the
    curvature drift. The first is species independent; the latter two reverse
    direction with charge sign. A mirror reflection is not itself a transverse
    drift: it is parallel slowing and reversal caused by the effective
    potential $mu B$.]
  )

  #summary[
    Gradients and curvature create effective guiding-center forces. The force
    drift turns $-mu grad B$ into grad-$B$ drift, while parallel inertia in a
    curved field produces curvature drift. Magnetic mirrors follow from
    conserving $mu$ while the field strength changes.
  ]

  #exam-prompts(
    (
      [(f) How is the magnetic moment $mu$ defined and how does the grad-B-drift follow from $F = -mu grad B$?],
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
      question: [What is the common geometric direction of grad-$B$ drift?],
      answer: [It is perpendicular to the local field and to $grad B$, with its sign set by the charge.],
    ),
    (
      question: [What approximation must be checked before classifying a drift with guiding-center theory?],
      answer: [The field and force must vary slowly across a gyroradius and a gyroperiod, so the relevant dimensionless ordering parameters must be small.],
    ),
  ))

  #chapter-nav(
    previous: (href: "01-introduction.html", title: [Introduction]),
    next: (href: "03-kinetic-theory.html", title: [Kinetic theory]),
  )
]
