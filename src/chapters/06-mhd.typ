#import "../theme.typ": *
#import "../figures.typ": mhd-reduction, mhd-ohm-balance, mhd-flux-diffusion, mhd-force-balance
#import "@preview/physica:0.9.8": div, grad, pdv, dv, curl, laplacian
#import "@preview/unify:0.8.1": qty, unit

#let chapter = [
  #page-title[6. Single-fluid theory and magnetohydrodynamics] <single-fluid-mhd>

  #lead[
    A single-fluid plasma model keeps the mass-weighted motion of all species
    and treats the magnetic field as a dynamical continuum variable. It is
    useful only after the species differences have been ordered: charge
    separation is small, collisions or inertia control the current response,
    and the pressure and heat flux have been closed. This chapter makes those
    reductions explicit before using the compact name MHD.
  ]

  #callout(
    [The MHD reduction has a visible logic],
    [Add species equations to obtain mass and momentum. Take an appropriate
    species difference to obtain generalized Ohm's law. Then state which
    terms are small before reducing the field equations to ideal or resistive
    MHD. The same sequence explains both the power and the limits of the
    model.]
  )

  #section-title[Single-fluid variables and conservation laws] <mhd-definitions>

  #lead[
    What does a one-fluid variable mean when electrons and ions still move
    differently? It is a carefully chosen sum, not an assertion that all
    species share one velocity. The mass-weighted velocity carries total
    momentum, while charge-weighted velocity differences still define the
    current.
  ]

  #objectives((
    [define the mass, charge, current, pressure, and velocity variables of a single-fluid model],
    [derive total mass and charge conservation from species balances],
    [identify the relative-flow stress retained in the summed momentum flux],
    [separate exact sums from quasi-neutral and one-fluid approximations],
  ))

  #unit-ledger[
    Gaussian CGS is active. Mass density is in #unit("g/cm^3"), velocity in
    #unit("cm/s"), pressure in #unit("erg/cm^3"), magnetic field in gauss,
    electric field in statvolt per #unit("cm"), and current density in
    statcoulomb per #unit("cm^2") per #unit("s"). The magnetic force density
    is in #unit("g") #unit("cm^-2") #unit("s^-2"); the factor $1/c$ in
    $(bold(j) times bold(B))/c$ belongs to Gaussian CGS.
  ]

  #definition(
    [Single-fluid variables are weighted sums],
    [Let $rho=sum_s rho_(s)$ be the total mass density and define the mass
    velocity by $rho bold(u)=sum_s rho_(s) bold(u)_(s)$. With
    $bold(V)_(s)=bold(u)_(s)-bold(u)$, the total pressure/transport tensor is
    $bold(P) = sum_s bold(P)_(s) + sum_s rho_(s) bold(V)_(s) bold(V)_(s)$.
    The charge density and current remain charge-weighted:
    $rho_q=sum_s q_(s)n_(s)$ and
    $bold(j)=sum_s q_(s)n_(s)bold(u)_(s)$.]
  )

  For the hydrogen plasma used here, $q_(e)=-e$, $q_(i)=+e$, and the mass
  velocity is approximately the ion velocity only when $m_(i) >> m_(e)$ and
  the current correction is small. Quasi-neutrality is the ordering
  $rho_q approx 0$; it does not remove $bold(j)$.

  The exact summed mass balance is

  $ pdv(rho, t) + div(rho bold(u)) = 0 $ <mhd-mass-continuity>

  Charge-weighting the species continuity equations gives

  $ pdv(rho_q, t) + div(bold(j)) = 0 $ <mhd-charge-continuity>

  The summed momentum balance from the multiple-fluid chapter is

  $ pdv(rho bold(u), t)
    + div(rho bold(u) bold(u) + bold(P))
    = rho_q bold(E) + (bold(j) times bold(B))/c
      + sum_s bold(R)_(s) $ <mhd-momentum>

  For isolated elastic interspecies collisions,
  $sum_s bold(R)_(s)=bold(0)$. In a quasi-neutral, nonrelativistic ordering
  the electric force density $rho_q bold(E)$ is subleading in the bulk
  momentum equation, but the magnetic force density remains through the total
  current.

  #details(
    [Derivation: sum species moments without losing relative flow],
    [Start with the species continuity equations
    $pdv(n_(s),t)+div(n_(s)bold(u)_(s))=0$. Multiply each by the
    constant mass $m_(s)$ and sum:
    $sum_s m_(s)pdv(n_(s),t)+sum_s m_(s)div(n_(s)bold(u)_(s))=0$.
    Moving the sum through the derivatives gives
    $pdv(sum_s rho_(s),t)+div(sum_s rho_(s)bold(u)_(s))=0$.
    Insert $rho=sum_s rho_(s)$ and
    $rho bold(u)=sum_s rho_(s)bold(u)_(s)$ to obtain the total mass balance.

    Multiply instead by $q_(s)$ and sum. The first term becomes
    $pdv(sum_s q_(s)n_(s),t)=pdv(rho_q,t)$ and the spatial flux becomes
    $div(sum_s q_(s)n_(s)bold(u)_(s))=div(bold(j))$. This gives charge
    conservation. No quasi-neutral approximation was needed.

    For momentum, add the conservative species equations. The flux first
    contains $sum_s rho_(s)bold(u)_(s)bold(u)_(s)+sum_s bold(P)_(s)$. Write
    $bold(u)_(s)=bold(u)+bold(V)_(s)$. Since
    $sum_s rho_(s)bold(V)_(s)=bold(0)$, expansion gives
    $sum_s rho_(s)bold(u)_(s)bold(u)_(s)
      =rho bold(u)bold(u)+sum_s rho_(s)bold(V)_(s)bold(V)_(s)$.
    The last dyadic is the relative-flow stress and remains in $bold(P)$.

    The force sums are
    $sum_s q_(s)n_(s)bold(E)=rho_q bold(E)$ and
    $(sum_s q_(s)n_(s)(bold(u)_(s)times bold(B)))/c
      =(bold(j)times bold(B))/c$. Internal collision sources cancel only when
    their species sum is zero. These identities yield the displayed total
    momentum equation.]
  )

  #mhd-reduction

  #rechenbeispiel[
    Context: a quasi-neutral hydrogen plasma has
    $n_(e)=n_(i)=qty("1.0e10", "cm^-3")$,
    $m_(e)=qty("9.109e-28", "g")$,
    $m_(i)=qty("1.673e-24", "g")$,
    $u_(i,x)=qty("2.0e7", "cm/s")$, and
    $u_(e,x)=qty("1.5e7", "cm/s")$. Use
    $e=qty("4.803e-10", "statC")$.

    Assumptions: singly charged species, equal densities, and one-dimensional
    flows along $x$.

    Target: report the total mass density, mass-weighted velocity, and
    $x$-directed current density.

    Numerical result: $rho=qty("1.674e-14", "g/cm^3")$,
    $u_x=qty("2.00e7", "cm/s")$, and
    $j_x=qty("2.40e7", "statC")$ per #unit("cm^2") per #unit("s").
  ]

  #interpretation(
    [One fluid does not mean one velocity for every species],
    [The mass velocity describes the center-of-mass motion. The current
    describes a charge-weighted relative motion, and the relative-flow stress
    stores the corresponding momentum flux. A one-fluid closure becomes
    accurate only when those additional variables are either small, prescribed,
    or related to the retained fields by another equation.]
  )

  #summary[
    Single-fluid variables are exact weighted sums of species moments. The mass
    balance is obtained by mass-weighting continuity, charge conservation by
    charge-weighting it, and momentum by adding the species momentum laws. The
    resulting pressure tensor includes relative-flow stress; quasi-neutrality
    constrains charge density but does not set current or species velocities to
    zero.
  ]

  #exam-prompts(
    (
      [(a) How are single-fluid mass, charge, current density, pressure and mass velocity defined?],
    ),
    [Plasma Physics Exam.pdf, p. 3, section 6(a)],
  )

  #knowledge-check((
    (
      question: [What weighting defines the single-fluid velocity?],
      answer: [Mass weighting defines it:
      $rho bold(u)=sum_s rho_(s)bold(u)_(s)$ with
      $rho=sum_s rho_(s)$. Charge weighting instead defines the current.]
    ),
    (
      question: [Which species difference can remain nonzero in a quasi-neutral plasma?],
      answer: [The velocity difference can remain nonzero. For hydrogen,
      $bold(j)=e n_(i)bold(u)_(i)-e n_(e)bold(u)_(e)$ can be finite even when
      $rho_q=e(n_(i)-n_(e)) approx 0$.]
    ),
    (
      question: [What extra term appears in the total pressure tensor?],
      answer: [The relative-flow stress
      $sum_s rho_(s)bold(V)_(s)bold(V)_(s)$ appears in addition to the sum of
      random pressure tensors. It disappears only when the relative flows are
      negligible or are closed separately.]
    ),
    (
      question: [What changes in the mass equation if the plasma is quasi-neutral?],
      answer: [Nothing at leading order: mass conservation remains
      $pdv(rho,t)+div(rho bold(u))=0$. Quasi-neutrality is a charge-density
      ordering, not a mass source or a velocity constraint.]
    ),
  ))

  #section-title[Generalized Ohm's law] <mhd-ohms-law>

  #lead[
    How does the current determine the electric field seen by the bulk plasma?
    The answer comes from the electron momentum equation. Subtracting or
    rearranging species momentum does not create an arbitrary constitutive law:
    the Hall, pressure, resistive, and electron-inertia terms each have a
    definite origin.
  ]

  #objectives((
    [derive the generalized Ohm-law balance from the electron equation],
    [identify the Hall, electron-pressure, resistive, and electron-inertia terms],
    [relate collisional drag to the scalar resistivity and conductivity],
    [state which ordering produces the ideal electric-field constraint],
  ))

  #unit-ledger[
    In Gaussian CGS, $bold(E)$ is in statvolt per #unit("cm"), $bold(j)$ is
    in statcoulomb per #unit("cm^2") per #unit("s"), and a scalar resistivity
    defined by $bold(E)=eta bold(j)$ has units #unit("s"). The electron
    pressure force per charge density is in statvolt per #unit("cm"). The
    coefficient $m_(e)/(e^2 n)$ multiplying a current time derivative has the
    units needed to produce an electric field.
  ]

  #assumption(
    [Two-species Ohm-law ordering],
    [Use a singly ionized hydrogen plasma with
    $n_(e) approx n_(i) approx n$, $m_(i) >> m_(e)$, and
    $bold(j)=e n (bold(u)_(i)-bold(u)_(e))$. Let $bold(u)$ be the mass
    velocity and use $bold(u)_(e) approx bold(u)-bold(j)/(e n)$ when the ion
    mass dominates. The generalized balance below keeps scalar electron
    pressure, collisional drag, and a leading current-inertia term; omitted
    electron convective-inertia and density-gradient terms must be small under
    the stated scale ordering.]
  )

  The electron momentum equation is

  $ m_(e)n (pdv(bold(u)_(e),t)
    + bold(u)_(e) dot grad(bold(u)_(e)))
    = -e n (bold(E) + (bold(u)_(e) times bold(B))/c)
      - grad(p_(e)) + bold(R)_(e) $ <mhd-electron-momentum>

  Solving it for the field in the electron frame and replacing
  $bold(u)_(e)$ by $bold(u)-bold(j)/(e n)$ gives the ordered generalized Ohm
  law

  $ bold(E) + (bold(u) times bold(B))/c
    = (bold(j) times bold(B))/(e n c)
      - (grad(p_(e)))/(e n)
      + eta bold(j)
      + m_(e)/(e^2 n) pdv(bold(j),t) $ <mhd-generalized-ohm>

  The four right-hand terms are, respectively, the Hall response, the
  electron-pressure or ambipolar response, collisional resistivity, and the
  leading electron-inertia response in a slowly varying bulk frame.

  For a linear electron--ion drag law, the force on electrons is

  $ bold(R)_(e) = m_(e)n nu_(e i)
    (bold(u)_(i)-bold(u)_(e))
    = (m_(e)nu_(e i) bold(j))/e $ <mhd-collisional-drag>

  Therefore

  $ eta = (m_(e)nu_(e i))/(n e^2),
    quad sigma = 1/eta = (n e^2)/(m_(e)nu_(e i)) $ <mhd-spitzer-resistivity>

  Here $nu_(e i)$ is the electron--ion momentum-transfer frequency. The
  frequency itself depends on the collision model and plasma state; the later
  collisions chapter supplies that kinetic input. In this chapter, the key
  point is that resistivity is drag per current, not an independent force.

  #details(
    [Derivation: locate every term in generalized Ohm's law],
    [Start with the electron material momentum equation and move the electric
    force to the left:
    $bold(E)+(bold(u)_(e)times bold(B))/c
      =-(grad(p_(e)))/(e n)+bold(R)_(e)/(e n)
        -(m_(e) (
          pdv(bold(u)_(e),t)
          + bold(u)_(e) dot grad(bold(u)_(e))))/e$,
    where the parenthesized sum is the electron material derivative.

    Add the difference between bulk and electron magnetic advection to both
    sides. Since
    $bold(u)-bold(u)_(e) approx bold(j)/(e n)$,
    $bold(E)+(bold(u)times bold(B))/c$
    equals the preceding right-hand side plus
    $(bold(j)times bold(B))/(e n c)$. This is the Hall term. It is the magnetic
    force expressed in the electron--bulk relative velocity.

    For a scalar electron pressure, the pressure force is already
    $-(grad(p_(e)))/(e n)$. If $n$ varies, it is useful to retain this form rather
    than split it into an electrostatic term and a density-gradient term; the
    distinction is a matter of ordering and closure.

    Model interspecies drag as a frictional force toward the ion velocity:
    $bold(R)_(e)=m_(e)n nu_(e i)(bold(u)_(i)-bold(u)_(e))$.
    Insert $bold(u)_(i)-bold(u)_(e)=bold(j)/(e n)$ to obtain
    $bold(R)_(e)/(e n)=(m_(e)nu_(e i)bold(j))/(n e^2)=eta bold(j)$.
    Thus $eta=(m_(e)nu_(e i))/(n e^2)$ and $sigma=1/eta$.

    Finally, write the electron velocity as
    $bold(u)_(e) approx bold(u)-bold(j)/(e n)$. In the slowly varying-density
    and slow-bulk-inertia ordering, the part of
    $-(m_(e) (
      pdv(bold(u)_(e),t)
      + bold(u)_(e) dot grad(bold(u)_(e))))/e$
    that depends on the current is
    $(m_(e)pdv(bold(j),t))/(e^2 n)$. If current advection or density variation is
    not small, this term must be replaced by the corresponding full
    electron-inertia operator; the displayed generalized law is then not
    sufficient.]
  )

  #mhd-ohm-balance

  #rechenbeispiel[
    Context: an electron--ion plasma has
    $n=qty("1.0e10", "cm^-3")$,
    $m_(e)=qty("9.109e-28", "g")$,
    $e=qty("4.803e-10", "statC")$, and
    $nu_(e i)=qty("2.54e3", "s^-1")$.

    Assumptions: scalar linear electron--ion drag, Gaussian-CGS resistivity,
    and the Spitzer form $eta=(m_(e)nu_(e i))/(n e^2)$.

    Target: report the scalar resistivity and conductivity.

    Numerical result: $eta=qty("1.00e-15", "s")$ and
    $sigma=qty("9.97e14", "s^-1")$.
  ]

  #interpretation(
    [The ideal field is a limit, not the starting equation],
    [If Hall, pressure, resistive, and electron-inertia terms are all small
    compared with $(bold(u)times bold(B))/c$, generalized Ohm's law reduces to
    $bold(E)+(bold(u)times bold(B))/c approx bold(0)$. If one correction is not
    small, the plasma is still a fluid but it is not described by ideal MHD.
    The ordering must be checked against the length, time, density, and field
    scales of the problem.]
  )

  #summary[
    Generalized Ohm's law is obtained from electron momentum. The Hall term
    comes from electron--bulk velocity difference, the pressure term from
    electron pressure, resistivity from collisional drag, and the current term
    from electron inertia. The ideal constraint is the result of ordering all
    four corrections below the bulk magnetic-advection term.
  ]

  #exam-prompts(
    (
      [(c) Sketch the derivation of Ohm’s law. Where does the current term finally come from? What’s the simplified form?],
      [(d) Relate collisional drag force to the current to get the Spitzer resistivity in terms of collision frequency.],
    ),
    [Plasma Physics Exam.pdf, p. 3, section 6(c)--(d)],
  )

  #knowledge-check((
    (
      question: [Which species equation is the most direct source of generalized Ohm's law?],
      answer: [The electron momentum equation is the direct source. Solving
      it for the electric field and replacing the electron--bulk velocity
      difference with $bold(j)/(e n)$ produces the Hall and current terms.]
    ),
    (
      question: [What physical process gives the scalar resistivity?],
      answer: [Electron--ion collisional drag gives
      $bold(R)_(e)=(m_(e)nu_(e i)bold(j))/e$, hence
      $eta=(m_(e)nu_(e i))/(n e^2)$. More frequent momentum transfer means
      larger resistivity and smaller conductivity.]
    ),
    (
      question: [When is the Hall term important?],
      answer: [It matters when
      $(bold(j)times bold(B))/(e n c)$ is not small compared with the bulk
      electric field. It is enhanced by large current, strong field, or low
      density and is absent only after a scale ordering justifies neglecting
      it.]
    ),
    (
      question: [What is the ideal-MHD electric-field condition in Gaussian CGS?],
      answer: [The condition is
      $bold(E)+(bold(u)times bold(B))/c=bold(0)$. It is a reduced generalized
      Ohm law and therefore requires all retained correction terms to be small.]
    ),
  ))

  #section-title[Linearized and simplified MHD equations] <mhd-linearized>

  #lead[
    Which finite set of equations is actually called MHD? After the current
    response has been ordered, the plasma can be described by mass density,
    bulk velocity, pressure, and magnetic field. Linearization around a
    uniform equilibrium then exposes the small-amplitude system that leads to
    the wave chapters.
  ]

  #objectives((
    [state the nonlinear ideal-MHD conservation laws and closures],
    [linearize mass, momentum, induction, and pressure equations about a uniform equilibrium],
    [define the sound-speed and magnetic-field constraints in the linear system],
    [distinguish a linear perturbation model from the underlying nonlinear equations],
  ))

  #unit-ledger[
    The dimensional MHD variables use Gaussian CGS: $rho$ in #unit("g/cm^3"),
    $bold(u)$ in #unit("cm/s"), $p$ in #unit("erg/cm^3"), and $bold(B)$ in
    gauss. The adiabatic sound speed
    $c_(s)=sqrt((gamma p_0)/rho_0)$ is in #unit("cm/s"). Perturbation symbols
    such as $(delta rho)/rho_0$, $(delta p)/p_0$, and
    $(delta bold(B))/B_0$ are dimensionless ratios.
  ]

  #assumption(
    [Simplified MHD ordering],
    [Use quasi-neutrality, negligible displacement current, isotropic pressure,
    negligible Hall and electron-pressure corrections, and a magnetic Reynolds
    number large enough for ideal induction. Close the pressure with the
    explicit material-derivative form
    $pdv(p rho^(-gamma),t)+bold(u) dot grad(p rho^(-gamma))=0$.
    For the linearized equations,
    take a static uniform equilibrium
    $(rho_0,p_0,bold(B)_0)$ with no equilibrium current or pressure gradient.]
  )

  The nonlinear ideal-MHD equations are

  $ pdv(rho,t) + div(rho bold(u)) = 0 $ <mhd-ideal-mass>

  $ rho (pdv(bold(u),t) + bold(u) dot grad(bold(u)))
    = -grad(p)
      + (curl(bold(B)) times bold(B))/(4 pi) $ <mhd-ideal-momentum>

  $ pdv(bold(B),t) = curl(bold(u) times bold(B)),
    quad div(bold(B))=0 $ <mhd-ideal-induction>

  $ pdv(p rho^(-gamma),t)
    + bold(u) dot grad(p rho^(-gamma)) = 0 $ <mhd-adiabatic-closure>

  The magnetic force has the Gaussian-CGS coefficient $1/(4 pi)$ because the
  displacement current has been neglected in Ampere's law:

  $ bold(j) = (c curl(bold(B)))/(4 pi) $ <mhd-ampere-reduced>

  The electric field is recovered from the ideal constraint, not evolved as an
  independent MHD variable.

  Let
  $rho=rho_0+delta rho$, $p=p_0+delta p$,
  $bold(u)=delta bold(u)$, and
  $bold(B)=bold(B)_0+delta bold(B)$, where perturbations are first order. For
  uniform equilibrium, the linearized equations are

  $ pdv(delta rho,t) + rho_0 div(delta bold(u)) = 0 $ <mhd-linear-mass>

  $ rho_0 pdv(delta bold(u),t)
    = -grad(delta p)
      + (curl(delta bold(B)) times bold(B)_0)/(4 pi) $ <mhd-linear-momentum>

  $ pdv(delta bold(B),t)
    = curl(delta bold(u) times bold(B)_0),
    quad div(delta bold(B))=0 $ <mhd-linear-induction>

  $ delta p = c_(s)^2 delta rho,
    quad c_(s)^2=(gamma p_0)/rho_0 $ <mhd-linear-closure>

  #details(
    [Derivation: linearize the ideal-MHD system],
    [For continuity, insert
    $rho=rho_0+delta rho$ and $bold(u)=delta bold(u)$ into
    $pdv(rho,t)+div(rho bold(u))=0$. Since $rho_0$ is constant and products
    of perturbations are second order,
    $pdv(delta rho,t)+rho_0 div(delta bold(u))=0$.

    In momentum, the equilibrium has $bold(u)_0=bold(0)$ and no pressure
    gradient. The inertial term becomes
    $rho (pdv(bold(u),t)+bold(u) dot grad(bold(u)))
      =rho_0 pdv(delta bold(u),t)+O(delta^2)$.
    The pressure force is $-grad(delta p)$. Expand the magnetic force:
    $1/(4 pi)[curl(bold(B)_0+delta bold(B))]
      times(bold(B)_0+delta bold(B))$.
    The uniform background has $curl(bold(B)_0)=bold(0)$, so the first-order
    term is $[curl(delta bold(B))times bold(B)_0]/(4 pi)$.

    Ideal induction is already linear in $bold(u)$ and $bold(B)$ through
    $curl(bold(u)times bold(B))$. Keeping one perturbation and one background
    field gives
    $pdv(delta bold(B),t)=curl(delta bold(u)times bold(B)_0)$.
    Divergence-free magnetic fields give
    $div(delta bold(B))=0$.

    Finally expand the adiabatic invariant
    $p rho^(-gamma)=p_0 rho_0^(-gamma)+delta(p rho^(-gamma))$.
    The first-order perturbation is proportional to
    $(delta p)/p_0-gamma ((delta rho)/rho_0)$. Its material derivative reduces to a
    time derivative because the equilibrium is static. For perturbations
    initially satisfying the adiabatic relation, this quantity stays zero:
    $(delta p)/p_0=gamma ((delta rho)/rho_0)$, or
    $delta p=((gamma p_0)/rho_0)delta rho=c_(s)^2delta rho$.
    Every discarded product contains at least two perturbation factors.]
  )

  #animation(
    "../media/exb-drift.mp4",
    "A charged particle gyros around a magnetic-field direction while its guiding center translates with the common electric drift. The axes are normalized by the reference gyroradius; the electric field points upward and the magnetic field points out of the page. The animation illustrates the shared perpendicular advection that becomes the ideal bulk constraint, not a full MHD solution.",
    caption: [
      Common $E times B$ advection as a visual bridge to ideal MHD. The
      animation is a deterministic normalized illustration; it does not show
      the linearized MHD perturbation equations or measured data.
    ],
    poster: "../media/exb-drift.png",
  )

  #rechenbeispiel[
    Context: a uniform equilibrium has
    $rho_0=qty("1.0e-14", "g/cm^3")$, $p_0=qty("1.0", "erg/cm^3")$,
    $gamma=5/3$, and a density perturbation
    $(delta rho)/rho_0=0.010$.

    Assumptions: ideal, adiabatic, small-amplitude MHD perturbations about a
    static uniform state.

    Target: report the adiabatic sound speed and pressure perturbation.

    Numerical result: $c_(s)=qty("1.29e7", "cm/s")$,
    $delta p=qty("1.67e-2", "erg/cm^3")$, and
    $(delta p)/p_0=0.0167$ (dimensionless).
  ]

  #interpretation(
    [What the linear system preserves and discards],
    [The linearized equations preserve pressure restoring forces, magnetic
    tension and compression, and the divergence-free field constraint. They
    discard perturbation--perturbation advection and any equilibrium gradients.
    The resulting waves are small-amplitude limits of nonlinear MHD; they are
    not valid for shocks, strong reconnection, or perturbations comparable to
    the background.]
  )

  #summary[
    Ideal MHD is a closed reduced system for $rho$, $bold(u)$, $p$, and
    $bold(B)$, supplemented by Ampere's reduced law and an adiabatic closure.
    Linearization around a uniform static state yields four first-order
    relations for $delta rho$, $delta p$, $delta bold(u)$, and
    $delta bold(B)$. The next wave chapters use this system to derive its
    characteristic branches.
  ]

  #exam-prompts(
    (
      [(b) Write down the linearized single-fluid MHD equations.],
    ),
    [Plasma Physics Exam.pdf, p. 3, section 6(b)],
  )

  #knowledge-check((
    (
      question: [Which equilibrium assumptions remove the first-order background magnetic force?],
      answer: [A uniform, time-independent $bold(B)_0$ has
      $curl(bold(B)_0)=bold(0)$, so it carries no equilibrium current in the
      reduced Ampere law. The background pressure and velocity are also taken
      uniform and static.]
    ),
    (
      question: [What closure relates pressure and density perturbations in the adiabatic model?],
      answer: [The first-order closure is
      $delta p=c_(s)^2delta rho$ with
      $c_(s)^2=(gamma p_0)/rho_0$. The sound speed has units #unit("cm/s"),
      while the perturbation ratios are dimensionless.]
    ),
    (
      question: [Why must a magnetic-field perturbation be divergence-free?],
      answer: [The constraint $div(bold(B))=0$ is part of Maxwell's equations.
      Splitting $bold(B)=bold(B)_0+delta bold(B)$ with
      $div(bold(B)_0)=0$ leaves $div(delta bold(B))=0$.]
    ),
    (
      question: [What nonlinear effect is lost on linearization?],
      answer: [Products of perturbations, such as
      $delta bold(u) dot grad(delta bold(u))$, are discarded. Therefore the
      linear model cannot represent finite-amplitude steepening, shocks, or
      perturbation-generated equilibrium changes.]
    ),
  ))

  #section-title[Frozen-in flux and magnetic diffusion] <mhd-flux>

  #lead[
    What does ideal MHD mean geometrically? Its induction equation says that
    magnetic flux through a surface moving with the fluid is conserved. A
    finite resistivity adds a competing diffusion process, so the magnetic
    Reynolds number decides whether field lines are effectively carried by the
    flow or can slip through it.
  ]

  #objectives((
    [derive the induction equation from Faraday's law and Ohm's law],
    [prove conservation of magnetic flux through a material surface],
    [define magnetic diffusivity and magnetic Reynolds number in CGS],
    [estimate the magnetic-field diffusion timescale and its limiting regime],
  ))

  #unit-ledger[
    The magnetic field is in gauss, characteristic length $L$ in #unit("cm"),
    bulk speed $U$ in #unit("cm/s"), resistivity $eta$ in #unit("s"), and
    magnetic diffusivity $D_(B)=(c^2 eta)/(4 pi)$ in #unit("cm^2/s"). The
    magnetic Reynolds number $R_(m)=(U L)/D_(B)$ is dimensionless. The
    advection time $tau_(A)=L/U$ and diffusion time $tau_(D)=L^2/D_(B)$ are
    both in #unit("s").
  ]

  #assumption(
    [Induction ordering],
    [Use Faraday's law, reduced Ampere's law
    $bold(j)=(c curl(bold(B)))/(4 pi)$, and a uniform scalar resistivity. For
    ideal MHD set $eta=0$ after the induction equation is derived. Assume
    $div(bold(B))=0$ when converting the double curl into a Laplacian. A
    material surface has boundary velocity $bold(u)$ and remains smooth while
    the flux theorem is applied.]
  )

  Faraday's law and generalized Ohm's law in the resistive MHD limit are

  $ curl(bold(E)) = -1/c pdv(bold(B),t),
    quad bold(E) + (bold(u) times bold(B))/c = eta bold(j) $ <mhd-faraday-ohm>

  Substitution of reduced Ampere's law gives the induction equation

  $ pdv(bold(B),t)
    = curl(bold(u) times bold(B))
      + D_(B) laplacian(bold(B)),
    quad D_(B)=(c^2 eta)/(4 pi) $ <mhd-resistive-induction>

  The first term advects and stretches field; the second diffuses it. The
  dimensionless competition is

  $ R_(m) = (U L)/D_(B) = tau_(D)/tau_(A) $ <mhd-magnetic-reynolds>

  For $R_(m) >> 1$, advection dominates and the approximate diffusion time is
  long. For a characteristic structure of size $L$, the finite-resistivity
  diffusion estimate is

  $ tau_(D) approx L^2/D_(B) = (4 pi L^2)/(c^2 eta) $ <mhd-diffusion-time>

  #details(
    [Derivation: induction equation and frozen magnetic flux],
    [Begin with
    $bold(E)+(bold(u)times bold(B))/c=eta bold(j)$ and solve for the electric
    field:
    $bold(E)=-(bold(u)times bold(B))/c+eta bold(j)$.
    Insert this into Faraday's law:
    $pdv(bold(B),t)=-c curl(bold(E))
      =curl(bold(u)times bold(B))-c eta curl(bold(j))$.

    The reduced Ampere law is
    $bold(j)=(c curl(bold(B)))/(4 pi)$. For uniform $eta$,
    $-c eta curl(bold(j))=-(c^2 eta curl(curl(bold(B))))/(4 pi)$.
    The identity
    $curl(curl(bold(B)))=grad(div(bold(B)))-laplacian(bold(B))$
    and $div(bold(B))=0$ give
    $-c eta curl(bold(j))=(c^2 eta laplacian(bold(B)))/(4 pi)$.
    Define $D_(B)=(c^2 eta)/(4 pi)$ to obtain the displayed induction equation.

    Now let $S(t)$ be a surface whose boundary moves with $bold(u)$ and let
    $Psi_(B)=integral_(S(t)) bold(B) dot dif bold(S)$ be its magnetic flux.
    The moving-surface transport theorem, or equivalently the flux rule for a
    moving loop, gives
    $dv(Psi_(B),t)
      =integral_(S(t))[pdv(bold(B),t)-curl(bold(u)times bold(B))]
        dot dif bold(S)$.
    The ideal induction equation sets the integrand to zero, so
    $dv(Psi_(B),t)=0$. Stokes' theorem shows the same result from the moving
    loop:
    $dv(Psi_(B),t)=integral_(S) pdv(bold(B),t) dot dif bold(S)
      -integral_(partial S)(bold(u)times bold(B))dot dif bold(l)$.
    Thus the flux through every material surface is constant, which is the
    frozen-flux theorem.

    Compare the induction terms with
    $|curl(bold(u)times bold(B))| approx (U B)/L$ and
    $|D_(B) laplacian(bold(B))| approx (D_(B)B)/(L^2)$. Their ratio is
    $(U L)/D_(B)=R_(m)$. The same ratio equals
    $(L/U)/(L^2/D_(B))=tau_(D)/tau_(A)$.]
  )

  #mhd-flux-diffusion

  #rechenbeispiel[
    Context: a magnetic structure has length
    $L=qty("1.0e3", "cm")$ and bulk speed
    $U=qty("1.0e7", "cm/s")$. Use scalar resistivity
    $eta=qty("1.00e-12", "s")$ and
    $c=qty("2.998e10", "cm/s")$.

    Assumptions: uniform resistivity, divergence-free magnetic field, and the
    resistive induction ordering stated above.

    Target: report the magnetic diffusivity, advection time, diffusion time,
    and magnetic Reynolds number.

    Numerical result: $D_(B)=qty("7.15e7", "cm^2/s")$,
    $tau_(A)=qty("1.00e-4", "s")$,
    $tau_(D)=qty("1.40e-2", "s")$, and
    $R_(m)=1.40 dot 10^2$ (dimensionless).
  ]

  #interpretation(
    [Frozen flux is an approximation with a precise failure mode],
    [Ideal MHD preserves flux through a surface that moves with $bold(u)$, so
    field-line connectivity is maintained as long as the smooth ideal
    description remains valid. Finite resistivity permits slippage and, in
    sufficiently localized regions, changes of connectivity. A large global
    $R_(m)$ does not guarantee that diffusion is negligible inside every thin
    current layer.]
  )

  #summary[
    Faraday's law plus Ohm's law produces advection and diffusion in the
    magnetic induction equation. In Gaussian CGS,
    $D_(B)=(c^2 eta)/(4 pi)$, $tau_(D)=L^2/D_(B)$, and
    $R_(m)=(U L)/D_(B)$. The ideal limit conserves flux through material surfaces;
    resistivity breaks that material conservation on the diffusion scale.
  ]

  #exam-prompts(
    (
      [(e) Sketch the derivation of the frozen-flux theorem.],
      [(f) Derive the diffusion equation for the B field and estimate the timescale.],
    ),
    [Plasma Physics Exam.pdf, p. 3, section 6(e)--(f)],
  )

  #knowledge-check((
    (
      question: [Which term changes the magnetic-field topology in the resistive induction equation?],
      answer: [The term $D_(B) laplacian(bold(B))$ represents magnetic diffusion.
      It is absent in ideal MHD and becomes important when its scale estimate
      is comparable with the advection term.]
    ),
    (
      question: [What surface is used in the frozen-flux statement?],
      answer: [It is a material surface whose boundary moves with the bulk
      velocity $bold(u)$. Flux through a fixed laboratory surface is not the
      same invariant.]
    ),
    (
      question: [How does the magnetic Reynolds number compare the timescales?],
      answer: [$R_(m)=tau_(D)/tau_(A)=(U L)/D_(B)$. Thus $R_(m)>>1$ means
      advection is faster than diffusion, while $R_(m)<<1$ means diffusion
      acts before the flow can transport the field across $L$.]
    ),
    (
      question: [What assumption is needed to replace the double curl by a Laplacian?],
      answer: [Use $div(bold(B))=0$ and uniform resistivity. Then
      $curl(curl(bold(B)))=-laplacian(bold(B))$, yielding the diffusion term with
      coefficient $D_(B)=(c^2 eta)/(4 pi)$.]
    ),
  ))

  #section-title[Static MHD equilibrium and magnetic force balance] <mhd-equilibrium>

  #lead[
    How can a plasma remain static while its pressure varies across the
    device? In a magnetized equilibrium, the current creates a magnetic force
    that balances the pressure gradient. The vector identity for this force
    separates magnetic pressure from field-line tension and makes cylindrical
    pinch configurations interpretable.
  ]

  #objectives((
    [derive the static MHD equilibrium equation from the momentum balance],
    [separate magnetic-pressure and magnetic-tension contributions],
    [deduce the restrictions on pressure along field lines and current across them],
    [explain why the parallel current requires field-line geometry and closure],
    [interpret theta-pinch, cylindrical pinch, and plasma-beta examples],
  ))

  #unit-ledger[
    Static pressure $p$ and magnetic pressure $B^2/(8 pi)$ are both in
    #unit("erg/cm^3") in Gaussian CGS. The current density is in
    statcoulomb per #unit("cm^2") per #unit("s"), and
    $(bold(j)times bold(B))/c$ is a force density in
    #unit("g") #unit("cm^-2") #unit("s^-2"). The plasma beta
    $beta=(8 pi p)/(B^2)$ is dimensionless.
  ]

  #assumption(
    [Static isotropic equilibrium],
    [Set $pdv(rho,t)=bold(0)$ and $bold(u)=bold(0)$, neglect gravity and the
    bulk electric force under quasi-neutrality, use scalar pressure, and use
    reduced Ampere's law. The magnetic field remains divergence-free. These
    assumptions describe magnetohydrostatics, not a general time-dependent
    plasma or a kinetic boundary layer.]
  )

  The static momentum equation is

  $ grad(p) = (bold(j) times bold(B))/c
    = (curl(bold(B)) times bold(B))/(4 pi) $ <mhd-static-force-balance>

  Using the vector identity
  $curl(bold(B)) times bold(B)
    = (bold(B) dot grad)bold(B)-grad(B^2/2)$,
  this becomes

  $ grad(p + B^2/(8 pi))
    = 1/(4 pi) (bold(B) dot grad)bold(B) $ <mhd-magnetic-pressure-tension>

  The left side is the gradient of gas plus magnetic pressure. The right side
  is field-line tension and vanishes for a straight, uniform field.

  Dotting the force balance with $bold(B)$ and with $bold(j)$ gives

  $ bold(B) dot grad(p)=0,
    quad bold(j) dot grad(p)=0 $ <mhd-equilibrium-geometry>

  Thus pressure is constant along each field line, and the current is tangent
  to pressure surfaces when the scalar-pressure equilibrium is valid. The
  perpendicular current follows by crossing the equilibrium with $bold(B)$:

  $ bold(j)_perp = (c (bold(B) times grad(p)))/(B^2) $ <mhd-equilibrium-current>

  The force balance fixes only this perpendicular component. Write the total
  current as

  $ bold(j) = j_(parallel) (bold(B)/B) + bold(j)_perp $

  Because reduced Ampere's law also implies $div(bold(j))=0$, the
  parallel component obeys the magnetic differential equation

  $ bold(B) dot grad(j_(parallel)/B)
    = -div(bold(j)_perp) $ <mhd-parallel-current>

  Thus $j_(parallel)$ requires field-line geometry and boundary or closure data;
  it is not determined by the local pressure balance alone.

  A useful dimensionless measure is

  $ beta = (8 pi p)/(B^2) $ <mhd-beta>

  Low $beta$ means magnetic pressure dominates thermal pressure; high $beta$
  means pressure gradients can strongly reshape the field or require stronger
  currents for equilibrium.

  #definition(
    [Two canonical pinch geometries],
    [A $theta$-pinch uses an externally applied, primarily axial field and an
    azimuthal current: $bold(B)=B_(z)(r)bold(e)_(z)$ and
    $bold(j)=j_(theta)(r)bold(e)_(theta)$. Straight field lines have no curvature
    tension, so the radial balance is a total-pressure balance. A cylindrical
    or $z$-pinch uses an axial plasma current and a self-generated azimuthal
    field: $bold(j)=j_(z)(r)bold(e)_(z)$ and
    $bold(B)=B_(theta)(r)bold(e)_(theta)$. The curved field then contributes an
    inward tension term.]
  )

  The two radial balances make the distinction quantitative:

  For a $theta$-pinch,

  $ dv(p+B_(z)^2/(8 pi),r)=0 $

  For a cylindrical or $z$-pinch,

  $ dv(p+B_(theta)^2/(8 pi),r) + (B_(theta)^2)/(4 pi r)=0 $

  The second term is the curvature tension of the azimuthal field. Both
  relations are special reductions of the same vector equilibrium equation;
  neither replaces the general force balance.

  #details(
    [Derivation: magnetic pressure, tension, and pinch balance],
    [Begin with the static momentum equation after reduced Ampere's law:
    $bold(0)=-grad(p)+(bold(j)times bold(B))/c$ and
    $bold(j)=(c curl(bold(B)))/(4 pi)$. Therefore
    $grad(p)=((curl(bold(B)))times bold(B))/(4 pi)$.

    For the magnetic identity, use components or the standard vector relation
    $grad(B^2/2)=(bold(B)dot grad)bold(B)
      +bold(B)times(curl(bold(B)))$.
    Since $bold(B)times curl(bold(B))=-curl(bold(B))times bold(B)$,
    rearrange to
    $curl(bold(B))times bold(B)
      =(bold(B)dot grad)bold(B)-grad(B^2/2)$.
    Substitute into the force balance and move the magnetic-pressure gradient
    to the left:
    $grad(p+B^2/(8 pi))=((bold(B)dot grad)bold(B))/(4 pi)$.
    The first term is compression of field magnitude, the second is field-line
    tension.

    Dot $grad(p)=(bold(j)times bold(B))/c$ with $bold(B)$. The right side is zero,
    so $bold(B)dot grad(p)=0$. Dot it with $bold(j)$ instead; again the right
    side is zero, so $bold(j)dot grad(p)=0$. Cross it from the left with
    $bold(B)$:
    $bold(B)times grad(p)
      =(bold(B)times(bold(j)times bold(B)))/c$.
    The triple-product identity gives
    $bold(B)times(bold(j)times bold(B))
      =B^2 bold(j)-bold(B)(bold(B)dot bold(j))$.
    The component perpendicular to $bold(B)$ is therefore
    $bold(j)_perp=(c (bold(B)times grad(p)))/(B^2)$.

    Decompose the current as
    $bold(j)=j_(parallel) (bold(B)/B)+bold(j)_perp$. Since
    $div(bold(j))=div((c curl(bold(B)))/(4 pi))=0$ and $div(bold(B))=0$,

    $0=div(bold(j))
      =div((j_(parallel) bold(B))/B)+div(bold(j)_perp)
      =bold(B)dot grad(j_(parallel)/B)+div(bold(j)_perp)$.

    This gives the displayed magnetic differential equation for the parallel
    current. A boundary condition or a separate closure is needed to select a
    solution along each field line.

    For a straight cylindrical field $bold(B)=B_(z)(r)bold(e)_(z)$, the reduced
    Ampere law gives
    $bold(j)=-(c dv(B_z,r))/(4 pi) bold(e)_theta$.
    The radial force balance is then
    $dv(p,r)=-(B_z dv(B_z,r))/(4 pi)$,
    so
    $dv(p+B_(z)^2/(8 pi),r)=0$.
    For a $theta$-pinch with a uniform axial field inside, the volume current
    and magnetic tension can vanish in the interior; the pressure change is
    balanced by the magnetic-pressure change across the boundary.

    For a cylindrical or $z$-pinch, take
    $bold(B)=B_(theta)(r)bold(e)_(theta)$ and
    $bold(j)=j_(z)(r)bold(e)_(z)$. Cylindrical Ampere's law gives
    $j_(z)=(c/(4 pi r))dv(r B_(theta),r)$. Since
    $bold(e)_z times bold(e)_theta=-bold(e)_r$, the radial force balance is
    $dv(p,r)=-(B_(theta)/(4 pi r))dv(r B_(theta),r)$.
    Expanding the derivative yields
    $dv(p+B_(theta)^2/(8 pi),r)+(B_(theta)^2)/(4 pi r)=0$.
    The final term is the inward magnetic tension from curved field lines.
    These examples are special geometries, not extra equilibrium laws.]
  )

  #mhd-force-balance

  #rechenbeispiel[
    Context: a straight theta-pinch has constant total pressure across its
    boundary. Inside, let
    $p_("in")=qty("10.0", "erg/cm^3")$ and
    $B_(z,"in")=qty("10.0", "G")$; outside, let
    $B_(z,"out")=qty("12.0", "G")$.

    Assumptions: scalar static equilibrium, straight axial field, and no
    field-line curvature contribution in the pressure balance.

    Target: report the outside gas pressure and the inside plasma beta.

    Numerical result: $p_("out")=qty("8.25", "erg/cm^3")$ and
    $beta_("in")=2.51$ (dimensionless).
  ]

  #interpretation(
    [Equilibrium is a geometry constraint],
    [The equation $grad(p)=(bold(j)times bold(B))/c$ says more than “forces
    cancel.” Pressure cannot vary along a field line, and current-driven force
    is perpendicular to the field. In a pinch, a pressure profile therefore
    determines the magnetic-field profile together with boundary conditions;
    the field is not chosen independently of the plasma pressure.]
  )

  #summary[
    Static MHD balances pressure force against magnetic force. In Gaussian CGS,
    $grad(p)=((curl(bold(B)))times bold(B))/(4 pi)$, or equivalently the gradient
    of gas plus magnetic pressure balances field-line tension. Pressure is
    constant along field lines, the perpendicular current follows from the
    pressure gradient, and the parallel current obeys a magnetic differential
    equation. The dimensionless $beta=(8 pi p)/(B^2)$ measures the relative
    strength of thermal and magnetic pressure.
  ]

  #exam-prompts(
    (
      [(g) Write down and explain the static MHD equilibrium equation.],
    ),
    [Plasma Physics Exam.pdf, p. 3, section 6(g)],
  )

  #knowledge-check((
    (
      question: [What is the static MHD force-balance equation in Gaussian CGS?],
      answer: [With the stated assumptions,
      $grad(p)=(bold(j)times bold(B))/c
        =((curl(bold(B)))times bold(B))/(4 pi)$.]
    ),
    (
      question: [What does the magnetic-pressure/tension decomposition show?],
      answer: [It rewrites the force as
      $grad(p+B^2/(8 pi))=((bold(B)dot grad)bold(B))/(4 pi)$. The gradient term
      is magnetic pressure and the directional derivative is field-line
      tension.]
    ),
    (
      question: [What is fixed locally about the current, and what determines its parallel component?],
      answer: [The pressure balance fixes
      $bold(j)_perp=(c (bold(B)times grad(p)))/(B^2)$. The parallel component is
      constrained by $bold(B) dot grad(j_(parallel)/B)=-div(bold(j)_perp)$ and
      therefore requires field-line geometry and boundary or closure data.]
    ),
    (
      question: [What does a large plasma beta indicate?],
      answer: [A large $beta=(8 pi p)/(B^2)$ means thermal pressure exceeds magnetic
      pressure in the chosen local scales. Magnetic stresses may still balance
      it, but a stronger field curvature or current response is generally
      required.]
    ),
  ))

  #chapter-nav(
    previous: (href: "05-multiple-fluids.html", title: [Multiple fluids]),
    next: (href: "07-collisions-conductivity.html", title: [Collisions and conductivity]),
  )
]
