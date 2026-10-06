#import "../theme.typ": *
#import "@preview/physica:0.9.8": pdv, dv
#import "../figures.typ": derived-plot
#import "../thermal-figures.typ": microstates, thermal-table, slot-standing-wave, slot-momentum-cutoff

#let chapter = [
  #page-title(number: 2)[Temperature, entropy, and thermal ionization] <thermal-equilibrium>
  #lead[
    Ionization costs energy, yet a hydrogen gas can become substantially ionized
    far below the temperature corresponding to the binding energy of one atom.
    Counting accessible states explains this balance. It also derives the
    Boltzmann electron response used in the next chapter. The statistical
    framework follows @reif1965; thermal ionization follows @saha1920.
  ]

  #section-title[Entropy as counted microstates] <thermal-microstates>
  #lead[
    A macroscopic description specifies totals, such as energy and particle
    number, without specifying each particle's microscopic state. How many
    microscopic arrangements realize the same totals? Their number is the
    multiplicity $W$. A microstate is one fully specified microscopic arrangement;
    a macrostate is the collection of constraints that those arrangements share.
  ]
  #objectives((
    [count independent binary choices and distinguish multiplication from addition],
    [explain why the logarithm converts multiplicity into additive entropy],
  ))
  #unit-ledger[
    Multiplicity $W$ is a dimensionless count. Entropy $S$ is in #unit("J/K");
    Boltzmann's constant $k_B$ is in #unit("J/K").
  ]
  Each cell in a simple counting model can be open or filled. A configuration
  specifies the state of every cell. For $a$ independent two-state cells,
  the next cell doubles the possibilities:
  $ W_a = 2^a, quad W_1 = 2, quad W_2 = 4, quad W_3 = 8 . $ <thermal-binary-count>
  Combining two independent systems A and B pairs every state of A with every
  state of B. Thus the combined count is $W_A W_B$, not $W_A+W_B$.
  Define entropy by taking the natural logarithm, denoted $ln$:
  $ S = k_B ln W, quad S_(A+B) = S_A + S_B . $ <thermal-entropy>
  The logarithm is dimensionless because its argument is a count. Multiplying
  by $k_B$ fixes the physical entropy scale. This counting definition assumes
  equal statistical weight for accessible microstates of an isolated system.
  #figure(microstates(),
    alt: "All two, four, and eight configurations of one, two, and three binary cells; a new independent cell doubles the count.",
    caption: [Rows enumerate microstates. Open and filled circles distinguish
      the two choices without relying on color. The counts $W$ have unit [1].])
  Interaction energy or shared constraints can prevent factorization; then
  independence must be justified before adding subsystem entropies.
  #summary[
    Independent possibilities multiply; their logarithms add. Entropy records
    the accessible microscopic freedom behind a macroscopic description.
  ]
  #knowledge-check((
    (
      question: [Two independent cells have three states each. What is their multiplicity?],
      answer: [Nine, a dimensionless count: each of the three first choices pairs with three second choices.],
    ),
    (
      question: [Why does adding one binary cell to two cells yield eight rather than six states?],
      answer: [Each of the four existing states receives two alternatives, so the count is multiplied by two.],
    ),
    (
      question: [How much entropy does an independent binary cell add?],
      answer: [$k_B ln 2$, in #unit("J/K"), because it multiplies the total multiplicity by two.],
    ),
    (
      question: [If two cells must always have equal states, may their individual counts be multiplied?],
      answer: [No. The constraint leaves only the two equal-state pairs, so the choices are correlated.],
    ),
  ))

  #section-title[Temperature] <thermal-temperature>
  #lead[
    Two boxes exchange a small energy while their combined energy remains
    fixed. The favored transfer is the one that opens more combined microstates.
    Temperature measures the entropy gained per unit energy, rather than the
    total energy in a box.
  ]
  #objectives((
    [define temperature through an entropy derivative with its fixed constraints],
    [infer the direction of energy exchange and the condition for equilibrium],
  ))
  #unit-ledger[
    Pressure $p$ is in #unit("Pa"). Chemical potential $mu$ is in #unit("J") per particle; total momentum
    $bold(P)$ is in #unit("kg.m/s"). Its conjugate bulk velocity $bold(u)$
    is in #unit("m/s").
  ]
  Let $E$ be total energy, $V$ volume, $N$ particle number, and $bold(P)$ total
  momentum. At fixed $V$, $N$, and $bold(P)$, define absolute temperature $T$,
  measured in #unit("K"), by
  $ 1/T = pdv(S, E), quad dif S = (dif E)/T . $ <thermal-temperature-definition>
  #equation-note[The derivative holds $V$, $N$, and $bold(P)$ fixed.
    Its unit is #unit("K^-1").]
  If A receives energy $dif E_A$ from B, then $dif E_B=-dif E_A$ and
  $ dif S_(A+B) = (1/T_A - 1/T_B) dif E_A . $ <thermal-exchange>
  At positive temperatures, energy flows from hotter to colder: taking
  $T_B>T_A$ makes the coefficient positive. At the maximum of total entropy,
  the first-order change vanishes for either transfer direction, so $T_A=T_B$.
  A stable maximum also requires negative curvature along the transfer direction.
  #definition([Thermodynamic differential], [
    Pressure $p$ is the mechanical force per area. Chemical potential $mu$
    measures the energy cost of adding a particle at fixed entropy, volume, and
    momentum. With bulk velocity $bold(u)$ conjugate to momentum,
    $ dif E = T dif S - p dif V + mu dif N + bold(u) dot dif bold(P) . $ <thermal-first-law>
    In a mixture, replace $mu dif N$ by the sum over species.
  ])
  The ideal translational gas considered here has an unbounded kinetic-energy
  spectrum and increasing entropy with energy, so $T>0$. Negative absolute
  temperatures require a bounded accessible energy spectrum and do not describe
  the Maxwellian plasma model.
  #details([Derivation: entropy maximum for two boxes], [
    Write $S_"tot"(E_A)=S_A(E_A)+S_B(E_"tot"-E_A)$ with fixed total
    energy $E_"tot"$. The chain rule gives
    $ dv(S_"tot", E_A)=pdv(S_A,E_A)-pdv(S_B,E_B)=1/T_A-1/T_B . $
    Setting this derivative to zero gives equality of temperatures. For positive
    heat capacities $C_A=dv(E_A,T_A)$ and $C_B=dv(E_B,T_B)$, each in #unit("J/K"),
    $ dv(S_"tot",E_A,2)=-1/(T_A^2 C_A)-1/(T_B^2 C_B)<0 . $
    Thus the stationary state is a maximum under energy exchange.
  ])
  #summary[
    Inverse temperature is the entropy slope with respect to energy. Equality
    of those slopes stops net energy exchange at thermal equilibrium.
  ]
  #knowledge-check((
    (
      question: [Which constraints belong to the entropy definition of temperature?],
      answer: [Volume, particle number, and total momentum stay fixed while energy changes.],
    ),
    (
      question: [A colder box receives a small energy from a hotter box. What happens to total entropy?],
      answer: [It increases: the colder box gains more entropy than the hotter box loses per joule.],
    ),
    (
      question: [Does equal energy in two boxes imply equal temperature?],
      answer: [No. Different particle numbers, volumes, or spectra can give different entropy slopes at the same energy.],
    ),
    (
      question: [Why are negative absolute temperatures excluded in this gas model?],
      answer: [Its kinetic-energy spectrum has no upper bound; the bounded-spectrum condition for a negative-temperature equilibrium is absent.],
    ),
  ))

  #section-title[The Boltzmann factor and the Maxwellian] <thermal-boltzmann>
  #lead[
    A small system can take energy from a much larger reservoir. A high-energy
    state of the small system leaves less energy, and fewer possibilities,
    for the reservoir. This loss supplies the Boltzmann factor.
  ]
  #objectives((
    [derive the weight of a subsystem microstate from a reservoir entropy expansion],
    [separate conserved bulk momentum from thermal motion and normalize a Maxwellian],
  ))
  #unit-ledger[
    Velocity probability density $F_s$ is in #unit("s^3/m^3").
  ]
  Let $P_a$ be the dimensionless probability of a particular subsystem
  microstate $a$ with energy $E_a$. The reservoir, labelled rest, has energy
  $E_"tot"-E_a$. At fixed reservoir volume and particle number,
  $ P_a prop W_"rest"(E_"tot"-E_a)
    = exp(S_"rest"(E_"tot"-E_a)/k_B) . $ <thermal-reservoir>
  A large reservoir changes temperature negligibly on exchanging $E_a$.
  Expanding its entropy to first order gives
  $ S_"rest"(E_"tot"-E_a) approx S_"rest"(E_"tot") - E_a/T,
    quad P_a = exp(-E_a/(k_B T))/Z . $ <thermal-boltzmann-factor>
  The dimensionless partition sum $Z=sum_a exp(-E_a/(k_B T))$ normalizes the probabilities.
  For an energy interval, also count the subsystem states in that interval;
  the Boltzmann factor alone is a weight per microstate, not an energy histogram.
  For $N$ equal-mass particles of mass $m$, conserved momentum sets the mean
  velocity $bold(u)=bold(P)/(N m)$. Their kinetic energy separates as
  $ sum_(j=1)^N (m bold(v)_j^2)/2
    = bold(P)^2/(2 N m) + sum_(j=1)^N (m (bold(v)_j-bold(u))^2)/2 . $ <thermal-flow-energy>
  The bulk term is fixed. The fluctuating velocity relative to $bold(u)$
  therefore receives the thermal weight. For species $s$, define $F_s$ as a
  velocity probability density with $integral F_s dif^3 v=1$:
  $ F_s(bold(v)) = 1/(pi^(3/2) v_("th",s)^3)
    exp(-((bold(v)-bold(u)_s)^2)/v_("th",s)^2),
    quad v_("th",s)=sqrt((2 k_B T_s)/m_s) . $ <thermal-maxwellian>
  #equation-note[$F_s$ has unit #unit("s^3/m^3"). Multiplying by the
    density $n_s$ gives the phase-space distribution at a homogeneous point.
    This is exactly the #chapter-link("intro-speed-energy-temperature")[§1.2]
    thermal-speed convention: the one-component variance is $k_B T_s/m_s$,
    and the most probable three-dimensional speed relative to the flow is $v_("th",s)$.]
  #figure(derived-plot("maxwellian_drift"),
    alt: "Normalized velocity distributions have the same width but shifted peaks as the mean flow changes; axes have unit [1].",
    caption: [Changing mean flow shifts a Maxwellian; heating changes its width.
      The velocity normalization uses the thermal speed defined in §1.2.])
  A Maxwellian requires thermal equilibration. Beams, anisotropy, or different
  electron and ion temperatures need a kinetic description beyond one common
  equilibrium temperature. The reservoir expansion fails if its temperature
  changes appreciably during the exchange.
  #summary[
    The reservoir's loss of states gives $exp(-E/(k_B T))$. At fixed bulk
    momentum, the relevant kinetic energy is measured relative to the mean flow.
  ]
  #knowledge-check((
    (
      question: [Why does a subsystem energy cost reduce its probability?],
      answer: [It removes energy from the reservoir, reducing reservoir entropy by approximately $E/T$.],
    ),
    (
      question: [Is the probability of an energy interval just its Boltzmann factor?],
      answer: [No. Multiply the microstate weight by the number of subsystem states in that interval.],
    ),
    (
      question: [A flow doubles while the random velocity variance stays fixed. Does the temperature change?],
      answer: [No. Temperature measures the velocity spread relative to the mean flow, whose kinetic energy is separately conserved.],
    ),
    (
      question: [When is the reservoir entropy expansion unreliable?],
      answer: [When exchanged energy changes the reservoir temperature substantially, so higher-order entropy terms matter.],
    ),
  ))
  #section-title[The Saha equation] <thermal-saha>
  #lead[
    Removing an electron from an atom costs ionization energy but gives that
    electron a vast set of free translational states. Counting the change in
    possibilities determines the equilibrium composition without requiring a
    typical particle's thermal energy to equal the binding energy.
  ]
  #objectives((
    [derive the add and remove factors for indistinguishable dilute particles],
    [derive Saha balance by canceling heavy-particle translational factors],
    [identify electron freedom, internal states, and the reservoir energy penalty],
  ))
  #unit-ledger[
    Planck's constant $h$ is in #unit("J.s"); thermal de Broglie wavelength
    $lambda_("th",s)$ is in #unit("m"). Ionization energy $chi$ is in
    #unit("J") or #unit("eV"). Box side $L$ and volume $V$ are in
    #unit("m") and #unit("m^3"). Momenta $p_s$ and $p_("th",s)$ are in
    #unit("kg.m/s"). Sharp-cutoff wavelength $lambda_s$ is in #unit("m");
    density $n_s$ is in #unit("m^-3"). Counts $M_s$,
    $N_s$, and $g_s$ have unit [1].
  ]
  #assumption([Dilute equilibrium mixture], [
    Neutral atoms n, singly ionized ions i, and free electrons e share one
    temperature and volume. Local thermodynamic equilibrium means that
    collisions establish thermal velocities and reversible ionization and
    recombination balance locally. Quantum occupation is dilute:
    $n_s lambda_("th",s)^3/g_s << 1$. Interactions do not shift the isolated
    atom's binding energy. Only one ionization stage is retained.
  ])
  First estimate the number of one-particle patterns in a box. A wave reflects
  from the walls and forms a standing mode. In one direction its wavelength
  $lambda_s=h/p_s$ fits an integer number of half-waves across side $L$.
  Independent directions give about one distinguishable pattern per spatial
  cell of volume $lambda_s^3$. For momentum scale $p_s$, the sharp-cutoff
  estimate is
  $ lambda_s=h/p_s, quad M_s approx g_s V/lambda_s^3,
    quad M_s/N_s approx g_s/(n_s lambda_s^3) . $ <thermal-mode-estimate>
  Geometry and boundary conditions change only order-one factors in this
  estimate. The internal degeneracy $g_s$ counts states with the same energy;
  $N_s=n_s V$ is the number of particles of species $s$.
  #figure(slot-standing-wave(),
    alt: "A standing wave is drawn between two box walls. Its normalized amplitude vanishes at both walls; a double arrow marks one wavelength lambda_s inside box side L.",
    caption: [A one-dimensional section of a box mode; independent standing-wave choices in the other two directions give the volume estimate $V/lambda_s^3$. The plotted amplitude is normalized and labelled [1]; $L$ and $lambda_s$ are lengths in #unit("m").])

  Let $bold(p)$ be a particle's momentum vector and $p=abs(bold(p))$ its
  magnitude. Thermal particles do not stop at a sharp momentum boundary.
  Momentum states carry a Maxwell--Boltzmann weight
  $exp(-bold(p)^2/(2m_s k_B T))$. The
  characteristic thermal momentum is $p_("th",s)=sqrt(2m_s k_B T)$, so the
  one-wavelength estimate would use $lambda_s=h/p_("th",s)$.
  #figure(slot-momentum-cutoff(),
    alt: "Relative weight per momentum state versus momentum magnitude divided by thermal momentum. The dashed sharp cutoff stays level below p_th and drops to zero above it; the solid Maxwellian weight decays smoothly as exp of minus p squared over p_th squared and has a tail beyond p_th.",
    caption: [The cutoff counts all states below $p_("th",s)$ equally. The Maxwellian assigns weight $exp(-(p/p_("th",s))^2)$ per state, with a tail beyond the marked thermal momentum. Both plotted axes are normalized and labelled [1].])

  The exact effective slot count averages over these weights. Each quantum
  state occupies phase-space volume $h^3$:
  $ integral exp(-bold(p)^2/(2m_s k_B T)) dif^3 p
      = (2 pi m_s k_B T)^(3/2) . $ <thermal-momentum-volume>
  Thus the Gaussian integral replaces the sharp momentum boundary by
  $ lambda_("th",s)=h/sqrt(2 pi m_s k_B T)
    = h/(sqrt(pi) m_s v_("th",s))
    = lambda_s/sqrt(pi) . $ <thermal-wavelength>
  The wavelength changes by the order-one factor $sqrt(pi)$; the corresponding
  momentum-space volume changes by $pi^(3/2)$. The thermal slot count and its
  count per particle are
  $ M_s=(g_s V)/lambda_("th",s)^3,
    quad M_s/N_s=g_s/(n_s lambda_("th",s)^3) . $ <thermal-slots>
  Exact-to-sharp-cutoff slot-volume ratio:
  $ M_s(T)/(g_s V/lambda_s^3)=pi^(3/2) . $ <thermal-slot-volume-correction>
  The full Gaussian momentum integral is the precise replacement for the
  de Broglie-cell estimate; the estimate captures the scale of the available
  translational states.
  #details([Derivation: thermally weighted slots], [
    A quantum state occupies phase-space volume $h^3$. With momentum $bold(p)$,
    $ M_s=(g_s V)/h^3 integral exp(-bold(p)^2/(2 m_s k_B T)) dif^3 p . $
    Each Cartesian Gaussian integral is $sqrt(2 pi m_s k_B T)$. Their product
    gives $(2 pi m_s k_B T)^(3/2)$ and hence $g_s V/lambda_("th",s)^3$.
  ])
  For $N_s$ indistinguishable particles, count each slot assignment once,
  rather than once per particle permutation. In the dilute limit,
  $ W_s(N_s) approx M_s^(N_s)/(N_s!) . $ <thermal-dilute-count>
  Adding and removing one particle respectively give
  $ W_s(N_s+1)/W_s(N_s)=M_s/(N_s+1) approx M_s/N_s . $ <thermal-add-remove>
  $ W_s(N_s-1)/W_s(N_s)=N_s/M_s . $ <thermal-remove>
  The approximation $N_s+1 approx N_s$ also assumes macroscopic populations.
  Counts factor across species in this ideal-mixture model. For one reaction
  $"A" <==> "A"^+ + e^-$, remove a neutral and add an ion and an electron.
  The reservoir pays energy $chi$, multiplying its possibilities by
  $exp(-chi/(k_B T))$. With $n_s=N_s/V$, the complete ratio is
  $ R=W_"after"/W_"before"
    = (n_n lambda_("th",n)^3)/g_n
    times g_i/(n_i lambda_("th",i)^3)
    times g_e/(n_e lambda_("th",e)^3)
    times exp(-chi/(k_B T)) . $ <thermal-ionization-ratio>
  Every factor and $R$ are dimensionless. If $R>1$, further ionization
  increases entropy; if $R<1$, recombination does. At the composition maximum,
  $R=1$. Since electron mass is small compared with atom or ion mass,
  $m_n approx m_i$ and $lambda_("th",n) approx lambda_("th",i)$.
  The wavelength and internal-state part of the neutral--ion factor cancels:
  $ (lambda_("th",n)/lambda_("th",i))^3 (g_i/g_n) approx 1 . $
  <thermal-translational-cancellation>
  The remaining $n_n/n_i$ is a composition factor, not part of that
  cancellation. This uses the lecture approximation $g_i=g_n=1$. Electron
  spin gives $g_e=2$:
  $ R approx n_n/(n_i n_e) (2 g_i)/(g_n lambda_("th",e)^3)
    exp(-chi/(k_B T)) . $ <thermal-heavy-cancellation>
  #governing-law([Saha composition balance], [
    Setting $R=1$ gives
    $ (n_i n_e)/n_n
      = underbrace(g_e/lambda_("th",e)^3, "free-electron states")
      underbrace(g_i/g_n, "internal states")
      underbrace(exp(-chi/(k_B T)), "energy penalty") . $
      <thermal-saha-equation>
    With $g_i=g_n=1$ and $g_e=2$, substituting the thermal wavelength gives
    $ (n_i n_e)/n_n
      = 2 (2 pi m_e k_B T/h^2)^(3/2) exp(-chi/(k_B T)) . $
      <thermal-saha-electron-mass>
  ])
  The left side and electron-state factor have unit #unit("m^-3"). The other
  factors are dimensionless. Internal quantum states add order-one factors;
  we ignore them here by setting $g_i=g_n=1$. This is a lecture simplification,
  not a detailed hydrogen partition-function calculation. The newly liberated
  free electron is the new translational freedom: its huge number of states
  compensates the energy penalty. Saha equilibrium @saha1920 does not describe
  every ionized gas; chemical detailed balance must also hold.
  #summary[
    One ionization removes a neutral, adds an ion and electron, and costs
    reservoir energy. Heavy-particle translational factors cancel; free-electron
    states provide the large entropy gain.
  ]
  #knowledge-check((
    (
      question: [Why does adding a particle give $M_s/(N_s+1)$ rather than $M_s$?],
      answer: [Indistinguishability gives the factorial ratio $N_s!/(N_s+1)!=1/(N_s+1)$.],
    ),
    (
      question: [What does the sharp-cutoff slot estimate count?],
      answer: [About $g_s V/lambda_s^3$ standing-wave patterns, one per de Broglie spatial cell up to geometric factors.],
    ),
    (
      question: [How does $lambda_s=h/p_("th",s)$ compare with $lambda_("th",s)$?],
      answer: [$lambda_s=sqrt(pi) lambda_("th",s)$; the Gaussian momentum integral gives the exact thermal wavelength.],
    ),
    (
      question: [Can this Saha model describe ionization by a nonthermal beam?],
      answer: [No. Beam ionization depends on the electron distribution and reaction kinetics; a reservoir weight is insufficient.],
    ),
  ))

  #section-title[How much thermal ionization?] <thermal-ionization>
  #lead[
    A composition equation becomes predictive when the total inventory is
    specified. For single-stage hydrogen, neutrality and nucleus conservation
    reduce three densities to one ionization fraction.
  ]
  #objectives((
    [compute a hydrogen ionization fraction at given temperature and nucleus density],
    [explain the logarithmic thermal threshold and its relation to binding energy],
    [select Saha or a kinetic rate model from the equilibration conditions],
  ))
  #unit-ledger[
    Ionization fraction $x$ and Saha parameter $A$ are dimensionless. Nucleus
    density $n=n_i+n_n$ is in #unit("m^-3"). Plot temperature is $k_B T$
    in #unit("eV"), with a second axis showing $T$ in #unit("K").
  ]
  Use $chi=qty("13.6","eV")$, $g_i=g_n=1$, and neutrality $n_e=n_i$.
  Density $n$ counts nuclei, not electrons plus ions plus neutrals. Define
  $x=n_i/n$, so $n_i=n_e=x n$ and $n_n=(1-x)n$. Then
  $ x^2/(1-x)=A(T,n), quad
    A(T,n)=2/(n lambda_("th",e)^3) exp(-chi/(k_B T)) . $ <thermal-fraction-balance>
  The physical root lies between zero and one:
  $ x=2 A/(A+sqrt(A^2+4 A))=2/(1+sqrt(1+4/A)) . $ <thermal-fraction-solution>
  For $A << 1$, $x approx sqrt(A)$; for $A >> 1$, $1-x approx 1/A$.
  #figure(derived-plot("saha_fraction", width: 100%),
    alt: "Hydrogen ionization rises with thermal energy; higher nucleus density shifts the half-ionization point upward. Four styled curves span 10^6 to 10^24 per cubic meter; markers show x=0.5 and five example-plasma temperatures are reference lines.",
    caption: [Single-stage equilibrium hydrogen with $g_i=g_n=1$. Markers show
      half ionization. Example temperatures provide context, not predictions
      for actual compositions; several examples are outside local thermodynamic equilibrium.])
  At $x=1/2$, the left side is $1/2$, not one. The exact condition is
  $ k_B T_(1/2)=chi/ln(4/(n lambda_("th",e)(T_(1/2))^3)) . $ <thermal-half-temperature>
  Iterate because the wavelength depends on temperature. Replacing 4 by 2
  gives a rough threshold at equal entropy and energy factors. That crossing
  actually has $x=(sqrt(5)-1)/2 approx 0.618$ instead of half ionization.
  #thermal-table()
  #figure(derived-plot("saha_factors", width: 100%),
    alt: "At nucleus density 10^18 per cubic meter electron-state freedom grows slowly with temperature while the inverse energy penalty falls quickly; exact half ionization includes a factor one half on the cost curve.",
    caption: [Competing factors at $n=qty("1e18","m^-3")$. Their unshifted
      equality gives $A=1$. The dotted cost includes the factor $1/2$ needed
      for exact half ionization, whose temperature is marked vertically.])
  Constants follow @nist2022. Here $chi/k_B approx qty("157821","K")$.
  Over the table's densities the exact logarithm falls from 48.93 to 6.02;
  half-ionization temperature rises from #qty("3226","K") to #qty("26230","K").
  At $n=qty("1e18","m^-3")$, the logarithm is 22.46 and
  $k_B T_(1/2)=qty("0.605","eV")$.
  Density enters the logarithm, so many orders of magnitude in density produce
  a much smaller relative threshold shift. The familiar $T tilde.op qty("1e4","K")$
  captures the order of magnitude at intermediate densities. It is neither a
  universal half-ionization temperature nor a definition of plasma.
  A dense, detached divertor provides a test of equilibrium among highly
  excited levels. In the Alcator C-Mod tokamak, the measured populations of
  excited deuterium atoms agree with Saha–Boltzmann predictions within a
  factor of 1.5 for principal quantum number $p >= 5$, at
  $k_B T_e=qty("1.2", "eV") approx qty("1.4e4", "K")$ and
  $n_e=n_i=qty("8.8e20", "m^-3")$ @lumma1997recombination.
  Here $p$ labels the bound level (dimensionless), and $n_("D")(p)$ is its
  neutral-deuterium population density in #unit("m^-3"). This partial
  equilibrium of excited levels does not imply Saha balance of ground-state
  atoms throughout the divertor.
  #figure(derived-plot("saha_cmod", width: 100%),
    alt: "Excited-deuterium densities in the detached Alcator C-Mod divertor rise from levels p=5 to 10; measured points lie 1.0 to 1.5 times above the Saha curve. The p=3 point is context. Bars show digitization uncertainty and the band spans measured electron temperature and density ranges.",
    caption: [Saha–Boltzmann populations compared with redrawn data from
      Lumma, Terry, and Lipschultz, _Physics of Plasmas_ *4*, 2555 (1997),
      #link("https://doi.org/10.1063/1.872234")[doi:10.1063/1.872234], Fig. 7b.
      Bars show digitization uncertainty only (±0.04 dex), not experimental
      confidence intervals. The band spans the measured
      $k_B T_e=qty("0.8", "eV")$–#qty("1.5", "eV") and ±20% $n_e$ ranges,
      with quasineutrality $n_i=n_e$.])
  #interpretation([Validity limits], [
    Saha requires local thermodynamic equilibrium and the appropriate reverse
    reactions. In dilute plasmas where radiative escape dominates recombination,
    such as the solar corona, tokamak edge, and many laboratory discharges,
    use coronal or collisional-radiative rate balance. External photons and
    nonthermal electrons ionize gases below a thermal threshold. At very high
    density, interactions lower or erase bound-state thresholds (pressure
    ionization), invalidating ideal dilute slots. High-density rows illustrate
    the ideal-model trend, without guaranteeing validity for a real sample.
    See @chen2016 @bittencourt2004.
  ])
  #summary[
    Saha plus nucleus conservation predicts $x(T,n)$. Electron-state freedom
    lowers the threshold by a logarithm, supporting a qualified $10^4$ K
    thermal rule; non-equilibrium ionization needs rate models.
  ]
  #knowledge-check((
    (
      question: [What densities follow from $x=1/4$ at nucleus density $n$?],
      answer: [$n_i=n_e=n/4$ and $n_n=3n/4$, each in #unit("m^-3").],
    ),
    (
      question: [What is $A$ at half ionization?],
      answer: [$A=1/2$, dimensionless, from $(1/2)^2/(1-1/2)$.],
    ),
    (
      question: [Why can half ionization occur with $k_B T << chi$?],
      answer: [Free-electron states compensate the Boltzmann penalty; binding energy is divided by a large logarithm.],
    ),
    (
      question: [Recombination photons escape a dilute plasma. Is a Maxwellian enough to justify Saha?],
      answer: [No. Chemical detailed balance is also necessary; escaping radiation can require rate balance even with thermal electrons.],
    ),
  ))

  #chapter-nav(
    previous: (href: "01-introduction.html", title: [Introduction]),
    next: (href: "03-debye-shielding.html", title: [Debye shielding]),
  )
]
