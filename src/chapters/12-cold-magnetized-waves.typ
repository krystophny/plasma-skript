#import "../theme.typ": *
#import "../figures.typ": magnetized-dielectric, magnetized-parallel-dispersion, magnetized-oblique-geometry, magnetized-cutoff-map
#import "@preview/physica:0.9.8": div, grad, pdv, curl
#import "@preview/unify:0.8.1": qty, unit

#let chapter = [
  #page-title[12. Waves in cold magnetized plasmas] <cold-magnetized-waves>

  #lead[
    A static magnetic field turns the isotropic plasma response into a tensor.
    This chapter derives that tensor from the cold-fluid momentum equation and
    uses it to organize parallel, perpendicular, and oblique wave propagation.
    Propagation direction, polarization, and frequency ordering are carried
    together throughout, following the standard cold-plasma treatment in
    @bittencourt2004.
  ]

  #callout(
    [The magnetic field selects a basis],
    [The magnetic field couples electric-field components perpendicular to
    $bold(B)_0$ and leaves the parallel response distinct. The wave vector
    $bold(k)$ supplies a second direction: a component perpendicular to
    $bold(B)_0$ need not be transverse to the wave. Keep these two geometries
    separate when identifying polarization.]
  )

  #section-title[Cold magnetized response and the dielectric tensor] <magnetized-dielectric>

  #lead[
    How does a uniform magnetic field enter a linear wave calculation? Start
    with the cold momentum equation for each species, solve the transverse
    velocity response, and convert the current into a dielectric tensor. Once
    this tensor is known, Maxwell's equations supply the wave matrix.
  ]

  #objectives((
    [state the cold, homogeneous, collisionless magnetized ordering],
    [derive the species current response from the linear momentum equation],
    [identify the transverse and parallel dielectric coefficients],
    [write the Maxwell wave matrix and its determinant condition],
  ))

  #unit-ledger[
    The dielectric coefficients and refractive index $N=(k c)/omega$ are
    dimensionless.
  ]

  #assumption(
    [Uniform cold magnetized equilibrium],
    [Use constant $n_(s,0)$ and $bold(B)_0=B_0 bold(e)_z$, with no equilibrium
    flow, no collisions, no pressure perturbation, and no spatial gradients
    of the equilibrium. The ions are fixed for the electron-response formulas
    below; retaining their inertia means summing the species responses. Use the
    Fourier convention $exp(i (bold(k) dot bold(r)-omega t))$.]
  )

  #definition(
    [Signed gyrofrequency and plasma frequency],
    [For species $s$, define the signed gyrofrequency and the positive plasma
    frequency by
    $Omega_s=(q_s B_0)/m_s$ and
    $omega_(p,s)^2=(n_(s,0) q_s^2)/(epsilon_0 m_s)$.
    For electrons it is useful to reserve
    $omega_(c,e)=(abs(q_e) B_0)/m_e>0$
    for the cyclotron-frequency magnitude. The sign of $q_e$ remains in the
    transverse polarization convention.]
  )

  #definition(
    [Cold dielectric tensor],
    [The current response is represented by
    $bold(epsilon)_(p) dot bold(E)_1=bold(E)_1+(i/(omega epsilon_0)) bold(j)_1$,
    so that $bold(epsilon)_(p)=bold(I)+sum_s bold(chi)_s$ with species
    susceptibility $bold(chi)_s=bold(sigma)_s/(-i omega epsilon_0)$ for the
    species conductivity $bold(sigma)_s$ defined by $bold(j)_(s,1)=bold(sigma)_s dot bold(E)_1$,
    with
    $bold(epsilon)_(p)=mat(
      epsilon_(perp), -i epsilon_(times), 0;
      i epsilon_(times), epsilon_(perp), 0;
      0, 0, epsilon_(parallel))$.
    For several species,
    $epsilon_(perp)=1-sum_s omega_(p,s)^2/(omega^2-Omega_s^2)$,
    $epsilon_(times)=sum_s
      ((Omega_s omega_(p,s)^2)/(omega (omega^2-Omega_s^2)))$,
    and
    $epsilon_(parallel)=1-sum_s omega_(p,s)^2/omega^2$.
    The off-diagonal coefficient changes sign with the charge convention.]
  )

  Each tensor column gives the response to one electric-field component.
  The coefficients $epsilon_(perp)$ and $epsilon_(parallel)$ describe
  response perpendicular and parallel to the background magnetic field;
  $epsilon_(times)$ couples the two perpendicular directions. The symbol
  $times$ in its subscript is a label, not an instruction to take another
  cross product. The identity part is the vacuum response, and the remaining
  terms describe the induced plasma current.

  #governing-law(
    [Magnetized Maxwell wave equation],
    [For a plane wave, Maxwell's equations reduce to
    $bold(k) times (bold(k) times bold(E)_1)
      +omega^2/c^2 bold(epsilon)_(p) dot bold(E)_1=bold(0)$.
    Equivalently,
    $bold(k)(bold(k) dot bold(E)_1)-k^2 bold(E)_1
      +omega^2/c^2 bold(epsilon)_(p) dot bold(E)_1=bold(0)$.
    The dispersion relation is the condition that the associated coefficient
    matrix has zero determinant.]
  )

  #details(
    [Derivation: from cold momentum to the dielectric tensor],
    [#derivation-step[Resolve the cold momentum equation]
    The linearized cold momentum equation is

    $ -i omega m_s bold(u)_(s,1)=q_s (
      bold(E)_1+bold(u)_(s,1) times bold(B)_0) .$

    With $bold(B)_0=B_0 bold(e)_z$, the transverse components form a coupled
    two-by-two system:

    $ -i omega u_(s,1,x)-Omega_s u_(s,1,y)
      =(q_s/m_s) E_(1,x) $

    and

    $ Omega_s u_(s,1,x)-i omega u_(s,1,y)
      =(q_s/m_s) E_(1,y) .$

    The parallel component is independent:

    $ -i omega u_(s,1,z)=(q_s/m_s) E_(1,z) .$

    #derivation-step[Invert the transverse response]
    Inverting the transverse system gives

    $ u_(s,1,x)=((i q_s omega)/(m_s (omega^2-Omega_s^2)))
      E_(1,x)
      -((q_s Omega_s)/(m_s (omega^2-Omega_s^2))) E_(1,y) ,$

    and

    $ u_(s,1,y)=((q_s Omega_s)/(m_s (omega^2-Omega_s^2)))
      E_(1,x)
      +((i q_s omega)/(m_s (omega^2-Omega_s^2))) E_(1,y) .$

    Multiply by $q_s n_(s,0)$ and sum over species to obtain $bold(j)_1$.
    The transverse entries are coupled because the Lorentz force rotates the
    velocity in the $x-y$ plane; the parallel motion has no magnetic force.

    #derivation-step[Define the dielectric response]
    Insert the current into

    $ bold(epsilon)_(p) dot bold(E)_1
      =bold(E)_1+(i/(omega epsilon_0)) bold(j)_1 .$

    Reading off the coefficients gives the cold dielectric tensor displayed
    above. Its off-diagonal entries encode the rotation of transverse motion.

    #derivation-step[Insert the response into Maxwell's equations]
    Fourier-transformed Faraday and Ampere laws are

    $ bold(k) times bold(E)_1=omega bold(B)_1 $

    and

    $ bold(k) times bold(B)_1=-(omega bold(E)_1)/c^2
      -i mu_0 bold(j)_1 .$

    Substitute the first relation into the second, eliminate $bold(j)_1$ by
    the dielectric definition with $mu_0 epsilon_0=1/c^2$, and use

    $ bold(k) times (bold(k) times bold(E)_1)
      =bold(k)(bold(k) dot bold(E)_1)-k^2 bold(E)_1 .$

    A nonzero field amplitude requires the determinant of the resulting wave
    matrix to vanish.]
  )

  #magnetized-dielectric

  #rechenbeispiel[
    Assume a homogeneous, cold, collisionless, magnetized electron response
    with fixed ions and a uniform field $bold(B)_0=B_0 bold(e)_z$.
    For a hydrogen plasma use
    $n_0=qty("1.0e16", "m^-3")$, $B_0=qty("1.0e-2", "T")$,
    $e=qty("1.602e-19", "C")$,
    $m_e=qty("9.109e-31", "kg")$, and
    $epsilon_0=qty("8.854e-12", "F/m")$. Determine the electron plasma frequency,
    the electron cyclotron-frequency magnitude, and their ratio.

    Numerical result: $omega_(p,e)=qty("5.64e9", "s^-1")$,
    $omega_(c,e)=qty("1.76e9", "s^-1")$, and
    #normalized-label[$omega_(c,e)/omega_(p,e)=qty("0.312", "1")$].
  ]

  #rechenbeispiel[
    Assume a homogeneous, cold, collisionless, fixed-ion electron response
    with $bold(B)_0$ along $z$. At angular
    frequency $omega=qty("1.00e10", "s^-1")$, use
    $omega_(p,e)=qty("5.64e9", "s^-1")$,
    $omega_(c,e)=qty("1.76e9", "s^-1")$, and the signed convention
    $Omega_e=-omega_(c,e)$. Evaluate the cold dielectric coefficients
    $epsilon_(perp)$, $epsilon_(times)$, and $epsilon_(parallel)$.

    Target: report the three dimensionless entries of the dielectric tensor.

    Numerical result: #normalized-label[$epsilon_(perp)=qty("0.672", "1")$],
    #normalized-label[$epsilon_(times)=qty("-5.78e-2", "1")$], and
    #normalized-label[$epsilon_(parallel)=qty("0.682", "1")$].
  ]

  #interpretation(
    [Anisotropy of a homogeneous plasma],
    [The tensor is anisotropic even though the equilibrium is homogeneous.
    Homogeneity lets us use plane waves; the magnetic field breaks rotational
    symmetry and determines which field components can exchange phase and
    energy.]
  )

  #summary[
    A cold uniform magnetic field makes the plasma response tensorial. Solving
    the transverse Lorentz-force response gives $epsilon_(perp)$ and
    $epsilon_(times)$, while parallel motion gives $epsilon_(parallel)$.
    Maxwell's wave matrix and its determinant then determine the modes.
  ]

  #knowledge-check((
    (
      question: [Which assumption makes the cold-fluid momentum equation algebraic in Fourier space?],
      answer: [A homogeneous equilibrium together with the plane-wave ansatz replaces derivatives by multiplication by $-i omega$ and $i bold(k)$. The cold ordering removes pressure gradients and the collisionless ordering removes drag terms.]
    ),
    (
      question: [Why are the two transverse electric components coupled?],
      answer: [The transverse velocity crossed with $bold(B)_0$ points into the other transverse direction. The Lorentz force therefore couples the $x$ and $y$ momentum equations and creates the off-diagonal dielectric coefficient $epsilon_(times)$.]
    ),
    (
      question: [Why is the parallel dielectric coefficient different from the transverse coefficient?],
      answer: [The magnetic force vanishes for motion parallel to $bold(B)_0$. Parallel motion therefore responds with the unmagnetized factor $1-sum_s omega_(p,s)^2/omega^2$, while transverse motion contains the gyrofrequency denominators.]
    ),
    (
      question: [What mathematical condition selects a wave mode?],
      answer: [The wave amplitudes satisfy a homogeneous matrix equation. A nonzero electric-field vector exists only when the matrix is singular, so its determinant must vanish.]
    ),
  ))

  #section-title[Parallel propagation and circular polarization] <parallel-magnetized-waves>

  #lead[
    When the wave travels along the magnetic field, the longitudinal and
    transverse problems separate. The transverse block is diagonalized by
    circular polarization: the two rotation senses see different effective
    dielectric coefficients, while the longitudinal branch remains a local
    plasma oscillation in the cold limit.
  ]

  #objectives((
    [factor the parallel wave matrix into longitudinal and circular branches],
    [derive the two circular-mode dispersion relations],
    [calculate the cutoff frequencies and identify the cyclotron resonance],
    [explain how different circular wave numbers rotate linear polarization],
  ))

  #unit-ledger[
    The refractive index $N=(k c)/omega$, normalized frequency is
    $W=omega/omega_(p,e)$, and magnetization is
    $Y=omega_(c,e)/omega_(p,e)$; all three are dimensionless. The dimensional
    $k$ is in #unit("m^-1"), $omega$ and $omega_(c,e)$ are in
    #unit("s^-1"), and phase or group velocities are in #unit("m/s").
  ]

  #assumption(
    [Parallel fixed-ion propagation],
    [Take $bold(k)=k bold(e)_z$ parallel to $bold(B)_0$, retain the cold
    collisionless electron response, and treat ions as stationary. The
    positive magnitude $omega_(c,e)$ is used below. The labels $+$ and $-$
    refer to the chosen Fourier and field-basis convention; reversing the
    time convention swaps the handedness names but not the two eigenvalues.]
  )

  #definition(
    [Circular eigenmodes],
    [For an electron plasma with fixed ions, define the circular eigenmode
    label $s=+1$ or $s=-1$ by
    $E_(1,y)=-i s E_(1,x)$.
    The corresponding refractive indices are
    $N_(s)^2=epsilon_(s)=epsilon_(perp)-s epsilon_(times)
      =1-omega_(p,e)^2/(omega(omega+s omega_(c,e)))$.
    Thus the $s=+1$ branch has the lower positive-frequency cutoff, while
    the $s=-1$ branch has a cyclotron-sensitive denominator at
    $omega=omega_(c,e)$.]
  )

  In these circular-mode formulas, $s$ labels polarization, not particle
  species. The factor $-i s$ specifies equal amplitudes with a
  quarter-cycle phase difference between the two electric components.
  This algebraic convention fixes the rotation sense without relying on
  an unstated viewing direction.

  #governing-law(
    [Parallel dispersion and cutoffs],
    [The longitudinal branch is
    $epsilon_(parallel)=0 quad => quad omega=omega_(p,e)$.
    The two transverse circular branches are
    $N_(s)^2=epsilon_(s)=1-omega_(p,e)^2/(omega(omega+s omega_(c,e)))$.
    Their positive-frequency cutoffs satisfy $N_(s)=0$ and are
    $omega_"cut,s"=(sqrt(omega_(c,e)^2+4 omega_(p,e)^2)-s omega_(c,e))/2$.
    A real $N$ denotes bulk propagation in this idealized model; $N^2<0$
    denotes an evanescent branch.]
  )

  #details(
    [Derivation: circular factorization and Faraday rotation],
    [#derivation-step[Factor the parallel wave matrix]
    For parallel propagation, divide the wave matrix by $omega^2/c^2$:

    $ mat(
      epsilon_(perp)-N^2, -i epsilon_(times), 0;
      i epsilon_(times), epsilon_(perp)-N^2, 0;
      0, 0, epsilon_(parallel))
      mat(E_x; E_y; E_z)=mat(0;0;0) .$

    The longitudinal factor gives $epsilon_(parallel)=0$. The transverse
    determinant is

    $ (epsilon_(perp)-N^2)^2-epsilon_(times)^2=0 .$

    Thus the two transverse eigenvalues are

    $ N^2=epsilon_(perp)+epsilon_(times), quad
      N^2=epsilon_(perp)-epsilon_(times) .$

    #derivation-step[Express the circular branches]
    For an electron, the signed gyrofrequency is negative when $B_0$ points
    along positive $z$. Use its positive magnitude $omega_(c,e)$ and the
    circular basis

    $ E_(1,y)=-i s E_(1,x) .$

    The two indices become

    $ N_(s)^2=epsilon_(perp)-s epsilon_(times)
      =1-omega_(p,e)^2/(omega(omega+s omega_(c,e))) .$

    Setting $N_(s)=0$ gives

    $ omega^2+s omega_(c,e) omega-omega_(p,e)^2=0 .$

    The positive root is the cutoff stated above. For $s=-1$, the denominator
    vanishes at the electron cyclotron frequency. The cold response is then
    singular, so finite temperature or collisions are required before that
    limit is interpreted.

    #derivation-step[Accumulate the relative phase]
    A linearly polarized wave is the equal-amplitude sum of the two circular
    eigenmodes. After a distance $L$, their relative phase is

    $ (k_+-k_-)L .$

    The major axis rotates by half this phase:

    $ theta_F=((k_+-k_-)L)/2 .$

    If the plasma varies slowly along the ray, use the local wave-number
    difference instead:

    $ theta_F=(integral (k_+(z)-k_-(z)) dif z)/2 .$
    ]
  )

  #magnetized-parallel-dispersion

  Faraday rotation compares two circular modes at the same frequency.
  When both propagate without attenuation and have equal amplitudes, their
  superposition remains linearly polarized. Different wave numbers rotate
  its polarization axis with distance; at a fixed position that axis remains
  fixed as the electric vector oscillates. If one component is evanescent or
  attenuated differently, the equal-amplitude linear-polarization picture
  no longer applies.

  #callout(
    [Pause and predict],
    [A linearly polarized wave enters the plasma with its electric field along
    $bold(e)_x$. Before opening the animation, predict whether the output
    polarization can remain fixed when $k_+ != k_-$. It cannot: the two
    circular components accumulate different phases, so their superposition
    rotates. The viewing direction and Fourier convention determine the sign
    of the rotation; its magnitude follows from $k_+-k_-$.]
  )

  #animation(
    "../media/magnetized-polarization.mp4",
    "Two equal-amplitude circular fields rotate with opposite senses at one temporal frequency. Their vector sum oscillates along a fixed linear axis at each position; those axes rotate with propagation distance. Dashed axes and distinct tip shapes identify polarization and components without relying on color. The fields and coordinates are normalized.",
    caption: [
      Faraday rotation: a linearly polarized wave can be decomposed into two
      circular eigenmodes. Because the magnetic field gives them different
      wave numbers, their relative phase changes along the path and the
      polarization plane rotates. The prescribed illustration uses
      $k_+ L_0=1.2$, $k_- L_0=0.8$, and $omega t_0=1$, with each component
      of amplitude $E_0/2$. Here $L_0$, $t_0$, and $E_0$ are reference
      length, time, and electric-field scales. The transverse
      panel shows the highlighted position $z=3 L_0$. At fixed
      position the polarization axis is stationary in time; the wave numbers
      are prescribed.
    ],
    poster: "../media/magnetized-polarization.png",
  )

  #rechenbeispiel[
    Assume a homogeneous, cold, collisionless, fixed-ion electron response
    with uniform $bold(B)_0$ and parallel propagation. For the
    fixed-ion plasma with
    $omega_(p,e)=qty("5.64e9", "s^-1")$,
    $omega_(c,e)=qty("1.76e9", "s^-1")$, and a parallel wave with
    $omega=qty("2.00e10", "s^-1")$ crossing a path of
    $L=qty("0.10", "m")$, determine the two refractive indices and the
    Faraday-rotation angle $theta_F=((k_+-k_-)L)/2$.

    Numerical result: #normalized-label[$N_+=qty("0.963", "1")$],
    #normalized-label[$N_-=qty("0.955", "1")$], and
    $theta_F=qty("2.45e-2", "rad")=qty("1.41", "deg")$.
  ]

  #interpretation(
    [The resonant branch is not an ordinary cutoff],
    [At a cutoff, $N$ goes to zero and the wavelength becomes large. At the
    cyclotron resonance, the cold susceptibility becomes singular and $N$ can
    grow without bound. The former is a propagation boundary; the latter is a
    warning that neglected orbit-scale, thermal, collisional, or kinetic
    physics may control the response.]
  )

  #summary[
    Parallel propagation separates a longitudinal plasma oscillation from two
    circularly polarized transverse modes. The magnetic field splits their
    cutoffs and creates a cyclotron-sensitive resonance. A linear polarization
    rotates because its two circular components accumulate different phases.
  ]

  #knowledge-check((
    (
      question: [Why are circular polarizations the natural eigenvectors for parallel propagation?],
      answer: [The transverse dielectric block has equal diagonal entries and antisymmetric off-diagonal entries. Its eigenvectors are the two circular combinations of $E_x$ and $E_y$, which remove the coupling.]
    ),
    (
      question: [What is the physical meaning of a circular-mode cutoff?],
      answer: [It is the frequency at which the corresponding refractive index vanishes. The wave number is then zero, so the branch meets the zero-wave-number boundary between propagation and non-propagation.]
    ),
    (
      question: [Which cold-plasma feature identifies the cyclotron-sensitive branch?],
      answer: [Its denominator contains $omega(omega-omega_(c,e))$ under the chosen convention, so the response becomes singular as $omega$ approaches the electron cyclotron frequency.]
    ),
    (
      question: [Why does a linearly polarized wave rotate in a magnetized plasma?],
      answer: [A linear wave is a sum of two circular eigenmodes. Since the modes have different wave numbers, their relative phase changes with distance and the direction of the linear polarization changes.]
    ),
  ))

  #section-title[Perpendicular propagation: ordinary and extraordinary modes] <perpendicular-magnetized-waves>

  #lead[
    Turning the wave vector perpendicular to the magnetic field changes which
    field component is decoupled. The ordinary mode has its electric field
    parallel to the background field and therefore sees the unmagnetized
    plasma response. The extraordinary mode has electric components in the
    plane perpendicular to the background field, including a component along
    the wave vector, and contains an upper-hybrid resonance.
  ]

  #objectives((
    [factor the perpendicular wave matrix into ordinary and extraordinary modes],
    [derive the ordinary and extraordinary refractive indices],
    [identify the upper-hybrid resonance and the extraordinary polarization],
    [distinguish a cutoff from a resonant stopband],
  ))

  #unit-ledger[
    The angle $theta$ is dimensionless and measured in radians. The refractive
    index $N=(k c)/omega$, $W=omega/omega_(p,e)$, and
    $Y=omega_(c,e)/omega_(p,e)$ are dimensionless. Dimensional $k$ is in
    #unit("m^-1"), $omega$ in #unit("s^-1"), and wavelengths in #unit("m").
  ]

  #assumption(
    [Perpendicular fixed-ion propagation],
    [Take $bold(k)=k bold(e)_x$ and
    $bold(B)_0=B_0 bold(e)_z$. Retain a cold collisionless electron fluid with
    fixed ions. The ordinary and extraordinary names refer to this geometry;
    they should not be transferred to an oblique mode without checking its
    polarization.]
  )

  #definition(
    [Ordinary and extraordinary indices],
    [For the ordinary mode, $bold(E)_1$ is parallel to $bold(B)_0$ and
    $N_O^2=epsilon_(parallel)=1-omega_(p,e)^2/omega^2$.
    The extraordinary mode is polarized in the $x-y$ plane and has
    $N_X^2=(epsilon_(perp)^2-epsilon_(times)^2)/epsilon_(perp)$.
    Define the upper-hybrid frequency by
    $omega_"UH"=sqrt(omega_(p,e)^2+omega_(c,e)^2)$; then
    $N_X^2=1-
      (omega_(p,e)^2 (omega^2-omega_(p,e)^2)) /
      (omega^2 (omega^2-omega_"UH"^2))$.
    The extraordinary polarization ratio is
    $E_x/E_y=(i epsilon_(times))/epsilon_(perp)$, away from zeros of the
    denominator.]
  )

  #governing-law(
    [Ordinary and extraordinary branches],
    [The ordinary branch obeys
    $omega^2=omega_(p,e)^2+c^2 k^2$ and has the same cutoff as the cold
    unmagnetized transverse wave. The extraordinary branch obeys
    $N_X^2=(epsilon_(+) epsilon_(-))/epsilon_(perp)$,
    with circular factors $epsilon_(s)$ from the parallel problem. Its
    denominator vanishes at $omega=omega_"UH"$, so the cold wave number
    diverges at the upper-hybrid resonance.]
  )

  #details(
    [Derivation: perpendicular factorization],
    [#derivation-step[Separate the ordinary mode]
    For $bold(k)=k bold(e)_x$, the wave equation is

    $ mat(
      epsilon_(perp), -i epsilon_(times), 0;
      i epsilon_(times), epsilon_(perp)-N^2, 0;
      0, 0, epsilon_(parallel)-N^2)
      mat(E_x;E_y;E_z)=mat(0;0;0) .$

    The $z$ equation is independent of the $x-y$ block. A nonzero $E_z$
    therefore requires

    $ N^2=epsilon_(parallel) .$

    This is the ordinary mode. Its electric field is parallel to
    $bold(B)_0$ but transverse to $bold(k)$, so the Lorentz force does not
    alter this component.

    #derivation-step[Factor the extraordinary block]
    The determinant of the $x-y$ block is

    $ epsilon_(perp)(epsilon_(perp)-N^2)-epsilon_(times)^2=0 .$

    Solving for the index gives

    $ N_X^2=(epsilon_(perp)^2-epsilon_(times)^2)/epsilon_(perp) .$

    For one electron species, define

    $ epsilon_(perp)=1-omega_(p,e)^2/(omega^2-omega_(c,e)^2) $

    and

    $ epsilon_(times)=-(omega_(c,e) omega_(p,e)^2)/
      (omega (omega^2-omega_(c,e)^2)) .$

    #derivation-step[Expose the upper-hybrid denominator]
    Let $d=omega^2-omega_(c,e)^2$ and $p=omega_(p,e)^2$. Then

    $ N_X^2=((d-p)^2-((omega_(c,e)^2 p^2)/omega^2))/(d(d-p)) .$

    Multiplying the two circular factors and simplifying yields

    $ N_X^2=1-
      (omega_(p,e)^2 (omega^2-omega_(p,e)^2)) /
      (omega^2 (omega^2-omega_(p,e)^2-omega_(c,e)^2)) .$

    The denominator vanishes at

    $ omega_"UH"^2=omega_(p,e)^2+omega_(c,e)^2 ,$

    which is the upper-hybrid resonance.

    #derivation-step[Read the extraordinary polarization]
    The first row of the transverse block is

    $ epsilon_(perp) E_x-i epsilon_(times) E_y=0 .$

    Hence

    $ E_x/E_y=(i epsilon_(times))/epsilon_(perp) ,$

    which is generally elliptical rather than purely linear polarization.]
  )

  #rechenbeispiel[
    Assume a homogeneous, cold, collisionless, fixed-ion electron response
    with perpendicular propagation and uniform $bold(B)_0$.
    For $n_0=qty("1.0e16", "m^-3")$ and $B_0=qty("1.0e-2", "T")$, use
    $omega_(p,e)=qty("5.64e9", "s^-1")$,
    $omega_(c,e)=qty("1.76e9", "s^-1")$, and
    $omega=qty("5.50e9", "s^-1")$. Classify the ordinary and extraordinary
    branches and report the wave number for the propagating branch.

    Numerical result: the ordinary branch is evanescent with
    $alpha_O=qty("4.17", "m^-1")$; the extraordinary branch
    propagates with #normalized-label[$N_X=qty("0.805", "1")$],
    $k_X=qty("14.8", "m^-1")$, and
    $lambda_X=qty("0.425", "m")$.
  ]

  #interpretation(
    [Ordinary does not mean unmagnetized everywhere],
    [The ordinary mode is unaffected by the magnetic field only because its
    electric field is parallel to $bold(B)_0$ in perpendicular propagation.
    Changing the angle mixes the field components and restores the full
    anisotropic determinant.]
  )

  #summary[
    Perpendicular propagation splits into an ordinary branch with
    $N_O^2=epsilon_(parallel)$ and an extraordinary branch with
    $N_X^2=(epsilon_(+)epsilon_(-))/epsilon_(perp)$. The latter is elliptically
    polarized in general and has an upper-hybrid resonance.
  ]

  #knowledge-check((
    (
      question: [Why is the ordinary mode unaffected by the magnetic field in perpendicular propagation?],
      answer: [Its electric field is parallel to $bold(B)_0$, so the perturbed velocity is parallel to the field and the magnetic part of the Lorentz force vanishes.]
    ),
    (
      question: [What distinguishes the extraordinary mode from the ordinary mode?],
      answer: [Its electric field lies in the plane perpendicular to $bold(B)_0$, with components both along and across $bold(k)$. Its index contains both circular factors and its polarization is generally elliptical.]
    ),
    (
      question: [What is the upper-hybrid frequency in the cold fixed-ion model?],
      answer: [It is $omega_"UH"=sqrt(omega_(p,e)^2+omega_(c,e)^2)$. It marks the zero of the extraordinary-mode denominator and the associated cold resonance.]
    ),
    (
      question: [How can a branch be evanescent even when the plasma is collisionless?],
      answer: [A collisionless response can still give $N^2<0$. Then $k$ is imaginary and the spatial solution decays rather than propagates; this is a stopband, not collisional damping.]
    ),
  ))

  #section-title[Oblique propagation and mode coupling] <oblique-magnetized-waves>

  #lead[
    At an arbitrary angle the clean parallel and perpendicular factorizations
    no longer apply. The wave vector has components both along and across the
    magnetic field, so the two electromagnetic branches are generally
    elliptically polarized and coupled through the full three-component wave
    matrix.
  ]

  #objectives((
    [set up the oblique coordinate system and its angle convention],
    [write the full cold magnetized wave matrix],
    [identify the two electromagnetic roots of the Appleton--Hartree form],
    [recover the parallel and perpendicular limits from the oblique model],
  ))

  #unit-ledger[
    The propagation angle $theta$ is dimensionless. Use
    $N=(k c)/omega$, $X_(omega)=omega_(p,e)^2/omega^2$, and
    $Y_(omega)=omega_(c,e)/omega$, all dimensionless. The dimensional wave
    number $k$ is in #unit("m^-1") and frequency $omega$ in
    #unit("s^-1").
  ]

  #assumption(
    [Oblique cold-fluid ordering],
    [Let $bold(B)_0=B_0 bold(e)_z$ and choose
    $bold(k)=k(sin theta bold(e)_x+cos theta bold(e)_z)$, with no $y$
    component. Keep the same homogeneous, cold, collisionless, fixed-ion
    ordering as before. The mode labels are branch labels, not fixed
    polarization labels at every angle.]
  )

  #governing-law(
    [Oblique wave matrix and Appleton--Hartree roots],
    [With $S=epsilon_(perp)$, $D=epsilon_(times)$, and
    $P=epsilon_(parallel)$, the normalized wave matrix is
    $mat(
      S-N^2 cos^2 theta, -i D, N^2 sin theta cos theta;
      i D, S-N^2, 0;
      N^2 sin theta cos theta, 0, P-N^2 sin^2 theta)
      mat(E_x;E_y;E_z)=mat(0;0;0)$.
    Its determinant gives two electromagnetic roots. For one cold electron
    species they can be written in the Appleton--Hartree form
    $N_(plus.minus)^2=1-(X_(omega)) /
      (1-(Y_(omega)^2 sin^2 theta)/(2(1-X_(omega)) )
      plus.minus sqrt(
        ((Y_(omega)^2 sin^2 theta)/(2(1-X_(omega))))^2
        +Y_(omega)^2 cos^2 theta))$.
    The upper sign defines $N_+$ and the lower sign defines $N_-$; their
    polarization and longitudinal content vary continuously with $theta$.]
  )

  Here $S$, $D$, and $P$ are dimensionless dielectric abbreviations; $D$
  is not a diffusion coefficient and $P$ is not pressure. The parameters
  $X_(omega)$ and $Y_(omega)$ use the wave frequency as their reference,
  whereas the earlier $W$ and $Y$ use the plasma frequency. Their relations
  are $X_(omega)=1/W^2$ and $Y_(omega)=Y/W$.

  The two roots give possible wave numbers at a specified frequency and
  angle. For each root, the matrix also determines the relative electric-field
  components. Following those components is necessary to identify a physical
  branch.

  #details(
    [Derivation: oblique matrix and limiting geometry],
    [#derivation-step[Insert the oblique wave vector]
    Use

    $ bold(k)=k(sin theta bold(e)_x+cos theta bold(e)_z) $

    in

    $ bold(k)(bold(k) dot bold(E)_1)-k^2 bold(E)_1
      +omega^2/c^2 bold(epsilon)_(p) dot bold(E)_1=bold(0) .$

    After division by $omega^2/c^2$, the geometric term contributes

    $ -N^2 cos^2 theta E_x+N^2 sin theta cos theta E_z $

    to the $x$ component, $-N^2 E_y$ to the $y$ component, and

    $ N^2 sin theta cos theta E_x-N^2 sin^2 theta E_z $

    to the $z$ component. Adding the dielectric tensor gives the displayed
    oblique matrix.

    #derivation-step[Reduce the determinant to a quadratic]
    Set $Z=N^2$, $a=sin theta$, and $b=cos theta$. Expanding the determinant
    gives

    $ det(M)=(P-Z a^2)((S-Z b^2)(S-Z)-D^2)
      -Z^2 a^2 b^2(S-Z) .$

    Collect terms as

    $ A Z^2-B Z+C=0 ,$

    where

    $ A=S a^2+P b^2, quad
      B=(S^2-D^2) a^2+P S(1+b^2), quad
      C=P(S^2-D^2) .$

    The two roots before specialization are

    $ Z_(plus.minus)=(B plus.minus sqrt(B^2-4 A C))/(2 A) .$

    #derivation-step[Specialize to one cold electron species]
    Insert

    $ S=1-X_(omega)/(1-Y_(omega)^2), quad
      P=1-X_(omega) ,$

    with $D$ of magnitude

    $ (Y_(omega) X_(omega))/(1-Y_(omega)^2) .$

    Since $a^2+b^2=1$, useful identities are

    $ S^2-D^2=((1-X_(omega))^2-Y_(omega)^2)/(1-Y_(omega)^2),
      quad A=S a^2+P b^2 .$

    Substitution into the quadratic formula, extraction of the common factor
    $1-X_(omega)$, and completion of the square in the angle-dependent term
    give the displayed Appleton--Hartree roots. The square-root term measures
    the splitting produced by the field component along the propagation
    direction together with transverse coupling.

    #derivation-step[Check the parallel and perpendicular endpoints]
    For $theta=0$, the matrix separates into the longitudinal factor $P$ and
    circular transverse factors $S plus.minus D$. For $theta=pi/2$, the $z$
    component decouples as the ordinary mode and the $x-y$ block produces the
    extraordinary mode. Without its endpoint polarization, an algebraic root
    can be assigned to the wrong physical branch.]
  )

  #magnetized-oblique-geometry

  #rechenbeispiel[
    Assume a homogeneous, cold, collisionless, fixed-ion electron response
    with uniform $bold(B)_0$ and oblique propagation. Use the
    normalized parameters
    #normalized-label[$Y=omega_(c,e)/omega_(p,e)=qty("0.30", "1")$],
    #normalized-label[$W=omega/omega_(p,e)=qty("1.50", "1")$], and
    $theta=pi/4$ radians. Evaluate the two
    Appleton--Hartree refractive indices.

    Numerical result: #normalized-label[$X_(omega)=qty("0.444", "1")$],
    #normalized-label[$Y_(omega)=qty("0.200", "1")$], and the two roots are
    #normalized-label[$N_+=qty("0.778", "1")$] and
    #normalized-label[$N_-=qty("0.686", "1")$], where the signs follow the
    displayed denominator signs.
  ]

  #interpretation(
    [Oblique modes exchange character],
    [An oblique branch can be mostly transverse at one frequency and mostly
    longitudinal near a resonance or slow-wave region. Naming a mode only by
    its endpoint label hides this conversion; track $N$, polarization, and
    charge response together.]
  )

  #summary[
    Oblique propagation requires the full three-component determinant. The
    Appleton--Hartree roots are the two electromagnetic branches of the cold
    anisotropic response, and the parallel or perpendicular modes appear as
    controlled endpoint limits.
  ]

  #knowledge-check((
    (
      question: [Why can the oblique wave matrix not be reduced to the parallel transverse block?],
      answer: [Both $k_(parallel)$ and $k_(perp)$ are nonzero. The geometric part of Maxwell's equation then couples $E_x$ and $E_z$ in addition to the dielectric coupling of $E_x$ and $E_y$.]
    ),
    (
      question: [How many electromagnetic refractive-index roots does the cold oblique determinant provide?],
      answer: [The determinant is quadratic in $N^2$, so it provides two electromagnetic roots. Their polarization vectors, not only their scalar indices, identify how they connect to the principal modes.]
    ),
    (
      question: [What happens to the oblique roots as the angle approaches zero?],
      answer: [The wave vector becomes parallel to the magnetic field, the longitudinal factor separates, and the two electromagnetic roots approach the circularly polarized parallel branches.]
    ),
    (
      question: [Why should a mode label be accompanied by its propagation angle?],
      answer: [The same branch can change from mostly transverse to partly longitudinal as the angle changes. The polarization and cutoff or resonance locations are angle-dependent even when some principal cutoffs are shared.]
    ),
  ))

  #section-title[Cutoffs, resonances, and controlled limits] <magnetized-limits>

  #lead[
    A cutoff, a resonance, an evanescent interval, and a high-frequency
    vacuum limit are different statements about the same refractive-index
    equation. Each holds only within the model that produced the diagram.
  ]

  #objectives((
    [distinguish $N=0$ cutoffs from divergent resonances],
    [classify propagation using the sign of $N^2$],
    [recover the unmagnetized and vacuum limits],
    [state when warm, collisional, or kinetic corrections are required],
  ))

  #unit-ledger[
    The normalized frequency $W=omega/omega_(p,e)$ and magnetization
    $Y=omega_(c,e)/omega_(p,e)$ are dimensionless. Define the normalized wave
    number $K=(k c)/omega_(p,e)=W N$. The refractive index $N$
    and angle $theta$ are dimensionless; dimensional $k$ is in
    #unit("m^-1"), $omega$ in #unit("s^-1"), and wavelengths in
    #unit("m").
  ]

  #assumption(
    [Validity of the cold model near resonances],
    [The diagnostic uses a homogeneous, collisionless, cold, fixed-ion plasma
    with a uniform magnetic field. Near a cyclotron or upper-hybrid resonance,
    the wavelength can approach the particle orbit scale and the cold fluid
    approximation loses its ordering. Collisions, finite temperature,
    boundaries, and kinetic resonances must then be added explicitly.]
  )

  #definition(
    [Cutoff, resonance, and propagation test],
    [A cutoff is a point where $N^2=0$, so $k=0$. A resonance is a singular
    response where the cold dispersion relation drives $N^2$ to infinity or
    a dielectric denominator to zero. A pole in an individual dielectric
    entry need not survive in every mode: check the complete dispersion
    relation for cancellations. For a real frequency, $N^2>0$ gives a
    real propagating wave number, whereas $N^2<0$ gives an imaginary wave
    number and spatial evanescence. The sign test is necessary but not
    sufficient: one must also check polarization and the approximation's
    scale ordering.]
  )

  #governing-law(
    [Normalized landmarks],
    [For $Y=omega_(c,e)/omega_(p,e)$, the parallel circular cutoffs are
    $W_"cut,s"=(sqrt(Y^2+4)-s Y)/2$.
    The perpendicular extraordinary resonance is
    $W_"UH"=sqrt(1+Y^2)$, while the ordinary cutoff is $W=1$.
    When $Y -> 0$, both circular modes merge into the unmagnetized transverse
    branch $W^2=1+K^2$ from the previous chapter, where $K=W N$.
    At frequencies much larger than both plasma and cyclotron frequencies,
    the propagating electromagnetic branches approach $N -> 1$, or
    equivalently $W approx K$.]
  )

  #details(
    [Derivation: limiting-case checks],
    [#derivation-step[Remove the magnetic field]
    Set $Y=0$ in the circular response. Both eigenvalues become

    $ N^2=1-1/W^2 ,$

    so multiplying by $W^2$ and using $K=W N$ gives the cold
    unmagnetized electromagnetic branch

    $ W^2=1+K^2 .$

    The longitudinal branch remains $W=1$ in the cold fixed-ion limit, so its
    zero group velocity is recovered as well.

    #derivation-step[Check high-frequency, cutoff, and resonance limits]
    As $W -> infinity$, every susceptibility term scales as $W^(-2)$ or
    faster away from a resonance. Therefore

    $ N^2 -> 1, quad omega -> c k .$

    The plasma becomes transparent. A cutoff is found from $N^2=0$ and is a
    finite-frequency, zero-wave-number endpoint. At a resonance, a denominator
    such as $omega(omega-omega_(c,e))$ or
    $omega^2-omega_"UH"^2$ vanishes. Then $N^2$ becomes large and the wave
    length becomes small. The cold response is singular because it has no
    thermal spread, collisions, finite orbit width, or nonlinear saturation.

    #derivation-step[Classify propagation intervals]
    For the extraordinary perpendicular branch, the two circular cutoffs and
    the upper-hybrid resonance divide the frequency axis into propagation and
    stopband intervals. Determine the correct interval by evaluating the sign
    of $N_X^2$ between adjacent landmarks.
    If density or magnetic field varies along a path, a local cutoff can
    reflect or mode-convert a wave. Approximating the wave locally by a plane
    wave additionally requires the background scale length to be long compared
    with the local wavelength; this condition fails near a cutoff where the
    wavelength grows without bound.

    #derivation-step[Return to the physical ordering]
    If $k lambda_D$ is not small, pressure and kinetic dispersion matter. If
    $omega$ is comparable to a collision frequency, the dielectric
    coefficients become complex. If $omega-k v_parallel$ is near zero for a
    significant particle population, kinetic susceptibility and resonant
    damping or growth replace the cold-fluid response.]
  )

  #magnetized-cutoff-map

  #rechenbeispiel[
    Assume a homogeneous, cold, collisionless, fixed-ion electron response
    with uniform $bold(B)_0$. Let
    #normalized-label[$Y=omega_(c,e)/omega_(p,e)=qty("0.30", "1")$].
    Determine the normalized circular cutoffs and upper-hybrid resonance,
    then classify the ordinary and extraordinary modes at
    #normalized-label[$W=qty("0.90", "1")$],
    #normalized-label[$W=qty("1.10", "1")$], and
    #normalized-label[$W=qty("1.30", "1")$].

    Numerical result: #normalized-label[$W_"cut,+"=qty("0.861", "1")$],
    #normalized-label[$W_"cut,-"=qty("1.161", "1")$], and
    #normalized-label[$W_"UH"=qty("1.044", "1")$]. At
    #normalized-label[$W=qty("0.90", "1")$], ordinary is evanescent and
    extraordinary propagates with #normalized-label[$N_X=qty("0.403", "1")$];
    at #normalized-label[$W=qty("1.10", "1")$], ordinary propagates with
    #normalized-label[$N_O=qty("0.417", "1")$] and extraordinary is
    evanescent; at #normalized-label[$W=qty("1.30", "1")$], both propagate
    with #normalized-label[$N_O=qty("0.639", "1")$] and
    #normalized-label[$N_X=qty("0.565", "1")$].
  ]

  #interpretation(
    [Unmagnetized, vacuum, and sign checks],
    [The unmagnetized limit checks the tensor algebra, the vacuum limit checks
    the current response, and the sign of $N^2$ checks propagation. Failure of
    any one of these tests usually indicates a convention, polarization, or
    omitted-physics error before it indicates an exotic new mode.]
  )

  #summary[
    Cutoffs are zero-wave-number boundaries; resonances are singular short-
    wavelength responses. Normalizing by $omega_(p,e)$ and tracking $Y$ makes
    the parallel, perpendicular, unmagnetized, and vacuum limits comparable.
    Near a resonance, the cold model must hand off to warm, collisional, or
    kinetic theory.
  ]

  #knowledge-check((
    (
      question: [What equation identifies a cutoff?],
      answer: [A cutoff is identified by $N^2=0$. The wave number vanishes at the cutoff, unlike a resonance where the refractive index becomes singular.]
    ),
    (
      question: [What is the vacuum limit of the cold magnetized response?],
      answer: [For frequencies much larger than the plasma and cyclotron frequencies, the dielectric response approaches the identity, $N^2$ approaches one, and the dispersion relation approaches $omega=c k$.]
    ),
    (
      question: [Why can the sign of $N^2$ be used to classify propagation?],
      answer: [For a real prescribed frequency and a homogeneous lossless cold model, $N^2>0$ gives real $k$ and oscillatory spatial dependence, while $N^2<0$ gives imaginary $k$ and exponential spatial dependence.]
    ),
    (
      question: [Which corrections should be considered near a cold-plasma resonance?],
      answer: [Finite temperature, collisions, particle-orbit effects, kinetic resonances, boundaries, and nonlinear effects can all regularize or replace the singular cold response. The relevant correction is selected by the ordering of the physical scales.]
    ),
  ))

  #chapter-nav(
    previous: (href: "11-introduction-waves.html", title: [Introduction to waves]),
    next: (href: "13-finite-temperature-waves.html", title: [Finite-temperature waves]),
  )
]
