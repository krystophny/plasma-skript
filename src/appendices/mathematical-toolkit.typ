#import "../theme.typ": *
#import "@preview/physica:0.9.8": div, grad, curl, pdv
#import "@preview/unify:0.8.1": unit

#let appendix = [
  #page-title[Appendix: Mathematical toolkit] <mathematical-toolkit>

  #lead[
    The course repeatedly moves between kinetic, fluid, and field
    descriptions. This appendix collects two pieces of working mathematics
    that make those translations auditable: the energy-weighted second moment
    of the kinetic equation and the differential operators used in Cartesian,
    cylindrical, and spherical coordinates. The formulas are written as a
    reference, but the derivation routes remain available when a result needs
    to be reconstructed rather than memorized.
  ]

  #callout(
    [Use the toolkit as a checklist],
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
    Gaussian CGS is active. The species distribution is defined by
    $d N_s=f_(s) dif^3 bold(r) dif^3 bold(v)$, with position in #unit("cm")
    and velocity in #unit("cm/s"). The mass density $rho_s=m_s n_s$ is in
    #unit("g cm^-3"). The energy density and energy flux below are in
    #unit("erg cm^-3") and #unit("erg cm^-2 s^-1"), respectively. The Lorentz force uses
    $bold(E)+bold(v) times bold(B)/c$; $c$ is the speed of
    light in #unit("cm/s"). No normalized variable is used in this section.
  ]

  #assumption(
    [Kinetic equation and velocity-space boundary],
    [For species $s$, use a smooth kinetic equation with acceleration
    $bold(a)_s=(q_s/m_s)(bold(E)+bold(v) times bold(B)/c)$. The distribution
    and the velocity-space flux $f_(s) bold(a)_s$ vanish sufficiently rapidly
    as $abs(bold(v)) -> infinity$, so surface terms at infinite speed are
    zero. Collisions may exchange energy between species, but their weighted
    integral is retained as a source rather than silently discarded.]
  )

  #definition(
    [Bulk and thermal variables],
    [The species flow velocity and random velocity are
    $bold(u)_s=1/n_s integral bold(v) f_(s) dif^3 bold(v)$ and
    $bold(c)_s=bold(v)-bold(u)_s$. Define the bulk kinetic-energy density,
    internal-energy density, pressure tensor, and heat-flux vector by
    $K_s=1/2 rho_s abs(bold(u)_s)^2$,
    $U_s=1/2 tr bold(P)_s$,
    $bold(P)_s=m_s integral bold(c)_s bold(c)_s f_(s) dif^3 bold(v)$, and
    $bold(q)_s=m_s/2 integral abs(bold(c)_s)^2 bold(c)_s f_(s) dif^3 bold(v)$.
    Here $bold(c)_s bold(c)_s$ is a dyadic product. The total second moment is
    $W_s=K_s+U_s=m_s/2 integral abs(bold(v))^2 f_(s) dif^3 bold(v)$.
    For a collision operator $C_(s)[f]$, define the collisional momentum
    transfer and kinetic-energy transfer by
    $bold(R)_s=m_s integral bold(v) C_(s)[f] dif^3 bold(v)$ and
    $Q_(s)=m_s/2 integral abs(bold(v))^2 C_(s)[f] dif^3 bold(v)$.
    The source $bold(R)_s$ is in #unit("g cm^-2 s^-2") and $Q_(s)$ is in
    #unit("erg cm^-3 s^-1").]
  )

  #governing-law(
    [Species total-energy equation],
    [The energy-weighted kinetic equation gives
    $pdv(W_s,t)+div_(bold(r))((W_s) bold(u)_s+bold(P)_s dot bold(u)_s+bold(q)_s)
      =q_s n_s bold(E) dot bold(u)_s+Q_(s)$,
    where $Q_(s)$ is the collisional rate of kinetic-energy transfer to
    species $s$ in #unit("erg cm^-3 s^-1"). The magnetic force is absent from
    the power term because $bold(v) dot (bold(v) times bold(B))=0$.]
  )

  #equation-note[
    The three terms in the energy flux have distinct meanings: bulk energy
    advection $W_s bold(u)_s$, pressure work transport $bold(P)_s dot
    bold(u)_s$, and random-energy transport $bold(q)_s$. They must not be
    merged into a scalar heat flux unless isotropy and a closure have been
    stated.
  ]

  #callout(
    [Derivation route],
    [Multiply the kinetic equation by $m_s abs(bold(v))^2/2$, integrate over
    all velocity space, commute time and space derivatives with the integral,
    integrate the acceleration term by parts in velocity, then decompose
    $bold(v)=bold(u)_s+bold(c)_s$. The hidden derivation records each of those
    steps and the boundary terms.]
  )

  #details(
    [Derivation: total energy from the kinetic equation],
    [Start from the non-conservative form
    $pdv(f_(s),t)+bold(v) dot grad_(bold(r))(f_(s))
      +bold(a)_s dot grad_(bold(v))(f_(s))=C_(s)[f]$.
    Since $bold(v)$ is independent of $bold(r)$, the streaming term may also
    be written as $div_(bold(r))(f_(s) bold(v))$. Set
    $epsilon_(s)(bold(v))=m_s abs(bold(v))^2/2$ and integrate after
    multiplication:
    $integral epsilon_(s) pdv(f_(s),t) dif^3 bold(v)
      +integral epsilon_(s) div_(bold(r))(f_(s) bold(v)) dif^3 bold(v)
      +integral epsilon_(s) bold(a)_s dot grad_(bold(v))(f_(s)) dif^3 bold(v)
      =integral epsilon_(s) C_(s)[f] dif^3 bold(v)$.

    The first term is
    $integral epsilon_(s) pdv(f_(s),t) dif^3 bold(v)
      =pdv(integral epsilon_(s) f_(s) dif^3 bold(v),t)=pdv(W_s,t)$.
    The second term commutes with the velocity integral:
    $integral epsilon_(s) div_(bold(r))(f_(s) bold(v)) dif^3 bold(v)
      =div_(bold(r))(m_s/2 integral abs(bold(v))^2 bold(v) f_(s) dif^3 bold(v))$.

    For the acceleration term, use the velocity-space product rule:
    $epsilon_(s) bold(a)_s dot grad_(bold(v))(f_(s))
      =grad_(bold(v)) dot(epsilon_(s) f_(s) bold(a)_s)
        -f_(s) bold(a)_s dot grad_(bold(v))(epsilon_(s))$.
    Integrating the first term gives a surface integral at infinite speed,
    $integral_("boundary V_v") epsilon_(s) f_(s) bold(a)_s dot d bold(S)_v$,
    which is zero by the boundary assumption. Because
    $grad_(bold(v))(epsilon_(s))=m_s bold(v)$, the remaining term is
    $-m_s integral f_(s) bold(a)_s dot bold(v) dif^3 bold(v)$.
    Substitute the Lorentz acceleration:
    $-q_s integral f_(s) bold(v) dot
      (bold(E)+bold(v) times bold(B)/c) dif^3 bold(v)$.
    The magnetic contribution vanishes pointwise, leaving
    $-q_s bold(E) dot integral bold(v) f_(s) dif^3 bold(v)
      =-q_s n_s bold(E) dot bold(u)_s$.
    Move this term to the right-hand side. Define the collision power
    $Q_(s)=integral epsilon_(s) C_(s)[f] dif^3 bold(v)$ to obtain
    $pdv(W_s,t)+div_(bold(r))(m_s/2 integral abs(bold(v))^2 bold(v) f_(s) dif^3 bold(v))
      =q_s n_s bold(E) dot bold(u)_s+Q_(s)$.

    It remains to reduce the flux. Substitute
    $bold(v)=bold(u)_s+bold(c)_s$ and expand
    $abs(bold(v))^2=abs(bold(u)_s)^2+2 bold(u)_s dot bold(c)_s+abs(bold(c)_s)^2$.
    The first-order random moment vanishes:
    $integral bold(c)_s f_(s) dif^3 bold(v)=bold(0)$.
    The terms that survive are
    $m_s/2 integral abs(bold(v))^2 bold(v) f_(s) dif^3 bold(v)
      =K_s bold(u)_s+U_s bold(u)_s+bold(P)_s dot bold(u)_s+bold(q)_s$.
    Since $W_s=K_s+U_s$, this is
    $W_s bold(u)_s+bold(P)_s dot bold(u)_s+bold(q)_s$.
    Substitution gives the stated total-energy equation.]
  )

  #governing-law(
    [Internal-energy equation],
    [Subtracting the bulk kinetic-energy equation obtained by dotting the
    species momentum equation with $bold(u)_s$ gives
    $pdv(U_s,t)+div_(bold(r))(U_s bold(u)_s+bold(q)_s)
      =-bold(P)_s:grad_(bold(r))(bold(u)_s)+Q_(s)
        -bold(u)_s dot bold(R)_s$.
    The double contraction is
    $bold(P)_s:grad_(bold(r))(bold(u)_s)
      =sum_(i,j) (P_s)_(i j) pdv((u_s)_(i),r_(j))$.
    For an isotropic pressure tensor $bold(P)_s=p_s bold(I)$, the pressure
    work reduces to $p_s div_(bold(r))(bold(u)_s)$ and
    $U_s=3 p_s/2$ in three spatial dimensions.]
  )

  #details(
    [Derivation: subtract bulk energy and identify pressure work],
    [The first moment of the kinetic equation is
    $pdv(rho_s bold(u)_s,t)+div_(bold(r))(rho_s bold(u)_s bold(u)_s+bold(P)_s)
      =q_s n_s (bold(E)+bold(u)_s times bold(B)/c)+bold(R)_s$.
    Dot this equation with $bold(u)_s$. Using mass continuity, the bulk-energy
    identity is
    $pdv(K_s,t)+div_(bold(r))(K_s bold(u)_s)
      =q_s n_s bold(E) dot bold(u)_s-bold(u)_s dot
      div_(bold(r))(bold(P)_s)+bold(u)_s dot bold(R)_s$.

    The total-energy equation contains the same electromagnetic power. Insert
    $W_s=K_s+U_s$ and subtract the bulk identity. This yields
    $pdv(U_s,t)+div_(bold(r))(U_s bold(u)_s+bold(P)_s dot bold(u)_s+bold(q)_s)
      =bold(u)_s dot div_(bold(r))(bold(P)_s)+Q_(s)-bold(u)_s dot bold(R)_s$.
    Apply the tensor product rule
    $div_(bold(r))(bold(P)_s dot bold(u)_s)
      =bold(u)_s dot div_(bold(r))(bold(P)_s)
        +bold(P)_s:grad_(bold(r))(bold(u)_s)$.
    The first term cancels, leaving the internal-energy equation. For
    $bold(P)_s=p_s bold(I)$, the contraction with the identity is the
    divergence, so the isotropic limit follows immediately.]
  )

  #interpretation(
    [What the second moment remembers],
    [The total-energy equation tracks directed and random kinetic energy
    together. The internal form isolates compressional work, anisotropic shear
    work, and heat-flux transport. A fluid model closes this equation only
    after choosing how $bold(P)_s$, $bold(q)_s$, and $Q_(s)$ are represented.
    In a collisionless plasma, $Q_(s)$ can vanish for the total energy of all
    species while energy is still exchanged between species or between fields
    and particles. For collisional species exchange, the internal source is
    $Q_(s)-bold(u)_s dot bold(R)_s$: total collisional power and bulk momentum
    transfer must be separated.]
  )

  #summary[
    Weighting the kinetic equation by $m_s abs(bold(v))^2/2$ gives a total
    energy balance. Velocity-space integration by parts turns the Lorentz
    force into electric work; the magnetic part does no work. Decomposing
    velocity into bulk plus random motion separates bulk advection, pressure
    work, and heat-flux transport. The next omitted moment is therefore a
    closure choice, not an algebraic accident.
  ]

  #knowledge-check((
    (
      question: [Why does the magnetic part of the Lorentz force not appear in the single-species energy source?],
      answer: [Its power is proportional to $bold(v) dot (bold(v) times bold(B))$, which is zero for every particle. The electric part contributes $q_s n_s bold(E) dot bold(u)_s$ in Gaussian CGS.],
    ),
    (
      question: [Which term transports random kinetic energy relative to the species flow?],
      answer: [The heat-flux vector $bold(q)_s=m_s/2 integral abs(bold(c)_s)^2 bold(c)_s f_(s) dif^3 bold(v)$ transports random energy. It is a third central velocity moment and needs a closure in a truncated fluid model.],
    ),
    (
      question: [What assumption removes the velocity-space surface term in the energy derivation?],
      answer: [The distribution and velocity-space flux must decay fast enough that the surface integral at $abs(bold(v)) -> infinity$ vanishes. If a high-energy boundary or source is present, that flux must be retained.],
    ),
    (
      question: [How does isotropic pressure simplify the internal-energy equation?],
      answer: [With $bold(P)_s=p_s bold(I)$, the tensor contraction becomes $bold(P)_s:grad_(bold(r))(bold(u)_s)=p_s div_(bold(r))(bold(u)_s)$ and the internal energy is $U_s=3p_s/2$ in three dimensions.],
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
    Gaussian CGS is active. Coordinates $x,y,z,r$ are lengths in #unit("cm"),
    angles $phi$ and $theta$ are dimensionless, and a scalar field $psi$ and
    vector field $bold(A)$ retain whatever physical units the model assigns.
    Thus $grad psi$ has units of $psi$ per #unit("cm"), $div bold(A)$ has
    units of $bold(A)$ per #unit("cm"), and $curl bold(A)$ has the same
    units. The formulas below are dimensional coordinate identities; no
    normalized radius is implied.
  ]

  #assumption(
    [Orthogonal curvilinear coordinates],
    [Let $(q_1,q_2,q_3)$ be orthogonal coordinates with unit basis vectors
    $bold(e)_(1)$, $bold(e)_(2)$, and $bold(e)_(3)$. Define scale factors by
    $d bold(r)=sum_i h_i d q_i bold(e)_(i)$. The basis is orthonormal at each
    point, but it may vary with position. Components $A_(i)$ are physical
    components along the local unit vectors, not covariant components.]
  )

  #definition(
    [Metric scale factors],
    [The scale factors $h_i$ convert coordinate increments to physical line
    elements. The three systems used most often here are
    $"Cartesian:" (q_1,q_2,q_3)=(x,y,z), (h_1,h_2,h_3)=(1,1,1)$,
    $"cylindrical:" (q_1,q_2,q_3)=(r,phi,z), (h_1,h_2,h_3)=(1,r,1)$,
    and
    $"spherical:" (q_1,q_2,q_3)=(r,theta,phi),
      (h_1,h_2,h_3)=(1,r,r sin(theta))$.
    The volume element is $dif V=h_1 h_2 h_3 dif q_1 dif q_2 dif q_3$.]
  )

  #governing-law(
    [Orthogonal-coordinate operators],
    [For a scalar $psi$ and vector
    $bold(A)=sum_i A_(i) bold(e)_(i)$, the operators are
    $grad psi=sum_i bold(e)_(i)/h_i pdv(psi,q_i)$,
    $div bold(A)=1/(h_1 h_2 h_3) sum_i pdv((h_j h_k A_(i)),q_i)$,
    where $(i,j,k)$ cycles through $(1,2,3)$, and
    $curl bold(A)=sum_i bold(e)_(i)/(h_j h_k)
      (pdv(h_k A_(k),q_j)-pdv(h_j A_(j),q_k))$.
    The scalar Laplacian is
    $nabla^2 psi=1/(h_1 h_2 h_3) sum_i pdv((h_j h_k/h_i) pdv(psi,q_i),q_i)$.
    Each derivative is with respect to the displayed coordinate, while the
    scale factors account for physical distance and area.]
  )

  #equation-note[
    In the cyclic formulas, for the component with index $i$, the remaining
    indices $(j,k)$ are taken in cyclic order. For example, the first curl
    component is $1/(h_2 h_3) [pdv(h_3 A_(3),q_2)-pdv(h_2 A_(2),q_3)]$.
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
    [Derivation: why scale factors enter],
    [The gradient follows from the definition of a directional differential.
    For a scalar field,
    $d psi=grad psi dot d bold(r)
      =sum_i (grad psi)_(i) h_i d q_i$.
    Independently, the chain rule gives
    $d psi=sum_i pdv(psi,q_i) d q_i$.
    Comparing coefficients yields
    $(grad psi)_(i)=1/h_i pdv(psi,q_i)$.

    For divergence, surround a small coordinate cell by its six physical
    faces. The volume is
    $dif V=h_1 h_2 h_3 dif q_1 dif q_2 dif q_3$.
    The outward flux through the pair of faces normal to
    $bold(e)_(1)$ is the difference of
    $h_2 h_3 A_(1)$ evaluated at the two $q_1$ faces, multiplied by
    $dif q_2 dif q_3$. The two other face pairs are cyclic permutations.
    Divide the sum of outward fluxes by $dif V$ and take the cell size to
    zero:
    $div bold(A)=1/(h_1 h_2 h_3)[
      pdv(h_2 h_3 A_(1),q_1)+pdv(h_3 h_1 A_(2),q_2)+pdv(h_1 h_2 A_(3),q_3)]$.

    For curl, use circulation around a small coordinate face. The face normal
    to $bold(e)_(1)$ has physical area $h_2 h_3 dif q_2 dif q_3$.
    The circulation of $bold(A)$ around its boundary is the difference of
    the tangential line integrals of $h_3 A_(3)$ and $h_2 A_(2)$. Divide by
    the face area and take the limit:
    $(curl bold(A))_(1)=1/(h_2 h_3)[
      pdv(h_3 A_(3),q_2)-pdv(h_2 A_(2),q_3)]$.
    Cyclic permutation gives the other two components.

    Finally apply $nabla^2 psi=div(grad psi)$. Inserting the gradient
    components into the divergence expression gives
    $nabla^2 psi=1/(h_1 h_2 h_3) sum_i
      pdv((h_j h_k/h_i) pdv(psi,q_i),q_i)$.
    This derivation also explains why the scale factors must be differentiated
    when they vary with position.]
  )

  #definition(
    [Cartesian specialization],
    [For $(x,y,z)$, all scale factors are one:
    $grad psi=bold(e)_x pdv(psi,x)+bold(e)_y pdv(psi,y)+bold(e)_z pdv(psi,z)$,
    $div bold(A)=pdv(A_(x),x)+pdv(A_(y),y)+pdv(A_(z),z)$,
    and
    $nabla^2 psi=pdv(psi,x,2)+pdv(psi,y,2)+pdv(psi,z,2)$.
    The Cartesian curl is
    $curl bold(A)=bold(e)_x [pdv(A_(z),y)-pdv(A_(y),z)]
      +bold(e)_y [pdv(A_(x),z)-pdv(A_(z),x)]
      +bold(e)_z [pdv(A_(y),x)-pdv(A_(x),y)]$.
    These are the local forms used in most linear wave derivations.]
  )

  #definition(
    [Cylindrical specialization],
    [For $(r,phi,z)$, the physical line element is
    $d bold(r)=d r bold(e)_(r)+r d phi bold(e)_(phi)+d z bold(e)_(z)$.
    Therefore
    $grad psi=bold(e)_(r) pdv(psi,r)+bold(e)_(phi)/r pdv(psi,phi)+bold(e)_(z) pdv(psi,z)$,
    $div bold(A)=1/r pdv(r A_(r),r)+1/r pdv(A_(phi),phi)+pdv(A_(z),z)$,
    and
    $nabla^2 psi=1/r pdv(r pdv(psi,r),r)+1/r^2 pdv(psi,phi,2)+pdv(psi,z,2)$.
    In an axisymmetric state $pdv(,phi)=0$, so the cylindrical area factor
    remains in the radial divergence even though the azimuthal derivative
    disappears.]
  )

  #definition(
    [Spherical specialization],
    [For $(r,theta,phi)$, the physical line element is
    $d bold(r)=d r bold(e)_(r)+r d theta bold(e)_(theta)
      +r sin(theta) d phi bold(e)_(phi)$.
    The gradient and divergence are
    $grad psi=bold(e)_(r) pdv(psi,r)+bold(e)_(theta)/r pdv(psi,theta)
      +bold(e)_(phi)/(r sin(theta)) pdv(psi,phi)$,
    $div bold(A)=1/r^2 pdv(r^2 A_(r),r)
      +1/(r sin(theta)) pdv(sin(theta) A_(theta),theta)
      +1/(r sin(theta)) pdv(A_(phi),phi)$,
    and the scalar Laplacian is
    $nabla^2 psi=1/r^2 pdv(r^2 pdv(psi,r),r)
      +1/(r^2 sin(theta)) pdv(sin(theta) pdv(psi,theta),theta)
      +1/(r^2 sin(theta)^2) pdv(psi,phi,2)$.
    The factors $r^2$ and $sin(theta)$ express the changing physical area of
    spherical coordinate surfaces.]
  )

  #governing-law(
    [Fast identity checks],
    [The coordinate formulas must satisfy
    $div(curl bold(A))=0$ and $curl(grad psi)=bold(0)$ whenever the fields
    are sufficiently smooth. A purely radial inverse-square flux in spherical
    geometry has $A_(r)=C/r^2$ and zero divergence away from the origin,
    because $r^2 A_(r)=C$. A constant scalar has zero gradient and zero
    Laplacian in every coordinate system. These checks catch missing metric
    factors before a plasma equilibrium or wave equation is trusted.]
  )

  #details(
    [Derivation: cylindrical radial conservation check],
    [Take an axisymmetric purely radial vector
    $bold(A)=A_(r)(r) bold(e)_(r)$. The cylindrical divergence reduces to
    $div bold(A)=1/r pdv(r A_(r),r)$.
    The flux through a cylindrical surface of radius $r$ and length $L$ is
    $Phi(r)=2 pi r L A_(r)(r)$. Its change between $r$ and $r+dif r$ is
    $dif Phi=2 pi L pdv(r A_(r),r) dif r$.
    The shell volume is $dif V=2 pi r L dif r$. Dividing gives
    $dif Phi/dif V=1/r pdv(r A_(r),r)$, exactly the cylindrical divergence.
    Thus the factor $1/r$ is the local conversion from radial flux change to
    volume change; it is not an optional correction.]
  )

  #interpretation(
    [Read operators geometrically],
    [A gradient points in the direction of greatest scalar increase. A
    divergence measures net outward flux density from a small physical volume.
    A curl measures circulation per physical area. The scale factors ensure
    that these meanings survive a coordinate change. In a normalized model,
    one may later set $xi=r/L$ and obtain $grad=1/L grad_(xi)$, but the
    reference length $L$ must be stated explicitly.]
  )

  #summary[
    Orthogonal-coordinate formulas are generated by physical line elements,
    face areas, and volumes. Cartesian coordinates have unit scale factors;
    cylindrical geometry contributes $r$; spherical geometry contributes
    $r$ and $r sin(theta)$. Check formulas with $curl(grad psi)=0$,
    $div(curl bold(A))=0$, and a symmetric flux before using them in a plasma
    derivation.
  ]

  #knowledge-check((
    (
      question: [Why does the cylindrical divergence contain $1/r$?],
      answer: [A radial shell has volume proportional to $r dif r$, while its outward surface flux is proportional to $r A_(r)$. Their ratio gives $1/r pdv(r A_(r),r)$, including the changing circumference.],
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
      answer: [If $xi=r/L$ with stated reference length $L$ in #unit("cm"), then $pdv(,r)=1/L pdv(,xi)$ and $grad_(r)=(1/L) grad_(xi)$. The normalized operator is dimensionless only after this scale is recorded.],
    ),
  ))

  #chapter-nav(previous: (href: "../chapters/13-sheaths-probes.html", title: [Plasma sheaths and Langmuir probes]))
]

#appendix
