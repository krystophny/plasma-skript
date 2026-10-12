#import "../theme.typ": *
#import "@preview/physica:0.9.8": grad, div, curl, laplacian, pdv, dv, vb
#import "../figures.typ": plasma-frequency-scale
#import "../opening-diagrams.typ": electron-slab

#let chapter = [
  #page-title(number: 3)[Plasma oscillations] <plasma-oscillations>

  #lead[
    A plasma is neutral on average, but its electrons are light and mobile.
    If a slab of electrons is shifted rigidly against the ions, the separated
    charge pulls it back, and electron inertia carries it past equilibrium
    into an oscillation. This cold slab model is the first rigid
    charge-separation model of the course and supplies the plasma-frequency
    scale used throughout, following @chen2016 @bittencourt2004.
  ]

  #section-title[Electron plasma oscillations] <intro-plasma-oscillations>

  #lead[
    What happens when all electrons in a region are displaced together,
    faster than thermal motion can rearrange them? Gauss's law gives the
    restoring electric field, and that field produces an electron plasma
    oscillation.
  ]

  #objectives((
    [derive the cold electron plasma frequency from a displacement model],
    [separate the restoring force from the equilibrium charge balance],
    [state how temperature, collisions, and magnetic fields change the model],
  ))

  #unit-ledger[
    The electron displacement $xi$ is in #unit("m"). Ions are singly charged
    and initially stationary.
  ]

  #assumption(
    [Cold, unmagnetized, collisionless response],
    [Displace a uniform electron slab by a small amount $xi$ relative to fixed
    ions. Ignore pressure, collisions, magnetic fields, and density variation
    within the slab. The model isolates the electrostatic restoring force and
    describes small-amplitude motion about equilibrium.]
  )

  A displacement creates two oppositely charged boundary sheets. The sheet
  charge magnitude is $e n_0 abs(xi)$, so the electric field between them is

  #figure(electron-slab(),
    alt: "Electrons shifted to the right leave positive charge at the left boundary and negative charge at the right; the electric field points right and the electron force points left.",
    caption: [The charge signs and arrow directions show the restoring force.
      This schematic shows geometry, not a numerical length scale.])

  $ bold(E) = (e n_0 xi)/epsilon_0 bold(e)_x $ <plasma-oscillation-field>

  #equation-note[
    $bold(e)_x$ is a fixed unit vector and $xi$ is the signed
    electron displacement along it. The field reverses when $xi$ changes sign
    and the electron force points opposite to it. The field
    is in #unit("V/m") when $n_0$ is in #unit("m^-3") and $xi$ in #unit("m").
  ]

  The electron force is opposite to the displacement:

  $ m_e dv(xi,t,2) = -e E = -(n_0 e^2)/epsilon_0 xi $ <plasma-oscillation-force>

  #equation-note[
    The force is in #unit("N"). The negative sign is the restoring
    sign for the electron charge $-e$.
  ]

  Dividing by $m_e$ gives the harmonic-oscillator equation

  $ dv(xi,t,2) + omega_(p,e)^2 xi = 0, quad omega_(p,e) = sqrt((n_0 e^2)/(epsilon_0 m_e)) $ <plasma-oscillation-frequency>

  #equation-note[
    $omega_(p,e)$ is an angular frequency in $upright("s")^(-1)$.
    The cold model has no damping and no thermal dispersive correction.
  ]

  #strong[Frequency and length scales] <oscillation-scales>

  For a homogeneous species $s$ with number density $n_s$ in #unit("m^-3"),
  charge $q_s$ in #unit("C"), and mass $m_s$ in #unit("kg"), the plasma frequency is

  $ omega_(p,s) = sqrt((n_s q_s^2) / (epsilon_0 m_s)) $ <intro-plasma-frequency>

  #equation-note[
    $omega_(p,s)$ is in $upright("s")^(-1)$ as an angular frequency.
    The corresponding ordinary frequency is $f_(p,s) = omega_(p,s)\/(2 pi)$
    in hertz.
  ]

  If the ions move as well, the electron and ion slabs oscillate against each
  other. Ions of charge $Z e$ and density $n_i = n_e\/Z$ shift by $xi_i$, the
  electrons by $xi_e$, and the field depends on the relative shift
  $xi = xi_e - xi_i$. Both species feel it, so the frequencies add:

  $ omega_p^2 = omega_(p,e)^2 + omega_(p,i)^2 = (n_e e^2)/(epsilon_0 m_"eff"),
    quad 1/m_"eff" = 1/m_e + Z/m_i $ <intro-plasma-frequency-ions>

  #equation-note[
    $m_"eff"$ is in #unit("kg"). Since $m_i >> m_e$, $m_"eff" approx m_e$:
    the ion correction to $omega_p^2$ is of relative size $Z m_e\/m_i$.
  ]

  #plasma-frequency-scale

  The species inertial length $d_s=c\/omega_(p,s)$ compares a light-transit
  time with the plasma-response time. Here $c$ is in
  #unit("m/s") and $d_s$ is in #unit("m"). This electromagnetic scale
  differs from the thermal screening length derived in
  #chapter-link("intro-debye-shielding")[Debye shielding].

  The inertial length also decides how an electromagnetic wave meets a
  plasma. A transverse wave of angular frequency $omega$ in a cold,
  unmagnetized plasma obeys $omega^2 = omega_(p,e)^2 + c^2 k^2$, with
  wavenumber $k$ in #unit("m^-1"), derived in
  #chapter-link("wave-dispersion")[electromagnetic dispersion]. Below
  $omega_(p,e)$ the electrons follow the field and screen it within the skin
  depth $c\/sqrt(omega_(p,e)^2 - omega^2)$, which tends to $d_e$ for
  $omega << omega_(p,e)$; the wave is reflected. Above $omega_(p,e)$ the
  electron bulk can no longer follow, and the wave is transmitted with a
  longer wavelength than in vacuum.

  #animation(
    "../media/em-wave-plasma-reflection.mp4",
    "Left: electron sheets near the edge of a plasma, their transverse displacement magnified thirty times. Right: the transverse electric field E_y over E_0 across vacuum and plasma, with the plasma edge marked. First run at omega = 0.5 omega_pe: the incident and reflected waves form a standing pattern in vacuum and the field decays inside the plasma; the electrons near the edge oscillate together. Second run at omega = 2 omega_pe: the wave enters the plasma with a longer wavelength and only a weak reflection. At the end of each run the linear-theory envelope fades in. Positions are normalized by c over omega_pe and time by the inverse plasma frequency, with unit [1].",
    caption: [
      An electromagnetic wave at a plasma edge, computed with kin6d: a
      one-dimensional Maxwell--Lorentz run with cold electron macroparticles,
      fixed ions and absorbing boundaries. At $omega = 0.5 omega_(p,e)$ the
      measured reflection is $abs(R) = 0.9996$ and the skin depth
      $1.155 c\/omega_(p,e)$; at $omega = 2 omega_(p,e)$ the reflection is
      $R = 0.072$ and the transmitted wavelength $3.628 c\/omega_(p,e)$, each
      within $0.1$~% of linear theory. Positions are $x omega_(p,e)\/c$ and
      time $omega_(p,e) t$, with unit [1]; the electron displacement is
      magnified for visibility.
    ],
    poster: "../media/em-wave-plasma-reflection.png",
  )

  #details(
    [Derivation: the displacement oscillator],
    [#derivation-step[Create the charge-separation field]
    At equilibrium, positive ion and negative electron charge densities
    cancel. Shift the electron slab by $xi$. The overlap region remains nearly
    neutral, while the two boundary layers carry sheet charges of magnitude
    $e n_0 abs(xi).$

    Gauss's law for two infinite sheets gives the uniform internal field

    $ E=(e n_0 xi)/epsilon_0 . $

    #derivation-step[Identify the oscillator]
    An electron feels $F=-e E$, so

    $ m_e dv(xi,t,2)=-(n_0 e^2)/epsilon_0 xi . $

    The coefficient of $xi$ has units of $upright("s")^(-2)$ and identifies the
    square of the plasma frequency. Within the small-amplitude model,

    $ xi(t)=xi_0 cos(omega_(p,e) t+delta) . $
    ]
  )

  #animation(
    "../media/plasma-oscillation.mp4",
    "An electron slab oscillates against fixed positive ions. The electric field points along the signed displacement, while the electron force points oppositely. Both vanish at equilibrium. Displacement is normalized by its amplitude and time by the inverse electron plasma frequency, with unit [1].",
    caption: [
      Cold electron plasma oscillation: the charge-separation field produces
      a restoring electron force. The animation uses $xi\/xi_0$ and
      $tau=omega_(p,e) t$, both with unit [1]. The trace $xi\/xi_0$ is a
      numerical solution of the cold slab equation computed with kin6d,
      enclosed by a certified error band thinner than the drawn line. The
      position scale $L_0$ is a quarter of the slab half-width $a$, with
      $xi_0\/a=0.1$, so $xi_0\/L_0=0.4$. The field scale is
      $E_0=e n_0 xi_0\/epsilon_0$; field and electron force are shown as
      $E\/E_0$ and $F_e\/(e E_0)$, respectively, both with unit [1].
    ],
    poster: "../media/plasma-oscillation.png",
  )

  #interpretation(
    [Limits and extensions],
    [Finite temperature adds pressure and produces a wavenumber-dependent
    Langmuir-wave frequency. Collisions damp the motion. A background magnetic
    field couples the displacement to gyromotion. Those effects belong to the
    kinetic and wave chapters, while the oscillator here provides the local
    response scale.]
  )

  #summary[
    A small collective electron displacement creates a restoring electric field.
    In the cold, collisionless, unmagnetized limit its natural angular
    frequency is $omega_(p,e)$. Pressure, collisions, and magnetic fields are
    controlled extensions of this baseline model.
  ]

  #exam-prompts(
    (
      [(f) Describe and derive electron plasma oscillations.],
    ),
    [Plasma Physics Exam.pdf, p. 1],
  )

  #knowledge-check((
    (
      question: [What supplies the restoring force in the cold plasma oscillator?],
      answer: [The charge separation between displaced electrons and stationary ions creates an electric field, and the electron charge makes the force oppose the displacement.],
    ),
    (
      question: [Why does the cold model produce a single local frequency rather than a dispersive frequency?],
      answer: [Pressure and spatial gradients were omitted, so the restoring coefficient contains density and particle constants but no wavenumber.],
    ),
    (
      question: [How would electron collisions change the oscillator qualitatively?],
      answer: [They introduce momentum loss and therefore damp the oscillation. The undamped harmonic equation is no longer complete.],
    ),
    (
      question: [What is the dimensional status of $t omega_(p,e)$ in the animation?],
      answer: [It is dimensionless because time in seconds is multiplied by an angular frequency in $upright("s")^(-1)$.],
    ),
  ))

  #chapter-nav(
    previous: (href: "02-thermal-equilibrium.html", title: [Temperature, entropy, and thermal ionization]),
    next: (href: "04-debye-shielding.html", title: [Debye shielding]),
  )
]
