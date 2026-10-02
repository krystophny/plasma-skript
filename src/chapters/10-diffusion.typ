#import "../theme.typ": *
#import "../figures.typ": random-walk-diffusion, ambipolar-balance, cross-field-diffusion, diffusion-scalings
#import "@preview/physica:0.9.8": div, grad, pdv, laplacian
#import "@preview/unify:0.8.1": qty, unit

#let chapter = [
  #page-title(number: 10)[Plasma diffusion] <plasma-diffusion>

  #lead[
    Diffusion is the macroscopic signature of many small changes in particle
    trajectories. Collisions randomize particle directions. Across a density
    gradient, more particles arrive from the dense side than from the dilute
    side, producing a net flux toward lower density even when individual
    steps are symmetric. Magnetic fields do not
    remove diffusion, but they make the transport direction dependent.
    This transport hierarchy follows the standard collisional and magnetized
    plasma description in @bittencourt2004.
  ]

  #callout(
    [Microscopic origin of $D$],
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
    A diffusion coefficient $D$ is in #unit("m^2/s"), and particle flux
    $bold(Gamma)$ is in #unit("m^-2/s"). The normalized variables $xi=x\/L_0$
    and $tau=t\/tau_0$ are dimensionless. In the one-dimensional Green
    function,

    $ N_0=integral_(-infinity)^infinity n(x,t) dif x $

    is the
    conserved column density in #unit("m^-2").
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
    $D=(Delta x)^2\/(2 Delta t)$. The diffusive particle flux obeys Fick's law
    $bold(Gamma)^(D)=-D grad(n)$, and a system of size $L$ has
    the characteristic diffusion time
    $tau_"D"=L^2\/D$. This is a scale estimate; a precise decay time also
    depends on geometry and boundary conditions. For particles starting at
    the origin with the same diffusivity in all three directions, the
    variance relation is
    $⟨abs(bold(r))^2⟩=6 D t$.]
  )

  Angle brackets denote an ensemble average over possible random walks.
  A finite collection of walkers need not have exactly zero mean at each
  time. The ensemble variance describes spreading around the starting point,
  not a directed displacement of the whole cloud.

  #details(
    [Derivation: from step statistics to the diffusion equation],
    [#derivation-step[Compute the moments of one random step]
    Let one step be $+Delta x$ or $-Delta x$ with equal probability. Then

    $ ⟨Delta x⟩=(Delta x)/2+(-Delta x)/2=0, quad
      ⟨(Delta x)^2⟩=((Delta x)^2)/2+((-Delta x)^2)/2=(Delta x)^2 . $

    #derivation-step[Accumulate independent steps]
    After $N=t\/(Delta t)$ statistically independent steps, cross terms in the
    squared displacement vanish because the individual means are zero. Thus

    $ ⟨x⟩=0, quad
      ⟨x^2⟩=N(Delta x)^2
        =(((Delta x)^2 t)/(Delta t))=2 D t . $

    This defines the one-dimensional coefficient
    $D=(Delta x)^2\/(2 Delta t).$

    #derivation-step[Derive the local diffusive flux]
    Consider a cell of width $Delta x$. Right-moving and left-moving
    populations sample densities displaced by one step. Expanding those
    densities to first order gives

    $ bold(Gamma)^(D)=-((Delta x)^2/(2 Delta t)) grad(n)=-D grad(n) . $

    Particle conservation is

    $ pdv(n,t)+div(bold(Gamma))=0 . $

    #derivation-step[Obtain the diffusion equation and Green function]
    Substitution yields

    $ pdv(n,t)=div(D grad(n)) . $

    For uniform $D$, this reduces to $pdv(n,t, style: "horizontal")=D laplacian(n)$. A point-like
    initial sheet $n(x,0)=N_0 delta(x)$ has Green-function solution

    $ n(x,t)=N_0/sqrt(4 pi D t) exp(-x^2/(4 D t)) . $

    Its second moment is $⟨x^2⟩=2 D t$. Independent Cartesian directions add,
    giving $⟨abs(bold(r))^2⟩=6 D t$ in three dimensions.]
  )

  #governing-law(
    [A normalized diffusion equation],
    [Choose reference length $L_0$ in #unit("m"), time $tau_0$ in
    #unit("s"), and density $n_0$ in #unit("m^-3"). Define the reference
    coefficient $D_0=L_0^2\/tau_0$ in #unit("m^2/s") and the dimensionless
    variables
    $bold(xi)=bold(r)\/L_0$, $tau=t\/tau_0$,
    $n_("norm")=n\/n_0$, and $D_("norm")=D\/D_0$.
    Spatial derivatives below act on $bold(xi)$.
    The diffusion equation then has the dimensionless form

    $ pdv(n_("norm"), tau)=div(D_("norm") grad(n_("norm"))) . $

    For a system length $L$ with $L_("norm")=L\/L_0$, the normalized
    diffusion time is $tau_"D"\/tau_0=L_("norm")^2\/D_("norm")$.
    Every dimensional result is recovered by restoring the stated reference
    scales; no unit is hidden in a normalized axis or coefficient.]
  )

  #random-walk-diffusion

  #animation(
    "../media/diffusion-random-walk.mp4",
    "Thirty-six one-dimensional walkers start at the origin and take eighteen seeded symmetric steps. Position is xi=x/L0 and time is tau=t/tau0, with step magnitude 0.34 and step duration 1 in these normalized units. The ensemble mean is zero, while the finite sample fluctuates. Selected path traces show spreading; the ensemble variance is 2 D-star tau with D-star=0.0578.",
    caption: [
      Random-walk spreading from 36 walkers taking 18 seeded independent
      symmetric steps. With $xi=x\/L_0$ and $tau=t\/tau_0$, each step has
      magnitude $Delta xi=0.34$ [1] and duration $Delta tau=1$ [1]. The
      coefficient $D_*=D tau_0\/L_0^2=0.0578$ [1] is
      $D_("norm")$ defined above. Restore dimensional steps as
      $Delta x=0.34 L_0$ and $Delta t=tau_0$. The ensemble mean is zero and
      its variance is $2 D_* tau$; finite-sample means and variances fluctuate.
    ],
    poster: "../media/diffusion-random-walk.png",
  )

  #rechenbeispiel[
    Assume independent symmetric one-dimensional steps in a neutral-collision
    model, with no directed drift. The model has a step
    magnitude
    $Delta x=qty("2.0e-3", "m")$ every
    $Delta t=qty("1.0e-7", "s")$. For a device of length
    $L=qty("1.0e-1", "m")$, determine the diffusion coefficient and the
    characteristic diffusion time.

    Numerical result: $D=qty("2.0e1", "m^2/s")$ and
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
    $bold(Gamma)^(D)=-D grad(n)$ and particle conservation produce
    $pdv(n,t, style: "horizontal")=div(D grad(n))$, with the scale
    $tau_"D"=L^2\/D$.
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
    $bold(Gamma)^(D)=-D grad(n)$. The coefficient $D$ measures the
      strength of that response.]
    ),
    (
      question: [How does the characteristic diffusion time scale with system size?],
      answer: [For a fixed coefficient, $tau_"D"=L^2\/D$, so doubling the
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
    The mobility $mu_s$ has units of velocity divided by electric field,
    #unit("m^2/V/s"), and $D_s$ is in #unit("m^2/s"). This electric-field
    mobility includes charge, unlike the force-based mobility introduced in
    Chapter 9.
  ]

  #assumption(
    [Local, isothermal neutral drag],
    [Use a weakly ionized plasma with a prescribed stationary neutral background, a
    constant momentum-transfer frequency $nu_s$, small drift relative to the
    thermal speed, and no magnetic field in this section. Let the species
    pressure be $p_s=n_s k_B T_s$, with spatially uniform $T_s$, and consider
    evolution slow compared with the momentum-relaxation time $1\/nu_s$.
    Neglect inertia in that regime.]
  )

  #definition(
    [Mobility and diffusion],
    [The species momentum equation is

    $ m_s n_s (pdv(bold(u)_s,t)+bold(u)_s dot grad(bold(u)_s))
      =q_s n_s bold(E)-grad(p_s)
      -m_s n_s nu_s bold(u)_s . $

    In the steady small-drift limit,
    $bold(u)_s=mu_s^(q) bold(E)-D_s (grad(n_s)\/n_s)$,
    where the signed mobility and diffusion coefficient are
    $mu_s^(q)=q_s\/(m_s nu_s)$ and
    $D_s=k_B T_s\/(m_s nu_s)$.]
  )

  #governing-law(
    [Weakly ionized drift-diffusion flux],
    [Multiplying the velocity law by $n_s$ gives
    $bold(Gamma)_s=n_s mu_s^(q) bold(E)-D_s grad(n_s)$.
    If a positive mobility is preferred, define
    $mu_s=abs(q_s)\/(m_s nu_s)$. The electric drift is then along the field
    for positive charges and opposite to it for electrons; multiply the
    mobility by the charge sign, not by the charge magnitude again.
    The Einstein relation is
    $D_s=mu_s k_B T_s\/abs(q_s)$.]
  )

  #details(
    [Derivation: collisional force balance],
    [#derivation-step[Apply the isothermal pressure law]
    Start with the species momentum equation and use

    $ grad(p_s)=k_B T_s grad(n_s) . $

    #derivation-step[Take the long-time force balance]
    On times longer than $nu_s^(-1)$, neglect inertia and solve

    $ m_s n_s nu_s bold(u)_s
        =q_s n_s bold(E)-k_B T_s grad(n_s) . $

    Division by $m_s n_s nu_s$ gives

    $ bold(u)_s=q_s/(m_s nu_s) bold(E)
        -(k_B T_s)/(m_s nu_s) ((grad(n_s))/n_s) . $

    #derivation-step[Identify mobility and diffusion]
    Define the signed mobility and diffusion coefficient

    $ mu_s^(q)=q_s/(m_s nu_s), quad
      D_s=(k_B T_s)/(m_s nu_s) . $

    Multiplication by $n_s$ produces the particle flux. With the positive
    mobility magnitude
    $abs(mu_s^(q))=abs(q_s)\/(m_s nu_s)$, the Einstein relation is

    $ D_s/abs(mu_s^(q))=(k_B T_s)/abs(q_s) . $

    #derivation-step[State the approximation boundary]
    The derivation assumes local, isothermal, unmagnetized drag. Inertia
    matters when the forcing varies on a time comparable to $nu_s^(-1)$, and
    a scalar coefficient is insufficient when a magnetic field makes the
    response tensorial.]
  )

  #rechenbeispiel[
    Assume local, isothermal, steady, unmagnetized neutral drag with
    negligible inertia. For electrons in a weakly
    ionized plasma, use
    $k_B T_e=qty("2.0", "eV")=qty("3.204e-19", "J")$,
    $m_e=qty("9.109e-31", "kg")$,
    $e=qty("1.602e-19", "C")$, and
    $nu_e=qty("1.0e8", "s^-1")$. Determine the positive mobility magnitude
    $mu_e=e\/(m_e nu_e)$ and the diffusion coefficient
    $D_e=k_B T_e\/(m_e nu_e)$.

    Numerical result: $mu_e=qty("1.76e3", "m^2/V/s")$ and
    $D_e=qty("3.52e3", "m^2/s")$.
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
    $bold(Gamma)_s=n_s mu_s^(q) bold(E)-D_s grad(n_s)$ with
    $mu_s^(q)=q_s\/(m_s nu_s)$ and
    $D_s=k_B T_s\/(m_s nu_s)$. The Einstein relation connects their
    magnitudes, while the sign of the force response remains set by $q_s$.
  ]

  #knowledge-check((
    (
      question: [Which term in the weakly ionized flux is driven by a density gradient?],
      answer: [The Fick term $-D_s grad(n_s)$ is gradient driven. It points
      down the density gradient and is distinct from the electric-force term.]
    ),
    (
      question: [How does increasing the neutral collision frequency affect unmagnetized diffusion?],
      answer: [At fixed temperature, $D_s=k_B T_s\/(m_s nu_s)$ decreases
      inversely with $nu_s$ because the mean free path and drift response are
      both shortened.]
    ),
    (
      question: [Why must the charge sign be kept separate from the positive mobility magnitude?],
      answer: [Electrons and ions drift in opposite directions under the same
      electric field. With $mu_s=abs(q_s)\/(m_s nu_s)$, the electric drift
      is $+mu_s bold(E)$ for positive ions and $-mu_s bold(E)$ for electrons.
      The charge magnitude is already included in $mu_s$.]
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
    The resulting charge separation creates an electric field that couples
    their transport. With zero-current boundary conditions in the transport
    direction, the field adjusts until the species carry the same particle
    flux. This coupled transport is ambipolar diffusion.
  ]

  #objectives((
    [write the electron and ion fluxes with explicit charge signs],
    [derive the ambipolar electric field from equal particle fluxes],
    [obtain the ambipolar diffusion coefficient],
    [explain the role of quasi-neutrality and zero net current],
  ))

  #unit-ledger[
    The ambipolar diffusion coefficient $D_a$ is in #unit("m^2/s").
  ]

  #assumption(
    [Quasi-neutral, singly charged hydrogen],
    [Use $n_i approx n_e=n$, $q_i=+e$, $q_e=-e$, spatially uniform
    temperatures within each species, and zero current in the transport
    direction, fixed by the boundary conditions. The temperatures of the
    two species may differ.
    The electron and ion drift-diffusion coefficients are evaluated locally,
    and the ambipolar field adjusts faster than the density profile evolves.]
  )

  #definition(
    [Species fluxes and quasi-neutrality],
    [With positive mobility magnitudes, the unmagnetized fluxes are
    $bold(Gamma)_i=mu_i n bold(E)-D_i grad(n)$ and
    $bold(Gamma)_e=-mu_e n bold(E)-D_e grad(n)$.
    The current is
    $bold(j)=e (bold(Gamma)_i-bold(Gamma)_e)$.
    The zero-current closure used here imposes
    $bold(j)=bold(0)$, equivalently
    $bold(Gamma)_i=bold(Gamma)_e$.]
  )

  Charge conservation gives $pdv(rho_q,t, style: "horizontal")+div(bold(j))=0$. Maintaining
  quasi-neutrality therefore constrains the leading current divergence;
  it does not require $bold(j)=bold(0)$. In one-dimensional steady transport,
  current is spatially constant, and a zero-current boundary sets that
  constant to zero. This additional condition gives the equal fluxes used
  below.

  #governing-law(
    [Ambipolar field and diffusion coefficient],
    [Solving the equal-flux condition gives

    $ bold(E)_a=((D_i-D_e)/(mu_i+mu_e)) ((grad(n))/n) . $

    Substitution into either species flux gives
    $bold(Gamma)_a=-D_a grad(n)$ with
    $D_a=(mu_i D_e+mu_e D_i)\/(mu_i+mu_e)$.]
  )

  #details(
    [Derivation: quasi-neutral flux balance],
    [#derivation-step[Write the two species fluxes]
    For positive ions, the electric force drives a flux in the direction of
    $bold(E):$

    $ bold(Gamma)_i=mu_i n bold(E)-D_i grad(n) . $

    Electrons have the opposite charge:

    $ bold(Gamma)_e=-mu_e n bold(E)-D_e grad(n) . $

    #derivation-step[Impose zero current]
    The current-free condition is

    $ bold(0)=bold(j)=e(bold(Gamma)_i-bold(Gamma)_e) . $

    Equating the two fluxes and collecting the field terms gives

    $ (mu_i+mu_e)n bold(E)=(D_i-D_e)grad(n) . $

    Hence

    $ bold(E)_a=((D_i-D_e)/(mu_i+mu_e)) ((grad(n))/n) . $

    #derivation-step[Insert the ambipolar field into the flux]
    The ion flux becomes

    $ bold(Gamma)_i
        =((mu_i n (D_i-D_e))/(mu_i+mu_e)) ((grad(n))/n)
        -D_i grad(n) . $

    Putting both terms over the common denominator produces

    $ bold(Gamma)_i
        =-(mu_i D_e+mu_e D_i)/(mu_i+mu_e) grad(n) . $

    The same result follows from the electron flux, so define

    $ D_a=(mu_i D_e+mu_e D_i)/(mu_i+mu_e) . $

    #derivation-step[Interpret the mobility hierarchy]
    For equal temperatures and comparable collision models, often
    $mu_e >> mu_i$. Then

    $ D_a approx D_i+(mu_i/mu_e) D_e . $

    Electron diffusion is consequently largely converted into the ambipolar
    electric field rather than a net current.]
  )

  #ambipolar-balance

  #rechenbeispiel[
    Assume local isothermal neutral drag in a weakly ionized, quasi-neutral,
    singly charged hydrogen plasma with no externally imposed current. Let
    the ambipolar field adjust rapidly compared with the
    density evolution. Consider the plasma with
    $n=qty("1.0e16", "m^-3")$,
    $grad(n)\/n=qty("-1.0", "m^-1")$, and
    $k_B T_i=k_B T_e=qty("1.0", "eV")=qty("1.602e-19", "J")$.
    Use $m_i=qty("1.673e-27", "kg")$,
    $m_e=qty("9.109e-31", "kg")$,
    $e=qty("1.602e-19", "C")$,
    $nu_i=qty("1.0e7", "s^-1")$, and
    $nu_e=qty("1.0e9", "s^-1")$. Determine the ambipolar field,
    coefficient, and particle flux.

    Numerical result:
    $bold(E)_a=qty("0.897", "V/m")$,
    $D_a=qty("1.82e1", "m^2/s")$, and
    $abs(bold(Gamma)_a)=qty("1.82e17", "m^-2/s")$.
  ]

  #interpretation(
    [Quasi-neutrality couples otherwise unequal rates],
    [The ambipolar field is generated by the species' unequal diffusion. A
    small departure from charge neutrality can support a field strong enough
    to slow the faster species and accelerate the slower one. Their equal
    particle fluxes point in the same direction: opposite charges cancel in
    the current, while both populations continue to spread.]
  )

  #summary[
    Equal electron and ion particle fluxes give

    $ bold(E)_a=((D_i-D_e)/(mu_i+mu_e)) ((grad(n))/n) $

    and
    $bold(Gamma)_a=-D_a grad(n)$, where
    $D_a=(mu_i D_e+mu_e D_i)\/(mu_i+mu_e)$. Ambipolar diffusion here
    follows from quasi-neutrality together with the zero-current
    boundary condition.
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
    [identify the magnetization parameter $abs(Omega_s)\/nu_s$],
    [separate ordinary diffusion from Hall-like transverse response],
    [explain why the collisionless limit suppresses classical cross-field diffusion],
  ))

  #unit-ledger[
    The magnetization parameter $abs(Omega_s)\/nu_s$ is dimensionless.
    Parallel, perpendicular, and Hall diffusion coefficients are in
    #unit("m^2/s").
  ]

  #assumption(
    [Uniform magnetic field and isotropic drag],
    [Use a locally uniform $bold(B)=B hat(bold(b))$, a scalar collision
    frequency for drag against stationary neutrals, small drift, spatially
    uniform species temperature, and a time-independent field. Pressure gradients
    and electric fields vary slowly over one gyration. Curvature, mirrors,
    finite orbit widths, and turbulence are postponed.]
  )

  #definition(
    [Magnetized diffusion tensor],
    [Let $Omega_s=q_s B\/m_s$ and
    $D_s=k_B T_s\/(m_s nu_s)$. The parallel coefficient is
    $D_(s,parallel)=D_s$, while
    $D_(s,perp)=D_s\/(1+(Omega_s\/nu_s)^2)$.
    A signed transverse coefficient is

    $ D_(s,H)=(D_s (Omega_s/nu_s))/(1+(Omega_s/nu_s)^2) . $

    The gradient contribution can be written

    $ bold(Gamma)_(s,perp)=-D_(s,perp)grad_(perp)(n_s)
      +D_(s,H) hat(bold(b)) times grad_(perp)(n_s) , $

    in the chosen orientation convention.]
  )

  #details(
    [Derivation: solving the perpendicular momentum balance],
    [#derivation-step[Write the perpendicular linear system]
    For $bold(B)=B hat(bold(z))$, arrange the steady perpendicular momentum
    equation as

    $ mat(nu_s,-Omega_s;Omega_s,nu_s)
        mat(u_(s,x);u_(s,y))
        =(q_s/m_s) mat(E_x;E_y)
        -(k_B T_s)/(m_s n_s) mat(pdv(n_s,x);pdv(n_s,y)) . $

    #derivation-step[Invert the drag--gyro matrix]
    Its inverse is

    $ (1)/(nu_s^2+Omega_s^2)
        mat(nu_s,Omega_s;-Omega_s,nu_s) . $

    #derivation-step[Read off the diffusion tensor]
    The gradient part of the flux has diagonal coefficient

    $ (k_(B) T_s nu_s)/(m_(s)(nu_s^2+Omega_s^2))
        =(D_s nu_s^2)/(nu_s^2+Omega_s^2) , $

    and signed off-diagonal coefficient

    $ (k_(B) T_s Omega_s)/(m_(s)(nu_s^2+Omega_s^2))
        =(D_s nu_s Omega_s)/(nu_s^2+Omega_s^2) . $

    These are the displayed $D_(s,perp)$ and $D_(s,H)$.

    #derivation-step[Check the strongly magnetized limit]
    The electric-force part contains the crossed-field drift

    $ bold(u)_(E times B)=(bold(E) times bold(B))/(B^2) . $

    When $abs(Omega_s)>>nu_s$,

    $ D_(s,perp) approx D_(s)(nu_s/Omega_s)^2 . $

    Thus $nu_s -> 0$ suppresses classical cross-field diffusion: without
    interruptions, guiding centers do not make a collisional random walk
    across field lines.

    #derivation-step[Relate the coefficient to the thermal gyroradius]
    With the Chapter 1 convention,

    $ v_("th,s")=sqrt((2 k_B T_s)/m_s), quad
      rho_("th,s")=v_("th,s")/abs(Omega_s) . $

    Therefore

    $ rho_("th,s")^2=(2 k_B T_s)/(m_s Omega_s^2), quad
      D_(s,perp) approx (nu_s/2) rho_("th,s")^2 . $

    An alternative one-dimensional scale would give
    $D_(s,perp) approx nu_s rho_("1D,s")^2$; it is not the thermal gyroradius
    convention used elsewhere in this script.]
  )

  For constant field direction $bold(b)$ and constant $D_(s,H)$, the
  Hall-like gradient flux $D_(s,H) bold(b) times grad(n_s)$ has zero
  divergence, since mixed spatial derivatives commute. It does not by itself
  broaden a density packet. Spatial variation of the coefficient or field
  direction, and boundary fluxes, can change that conclusion.

  The formal collisionless limit requires care. At fixed nonzero magnetic
  field, the classical perpendicular coefficient tends to zero. The parallel
  formula instead grows as $1\/nu_s$; once the mean free path is comparable
  to the system length, local diffusion along the field no longer applies.
  Particles then retain memory of their motion and boundaries.

  #cross-field-diffusion

  #rechenbeispiel[
    Assume a local uniform magnetic field, isotropic steady collisional drag
    and the scalar diffusion model derived above. Ignore field
    curvature, finite-orbit effects, and turbulence. For electrons at
    $k_B T_e=qty("1.0", "eV")=qty("1.602e-19", "J")$, use
    $m_e=qty("9.109e-31", "kg")$,
    $e=qty("1.602e-19", "C")$,
    $B=qty("1.0e-2", "T")$, and
    $nu_e=qty("1.0e7", "s^-1")$. Determine the magnitude of the cyclotron
    frequency, the parallel coefficient, and the perpendicular coefficient.

    Numerical result:
    $abs(Omega_e)=qty("1.76e9", "s^-1")$,
    $D_(e,parallel)=qty("1.76e4", "m^2/s")$,
    $D_(e,perp)=qty("0.569", "m^2/s")$, and
    $D_(e,perp)\/D_(e,parallel)=qty("3.23e-5", "1")$.
  ]

  #interpretation(
    [Ambipolarity depends on geometry],
    [The zero-current closure used in the preceding section does not force
    transverse electron and ion fluxes to match in every geometry. Rapid
    parallel electron transport can short-circuit a charge imbalance created
    by unequal cross-field fluxes. Whether a loss is ambipolar therefore also
    depends on field-line connection and boundary conditions.]
  )

  #interpretation(
    [Collisions facilitate cross-field transport],
    [More collisions shorten the free path, yet a nonzero collision rate is needed to break the
    indefinite gyromotion. The competition is measured by
    $abs(Omega_s)\/nu_s$: it is small for nearly isotropic transport and
    large for strong perpendicular suppression.]
  )

  #summary[
    A magnetic field leaves $D_parallel=D_s$ but reduces the classical
    cross-field coefficient to
    $D_perp=D_s\/(1+(Omega_s\/nu_s)^2)$. The signed Hall-like coefficient
    describes a transverse response; in the strongly magnetized limit
    $D_(s,perp)$ scales as $(nu_s\/2) rho_("th,s")^2$ under the thermal-speed
    convention used in Chapter 1.
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
      answer: [The ratio $abs(Omega_s)\/nu_s$ compares the gyration rate with
      the collision rate. It is the control parameter in the tensor
      coefficients.]
    ),
    (
      question: [What happens to classical cross-field diffusion as collisions vanish?],
      answer: [For fixed $B$ it tends to zero as
      $D_perp approx D_(s)(nu_s\/Omega_s)^2$. A collisionless particle remains
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
    The classical and Bohm-like diffusion coefficients are in #unit("m^2/s").
  ]

  #assumption(
    [Quasi-neutral, weakly coupled fluid transport],
    [Use a fully ionized, quasi-neutral hydrogen plasma with a scalar
    conductivity, a locally uniform magnetic field, and steady perpendicular
    force balance. Take each species temperature to be spatially uniform,
    though the electron and ion temperatures may differ. The classical result
    neglects turbulent fluctuations and
    finite-orbit neoclassical geometry. Bohm transport is presented only as
    an empirical comparison.]
  )

  #definition(
    [Classical fully ionized diffusion],
    [The steady force balance and resistive Ohm law are
    $bold(0)=-grad(p)+bold(j) times bold(B)$ and
    $bold(j)=sigma (bold(E)+bold(u) times bold(B))$.
    The perpendicular velocity contains

    $ bold(u)_perp=(bold(E) times bold(B))/(B^2)
      -(grad_(perp)(p))/(sigma B^2) . $

    For $p=n k_(B)(T_e+T_i)$, the pressure-driven flux is
    $bold(Gamma)_perp=-D_perp^("cl") grad_(perp)(n)$ with

    $ D_perp^("cl")=(n k_(B)(T_e+T_i))/(sigma B^2)
      =(eta n k_(B)(T_e+T_i))/(B^2) . $
    ]
  )

  #governing-law(
    [Classical and Bohm-like scalings],
    [At fixed density, temperatures, and conductivity,
    $D_perp^("cl") ∝ B^(-2)$. A commonly used empirical Bohm estimate is
    $D_perp^(B) approx k_B T_e\/(16 e B)$,
    so $D_perp^(B) ∝ B^(-1)$. The numerical factor is empirical and
    should not be mistaken for a derivation from the collisional model.]
  )

  The coefficient here describes particle transport. It is different from
  the magnetic diffusivity $D_(B)$ of Chapter 8, which describes resistive
  smoothing of the magnetic field. In $D_perp^(B)$ above, the superscript
  labels the Bohm estimate. The identical diffusion units do not make these
  coefficients interchangeable.

  #details(
    [Derivation: pressure-driven classical flux],
    [#derivation-step[Combine force balance with Ohm's law]
    Start from

    $ bold(0)=-grad(p)+bold(j) times bold(B) $

    and substitute

    $ bold(j)=sigma(bold(E)+bold(u) times bold(B)) . $

    Using

    $ (bold(u) times bold(B)) times bold(B)=-B^2 bold(u)_perp $

    gives

    $ bold(0)=-grad_(perp)(p)
        +sigma (bold(E) times bold(B))
        -sigma B^2 bold(u)_perp . $

    #derivation-step[Solve for the perpendicular velocity]
    Rearranging gives

    $ bold(u)_perp=(bold(E) times bold(B))/(B^2)
        -(grad_(perp)(p))/(sigma B^2) . $

    #derivation-step[Identify the pressure-driven diffusion]
    Multiply by $n$. The first term is a common crossed-field drift and does
    not diffuse a uniform density. For an isothermal two-temperature hydrogen
    plasma,

    $ grad_(perp)(p)=k_(B)(T_e+T_i)grad_(perp)(n) . $

    The pressure term in the particle flux is consequently

    $ bold(Gamma)_perp^("diff")
        =-(n k_(B)(T_e+T_i) grad_(perp)(n))/(sigma B^2) . $

    Therefore

    $ D_perp^("cl")=(n k_(B)(T_e+T_i))/(sigma B^2)
        =(eta n k_(B)(T_e+T_i))/(B^2) . $

    The factor $1\/B^2$ arises because the field enters twice: once through
    the Lorentz force density $bold(j) times bold(B)$ and once through the
    motional term $bold(u) times bold(B)$ in Ohm's law.

    #derivation-step[State the comparison with anomalous transport]
    The classical loss time for a macroscopic length $L$ is

    $ tau_"D"=L^2/D_perp^("cl") . $

    The Bohm expression is not obtained by this force-balance derivation; it
    is a phenomenological comparison motivated by turbulent or anomalous
    transport. Neoclassical calculations add field geometry, trapped-particle
    orbits, and finite collisionality.]
  )

  #diffusion-scalings

  #rechenbeispiel[
    Assume a quasi-neutral, fully ionized hydrogen plasma in steady classical
    perpendicular force balance, with scalar conductivity.
    Neglect turbulent and finite-orbit corrections; use the Bohm expression
    only as an empirical comparison. For the plasma, use
    $n=qty("1.0e16", "m^-3")$,
    $k_B T_e=k_B T_i=qty("10", "eV")=qty("1.602e-18", "J")$,
    $sigma=qty("1.0e5", "S/m")$,
    $B=qty("1.0e-2", "T")$, and
    $e=qty("1.602e-19", "C")$. Determine the classical coefficient,
    the Bohm estimate, and their ratio. For a device of length
    $L=qty("1.0", "m")$, also estimate the classical diffusion time.

    Numerical result:
    $D_perp^("cl")=qty("3.20e-3", "m^2/s")$,
    $D_perp^(B)=qty("6.25e1", "m^2/s")$,
    $D_perp^(B)\/D_perp^("cl")=qty("1.95e4", "1")$, and
    $tau_"D"^("cl")=qty("3.12e2", "s")$.
  ]

  #interpretation(
    [Classical, neoclassical, and anomalous transport],
    [The $B^(-2)$ classical law is a collisional consequence of the local
    force balance. Neoclassical transport modifies it through magnetic
    geometry and orbit effects. A Bohm-like $B^(-1)$ law is an empirical
    anomalous scaling associated with unresolved turbulence; it is not a
    replacement for stating the collision and geometry model.]
  )

  #summary[
    Fully ionized classical transport gives

    $ D_perp^("cl")=(n k_(B)(T_e+T_i))/(sigma B^2) $

    and
    $tau_"D"=L^2\/D$. It scales as $B^(-2)$, while the empirical Bohm
    estimate scales as $B^(-1)$. The two rest on different physical
    assumptions.
  ]

  #knowledge-check((
    (
      question: [Why does the classical diffusion coefficient scale as $B^(-2)$ rather than $B^(-1)$?],
      answer: [The field enters through both $bold(j) times bold(B)$ in force
      balance and $bold(u) times bold(B)$ in Ohm's law. Solving the
      perpendicular balance therefore produces the factor $1\/(sigma B^2)$ in
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
      $tau_"D"=L^2\/D$. Geometry changes the numerical factor, but not the
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
      href: "09-collisions-conductivity.html",
      title: [Collisions and conductivity],
    ),
    next: (
      href: "11-introduction-waves.html",
      title: [Introduction to waves],
    ),
  )
]
