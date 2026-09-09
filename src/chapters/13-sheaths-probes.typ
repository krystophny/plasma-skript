#import "../theme.typ": *
#import "../figures.typ": sheath-structure, sheath-profile, probe-iv-characteristic
#import "@preview/physica:0.9.8": div, grad, pdv, dv
#import "@preview/unify:0.8.1": qty, unit

#let chapter = [
  #page-title[13. Plasma sheaths and Langmuir probes] <plasma-sheaths>

  #lead[
    A material boundary is not a passive edge of a plasma. Electrons and ions
    arrive at a surface with different thermal speeds, so the surface charges
    until an electric field filters the particle fluxes. This chapter derives
    the planar collisionless sheath model, obtains the Bohm entry condition
    and floating potential, and turns the same flux picture into a
    Langmuir-probe diagnostic.
  ]

  #callout(
    [A sheath is a self-consistent boundary condition],
    [The plasma does not simply stop at a wall. The surface potential, the
    directed ion flow, the electron distribution, and Poisson's equation must
    agree. A probe measures the resulting current--voltage response, not a
    local density or temperature in isolation.]
  )

  #section-title[Particle flux and the need for a sheath] <sheath-flux>

  #lead[
    What reaches a surface when the nearby distribution is isotropic? The
    answer is a one-sided velocity moment. Because the electron thermal speed
    is much larger than the ion thermal speed, an initially uncharged wall
    receives a much larger electron current. The resulting negative charging
    creates the barrier that defines a sheath.
  ]

  #objectives((
    [define directed particle flux as a half-space velocity moment],
    [derive the isotropic Maxwellian flux to a planar surface],
    [compare electron and ion flux scales without confusing flux and density],
    [explain why a wall potential must form before steady current balance],
  ))

  #unit-ledger[
    Gaussian CGS is active. Number density $n_s$ is in #unit("cm^-3"),
    velocity is in #unit("cm/s"), mass is in #unit("g"), and the directed
    particle flux $Gamma_s$ is in #unit("cm^-2 s^-1"). Charge is in
    statcoulomb, so a current density $J_s=q_s Gamma_s$ is in
    statcoulomb per #unit("cm^2") per #unit("s"). Thermal energy $k_B T_s$
    and potential energy $q_s phi$ are in #unit("erg"). Ratios such as
    $Gamma_e/Gamma_i$ and $(e phi)/(k_B T_e)$ are dimensionless.
  ]

  #assumption(
    [Isotropic distribution next to a planar surface],
    [Take a locally planar boundary with outward normal $bold(e)_n$ and a
    distribution that is isotropic on the plasma side. The surface is
    collisionless over the collection distance, absorbs particles that reach
    it, and has no secondary emission in the first flux estimate. This
    estimate is a boundary flux, not a claim that the distribution remains
    isotropic inside the sheath.]
  )

  #definition(
    [Directed particle flux],
    [The number of particles of species $s$ crossing a unit area toward the
    surface is
    $Gamma_s = integral_(v_n>0) v_n f_(s)(bold(v)) dif^3 bold(v)$,
    where $v_n=bold(v) dot bold(e)_n$. For an isotropic distribution, the
    tangential velocity integrals can be performed first, leaving the
    positive half of the normal-velocity distribution.]
  )

  #governing-law(
    [Maxwellian half-space flux],
    [For a three-dimensional Maxwellian with density $n_s$ and temperature
    $T_s$, the unretarded flux toward a plane is
    $Gamma_(s,0)=n_s sqrt((k_B T_s)/(2 pi m_s))
      =(n_s v_"th,s")/(2 sqrt(pi))
      =(n_s v_"mean,s")/4$,
    where $v_"th,s"=sqrt((2 k_B T_s)/m_s)$ and
    $v_"mean,s"=sqrt((8 k_B T_s)/(pi m_s))$. Equal temperatures therefore
    give $Gamma_(e,0)/Gamma_(i,0)=sqrt(m_i/m_e)$, even though the
    equilibrium densities can be equal.]
  )

  #details(
    [Derivation: the one-sided Maxwellian flux],
    [Choose the surface normal as the $z$ direction. The isotropic
    Maxwellian is
    $f_(s)(bold(v))=
      n_s (m_s/(2 pi k_B T_s))^(3/2)
      exp(-(m_s (v_x^2+v_y^2+v_z^2))/(2 k_B T_s))$.
    Insert it into the half-space definition:
    $Gamma_(s,0)=
      integral_0^infinity integral_(-infinity)^infinity
      integral_(-infinity)^infinity
      v_z f_(s)(bold(v)) dif v_x dif v_y dif v_z$.

    The two tangential Gaussian integrals each give
    $integral_(-infinity)^infinity
      exp(-(m_s v_x^2)/(2 k_B T_s)) dif v_x
      =sqrt((2 pi k_B T_s)/m_s)$.
    After both are evaluated, the remaining factor is
    $Gamma_(s,0)=
      n_s sqrt(m_s/(2 pi k_B T_s))
      integral_0^infinity v_z
      exp(-(m_s v_z^2)/(2 k_B T_s)) dif v_z$.

    Use $integral_0^infinity v exp(-a v^2) dif v=1/(2a)$ with
    $a=m_s/(2 k_B T_s)$. The normal integral is $(k_B T_s)/m_s$, so
    $Gamma_(s,0)=n_s sqrt((k_B T_s)/(2 pi m_s))$.
    Substituting $v_"th,s"=sqrt((2 k_B T_s)/m_s)$ gives the second form.
    The mean speed of the same three-dimensional Maxwellian is
    $v_"mean,s"=sqrt((8 k_B T_s)/(pi m_s))$, which gives
    $Gamma_(s,0)=(n_s v_"mean,s")/4$.]
  )

  #sheath-structure

  #rechenbeispiel[
    Consider a hydrogen plasma with equal electron and ion temperatures and
    $n_e=n_i$. Let $m_i/m_e=1836$. Determine the ratio of the unretarded
    electron and ion fluxes to the same planar surface.

    Numerical result: $Gamma_(e,0)/Gamma_(i,0)=sqrt(1836) approx 42.8$.
  ]

  #interpretation(
    [Flux imbalance charges the boundary],
    [At equal density and temperature, electrons arrive faster by the square
    root of the ion-to-electron mass ratio. The first electron loss leaves a
    negative wall charge. Its potential repels further electrons and attracts
    ions until the net current is compatible with the electrical boundary
    condition. The density equality in the plasma therefore does not imply
    equal wall fluxes.]
  )

  #summary[
    A surface samples a half-space moment, not the total thermal density.
    An isotropic Maxwellian supplies
    $Gamma_(s,0)=n_s sqrt((k_B T_s)/(2 pi m_s))$.
    The much larger electron flux charges an initially neutral wall
    negatively, creating the electrostatic sheath required for steady
    current balance.
  ]

  #knowledge-check((
    (
      question: [Why is the flux to a plane not $n_s v_"mean,s"$?],
      answer: [Only the velocity component normal to the plane contributes, and only particles with positive normal velocity cross the surface. The angular average and half-space restriction together give $Gamma_(s,0)=(n_s v_"mean,s")/4$.]
    ),
    (
      question: [Why can equal electron and ion densities still produce unequal wall currents?],
      answer: [The flux contains the thermal speed, which scales as $m_s^(-1/2)$ at equal temperature. Electrons therefore arrive much more rapidly than ions even when the volume densities are equal.]
    ),
    (
      question: [What physical process starts the formation of a floating sheath?],
      answer: [The initial electron flux is larger, so the wall loses negative charge and its potential becomes negative relative to the plasma. This potential filters electrons and accelerates ions.]
    ),
    (
      question: [Which assumption makes the half-space flux formula a local estimate rather than a sheath solution?],
      answer: [The distribution is taken to be isotropic on the plasma side of the boundary. Inside a sheath the electric field makes the distribution anisotropic, so the collected flux must be obtained from the orbit and boundary conditions.]
    ),
  ))

  #section-title[Sheath structure and the Bohm criterion] <bohm-criterion>

  #lead[
    The flux argument says that a boundary layer must form, but not how its
    potential varies in space. A one-dimensional model makes the coupling
    explicit: Boltzmann electrons respond to the potential, cold ions
    accelerate through it, and Poisson's equation determines the curvature.
    The requirement that a monotone sheath can attach to a quasineutral
    plasma is the Bohm criterion.
  ]

  #objectives((
    [set a consistent wall-to-plasma coordinate and potential reference],
    [combine Boltzmann electrons with cold-ion continuity and energy],
    [nondimensionalize Poisson's equation with the electron Debye length],
    [derive the sonic lower bound on ion speed at the sheath edge],
  ))

  #unit-ledger[
    The coordinate $x$ and Debye length $lambda_D$ are in #unit("cm"),
    potential $phi$ is in #unit("statvolt"), electric field is in statvolt
    per #unit("cm"), and densities are in #unit("cm^-3"). Ion speed and the
    cold-ion sound speed are in #unit("cm/s"). The normalized coordinate
    $xi=x/lambda_D$, potential barrier $eta=-(e phi)/(k_B T_e)$, and Mach
    number $M=u_s/c_s$ are dimensionless. In Gaussian CGS,
    $lambda_D^2=(k_B T_e)/(4 pi n_0 e^2)$.
  ]

  #assumption(
    [Steady planar collisionless sheath],
    [Let the wall be at $x=0$ and the plasma occupy $x>0$, with
    $phi(infinity)=0$ and a negative wall potential. Use cold ions with
    charge $+e$, Boltzmann electrons with temperature $T_e$, no magnetic
    field, no collisions inside the sheath, and a steady ion flux. The
    sheath edge is an asymptotic matching region, not an infinitely sharp
    physical discontinuity.]
  )

  #definition(
    [Normalized sheath variables],
    [Define the positive electron barrier and distance from the wall by
    $eta(x)=-(e phi(x))/(k_B T_e) >= 0$ and
    $xi=x/lambda_D$. The electron density is
    $n_e/n_0=exp(-eta)$. Let $u_s$ and $n_s$ be the ion speed and density
    at the sheath edge, define
    $c_s=sqrt((k_B T_e)/m_i)$ and $M=u_s/c_s$, and take $eta=0$ at the
    matching edge.]
  )

  #governing-law(
    [Planar sheath equation],
    [Ion continuity and energy give
    $n_i/n_s=M/(M^2+2 eta)^(1/2)$.
    Gaussian-CGS Poisson's equation, written with
    $bold(E)=-grad_(bold(r))(phi)$ and
    $div_(bold(r))(bold(E))=4 pi e(n_i-n_e)$, becomes
    $dv(eta,xi,2) =
      M/(M^2+2 eta)^(1/2)-exp(-eta)$.
    Expanding at the quasineutral edge gives
    $dv(eta,xi,2) approx (1-M^(-2)) eta$.
    A monotone solution that leaves the edge therefore requires
    $M >= 1$, or
    $u_s >= c_s=sqrt((k_B T_e)/m_i)$.
    This is the cold-ion Bohm criterion.]
  )

  #details(
    [Derivation: Boltzmann response, ion flow, and the sheath edge],
    [For a species in a static electrostatic potential, the stationary
    Maxwell--Boltzmann response is
    $n_(s)(phi)=n_(s,infinity)
      exp(-(q_s phi)/(k_B T_s))$.
    For electrons $q_e=-e$ and the plasma reference is $phi(infinity)=0$,
    so $n_e=n_0 exp((e phi)/(k_B T_e))=n_0 exp(-eta)$.

    For cold steady ions, the continuity equation is
    $dv(n_i u_i,x)=0$.
    Thus $n_i u_i=n_s u_s=Gamma_i$. The ion momentum equation is
    $m_i u_i dv(u_i,x)=-e dv(phi,x)$.
    Multiply by $u_i$ and use
    $(u_i dv(u_i^2,x))/2=u_i^2 dv(u_i,x)$:
    $dv((m_i u_i^2)/2+e phi,x)=0$.
    At the edge, where $eta=0$, this gives
    $(m_i u_i^2)/2+e phi=(m_i u_s^2)/2$.
    Since $e phi=-k_B T_e eta$,
    $u_i^2=u_s^2+(2 k_B T_e eta)/m_i
      =c_(s)^(2) (M^2+2 eta)$.
    Continuity then gives
    $n_i/n_s=u_s/u_i=M/(M^2+2 eta)^(1/2)$.

    Poisson's equation in Gaussian CGS is
    $div_(bold(r))(bold(E))=4 pi rho_q
      =4 pi e(n_i-n_e)$.
    In one dimension, $E_x=-dv(phi,x)$, so
    $-dv(phi,x,2)=4 pi e(n_i-n_e)$.
    With $phi=-((k_B T_e)/e) eta$ and
    $x=lambda_D xi$, the left side is
    $((k_B T_e)/(e lambda_D^2)) dv(eta,xi,2)$.
    Use $lambda_D^2=(k_B T_e)/(4 pi n_0 e^2)$ and set $n_s=n_0$
    at the ideal matching edge. The result is
    $dv(eta,xi,2)=n_i/n_0-n_e/n_0
      =M/(M^2+2 eta)^(1/2)-exp(-eta)$.

    Expand both terms for small eta:
    $M/(M^2+2 eta)^(1/2)
      =(1+(2 eta)/(M^2))^(-1/2)
      approx 1-eta/M^2$,
    while $exp(-eta) approx 1-eta$. Their difference is
    $(1-M^(-2))eta$. If $M<1$, the coefficient is negative and the
    edge curvature has the wrong sign for a monotone positive barrier
    attached to the plasma. Therefore $M>=1$. Equality is the sonic
    threshold; additional ion temperature or kinetic effects modify the
    sound speed and the generalized criterion.]
  )

  #details(
    [Derivation: electron-free planar edge and Child--Langmuir scaling],
    [Near a sufficiently negative wall, take the electron density to be
    negligible and write $V=-phi>0$ for the potential drop measured from
    the plasma reference. Let $x$ increase from the wall toward the
    sheath edge, and let the electron-free layer have thickness $d$.
    Ion energy in the large-drop limit gives
    $u_i approx sqrt((2 e V)/m_i)$.
    With constant ion flux $Gamma_i=n_i u_i$, the ion density is
    $n_i=Gamma_i sqrt(m_i/(2 e V))$.

    Poisson's equation for $phi=-V$ is
    $dv(V,x,2)
      =4 pi e n_i
      =C V^(-1/2)$,
    where $C=4 pi Gamma_i sqrt((e m_i)/2)$.
    Introduce the distance $s=d-x$ measured inward from the
    electron-free edge toward the wall. Then $dv(V,s,2)=C V^(-1/2)$.
    Multiply by $dv(V,s)$ and integrate:
    $((dv(V,s))^2)/2=2 C V^(1/2)+C_1$.
    At the edge $s=0$, $V=0$, and the idealized matching condition gives
    $dv(V,s)=0$, so $C_1=0$. Take the positive branch and separate
    variables:
    $V^(-1/4) dv(V,s)=2 sqrt(C) dif s$.
    Integration from the edge gives
    $4/3 V^(3/4)=2 sqrt(C) s$,
    hence
    $V(s)=((9 C)/4)^(2/3) s^(4/3)$.
    At the wall, $s=d$ and $V=V_w$, so
    $V_w^(3/2)=((9 C)/4)d^2$.
    Solving for the ion flux and multiplying by $e$ gives the
    planar Child--Langmuir scaling in Gaussian CGS:
    $J_i=e Gamma_i
      =(sqrt((2 e)/m_i) V_w^(3/2))/(9 pi d^2)$.
    This is a near-wall space-charge result. It does not replace the
    Boltzmann-electron sheath equation across the whole boundary layer.]
  )

  #sheath-profile

  #rechenbeispiel[
    For a hydrogen plasma use
    $n_0=qty("1.0e10", "cm^-3")$,
    $k_B T_e=qty("1.602e-11", "erg")$,
    $m_i=qty("1.673e-24", "g")$, and
    $e=qty("4.803e-10", "statcoulomb")$. Let the normalized sheath-edge
    speed be $M=1.50$ (dimensionless). Determine the electron Debye length,
    cold-ion sound speed, sheath-edge ion speed, and ion particle flux
    $Gamma_i=n_0 M c_s$.

    Numerical result: $lambda_D approx qty("2.35e-2", "cm")$,
    $c_s approx qty("3.09e6", "cm/s")$,
    $u_s approx qty("4.64e6", "cm/s")$, and
    $Gamma_i approx qty("4.64e16", "cm^-2 s^-1")$. The chosen
    $M=1.50>1$ is above the cold-ion Bohm threshold.
  ]

  #interpretation(
    [The Bohm condition is an attachment condition],
    [The criterion does not say that every ion in the plasma moves at exactly
    the sound speed. It says that the directed ion flow arriving at the
    sheath edge must be at least sonic in the cold-ion model. The presheath
    supplies this flow; the Debye-scale sheath then supplies the remaining
    potential drop and particle filtering.]
  )

  #summary[
    Boltzmann electrons, cold-ion continuity, ion energy, and cgs Poisson
    combine into
    $dv(eta,xi,2)=M/(M^2+2 eta)^(1/2)-exp(-eta)$.
    Its small-$eta$ expansion requires $M>=1$: ions must enter the sheath
    with at least $c_s=sqrt((k_B T_e)/m_i)$. A strongly electron-free
    near-wall region has the separate Child--Langmuir scaling
    $J_i$ scales as $V_w^(3/2)/d^2$.
  ]

  #knowledge-check((
    (
      question: [Why is the electron density Boltzmann-suppressed in a negative sheath?],
      answer: [For electrons $q_e=-e$, the equilibrium factor is $exp(-(q_e phi)/(k_B T_e))=exp((e phi)/(k_B T_e))$. A negative potential makes this factor smaller than one, so electrons are repelled.]
    ),
    (
      question: [Where does ion acceleration enter the cold sheath model?],
      answer: [The ion energy integral gives $u_i^2=u_s^2+(2 k_B T_e eta)/m_i$. As the potential becomes more negative, eta grows and the ion speed increases; continuity then changes the ion density.]
    ),
    (
      question: [What mathematical sign produces the Bohm criterion?],
      answer: [Near the quasineutral edge the normalized Poisson equation becomes $dv(eta,xi,2) approx (1-M^(-2))eta$. A monotone positive barrier can attach to the edge only when this coefficient is nonnegative, giving $M>=1$.]
    ),
    (
      question: [Why is the Child--Langmuir profile not the full sheath solution?],
      answer: [It neglects the electron density and assumes a large ion potential drop. It describes an electron-free space-charge subregion near the wall, while the full sheath must match to a quasineutral plasma with both species present.]
    ),
  ))

  #section-title[Floating potential and current balance] <floating-potential>

  #lead[
    A conducting surface can be electrically isolated, externally biased, or
    held at a prescribed potential. The isolated case is especially useful:
    the surface settles at the floating potential for which the net
    conventional current vanishes. The result makes the mass asymmetry of
    the incoming flux visible in one logarithm.
  ]

  #objectives((
    [write electron and ion currents with an explicit sign convention],
    [derive the exponential electron collection factor for a negative wall],
    [obtain the floating potential from zero net current],
    [separate the ideal cold-ion result from presheath and surface corrections],
  ))

  #unit-ledger[
    The floating potential $phi_f$ is in #unit("statvolt") relative to the
    plasma potential, and $(k_B T_e)/e$ is the corresponding potential scale.
    Fluxes are in #unit("cm^-2 s^-1"), current densities in
    statcoulomb per #unit("cm^2") per #unit("s"), and probe area is in
    #unit("cm^2"). The normalized wall bias
    $u_f=(e phi_f)/(k_B T_e)$ and all flux ratios are dimensionless.
  ]

  #assumption(
    [Floating planar wall with cold-ion Bohm entry],
    [Use a singly ionized hydrogen plasma, a Maxwellian electron population
    at the sheath edge, cold ions entering at the sonic speed
    $c_s=sqrt((k_B T_e)/m_i)$, and an absorbing surface without secondary
    emission. Take conventional current into the wall as positive for ions:
    $J=+e Gamma_i-e Gamma_e$. The plasma potential is the zero of $phi$.]
  )

  #definition(
    [Floating potential],
    [The floating potential $phi_f$ is the surface potential for which
    $J(phi_f)=0$. For a negative surface bias, the electron flux is
    the unretarded Maxwellian flux multiplied by the Boltzmann transmission factor:
    $Gamma_(e)(phi_f)=Gamma_(e,0) exp((e phi_f)/(k_B T_e))$.
    The ion flux is set primarily by the presheath and sheath-edge entry
    condition, so in the simplest model $Gamma_i=n_0 c_s$.]
  )

  #governing-law(
    [Zero-current balance],
    [Set
    $0=J_f=e Gamma_i-e Gamma_(e,0)
      exp((e phi_f)/(k_B T_e))$.
    Solving gives
    $phi_f=((k_B T_e)/e) ln(Gamma_i/Gamma_(e,0))$.
    With $Gamma_i=n_0 sqrt((k_B T_e)/m_i)$ and
    $Gamma_(e,0)=n_0 sqrt((k_B T_e)/(2 pi m_e))$,
    $phi_f=((k_B T_e)/(2e)) ln((2 pi m_e)/m_i)$.
    For hydrogen this ideal cold-ion value is approximately
    $phi_f approx -(2.84 k_B T_e)/e$.]
  )

  #details(
    [Derivation: electron transmission and the floating logarithm],
    [Let the plasma potential be zero and the wall potential be
    $phi_w<0$. An electron has potential energy $q_e phi=-e phi$, so an
    electron arriving from the plasma reaches the wall only if its normal
    kinetic energy exceeds the barrier $e abs(phi_w)$. For a Maxwellian,
    the flux integral over the transmitted part of velocity space is
    the unretarded flux times the Boltzmann factor:
    $Gamma_(e)(phi_w)=Gamma_(e,0)
      exp(-(e abs(phi_w))/(k_B T_e))
      =Gamma_(e,0) exp((e phi_w)/(k_B T_e))$.
    The equality uses $phi_w<0$.

    The conventional ion current density into the wall is positive,
    $J_i=+e Gamma_i$, while electron charge transport is negative,
    $J_e=-e Gamma_e$. Thus
    $J(phi_w)=e Gamma_i-e Gamma_(e,0)
      exp((e phi_w)/(k_B T_e))$.
    At a floating surface no external circuit supplies current, so set
    $J(phi_f)=0$:
    $Gamma_(e,0) exp((e phi_f)/(k_B T_e))=Gamma_i$.
    Divide by $Gamma_(e,0)$, take the natural logarithm, and multiply by
    $(k_B T_e)/e$:
    $phi_f=((k_B T_e)/e)ln(Gamma_i/Gamma_(e,0))$.

    The cold-ion Bohm flux is
    $Gamma_i=n_0 sqrt((k_B T_e)/m_i)$, while the thermal electron flux is
    $Gamma_(e,0)=n_0 sqrt((k_B T_e)/(2 pi m_e))$.
    Their ratio is $sqrt((2 pi m_e)/m_i)$. Substitution gives
    $phi_f=((k_B T_e)/(2e))ln((2 pi m_e)/m_i)$.
    For hydrogen, $(2 pi m_e)/m_i approx 0.00343$, whose logarithm is
    approximately $-5.68$, and half of it is $-2.84$.
    The numerical example then follows by evaluating the stated cgs
    definitions; no additional probe geometry factor has been introduced.]
  )
  #rechenbeispiel[
    Use a hydrogen plasma with
    $n_0=qty("1.0e10", "cm^-3")$ and
    $k_B T_e=qty("4.806e-12", "erg")$ (3.00 eV). Take
    $m_e=qty("9.109e-28", "g")$,
    $m_i=qty("1.673e-24", "g")$, and
    $e=qty("4.803e-10", "statcoulomb")$. Use the cold-ion Bohm flux and
    a planar area of $1.0 #unit("cm^2")$. Determine $lambda_D$, the
    electron and ion edge fluxes, the floating potential, and the ion
    current collected at the floating surface.

    Numerical result:
    $lambda_D approx qty("1.29e-2", "cm")$,
    $Gamma_(e,0) approx qty("2.90e17", "cm^-2 s^-1")$,
    $Gamma_i approx qty("1.70e16", "cm^-2 s^-1")$,
    $phi_f approx -(2.84 k_B T_e)/e approx -0.0284 #unit("statvolt")$
    (approximately $-8.52 #unit("V")$), and
    $e Gamma_i A approx qty("8.14e6", "statC/s")$, corresponding to
    approximately $2.72 #unit("mA")$.
  ]
  #interpretation(
    [Floating does not mean field-free],
    [Zero net current is a global electrical condition, not the statement
    that the electric field vanishes at the surface. The sheath field can be
    strong while the integrated ion and electron charge currents cancel.
    Changing ion temperature, presheath losses, secondary emission, magnetic
    incidence, or surface geometry changes the fluxes and therefore the
    floating potential.]
  )
  #summary[
    For a negative absorbing wall, electron collection is exponentially
    reduced:
    $Gamma_e=Gamma_(e,0) exp((e phi_w)/(k_B T_e))$.
    The ideal cold-ion floating condition is
    $phi_f=((k_B T_e)/e)ln(Gamma_i/Gamma_(e,0))
      approx -(2.84 k_B T_e)/e$ for hydrogen. The coefficient is a model
    result, not a universal material constant.
  ]
  #knowledge-check((
    (
      question: [Why does the electron current contain an exponential wall-potential factor?],
      answer: [A negative wall imposes a kinetic-energy barrier on electrons. Integrating the Maxwellian tail above that barrier multiplies the unretarded flux by $exp((e phi_w)/(k_B T_e))$.]
    ),
    (
      question: [What current sign convention is used for a floating surface?],
      answer: [Conventional current into the surface is positive for ions and negative for electrons: $J=e Gamma_i-e Gamma_e$. Floating means this signed sum is zero.]
    ),
    (
      question: [Why does the floating potential scale with electron temperature?],
      answer: [The electron barrier is measured by the dimensionless ratio $(e phi_f)/(k_B T_e)$. A hotter electron population requires a larger potential-energy barrier, so the potential drop scales with $(k_B T_e)/e$.]
    ),
    (
      question: [Why should the coefficient $-2.84$ not be transferred unchanged to every experiment?],
      answer: [It assumes cold ions at the Bohm speed, planar collection, Maxwellian electrons, no secondary emission, and no magnetic or collisional correction. Changing any of these changes the ion-to-electron flux ratio.]
    ),
  ))
  #section-title[Langmuir-probe current--voltage diagnostics] <langmuir-probe>
  #lead[
    A Langmuir probe turns the floating-surface balance into a controlled
    measurement. By sweeping the probe potential relative to the plasma and
    separating ion, retarding-electron, and electron-saturation regions, one
    can infer electron temperature, density, and an estimate of the plasma
    potential. The fit is only meaningful when the collection model and
    surface physics are stated.
  ]
  #objectives((
    [define probe bias and conventional probe current consistently],
    [identify ion-saturation, electron-retardation, and electron-saturation regions],
    [derive the temperature from the semilog slope of the electron current],
    [infer density from the electron saturation scale and list major corrections],
  ))
  #unit-ledger[
    Probe bias $phi_p-phi_"pl"$ is in #unit("statvolt") or a clearly stated
    converted voltage, current $I_p$ is in statcoulomb per #unit("s") in cgs
    (often reported in #unit("A")), and collection area $A$ is in
    #unit("cm^2"). The normalized bias
    $u=(e (phi_p-phi_"pl"))/(k_B T_e)$ and normalized current
    $I_p/(e Gamma_(e,0) A)$ are dimensionless. When temperature is quoted
    in electron-volts, $k_B T_e$ is an energy and
    $(e phi)/(k_B T_e)$ is evaluated with the same energy unit.
  ]
  #assumption(
    [Ideal planar probe characteristic],
    [Use a small absorbing planar probe in a stationary Maxwellian plasma.
    In the negative-bias branch, take the ion current as approximately
    saturated and the electron current as Boltzmann-retarded. Neglect
    magnetic-orbit effects, collisions in the sheath, secondary emission,
    photoemission, RF fluctuations, and probe perturbation of the bulk
    plasma. These assumptions define a diagnostic baseline, not a universal
    probe law.]
  )
  #definition(
    [Probe bias and current regions],
    [Let $phi_p$ be the probe potential and $phi_"pl"$ the plasma potential.
    Define $u=(e (phi_p-phi_"pl"))/(k_B T_e)$. With conventional current into
    the probe,
    $I_p=A(e Gamma_i-e Gamma_e)$.
    For strongly negative $u$, ions form an ion-saturation branch. As $u$
    increases, the electron current grows exponentially in the
    electron-retardation region. At still more positive bias, the electron
    collection becomes geometry- and sheath-limited, producing an electron
    saturation region rather than an unlimited exponential.]
  )
  #governing-law(
    [Idealized probe characteristic],
    [On the negative-bias side, write
    $I_(p)(u)=A [e Gamma_i-e Gamma_(e,0) exp(u)]$.
    The floating point is the zero of this curve. If
    $I_e=-e A Gamma_e$ denotes the electron current alone, then the
    electron-retarding branch satisfies
    $ln(abs(I_e)/I_(e,0))=u$.
    Its slope is therefore
    $dv(ln(abs(I_e)),phi_p)=e/(k_B T_e)$.
    The electron saturation scale gives
    $n_e=abs(I_(e,0))/[e A sqrt((k_B T_e)/(2 pi m_e))]$
    for the ideal planar collection model.]
  )
  #details(
    [Derivation: semilog temperature and density inversion],
    [The negative-bias electron flux is
    $Gamma_(e)(phi_p)=Gamma_(e,0)
      exp((e (phi_p-phi_"pl"))/(k_B T_e))$.
    The electron current is $I_e=-e A Gamma_e$. Its magnitude is
    $abs(I_e)=e A Gamma_(e,0)
      exp((e (phi_p-phi_"pl"))/(k_B T_e))$.
    Take the natural logarithm:
    $ln(abs(I_e))=ln(e A Gamma_(e,0))
      +(e (phi_p-phi_"pl"))/(k_B T_e)$.
    Differentiate with respect to probe potential:
    $dv(ln(abs(I_e)),phi_p)=e/(k_B T_e)$.
    Invert the slope to obtain
    $k_B T_e=e (dv(ln(abs(I_e)),phi_p))^(-1)$.
    If the voltage unit is volts and the energy unit is electron-volts,
    the numerical value of $k_B T_e$ in eV is the inverse slope in
    #unit("V^-1").

    At the extrapolated electron saturation reference, set
    $abs(I_(e,0))=e A Gamma_(e,0)$.
    The Maxwellian half-space flux is
    $Gamma_(e,0)=n_e sqrt((k_B T_e)/(2 pi m_e))$.
    Substitute and solve for density:
    $n_e=abs(I_(e,0))/[
      e A sqrt((k_B T_e)/(2 pi m_e))]$.
    This inversion uses the measured current in a consistent charge-current
    unit. In the numerical example, converting the cgs charge flux to
    amperes gives the stated density.]
  )
  #probe-iv-characteristic
  #animation(
    "../media/sheath-formation.mp4",
    "A normalized planar-boundary illustration shows a quasineutral plasma, a marked sheath edge, a charge-separated sheath, and a material wall. Electron and ion density profiles separate in the sheath, the normalized negative potential-energy barrier grows toward the wall, a fast-electron marker reflects, and an ion marker reaches the wall. The animation is schematic and not a particle-in-cell simulation.",
    caption: [
      A surface charges until the potential barrier and directed ion flow
      regulate the two collection fluxes. All coordinates and plotted
      profiles are normalized; the animation is a visual guide to the
      boundary conditions.
    ],
    poster: "../media/sheath-formation.png",
  )
  #animation(
    "../media/langmuir-probe.mp4",
    "A normalized idealized probe current--voltage curve is divided into ion saturation, electron retardation, and electron saturation regions. A marked floating bias is where the conventional current is zero. A companion panel shows a probe surrounded by a sheath, with electron and ion collection arrows. The animation is a teaching map, not experimental data.",
    caption: [
      Probe bias moves the operating point across collection regimes. The
      retarding branch carries the temperature information in its logarithmic
      slope, while the saturation scale carries the density information under
      the stated collection model.
    ],
    poster: "../media/langmuir-probe.png",
  )
  #rechenbeispiel[
    A planar probe has area $A=qty("0.10", "cm^2")$. In its electron-retarding
    region, a fit gives
    $dv(ln(abs(I_e)),phi_p)=qty("0.40", "V^-1")$.
    The extrapolated zero-bias electron saturation current magnitude is
    $abs(I_(e,0))=qty("4.0", "mA")$. Use the ideal planar model and determine
    the electron temperature in eV and density in #unit("cm^-3").
    Numerical result: $(k_B T_e)/e approx 2.50 #unit("V")$, so
    $T_e approx 2.50 #unit("eV")$, and
    $n_e approx qty("9.44e9", "cm^-3")$.
  ]
  #interpretation(
    [A probe measures a model-dependent collection response],
    [The semilog slope is powerful because it is local to the retarding
    branch, but the density scale depends on area and collection geometry.
    Cylindrical or spherical probes, magnetized plasmas, collisional sheaths,
    ion drift, secondary emission, photoemission, RF fluctuations, and
    contamination can all alter the characteristic. A reliable analysis
    reports the fit interval and the corrections used.]
  )
  #summary[
    A Langmuir probe sweeps
    $u=(e (phi_p-phi_"pl"))/(k_B T_e)$ through ion saturation, electron
    retardation, and electron saturation. On the ideal retarding branch,
    $dv(ln(abs(I_e)),phi_p)=e/(k_B T_e)$; the extrapolated saturation
    scale then gives density after the collection area and model are fixed.
  ]
  #knowledge-check((
    (
      question: [Which part of an ideal probe characteristic carries the electron-temperature information?],
      answer: [The logarithmic slope of the magnitude of the electron-retarding current is $e/(k_B T_e)$. The fit must exclude the ion and electron saturation regions.]
    ),
    (
      question: [What does the zero-current point represent on a floating probe?],
      answer: [It is the bias at which the signed ion and electron currents cancel. The point is the probe analogue of the floating wall condition.]
    ),
    (
      question: [Why can the electron saturation current be used to estimate density?],
      answer: [Under the planar Maxwellian model it is $e A n_e sqrt((k_B T_e)/(2 pi m_e))$. Once temperature and collection area are known, the current scale is proportional to density.]
    ),
    (
      question: [Why is an ideal Langmuir-probe fit not automatically a local plasma measurement?],
      answer: [The probe creates a sheath and samples an orbit-selected collection region. Geometry, magnetic field, collisions, emission, and RF effects can change the current before it is interpreted as a bulk parameter.]
    ),
  ))
  #chapter-nav(
    previous: (href: "12-hot-plasma-waves.html", title: [Hot plasma waves]),
    next: (href: "../appendices/mathematical-toolkit.html", title: [Mathematical toolkit]),
  )
]
