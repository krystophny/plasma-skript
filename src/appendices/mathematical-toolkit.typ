#import "../theme.typ": *
#import "@preview/physica:0.9.8": div, grad, curl, pdv, dv, laplacian
#import "@preview/unify:0.8.1": unit

#let appendix = [
  #page-title[Appendix: Mathematical toolkit] <mathematical-toolkit>

  #lead[
    The course repeatedly moves between kinetic, fluid, and field
    descriptions. This appendix collects the energy-weighted second moment
    of the kinetic equation and the differential operators used in Cartesian,
    cylindrical, and spherical coordinates, with collapsed derivations for
    reconstructing each result.
  ]

  #callout(
    [Checklist for compact plasma equations],
    [Before manipulating a compact plasma equation, identify the species,
    the integration measure, the active unit convention, the coordinate scale
    factors, and the boundary terms. Most apparent sign or missing-factor
    errors can be found at one of those five checkpoints.]
  )

  #section-title[Energy-weighted second moment] <second-moment-toolkit>

  #lead[
    How does the kinetic equation produce an energy equation? Weighting by
    the single-particle kinetic energy and integrating over velocity converts
    velocity-space transport into electromagnetic work, spatial transport,
    and collisional energy exchange. The result is the bridge between a
    distribution function and the fluid energy equations used later in the
    script.
  ]

  #objectives((
    [define the bulk, internal, and heat-flux contributions to a species energy moment],
    [carry out the velocity-space integration by parts without dropping the boundary condition],
    [identify why the magnetic part of the Lorentz force does no work],
    [separate the total-energy equation from the internal-energy equation],
  ))

  #unit-ledger[
    The species distribution is defined by $d N_s=f_(s) dif^3 bold(r) dif^3
    bold(v)$. The energy density and energy flux below are in #unit("J m^-3")
    and #unit("W m^-2"), respectively.
  ]

  #assumption(
    [Kinetic equation and velocity-space boundary],
    [For species $s$, use a smooth kinetic equation with acceleration
    $bold(a)_s=(q_s\/m_s)(bold(E)+bold(v) times bold(B))$. The distribution
    and the velocity-space flux $f_(s) bold(a)_s$ vanish sufficiently rapidly
    as $abs(bold(v)) -> infinity$, so surface terms at infinite speed are
    zero. Require species-number-conserving collisions,

    $ integral C_(s)[f] dif^3 bold(v)=0 , $

    so
    $pdv(rho_s,t, style: "horizontal")+div(rho_s bold(u)_s)=0$. Ionization and recombination
    are excluded from the internal-energy balance below.
    Collisions may exchange energy between species, but their weighted
    integral is retained as a source.]
  )

  #definition(
    [Bulk and thermal variables],
    [The species flow velocity and random velocity are

    $ bold(u)_s=(integral bold(v) f_(s) dif^3 bold(v))/(n_s) $

    and
    $bold(c)_s=bold(v)-bold(u)_s$. Define the bulk kinetic-energy density,
    internal-energy density, pressure tensor, and heat-flux vector by
    $K_s=rho_s abs(bold(u)_s)^2\/2$,
    $U_s=tr bold(P)_s\/2$,

    $ bold(P)_s=m_s integral bold(c)_s bold(c)_s f_(s) dif^3 bold(v) , quad "and" quad
      bold(q)_s=(m_s integral abs(bold(c)_s)^2 bold(c)_s f_(s) dif^3 bold(v))/2 . $

    Here $bold(c)_s bold(c)_s$ is a dyadic product. The total second moment is

    $ W_s=K_s+U_s=(m_s integral abs(bold(v))^2 f_(s) dif^3 bold(v))/2 . $

    For a collision operator $C_(s)[f]$, define the collisional momentum
    transfer and kinetic-energy transfer by

    $ bold(R)_s=m_s integral bold(v) C_(s)[f] dif^3 bold(v) quad "and" quad
      Q_(s)=(m_s integral abs(bold(v))^2 C_(s)[f] dif^3 bold(v))/2 . $

    The source $bold(R)_s$ is in #unit("N m^-3") and $Q_(s)$ is in
    #unit("W m^-3").]
  )

  #governing-law(
    [Species total-energy equation],
    [The energy-weighted kinetic equation gives

    $ pdv(W_s,t)+div((W_s) bold(u)_s+bold(P)_s dot bold(u)_s+bold(q)_s)
      =q_s n_s bold(E) dot bold(u)_s+Q_(s) , $

    where $Q_(s)$ is the collisional rate of kinetic-energy transfer to
    species $s$ in #unit("W m^-3"). The magnetic force is absent from
    the power term because $bold(v) dot (bold(v) times bold(B))=0$.]
  )

  #equation-note[
    The three terms in the energy flux have distinct meanings: advection of
    total particle kinetic energy $W_s bold(u)_s$ (bulk plus internal),
    pressure work transport $bold(P)_s dot
    bold(u)_s$, and random-energy transport $bold(q)_s$. They must not be
    merged into a scalar heat flux unless isotropy and a closure have been
    stated.
  ]

  #callout(
    [Derivation route],
    [Multiply the kinetic equation by $m_s abs(bold(v))^2\/2$, integrate over
    all velocity space, commute time and space derivatives with the integral,
    integrate the acceleration term by parts in velocity, then decompose
    $bold(v)=bold(u)_s+bold(c)_s$. The collapsed derivation gives each step
    and the boundary terms.]
  )

  #details(
    [Derivation: total energy from the kinetic equation],
    [#derivation-step[Weight the kinetic equation]
    Start from the non-conservative form

    $ pdv(f_(s),t)+bold(v) dot grad(f_(s))
      +bold(a)_s dot pdv(f_(s),bold(v))=C_(s)[f] . $

    Since $bold(v)$ is independent of $bold(r)$, the streaming term is also
    $div(f_(s) bold(v))$. Define the single-particle kinetic energy

    $ epsilon_(s)(bold(v))=(m_s abs(bold(v))^2)/2 . $

    Multiply the kinetic equation by this energy and integrate over all
    velocity space:

    $ integral epsilon_(s) pdv(f_(s),t) dif^3 bold(v)
      +integral epsilon_(s) div(f_(s) bold(v)) dif^3 bold(v)
      +integral epsilon_(s) bold(a)_s dot pdv(f_(s),bold(v)) dif^3 bold(v)
      =integral epsilon_(s) C_(s)[f] dif^3 bold(v) . $

    #derivation-step[Evaluate the temporal and streaming terms]
    The temporal term is

    $ integral epsilon_(s) pdv(f_(s),t) dif^3 bold(v)
      =pdv(integral epsilon_(s) f_(s) dif^3 bold(v),t)=pdv(W_s,t) . $

    The streaming term commutes with the velocity integral:

    $ integral epsilon_(s) div(f_(s) bold(v)) dif^3 bold(v)
      =div((m_s integral abs(bold(v))^2 bold(v) f_(s) dif^3 bold(v))/2) . $

    #derivation-step[Integrate the acceleration term by parts]
    Write the contracted velocity divergence explicitly as

    $ div_(bold(v))(bold(A))=sum_j pdv(A_(j),v_(j)) . $

    The velocity-space product rule is

    $ epsilon_(s) bold(a)_s dot pdv(f_(s),bold(v))
      =div_(bold(v))(epsilon_(s) f_(s) bold(a)_s)
        -f_(s) bold(a)_s dot pdv(epsilon_(s),bold(v))
        -epsilon_(s) f_(s) div_(bold(v))(bold(a)_s) . $

    For the Lorentz acceleration, $div_(bold(v))(bold(a)_s)=0$:
    the electric field is independent of velocity and the magnetic linear
    map is antisymmetric, hence has zero trace. The last term therefore
    vanishes.

    The first term becomes the surface integral

    $ integral_("boundary V_v") epsilon_(s) f_(s) bold(a)_s
      dot d bold(S)_v , $

    which vanishes at infinite speed by the boundary assumption. Because
    $pdv(epsilon_(s),bold(v), style: "horizontal")=m_s bold(v)$, the remaining term is

    $ -m_s integral f_(s) bold(a)_s dot bold(v) dif^3 bold(v) . $

    Insert the Lorentz acceleration. The magnetic contribution vanishes
    pointwise, leaving

    $ -q_s bold(E) dot integral bold(v) f_(s) dif^3 bold(v)
      =-q_s n_s bold(E) dot bold(u)_s . $

    Define the collision power

    $ Q_(s)=integral epsilon_(s) C_(s)[f] dif^3 bold(v) . $

    Moving the electric term to the right gives the conservative energy
    equation

    $ pdv(W_s,t)+div((m_s integral abs(bold(v))^2 bold(v) f_(s)
      dif^3 bold(v))/2)=q_s n_s bold(E) dot bold(u)_s+Q_(s) . $

    #derivation-step[Decompose the energy flux]
    Substitute

    $ bold(v)=bold(u)_s+bold(c)_s $ \
    $ abs(bold(v))^2=abs(bold(u)_s)^2+2 bold(u)_s dot bold(c)_s
      +abs(bold(c)_s)^2 . $

    The first-order random moment vanishes:

    $ integral bold(c)_s f_(s) dif^3 bold(v)=bold(0) . $

    The surviving flux terms are

    $ (m_s integral abs(bold(v))^2 bold(v) f_(s) dif^3 bold(v))/2
      =K_s bold(u)_s+U_s bold(u)_s+bold(P)_s dot bold(u)_s+bold(q)_s . $

    Since $W_s=K_s+U_s$, this becomes

    $ W_s bold(u)_s+bold(P)_s dot bold(u)_s+bold(q)_s . $

    Substitution gives the stated total-energy equation.]
  )

  #governing-law(
    [Internal-energy equation],
    [Subtracting the bulk kinetic-energy equation obtained by dotting the
    species momentum equation with $bold(u)_s$ gives

    $ pdv(U_s,t)+div(U_s bold(u)_s+bold(q)_s)
      =-bold(P)_s:grad(bold(u)_s)+Q_(s)
      -bold(u)_s dot bold(R)_s . $

    The double contraction is

    $ bold(P)_s:grad(bold(u)_s)
      =sum_(i,j) (P_s)_(i j) pdv((u_s)_(i),r_(j)) . $

    For an isotropic pressure tensor $bold(P)_s=p_s bold(I)$, the pressure
    work reduces to $p_s div(bold(u)_s)$ and
    $U_s=3 p_s\/2$ in three spatial dimensions.]
  )

  #details(
    [Derivation: subtract bulk energy and identify pressure work],
    [#derivation-step[Start from the momentum balance]
    The first moment of the kinetic equation is

    $ pdv(rho_s bold(u)_s,t)+div(rho_s bold(u)_s bold(u)_s+bold(P)_s)
        =q_s n_s (bold(E)+bold(u)_s times bold(B))+bold(R)_s . $

    Dot this equation with $bold(u)_s$. The number-conserving assumption
    gives $pdv(rho_s,t, style: "horizontal")+div(rho_s bold(u)_s)=0$, so the product rule yields

    $ pdv(K_s,t)+div(K_s bold(u)_s)
        =q_s n_s bold(E) dot bold(u)_s
        -bold(u)_s dot div(bold(P)_s)
        +bold(u)_s dot bold(R)_s . $

    #derivation-step[Subtract bulk energy from total energy]
    The total-energy equation contains the same electromagnetic power. Insert
    $W_s=K_s+U_s$ and subtract the bulk identity:

    $ pdv(U_s,t)+div(U_s bold(u)_s+bold(P)_s dot bold(u)_s+bold(q)_s)
        =bold(u)_s dot div(bold(P)_s)
        +Q_(s)-bold(u)_s dot bold(R)_s . $

    #derivation-step[Rewrite pressure work]
    Apply

    $ div(bold(P)_s dot bold(u)_s)
        =bold(u)_s dot div(bold(P)_s)
        +bold(P)_s:grad(bold(u)_s) . $

    The first term cancels, leaving the internal-energy equation with pressure
    work and heat-flux transport. For $bold(P)_s=p_s bold(I)$,

    $ bold(P)_s:grad(bold(u)_s)=p_s div(bold(u)_s) . $

    This is the isotropic limit.]
  )

  #interpretation(
    [Content of the second-moment equations],
    [The total-energy equation tracks directed and random kinetic energy
    together. The internal form isolates compressional work, anisotropic shear
    work, and heat-flux transport. A fluid model closes this equation only
    after choosing how $bold(P)_s$, $bold(q)_s$, and $Q_(s)$ are represented.
    When $C_(s)[f]=0$, both $Q_(s)=0$ and $bold(R)_s=bold(0)$ for each
    species. Energy exchange with the fields enters through electric work,
    not a collision source. For collisional species exchange, the internal source is
    $Q_(s)-bold(u)_s dot bold(R)_s$: total collisional power and bulk momentum
    transfer must be separated.]
  )

  #summary[
    Weighting the kinetic equation by $m_s abs(bold(v))^2\/2$ gives a total
    energy balance. Velocity-space integration by parts turns the Lorentz
    force into electric work; the magnetic part does no work. Decomposing
    velocity into bulk plus random motion separates total-energy advection, pressure
    work, and heat-flux transport. Representing $bold(P)_s$ and $bold(q)_s$
    in terms of lower moments is a closure choice.
  ]

  #knowledge-check((
    (
      question: [Why does the magnetic part of the Lorentz force not appear in the single-species energy source?],
      answer: [Its power is proportional to $bold(v) dot (bold(v) times bold(B))$, which is zero for every particle. The electric part contributes $q_s n_s bold(E) dot bold(u)_s$ in #unit("W m^-3").],
    ),
    (
      question: [Which term transports random kinetic energy relative to the species flow?],
      answer: [The heat-flux vector

      $ bold(q)_s=(m_s integral abs(bold(c)_s)^2 bold(c)_s f_(s) dif^3 bold(v))/2 $

      transports random energy. It is a third central velocity moment and needs a closure in a truncated fluid model.],
    ),
    (
      question: [What assumption removes the velocity-space surface term in the energy derivation?],
      answer: [The distribution and velocity-space flux must decay fast enough that the surface integral at $abs(bold(v)) -> infinity$ vanishes. If a high-energy boundary or source is present, that flux must be retained.],
    ),
    (
      question: [How does isotropic pressure simplify the internal-energy equation?],
      answer: [With $bold(P)_s=p_s bold(I)$, the tensor contraction becomes $bold(P)_s:grad(bold(u)_s)=p_s div(bold(u)_s)$ and the internal energy is $U_s=3p_s\/2$ in three dimensions.],
    ),
  ))

  #section-title[Vector operators and coordinate geometry] <vector-toolkit>

  #lead[
    Plasma equations are often simplest in the coordinates selected by the
    geometry: Cartesian coordinates for a local wave, cylindrical coordinates
    for a column or pinch, and spherical coordinates for a nearly isotropic
    expansion. The physical vector is unchanged by the coordinate choice, but
    the basis vectors and area elements vary. Where do the extra factors of
    $r$ and $sin(theta)$ come from? They are metric scale factors, not new
    physics.
  ]

  #objectives((
    [state the gradient, divergence, curl, and scalar Laplacian in orthogonal coordinates],
    [specialize the formulas to Cartesian, cylindrical, and spherical systems],
    [use a divergence or curl identity as a dimensional and limiting-case check],
    [choose coordinates that expose the symmetry of a plasma configuration],
  ))

  #unit-ledger[
    Coordinates $x,y,z,r$ are lengths in #unit("m"), angles $phi$ and $theta$
    are dimensionless, and a scalar field $psi$ and vector field $bold(A)$
    retain whatever physical units the model assigns. Thus $grad(psi)$ has
    units of $psi$ per #unit("m"), $div(bold(A))$ has units of $bold(A)$ per
    #unit("m"), and $curl(bold(A))$ has the same units. The formulas below are
    dimensional coordinate identities; no normalized radius is implied.
  ]

  #assumption(
    [Orthogonal curvilinear coordinates],
    [Let $(q_1,q_2,q_3)$ be right-handed orthogonal coordinates with unit basis vectors
    $bold(e)_(1)$, $bold(e)_(2)$, and $bold(e)_(3)$. Define scale factors by
    $d bold(r)=sum_i h_i d q_i bold(e)_(i)$. The basis is orthonormal at each
    point, but it may vary with position. Components $A_(i)$ are physical
    components along the local unit vectors, not covariant components.]
  )

  #definition(
    [Metric scale factors],
    [The scale factors $h_i$ convert coordinate increments to physical line
    elements. The three systems used most often here are

    $ "Cartesian:" (q_1,q_2,q_3)=(x,y,z), (h_1,h_2,h_3)=(1,1,1) , $

    $ "cylindrical:" (q_1,q_2,q_3)=(r,phi,z), (h_1,h_2,h_3)=(1,r,1) , $

    and

    $ "spherical:" (q_1,q_2,q_3)=(r,theta,phi),
      (h_1,h_2,h_3)=(1,r,r sin(theta)) . $

    In spherical coordinates $theta$ is the polar angle from positive $z$,
    and $phi$ is the azimuth measured from positive $x$ toward positive $y$.
    The volume element is $dif V=h_1 h_2 h_3 dif q_1 dif q_2 dif q_3$.]
  )

  #governing-law(
    [Orthogonal-coordinate operators],
    [For a scalar $psi$ and vector
    $bold(A)=sum_i A_(i) bold(e)_(i)$, the operators are

    $ grad(psi)=sum_i (bold(e)_(i)/h_i) pdv(psi,q_i) , $

    $ div(bold(A))=(sum_i pdv((h_j h_k A_(i)),q_i))/(h_1 h_2 h_3) , $

    where $(i,j,k)$ cycles through $(1,2,3)$, and

    $ curl(bold(A))=sum_i (bold(e)_(i)/(h_j h_k))
      (pdv(h_k A_(k),q_j)-pdv(h_j A_(j),q_k)) . $

    The scalar Laplacian is

    $ laplacian(psi)=(sum_i pdv(((h_j h_k)/h_i) pdv(psi,q_i),q_i))/(h_1 h_2 h_3) . $

    Each derivative is with respect to the displayed coordinate, while the
    scale factors account for physical distance and area.]
  )

  #equation-note[
    In the cyclic formulas, for the component with index $i$, the remaining
    indices $(j,k)$ are taken in cyclic order. For example, the first curl
    component is

    $ (pdv(h_3 A_(3),q_2)-pdv(h_2 A_(2),q_3))/(h_2 h_3) . $

    Writing the scale factors explicitly is safer than importing a Cartesian
    formula and inserting $r$ by intuition.
  ]

  #callout(
    [Coordinate choice is a symmetry choice],
    [A straight, locally uniform wave naturally uses Cartesian components. A
    cylindrical pinch makes $A_(phi)$ and $B_(z)$ natural components, while a
    spherically expanding plasma makes the area factor $4 pi r^2$ visible in
    a divergence. The operator does not change the physical conservation law;
    only its coordinate representation changes.]
  )

  #details(
    [Derivation: origin of the scale factors],
    [#derivation-step[Derive the gradient components]
    The directional differential of a scalar field is

    $ d psi=grad(psi) dot d bold(r)
        =sum_i (grad(psi))_(i) h_i d q_i . $

    The chain rule gives $d psi=sum_i pdv(psi,q_i, style: "horizontal") d q_i$. Comparing
    coefficients yields

    $ (grad(psi))_(i)=pdv(psi,q_i)/(h_i) . $

    #derivation-step[Derive the divergence]
    A small coordinate cell has physical volume

    $ dif V=h_1 h_2 h_3 dif q_1 dif q_2 dif q_3 . $

    The outward flux through the pair of faces normal to $bold(e)_(1)$ is the
    difference of $h_2 h_3 A_(1)$ at the two faces, multiplied by
    $dif q_2 dif q_3$. Cyclic permutations give the other faces. Divide the
    total flux by $dif V$:

    $ div(bold(A))=(pdv(h_2 h_3 A_(1),q_1)
        +pdv(h_3 h_1 A_(2),q_2)
        +pdv(h_1 h_2 A_(3),q_3))/(h_1 h_2 h_3) . $

    #derivation-step[Derive curl and the Laplacian]
    Circulation around the face normal to $bold(e)_(1)$ gives

    $ (curl(bold(A)))_(1)
        =(pdv(h_3 A_(3),q_2)-pdv(h_2 A_(2),q_3))/(h_2 h_3) . $

    Cyclic permutation gives the other components. Finally insert
    $laplacian(psi)=div(grad(psi)):$

    $ laplacian(psi)=
        (sum_i pdv(((h_j h_k)/h_i) pdv(psi,q_i),q_i))/(h_1 h_2 h_3) . $

    The scale factors must be differentiated whenever they vary with
    position; otherwise physical flux and circulation are misrepresented.]
  )

  #definition(
    [Cartesian specialization],
    [For $(x,y,z)$, all scale factors are one:

    $ grad(psi)=bold(e)_x pdv(psi,x)+bold(e)_y pdv(psi,y)+bold(e)_z pdv(psi,z) , $

    $ div(bold(A))=pdv(A_(x),x)+pdv(A_(y),y)+pdv(A_(z),z) , $

    and

    $ laplacian(psi)=pdv(psi,x,2)+pdv(psi,y,2)+pdv(psi,z,2) . $

    The Cartesian curl is

    $ curl(bold(A))=bold(e)_x [pdv(A_(z),y)-pdv(A_(y),z)]
      +bold(e)_y [pdv(A_(x),z)-pdv(A_(z),x)]
      +bold(e)_z [pdv(A_(y),x)-pdv(A_(x),y)] . $

    These are the local forms used in most linear wave derivations.]
  )

  #definition(
    [Cylindrical specialization],
    [For $(r,phi,z)$, the physical line element is
    $d bold(r)=d r bold(e)_(r)+r d phi bold(e)_(phi)+d z bold(e)_(z)$.
    Therefore

    $ grad(psi)=bold(e)_(r) pdv(psi,r)+(bold(e)_(phi)/r) pdv(psi,phi)+bold(e)_(z) pdv(psi,z) , $

    $ div(bold(A))=(pdv(r A_(r),r))/r+(pdv(A_(phi),phi))/r+pdv(A_(z),z) , $

    and

    $ laplacian(psi)=(pdv(r pdv(psi,r),r))/r+pdv(psi,phi,2)/(r^2)+pdv(psi,z,2) . $

    In an axisymmetric state $pdv(psi,phi, style: "horizontal")=0$, so the cylindrical area factor
    remains in the radial divergence even though the azimuthal derivative
    disappears.]
  )

  #definition(
    [Spherical specialization],
    [For $(r,theta,phi)$, the physical line element is

    $ d bold(r)=d r bold(e)_(r)+r d theta bold(e)_(theta)
      +r sin(theta) d phi bold(e)_(phi) . $

    The gradient and divergence are

    $ grad(psi)=bold(e)_(r) pdv(psi,r)+(bold(e)_(theta)/r) pdv(psi,theta)
      +(bold(e)_(phi)/(r sin(theta))) pdv(psi,phi) , $

    $ div(bold(A))=(pdv(r^2 A_(r),r))/(r^2)
      +(pdv(sin(theta) A_(theta),theta))/(r sin(theta))
      +(pdv(A_(phi),phi))/(r sin(theta)) , $

    and the scalar Laplacian is

    $ laplacian(psi)=(pdv(r^2 pdv(psi,r),r))/(r^2)
      +(pdv(sin(theta) pdv(psi,theta),theta))/(r^2 sin(theta))
      +pdv(psi,phi,2)/(r^2 sin(theta)^2) . $

    The factors $r^2$ and $sin(theta)$ express the changing physical area of
    spherical coordinate surfaces.]
  )

  #governing-law(
    [Fast identity checks],
    [The coordinate formulas must satisfy
    $div(curl(bold(A)))=0$ and $curl(grad(psi))=bold(0)$ whenever the fields
    are sufficiently smooth. A purely radial inverse-square flux in spherical
    geometry has $A_(r)=C\/r^2$ and zero divergence away from the origin,
    because $r^2 A_(r)=C$. A constant scalar has zero gradient and zero
    Laplacian in every coordinate system. These checks catch missing metric
    factors before a plasma equilibrium or wave equation is trusted.]
  )

  #details(
    [Derivation: cylindrical radial conservation check],
    [#derivation-step[Choose the radial flux]
    Take an axisymmetric purely radial vector

    $ bold(A)=A_(r)(r) bold(e)_(r) . $

    #derivation-step[Compute the cylindrical surface flux]
    The cylindrical divergence is

    $ div(bold(A))=(pdv(r A_(r),r))/r . $

    The flux through a cylindrical surface of radius $r$ and length $L$ is

    $ Phi(r)=2 pi r L A_(r)(r) . $

    Between $r$ and $r+dif r$,

    $ dif Phi=2 pi L pdv(r A_(r),r) dif r , $

    while the shell volume is

    $ dif V=2 pi r L dif r . $

    #derivation-step[Compare flux change with volume]
    Dividing gives

    $ dv(Phi,V)=(pdv(r A_(r),r))/r , $

    exactly the cylindrical divergence. The factor $1\/r$ converts radial
    flux change into flux per physical volume.]
  )

  #rechenbeispiel[
    In an axisymmetric cylindrical plasma column, let the radial particle-flux
    vector be $bold(Gamma)=Gamma_(r)(r) bold(e)_(r)$ with
    $Gamma_(r)(r)=C\/r$. Use
    $C=qty("2.00e12", "m^-1 s^-1")$, and evaluate the flux at
    $r_1=qty("0.100", "m")$ and $r_2=qty("0.200", "m")$. Determine both
    radial fluxes and $div(bold(Gamma))$ for $r>0$.

    Numerical result: $Gamma_(r)(r_1)=qty("2.00e13", "m^-2 s^-1")$,
    $Gamma_(r)(r_2)=qty("1.00e13", "m^-2 s^-1")$, and
    $div(bold(Gamma))=qty("0", "m^-3 s^-1")$.
  ]

  #interpretation(
    [Read operators geometrically],
    [A gradient points in the direction of greatest scalar increase. A
    divergence measures net outward flux density from a small physical volume.
    A curl measures circulation per physical area. The scale factors ensure
    that these meanings survive a coordinate change. In a normalized model,
    one may later set #normalized-label[$xi=r\/L$] and obtain

    $ pdv(psi,r)=(pdv(psi,xi))/L , $

    but the reference length $L$ in
    #unit("m") must be stated explicitly.]
  )

  #summary[
    Orthogonal-coordinate formulas are generated by physical line elements,
    face areas, and volumes. Cartesian coordinates have unit scale factors;
    cylindrical geometry contributes $r$; spherical geometry contributes
    $r$ and $r sin(theta)$. Check formulas with $curl(grad(psi))=0$,
    $div(curl(bold(A)))=0$, and a symmetric flux before using them in a plasma
    derivation.
  ]

  #knowledge-check((
    (
      question: [Why does the cylindrical divergence contain $1\/r$?],
      answer: [A radial shell has volume proportional to $r dif r$, while its outward surface flux is proportional to $r A_(r)$. Their ratio gives

      $ (pdv(r A_(r),r))/r , $

      including the changing circumference.],
    ),
    (
      question: [What does the factor $r sin(theta)$ represent in spherical coordinates?],
      answer: [It is the physical line scale for an azimuthal angle increment: $d l_(phi)=r sin(theta) d phi$. It also enters the face areas and therefore the divergence, curl, and Laplacian.],
    ),
    (
      question: [Which coordinate system is usually the cleanest starting point for a locally plane plasma wave?],
      answer: [Cartesian coordinates, because the basis vectors and scale factors are constant. Cylindrical or spherical coordinates become preferable when the equilibrium or boundary has that symmetry.],
    ),
    (
      question: [How would a normalized radial coordinate change the gradient?],
      answer: [If #normalized-label[$xi=r\/L$] with stated reference length $L$ in #unit("m"), then

      $ pdv(psi,r)=(pdv(psi,xi))/L . $

      Each physical gradient component therefore carries the inverse length scale, which must be recorded before a normalized operator is used.],
    ),
  ))

  #chapter-nav(previous: (href: "../chapters/15-sheaths-probes.html", title: [Plasma sheaths and Langmuir probes]))
]

#appendix
