#import "../theme.typ": *
#import "@preview/physica:0.9.8": grad, div, curl, laplacian, pdv, dv, vb
#import "../figures.typ": debye-potential-comparison, debye-regime-map, debye-screened-point

#let chapter = [
  #page-title(number: 3)[Debye shielding] <debye-shielding>

  #lead[
    Mobile charges rearrange around a localized disturbance. The equilibrium
    electron response defines the Debye length and explains the reduction of
    the potential around a localized charge.
    A finite spherical source separates ordinary geometric spreading from
    screening by the surrounding plasma. The treatment follows
    @chen2016 @bittencourt2004.
  ]

  #section-title[Debye shielding] <intro-debye-shielding>

  #lead[
    A test charge disturbs the surrounding plasma. How far does its
    electrostatic influence extend once mobile electrons rearrange? In the
    weak-potential, equilibrium limit, the answer is the Debye length.
  ]

  #objectives((
    [state the equilibrium and ordering assumptions behind Debye shielding],
    [connect the Boltzmann response to the screened Poisson equation],
    [interpret the Debye length as a collective response scale],
  ))

  #unit-ledger[
    The screening length $lambda_D$ is in #unit("m").
  ]

  A first estimate of the size of a charge-separated region can be obtained
  before solving the shielding profile. Let $N$ denote a number density in a
  uniformly charged spherical region of radius $R$, with charge magnitude
  $e$ per particle. Gauss's law gives the boundary potential scale

  $ phi(R) = (N e R^2)/(3 epsilon_0),
    quad abs(e phi(R)) approx k_B T_e
    => R approx sqrt((3 epsilon_0 k_B T_e)/(N e^2)) $ <debye-charge-separation-scale>

  #equation-note[
    $N$ is a number density in #unit("m^-3"), $R$ is in #unit("m"),
    and $phi$ is in #unit("V"). The numerical factor depends on the assumed
    charge profile; the robust result is the scaling
    $R$ proportional to $sqrt(epsilon_0 k_B T_e\/(N e^2))$.
  ]

  #details(
    [Derivation: potential scale of a uniformly charge-separated sphere],
    [#derivation-step[Compute the enclosed charge and field]
    The enclosed charge at radius $r$ is

    $ Q(r)=(4 pi)/3 N e r^3 . $

    Applying Gauss's flux law to a sphere gives

    $ E(r) 4 pi r^2=Q(r)/epsilon_0 , $

    and hence

    $ E(r)=(N e r)/(3 epsilon_0) . $

    #derivation-step[Estimate the boundary potential]
    Measured relative to infinity, the potential at the boundary of the
    uniformly charged sphere is

    $ phi(R)=Q(R)/(4 pi epsilon_0 R)=(N e R^2)/(3 epsilon_0) . $

    A thermal particle can cross or substantially rearrange the region when
    $abs(e phi(R))$ is comparable to $k_B T_e$. Solving that balance gives the
    displayed estimate. If $N=n_0$, then

    $ R approx sqrt(3) lambda_D . $

    The order-one factor depends on the charge geometry.]
  )

  #assumption(
    [Linearized Boltzmann response],
    [Take a uniform, stationary ion background with $n_i = n_0$, mobile
    electrons at temperature $T_e$, no magnetic force in the equilibrium
    response, and a weak potential satisfying $abs(e phi) << k_B T_e$. The
    ions are treated as fixed on the electron response time.]
  )

  The electron equilibrium density follows from the electrostatic potential
  energy $-e phi$:

  $ n_e = n_0 exp((e phi) / (k_B T_e)) approx n_0 (1 + (e phi) / (k_B T_e)) $ <debye-boltzmann-response>

  #equation-note[
    $n_e$ and $n_0$ are in #unit("m^-3"), and $e phi$ and $k_B T_e$
    are energies in #unit("J"). The approximation is dimensionless and requires
    $abs(e phi)\/(k_B T_e) << 1$.
  ]

  The net charge density is therefore

  $ rho_q = e n_i - e n_e approx - (e^2 n_0)/(k_B T_e) phi $ <debye-charge-response>

  #equation-note[
    The sign expresses the restoring response of electrons to a
    positive potential perturbation.
  ]

  Poisson's equation is

  $ laplacian phi = -rho_q/epsilon_0 $ <debye-poisson>

  #equation-note[
    This equation defines the electrostatic field convention used
    here, with vacuum permittivity $epsilon_0$ in #unit("F/m").
  ]

  Substitution gives the screened equation

  $ laplacian phi - phi / lambda_D^2 = 0, quad lambda_D = sqrt((epsilon_0 k_B T_e) / (n_0 e^2)) $ <debye-screened-equation>

  #equation-note[
    $lambda_D$ is in #unit("m"). The equation is valid outside the
    localized source and within the linearized, static response model.
  ]

  #details(
    [Derivation: from particle response to shielding],
    [#derivation-step[Linearize the electron response]
    For a positive test potential, the electron potential energy is $-e phi$.
    The equilibrium Boltzmann factor is therefore

    $ exp((-(-e phi))/(k_B T_e))=exp((e phi)/(k_B T_e)) . $

    When $abs(e phi)\/(k_B T_e) << 1$, expand it to first order:

    $ n_e approx n_0 (1+(e phi)/(k_B T_e)) . $

    With immobile ions, the charge density becomes

    $ rho_q=e n_0-e n_e approx -(e^2 n_0 phi)/(k_B T_e) . $

    #derivation-step[Insert the response into Poisson's equation]
    Define the Debye coefficient by

    $ lambda_D^(-2)=(n_0 e^2)/(epsilon_0 k_B T_e) . $

    Inserting the charge response into the Poisson equation gives

    $ laplacian phi-phi/lambda_D^2=0 . $

    In spherical symmetry, the decaying source solution has the form

    $ phi(r) "proportional to" exp(-r/lambda_D)/r . $

    The exponential factor is the shielding; $1\/r$ is the unscreened geometric
    spreading of a point source.]
  )

  #debye-screened-point

  #summary[
    Debye shielding is a linear equilibrium response: the Boltzmann electron
    density modifies Poisson's equation and introduces the length $lambda_D$.
    The derivation depends on weak potential, mobile electrons, and a stationary
    ion background.
  ]

  #exam-prompts(
    (
      [(d) A spherical region of complete charge separation has a potential $Phi(r) = (N q_e / epsilon_0) r^2$ at its boundary. What size can such a region roughly have in a thermal plasma of temperature $T$ (potential energy = thermal energy)?],
      [(e) Describe and give an overview of the derivation for Debye shielding.],
    ),
    [Plasma Physics Exam.pdf, p. 1],
  )

  #knowledge-check((
    (
      question: [Why does a positive electrostatic potential increase the equilibrium electron density in the Boltzmann response?],
      answer: [An electron has charge $-e$, so its potential energy is $-e phi$. A positive $phi$ lowers that energy and produces the factor $exp(e phi\/(k_B T_e))$.],
    ),
    (
      question: [Which approximation turns the exponential Boltzmann response into a linear screening equation?],
      answer: [The weak-potential ordering $abs(e phi) << k_B T_e$ permits a first-order expansion of the exponential.],
    ),
    (
      question: [What happens to the screened potential at distances much larger than $lambda_D$ in this model?],
      answer: [The exponential factor suppresses it, so the localized electrostatic influence is small compared with the unscreened $1\/r$ field.],
    ),
    (
      question: [Give one situation in which the linear Debye-shielding derivation should not be used without modification.],
      answer: [A potential comparable to or larger than $k_B T_e\/e$, a time-dependent kinetic response, or a boundary within the shielding region violates the stated assumptions.],
    ),
  ))

  #section-title[Finite charge distribution] <debye-finite-source>

  #objectives((
    [derive the bare potential of a uniformly charged sphere from Gauss's law],
    [match the screened interior and exterior solutions at the source boundary],
    [separate the source-size effect from the exponential screening factor],
  ))

  #definition(
    [Finite spherical test charge],
    [To separate the size of the source from the plasma response, let the test
    charge be a uniformly charged three-dimensional sphere of radius $R$ and
    total charge $Q$. Its volume charge density is

    $ rho_Q = (3 Q)/(4 pi R^3) . $

    The animation shows a two-dimensional cross-section of this sphere. The
    randomly scattered source markers represent the continuous charge density.
    The fixed source charge is permeable to the plasma: electrons occupy both
    its interior and exterior.]
  )

  For this finite source, the exact bare potential is

  $ phi_"C" (r) = Q/(8 pi epsilon_0 R) (3 - r^2/R^2), quad 0 <= r <= R $ <debye-sphere-potential-inside>

  and

  $ phi_"C" (r) = Q/(4 pi epsilon_0 r), quad r >= R $ <debye-sphere-potential-outside>

  #equation-note[
    $Q$ is in #unit("C"), $r$ and $R$ are in #unit("m"), and $phi_"C"$
    is in #unit("V") when the reference potential is zero at infinity. The
    interior expression is quadratic in $r$ and joins the exterior Coulomb
    expression continuously at $r=R$: both give $Q\/(4 pi epsilon_0 R)$ there.
  ]

  The quadratic interior is the potential of the extended source itself. It
  removes the point-charge singularity at the center. Outside the sphere,
  spherical symmetry reduces the source to its total charge and restores the
  $1\/r$ Coulomb decay.

  The plasma response is a separate effect. In the linearized, static model,
  the same source satisfies the spherical Debye--Hückel equations

  $ laplacian phi_"D" - phi_"D"/lambda_D^2 = -rho_Q/epsilon_0, quad r < R $

  $ laplacian phi_"D" - phi_"D"/lambda_D^2 = 0, quad r > R . $

  #equation-note[
    $rho_Q$ is the source charge density, while the mobile
    electron response has already been absorbed into the term
    $-phi_"D"\/lambda_D^2$. The fields and potentials are matched at the source
    boundary, and the exterior solution decays at infinity. Linearization
    requires $abs(e phi_"D")\/(k_B T_e) << 1$ everywhere. A sufficient
    condition for a positive source is

    $ (3 e Q)/(8 pi epsilon_0 R k_B T_e) << 1 , $

    using the maximum bare potential. Normalizing the plotted potential by
    $Q\/(4 pi epsilon_0 lambda_D)$ does not by itself impose this small-source condition.
  ]

  #details(
    [Derivation: bare potential of a uniform sphere],
    [#derivation-step[Enclose the source]
    For $r<R$, the charge enclosed by a concentric spherical surface is

    $ Q_"enc" (r) = rho_Q (4 pi r^3)/3 = Q r^3/R^3 . $

    Gauss's law then gives

    $ E_"C" (r) 4 pi r^2 = Q_"enc" (r)/epsilon_0
      => E_"C" (r) = (Q r)/(4 pi epsilon_0 R^3), quad r<R . $

    For $r>R$, the enclosed charge is $Q$, so

    $ E_"C" (r) = Q/(4 pi epsilon_0 r^2), quad r>R . $

    #derivation-step[Integrate the field with the boundary condition]
    Set $phi_"C" (infinity)=0$ and integrate inward from the exterior. This
    gives $phi_"C" (r)=Q\/(4 pi epsilon_0 r)$ outside the source and

    $ phi_"C" (r) = phi_"C" (R) + integral_r^R E_"C" (r') dif r'
      = Q/(4 pi epsilon_0 R) + integral_r^R (Q r')/(4 pi epsilon_0 R^3) dif r'
      = Q/(8 pi epsilon_0 R) (3-r^2/R^2) $

    inside. At $r=R$, the potential and the radial field agree on both sides,
    so the piecewise solution is continuous and has no artificial surface
    charge.]
  )

  #details(
    [Derivation: matched finite-source Debye response],
    [#derivation-step[Choose regular and decaying radial solutions]
    Write $kappa=1\/lambda_D$ and $x=kappa R$. In the source region, a constant
    particular solution and the regular homogeneous solution give

    $ phi_(D,"in")(r) = phi_"p" + A (sinh(kappa r))/r,
      quad phi_"p" = rho_Q/(epsilon_0 kappa^2) = (3 Q)/(4 pi epsilon_0 kappa^2 R^3) . $

    Outside the source, decay at infinity selects

    $ phi_(D,"out")(r) = B e^(-kappa r)/r . $

    #derivation-step[Match the source boundary]
    Continuity of potential and radial derivative at $r=R$ gives

    $ phi_(D,"in")(R) = phi_(D,"out")(R) $

    and

    $ dv(phi_(D,"in"), r) |_(r=R) = dv(phi_(D,"out"), r) |_(r=R) . $

    Solving these two equations gives

    $ A = -(R phi_"p" (x+1) e^(-x))/x $

    and

    $ B = (R phi_"p")/(2 x) (e^x (x-1) + (x+1) e^(-x)) . $

    Therefore the exterior response contains both the geometrical Coulomb
    factor $1\/r$ and the shielding factor $e^(-r\/lambda_D)$. For a finite
    source, the coefficient $B$ records the source-size correction.]
  )

  #interpretation(
    [Reduction of the exterior potential],
    [For a point source, the ratio of the Debye-screened to bare potential is
    $phi_"D"\/phi_"C" = e^(-r\/lambda_D)$. A finite sphere changes the amplitude
    near $r=R$, but the exterior screening still supplies the exponential
    suppression. At distances several Debye lengths from the source, the
    Coulomb tail is therefore reduced exponentially.]
  )

  #debye-potential-comparison

  #animation(
    "../media/debye-potential-reduction.mp4",
    "A cross-section of a permeable, uniformly charged three-dimensional sphere uses plus signs for the fixed positive source and dots for mobile electrons, present inside and outside the sphere. Electron markers move inward during an illustrative transition. A radial plot compares the dashed bare potential, quadratic inside R and Coulomb-like outside, with the solid screened equilibrium potential and its exponentially reduced exterior tail. Radius and potential are normalized by the Debye length and by Q divided by 4 pi epsilon_0 times the Debye length, with unit [1]. Intermediate curves and marker motion are explanatory interpolation, not a computed transient.",
    caption: [
      A finite spherical source and its potential. The source is shown as a
      two-dimensional cross-section of a uniformly charged three-dimensional
      permeable sphere. Electrons are present inside and outside the source.
      As representative markers move inward, the solid screened curve
      falls below the dashed bare curve outside $R$: the Coulomb $1\/r$ tail
      acquires the Debye suppression factor. Marker motion and intermediate
      curves interpolate between states for explanation; they do not solve
      a time-dependent shielding problem.
    ],
    poster: "../media/debye-potential-reduction.png",
  )

  The static reading is sufficient to identify both mechanisms. The orange
  source markers stay inside the sphere, where the bare potential is finite
  and quadratic. Mobile electrons occupy the interior as well as the
  surrounding region, while the
  analytic curve changes from the bare spherical potential to the matched
  Debye--Hückel solution. The screened curve is lower outside the source but
  remains continuous at its boundary. Its interior is regular but is not
  exactly quadratic once the plasma response is included.

  #animation(
    "../media/debye-shielding.mp4",
    "Circular electron markers move toward a positive test charge while triangular ion markers remain fixed. Separate one-dimensional profiles show an electron-density excess and a reduced potential. Positions are normalized by the Debye length and time by the relaxation time, with unit [1]. The prescribed two-dimensional marker motion does not generate the one-dimensional fields.",
    caption: [
      Two views of shielding: prescribed electron markers move toward a
      positive source in the left panel. The right panel shows a separate
      normalized one-dimensional slab calculation, in which an electron
      excess reduces the potential. Ions remain fixed; the slab calculation
      uses a periodic box with compensating background charge.
    ],
    poster: "../media/debye-shielding.png",
  )

  The two panels illustrate related but distinct models. On the left,
  prescribed two-dimensional marker trajectories show inward rearrangement;
  those markers do not generate the plotted field. On the right, density
  and potential come from one coupled one-dimensional drift--diffusion and
  Poisson calculation in a periodic box with compensating background charge.
  That computed electron excess reduces the source field. The independently
  drawn marker cloud must not be read as a self-consistent two-dimensional
  simulation of the right-hand profiles.

  The next animation removes the prescription: the electrons move under their
  own Coulomb forces. The test charge $Q = -4 pi kappa n_0 lambda_D^3 e$ has
  the electrons' sign, so the linearized Boltzmann response and the screened
  potential derived above predict an electron deficit
  $-delta n_e\/(kappa n_0) = (lambda_D\/r) e^(-r\/lambda_D)$, valid where
  $r >> kappa lambda_D$. Here $delta n_e = n_e - n_0$ and $kappa = 0.05$ is
  dimensionless. Time is measured in units of $1\/omega_(p,e)$, with the
  electron plasma frequency $omega_(p,e) = sqrt(n_0 e^2\/(epsilon_0 m_e))$
  of Chapter 4 and the electron mass $m_e$.

  #animation(
    "../media/debye-shielding-particles.mp4",
    "Left: blue electron markers in a thin slab around a fixed negative test charge, drawn as a white disc, over a uniform positive background in a periodic cube. The markers move thermally; no hole around the test charge is visible in any single frame. Right: the measured electron deficit in spherical shells around the charge, averaged over time and over eight independent runs, plotted as dots against distance. The dots start noisy and settle onto a solid Debye curve, well below a dashed unscreened 1/r curve; at the end, vertical bars show 95 percent intervals over the runs. Positions are normalized by the Debye length, time by the inverse plasma frequency, and the deficit by kappa n0, with unit [1].",
    caption: [
      Debye shielding from particle dynamics, computed with kin6d. A classical
      electron one-component plasma (mobile electrons, uniform neutralizing
      background in place of immobile ions) fills a periodic cube of edge
      $4 lambda_D$ with $n_0 lambda_D^3 = 100$, that is $N_D approx 420$ and
      6400 electrons, interacting by the unsoftened Coulomb force. A fixed
      test charge of the electrons' sign sits at the centre. Left: one run,
      electrons in the slab $abs(z) < lambda_D\/2$ around the charge; a
      single snapshot shows no visible hole, because beyond
      $r approx lambda_D\/2$ the deficit is only a few percent of $n_0$,
      smaller than the counting fluctuations. Right:
      the deficit $-delta n_e\/(kappa n_0)$ averaged over time up to
      $omega_(p,e) t = 40$ and over eight independent runs. It follows the
      linear Debye reference for the periodic cube (solid) and lies far below
      the unscreened response $1\/r$ (dashed). Positions are $x\/lambda_D$,
      $y\/lambda_D$, $r\/lambda_D$ and time $omega_(p,e) t$, all with unit
      [1]. The bars are statistical 95~% intervals, not exact error bounds.
    ],
    poster: "../media/debye-shielding-particles.png",
  )

  The screening cloud of the derivation is therefore an average, not a
  picture of individual electrons. The Boltzmann density describes the mean
  occupation of a shell around
  the charge, and with hundreds of electrons per Debye sphere this mean
  emerges only after averaging over many configurations. The same
  requirement, $N_D >> 1$, returns as the plasma parameter below.

  #interpretation(
    [Scope of the Debye length],
    [The Debye length is the distance over which this
    particular equilibrium response reduces a localized electrostatic field.
    Strong potentials, rapid time dependence, boundaries, insufficient Debye
    number, and kinetic non-equilibrium require a more complete model.]
  )

  #summary[
    A uniformly charged sphere of radius $R$ and charge $Q$ has a bare
    potential that is quadratic in the radius $r$ inside the source and equal
    to the Coulomb potential $Q\/(4 pi epsilon_0 r)$ outside it. In the
    linearized Debye--Hückel model, the screened potential $phi_"D"$ is
    regular inside the source and equals

    $ B e^(-r/lambda_D)/r $

    outside, where
    continuity of potential and radial field at $r=R$ fixes the coefficient
    $B$. The source size sets the amplitude near $r=R$, and the electron
    response supplies the exterior factor $e^(-r\/lambda_D)$. Linearization
    holds everywhere when

    $ (3 e Q)/(8 pi epsilon_0 R k_B T_e) << 1 . $
  ]

  #knowledge-check((
    (
      question: [Use Gauss's law to find the bare field inside the uniform sphere. How large is the bare potential at the center compared with its value at the surface $r=R$?],
      answer: [The enclosed charge is $Q r^3\/R^3$, so $E_"C" = Q r\/(4 pi epsilon_0 R^3)$ grows linearly with $r$. Integrating this field from $r$ to $R$ and adding the surface value $Q\/(4 pi epsilon_0 R)$ gives $phi_"C" (0) = 3 Q\/(8 pi epsilon_0 R)$, which is $3\/2$ of the surface value and finite.],
    ),
    (
      question: [A positive source keeps its charge $Q$ while its radius $R$ is halved. How does the sufficient condition for linearization change?],
      answer: [The parameter

      $ (3 e Q)/(8 pi epsilon_0 R k_B T_e) $

      is the bare potential energy $e phi_"C" (0)$ at the center divided by the electron thermal energy $k_B T_e$, and it scales as $1\/R$. Halving $R$ doubles it, so the same margin of validity requires half the charge or twice the electron temperature.],
    ),
    (
      question: [What does the exterior coefficient $B$ become when $R -> 0$ at fixed $Q$, and which earlier result does the exterior potential then reproduce?],
      answer: [$B -> Q\/(4 pi epsilon_0)$, so the exterior potential becomes

      $ Q e^(-r/lambda_D)/(4 pi epsilon_0 r) , $

      the screened point charge of the previous section. The finite-source correction is contained entirely in $B$.],
    ),
    (
      question: [With $kappa = 1\/lambda_D$, explain why the interior solution uses $sinh(kappa r)\/r$, the exterior solution uses $e^(-kappa r)\/r$, and two conditions at $r=R$ suffice to fix them.],
      answer: [The interior solution must stay finite at $r=0$, and $sinh(kappa r)\/r -> kappa$ there, while $e^(-kappa r)\/r$ diverges. The exterior solution must decay at infinity, which excludes the growing $e^(kappa r)\/r$. Each region then carries one free amplitude, $A$ and $B$, and continuity of $phi_"D"$ and of $dv(phi_"D", r, style: "horizontal")$ at $r=R$ gives two equations for them.],
    ),
  ))

  #section-title[Plasma parameter] <debye-collective-validity>

  #objectives((
    [compute the Debye number from the electron density and the Debye length],
    [relate the coupling parameter $Gamma_s$ to the Debye number],
    [decide from $N_D$, $Gamma_s$ and $lambda_D\/L$ whether a collective, quasineutral description applies],
  ))

  The Debye number counts electrons within a sphere of radius $lambda_D$.
  A smooth collective description requires this number to be large:

  $ N_D = (4 pi)/(3) n_e lambda_D^3 >> 1 $ <intro-debye-number>

  #equation-note[
    Dimensionless. $N_D$ counts electrons inside a Debye sphere. The symbol
    $>> 1$ states an ordering assumption.
  ]

  #definition(
    [Ideal-plasma convention used here],
    [For the purposes of this script, an ideal plasma is weakly coupled and
    sufficiently populated that collective fields can be treated smoothly.
    A useful weak-coupling parameter is

    $ Gamma_s = (q_s^2) / (4 pi epsilon_0 a_s k_B T_s) , $

    where $a_s = (3\/(4 pi n_s))^(1\/3)$ is the mean-spacing scale. The
    classical collective ordering also requires many particles in a Debye
    sphere and, when quasineutral fluid behavior is invoked, a system scale
    $L$ much larger than $lambda_D$.]
  )

  #equation-note[
    $a_s$ is in #unit("m"), $q_s^2\/(4 pi epsilon_0 a_s k_B T_s)$ is
    dimensionless, and the weak-coupling condition is $Gamma_s << 1$.
  ]

  Compare the screening length with the system or gradient length $L$ in
  #unit("m"). The dimensionless ratio $lambda_D\/L << 1$ supports bulk
  quasineutrality away from boundaries; it does not establish a collisional
  fluid closure. Collision scales are treated in
  #chapter-link("kinetic-collisions")[Collisions in gases and plasmas].

  #debye-regime-map

  #summary[
    The Debye number $N_D = (4 pi\/3) n_e lambda_D^3$ counts the electrons in a
    sphere of radius $lambda_D$, and a smooth collective field requires
    $N_D >> 1$. The coupling parameter $Gamma_s$ compares the Coulomb energy of
    two particles of species $s$ at the mean spacing $a_s$ with their thermal
    energy $k_B T_s$, and an ideal plasma has $Gamma_s << 1$. For electrons,
    $Gamma_e N_D^(2\/3) = 1\/3$, independent of $n_e$ and $T_e$, so weak coupling and
    a large Debye number are one condition. Bulk quasineutrality additionally
    requires $lambda_D\/L << 1$ for the system or gradient length $L$.
  ]

  #knowledge-check((
    (
      question: [How does $N_D$ scale with the electron density $n_e$ at fixed $T_e$, and with $T_e$ at fixed $n_e$? Which corner of the density--temperature plane violates $N_D >> 1$?],
      answer: [Since $lambda_D$ is proportional to $sqrt(T_e\/n_e)$, $N_D$ is proportional to $n_e lambda_D^3$ and hence to $T_e^(3\/2) n_e^(-1\/2)$. Dense, cold plasmas reach $N_D approx 1$, the shaded high-density, low-temperature region of the regime map.],
    ),
    (
      question: [Show that $Gamma_e N_D^(2\/3)$ contains neither $n_e$ nor $T_e$, using $a_e = (3\/(4 pi n_e))^(1\/3)$ and $lambda_D^2 = epsilon_0 k_B T_e\/(n_e e^2)$.],
      answer: [

      $ Gamma_e = e^2/(4 pi epsilon_0 k_B T_e) ((4 pi n_e)/3)^(1/3)
        quad "and" quad
        N_D^(2/3) = ((4 pi n_e)/3)^(2/3) (epsilon_0 k_B T_e)/(n_e e^2) . $

      In the product, $e^2$, $epsilon_0$ and $k_B T_e$ cancel, and the density factors combine to $n_e\/n_e$, leaving a pure number. A large $N_D$ therefore implies $Gamma_e << 1$, and conversely.],
    ),
    (
      question: [A plasma has $N_D >> 1$ and $Gamma_e << 1$, but its size $L$ is comparable to $lambda_D$. Which condition fails, and which modeling assumption must be dropped?],
      answer: [The ordering $lambda_D\/L << 1$ fails. Screening layers then span the whole system, and bulk quasineutrality cannot be assumed. The collective field remains smooth because $N_D >> 1$ still holds.],
    ),
    (
      question: [The line $lambda_D = L$ in the density--temperature plane is $k_B T_e = e^2 n_e L^2\/epsilon_0$. On which side is the bulk quasineutral, and how does the line move when $L$ doubles?],
      answer: [Quasineutral bulk requires $lambda_D < L$, which is $k_B T_e < e^2 n_e L^2\/epsilon_0$, the side of higher density at given temperature. Doubling $L$ multiplies the temperature on the line by four at each density, so the quasineutral region grows.],
    ),
  ))

  #chapter-nav(
    previous: (href: "02-thermal-equilibrium.html", title: [Temperature, entropy, and thermal ionization]),
    next: (href: "04-plasma-oscillations.html", title: [Plasma oscillations]),
  )
]
