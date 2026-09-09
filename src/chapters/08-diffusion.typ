#import "../theme.typ": *
#import "../figures.typ": random-walk-diffusion, ambipolar-balance, cross-field-diffusion, diffusion-scalings
#import "@preview/physica:0.9.8": div, grad, pdv
#import "@preview/unify:0.8.1": qty, unit

#let chapter = [
  #page-title[8. Plasma diffusion] <plasma-diffusion>

  #lead[
    Diffusion is the macroscopic signature of many small changes in particle
    trajectories. Collisions randomize a particle's direction; gradients bias
    the resulting random walk toward lower density. Magnetic fields do not
    remove diffusion, but they make the transport direction dependent.
  ]

  #callout(
    [A transport question],
    [Which microscopic step length and time set the macroscopic coefficient
    $D$? The answer depends on whether particles are unmagnetized, tied
    together by quasi-neutrality, interrupted by collisions across $bold(B)$,
    or transported by unresolved turbulence.]
  )

  #section-title[Random walks and the diffusion coefficient] <random-walk-diffusion>

  #lead[
    A symmetric random walk has no preferred direction, so its mean displacement
    remains zero. Its variance does not remain zero: independent steps add in
    quadrature. That distinction is the origin of a diffusion equation.
  ]

  #objectives((
    [derive the diffusion coefficient from a symmetric random walk],
    [connect Fick's law to the continuity equation],
    [interpret the diffusive timescale and the Gaussian spreading solution],
    [state which assumptions distinguish diffusion from directed advection],
  ))

  #unit-ledger[
    Gaussian CGS is active. Number density $n$ is in #unit("cm^-3"), position
    and length scales are in #unit("cm"), time is in #unit("s"), a diffusion
    coefficient $D$ is in #unit("cm^2/s"), and particle flux
    $bold(Gamma)$ is in #unit("cm^-2/s"). The normalized variables
    $xi=x/L_0$ and $tau=t/tau_0$ are dimensionless.
  ]

  #assumption(
    [Independent, symmetric steps],
    [Use a large number of uncorrelated steps with finite variance, zero mean
    displacement, and a step time short compared with the macroscopic
    evolution time. The density varies slowly over one step, so a local
    gradient expansion is meaningful. Directed drifts are either absent or
    separated from the diffusive flux.]
  )

  #definition(
    [Diffusion from a random walk],
    [For a one-dimensional step of magnitude $Delta x$ every $Delta t$, define
    $D=(Delta x)^2/(2 Delta t)$. The diffusive particle flux obeys Fick's law
    $bold(Gamma)^(D)=-D grad_(bold(r))(n)$, and a system of size $L$ has
    the diffusion time
    $tau_"D"=L^2/D$. In three dimensions, the variance relation is
    $⟨abs(bold(r))^2⟩=6 D t$.]
  )

  #details(
    [Derivation: from step statistics to the diffusion equation],
    [Let one step be $+Delta x$ or $-Delta x$ with equal probability. Its
    first moment is
    $⟨Delta x⟩=(Delta x)/2+(-Delta x)/2=0$,
    while its second moment is
    $⟨(Delta x)^2⟩=((Delta x)^2)/2+((-Delta x)^2)/2=(Delta x)^2$.

    After $N=t/Delta t$ statistically independent steps, cross terms in the
    square of the total displacement vanish because the individual means are
    zero. Therefore
    $⟨x⟩=0$ and
    $⟨x^2⟩=N(Delta x)^2
      =(((Delta x)^2 t)/Delta t)=2 D t$,
    which defines the one-dimensional coefficient.

    To obtain the local flux, consider a cell of width $Delta x$. The
    right-moving and left-moving populations sample densities displaced by
    one step. Expanding those densities to first order gives a net flux
    proportional to the negative density gradient:
    $bold(Gamma)^(D)=-((Delta x)^2/(2 Delta t)) grad n=-D grad n$.
    Particle conservation is
    $pdv(n,t)+div(bold(Gamma))=0$.
    Substitution yields the variable-coefficient diffusion equation
    $pdv(n,t)=div(D grad n)$.
    When $D$ is uniform, this reduces to
    $pdv(n,t)=D nabla^2 n$.

    For a point-like initial packet in one dimension, the normalized Green
    function is
    $n(x,t)=N_0/sqrt(4 pi D t)
      exp(-x^2/(4 D t))$.
    Its second moment evaluates to $⟨x^2⟩=2 D t$. Independent Cartesian
    directions add, giving $⟨abs(bold(r))^2⟩=6 D t$ in three dimensions.]
  )

  #governing-law(
    [A normalized diffusion equation],
    [Choose reference length $L_0$ in #unit("cm"), time $tau_0$ in
    #unit("s"), and density $n_0$ in #unit("cm^-3"). Define the reference
    coefficient $D_0=L_0^2/tau_0$ in #unit("cm^2/s") and the dimensionless
    variables
    $bold(xi)=bold(r)/L_0$, $tau=t/tau_0$,
    $n_("norm")=n/n_0$, and $D_("norm")=D/D_0$.
    The diffusion equation then has the dimensionless form
    $pdv(n_("norm"), tau)=div_(bold(xi))
      (D_("norm") grad_(bold(xi))(n_("norm")))$.
    For a system length $L$ with $L_("norm")=L/L_0$, the normalized
    diffusion time is $tau_"D"/tau_0=L_("norm")^2/D_("norm")$.
    Every dimensional result is recovered by restoring the stated reference
    scales; no unit is hidden in a normalized axis or coefficient.]
  )

  #random-walk-diffusion

  #animation(
    "../media/diffusion-random-walk.mp4",
    "A normalized one-dimensional ensemble of walkers starts at the same position and takes reproducible symmetric steps. As time advances, the blue walkers spread to both sides while their mean position remains near the origin. Teal traces show selected paths, and the displayed relation states that the variance grows as two times the diffusion coefficient times time.",
    caption: [
      Random-walk spreading: the mean displacement cancels while the variance
      grows. The animation is a deterministic normalized illustration, not a
      Monte-Carlo transport calculation or measured data.
    ],
    poster: "../media/diffusion-random-walk.png",
  )

  #rechenbeispiel[
    A one-dimensional neutral-collision model has a step magnitude
    $Delta x=qty("2.0e-1", "cm")$ every
    $Delta t=qty("1.0e-7", "s")$. For a device of length
    $L=qty("1.0e1", "cm")$, determine the diffusion coefficient and the
    characteristic diffusion time.

    Numerical result: $D=qty("2.0e5", "cm^2/s")$ and
    $tau_"D"=qty("5.0e-4", "s")$.
  ]

  #interpretation(
    [Diffusion is not advection],
    [A uniform density has no diffusive flux even when particles move
    thermally. A density gradient produces a flux down the gradient, whereas
    an externally imposed velocity produces directed advection. If the
    collision correlation time is not short compared with the observation
    time, the random-walk approximation can fail and the transport becomes
    ballistic or anomalous.]
  )

  #summary[
    Independent symmetric steps give $⟨x⟩=0$ but
    $⟨x^2⟩=2 D t$ in one dimension. Fick's law
    $bold(Gamma)^(D)=-D grad n$ and particle conservation produce
    $pdv(n,t)=div(D grad n)$, with the scale
    $tau_"D"=L^2/D$.
  ]

  #knowledge-check((
    (
      question: [Why does a symmetric random walk have zero mean displacement but nonzero spreading?],
      answer: [The positive and negative steps cancel in the first moment, but
      the squared steps are positive and add. Thus $⟨x⟩=0$ while
      $⟨x^2⟩$ grows linearly with time.]
    ),
    (
      question: [What physical statement is encoded by Fick's law?],
      answer: [The diffusive particle flux points down the density gradient:
      $bold(Gamma)^(D)=-D grad n$. The coefficient $D$ measures the
      strength of that response.]
    ),
    (
      question: [How does the characteristic diffusion time scale with system size?],
      answer: [For a fixed coefficient, $tau_"D"=L^2/D$, so doubling the
      length makes the diffusive time four times larger.]
    ),
    (
      question: [Which assumption separates diffusion from ballistic transport?],
      answer: [Diffusion requires many weakly correlated steps and a local
      gradient over the observation time. If a particle retains its direction
      over the whole experiment, a ballistic description is more appropriate.]
    ),
  ))

  #section-title[Diffusion in weakly ionized plasmas] <weakly-ionized-diffusion>

  #lead[
    In a weakly ionized plasma, collisions with neutrals provide the drag that
    converts a force or a pressure gradient into a drift. The same momentum
    equation therefore contains both mobility and diffusion.
  ]

  #objectives((
    [reduce the collisional momentum equation to a drift-diffusion law],
    [define signed mobility and positive diffusion coefficients],
    [use the Einstein relation without losing the charge-sign convention],
    [identify when the weakly ionized approximation is local and isothermal],
  ))

  #unit-ledger[
    In Gaussian CGS, $q_s$ is in statcoulomb, $m_s$ in #unit("g"), collision
    frequency $nu_s$ in #unit("s^-1"), temperature energy $k_B T_s$ in
    #unit("erg"), mobility $mu_s$ has units of velocity divided by electric
    field, and $D_s$ is in #unit("cm^2/s"). The flux remains in
    #unit("cm^-2/s").
  ]

  #assumption(
    [Local, isothermal neutral drag],
    [Use a weakly ionized plasma with a prescribed neutral background, a
    constant momentum-transfer frequency $nu_s$, small drift relative to the
    thermal speed, and no magnetic field in this section. Let the species
    pressure be $p_s=n_s k_B T_s$ and neglect inertia on the collision time.]
  )

  #definition(
    [Mobility and diffusion],
    [The species momentum equation is
    $m_s n_s (pdv(bold(u)_s,t)+bold(u)_s dot grad bold(u)_s)
      =q_s n_s bold(E)-grad p_s
        -m_s n_s nu_s bold(u)_s$.
    In the steady small-drift limit,
    $bold(u)_s=mu_s^(q) bold(E)-D_s (grad n_s)/n_s$,
    where the signed mobility and diffusion coefficient are
    $mu_s^(q)=q_s/(m_s nu_s)$ and
    $D_s=(k_B T_s)/(m_s nu_s)$.]
  )

  #governing-law(
    [Weakly ionized drift-diffusion flux],
    [Multiplying the velocity law by $n_s$ gives
    $bold(Gamma)_s=n_s mu_s^(q) bold(E)-D_s grad n_s$.
    If a positive mobility is preferred, define
    $mu_s=abs(q_s)/(m_s nu_s)$ and keep the sign of $q_s$ explicitly
    in the force term. The Einstein relation is
    $D_s=(mu_s k_B T_s)/abs(q_s)$.]
  )

  #details(
    [Derivation: collisional force balance],
    [Start with the species momentum equation and use the isothermal equation
    of state:
    $grad p_s=k_B T_s grad n_s$.
    On times longer than $nu_s^(-1)$, neglect the inertial terms and solve
    the remaining algebraic equation:
    $m_s n_s nu_s bold(u)_s
      =q_s n_s bold(E)-k_B T_s grad n_s$.
    Division by $m_s n_s nu_s$ gives
    $bold(u)_s=q_s/(m_s nu_s) bold(E)
      -(k_B T_s)/(m_s nu_s) (grad n_s)/n_s$.

    Identifying the first coefficient as the signed mobility
    $mu_s^(q)=q_s/(m_s nu_s)$ and the second as
    $D_s=(k_B T_s)/(m_s nu_s)$ gives the displayed velocity law. Multiplication
    by $n_s$ produces the flux. For the magnitude convention,
    $abs(mu_s^(q))=abs(q_s)/(m_s nu_s)$, so
    $D_s/abs(mu_s^(q))=(k_B T_s)/abs(q_s)$.
    This is the Einstein relation in the present local, isothermal model.

    The derivation also identifies the approximation boundary: inertia matters
    when the forcing varies on a time comparable to $nu_s^(-1)$, and the
    scalar coefficient is insufficient when a magnetic field makes the
    response tensorial.]
  )

  #rechenbeispiel[
    For electrons in a weakly ionized plasma, use
    $k_B T_e=qty("3.204e-12", "erg")$,
    $m_e=qty("9.109e-28", "g")$,
    $e=qty("4.803e-10", "statC")$, and
    $nu_e=qty("1.0e8", "s^-1")$. Determine the positive mobility magnitude
    $mu_e=e/(m_e nu_e)$ and the diffusion coefficient
    $D_e=(k_B T_e)/(m_e nu_e)$.

    Numerical result: $mu_e=qty("5.27e9", "cm^2/statV/s")$ and
    $D_e=qty("3.52e7", "cm^2/s")$.
  ]

  #interpretation(
    [The same collision rate controls two responses],
    [A larger collision frequency reduces the drift mobility and the
    unmagnetized diffusion coefficient. This does not mean that collisions
    always reduce transport: across a magnetic field, collisions are also
    what interrupt gyromotion and allow a random walk between field lines.]
  )

  #summary[
    Neutral drag yields
    $bold(Gamma)_s=n_s mu_s^(q) bold(E)-D_s grad n_s$ with
    $mu_s^(q)=q_s/(m_s nu_s)$ and
    $D_s=(k_B T_s)/(m_s nu_s)$. The Einstein relation connects their
    magnitudes, while the sign of the force response remains set by $q_s$.
  ]

  #knowledge-check((
    (
      question: [Which term in the weakly ionized flux is driven by a density gradient?],
      answer: [The Fick term $-D_s grad n_s$ is gradient driven. It points
      down the density gradient and is distinct from the electric-force term.]
    ),
    (
      question: [How does increasing the neutral collision frequency affect unmagnetized diffusion?],
      answer: [At fixed temperature, $D_s=(k_B T_s)/(m_s nu_s)$ decreases
      inversely with $nu_s$ because the mean free path and drift response are
      both shortened.]
    ),
    (
      question: [Why must the charge sign be kept separate from the positive mobility magnitude?],
      answer: [Electrons and ions drift in opposite directions under the same
      electric field. Writing $mu_s=abs(q_s)/(m_s nu_s)$ and retaining $q_s$
      in the force term prevents that sign from being lost.]
    ),
    (
      question: [When is the scalar Einstein relation insufficient?],
      answer: [It is insufficient when the response is anisotropic, such as in
      a magnetic field, or when the plasma is non-isothermal or strongly
      time-dependent.]
    ),
  ))

  #section-title[Ambipolar diffusion and the ambipolar electric field] <ambipolar-diffusion>

  #lead[
    Electrons usually diffuse faster than ions because their mass is smaller.
    A plasma cannot tolerate sustained charge separation, however. A small
    electric field develops until the species carry the same particle flux.
    This coupled transport is ambipolar diffusion.
  ]

  #objectives((
    [write the electron and ion fluxes with explicit charge signs],
    [derive the ambipolar electric field from equal particle fluxes],
    [obtain the ambipolar diffusion coefficient],
    [explain the role of quasi-neutrality and zero net current],
  ))

  #unit-ledger[
    The density $n$ is in #unit("cm^-3"), density gradient is in
    #unit("cm^-4"), species fluxes and the common ambipolar flux are in
    #unit("cm^-2/s"), the ambipolar field is in statvolt per #unit("cm"),
    and $D_a$ is in #unit("cm^2/s"). The hydrogen charge magnitude $e$ is in
    statcoulomb.
  ]

  #assumption(
    [Quasi-neutral, singly charged hydrogen],
    [Use $n_i approx n_e=n$, $q_i=+e$, $q_e=-e$, equal isothermal
    temperatures within each species, and no externally imposed current.
    The electron and ion drift-diffusion coefficients are evaluated locally,
    and the ambipolar field adjusts faster than the density profile evolves.]
  )

  #definition(
    [Species fluxes and quasi-neutrality],
    [With positive mobility magnitudes, the unmagnetized fluxes are
    $bold(Gamma)_i=mu_i n bold(E)-D_i grad n$ and
    $bold(Gamma)_e=-mu_e n bold(E)-D_e grad n$.
    The current is
    $bold(j)=e (bold(Gamma)_i-bold(Gamma)_e)$.
    Quasi-neutral ambipolar transport imposes
    $bold(j)=bold(0)$, equivalently
    $bold(Gamma)_i=bold(Gamma)_e$.]
  )

  #governing-law(
    [Ambipolar field and diffusion coefficient],
    [Solving the equal-flux condition gives
    $bold(E)_a=((D_i-D_e)/(mu_i+mu_e)) (grad n)/n$.
    Substitution into either species flux gives
    $bold(Gamma)_a=-D_a grad n$ with
    $D_a=(mu_i D_e+mu_e D_i)/(mu_i+mu_e)$.]
  )

  #details(
    [Derivation: quasi-neutral flux balance],
    [For positive ions, the electric force drives a flux in the direction of
    $bold(E)$:
    $bold(Gamma)_i=mu_i n bold(E)-D_i grad n$.
    Electrons have the opposite charge, so
    $bold(Gamma)_e=-mu_e n bold(E)-D_e grad n$.
    The current-free condition is
    $bold(0)=bold(j)=e(bold(Gamma)_i-bold(Gamma)_e)$.
    Equating the two fluxes and collecting the field terms gives
    $(mu_i+mu_e)n bold(E)=(D_i-D_e)grad n$,
    hence
    $bold(E)_a=((D_i-D_e)/(mu_i+mu_e)) (grad n)/n$.

    Insert this field into the ion flux:
    $bold(Gamma)_i
      =((mu_i n (D_i-D_e))/(mu_i+mu_e)) ((grad n)/n)-D_i grad n$.
    Putting both terms over the common denominator produces
    $bold(Gamma)_i
      =-(mu_i D_e+mu_e D_i)/(mu_i+mu_e) grad n$.
    The same result follows from the electron flux, so define
    $D_a=(mu_i D_e+mu_e D_i)/(mu_i+mu_e)$.

    For equal temperatures and comparable collision models, the mobility
    hierarchy often gives $mu_e >> mu_i$. Then
    $D_a approx D_i+(mu_i/mu_e) D_e$; the electron diffusion is largely
    converted into the ambipolar electric field rather than a net current.]
  )

  #ambipolar-balance

  #rechenbeispiel[
    Consider a weakly ionized hydrogen plasma with
    $n=qty("1.0e10", "cm^-3")$,
    $(grad n)/n=qty("-1.0e-2", "cm^-1")$, and
    $k_B T_i=k_B T_e=qty("1.602e-12", "erg")$.
    Use $m_i=qty("1.673e-24", "g")$,
    $m_e=qty("9.109e-28", "g")$,
    $e=qty("4.803e-10", "statC")$,
    $nu_i=qty("1.0e7", "s^-1")$, and
    $nu_e=qty("1.0e9", "s^-1")$. Determine the ambipolar field,
    coefficient, and particle flux.

    Numerical result:
    $bold(E)_a=qty("2.99e-5", "statV/cm")$,
    $D_a=qty("1.82e5", "cm^2/s")$, and
    $abs(bold(Gamma)_a)=qty("1.82e13", "cm^-2/s")$.
  ]

  #interpretation(
    [Quasi-neutrality couples otherwise unequal rates],
    [The ambipolar field is not an externally prescribed equilibrium field.
    It is the small electrostatic correction required to prevent the faster
    species from running ahead. The total particle flux can remain finite
    even though the net current is approximately zero.]
  )

  #summary[
    Equal electron and ion particle fluxes give
    $bold(E)_a=((D_i-D_e)/(mu_i+mu_e)) (grad n)/n$ and
    $bold(Gamma)_a=-D_a grad n$, where
    $D_a=(mu_i D_e+mu_e D_i)/(mu_i+mu_e)$. Ambipolar diffusion is
    therefore a collective consequence of quasi-neutrality.
  ]

  #knowledge-check((
    (
      question: [Why does an ambipolar electric field form?],
      answer: [The more mobile species would otherwise diffuse away faster,
      creating charge separation. The resulting field opposes that separation
      until the electron and ion particle fluxes match.]
    ),
    (
      question: [What condition was used to derive the ambipolar coefficient?],
      answer: [For singly charged hydrogen we imposed zero net current,
      $bold(j)=e(bold(Gamma)_i-bold(Gamma)_e)=bold(0)$, together with
      quasi-neutral density.]
    ),
    (
      question: [Can ambipolar diffusion carry particles when the current vanishes?],
      answer: [Yes. Equal oppositely charged particle fluxes cancel in the
      current but add to the total particle transport.]
    ),
    (
      question: [What changes if the plasma is not quasi-neutral on the transport scale?],
      answer: [The electric field must then be obtained from Poisson's equation
      and a charge-separation model; the equal-flux ambipolar closure is no
      longer sufficient.]
    ),
  ))

  #section-title[Cross-field diffusion in a magnetic field] <cross-field-diffusion>

  #lead[
    Along a magnetic field, a colliding particle can random-walk as if it were
    unmagnetized. Across the field, the guiding center is tied to a field line
    between collisions. A collision interrupts gyromotion and creates the
    cross-field step.
  ]

  #objectives((
    [derive the parallel and perpendicular diffusion coefficients],
    [identify the magnetization parameter $abs(Omega_s)/nu_s$],
    [separate ordinary diffusion from Hall-like transverse response],
    [explain why the collisionless limit suppresses classical cross-field diffusion],
  ))

  #unit-ledger[
    In Gaussian CGS, $bold(B)$ is in gauss, the signed cyclotron frequency
    $Omega_s=(q_s B)/(m_s c)$ is in #unit("s^-1"), and the magnetization
    parameter $abs(Omega_s)/nu_s$ is dimensionless. Parallel, perpendicular,
    and Hall diffusion coefficients are in #unit("cm^2/s").
  ]

  #assumption(
    [Uniform magnetic field and isotropic drag],
    [Use a locally uniform $bold(B)=B hat(bold(b))$, a scalar collision
    frequency, small drift, and a time-independent field. Pressure gradients
    and electric fields vary slowly over one gyration. Curvature, mirrors,
    finite orbit widths, and turbulence are postponed.]
  )

  #definition(
    [Magnetized diffusion tensor],
    [Let $Omega_s=(q_s B)/(m_s c)$ and
    $D_s=(k_B T_s)/(m_s nu_s)$. The parallel coefficient is
    $D_(s,parallel)=D_s$, while
    $D_(s,perp)=D_s/(1+(Omega_s/nu_s)^2)$.
    A signed transverse coefficient is
    $D_(s,H)=(D_s (Omega_s/nu_s))/(1+(Omega_s/nu_s)^2)$.
    The gradient contribution can be written
    $bold(Gamma)_(s,perp)=-D_(s,perp)grad_perp n_s
      +D_(s,H) hat(bold(b)) times grad_perp n_s$,
    in the chosen orientation convention.]
  )

  #details(
    [Derivation: solving the perpendicular momentum balance],
    [For $bold(B)=B hat(bold(z))$, the steady perpendicular momentum equation
    can be arranged as
    $[
      [nu_s, -Omega_s],
      [Omega_s, nu_s]
    ] [u_(s,x), u_(s,y)]^T
      =(q_s/m_s) [E_x,E_y]^T
        -(k_B T_s)/(m_s n_s) [pdv(n_s,x),pdv(n_s,y)]^T$.
    The inverse matrix is
    $1/(nu_s^2+Omega_s^2)
      [
        [nu_s, Omega_s],
        [-Omega_s,nu_s]
      ]$.

    The gradient part of the flux therefore has diagonal coefficient
    $(k_(B) T_s nu_s)/(m_(s)(nu_s^2+Omega_s^2))
      =(D_s nu_s^2)/(nu_s^2+Omega_s^2)$
    and signed off-diagonal coefficient
    $(k_(B) T_s Omega_s)/(m_(s)(nu_s^2+Omega_s^2))
      =(D_s nu_s Omega_s)/(nu_s^2+Omega_s^2)$.
    These are the displayed $D_(s,perp)$ and $D_(s,H)$.

    The electric-force part contains the familiar crossed-field drift
    $bold(u)_(E times B)=(c (bold(E) times bold(B)))/(B^2)$ as well as a
    collision-reduced force response. In the strongly magnetized limit,
    $abs(Omega_s)>>nu_s$, the perpendicular coefficient becomes
    $D_(s,perp) approx D_(s)(nu_s/Omega_s)^2$.
    Since $D_s=(k_B T_s)/(m_s nu_s)$ and
    $rho_(s,"thermal")^2=(k_B T_s)/(m_s Omega_s^2)$, this is
    $D_(s,perp) approx nu_s rho_(s,"thermal")^2$.
    The limit $nu_s -> 0$ therefore suppresses classical cross-field
    diffusion: without interruptions, guiding centers do not make a
    collisional random walk across field lines.]
  )

  #cross-field-diffusion

  #rechenbeispiel[
    For electrons at $k_B T_e=qty("1.602e-12", "erg")$, use
    $m_e=qty("9.109e-28", "g")$,
    $e=qty("4.803e-10", "statC")$,
    $c=qty("2.998e10", "cm/s")$,
    $B=qty("1.0e2", "G")$, and
    $nu_e=qty("1.0e7", "s^-1")$. Determine the magnitude of the cyclotron
    frequency, the parallel coefficient, and the perpendicular coefficient.

    Numerical result:
    $abs(Omega_e)=qty("1.76e9", "s^-1")$,
    $D_(e,parallel)=qty("1.76e8", "cm^2/s")$,
    $D_(e,perp)=qty("5.69e3", "cm^2/s")$, and
    $D_(e,perp)/D_(e,parallel)=qty("3.23e-5", "1")$.
  ]

  #interpretation(
    [Collisions facilitate cross-field transport],
    [This is a counterintuitive but central ordering. More collisions shorten
    the free path, yet a nonzero collision rate is needed to break the
    indefinite gyromotion. The competition is measured by
    $abs(Omega_s)/nu_s$: it is small for nearly isotropic transport and
    large for strong perpendicular suppression.]
  )

  #summary[
    A magnetic field leaves $D_parallel=D_s$ but reduces the classical
    cross-field coefficient to
    $D_perp=D_s/(1+(Omega_s/nu_s)^2)$. The signed Hall-like coefficient
    describes a transverse response; in the strongly magnetized limit
    $D_perp$ scales as $nu_s rho_"thermal"^2$.
  ]

  #knowledge-check((
    (
      question: [Why is diffusion along a uniform magnetic field not reduced in the same way as cross-field diffusion?],
      answer: [Gyromotion constrains only the perpendicular plane. Along the
      field, particles can continue their collisional random walk, so
      $D_parallel=D_s$ in this local model.]
    ),
    (
      question: [What dimensionless parameter measures magnetization?],
      answer: [The ratio $abs(Omega_s)/nu_s$ compares the gyration rate with
      the collision rate. It is the control parameter in the tensor
      coefficients.]
    ),
    (
      question: [What happens to classical cross-field diffusion as collisions vanish?],
      answer: [For fixed $B$ it tends to zero as
      $D_perp approx D_(s)(nu_s/Omega_s)^2$. A collisionless particle remains
      on its guiding-center orbit apart from other drifts.]
    ),
    (
      question: [What is the physical distinction between $D_perp$ and $D_H$?],
      answer: [$D_perp$ multiplies the gradient-aligned dissipative flux,
      whereas the signed $D_H$ term rotates the response in the perpendicular
      plane. The latter is Hall-like and changes sign with charge.]
    ),
  ))

  #section-title[Fully ionized diffusion and characteristic timescales] <fully-ionized-diffusion>

  #lead[
    In a fully ionized plasma, Coulomb collisions couple the species and the
    electromagnetic force balance must be used consistently. The classical
    cross-field coefficient follows from pressure balance and conductivity.
    Experiments can show faster, anomalous transport, often summarized by the
    empirical Bohm scaling.
  ]

  #objectives((
    [derive the classical fully ionized cross-field coefficient from force balance],
    [state the magnetic-field scaling of classical and Bohm-like transport],
    [use a diffusion coefficient to estimate a loss time],
    [separate a derived collisional result from an empirical turbulent law],
  ))

  #unit-ledger[
    Gaussian CGS is active. Pressure is in #unit("dyn/cm^2"), current density
    in statcoulomb per #unit("cm^2") per #unit("s"), conductivity $sigma$ in
    #unit("s^-1"), $bold(B)$ in gauss, and the classical and Bohm-like
    diffusion coefficients are in #unit("cm^2/s"). The factor $c$ is
    #unit("cm/s") and must remain explicit in Gaussian electromagnetic force
    balance.
  ]

  #assumption(
    [Quasi-neutral, weakly coupled fluid transport],
    [Use a fully ionized, quasi-neutral hydrogen plasma with a scalar
    conductivity, a locally uniform magnetic field, and steady perpendicular
    force balance. The classical result neglects turbulent fluctuations and
    finite-orbit neoclassical geometry. Bohm transport is presented only as
    an empirical comparison.]
  )

  #definition(
    [Classical fully ionized diffusion],
    [The steady force balance and resistive Ohm law are
    $bold(0)=-grad p+(bold(j) times bold(B))/c$ and
    $bold(j)=sigma (bold(E)+(bold(u) times bold(B))/c)$.
    The perpendicular velocity contains
    $bold(u)_perp=(c (bold(E) times bold(B)))/(B^2)
      -(c^2 grad_perp p)/(sigma B^2)$.
    For $p=n k_(B)(T_e+T_i)$, the pressure-driven flux is
    $bold(Gamma)_perp=-D_perp^("cl") grad_perp n$ with
    $D_perp^("cl")=(n c^2 k_(B)(T_e+T_i))/(sigma B^2)$.]
  )

  #governing-law(
    [Classical and Bohm-like scalings],
    [At fixed density, temperatures, and conductivity,
    $D_perp^("cl") ∝ B^(-2)$. A commonly used empirical Bohm estimate in
    Gaussian CGS is
    $D_perp^(B) approx (c k_B T_e)/(16 e B)$,
    so $D_perp^(B) ∝ B^(-1)$. The numerical factor is empirical and
    should not be mistaken for a derivation from the collisional model.]
  )

  #details(
    [Derivation: pressure-driven classical flux],
    [Start from
    $bold(0)=-grad p+(bold(j) times bold(B))/c$
    and substitute
    $bold(j)=sigma(bold(E)+(bold(u) times bold(B))/c)$.
    The cross product identity
    $(bold(u) times bold(B)) times bold(B)=-B^2 bold(u)_perp$
    gives
    $bold(0)=-grad_perp p
      +(sigma (bold(E) times bold(B)))/c
      -(sigma B^2 bold(u)_perp)/(c^2)$.
    Solving for the perpendicular velocity yields
    $bold(u)_perp=(c (bold(E) times bold(B)))/(B^2)
      -(c^2 grad_perp p)/(sigma B^2)$.

    Multiply by $n$. The first term is a common crossed-field drift and does
    not diffuse a uniform density. For an isothermal two-temperature hydrogen
    plasma,
    $grad_perp p=k_(B)(T_e+T_i)grad_perp n$.
    The pressure term in the particle flux is consequently
    $bold(Gamma)_perp^("diff")
      =-(n c^2 k_(B)(T_e+T_i) grad_perp n)/(sigma B^2)$,
    which identifies
    $D_perp^("cl")=(n c^2 k_(B)(T_e+T_i))/(sigma B^2)$.
    The explicit $c^2$ is required because both the Lorentz force density and
    the magnetic part of Ohm's law use the Gaussian-CGS convention.

    The classical loss time for a macroscopic length $L$ is
    $tau_"D"=L^2/D_perp^("cl")$.
    The Bohm expression is not obtained by this force-balance derivation; it
    is a phenomenological fit motivated by turbulent or anomalous transport.
    Neoclassical calculations add field geometry, trapped-particle orbits, and
    finite collisionality before comparing with such an empirical law.]
  )

  #diffusion-scalings

  #rechenbeispiel[
    For a fully ionized hydrogen plasma, use
    $n=qty("1.0e10", "cm^-3")$,
    $k_B T_e=k_B T_i=qty("1.602e-11", "erg")$,
    $sigma=qty("1.0e15", "s^-1")$,
    $B=qty("1.0e2", "G")$,
    $c=qty("2.998e10", "cm/s")$, and
    $e=qty("4.803e-10", "statC")$. Determine the classical coefficient,
    the Bohm estimate, and their ratio. For a device of length
    $L=qty("1.0e2", "cm")$, also estimate the classical diffusion time.

    Numerical result:
    $D_perp^("cl")=qty("2.88e1", "cm^2/s")$,
    $D_perp^(B)=qty("6.25e5", "cm^2/s")$,
    $D_perp^(B)/D_perp^("cl")=qty("2.17e4", "1")$, and
    $tau_"D"^("cl")=qty("3.47e2", "s")$.
  ]

  #interpretation(
    [Classical, neoclassical, and anomalous are different claims],
    [The $B^(-2)$ classical law is a collisional consequence of the local
    force balance. Neoclassical transport modifies it through magnetic
    geometry and orbit effects. A Bohm-like $B^(-1)$ law is an empirical
    anomalous scaling associated with unresolved turbulence; it is not a
    replacement for stating the collision and geometry model.]
  )

  #summary[
    Fully ionized classical transport gives
    $D_perp^("cl")=(n c^2 k_(B)(T_e+T_i))/(sigma B^2)$ and
    $tau_"D"=L^2/D$. It scales as $B^(-2)$, while the empirical Bohm
    estimate scales as $B^(-1)$. The two describe different physical
    assumptions and must not be conflated.
  ]

  #knowledge-check((
    (
      question: [Where does the factor of c enter the Gaussian-CGS classical diffusion coefficient?],
      answer: [It enters through both $(bold(j) times bold(B))/c$ in force
      balance and $(bold(u) times bold(B))/c$ in Ohm's law. Solving the
      perpendicular balance therefore produces the explicit $c^2$ in
      $D_perp^("cl")$.]
    ),
    (
      question: [What magnetic-field scaling distinguishes classical from Bohm-like diffusion?],
      answer: [The local classical result scales as $B^(-2)$, whereas the
      empirical Bohm estimate scales as $B^(-1)$ at fixed temperature.]
    ),
    (
      question: [How is a diffusion loss time estimated from a coefficient?],
      answer: [For a characteristic length $L$, use
      $tau_"D"=L^2/D$. Geometry changes the numerical factor, but not the
      basic dimensional scaling.]
    ),
    (
      question: [Why should a Bohm coefficient be labelled empirical?],
      answer: [Its $B^(-1)$ dependence summarizes anomalous transport linked
      to turbulence; it is not derived from the local collisional force balance
      used for $D_perp^("cl")$.]
    ),
  ))

  #chapter-nav(
    previous: (
      href: "07-collisions-conductivity.html",
      title: [Collisions and conductivity],
    ),
    next: (
      href: "09-introduction-waves.html",
      title: [Introduction to waves],
    ),
  )
]
