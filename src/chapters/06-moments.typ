#import "../theme.typ": *
#import "../figures.typ": moment-hierarchy
#import "@preview/physica:0.9.8": div, grad, pdv
#import "@preview/unify:0.8.1": unit

#let chapter = [
  #page-title(number: 6)[Moments of the Boltzmann equation] <moments>

  #lead[
    Many plasma problems concern density, flow, or energy transport rather
    than the full velocity distribution. Velocity moments turn the kinetic
    equation from Chapter 5 into evolution equations for these fluid fields.
    The reduction remains incomplete: the transport equation for one moment
    usually introduces a higher moment, so a finite model needs a closure.
  ]

  #callout(
    [Moment models and closure],
    [A moment model is obtained by integrating the kinetic equation against a chosen weight,
    keeping the resulting conservation laws, and then stating how the first
    omitted moment is represented. The closure is part of the model and must
    be visible.]
  )

  #section-title[Velocity moments and fluid variables] <moments-definitions>

  #lead[
    Which macroscopic quantities can be computed from a one-particle
    distribution? Start with the number of particles in a velocity-space
    element, then use increasingly informative velocity weights.
  ]

  #objectives((
    [define number, mass, charge, and current densities as moments of $f_s$],
    [compute the species fluid velocity from the first moment],
    [construct the pressure tensor from the random velocity],
    [identify which information is discarded at each moment order],
  ))

  #unit-ledger[
    Mass density is in #unit("kg/m^3"), momentum density is in
    #unit("kg m^-2 s^-1"), and pressure is in #unit("Pa") $=$ #unit("N/m^2")
    $=$ #unit("kg m^-1 s^-2"). The symbols $bold(u)_s$, $bold(P)_s$, and
    $bold(q)_s$ below denote velocity, pressure tensor, and heat-flux vector,
    respectively. The bold heat-flux symbol $bold(q)_s$ is distinct from the
    scalar particle charge $q_s$.
  ]

  #definition(
    [Distribution and velocity moment],
    [For species $s$, the phase-space distribution is defined by
    $d N_s = f_(s)(t, bold(r), bold(v)) dif^3 bold(r) dif^3 bold(v)$. For a
    velocity weight $A(bold(v))$, its local velocity moment is
    $integral A(bold(v)) f_s dif^3 bold(v)$. The zeroth moment counts particles,
    while the weight determines which physical average is retained.]
  )

  At fixed position, integration over velocity gives the species number
  density:

  $ n_s = integral_(RR^3) f_s dif^3 bold(v) $ <moments-number-density>

  The corresponding mass density, charge density, and current density are

  $ rho_s = m_s n_s, quad
    rho_q = sum_s q_s n_s, quad
    bold(j)_s = q_s integral_(RR^3) bold(v) f_s dif^3 bold(v) $ \
  $ bold(j) = sum_s bold(j)_s $ <moments-charge-current>

  #equation-note[
    The charge density $rho_q$ is in #unit("C/m^3"). The
    current density $bold(j)$ is the charge-weighted particle flux. Because
    both are sums over species, an electrically neutral plasma can have
    $rho_q approx 0$ while carrying a nonzero current.
  ]

  The first velocity moment is the particle flux. Dividing it by number
  density defines the species fluid velocity:

  $ bold(u)_s = (1/n_s) integral_(RR^3) bold(v) f_s dif^3 bold(v), quad
    bold(j)_s = q_s n_s bold(u)_s $ <moments-fluid-velocity>

  Introduce the random velocity relative to this local mean,

  $ bold(w)_s = bold(v) - bold(u)_s, quad
    integral_(RR^3) bold(w)_s f_s dif^3 bold(v) = bold(0) $ \
  <moments-random-velocity>

  The second central moment is the pressure tensor:

  $ bold(P)_s = m_s integral_(RR^3)
    bold(w)_s bold(w)_s f_s dif^3 bold(v) $ <moments-pressure-tensor>

  #equation-note[
    The product $bold(w)_s bold(w)_s$ is dyadic, so $bold(P)_s$ is a rank-two
    tensor. Its diagonal entries are normal momentum fluxes and its
    off-diagonal entries are shear momentum fluxes. In an isotropic state the
    tensor reduces to a scalar pressure times the identity, but isotropy is an
    additional assumption, not a consequence of taking a moment.
  ]

  “Raw” moments use the laboratory velocity $bold(v)$; “central” moments use
  the velocity relative to the local flow. The raw second moment therefore
  contains both directed flow and random motion:

  $ bold(M)_s = m_s integral_(RR^3)
    bold(v) bold(v) f_s dif^3 bold(v)
    = bold(P)_s + rho_s bold(u)_s bold(u)_s $ <moments-raw-second>

  #details(
    [Derivation: central and raw second moments],
    [#derivation-step[Split velocity into bulk and random parts]
    Insert

    $ bold(v)=bold(u)_s+bold(w)_s $

    into the raw second moment. The dyadic expansion is

    $ bold(v) bold(v)=bold(u)_s bold(u)_s
        +bold(u)_s bold(w)_s+bold(w)_s bold(u)_s
        +bold(w)_s bold(w)_s .$

    #derivation-step[Use the definition of the local mean]
    By construction,

    $ integral bold(w)_s f_s dif^3 bold(v)=bold(0) .$

    The two cross terms therefore vanish. The bulk term gives
    $n_s bold(u)_s bold(u)_s$, which becomes
    $rho_s bold(u)_s bold(u)_s$ after multiplication by $m_s$.

    #derivation-step[Identify the pressure tensor]
    The remaining central term is the pressure tensor:

    $ bold(P)_s=m_s integral bold(w)_s bold(w)_s f_s dif^3 bold(v) .$

    Consequently,

    $ bold(M)_s=bold(P)_s+rho_s bold(u)_s bold(u)_s .$

    Both terms are momentum fluxes with units
    #unit("Pa") $=$ #unit("kg m^-1 s^-2"). The central tensor vanishes for
    a cold delta-like velocity distribution.]
  )

  #moment-hierarchy

  #animation(
    "../media/moment-hierarchy.mp4",
    "The animation reduces the distribution function to number density, bulk velocity, pressure tensor, and the full third central moment tensor. Heat flux is identified as a contraction of the third central tensor. Arrows show how each transport equation introduces a higher moment and therefore requires closure.",
    caption: [
      Moment hierarchy from kinetic information to fluid fields. The animation
      labels dimensional quantities.
      The full third central tensor $Q_(i j k)$ contains more information
      than heat flux $q_i=(1/2) sum_j Q_(i j j)$.
    ],
    poster: "../media/moment-hierarchy.png",
  )

  #interpretation(
    [Information discarded at each moment order],
    [The density forgets how particles are distributed in velocity. The flow
    velocity restores the first directional average. The pressure tensor
    retains the covariance of random motion, including anisotropy and shear.
    Higher moments retain asymmetric tails and energy transport. Two
    distributions can therefore have the same $n_s$, $bold(u)_s$, and
    $bold(P)_s$ while carrying different heat fluxes or kinetic instabilities.]
  )

  #summary[
    Integrating $f_s$ over velocity gives number density. Multiplying by mass
    or charge gives mass or charge density, and weighting once gives the fluid
    velocity and current. The central second moment is the pressure tensor.
    These are exact definitions. Replacing the tensor or the higher moments by
    simpler forms is a later closure assumption.
  ]

  #exam-prompts(
    (
      [(a) How are particle density, mass density and charge density computed from a given (one-particle) distribution function f(t,x,v)?],
      [(b) How are species fluid velocity and pressure tensor computed starting from a kinetic description?],
    ),
    [Plasma Physics Exam.pdf, p. 2],
  )

  #knowledge-check((
    (
      question: [Which velocity weight produces the number density?],
      answer: [The zeroth weight, $A=1$, gives
      $n_s=integral f_s dif^3 bold(v)$ in #unit("m^-3").],
    ),
    (
      question: [Why can a neutral plasma carry current?],
      answer: [Neutrality constrains the charge-weighted density
      $rho_q=sum_s q_s n_s$, whereas current depends on the charge-weighted
      flow $bold(j)=sum_s q_s n_s bold(u)_s$. Opposite species flows can cancel
      charge while adding current.]
    ),
    (
      question: [What is removed when the pressure tensor is replaced by a scalar pressure?],
      answer: [Directional information is removed. The replacement keeps only
      $p_s=(sum_i (P_s)_(i i))/3$ and discards anisotropic normal stresses and
      off-diagonal shear stresses.]
    ),
    (
      question: [How would a cold distribution appear in the central second moment?],
      answer: [If every particle has the local velocity $bold(u)_s$, then
      $bold(w)_s=bold(0)$ and $bold(P)_s=bold(0)$. Finite spread in velocity
      produces nonzero pressure.]
    ),
  ))

  #section-title[Zeroth moment and continuity] <moments-continuity>

  #lead[
    A fluid density changes only when particles cross a spatial boundary or
    when the model creates or removes particles. The zeroth velocity moment of
    the kinetic equation turns that statement into a local continuity law.
  ]

  #objectives((
    [integrate the kinetic equation over all velocity space],
    [identify the vanishing velocity-space and collision contributions],
    [derive species number, mass, and charge continuity equations],
    [rewrite continuity in Eulerian and fluid-following forms],
  ))

  #unit-ledger[
    The continuity equation balances a density in #unit("m^-3") per #unit("s")
    with the divergence of a flux in #unit("m^-2 s^-1"). The same balance
    multiplied by mass or charge gives mass or charge continuity.
  ]

  #assumption(
    [Velocity-space boundary and particle conservation],
    [Assume $f_s$ and the velocity-space flux vanish sufficiently rapidly as
    $abs(bold(v)) -> infinity$. Assume ordinary collisions do not create or
    destroy particles of species $s$, so
    $integral C_(s)[f] dif^3 bold(v)=0$. Ionization, recombination, or an imposed
    source would add a nonzero right-hand side and must be stated separately.]
  )

  Start from the conservative kinetic equation for the species. As in
  Chapter 5, the streaming divergence acts on position and the acceleration
  divergence acts on velocity:

  $ pdv(f_s,t) + div(f_s bold(v))
    + div(f_s bold(a)_s) = C_(s)[f] $ <moments-kinetic-balance>

  Integrate it over all velocity space. The result is

  $ integral_(RR^3) pdv(f_s,t) dif^3 bold(v)
    + integral_(RR^3) div(f_s bold(v)) dif^3 bold(v)
    + integral_(RR^3) div(f_s bold(a)_s) dif^3 bold(v)
    = integral_(RR^3) C_(s)[f] dif^3 bold(v) $ <moments-zeroth-integral>

  The time derivative passes through the velocity integral, and the spatial
  divergence does too because velocity is an independent integration
  variable:

  $ integral_(RR^3) pdv(f_s,t) dif^3 bold(v) = pdv(n_s,t), quad
    integral_(RR^3) div(f_s bold(v)) dif^3 bold(v)
    = div(n_s bold(u)_s) $ <moments-continuity-terms>

  The velocity-space term is a surface flux at infinity and vanishes under the
  stated boundary assumption. The collision integral vanishes by particle
  conservation. Thus the species continuity equation is

  $ pdv(n_s,t) + div(n_s bold(u)_s) = 0 $ \
  <moments-number-continuity>

  Multiplying by the constant species mass gives mass continuity:

  $ pdv(rho_s,t) + div(rho_s bold(u)_s) = 0 $ \
  <moments-mass-continuity>

  Multiplying by charge and summing over species gives total charge
  continuity:

  $ pdv(rho_q,t) + div(bold(j)) = 0 $ <moments-charge-continuity>

  #equation-note[
    The flux in the number equation is $n_s bold(u)_s$ in
    #unit("m^-2 s^-1"). A source, sink, or ionization model would
    appear as $S_s$ on the right-hand side. The source-free equation is local,
    so it applies even when the total number in a finite region changes by
    flux through its boundary.
  ]

  #details(
    [Derivation: every term in the zeroth moment],
    [#derivation-step[Integrate the temporal term]
    Integrate the kinetic equation over a velocity-space domain $V_v$ and then
    let its boundary tend to infinity:

    $ integral_(V_v) pdv(f_s,t) dif^3 bold(v)
        =pdv(integral_(V_v) f_s dif^3 bold(v),t)
        -> pdv(n_s,t) .$

    #derivation-step[Identify the spatial particle flux]
    Commute the spatial divergence with the velocity integral:

    $ integral_(V_v) div(f_s bold(v)) dif^3 bold(v)
        =div(integral_(V_v) bold(v) f_s dif^3 bold(v))
        =div(n_s bold(u)_s) .$

    #derivation-step[Discard velocity-space and collision sources]
    The velocity-space divergence becomes a boundary integral:

    $ integral_(V_v) div(f_s bold(a)_s) dif^3 bold(v)
        =integral_(partial V_v) f_s bold(a)_s dot d bold(S)_v .$

    It vanishes when the distribution decays faster than the surface measure
    grows. Number-conserving collisions obey

    $ integral_(RR^3) C_(s)[f] dif^3 bold(v)=0 .$

    #derivation-step[Assemble the continuity equation]
    Substituting the four terms yields

    $ pdv(n_s,t)+div(n_s bold(u)_s)=0 .$

    Integrating this local equation over a finite spatial volume gives a rate
    of change equal to the negative outward particle flux. The local and
    integral forms are therefore the same conservation law.]
  )

  #rechenbeispiel[
    Context: a uniform singly ionized particle stream has
    $n_s=qty("1.0e16", "m^-3")$, normal speed
    $u_s=qty("2.0e5", "m/s")$, and reaches a planar collector of area
    $A=qty("1.0e-4", "m^2")$.

    Assumptions: steady source-free flow with the velocity normal to the
    collector.

    Target: report the particle flux $Gamma_s$ and the collection rate
    $dot(N)_s$.

    Numerical result: $Gamma_s=qty("2.0e21", "m^-2 s^-1")$ and
    $dot(N)_s=qty("2.0e17", "s^-1")$.
  ]

  #interpretation(
    [Eulerian reading of continuity],
    [The term $pdv(n_s,t)$ measures accumulation at a fixed position. The
    divergence $div(n_s bold(u)_s)$ measures net outward particle
    flux. If the flow converges, the divergence is negative and the density
    increases. This is the divergence of particle flux, which depends on
    both density and velocity. Even an incompressible velocity field can
    transport a density gradient past a fixed observer.]
  )

  #summary[
    The zeroth moment of a number-conserving kinetic equation is continuity.
    Velocity-space force transport contributes only a boundary flux, and
    ordinary collisions rearrange velocities without changing species number.
    Multiplication by mass or charge produces the corresponding continuity
    laws. Any source process must be added explicitly.
  ]

  #exam-prompts(
    (
      [(c) How do fluid equations follow from the Boltzmann equation? Perform the derivation for the continuity equation.],
    ),
    [Plasma Physics Exam.pdf, p. 2],
  )

  #knowledge-check((
    (
      question: [Which kinetic term becomes the particle flux in continuity?],
      answer: [The spatial streaming term becomes
      $div(integral bold(v) f_s dif^3 bold(v))
      =div(n_s bold(u)_s)$.]
    ),
    (
      question: [Why does the Lorentz force not create particles in the zeroth moment?],
      answer: [It transports the distribution through velocity space. Its
      divergence integrates to a boundary flux, which is zero when the
      distribution vanishes at infinite speed.]
    ),
    (
      question: [What changes in continuity if ionization is included?],
      answer: [A source term appears, for example
      $pdv(n_s,t)+div(n_s bold(u)_s)=S_s$. The source has the same
      density-per-time units as the left-hand side.]
    ),
    (
      question: [What does a negative divergence of particle flux imply locally?],
      answer: [With no source, $pdv(n_s,t)=-div(n_s bold(u)_s)$, so a negative
      flux divergence means positive local density accumulation.]
    ),
  ))

  #section-title[First moment and momentum transport] <moments-momentum>

  #lead[
    Number continuity tracks how many particles occupy a region. Momentum
    transport additionally records how directed motion and random motion move
    across its boundary and how electromagnetic forces change the momentum.
  ]

  #objectives((
    [derive the momentum equation by weighting the kinetic equation with $m_s bold(v)$],
    [separate directed momentum flux from the pressure tensor],
    [evaluate the Lorentz force moment],
    [interpret the collision moment as interspecies momentum exchange],
  ))

  #unit-ledger[
    The divergence of a pressure tensor and an electromagnetic force density
    are in #unit("N/m^3") $=$ #unit("kg m^-2 s^-2"). The Lorentz acceleration
    is $bold(a)_s=q_s/m_s (bold(E)+bold(v) times bold(B))$.
  ]

  #assumption(
    [Fields and velocity-space boundary],
    [The prescribed electromagnetic fields depend on $t$ and $bold(r)$, not
    on the velocity integration variable. The distribution and weighted
    velocity-space flux vanish at $abs(bold(v)) -> infinity$. Collisions may
    exchange momentum between species, so their first moment is retained as a
    source until species are summed.]
  )

  Multiply the conservative kinetic equation by $m_s bold(v)$ and integrate
  over velocity. The result is

  $ m_s integral bold(v) pdv(f_s,t) dif^3 bold(v)
    + m_s integral bold(v) div(bold(v) f_s) dif^3 bold(v)
    + m_s integral bold(v) div(f_s bold(a)_s) dif^3 bold(v)
    = m_s integral bold(v) C_(s)[f] dif^3 bold(v) $ <moments-first-integral>

  Define the collision momentum source

  $ bold(R)_s = m_s integral_(RR^3) bold(v) C_(s)[f] dif^3 bold(v) $ \
  <moments-collision-momentum>

  The time term is the time derivative of momentum density:

  $ m_s integral bold(v) pdv(f_s,t) dif^3 bold(v)
    = pdv(rho_s bold(u)_s,t) $ <moments-momentum-time>

  For the spatial term, move the divergence outside the velocity integral:

  $ m_s integral bold(v) div(bold(v) f_s) dif^3 bold(v)
    = div(m_s integral bold(v) bold(v) f_s dif^3 bold(v))
    = div(bold(M)_s) $ <moments-momentum-flux>

  Use the decomposition of the raw second moment from the first section:

  $ div(bold(M)_s)
    = div(rho_s bold(u)_s bold(u)_s + bold(P)_s) $ \
  <moments-momentum-flux-split>

  Integration by parts transfers the velocity derivative from the force flux
  to the weight $m_s bold(v)$; the assumed boundary decay removes the surface
  term. In components, with repeated Cartesian indices summed and
  $delta_(i j)$ equal to one for $i=j$ and zero otherwise,

  $ m_s integral v_i pdv((a_(s,j) f_s),v_j) dif^3 bold(v)
    = -m_s integral delta_(i j) a_(s,j) f_s dif^3 bold(v)
    = -m_s integral a_(s,i) f_s dif^3 bold(v) $ \
  <moments-force-integration>

  Therefore the force contribution on the right-hand side of the momentum
  balance is

  $ m_s integral bold(a)_s f_s dif^3 bold(v)
    = q_s n_s (bold(E) + bold(u)_s times bold(B)) $ \
  <moments-lorentz-force-density>

  The species momentum equation is consequently

  $ pdv(rho_s bold(u)_s,t)
    + div(rho_s bold(u)_s bold(u)_s + bold(P)_s)
    = q_s n_s (bold(E) + bold(u)_s times bold(B)) + bold(R)_s $ \
  <moments-momentum-equation>

  #equation-note[
    The pressure force density is $-div(bold(P)_s)$. In the
    fluid-following form, obtained with species continuity, the equation reads
    $rho_s (pdv(bold(u)_s,t)+bold(u)_s dot grad(bold(u)_s))
      = q_s n_s (bold(E)+bold(u)_s times bold(B))
      -div(bold(P)_s) + bold(R)_s$. Every term has force-density
    units in #unit("N/m^3"). The acceleration
    now follows a fluid element moving at $bold(u)_s$, not an
    individual particle moving at $bold(v)$. Pressure accounts for the
    momentum transport caused by their velocity difference.
  ]

  #details(
    [Derivation: the first moment term by term],
    [#derivation-step[Evaluate the time and streaming terms]
    Commute the time derivative with the velocity integral and use

    $ m_s integral bold(v) f_s dif^3 bold(v)=rho_s bold(u)_s .$

    For spatial streaming, the component identity is

    $ m_s integral v_i pdv((v_j f_s),x_j) dif^3 bold(v)
        =pdv((m_s integral v_i v_j f_s dif^3 bold(v)),x_j) .$

    This is the divergence of the raw second-moment tensor.

    #derivation-step[Integrate the force term by parts]
    For each component,

    $ m_s integral v_i pdv((a_(s,j)f_s),v_j) dif^3 bold(v)
        =m_s integral_("boundary") v_i a_(s,j)f_s d S_j
        -m_s integral pdv(v_i,v_j) a_(s,j)f_s dif^3 bold(v) .$

    The surface term vanishes and $pdv(v_i,v_j)=delta_(i j)$. The force term
    is therefore $-m_s integral a_(s,i) f_s dif^3 bold(v)$ on the left.

    #derivation-step[Insert the Lorentz acceleration]
    Move the force term to the right. Substitution of the Lorentz acceleration
    gives

    $ q_s bold(E) integral f_s dif^3 bold(v)
        +q_s (integral bold(v)f_s dif^3 bold(v)) times bold(B)
        =q_s n_s (bold(E)+bold(u)_s times bold(B)) .$

    #derivation-step[Split the momentum flux and use continuity]
    Insert $bold(v)=bold(u)_s+bold(w)_s$ into the raw second moment. The terms
    linear in $bold(w)_s$ vanish, leaving

    $ bold(M)_s=rho_s bold(u)_s bold(u)_s+bold(P)_s .$

    Finally use

    $ pdv(rho_s bold(u)_s,t)+div(rho_s bold(u)_s bold(u)_s)
        =rho_s (pdv(bold(u)_s,t)+bold(u)_s dot grad(bold(u)_s))
        +bold(u)_s (pdv(rho_s,t)+div(rho_s bold(u)_s)) .$

    The final bracket is zero by mass continuity, so the conservative equation
    becomes the species material-acceleration equation.]
  )

  #rechenbeispiel[
    Context: a uniform singly ionized hydrogen plasma has
    $n_i=qty("1.0e16", "m^-3")$, $q_i=e=qty("1.602e-19", "C")$,
    and an electric field $E=qty("6.00e4", "V/m")$ along $x$.

    Assumptions: neglect pressure gradients and magnetic forces, and use the
    electrostatic force density $f_(E,x)=n_i q_i E_x$.

    Target: report the $x$-directed electric force density.

    Numerical result: $f_(E,x)=qty("96.1", "N/m^3")$,
    equivalently $qty("96.1", "kg m^-2 s^-2")$.
  ]

  #interpretation(
    [Pressure is a momentum flux],
    [Particles with random
    velocities carry momentum across a surface, and the imbalance of that
    flux produces $-div(bold(P))$ in the momentum equation. Anisotropic
    velocity spread therefore produces a force that cannot generally be
    represented by the gradient of one scalar.]
  )

  #summary[
    Weighting the kinetic equation with $m_s bold(v)$ gives momentum density,
    raw momentum flux, Lorentz force density, and the first collision moment.
    The raw flux splits exactly into directed transport and pressure tensor.
    The collision term is not automatically zero for one species because
    collisions can transfer momentum between species.
  ]

  #knowledge-check((
    (
      question: [Which moment produces the pressure tensor in the momentum flux?],
      answer: [The raw second velocity moment produces
      $bold(M)_s=bold(P)_s+rho_s bold(u)_s bold(u)_s$. The central part is the
      random momentum flux.]
    ),
    (
      question: [Why does the magnetic part of the Lorentz force do no work but still affect momentum?],
      answer: [It is perpendicular to the instantaneous velocity, so it does
      no kinetic-energy work. It is nevertheless a directional force and
    appears in the momentum source $q_s n_s (bold(u)_s times bold(B))$.]
    ),
    (
      question: [When can the collision momentum sources cancel?],
      answer: [For internal binary collisions, summing over all participating
      species cancels equal and opposite momentum exchange. A single species
      equation generally retains $bold(R)_s$.]
    ),
    (
      question: [What approximation turns the pressure force into a scalar gradient?],
      answer: [Assume isotropy, $bold(P)_s=p_s bold(I)$. Then
      $div(bold(P)_s)=grad(p_s)$. Without isotropy the full tensor divergence is
      required.]
    ),
  ))

  #section-title[Second moment: energy and heat transport] <moments-energy>

  #lead[
    Contracting the second moment to a scalar gives kinetic-energy density.
    Some of that energy is in the bulk flow and some is in random motion.
    Their combined flux contains transport by the flow, pressure work, and
    heat carried relative to the moving fluid.
  ]

  #objectives((
    [derive the total kinetic-energy equation from the second moment],
    [decompose energy density and energy flux into bulk, pressure, and heat parts],
    [relate pressure-tensor divergence to scalar-pressure gradient under isotropy],
    [identify the next moment that prevents an exact finite fluid hierarchy],
  ))

  #unit-ledger[
    Energy density is in #unit("J/m^3") $=$ #unit("kg m^-1 s^-2"), and energy
    flux is in #unit("W/m^2") $=$ #unit("kg s^-3"). Heat flux $bold(q)_s$ is
    an energy flux. The scalar pressure $p_s$ has the same units as
    $bold(P)_s$. The ratio $gamma=5/3$ below is dimensionless and applies to a
    three-dimensional monatomic closure.
  ]

  #assumption(
    [Finite energy and decaying velocity tails],
    [Assume the distribution and all weighted velocity-space boundary fluxes
    vanish at infinity. The electromagnetic fields are independent of velocity.
    The energy collision moment may remain nonzero for one species because
    collisions can exchange thermal energy, even though total energy is
    conserved for a closed set of interacting species.]
  )

  Define the kinetic-energy density and its bulk and internal parts:

  $ W_s = (m_s/2) integral_(RR^3) abs(bold(v))^2 f_s dif^3 bold(v), quad
    epsilon_s = (sum_i (P_s)_(i i))/2, quad
    W_s = (rho_s abs(bold(u)_s)^2)/2 + epsilon_s $ \
  <moments-energy-density>

  Randomly moving particles also carry kinetic energy relative to the flow.
  Weighting their random velocity by that energy gives the heat-flux vector,
  a contraction of the mass-weighted third central tensor:

  $ bold(q)_s = (m_s/2) integral_(RR^3)
    abs(bold(w)_s)^2 bold(w)_s f_s dif^3 bold(v) $ \
  <moments-heat-flux>

  and the energy collision source is

  $ Q_s = (m_s/2) integral_(RR^3) abs(bold(v))^2 C_(s)[f] dif^3 bold(v) $ \
  <moments-energy-collision>

  Weight the kinetic equation by $(m_s abs(bold(v))^2)/2$. The time term is
  $pdv(W_s,t)$. The spatial term is the divergence of the raw energy flux

  $ bold(F)_s = (m_s/2) integral_(RR^3)
    abs(bold(v))^2 bold(v) f_s dif^3 bold(v) $ <moments-energy-flux>

  Integration by parts of the force term gives

  $ (m_s/2) integral abs(bold(v))^2
    div(f_s bold(a)_s) dif^3 bold(v)
    = -m_s integral bold(v) dot bold(a)_s f_s dif^3 bold(v) $ \
  <moments-energy-force>

  For Lorentz acceleration, $bold(v) dot (bold(v) times bold(B))=0$, so the
  force moment is electric work only. The conservative energy equation is

  $ pdv(W_s,t) + div(bold(F)_s)
    = q_s n_s bold(u)_s dot bold(E) + Q_s $ \
  <moments-energy-equation-raw>

  Decompose the energy flux with $bold(v)=bold(u)_s+bold(w)_s$:

  $ bold(F)_s = W_s bold(u)_s + bold(P)_s dot bold(u)_s + bold(q)_s $ \
  <moments-energy-flux-split>

  Thus the total kinetic-energy equation is

  $ pdv(W_s,t) + div(W_s bold(u)_s + bold(P)_s dot bold(u)_s + bold(q)_s)
    = q_s n_s bold(u)_s dot bold(E) + Q_s $ \
  <moments-energy-equation>

  #equation-note[
    The magnetic field does no direct work because it is perpendicular to
    $bold(v)$. The pressure work term is contained in
    $div(bold(P) dot bold(u))$. The heat flux is independent information: it
    transports random energy relative to the local bulk frame and is not fixed
    by $n_s$, $bold(u)_s$, and $bold(P)_s$ alone.
  ]

  The pressure tensor has scalar pressure

  $ p_s = (sum_i (P_s)_(i i))/3 $ <moments-scalar-pressure>

  as its isotropic part. If the distribution is isotropic in the local fluid
  frame, then

  $ bold(P)_s = p_s bold(I), quad
    div(bold(P)_s) = grad(p_s) $ \
  <moments-isotropic-pressure>

  In components, however,

  $ (div(bold(P)_s))_i
    = sum_j pdv((P_s)_(i j),x_j) $ <moments-pressure-divergence>

  so the scalar gradient is insufficient when anisotropy or shear is present.

  #details(
    [Derivation: energy density and energy flux decomposition],
    [#derivation-step[Weight the kinetic equation by particle energy]
    Multiply the kinetic equation by $(m_s v^2)/2$ and integrate. The time
    derivative gives $pdv(W_s,t)$. The spatial streaming term gives

    $ div((m_s/2) integral v^2 bold(v) f_s dif^3 bold(v)) .$

    #derivation-step[Evaluate the force work]
    Integrating the force term by parts in velocity gives

    $ (m_s/2) integral v^2 div(f_s bold(a)_s) dif^3 bold(v)
        =-(m_s/2) integral pdv(v^2,bold(v)) dot bold(a)_s f_s dif^3 bold(v)
        =-m_s integral bold(v) dot bold(a)_s f_s dif^3 bold(v) .$

    The magnetic force does no work because
    $bold(v) dot (bold(v) times bold(B))=0$. The remaining electric term is
    $-q_s bold(E) dot integral bold(v) f_s dif^3 bold(v)$ on the left. Move it
    to the right and use

    $ integral bold(v)f_s dif^3 bold(v)=n_s bold(u)_s .$

    #derivation-step[Split the energy flux]
    Use

    $ abs(bold(v))^2=abs(bold(u)_s)^2+2 bold(u)_s dot bold(w)_s
        +abs(bold(w)_s)^2, quad
      bold(v)=bold(u)_s+bold(w)_s .$

    The terms separate into bulk kinetic energy transported by
    $bold(u)_s$, internal energy transported by $bold(u)_s$, the pressure-work
    cross term

    $ m_s integral (bold(u)_s dot bold(w)_s) bold(w)_s f_s dif^3 bold(v)
        =bold(P)_s dot bold(u)_s ,$

    and the third central moment $bold(q)_s$. Terms with one unpaired
    $bold(w)_s$ vanish by the definition of the local mean. The total energy
    flux is

    $ bold(F)_s=W_s bold(u)_s+bold(P)_s dot bold(u)_s+bold(q)_s .$

    #derivation-step[Check the pressure divergence]
    In Cartesian components,

    $ (div(bold(P)_s))_i=sum_j pdv((P_s)_(i j),x_j) .$

    If $P_(i j)=p_s delta_(i j)$, the sum reduces to
    $pdv(p_s,x_i)$, which is $grad(p_s)$. A scalar pressure is therefore a
    special isotropic closure.]
  )

  #details(
    [Derivation: internal-energy balance],
    [#derivation-step[Form the bulk kinetic-energy balance]
    Dot the momentum equation with $bold(u)_s$ and use mass continuity. The
    bulk kinetic-energy balance is

    $ pdv((rho_s abs(bold(u)_s)^2)/2,t)
        +div((rho_s abs(bold(u)_s)^2 bold(u)_s)/2)
        +bold(u)_s dot div(bold(P)_s)
        =q_s n_s bold(u)_s dot bold(E)+bold(u)_s dot bold(R)_s .$

    #derivation-step[Rewrite the pressure work]
    The colon denotes a double contraction: multiply corresponding tensor
    components and sum both indices. Use the product identity

    $ bold(u)_s dot div(bold(P)_s)
        =div(bold(P)_s dot bold(u)_s)
        -bold(P)_s:grad(bold(u)_s) .$

    #derivation-step[Subtract from the total energy balance]
    Subtract the bulk equation from the total energy equation. The electric
    work cancels, while collisional momentum transfer contributes to the
    internal-energy source:

    $ pdv(epsilon_s,t)+div(epsilon_s bold(u)_s+bold(q)_s)
        +bold(P)_s:grad(bold(u)_s)
        =Q_s-bold(u)_s dot bold(R)_s .$

    #derivation-step[Apply the isotropic adiabatic closure]
    For an isotropic three-dimensional pressure tensor,

    $ epsilon_s=(3 p_s)/2, quad
      bold(P)_s:grad(bold(u)_s)=p_s div(bold(u)_s) .$

    With no heat flux and no net collisional internal heating, this becomes

    $ pdv(p_s,t)+bold(u)_s dot grad(p_s)
        +(5 p_s)/3 div(bold(u)_s)=0 .$

    This is the adiabatic pressure law used by one common warm-fluid closure;
    retaining anisotropy or heat flux requires the unclosed tensor equation.]
  )

  #rechenbeispiel[
    Context: an isotropic hydrogen-ion population has
    $n_i=qty("1.0e16", "m^-3")$, $m_i=qty("1.673e-27", "kg")$,
    $k_B T_i=qty("1.602e-18", "J")$ ($qty("10", "eV")$), and bulk speed
    $u_i=qty("1.0e5", "m/s")$.

    Assumptions: Maxwellian random motion, isotropic pressure, and the
    three-dimensional kinetic-energy definitions used above.

    Target: report the internal energy density $epsilon_i$, bulk kinetic-energy
    density, and total kinetic-energy density $W_i$.

    Numerical result: $epsilon_i=qty("0.0240", "J/m^3")$,
    $W_("bulk",i)=qty("0.0836", "J/m^3")$, and
    $W_i=qty("0.108", "J/m^3")$.
  ]

  #interpretation(
    [Open moment hierarchy],
    [The continuity equation needs the first moment. The momentum equation
    needs the second moment. The scalar energy equation needs the contracted
    third central moment $bold(q)_s$; evolving a general anisotropic pressure
    tensor requires the full third central tensor. Its evolution introduces
    fourth moments. Exact kinetic information therefore generates an infinite moment
    hierarchy. A finite fluid system exists only after a constitutive closure.]
  )

  #summary[
    The second moment gives energy density and an energy flux made of bulk
    energy transport, pressure work, and heat flux. The magnetic field does no
    kinetic-energy work, while the electric field supplies power. Scalar
    pressure is equivalent to the pressure tensor only under isotropy. The
    third central moment is the first omitted variable in a pressure-based
    fluid model.
  ]

  #exam-prompts(
    (
      [(d) Give the key steps of the derivation of momentum and heat transport equation.],
      [(e) How are pressure tensor and scalar pressure and their divergence/gradient related?],
    ),
    [Plasma Physics Exam.pdf, p. 3],
  )

  #knowledge-check((
    (
      question: [Which field supplies power in the species energy equation?],
      answer: [The electric field supplies $q_s n_s bold(u)_s dot bold(E)$.
      The magnetic force is perpendicular to the particle velocity and does no
      direct work.]
    ),
    (
      question: [What physical transport does $bold(q)_s$ represent?],
      answer: [It is the energy flux carried by random motion in the local
      bulk frame, $(m_s/2) integral abs(bold(w)_s)^2 bold(w)_s f_s dif^3 bold(v)$.]
    ),
    (
      question: [When may $grad(p_s)$ replace $div(bold(P)_s)$?],
      answer: [Only when $bold(P)_s=p_s bold(I)$ is isotropic. Anisotropic or
      sheared distributions require the full tensor divergence.]
    ),
    (
      question: [Why is the energy equation not the end of the exact hierarchy?],
      answer: [Its flux contains the third central moment $bold(q)_s$. The
      transport equation for that heat flux introduces a fourth moment, so a
      finite model needs closure.]
    ),
  ))

  #section-title[Cold and warm closures] <moments-closures>

  #lead[
    A fluid description becomes predictive only after it specifies the first
    omitted moment. Cold and warm plasma models make different choices about
    pressure and energy transport, while collisional models choose how velocity
    space relaxes toward equilibrium.
  ]

  #objectives((
    [state what is retained in cold and warm plasma models],
    [write an empirical BGK collision model and identify its moment sources],
    [distinguish species exchange from total conservation],
    [close the hierarchy with an equation of state or a polytropic law],
  ))

  #unit-ledger[
    The Maxwellian reference $f_(M,s)$ has the units of $f_s$,
    #unit("s^3 m^-6"). The collision operator has units of distribution per
    time, #unit("s^2 m^-6"). Closure parameters such as $gamma$, the Knudsen
    number, and $nu_s tau$ are dimensionless.
  ]

  #definition(
    [Closure],
    [A closure is a constitutive relation or distributional assumption that
    expresses an unretained moment in terms of retained fields. It supplies
    information that cannot be recovered from the retained moment equations
    alone.]
  )

  The hierarchy may be written schematically as

  $ f_s -> (n_s, bold(u)_s, bold(P)_s) -> bold(q)_s ->
    "fourth moment" -> dots $ <moments-hierarchy-chain>

  The cold-plasma closure sets random momentum transport to zero:

  $ bold(P)_s = bold(0), quad bold(q)_s = bold(0) $ \
  <moments-cold-closure>

  It is the formal zero-temperature limit in which all particles of a species
  share one local velocity. It can be useful when thermal speed is small
  compared with the flow or wave speed, but it cannot describe pressure
  balance, thermal conduction, or pressure-driven waves.

  A warm isotropic model retains a scalar pressure:

  $ bold(P)_s = p_s bold(I), quad epsilon_s=(3 p_s)/2 $ \
  <moments-warm-isotropic>

  and must supply one additional relation. Examples include an isothermal
  equation of state and an adiabatic or polytropic law:

  $ p_s = n_s k_B T_s quad (T_s "prescribed"), quad
    p_s n_s^(-gamma) = "constant along a fluid path" $ \
  <moments-closures-examples>

  For a source-free, heat-flux-free three-dimensional monatomic fluid, the
  second relation is equivalently

  $ pdv(p_s,t) + bold(u)_s dot grad(p_s)
    + gamma p_s div(bold(u)_s) = 0, quad gamma=5/3 $ \
  <moments-polytropic-law>

  This pressure law closes the model without evolving heat flux as an
  independent variable. It describes compression with no heat transport or
  internal heating under the stated isotropic assumptions. An isothermal
  closure instead holds temperature fixed, so compression requires energy
  exchange to maintain that temperature.

  #definition(
    [BGK relaxation model],
    [The Bhatnagar--Gross--Krook (BGK) model replaces the detailed collision
    integral by relaxation toward a local Maxwellian:
    $C_("BGK")[f_s] = -nu_s (f_s-f_(M,s))$. Here $nu_s$ is a model collision
    frequency and $f_(M,s)$ is chosen to share selected local moments with
    $f_s$. The model is useful for explaining relaxation and for constructing
    reduced calculations, but its conservation properties depend on which
    moments are matched.]
  )

  #equation-note[
    If $f_(M,s)$ has the same density as $f_s$, then
    $integral C_("BGK")[f_s] dif^3 bold(v)=0$. If it also has the same flow and
    energy moments, the corresponding momentum and energy collision moments
    vanish for that single-species model. In a multispecies plasma, physical
    interspecies collisions may still exchange momentum and energy between
    species even though the total exchange sums to zero.
  ]

  #details(
    [Derivation: where the collision term remains],
    [#derivation-step[Define the collision moments]
    For a general collision operator, the number, momentum, and energy sources
    are respectively

    $ S_("N,s")=integral C_(s)[f] dif^3 bold(v), quad
      bold(R)_s=m_s integral bold(v) C_(s)[f] dif^3 bold(v), quad
      Q_s=(m_s/2) integral v^2 C_(s)[f] dif^3 bold(v) .$

    Ordinary elastic collisions within one species have
    $S_("N,s")=0$. Interspecies collisions can give nonzero
    $bold(R)_s$ and $Q_s$ for each species.

    #derivation-step[Apply total conservation]
    For an isolated elastic system, summing over all collision partners gives

    $ sum_s bold(R)_s=bold(0), quad
      sum_s Q_s=0 .$

    Individual species equations may still contain exchange terms; only the
    total balance removes them.

    #derivation-step[Inspect the BGK example]
    For BGK relaxation, substitute

    $ C_("BGK")[f_s]=-nu_s dot (f_s-f_(M,s)) .$

    Matching the density makes the zeroth moment zero. Matching density, flow,
    and temperature additionally makes the first and second collision moments
    zero. If a background is fixed or only number is matched, the remaining
    moments represent momentum or energy exchange with that background.

    The collision term therefore disappears from a moment equation only after
    a conservation or closure condition justifies that step.]
  )

  #callout(
    [Cold and warm model assumptions],
    [“Warm” means that a pressure or temperature scale is retained, not that
    the distribution must be exactly Maxwellian. “Cold” means that pressure
    forces are neglected in the selected equations, not that electromagnetic
    forces or all kinetic effects vanish. The validity of either model is a
    scale-ordering statement.]
  )

  #rechenbeispiel[
    Context: a warm isotropic closure follows a polytropic law with
    $gamma=5/3$. The density changes from $n_0$ to
    $n_1=8 n_0$.

    Assumptions: source-free adiabatic compression with
    $p n^(-gamma)$ constant along the fluid path.

    Target: report the pressure ratio $p_1/p_0$ and temperature ratio
    $T_1/T_0$.

    Numerical result: $p_1/p_0=32$ and $T_1/T_0=4$; both ratios are
    dimensionless.
  ]

  #interpretation(
    [Choosing a closure],
    [Use a cold closure when thermal pressure is asymptotically small for the
    phenomenon of interest. Use an isotropic warm closure when collisions or
    another isotropization mechanism erase directional pressure differences
    and an equation of state is credible. Gyrophase mixing only removes
    dependence on the angle around $bold(B)$: a gyrotropic distribution can
    still have $p_parallel != p_perp$. Retain both pressures, a general tensor,
    or return to
    kinetic theory when anisotropy, heat flux, resonances, or boundary layers
    are dynamically important.]
  )

  #summary[
    The moment equations are exact until a closure is introduced. Cold models
    set pressure transport to zero. Warm models retain pressure and then choose
    an equation of state, energy law, or pressure tensor model. BGK is an
    empirical collision operator whose moments vanish only when its reference
    state is matched appropriately. Species exchange can remain nonzero even
    when total momentum and energy are conserved.
  ]

  #exam-prompts(
    (
      [(f) How can one empirically model the collision term? In which equations does it stay or disappear and why?],
      [(g) What is the difference between cold and warm plasma model?],
      [(h) How can one close the hierarchy of fluid equations to avoid requiring a heat transport law?],
    ),
    [Plasma Physics Exam.pdf, p. 3],
  )

  #knowledge-check((
    (
      question: [What does the cold closure remove from the momentum equation?],
      answer: [It sets $bold(P)_s=bold(0)$, so the pressure force
      $-div(bold(P)_s)$ is absent. It does not remove the Lorentz force.]
    ),
    (
      question: [Which BGK matching condition guarantees number conservation?],
      answer: [Choose $f_(M,s)$ with the same density as $f_s$. Then the
      velocity integral of $C_("BGK")$ is zero.]
    ),
    (
      question: [Why can a collision term vanish in total momentum but remain in a species equation?],
      answer: [Interspecies collisions transfer equal and opposite momentum.
      The species sources are nonzero, but their sum is zero for an isolated
      elastic system.]
    ),
    (
      question: [Give one closure that avoids a separate heat-transport law and state its assumption.],
      answer: [A polytropic law $p_s n_s^(-gamma)="constant"$ along a fluid path
      closes pressure using density. It assumes a prescribed effective energy
      response, such as adiabatic compression when $gamma=5/3$.]
    ),
  ))

  #chapter-nav(
    previous: (href: "05-kinetic-theory.html", title: [Kinetic theory]),
    next: (href: "07-multiple-fluids.html", title: [Multiple fluids]),
  )
]
