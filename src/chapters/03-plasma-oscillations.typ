#import "../theme.typ": *
#import "@preview/physica:0.9.8": grad, div, curl, laplacian, pdv, dv, vb
#import "../figures.typ": plasma-frequency-scale

#let chapter = [
  #page-title(number: 3)[Plasma oscillations] <plasma-oscillations>

  #lead[
    Debye shielding describes an equilibrium rearrangement of charge.
    Electron inertia also allows a displaced population to overshoot
    equilibrium and oscillate. The cold slab model isolates this dynamic
    response and supplies the plasma-frequency scale used throughout the
    course, following @chen2016 @bittencourt2004.
  ]

  #section-title[Electron plasma oscillations] <intro-plasma-oscillations>

  #lead[
    Shielding is a static response. What happens when electrons are displaced
    faster than they can rearrange thermally? The restoring electric field then
    produces an electron plasma oscillation.
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
    The corresponding ordinary frequency is $f_(p,s) = omega_(p,s)/(2 pi)$
    in hertz.
  ]

  #plasma-frequency-scale

  The electron Debye length $lambda_D$, in #unit("m"), is also related to the distance an electron at the thermal
  speed travels during an inverse plasma frequency:

  $ lambda_D = v_("th,e")/(sqrt(2) omega_(p,e)),
    quad omega_(p,e) = v_("th,e")/(sqrt(2) lambda_D) $ <intro-plasma-frequency-debye-relation>

  #equation-note[
    The factor $sqrt(2)$ follows from the convention
    $v_("th,e")=sqrt((2 k_B T_e)/m_e)$. If a source defines thermal speed as
    $sqrt((k_B T_e)/m_e)$, the same relation is written without that factor.
  ]

  The species inertial length $d_s=c/omega_(p,s)$ compares a light-transit
  time with the plasma-response time. Here $c$ is in
  #unit("m/s") and $d_s$ is in #unit("m"). This electromagnetic scale
  differs from the thermal screening length derived in
  #chapter-link("intro-debye-shielding")[Debye shielding].
  Here $v_("th,e")=sqrt((2 k_B T_e)/m_e)$ is the electron thermal-speed
  convention, in #unit("m/s"); $T_e$ is in kelvin.

  #details(
    [Derivation: the displacement oscillator],
    [#derivation-step[Create the charge-separation field]
    At equilibrium, positive ion and negative electron charge densities
    cancel. Shift the electron slab by $xi$. The overlap region remains nearly
    neutral, while the two boundary layers carry sheet charges of magnitude
    $e n_0 abs(xi).$

    Gauss's law for two infinite sheets gives the uniform internal field

    $ E=(e n_0 xi)/epsilon_0 .$

    #derivation-step[Identify the oscillator]
    An electron feels $F=-e E$, so

    $ m_e dv(xi,t,2)=-(n_0 e^2)/epsilon_0 xi .$

    The coefficient of $xi$ has units of $upright("s")^(-2)$ and identifies the
    square of the plasma frequency. Within the small-amplitude model,

    $ xi(t)=xi_0 cos(omega_(p,e) t+delta) .$
    ]
  )

  #animation(
    "../media/plasma-oscillation.mp4",
    "An electron slab oscillates against fixed positive ions. The electric field points along the signed displacement, while the electron force points oppositely. Both vanish at equilibrium. Displacement is normalized by its amplitude and time by the inverse electron plasma frequency, with unit [1].",
    caption: [
      Cold electron plasma oscillation: the charge-separation field produces
      a restoring electron force. The animation uses $xi/xi_0$ and
      $tau=omega_(p,e) t$, both with unit [1]. The position scale $L_0$
      satisfies $xi_0/L_0=0.55$. The field scale is
      $E_0=(e n_0 xi_0)/epsilon_0$; field and electron force are shown as
      $E/E_0$ and $F_e/(e E_0)$, respectively, both with unit [1].
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
      [(i) Estimate the plasma frequency $omega_p$ from thermal velocity $v_t$ and Debye length $lambda_D$.],
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
    previous: (href: "02-debye-shielding.html", title: [Debye shielding]),
    next: (href: "04-single-particle-motion.html", title: [Single-particle motion]),
  )
]
