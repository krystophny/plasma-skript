#import "../theme.typ": *
#import "../figures.typ": collision-regimes, coulomb-cutoff, conductivity-tensor
#import "@preview/physica:0.9.8": div, grad, pdv, curl
#import "@preview/unify:0.8.1": qty, unit

#let chapter = [
  #page-title[7. Collisions and plasma conductivity] <collisions-conductivity>

  #lead[
    Collisions are not merely a loss mechanism. They convert random thermal
    motion into directed transport: inhomogeneity produces diffusion, while an
    external force produces mobility and electrical current. This chapter
    builds the collision frequencies first and only then uses them in
    resistivity and conductivity models.
  ]

  #callout(
    [Two routes to a transport coefficient],
    [A collision model supplies a rate at which momentum is redirected or
    removed. The same bookkeeping supports neutral-collision transport and
    Coulomb transport. The resulting coefficient is meaningful only together
    with its collision regime, velocity average, and unit convention.]
  )

  #section-title[Collision bookkeeping and transport mechanisms] <collision-bookkeeping>

  #lead[
    What does it mean to say that a particle collides? The useful answer is a
    rate, a mean free path, and a momentum-transfer rule. A cross section is an
    effective area, not a literal hard-sphere diameter; it may depend strongly
    on relative speed and scattering angle.
  ]

  #objectives((
    [distinguish collision frequency, collision time, cross section, and mean free path],
    [derive the collision rate from a path-length probability],
    [identify diffusion and force-driven mobility as distinct transport routes],
    [state the Knudsen ordering that separates fluid-like from collisionless motion],
  ))

  #unit-ledger[
    Gaussian CGS is active. Number density $n_s$ is in #unit("cm^-3"), a
    cross section $sigma_(a b)$ is in #unit("cm^2"), speed is in
    #unit("cm/s"), mean free path is in #unit("cm"), and collision frequency
    $nu_(a b)$ is in #unit("s^-1"). Time is in #unit("s"); a normalized
    collision count such as $nu tau$ and a Knudsen number are dimensionless.
  ]

  #definition(
    [Rate, time, and length scales],
    [For a test species $a$ moving through targets $b$, define the effective
    collision frequency by
    $nu_(a b)=n_b ⟨sigma_(a b) v_"rel"⟩$.
    The brackets denote the prescribed velocity-space average. The collision
    time is $tau_(a b)=1/nu_(a b)$ and, with the same averaging convention,
    the mean free path is
    $lambda_(a b)=⟨v_"rel"⟩/nu_(a b)$.
    If the cross section is independent of speed, this becomes
    $lambda_(a b)=1/(n_b sigma_(a b))$.]
  )

  #collision-regimes

  The two transport mechanisms are separated conceptually. A spatial
  gradient produces a diffusive particle flux, schematically
  $bold(G)_"diff"=-D grad_(bold(r))(n)$, while an external force produces a
  drift velocity, schematically
  $bold(u)_"mob"=mu bold(F)$. For an electric force, the charge-weighted
  drift contributes to the current $bold(j)=sum_s q_(s)n_(s)bold(u)_(s)$.
  These are macroscopic summaries; the microscopic coefficient still depends
  on the collision operator and the ordering of scales.

  #assumption(
    [A dilute binary-collision model],
    [Treat encounters as independent binary events. The target population is
    dilute enough that a particle samples one local density during an
    encounter, and the effective cross section includes the momentum transfer
    relevant to the observable. A collision frequency is therefore a local
    model parameter, not a universal constant of the species pair.]
  )

  #details(
    [Derivation: path probability and the mean free path],
    [During a path segment $dif ell$, a particle sweeps an effective volume
    $sigma_(a b) dif ell$. The expected number of targets in that volume is
    $n_b sigma_(a b) dif ell$, so the probability of one collision to first
    order is $dif P=n_b sigma_(a b)dif ell$. If $P_(0)(ell)$ is the probability
    of no collision, independent segments give
    $dif P_0=-n_b sigma_(a b)P_0 dif ell$.
    Integrating with $P_(0)(0)=1$ gives
    $P_(0)(ell)=exp(-n_b sigma_(a b)ell)$.

    The mean distance is the survival-probability integral
    $lambda_(a b)=integral_0^infinity P_(0)(ell) dif ell
      =1/(n_b sigma_(a b))$.
    A particle with relative speed $v_"rel"$ travels $dif ell=v_"rel"dif t$.
    Therefore the rate is $nu_(a b)=n_b sigma_(a b)v_"rel"$ for a fixed
    speed. Averaging over the relative-velocity distribution gives the
    displayed rate $n_b ⟨sigma_(a b)v_"rel"⟩$ and
    fixes the corresponding mean-free-path convention.

    For a macroscopic length $L$, the dimensionless Knudsen number is
    $K_"n"=lambda/L$. The collisional fluid ordering is $K_"n" << 1$;
    $K_"n" approx 1$ marks a transition, and $K_"n" >> 1$ requires kinetic
    or ballistic reasoning.]
  )

  #interpretation(
    [A collision frequency is an averaged observable],
    [The same particles have a distribution of relative speeds and scattering
    angles. The symbol $nu$ is useful only after the averaging and momentum-
    transfer convention have been stated. Confusing a geometric cross section
    with a momentum-transfer cross section can change both a transport
    coefficient and its physical interpretation.]
  )

  #summary[
    Collision bookkeeping starts with an effective cross section and a target
    density. It gives $nu=n⟨sigma v⟩$, $tau=1/nu$,
    and $lambda=⟨v⟩/nu$. Diffusion responds to
    inhomogeneity, mobility responds to a force, and the Knudsen number states
    whether a local fluid description is plausible.
  ]

  #knowledge-check((
    (
      question: [What is the difference between collision time and collision frequency?],
      answer: [They are reciprocals under the same averaging convention:
      $tau=1/nu$. The frequency counts effective momentum-transfer events per
      #unit("s"); the time is the corresponding mean interval.]
    ),
    (
      question: [What are the Gaussian-CGS units of a collision cross section and mean free path?],
      answer: [A cross section is an area in #unit("cm^2"), and a mean free
      path is a length in #unit("cm"). The collision frequency is in
      #unit("s^-1").]
    ),
    (
      question: [Which dimensionless parameter compares a mean free path with a device length?],
      answer: [The Knudsen number $K_"n"=lambda/L$ does so. Small $K_"n"$
      supports a local collisional fluid model, whereas large $K_"n"$ signals
      kinetic or ballistic transport.]
    ),
    (
      question: [What distinguishes diffusion from force-driven mobility?],
      answer: [Diffusion is driven by a spatial gradient and has the schematic
      flux $-D grad n$. Mobility is driven by an external force and produces a
      drift proportional to that force. Both coefficients depend on
      collisions.]
    ),
  ))

  #section-title[Weakly ionized plasmas: neutral collisions] <neutral-collisions>

  #lead[
    How does a neutral background impede charged-particle motion? Neutral atoms
    and molecules act as compact scattering centers. For a weakly ionized
    plasma, the neutral density is usually much larger than the charged
    density, so electron--neutral and ion--neutral collisions can dominate even
    though the plasma remains electrically active.
  ]

  #objectives((
    [derive the neutral-collision frequency and mean free path],
    [distinguish total scattering from momentum-transfer cross section],
    [write the neutral drag force for stationary and moving neutrals],
    [explain why momentum and energy relaxation need not have the same rate],
  ))

  #unit-ledger[
    Neutral density $n_"n"$ is in #unit("cm^-3"); electron or ion speed is
    in #unit("cm/s"); the momentum-transfer cross section
    $sigma_"mt"$ is in #unit("cm^2"); and $nu_"en"$, $nu_"in"$, and their
    relaxation times are in #unit("s^-1") and #unit("s"), respectively. The
    drag force density is in #unit("g") #unit("cm^-2") #unit("s^-2").
  ]

  #assumption(
    [Weak ionization and stationary neutrals],
    [Use $n_"n" >> n_"e"$, a neutral temperature and velocity that vary
    slowly on the collision time, and binary electron--neutral or
    ion--neutral encounters. For a stationary neutral background
    $bold(u)_"n"=bold(0)$, the leading drag is proportional to the charged
    species drift velocity. Finite neutral mass, excitation, ionization, and
    charge exchange can require additional collision channels.]
  )

  The momentum-transfer cross section is the angle-weighted quantity:

  $ sigma_"mt"(v)=integral (1-cos chi) dif sigma/dif Omega dif Omega $

  It weights a scattering event by the fraction of directed momentum removed.
  A collision that changes the direction only slightly can have a sizeable
  total cross section but a small momentum-transfer cross section.

  #definition(
    [Neutral collision rate and drag],
    [For electrons in a neutral background,
    $nu_"en"=n_"n"⟨sigma_"mt,en" v_"e"⟩$ and
    $lambda_"en"=⟨v_"e"⟩/nu_"en"$.
    The analogous ion rate is
    $nu_"in"=n_"n"⟨sigma_"mt,in" v_"i"⟩$.
    If neutrals are stationary, the electron drag force density is
    $bold(R)_"en"=-m_"e" n_"e" nu_"en" bold(u)_"e"$.
    For a moving neutral population, replace the drift by
    $bold(u)_"e"-bold(u)_"n"$.]
  )

  #rechenbeispiel[
    Given a weakly ionized gas with neutral density
    $n_"n"=qty("2.0e14", "cm^-3")$, momentum-transfer cross section
    $sigma_"mt,en"=qty("2.0e-15", "cm^2")$, and representative electron
    speed $v_"e"=qty("1.0e7", "cm/s")$, determine the effective collision
    frequency and mean free path.

    Numerical result: $nu_"en"=qty("4.0e6", "s^-1")$ and
    $lambda_"en"=qty("2.5e0", "cm")$.
  ]

  #details(
    [Derivation: neutral drag from momentum transfer],
    [A particle that suffers a collision changes its average directed momentum
    by an amount proportional to $m_a bold(u)_a$ times the momentum-transfer
    factor. In time $dif t$, the number of encounters per particle is
    $nu_(a n)dif t$. Multiplying the momentum change per encounter by the
    number density $n_a$ gives a force density proportional to
    $-m_a n_a nu_(a n)(bold(u)_a-bold(u)_n)$.

    The sign is restorative: the force vanishes when the charged species and
    neutral background share a velocity. With stationary neutrals, it reduces
    to $-m_a n_a nu_(a n)bold(u)_a$. The rate is a momentum-transfer rate,
    not necessarily the frequency of every microscopic encounter.

    Energy transfer has a separate mass-ratio dependence. An electron can
    reverse direction in an elastic encounter with a heavy neutral while
    transferring only a small fraction of its kinetic energy. Excitation and
    ionization introduce inelastic energy-loss channels that must be added to
    an energy equation rather than hidden inside a momentum drag coefficient.]
  )

  #interpretation(
    [Weak ionization is a collision hierarchy],
    [The dominant rate is selected by the product of density, cross section,
    and relative speed. A neutral-rich plasma can therefore be strongly
    collisional for electron momentum while still having a long energy-
    relaxation time. The transport model should name the channel being
    relaxed.]
  )

  #summary[
    Neutral collisions are described by momentum-transfer cross sections and
    effective rates such as
    $nu_"en"=n_"n"⟨sigma_"mt,en"v_"e"⟩$.
    Stationary neutrals exert a drag $-m n nu bold(u)$, while moving neutrals
    replace the velocity by the relative drift. Momentum and energy
    relaxation are distinct when the neutral is much heavier than the charged
    particle.
  ]

  #knowledge-check((
    (
      question: [Why is a momentum-transfer cross section more useful than a total cross section for conductivity?],
      answer: [Conductivity responds to directed momentum loss. The factor
      $1-cos chi$ weights each event by its momentum change, so small-angle
      scattering is not counted as a full reversal.]
    ),
    (
      question: [How does the neutral density enter the collision frequency?],
      answer: [It enters linearly:
      $nu_"en"=n_"n"⟨sigma_"mt,en"v_"e"⟩$.
      Doubling the target density doubles the rate when the cross section and
      velocity distribution are unchanged.]
    ),
    (
      question: [What is the drag force when the neutral background moves?],
      answer: [Use the relative velocity:
      $bold(R)_"en"=-m_"e"n_"e"nu_"en"
      (bold(u)_"e"-bold(u)_"n")$. It vanishes when the two populations share
      a velocity.]
    ),
    (
      question: [Why can momentum relaxation be faster than energy relaxation in electron--neutral collisions?],
      answer: [A heavy neutral can redirect an electron efficiently while
      taking only a small fraction of its kinetic energy. Directional momentum
      loss and energy exchange therefore have different mass-ratio scalings.]
    ),
  ))

  #section-title[Fully ionized plasmas: Coulomb collisions] <coulomb-collisions>

  #lead[
    Why is a Coulomb collision not characterized by one hard-sphere radius?
    The interaction is long range, so most encounters produce small deflections
    and a few produce large deflections. A controlled collision model must set a
    lower strong-scattering scale and an upper shielding scale before it can
    sum the cumulative angular diffusion.
  ]

  #objectives((
    [define the ninety-degree impact parameter and large-angle collision rate],
    [show why cumulative small-angle scattering produces a logarithm],
    [use Debye shielding as the upper impact-parameter cutoff],
    [state the weak-coupling condition behind a Coulomb collision frequency],
  ))

  #unit-ledger[
    In Gaussian CGS, charge is in statcoulomb, reduced mass $m_r$ is in
    #unit("g"), relative speed is in #unit("cm/s"), and the impact parameter
    $b_90$ and Debye length $lambda_D$ are in #unit("cm"). The Coulomb
    logarithm $ln Lambda$ and plasma parameter $Lambda$ are dimensionless;
    collision frequencies are in #unit("s^-1").
  ]

  #assumption(
    [Weakly coupled, fully ionized plasma],
    [Use a plasma containing only charged particles on the collision scale,
    treat a heavy ion as stationary for the electron--ion estimate, and assume
    $Lambda=n_"e"lambda_D^3 >> 1$. The interaction is screened beyond
    approximately $lambda_D$, and many small-angle encounters can be treated
    statistically. A strongly coupled plasma requires a different kinetic
    description.]
  )

  #definition(
    [Strong-deflection scale],
    [For charges $q_a$ and $q_b$ with reduced mass $m_r$ and relative speed
    $v_"rel"$, define the ninety-degree impact parameter in Gaussian CGS by
    $b_90=abs(q_a q_b)/(m_r v_"rel"^2)$.
    For an electron scattering from a singly charged ion,
    $b_90=e^2/(m_"e"v_"e"^2)$ in the heavy-ion approximation and
    $sigma_90=pi b_90^2$. A closest-approach convention based on equating
    kinetic and Coulomb potential energies differs by an order-one factor; the
    collision logarithm is insensitive to that convention at leading order.]
  )

  #coulomb-cutoff

  The large-angle estimate is:

  $ nu_90 approx n_"i" sigma_90 v_"e"
    =pi n_"i" e^4/(m_"e"^2 v_"e"^3) $

  It is not the full electron--ion relaxation rate because the many more
  distant encounters contribute cumulatively.

  #definition(
    [Coulomb logarithm and electron--ion rate],
    [For impact parameters $b$ much larger than $b_90$, the deflection is
    small, $chi(b) approx 2b_90/b$. The screened upper cutoff is
    $b_"max" approx lambda_D$. The broad-impact-parameter measure is recorded
    by
    $Lambda=n_"e"lambda_D^3$ and
    $ln Lambda=ln(lambda_D/b_90)$ up to the order-one convention used for the
    lower cutoff. For the collision-frequency convention used here,
    $nu_(e i) approx sqrt(2) omega_(p,e)^4/(64 pi n_"e")
      (k_B T_"e"/m_"e")^(-3/2) ln Lambda$,
    where $omega_(p,e)=sqrt(4 pi n_"e"e^2/m_"e")$.
    The corresponding mean free path is
    $lambda_(e i)=⟨v_"e"⟩/nu_(e i)$.]
  )

  #rechenbeispiel[
    For a fully ionized hydrogen plasma, use
    $n_"e"=qty("1.0e10", "cm^-3")$,
    $k_B T_"e"=qty("1.602e-11", "erg")$,
    $e=qty("4.803e-10", "statC")$,
    $m_"e"=qty("9.109e-28", "g")$, and
    $⟨v_"e"⟩
      =qty("2.12e8", "cm/s")$.
    Determine $lambda_D$, $Lambda$, $ln Lambda$, $nu_(e i)$ using the
    collision-frequency convention above, and $lambda_(e i)$.

    Numerical result: $lambda_D=qty("2.35e-2", "cm")$,
    $Lambda=qty("1.30e5", "1")$, $ln Lambda=qty("11.8", "1")$,
    $nu_(e i)=qty("2.54e3", "s^-1")$, and
    $lambda_(e i)=qty("8.35e4", "cm")$.
  ]

  #details(
    [Derivation: cumulative small-angle scattering],
    [For $b >> b_90$, Rutherford scattering gives
    $chi(b) approx 2b_90/b$. During $dif t$, the number of target ions with
    impact parameters in the annulus $b$ to $b+dif b$ is proportional to
    $n_"i"v_"rel" 2 pi b dif b dif t$. The squared transverse kick from each
    event is proportional to $v_"rel"^2 chi(b)^2$. The rate of accumulated
    squared deflection therefore has the scale
    $dif ⟨Delta v_perp^2⟩/dif t
      ∝ n_"i"v_"rel"^3 b_90^2
      integral_(b_90)^(lambda_D) dif b/b$.
    The integral is
    $ln(lambda_D/b_90)$, the Coulomb logarithm. The logarithm is why small
    deflections cannot simply be discarded even though a single distant
    encounter changes the velocity very little.

    For a Maxwellian electron population use
    $⟨v_"e"⟩
      =sqrt(8 k_B T_"e"/(pi m_"e"))$ in the rate convention. Insert
    $omega_(p,e)^2=4 pi n_"e"e^2/m_"e"$ and the velocity scale into the
    statistical scattering estimate. This yields the displayed
    $nu_(e i) ∝ T_"e"^(-3/2)ln Lambda$ expression. The ratio of
    distant to strong-scattering scales is large only when
    $Lambda=n_"e"lambda_D^3 >> 1$; otherwise independent binary encounters
    and a weak-coupling collision operator are not self-consistent.]
  )

  #interpretation(
    [Screening makes the long-range interaction finite],
    [Without shielding, integrating over arbitrarily large impact parameters
    would make the cumulative rate ill-defined. Debye shielding supplies the
    physical upper scale. The lower scale is set by strong deflection or by a
    quantum correction when classical impact parameters become too small. The
    Coulomb logarithm is therefore a controlled scale ratio, not a mysterious
    fitting constant.]
  )

  #summary[
    Fully ionized collisions are dominated in number by small-angle encounters
    but in cumulative effect by the logarithmic interval between $b_90$ and
    $lambda_D$. The weak-coupling parameter
    $Lambda=n_"e"lambda_D^3 >> 1$ justifies the statistical treatment, and the
    electron--ion rate scales as $T_"e"^(-3/2)ln Lambda$ in the stated
    convention.
  ]

  #knowledge-check((
    (
      question: [Why is the ninety-degree cross section not the complete Coulomb collision rate?],
      answer: [Distant encounters are much more numerous. Each gives a small
      deflection, but their squared kicks add over impact parameters and
      produce the factor $ln Lambda$.]
    ),
    (
      question: [How does the ninety-degree impact parameter scale with speed?],
      answer: [For fixed charges and reduced mass,
      $b_90=abs(q_a q_b)/(m_r v_"rel"^2)$, so faster particles have a smaller
      strong-deflection scale.]
    ),
    (
      question: [What sets the upper impact-parameter cutoff in a plasma?],
      answer: [Collective Debye shielding sets
      $b_"max" approx lambda_D$. Encounters at larger scales are screened by
      the surrounding plasma and cannot be added as independent unscreened
      Coulomb kicks.]
    ),
    (
      question: [What condition makes the weakly coupled Coulomb model self-consistent?],
      answer: [The plasma parameter must be large:
      $Lambda=n_"e"lambda_D^3 >> 1$. It implies many particles occupy a Debye
      sphere and supports a statistical, weak-coupling description.]
    ),
  ))

  #section-title[Specific resistivity and Spitzer scaling] <specific-resistivity>

  #lead[
    How does collisional drag become a resistivity? The current is a measure of
    relative charge-carrier motion, while drag removes that relative momentum.
    Equating the two gives the resistivity directly; the collision model enters
    only through the appropriate momentum-transfer frequency.
  ]

  #objectives((
    [derive scalar resistivity from a drag force and the current],
    [distinguish neutral-limited and Coulomb-limited resistivity],
    [obtain the temperature and density scaling of Spitzer resistivity],
    [connect resistivity to conductivity in Gaussian CGS],
  ))

  #unit-ledger[
    In Gaussian CGS, $bold(E)$ is in statvolt per #unit("cm"), current density
    $bold(j)$ is in statcoulomb per #unit("cm^2") per #unit("s"), resistivity
    $eta$ in $bold(E)=eta bold(j)$ is in #unit("s"), and conductivity
    $sigma=1/eta$ is in #unit("s^-1"). The drag force density is in
    #unit("g") #unit("cm^-2") #unit("s^-2").
  ]

  #assumption(
    [Linear, isotropic drag],
    [Use a small drift relative to the random thermal speed, so that the
    collision frequency can be evaluated from the equilibrium distribution.
    Treat the drag as linear in relative velocity and use a scalar frequency
    $nu$ for the chosen collision channel. Magnetization and tensor response
    are postponed to the conductivity section.]
  )

  #definition(
    [Resistivity from momentum transfer],
    [For a hydrogen plasma, the electron--ion drag force density can be written
    $bold(R)_"e i"=m_"e"n_"e"nu_"e i"
      (bold(u)_"i"-bold(u)_"e")$.
    Since $bold(j)=e n_"e"(bold(u)_"i"-bold(u)_"e")$, the force per electron
    charge density is $eta bold(j)$ with
    $eta=m_"e"nu_"e i"/(n_"e"e^2)$.
    More generally use $nu=nu_"en"$ for a stationary neutral background or
    the sum of the relevant momentum-transfer frequencies. The scalar
    conductivity is $sigma_"dc"=1/eta=n_"e"e^2/(m_"e"nu)$.]
  )

  #governing-law(
    [Spitzer scaling in the stated collision convention],
    [$nu_"e i" approx sqrt(2) omega_(p,e)^4/(64 pi n_"e")
      (k_B T_"e"/m_"e")^(-3/2) ln Lambda$ gives
    $eta_"Sp" approx pi/(2 sqrt(2))
      e^2 sqrt(m_"e")/(k_B T_"e")^(3/2) ln Lambda$.
    Thus $eta_"Sp"$ is approximately independent of density at fixed
    temperature, apart from the weak density dependence hidden in
    $ln Lambda$. Its dominant temperature scaling is
    $eta_"Sp" ∝ T_"e"^(-3/2)$, while
    $sigma_"Sp"$ scales as $T_"e"^(3/2)/ln Lambda$.]
  )

  #rechenbeispiel[
    Using the Coulomb rate from the previous section for
    $n_"e"=qty("1.0e10", "cm^-3")$ and
    $nu_"e i"=qty("2.54e3", "s^-1")$, calculate the scalar resistivity and
    DC conductivity in Gaussian CGS with
    $e=qty("4.803e-10", "statC")$ and
    $m_"e"=qty("9.109e-28", "g")$.

    Numerical result: $eta_"Sp"=qty("1.00e-15", "s")$ and
    $sigma_"dc"=qty("9.97e14", "s^-1")$.
  ]

  #details(
    [Derivation: drag, current, and Spitzer scaling],
    [Start with the electron--ion frictional force density
    $bold(R)_"e i"=m_"e"n_"e"nu_"e i"
      (bold(u)_"i"-bold(u)_"e")$.
    For singly charged hydrogen and quasi-neutrality,
    $bold(j)=e n_"e"(bold(u)_"i"-bold(u)_"e")$.
    Divide the drag by the charge density scale $e n_"e"$:
    $bold(R)_"e i"/(e n_"e")
      =m_"e"nu_"e i"bold(j)/(n_"e"e^2)$.
    Identifying the coefficient of $bold(j)$ with the resistivity gives
    $eta=m_"e"nu_"e i"/(n_"e"e^2)$ and therefore
    $sigma_"dc"=n_"e"e^2/(m_"e"nu_"e i")$.

    Insert the Coulomb rate and
    $omega_(p,e)^4=(4 pi n_"e"e^2/m_"e")^2$:
    $eta_"Sp"=m_"e"/(n_"e"e^2)
      [sqrt(2)omega_(p,e)^4/(64 pi n_"e")]
      (k_B T_"e"/m_"e")^(-3/2)ln Lambda$.
    Cancelling the explicit density factors gives the displayed temperature
    scaling and leaves only the weak logarithmic density dependence. The
    cancellation does not mean that density is irrelevant to the plasma: it
    changes current for a given drift and changes $Lambda$.]
  )

  #interpretation(
    [More carriers do not automatically mean lower resistivity],
    [Adding carriers raises the current available at a given drift, but in a
    fully ionized plasma it also raises the collision rate. At fixed
    temperature these effects largely cancel in the scalar Spitzer resistivity;
    the conductivity still tells how much current a specified electric field
    drives.]
  )

  #summary[
    Linear drag converts the collision frequency into
    $eta=m_"e"nu/(n_"e"e^2)$ and
    $sigma_"dc"=n_"e"e^2/(m_"e"nu)$. Neutral and Coulomb channels supply
    different $nu$. With the stated Coulomb convention, Spitzer resistivity
    scales mainly as $T_"e"^(-3/2)ln Lambda$ and is nearly density-independent
    at fixed temperature.
  ]

  #knowledge-check((
    (
      question: [What physical quantity is divided by the charge density to obtain resistivity?],
      answer: [The collisional drag force density is divided by the charge
      density scale and expressed per current. This gives
      $eta=m_"e"nu/(n_"e"e^2)$ in the scalar model.]
    ),
    (
      question: [How are resistivity and conductivity related in this Gaussian-CGS convention?],
      answer: [They are reciprocals in the scalar model:
      $sigma=1/eta$. Resistivity has units #unit("s") and conductivity has
      units #unit("s^-1") when $bold(E)=eta bold(j)$.]
    ),
    (
      question: [What is the dominant temperature scaling of Spitzer resistivity?],
      answer: [At fixed Coulomb logarithm,
      $eta_"Sp" ∝ T_"e"^(-3/2)$. The logarithm varies only weakly
      with density and temperature in a weakly coupled plasma.]
    ),
    (
      question: [Why must the collision channel be stated before quoting a resistivity?],
      answer: [Because $nu$ may be electron--neutral, electron--ion, or a sum
      of momentum-transfer channels. Different target populations and cross
      sections produce different drag and therefore different resistivity.]
    ),
  ))

  #section-title[Plasma conductivity: DC, AC, and ion motion] <plasma-conductivity>

  #lead[
    How does a magnetic field change the relation between electric field and
    current? It makes the response anisotropic. Current parallel to the field
    is not gyroscopically deflected, while perpendicular current is split into
    a dissipative Pedersen part and a nondissipative Hall part. At finite
    frequency, inertia makes every entry complex.
  ]

  #objectives((
    [derive the unmagnetized DC conductivity from the linear momentum equation],
    [construct the magnetized conductivity tensor and identify its three components],
    [extend the tensor to harmonic AC response],
    [include ion motion and identify the limits of an electron-only model],
  ))

  #unit-ledger[
    Gaussian CGS is active: $bold(E)$ is in statvolt per #unit("cm"),
    $bold(B)_0$ is in gauss, $bold(j)$ is in statcoulomb per #unit("cm^2")
    per #unit("s"), and all collision, cyclotron, and wave frequencies are in
    #unit("s^-1"). The conductivity tensor entries are in #unit("s^-1");
    $omega$ and $Omega$ are frequencies, while $i$ is the dimensionless
    imaginary unit with $i^2=-1$.
  ]

  #assumption(
    [Homogeneous linear response],
    [Linearize around a uniform equilibrium with
    $bold(B)=bold(B)_0+bold(B)_1$, $n_"e"=n_"e0"+n_"e1"$,
    $bold(E)_0=bold(0)$, and $bold(u)_"e0"=bold(0)$. Neglect pressure
    gradients in the homogeneous conductivity calculation. First take ions
    as immobile, then add their current as a species sum. Use fields
    proportional to $exp(-i omega t)$.]
  )

  The linear electron momentum equation becomes

  $m_"e"(nu_"e"-i omega)bold(u)_"e"
    =q_"e"(bold(E)+bold(u)_"e"times bold(B)_0/c)$.

  For an unmagnetized plasma, $bold(B)_0=bold(0)$, so

  $bold(j)=sigma_"dc"bold(E),
    quad sigma_"dc"=n_"e"q_"e"^2/(m_"e"nu_"e")$.

  Align the $z$ axis with $bold(B)_0$ and define the signed electron
  cyclotron frequency

  $Omega_"e"=q_"e"B_0/(m_"e"c)$.

  #conductivity-tensor

  For DC response, set $omega=0$. The component equations are

  $ J_x=sigma_"dc" E_x+(Omega_"e"/nu_"e")J_y,
    quad J_y=sigma_"dc" E_y-(Omega_"e"/nu_"e")J_x,
    quad J_z=sigma_"dc" E_z $.

  Thus

  $ mat(J_x; J_y; J_z)
    =mat(sigma_"perp", sigma_"H", 0;
         -sigma_"H", sigma_"perp", 0;
         0, 0, sigma_"parallel") mat(E_x; E_y; E_z), $

  with

  $ sigma_"parallel"=sigma_"dc",
    quad sigma_"perp"=sigma_"dc"nu_"e"^2/(nu_"e"^2+Omega_"e"^2),
    quad sigma_"H"=sigma_"dc"nu_"e"Omega_"e"
      /(nu_"e"^2+Omega_"e"^2) $.

  The sign of $sigma_"H"$ follows the signed charge convention. Its magnitude
  describes current perpendicular to both the applied electric field and the
  background magnetic field.

  #rechenbeispiel[
    Consider a homogeneous electron plasma with
    $n_"e"=qty("1.0e10", "cm^-3")$,
    $nu_"e"=qty("2.5e3", "s^-1")$,
    $B_0=qty("100", "G")$,
    $e=qty("4.803e-10", "statC")$,
    $m_"e"=qty("9.109e-28", "g")$, and
    $c=qty("2.998e10", "cm/s")$. With
    $q_"e"=-e$, determine the signed cyclotron frequency and the three DC
    tensor entries.

    Numerical result: $Omega_"e"=qty("-1.76e9", "s^-1")$,
    $sigma_"parallel"=qty("1.01e15", "s^-1")$,
    $sigma_"perp"=qty("2.05e3", "s^-1")$, and
    $sigma_"H"=qty("-1.44e9", "s^-1")$.
  ]

  #details(
    [Derivation: DC and AC conductivity tensor],
    [Let $a_"e"=nu_"e"-i omega$. Multiplying the harmonic momentum equation
    by $n_"e"q_"e"$ and using $bold(j)=n_"e"q_"e"bold(u)_"e"$ gives
    $bold(j)=n_"e"q_"e"^2/(m_"e"a_"e")bold(E)
      + (Omega_"e"/a_"e")bold(j)times hat(bold(z))$.
    In components,
    $J_x=sigma_0 E_x+(Omega_"e"/a_"e")J_y$ and
    $J_y=sigma_0 E_y-(Omega_"e"/a_"e")J_x$ with
    $sigma_0=n_"e"q_"e"^2/(m_"e"a_"e")$.
    Solving the two coupled equations gives
    $sigma_"perp"=n_"e"q_"e"^2 a_"e"
      /(m_"e"(a_"e"^2+Omega_"e"^2))$,
    $sigma_"H"=n_"e"q_"e"^2 Omega_"e"
      /(m_"e"(a_"e"^2+Omega_"e"^2))$, and
    $sigma_"parallel"=n_"e"q_"e"^2/(m_"e"a_"e")$.
    Setting $omega=0$ recovers the displayed real DC tensor.

    If ions are mobile, sum the response of every species. Define
    $omega_(p,s)^2=4 pi n_s q_s^2/m_s$,
    $Omega_s=q_s B_0/(m_s c)$, and
    $a_s=nu_s-i omega$. In Gaussian CGS,
    $sigma_"parallel"=1/(4 pi)sum_s omega_(p,s)^2/a_s$,
    $sigma_"perp"=1/(4 pi)sum_s
      omega_(p,s)^2 a_s/(a_s^2+Omega_s^2)$, and
    $sigma_"H"=1/(4 pi)sum_s
      omega_(p,s)^2 Omega_s/(a_s^2+Omega_s^2)$.
    These sums are additive because the total current is
    $bold(j)=sum_s n_s q_s bold(u)_s$. An electron-only model is appropriate
    when the ions are effectively fixed on the frequency and collision scales;
    at low frequency, ion motion can change every tensor entry.]
  )

  #interpretation(
    [Three current directions, three physical responses],
    [The parallel conductivity measures current along $bold(B)_0$. The
    Pedersen conductivity is the dissipative perpendicular response, reduced
    when $abs(Omega_"e") >> nu_"e"$. The Hall conductivity rotates the
    perpendicular current and changes sign when the charge sign changes. AC
    response replaces the real drag rate by $nu-i omega$, revealing phase lag
    from inertia.]
  )

  #summary[
    A magnetic field turns scalar Drude conductivity into a tensor with
    parallel, perpendicular/Pedersen, and Hall entries. In harmonic response
    use $a_s=nu_s-i omega$; with mobile ions, add the species conductivity
    tensors. Every entry is in #unit("s^-1") in Gaussian CGS and carries the
    signed-charge convention through $Omega_s$.
  ]

  #knowledge-check((
    (
      question: [Why is the conductivity tensor anisotropic in a magnetic field?],
      answer: [Gyromotion deflects a perpendicular drift but does not deflect
      motion parallel to $bold(B)_0$. The electric-field direction therefore
      no longer determines the current direction by a scalar coefficient.]
    ),
    (
      question: [What is the physical distinction between Pedersen and Hall current?],
      answer: [Pedersen current follows the perpendicular electric field and
      dissipates energy through collisions. Hall current is perpendicular to
      both the perpendicular electric field and $bold(B)_0$ and reverses with
      the signed charge convention.]
    ),
    (
      question: [How is DC conductivity generalized to harmonic AC response?],
      answer: [For fields proportional to $exp(-i omega t)$, replace
      $nu$ by $a=nu-i omega$ in the coupled momentum equations. The resulting
      conductivities are complex and contain collisional drag and inertia.]
    ),
    (
      question: [When must ion motion be included in the conductivity?],
      answer: [Include it when the frequency is low enough, or the collision and
      magnetization ordering is such, that ions acquire a significant drift.
      Then use the additive species current
      $bold(j)=sum_s n_s q_s bold(u)_s$ rather than an electron-only model.]
    ),
  ))

  #chapter-nav(
    previous: (href: "06-mhd.html", title: [Single-fluid MHD]),
    next: (href: "08-diffusion.html", title: [Diffusion]),
  )
]
