#import "../theme.typ": animation, callout, lead, page-title, section-title

#let chapter = [
  #page-title[Charged-particle motion] <orbits-heading>

  #lead[
    A single charged particle already contains the central geometry of plasma
    physics: electric fields change the particle's energy, while magnetic fields
    bend its path.
  ]

  Plasma is a collection of charged particles whose motion is coupled through
  electromagnetic fields. The first model keeps one particle and prescribed
  fields. It gives us a reference orbit before collective effects are added.

  #section-title[The Lorentz force]

  Let a particle have mass $m$, charge $q$, position $bold(r)(t)$, and velocity
  $bold(v)(t)$. Its equation of motion is

  $ m d bold(v) / d t = q (bold(E) + bold(v) times bold(B)) $ <lorentz-force>

  The electric term is parallel to $bold(E)$ and can change the kinetic energy.
  The magnetic term is perpendicular to the instantaneous velocity because
  $bold(v) dot (bold(v) times bold(B)) = 0$. A uniform magnetic field therefore
  bends the orbit without doing work.

  #callout(
    [Reading the orbit],
    [The fast circular motion is gyromotion. The slow translation of its center
    is the guiding-center motion. Keeping those time scales separate is the
    starting point for reduced plasma models.],
  )

  #section-title[Crossed fields]

  Consider uniform fields with $bold(E) dot bold(B) = 0$. The guiding-center
  drift that is shared by positive and negative charges is

  $ bold(v)_(E times B) = (bold(E) times bold(B)) / B^2 $ <exb-drift>

  Its direction is fixed by the cross product. Its magnitude is independent of
  the particle mass and charge. The animation uses a positive charge, with
  $bold(E)$ upward and $bold(B)$ out of the page, so the drift points to the
  right.

  #animation(
    "../media/exb-drift.mp4",
    [A positive charge circles around a guiding center while the crossed fields
    translate that center in the $bold(E) times bold(B)$ direction. The axes are
    normalized by a reference gyroradius $rho$.],
  )

  #section-title[A first validity boundary]

  The single-particle picture is useful when the fields are specified or vary
  slowly across one orbit. It stops describing the experiment when the fields
  must be computed from the particles themselves, when collisions dominate, or
  when the orbit scale is comparable to the system size. Those cases lead to
  fluid, kinetic, or fully electromagnetic models.

  #callout(
    [Checkpoint],
    [For a uniform magnetic field, identify which term in the Lorentz force
    changes the particle's energy. Then use the right-hand rule to predict the
    direction of $bold(E) times bold(B)$ drift when $bold(E)$ points upward and
    $bold(B)$ points into the page.],
  )
]
