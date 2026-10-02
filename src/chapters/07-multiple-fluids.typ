#import "../theme.typ": *
#import "../figures.typ": multiple-fluid-hierarchy
#import "@preview/physica:0.9.8": div, grad, pdv, curl
#import "@preview/unify:0.8.1": qty, unit

#let chapter = [
  #page-title(number: 7)[Multiple-fluid theory of plasmas] <multiple-fluids>

  #lead[
    A plasma can contain several interpenetrating fluids at the same position.
    Electrons and ions feel the same fields but have different masses, charges,
    temperatures, and collision rates. Keeping their equations separate makes
    those differences explicit before a one-fluid approximation is chosen.
  ]

  #callout(
    [The species-resolved model],
    [A multiple-fluid model is obtained by taking moments of one kinetic
    equation for each species. The electric and magnetic fields couple the
    species, while pressure and collision terms can remain species-specific.
    Summing the species equations gives total-fluid balances, but further
    assumptions are needed to close a one-fluid model. Quasi-neutrality alone
    does not supply those assumptions.]
  )

  #section-title[Species-resolved plasma variables] <multiple-definitions>

  #lead[
    When is one bulk velocity insufficient? It is insufficient whenever
    electrons and ions carry different momentum or respond differently to a
    force. The first step is therefore to define one set of fluid variables
    for each species.
  ]

  #objectives((
    [define the species variables needed by a two-fluid model],
    [distinguish quasi-neutrality from equality of species velocities],
    [identify the common electromagnetic coupling and species-specific terms],
    [trace the information retained when kinetic distributions become fluids],
  ))

  #definition(
    [Hydrogen two-fluid variables],
    [Use $s in {e, i}$ for electrons and singly charged ions. Their charges
    are $q_(e)=-e$ and $q_(i)=+e$, with masses
    $m_(e)=qty("9.109e-31", "kg")$ and
    $m_(i)=qty("1.673e-27", "kg")$. For each species, $n_(s)$ is number
    density, $bold(u)_(s)$ is mean velocity, $bold(P)_(s)$ is the pressure
    tensor, and $bold(R)_(s)$ is the collisional momentum source.]
  )

  The species moments from the kinetic description are

  $ rho_(s) = m_(s) n_(s), quad
    rho_q = sum_s q_(s) n_(s), quad
    bold(j) = sum_s q_(s) n_(s) bold(u)_(s) $ <multiple-species-moments>

  #equation-note[
    The mass density $rho_(s)$ is in #unit("kg/m^3"), charge density $rho_q$
    is in #unit("C/m^3"), and $bold(j)$ is the total current density in
    #unit("A/m^2"). The charge $e$ is measured in #unit("C"). In a quasi-neutral
    hydrogen plasma, $n_(e) approx n_(i)$, but generally
    $bold(u)_(e) != bold(u)_(i)$; the difference is precisely what permits a
    current.
  ]

  #details(
    [Derivation: species moments retain separate fluids],
    [#derivation-step[Take moments species by species]
    Begin with a distribution $f_(s)(t,bold(r),bold(v))$ for every species.
    Its zeroth and first velocity moments are

    $ n_(s)=integral f_(s) dif^3 bold(v), quad
      n_(s) bold(u)_(s)=integral bold(v) f_(s) dif^3 bold(v) . $

    Multiplication by $m_(s)$ or $q_(s)$ gives the species mass and current
    contributions.

    #derivation-step[Form total variables only after the species moments]
    Because the moments are taken before summing over $s$, electron and ion
    velocities remain independent fields. Only after those fields have been
    defined may one form

    $ rho=sum_s rho_(s), quad
      bold(j)=sum_s q_(s)n_(s)bold(u)_(s) . $

    A mass-weighted bulk velocity is another derived quantity.

    #derivation-step[Separate quasi-neutrality from current]
    Quasi-neutrality constrains only the zeroth charge moment:

    $ rho_q=sum_s q_(s)n_(s) approx 0 . $

    It does not set the first moments equal. For hydrogen,

    $ rho_q approx e(n_(i)-n_(e)), quad
      bold(j)=e n_(i) bold(u)_(i)-e n_(e) bold(u)_(e) . $

    The current can therefore remain finite even when the charge density is
    small.]
  )

  #multiple-fluid-hierarchy

  #interpretation(
    [Quasi-neutrality is not one-fluid motion],
    [The net charge density on bulk scales can be small while electron and ion
    flows differ substantially. Quasi-neutrality removes a large charge-density
    imbalance from the bulk ordering; it does not remove species momentum,
    pressure, or current.]
  )

  #summary[
    A two-fluid description assigns density, velocity, pressure, and source
    terms to each species. Quasi-neutrality constrains the charge-weighted
    densities, whereas current depends on charge-weighted velocities. The
    electromagnetic field is common to all species, but the response to it is
    species-dependent through $q_(s)$ and $m_(s)$.
  ]

  #knowledge-check((
    (
      question: [Which species variables are retained by a two-fluid model?],
      answer: [At minimum, each species has $n_(s)$, $bold(u)_(s)$, and a
      pressure model $bold(P)_(s)$, together with fields and collision or
      source terms.]
    ),
    (
      question: [What does quasi-neutrality constrain?],
      answer: [It constrains the charge density
      $rho_q=sum_s q_(s)n_(s)$ to be small in the adopted ordering. It does not
      require $bold(u)_(e)=bold(u)_(i)$.]
    ),
    (
      question: [Why can a quasi-neutral plasma carry a current?],
      answer: [Because the current is
      $bold(j)=sum_s q_(s)n_(s)bold(u)_(s)$. Equal and opposite charge
      densities can be accompanied by different species velocities.]
    ),
    (
      question: [What is the physical role of the magnetic field in the
      species equations?],
      answer: [It couples to each species through
      $q_(s)n_(s) (bold(u)_(s) times bold(B))$. The force is perpendicular to
      the instantaneous velocity and changes direction of motion without
      directly doing work.]
    ),
  ))

  #section-title[Complete two-fluid equations] <multiple-equations>

  #lead[
    What must be evolved once the species variables are defined? Each species
    needs particle conservation, momentum transport, and an energy or pressure
    closure. Maxwell's equations provide the shared fields and the coupling
    between the species currents and charge density.
  ]

  #objectives((
    [write the conservative continuity, momentum, and energy equations],
    [identify the Lorentz force and collision moments in each species equation],
    [state the Maxwell equations that close the field coupling],
    [separate exact moment equations from pressure and collision closures],
  ))

  #unit-ledger[
    The Lorentz force density is in #unit("N/m^3"), because $q_(s)n_(s)
    bold(E)$ and $q_(s)n_(s)(bold(u)_(s) times bold(B))$ have that unit. The
    pressure divergence and $bold(R)_(s)$ are also force densities.
  ]

  #assumption(
    [Equation ledger],
    [Use fixed species labels $e$ and $i$, no ionization or recombination
    source, and a smooth distribution that vanishes at large velocity. The
    collision moments are left explicit: $bold(R)_(s)$ transfers momentum and
    $Q_(s)$ transfers energy. For isolated elastic interspecies collisions,
    $sum_s bold(R)_(s)=bold(0)$ and $sum_s Q_(s)=0$.]
  )

  The species continuity equation is

  $ pdv(n_(s), t) + div(n_(s) bold(u)_(s)) = 0 $
    <multiple-continuity>

  In conservative momentum form,

  $ pdv(rho_(s) bold(u)_(s), t)
    + div(rho_(s) bold(u)_(s) bold(u)_(s) + bold(P)_(s))
    = q_(s) n_(s) (bold(E) + bold(u)_(s) times bold(B))
    + bold(R)_(s) $ <multiple-momentum-conservative>

  Equivalently, after using continuity, the left-hand side can be written as
  the species material derivative:

  $ rho_(s) (pdv(bold(u)_(s), t)
    + bold(u)_(s) dot grad(bold(u)_(s)))
    = q_(s) n_(s) (bold(E) + bold(u)_(s) times bold(B))
    - div(bold(P)_(s)) + bold(R)_(s) $
    <multiple-momentum-material>

  #equation-note[
    The momentum density is in #unit("kg m^-2 s^-1"). Every term in the
    material equation is a force density in #unit("N/m^3"). The tensor divergence becomes
    $grad(p_(s))$ only for an isotropic pressure tensor.
  ]

  As in Chapter 6, $bold(w)_(s)=bold(v)-bold(u)_(s)$ is the random velocity
  relative to the species flow. Define the total species kinetic-energy
  density and heat-flux vector by

  $ W_(s) = (rho_(s) bold(u)_(s)^2)/2 + epsilon_(s), quad
    epsilon_(s) = (m_(s) integral bold(w)_(s)^2 f_(s) dif^3 bold(v))/2 $
    <multiple-energy-definitions>

  $ bold(q)_(h,s) = (m_(s) integral bold(w)_(s)^2 bold(w)_(s)
    f_(s) dif^3 bold(v))/2 $ <multiple-heat-flux>

  The subscript $h$ labels heat flux, distinguishing this vector from particle
  charge $q_(s)$. The energy $W_(s)$ contains bulk and random kinetic energy;
  electromagnetic field energy is separate.

  The corresponding energy balance is

  $ pdv(W_(s), t) + div(W_(s) bold(u)_(s) + bold(P)_(s) dot bold(u)_(s)
      + bold(q)_(h,s))
    = q_(s)n_(s) bold(u)_(s) dot bold(E) + Q_(s) $
    <multiple-energy>

  The field equations are

  $ div(bold(E)) = rho_q/epsilon_0, quad div(bold(B)) = 0 $
    <multiple-gauss-laws>

  $ curl(bold(E)) = -pdv(bold(B), t), quad
    curl(bold(B)) = mu_0 bold(j) + mu_0 epsilon_0 pdv(bold(E), t) $
    <multiple-maxwell>

  #details(
    [Derivation: from the kinetic equation to the fluid balances],
    [#derivation-step[Start with the conservative kinetic equation]
    Use

    $ pdv(f_(s),t)+div(f_(s)bold(v))
        +div(f_(s)bold(a)_(s))=C_(s)[f] , $

    with

    $ bold(a)_(s)=q_(s)/m_(s)
        (bold(E)+bold(v) times bold(B)) . $

    #derivation-step[Take the zeroth moment]
    Integrating over velocity gives $pdv(n_(s),t)$ from the time term and
    $div(n_(s)bold(u)_(s))$ from spatial streaming. The velocity divergence is
    a vanishing surface term, and particle-conserving collisions have zero
    zeroth moment. This gives the species continuity equation.

    #derivation-step[Take the first moment]
    Multiply by $m_(s)bold(v)$ and integrate. In components, spatial streaming
    gives

    $ m_(s) integral v_i pdv((v_j f_(s)),x_j) dif^3 bold(v)
        =pdv((m_(s) integral v_i v_j f_(s) dif^3 bold(v)),x_j) . $

    Writing $bold(v)=bold(u)_(s)+bold(w)_(s)$ decomposes the raw tensor into

    $ rho_(s)bold(u)_(s)bold(u)_(s)+bold(P)_(s) . $

    #derivation-step[Evaluate the Lorentz and collision moments]
    Integration by parts in velocity gives

    $ m_(s) integral v_i pdv((a_(s,j)f_(s)),v_j) dif^3 bold(v)
        =-m_(s) integral a_(s,i)f_(s) dif^3 bold(v) . $

    Moving this term to the right gives

    $ m_(s) integral bold(a)_(s)f_(s) dif^3 bold(v)
        =q_(s)n_(s)bold(E)
        +q_(s)n_(s)(bold(u)_(s)times bold(B)) . $

    The remaining collision moment is

    $ bold(R)_(s)=m_(s) integral bold(v)C_(s)[f] dif^3 bold(v) . $

    #derivation-step[Take the energy moment]
    Multiply by $(m_(s)v^2)/2$. After integration by parts, the force work is
    $-m_(s) integral bold(v) dot bold(a)_(s) f_(s)dif^3 bold(v)$. The magnetic
    contribution vanishes because
    $bold(v) dot (bold(v) times bold(B))=0$, while the electric contribution
    is $q_(s)n_(s)bold(u)_(s)dot bold(E)$.

    Splitting

    $ v^2=bold(u)_(s)^2+2bold(u)_(s)dot bold(w)_(s)+bold(w)_(s)^2 $

    separates directed kinetic energy, internal energy, pressure work, and
    heat flux. The collision energy moment is

    $ Q_(s)=(m_(s)/2) integral v^2 C_(s)[f] dif^3 bold(v) . $

    No pressure equation has been assumed. Replacing $bold(P)_(s)$ by a scalar
    or $bold(q)_(h,s)$ by a constitutive law is a separate closure choice.]
  )

  #rechenbeispiel[
    Context: a quasi-neutral hydrogen plasma has
    $n_(e)=n_(i)=qty("1.0e16", "m^-3")$, ion speed
    $u_(i,x)=qty("2.0e5", "m/s")$, electron speed
    $u_(e,x)=qty("1.5e5", "m/s")$, and
    $e=qty("1.602e-19", "C")$.

    Assumptions: singly charged species, equal densities, and one-dimensional
    flows along $x$.

    Target: report the charge density and the total $x$-directed current
    density.

    Numerical result: $rho_q=qty("0", "C/m^3")$ and
    $j_x=qty("80.1", "A/m^2")$.
  ]

  #interpretation(
    [Electromagnetic and collisional coupling],
    [The electron and ion equations are separate, but they share
    $bold(E)$ and $bold(B)$. The fields depend on the total charge and current,
    while collisions can transfer momentum and energy between species. The
    coupling is therefore both electromagnetic and collisional.]
  )

  #summary[
    The complete two-fluid model consists of one continuity, momentum, and
    energy balance for each species, Maxwell's equations, and constitutive
    choices for pressure and collisions. The moment balances are exact under
    the stated boundary assumptions. Cold, isotropic, collisional, and
    collisionless models arise only after additional terms are ordered or
    closed.
  ]

  #exam-prompts(
    (
      [(a) Write down the two-fluid equations of a hydrogen plasma.],
    ),
    [Plasma Physics Exam.pdf, p. 3],
  )

  #knowledge-check((
    (
      question: [Which term couples a species momentum equation to the
      electromagnetic field?],
      answer: [The Lorentz force density
      $q_(s)n_(s)(bold(E)+bold(u)_(s)times bold(B))$ couples the species
      momentum to the common fields.]
    ),
    (
      question: [When can the pressure-tensor divergence be written as a
      pressure gradient?],
      answer: [When the pressure tensor is isotropic,
      $bold(P)_(s)=p_(s)bold(I)$, so that
      $div(bold(P)_(s))=grad(p_(s))$. Isotropy is an additional model assumption.]
    ),
    (
      question: [Why does the magnetic force not appear in the species energy
      source?],
      answer: [Because
      $bold(u)_(s) dot (bold(u)_(s)times bold(B))=0$. The magnetic force changes
      direction but does no direct work; the electric field contributes
      $q_(s)n_(s)bold(u)_(s)dot bold(E)$.]
    ),
    (
      question: [What must be specified in addition to the exact moment
      balances to obtain a usable fluid model?],
      answer: [One must choose pressure and heat-flux closures and specify
      collision or source models. Those choices state which kinetic information
      has been discarded.]
    ),
  ))

  #section-title[Perpendicular drift balance] <multiple-perpendicular-drifts>

  #lead[
    How does a pressure gradient move a magnetized species? On scales longer
    than its gyroradius, the perpendicular momentum equation can balance the
    pressure force against the Lorentz force. Solving that local balance
    reveals a common electric drift and a species-dependent diamagnetic drift.
  ]

  #objectives((
    [state the ordering behind a local perpendicular force balance],
    [derive the electric and pressure-gradient drift velocities],
    [track the sign of the diamagnetic drift for electrons and ions],
    [identify the terms that invalidate the low-inertia drift ordering],
  ))

  #assumption(
    [Local drift ordering],
    [Assume a locally uniform magnetic field, an isotropic pressure tensor, and
    a perpendicular scale much larger than the gyroradius. Neglect the
    perpendicular inertial, collisional, and time-derivative terms for the
    leading balance.]
  )

  Let $bold(b)=bold(B)/B$ and project the species momentum balance
  perpendicular to the field:

  $ 0 approx q_(s)n_(s) (bold(E)_perp + bold(u)_(s,perp) times bold(B))
    - grad_perp p_(s) $ <multiple-perpendicular-balance>

  Here $bold(E)_perp=bold(E)-bold(b)(bold(b)dot bold(E))$ and
  $grad_perp=grad-bold(b)(bold(b)dot grad)$ are perpendicular projections.
  Solving for the perpendicular velocity gives

  $ bold(u)_(s,perp) = bold(u)_(E times B) + bold(u)_(*,s) $
    <multiple-drift-decomposition>

  $ bold(u)_(E times B) = (bold(E) times bold(B))/(B^2) $
    <multiple-exb-drift>

  $ bold(u)_(*,s) = (bold(B) times grad(p_(s)))/(q_(s)n_(s)B^2) $ <multiple-diamagnetic-drift>

  #equation-note[
    Both velocities are in #unit("m/s"). The electric drift is independent
    of species, while the diamagnetic drift changes sign with $q_(s)$ and
    depends on the species pressure gradient. The star labels the diamagnetic
    contribution; it is not a complex conjugate. If the pressure is uniform,
    $bold(u)_(*,s)=bold(0)$.
  ]

  #details(
    [Derivation: solve the perpendicular force balance],
    [#derivation-step[Write the perpendicular force balance]
    Start with

    $ q_(s)n_(s)(bold(E)_perp+bold(u)_(s,perp)times bold(B))
        =grad_perp p_(s) . $

    #derivation-step[Eliminate the magnetic cross product]
    Cross the equation with $bold(B)$ from the right. The identity

    $ (bold(u)times bold(B))times bold(B)=-B^2 bold(u)_perp $

    gives

    $ q_(s)n_(s)bold(E)times bold(B)
        -q_(s)n_(s)B^2 bold(u)_(s,perp)
        =grad(p_(s))times bold(B) . $

    #derivation-step[Separate the two perpendicular drifts]
    Rearrange and use
    $grad(p) times bold(B)=-bold(B)times grad(p):$

    $ bold(u)_(s,perp)=(bold(E)times bold(B))/(B^2)
        +(bold(B)times grad(p_(s)))/(q_(s)n_(s)B^2) . $

    The first term is the common electric drift because $q_(s)$ cancels from
    the electric force balance. The second is the charge-dependent
    diamagnetic drift. The spatial ordering requires the pressure-gradient
    scale $L_perp$ to be much larger than the species gyroradius $r_(L,s)$,
    both measured in metres:

    $ r_(L,s)/L_perp << 1 . $

    This dimensionless inequality supports a local orbit average. Neglecting
    inertia also requires slow evolution and small convective acceleration
    relative to the retained forces, as assumed above. Here $r_(L,s)$ denotes
    orbit size; $rho_(s)$ continues to denote mass density.]
  )

  #rechenbeispiel[
    Context: in a local Cartesian frame, take
    $bold(B)=qty("0.0100", "T") bold(e)_(z)$,
    $bold(E)=qty("30.0", "V/m") bold(e)_(x)$,
    $n_(i)=n_(e)=qty("1.0e14", "m^-3")$, and
    $grad(p_(i))=grad(p_(e))=qty("1.602e-5", "Pa/m") bold(e)_(x)$.
    Use $e=qty("1.602e-19", "C")$, with $q_i=+e$ and $q_e=-e$.

    Assumptions: scalar pressure, locally uniform fields, and the
    inertia-free perpendicular drift ordering.

    Target: report the common electric drift and the ion and electron
    diamagnetic drift velocities.

    Numerical result: $bold(u)_(E times B)=-3.00 dot 10^3
    #unit("m/s") bold(e)_(y)$, $bold(u)_(*,i)=+1.00 dot 10^2
    #unit("m/s") bold(e)_(y)$, and
    $bold(u)_(*,e)=-1.00 dot 10^2 #unit("m/s") bold(e)_(y)$.
  ]

  #interpretation(
    [Common and species-dependent drifts],
    [$bold(u)_(E times B)$ advects both species together, so its current
    cancels to leading order under quasi-neutrality. For pressure gradients
    pointing in the same direction, the diamagnetic velocities of ions and
    electrons point oppositely. These are local fluid velocity moments;
    they need not represent motion of the orbit centers. Charge-weighting
    them gives the diamagnetic current discussed in the next section.]
  )

  #summary[
    A perpendicular pressure force is balanced locally by the magnetic force.
    The resulting velocity is the sum of the common $E times B$ drift and the
    charge-dependent diamagnetic drift. The expression is valid only when
    inertia, collisions, and field nonuniformity are subleading on the chosen
    scale.
  ]

  #knowledge-check((
    (
      question: [Which term makes the electric drift common to both species?],
      answer: [The electric force is proportional to $q_(s)$, which cancels
      the $1/q_(s)$ introduced when the perpendicular Lorentz balance is
      solved. Thus $bold(u)_(E times B)=(bold(E)times bold(B))/(B^2)$.]
    ),
    (
      question: [How does reversing the charge affect the diamagnetic drift?],
      answer: [It reverses $bold(u)_(*,s)$ because the drift is proportional to
      $1/q_(s)$. The pressure gradient and magnetic-field directions remain
      unchanged.]
    ),
    (
      question: [What scale ordering supports the local drift balance?],
      answer: [The pressure-gradient scale must be much larger than the
      species gyroradius, and perpendicular inertia and collisions must be
      small compared with the Lorentz and pressure forces.]
    ),
    (
      question: [What happens to the pressure-gradient drift when
      $grad(p_(s))=bold(0)$?],
      answer: [It vanishes. The species can still share a nonzero electric
      $E times B$ drift if a perpendicular electric field is present.]
    ),
  ))

  #section-title[Diamagnetic current] <multiple-diamagnetic-current>

  #lead[
    Why can opposite particle drifts produce one current direction? Current is
    charge-weighted flow. The charge sign that reverses the electron drift is
    multiplied once more when the electron contribution to the current is
    formed, so the two species contributions add.
  ]

  #objectives((
    [sum the species drift currents in a quasi-neutral plasma],
    [show why the common electric drift contributes little net current],
    [relate the diamagnetic current to the total pressure gradient],
    [distinguish current response from bulk mass transport],
  ))

  #assumption(
    [Quasi-neutral local sum],
    [Use $n_(e) approx n_(i)$ only when evaluating the common electric-drift
    current. Retain separate species pressures and velocities. The magnetic
    field is locally smooth, and the pressure tensor is represented by scalar
    pressures for this interpretation.]
  )

  Insert the perpendicular drift into the current definition:

  $ bold(j)_perp = sum_s q_(s)n_(s)bold(u)_(s,perp)
    = (rho_q (bold(E) times bold(B)))/(B^2)
      + (sum_s (bold(B) times grad(p_(s))))/(B^2) $
    <multiple-current-sum>

  Under quasi-neutrality, the first term is small and the pressure term is

  $ bold(j)_* = (bold(B) times grad(p_(e)+p_(i)))/(B^2) $
    <multiple-diamagnetic-current>

  For scalar ideal-gas pressures, $p_(s)=n_(s) k_B T_(s)$. If
  $n_(e) approx n_(i) approx n$, then

  $ grad(p_(e)+p_(i)) = k_B ((T_(e)+T_(i)) grad(n)
    + n grad(T_(e)+T_(i))) $ <multiple-pressure-gradient>

  #equation-note[
    The diamagnetic current is perpendicular to both $bold(B)$ and the total
    pressure gradient. A pressure gradient can therefore drive a current even while the
    leading-order charge density remains nearly zero.
  ]

  For example, take uniform $bold(B)=B bold(e)_(z)$, no electric field,
  constant temperature, and a density increasing with $x$ over many
  gyroradii. More gyro-orbits centered on the dense side cross a given point
  than do orbits centered on the dilute side. Their opposite local velocities
  therefore do not cancel: positive ions have a mean velocity along
  $+bold(e)_(y)$ and electrons along $-bold(e)_(y)$. The guiding centers have
  no perpendicular drift in this uniform field. The local velocity moment
  records the imbalance of orbit crossings, not migration of their centers.

  #details(
    [Derivation: add the charge-weighted drift responses],
    [#derivation-step[Charge-weight one species]
    For each species, the diamagnetic contribution obeys

    $ q_(s)n_(s)bold(u)_(*,s)
        =(bold(B)times grad(p_(s)))/(B^2) . $

    The factors $q_(s)n_(s)$ cancel the denominator in the species velocity.

    #derivation-step[Sum the diamagnetic currents]
    Summing over electrons and ions gives

    $ bold(j)_*=(bold(B)times[
          grad(p_(e))+grad(p_(i))])/(B^2) . $

    The pressure-drift velocities are opposite for opposite charges, but their
    charge-weighted currents add.

    #derivation-step[Check the common electric drift]
    The common drift instead gives

    $ sum_s q_(s)n_(s)bold(u)_(E times B)
        =rho_q bold(u)_(E times B) . $

    It vanishes at leading order when $rho_q approx 0$. This cancellation is
    different from the diamagnetic sum because the electric drift is the same
    for both species.

    #derivation-step[Interpret the result as a current response]
    The formula does not by itself assert that the center of mass moves across
    the pressure gradient. In a stationary, locally ordered configuration,
    diamagnetic flow can be divergence-free. Whether it transports mass or
    changes the pressure profile requires the full continuity and momentum
    equations, boundary conditions, and the terms omitted in the local
    balance.]
  )

  #rechenbeispiel[
    Context: a quasi-neutral hydrogen plasma has
    $bold(B)=qty("0.0100", "T") bold(e)_(z)$ and total pressure gradient
    $grad(p_(e)+p_(i))=qty("3.204e-5", "Pa/m") bold(e)_(x)$.
    Neglect the charge-density contribution to the common electric drift
    current.

    Assumptions: local scalar-pressure drift ordering with
    $rho_q approx 0$.

    Target: report the diamagnetic current density and the leading-order
    electric-drift current density.

    Numerical result: $bold(j)_*=+3.20 dot 10^(-3) #unit("A/m^2") bold(e)_(y)$,
    while $bold(j)_(E times B)=qty("0", "A/m^2")$.
  ]

  #interpretation(
    [Current without bulk advection],
    [Current weights each species flow by charge; mass flux weights it by
    mass. They therefore describe different aspects of the same distribution.
    In the uniform-field example, unequal orbit crossings produce a local
    diamagnetic current even though the guiding centers do not drift across
    the field. A local flow moment alone does not establish transport across
    the pressure profile.]
  )

  #summary[
    Charge-weighting converts opposite diamagnetic velocities into additive
    current contributions. In a quasi-neutral hydrogen plasma,
    $bold(j)_*=(bold(B)times grad(p_(e)+p_(i)))/(B^2)$, while the common electric
    drift contributes only through the small charge density. The current is a
    response to the pressure gradient; its interpretation as transport needs
    the full fluid balance and boundary conditions.
  ]

  #exam-prompts(
    (
      [(b) What is the diamagnetic drift? Derive and interpret it. How does it
      result in a diamagnetic current?],
    ),
    [Plasma Physics Exam.pdf, p. 3],
  )

  #knowledge-check((
    (
      question: [Why do the electron and ion diamagnetic currents add?],
      answer: [Their diamagnetic velocities have opposite signs, but each
      current is multiplied by its own charge. Since
      $q_(s)n_(s)bold(u)_(*,s)=(bold(B)times grad(p_(s)))/(B^2)$, both contributions
      point along the corresponding pressure-gradient cross-field direction.]
    ),
    (
      question: [What is the quasi-neutral electric-drift current?],
      answer: [It is
      $bold(j)_(E times B)=rho_q bold(u)_(E times B)$, so it is small when
      $rho_q approx 0$.]
    ),
    (
      question: [Which pressure enters the two-species diamagnetic current?],
      answer: [The total scalar pressure gradient enters:
      $grad(p_(e)+p_(i))$. Separate species pressures add after the
      charge-weighted drift sum is formed.]
    ),
    (
      question: [Why should a diamagnetic current not automatically be called
      a net mass flux?],
      answer: [Current is charge-weighted flow, whereas mass flux is
      $sum_s rho_(s)bold(u)_(s)$. A pressure-driven current can be locally
      divergence-free and require no comparable center-of-mass transport.]
    ),
  ))

  #section-title[Parallel force balance and the one-fluid limit] <multiple-parallel-balance>

  #lead[
    What remains after perpendicular drifts have been separated? Along the
    magnetic field, the Lorentz force has no magnetic component. Parallel
    pressure gradients, electric fields, inertia, and collisions therefore
    determine the species response and provide the bridge to one-fluid models.
  ]

  #objectives((
    [project the species momentum equation along the magnetic field],
    [derive the isothermal electron Boltzmann response as a limiting case],
    [define total mass velocity, pressure, charge, and current variables],
    [identify the relative-flow stress retained when species equations are
    summed],
  ))

  #assumption(
    [Parallel ordering],
    [Let $bold(b)=bold(B)/B$. The magnetic part of the Lorentz force has zero
    projection along $bold(b)$ exactly. Use scalar species pressures in the
    displayed parallel equation. For the scalar parallel-velocity form,
    take the field direction as locally fixed on the scale of interest;
    otherwise retain $bold(b) dot pdv(bold(u)_(s),t)$ and the associated
    field-line geometry rather than replacing it by a derivative of
    $u_(parallel,s)$. Keep inertia and collisions until a further limit is
    stated. The Boltzmann response below additionally assumes negligible
    parallel inertia and collisions, scalar isothermal electron pressure, and
    a connected field line.]
  )

  Projecting the species momentum equation gives

  $ rho_(s) (pdv(u_(parallel,s), t)
    + bold(u)_(s) dot grad(u_(parallel,s)))
    = -bold(b) dot grad(p_(s))
      + q_(s)n_(s) E_parallel + R_(parallel,s),
    quad E_parallel = bold(b) dot bold(E) $
    <multiple-parallel-equation>

  For inertialess, collisionless electrons with $q_(e)=-e$,

  $ 0 = -bold(b) dot grad(p_(e)) - e n_(e) E_parallel $
    <multiple-electron-balance>

  With $p_(e)=n_(e) k_B T_(e)$ and uniform $T_(e)$, this becomes

  $ E_parallel = -((k_B T_(e))/e) bold(b) dot grad(ln n_(e)),
    quad E_parallel=-bold(b) dot grad(phi) $
    <multiple-boltzmann-field>

  and integration along a field line gives the electron Boltzmann relation

  $ n_(e) = n_(e,0) exp((e (phi-phi_0))/(k_B T_(e))) $
    <multiple-boltzmann-response>

  Here $n_(e,0)$ is the density at a reference point with potential $phi_0$
  on the same field line. Parallel balance fixes the density variation along
  that line; it does not set a common reference density for all field lines.

  The exact one-fluid definitions are

  $ rho = sum_s rho_(s), quad
    rho bold(u) = sum_s rho_(s) bold(u)_(s), quad
    bold(P)_(1) = sum_s bold(P)_(s)
      + sum_s rho_(s) bold(V)_(s) bold(V)_(s) $
    <multiple-one-fluid-pressure>

  $ rho_q = sum_s q_(s)n_(s), quad
    bold(j) = sum_s q_(s)n_(s)bold(u)_(s), quad
    bold(V)_(s)=bold(u)_(s)-bold(u) $ <multiple-one-fluid-definitions>

  Here $bold(P)_(1)$ includes both random pressure and relative-flow stress.
  Adding the species momentum equations then yields

  $ pdv(rho bold(u),t)
    + div(rho bold(u) bold(u)+bold(P)_(1))
    = rho_q bold(E) + bold(j) times bold(B)
      + sum_s bold(R)_(s) $ <multiple-summed-momentum>

  For isolated elastic collisions, the last term vanishes. Dropping the
  relative-flow part of $bold(P)_(1)$ is an additional one-fluid closure, not a
  consequence of adding the equations.

  #details(
    [Derivation: parallel balance and species summation],
    [#derivation-step[Project one species along the field]
    Dot the material momentum equation with $bold(b)$. Since
    $bold(b) dot (bold(u)_(s)times bold(B))=0$, the magnetic force disappears.
    The projected pressure, electric, and collision terms are

    $ -bold(b)dot div(bold(P)_(s)), quad
      q_(s)n_(s)E_parallel, quad
      R_(parallel,s)=bold(b)dot bold(R)_(s) . $

    For scalar pressure, the first term becomes
    $-bold(b)dot grad(p_(s)).$

    #derivation-step[Derive the electron Boltzmann response]
    Set electron inertia and collisions to zero and use $q_(e)=-e$:

    $ bold(b)dot grad(p_(e))=-e n_(e)E_parallel . $

    Isothermal pressure gives
    $bold(b)dot grad(p_(e))=k_B T_(e)bold(b)dot grad(n_(e))$, so

    $ E_parallel=-((k_B T_(e))/e) bold(b)dot grad(ln n_(e)) . $

    With $E_parallel=-bold(b)dot grad(phi)$,

    $ bold(b)dot grad(ln n_(e)-(e phi)/(k_B T_(e)))=0 . $

    Along a connected field line,

    $ n_(e)=n_(e,0)exp((e(phi-phi_0))/(k_B T_(e))) . $

    #derivation-step[Sum the species momentum equations]
    Write

    $ bold(u)_(s)=bold(u)+bold(V)_(s) . $

    Then

    $ sum_s rho_(s)bold(u)_(s)bold(u)_(s)
        =rho bold(u)bold(u)+sum_s rho_(s)bold(V)_(s)bold(V)_(s) , $

    because

    $ sum_s rho_(s)bold(V)_(s)
        =sum_s rho_(s)bold(u)_(s)-rho bold(u)=bold(0) . $

    The field forces become

    $ sum_s q_(s)n_(s)bold(E)=rho_q bold(E), quad
      sum_s q_(s)n_(s)(bold(u)_(s)times bold(B))
        =bold(j)times bold(B) . $

    These identities give the summed momentum equation. If interspecies
    collisions are internal, their momentum sources cancel in the sum.]
  )

  #rechenbeispiel[
    Context: an isothermal electron population has reference density
    $n_(e,0)=qty("1.0e16", "m^-3")$, thermal energy
    $k_B T_(e)=qty("4.806e-19", "J")=qty("3.00", "eV")$, and a parallel
    potential increase $phi-phi_0=qty("3.00", "V")$. Use
    $e=qty("1.602e-19", "C")$.

    Assumptions: connected field line, negligible parallel electron inertia
    and collisions, electrostatic parallel field, and uniform $T_(e)$.

    Target: report the Boltzmann density ratio and the resulting electron
    density.

    Numerical result: $n_(e)/n_(e,0)=2.72$ (dimensionless) and
    $n_(e)=qty("2.72e16", "m^-3")$.
  ]

  #interpretation(
    [Species differences in the one-fluid limit],
    [Summing removes the labels from the total mass balance, but it does not
    erase current, relative velocity, anisotropic pressure, or collision
    exchange. A one-fluid model becomes simpler only when an ordering or
    closure justifies neglecting or modelling those species differences.]
  )

  #summary[
    Parallel force balance exposes the electron pressure--electric-field
    response and, in an isothermal collisionless limit, the Boltzmann density.
    Summing species equations defines one-fluid mass and momentum variables,
    but the relative-flow stress and current remain explicit until a further
    closure, such as the MHD ordering of Chapter 8, is made.
  ]

  #knowledge-check((
    (
      question: [Why does the magnetic force disappear from the parallel
      momentum equation?],
      answer: [The magnetic force is proportional to
      $bold(u)_(s)times bold(B)$ and is perpendicular to $bold(B)$, so its dot
      product with $bold(b)$ is zero.]
    ),
    (
      question: [Which assumptions produce the electron Boltzmann relation?],
      answer: [Negligible parallel electron inertia and collisions, scalar
      isothermal pressure, electrostatic parallel balance, and a connected
      field line lead to
      $n_(e)/n_(e,0)=exp((e(phi-phi_0))/(k_B T_(e)))$.]
    ),
    (
      question: [What is the one-fluid velocity?],
      answer: [It is the mass-weighted velocity defined by
      $rho bold(u)=sum_s rho_(s)bold(u)_(s)$, with
      $rho=sum_s rho_(s)$.]
    ),
    (
      question: [What relative-flow contribution appears in the summed
      momentum flux?],
      answer: [The tensor
      $sum_s rho_(s)bold(V)_(s)bold(V)_(s)$, where
      $bold(V)_(s)=bold(u)_(s)-bold(u)$, remains in the total pressure tensor.
      It can be neglected only under an additional ordering.]
    ),
  ))

  #chapter-nav(
    previous: (href: "06-moments.html", title: [Moments]),
    next: (href: "08-mhd.html", title: [Single-fluid MHD]),
  )
]
