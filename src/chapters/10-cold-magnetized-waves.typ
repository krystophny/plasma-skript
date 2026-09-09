#import "../theme.typ": *
#import "../figures.typ": magnetized-dielectric, magnetized-parallel-dispersion, magnetized-oblique-geometry, magnetized-cutoff-map
#import "@preview/physica:0.9.8": div, grad, pdv, curl
#import "@preview/unify:0.8.1": qty, unit

#let chapter = [
  #page-title[10. Waves in cold magnetized plasmas] <cold-magnetized-waves>

  #lead[
    A static magnetic field turns the isotropic plasma response into a tensor.
    This chapter derives that tensor from the cold-fluid momentum equation and
    uses it to organize parallel, perpendicular, and oblique wave propagation.
    The central habit is to carry the propagation direction, polarization, and
    frequency ordering together.
  ]

  #callout(
    [The magnetic field selects a basis],
    [A cold magnetized plasma does not merely shift one scalar dielectric
    constant. It couples the two transverse field components, leaves the
    parallel response distinct, and therefore creates different wave branches
    for different polarization and propagation direction.]
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
    Gaussian CGS is active. Number density $n_s$ is in #unit("cm^-3"),
    charge $q_s$ is in #unit("statcoulomb"), mass $m_s$ is in #unit("g"),
    $bold(E)$ is in statvolt per #unit("cm"), $bold(B)$ is in #unit("G"),
    and $bold(j)$ is in statcoulomb per #unit("cm^2") per #unit("s").
    Frequencies $omega$ and $Omega_s$ are in #unit("s^-1"), wave number $k$
    is in #unit("cm^-1"), and $c$ is in #unit("cm/s"). The dielectric
    coefficients and refractive index $N=(k c)/omega$ are dimensionless.
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
    $Omega_s=(q_s B_0)/(m_s c)$ and
    $omega_(p,s)^2=(4 pi n_(s,0) q_s^2)/m_s$.
    For electrons it is useful to reserve
    $omega_(c,e)=(abs(q_e) B_0)/(m_e c)>0$
    for the cyclotron-frequency magnitude. The sign of $q_e$ remains in the
    transverse polarization convention.]
  )

  #definition(
    [Cold dielectric tensor],
    [The current response is represented by
    $bold(epsilon)_(p) dot bold(E)_1=bold(E)_1+((4 pi i)/omega) bold(j)_1$,
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
    [The linearized cold momentum equation is
    $-i omega m_(s) bold(u)_(s,1)=q_(s)(
      bold(E)_1+(bold(u)_(s,1) times bold(B)_0)/c)$.
    With $bold(B)_0=B_0 bold(e)_z$, its transverse components are
    $-i omega bold(u)_(s,1,x)-Omega_s bold(u)_(s,1,y)
      =(q_s/m_s) bold(E)_(1,x)$ and
    $Omega_s bold(u)_(s,1,x)-i omega bold(u)_(s,1,y)
      =(q_s/m_s) bold(E)_(1,y)$.
    The parallel component is
    $-i omega bold(u)_(s,1,z)=(q_s/m_s) bold(E)_(1,z)$.

    Inverting the transverse two-by-two system gives
    $bold(u)_(s,1,x)=((i q_s omega)/(m_(s)(omega^2-Omega_s^2))) bold(E)_(1,x)
      -(q_s Omega_s/(m_(s)(omega^2-Omega_s^2))) bold(E)_(1,y)$ and
    $bold(u)_(s,1,y)=(q_s Omega_s/(m_(s)(omega^2-Omega_s^2))) bold(E)_(1,x)
      +((i q_s omega)/(m_(s)(omega^2-Omega_s^2))) bold(E)_(1,y)$.
    Multiplication by $q_s n_(s,0)$ and summation produces $bold(j)_1$.
    Inserting the result into
    $bold(epsilon)_(p) dot bold(E)_1=bold(E)_1+((4 pi i)/omega) bold(j)_1$
    yields the three coefficients shown above. The transverse entries are
    coupled because the Lorentz force rotates the velocity in the $x-y$
    plane; the $z$ motion has no magnetic force.

    Faraday's and Ampere's laws in Fourier form are
    $bold(k) times bold(E)_1=(omega bold(B)_1)/c$ and
    $bold(k) times bold(B)_1=-(omega bold(E)_1)/c
      -(4 pi i bold(j)_1)/c$.
    Substitute the first into the second, eliminate $bold(j)_1$ with the
    dielectric definition, and use
    $bold(k) times (bold(k) times bold(E)_1)
      =bold(k)(bold(k) dot bold(E)_1)-k^2 bold(E)_1$.
    A nonzero field amplitude then requires the determinant of the resulting
    wave matrix to vanish. This is why the dielectric tensor is the bridge
    between particle response and the dispersion branches.]
  )

  #magnetized-dielectric

  #rechenbeispiel[
    For a fixed-ion hydrogen plasma use
    $n_0=qty("1.0e10", "cm^-3")$, $B_0=qty("100", "G")$,
    $e=qty("4.803e-10", "statcoulomb")$,
    $m_e=qty("9.109e-28", "g")$, and
    $c=qty("2.998e10", "cm/s")$. Determine the electron plasma frequency,
    the electron cyclotron-frequency magnitude, and their ratio.

    Numerical result: $omega_(p,e)=5.64 dot 10^9 #unit("s^-1")$,
    $omega_(c,e)=1.76 dot 10^9 #unit("s^-1")$, and
    $omega_(c,e)/omega_(p,e)=0.312$.
  ]

  #rechenbeispiel[
    At angular frequency $omega=qty("1.00e10", "s^-1")$, use the same
    fixed-ion plasma and constants as above. Take the electron charge to be
    $q_(e)=-e$ and evaluate the cold dielectric coefficients
    $epsilon_(perp)$, $epsilon_(times)$, and $epsilon_(parallel)$.

    Assumptions: homogeneous, cold, collisionless electron response with
    $bold(B)_0$ along $z$ and Gaussian-CGS conventions.

    Target: report the three dimensionless entries of the dielectric tensor.

    Numerical result: $epsilon_(perp)=qty("0.672", "1")$,
    $epsilon_(times)=qty("-5.78e-2", "1")$, and
    $epsilon_(parallel)=qty("0.682", "1")$.
  ]

  #interpretation(
    [Anisotropy is a response, not a label],
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
    $k$ is in #unit("cm^-1"), $omega$ and $omega_(c,e)$ are in
    #unit("s^-1"), and phase or group velocities are in #unit("cm/s").
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
    $bold(E)_(1,y)=-i s bold(E)_(1,x)$.
    The corresponding refractive indices are
    $N_(s)^2=epsilon_(s)=epsilon_(perp)-s epsilon_(times)
      =1-omega_(p,e)^2/(omega(omega+s omega_(c,e)))$.
    Thus the $s=+1$ branch has the lower positive-frequency cutoff, while
    the $s=-1$ branch has a cyclotron-sensitive denominator at
    $omega=omega_(c,e)$.]
  )

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
    [For parallel propagation, divide the transverse part of the wave matrix
    by $omega^2/c^2$ and write it as
    $mat(
      epsilon_(perp)-N^2, -i epsilon_(times), 0;
      i epsilon_(times), epsilon_(perp)-N^2, 0;
      0, 0, epsilon_(parallel)) mat(E_x; E_y; E_z)=mat(0;0;0)$.
    The longitudinal factor gives $epsilon_(parallel)=0$. The transverse
    determinant is
    $(epsilon_(perp)-N^2)^2-epsilon_(times)^2=0$,
    so $N^2=epsilon_(perp)+epsilon_(times)$ or
    $N^2=epsilon_(perp)-epsilon_(times)$.

    For an electron, the signed gyrofrequency is negative when $B_0$ points
    along positive $z$. Rewriting the two eigenvalues using the positive
    magnitude $omega_(c,e)$ and the basis
    $bold(E)_(1,y)=-i s bold(E)_(1,x)$ gives
    $N_(s)^2=epsilon_(perp)-s epsilon_(times)
      =1-omega_(p,e)^2/(omega(omega+s omega_(c,e)))$.
    Setting this index to zero gives
    $omega^2+s omega_(c,e) omega-omega_(p,e)^2=0$.
    The positive root is the cutoff written above. The $s=-1$ denominator
    vanishes at the electron cyclotron frequency, so the cold response becomes
    singular there. A finite-temperature or collisional model is required
    before interpreting the singular limit.

    A linearly polarized wave is the equal-amplitude sum of the two circular
    eigenmodes. After distance $L$ their relative phase is
    $(k_+-k_-)L$. The major axis of the resulting linear polarization rotates
    by half that relative phase:
    $theta_F=((k_+-k_-)L)/2$.
    If the plasma varies slowly along the ray, replace the constant difference
    by $theta_F=(integral (k_+(z)-k_-(z)) d z)/2$.]
  )

  #magnetized-parallel-dispersion

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
    "Two circular eigenmode phasors rotate at different normalized phase rates. Their equal-amplitude superposition is represented by transverse polarization arrows at successive positions along the propagation direction, and the arrows rotate progressively with distance. The animation is a deterministic illustration of Faraday rotation, not a measurement or a ray-tracing calculation.",
    caption: [
      Faraday rotation: a linearly polarized wave can be decomposed into two
      circular eigenmodes. Because the magnetic field gives them different
      wave numbers, their relative phase changes along the path and the
      polarization plane rotates.
    ],
    poster: "../media/magnetized-polarization.png",
  )

  #rechenbeispiel[
    For the fixed-ion plasma with
    $omega_(p,e)=qty("5.64e9", "s^-1")$,
    $omega_(c,e)=qty("1.76e9", "s^-1")$, and a parallel wave with
    $omega=qty("2.00e10", "s^-1")$ crossing a path of
    $L=qty("10", "cm")$, determine the two refractive indices and the
    Faraday-rotation angle $theta_F=((k_+-k_-)L)/2$.

    Numerical result: $N_+=0.963$, $N_-=0.955$, and
    $theta_F=2.47 dot 10^-2$ rad $=1.42 degree$.
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
    plasma response. The extraordinary mode lives in the coupled transverse
    plane and contains a characteristic upper-hybrid resonance.
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
    #unit("cm^-1"), $omega$ in #unit("s^-1"), and wavelengths in #unit("cm").
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
    $E_x/E_y=i epsilon_(times)/epsilon_(perp)$, away from zeros of the
    denominator.]
  )

  #governing-law(
    [Ordinary and extraordinary branches],
    [The ordinary branch obeys
    $omega^2=omega_(p,e)^2+c^2 k^2$ and has the same cutoff as the cold
    unmagnetized transverse wave. The extraordinary branch obeys
    $N_X^2=epsilon_(+) epsilon_(-)/epsilon_(perp)$,
    with circular factors $epsilon_(s)$ from the parallel problem. Its
    denominator vanishes at $omega=omega_"UH"$, so the cold wave number
    diverges at the upper-hybrid resonance.]
  )

  #details(
    [Derivation: perpendicular factorization],
    [For $bold(k)=k bold(e)_x$, the wave equation becomes
    $mat(
      epsilon_(perp), -i epsilon_(times), 0;
      i epsilon_(times), epsilon_(perp)-N^2, 0;
      0, 0, epsilon_(parallel)-N^2) mat(E_x;E_y;E_z)=mat(0;0;0)$.
    The $z$ equation is independent of the $x-y$ block. A nonzero $E_z$
    therefore requires $N^2=epsilon_(parallel)$, which is the ordinary mode.
    Since $E_z$ is parallel to $bold(B)_0$ but transverse to $bold(k)$, the
    Lorentz force does not alter this response.

    The determinant of the $x-y$ block is
    $epsilon_(perp)(epsilon_(perp)-N^2)-epsilon_(times)^2=0$.
    Solving for $N^2$ gives
    $N_X^2=(epsilon_(perp)^2-epsilon_(times)^2)/epsilon_(perp)$.
    For one electron species, write
    $epsilon_(perp)=1-omega_(p,e)^2/(omega^2-omega_(c,e)^2)$ and
    $epsilon_(times)=-(omega_(c,e) omega_(p,e)^2)/
      (omega(omega^2-omega_(c,e)^2))$
    after choosing the positive-magnitude convention for the eigenvalue
    labels. Multiplying the two circular factors and simplifying yields
    $N_X^2=1-
      (omega_(p,e)^2 (omega^2-omega_(p,e)^2)) /
      (omega^2 (omega^2-omega_(p,e)^2-omega_(c,e)^2))$.
    The denominator is zero at $omega_"UH"^2=omega_(p,e)^2+omega_(c,e)^2$.
    The first row of the transverse block gives
    $epsilon_(perp) E_x-i epsilon_(times) E_y=0$,
    hence $E_x/E_y=i epsilon_(times)/epsilon_(perp)$ and the generally
    elliptical extraordinary polarization.]
  )

  #rechenbeispiel[
    For $n_0=qty("1.0e10", "cm^-3")$ and $B_0=qty("100", "G")$, use
    $omega_(p,e)=qty("5.64e9", "s^-1")$,
    $omega_(c,e)=qty("1.76e9", "s^-1")$, and
    $omega=qty("5.50e9", "s^-1")$. Classify the ordinary and extraordinary
    branches and report the wave number for the propagating branch.

    Numerical result: the ordinary branch is evanescent with
    $alpha_O=4.17 dot 10^-2 #unit("cm^-1")$; the extraordinary branch
    propagates with $N_X=0.805$, $k_X=1.48 dot 10^-1 #unit("cm^-1")$,
    and $lambda_X=42.5 #unit("cm")$.
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
    $N_X^2=epsilon_(+)epsilon_(-)/epsilon_(perp)$. The latter is elliptically
    polarized in general and has an upper-hybrid resonance.
  ]

  #knowledge-check((
    (
      question: [Why is the ordinary mode unaffected by the magnetic field in perpendicular propagation?],
      answer: [Its electric field is parallel to $bold(B)_0$, so the perturbed velocity is parallel to the field and the magnetic part of the Lorentz force vanishes.]
    ),
    (
      question: [What distinguishes the extraordinary mode from the ordinary mode?],
      answer: [The extraordinary mode has electric-field components in the coupled transverse plane. Its index contains both circular factors and its polarization is generally elliptical.]
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
    number $k$ is in #unit("cm^-1") and frequency $omega$ in
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

  #details(
    [Derivation: oblique matrix and limiting geometry],
    [Insert
    $bold(k)=k(sin theta bold(e)_x+cos theta bold(e)_z)$
    into
    $bold(k)(bold(k) dot bold(E)_1)-k^2 bold(E)_1
      +omega^2/c^2 bold(epsilon)_(p) dot bold(E)_1=bold(0)$.
    The $x$ component of the geometric term contributes
    $-N^2 cos^2 theta E_x+N^2 sin theta cos theta E_z$ after division by
    $omega^2/c^2$. The $y$ component contributes $-N^2 E_y$, and the $z$
    component contributes
    $N^2 sin theta cos theta E_x-N^2 sin^2 theta E_z$.
    Adding the dielectric tensor gives the displayed matrix.

    The determinant is a quadratic polynomial in $N^2$. Insert the single
    electron coefficients
    $S=1-X_(omega)/(1-Y_(omega)^2)$,
    $D$ with magnitude
    $(Y_(omega) X_(omega))/(1-Y_(omega)^2)$, and
    $P=1-X_(omega)$. Collect the terms in $N^4$, $N^2$, and the constant
    term, then use the quadratic formula. Completing the square in the
    angle-dependent coefficient produces the two Appleton--Hartree roots.
    The square-root term measures the splitting produced by the component of
    the magnetic field along the propagation direction together with the
    transverse coupling.

    For $theta=0$, the matrix separates into the longitudinal factor $P$ and
    the circular transverse factors $S plus.minus D$. For $theta=pi/2$, the
    $z$ component decouples as the ordinary mode and the $x-y$ block produces
    the extraordinary mode. These checks are essential because an algebraic
    root without the correct endpoint polarization can be assigned to the
    wrong physical branch.]
  )

  #magnetized-oblique-geometry

  #rechenbeispiel[
    Use the normalized parameters $Y=omega_(c,e)/omega_(p,e)=0.30$,
    $W=omega/omega_(p,e)=1.50$, and $theta=pi/4$. Evaluate the two
    Appleton--Hartree refractive indices.

    Numerical result: $X_(omega)=0.444$, $Y_(omega)=0.200$, and the two roots
    are $N_+=0.778$ and $N_-=0.686$, where the signs follow the displayed
    denominator signs.
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
      answer: [Both $k_"parallel"$ and $k_"perp"$ are nonzero. The geometric part of Maxwell's equation then couples $E_x$ and $E_z$ in addition to the dielectric coupling of $E_x$ and $E_y$.]
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
    Dispersion diagrams are useful only when their limits are read with the
    model attached. A cutoff, a resonance, an evanescent interval, and a
    high-frequency vacuum limit are different statements about the same
    refractive-index equation. This section turns those statements into a
    reusable diagnostic workflow.
  ]

  #objectives((
    [distinguish $N=0$ cutoffs from divergent resonances],
    [classify propagation using the sign of $N^2$],
    [recover the unmagnetized and vacuum limits],
    [state when warm, collisional, or kinetic corrections are required],
  ))

  #unit-ledger[
    The normalized frequency $W=omega/omega_(p,e)$ and magnetization
    $Y=omega_(c,e)/omega_(p,e)$ are dimensionless. The refractive index $N$
    and angle $theta$ are dimensionless; dimensional $k$ is in
    #unit("cm^-1"), $omega$ in #unit("s^-1"), and wavelengths in
    #unit("cm").
  ]

  #assumption(
    [Interpret branches only within the cold model],
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
    a dielectric denominator to zero. For a real frequency, $N^2>0$ gives a
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
    branch $W^2=1+N^2$ from the previous chapter. When $W$ is much larger
    than unity, all cold branches approach the vacuum relation $W=N$ where
    they propagate.]
  )

  #details(
    [Derivation: limiting-case checks],
    [Set $Y=0$ in the circular response. Both eigenvalues become
    $N^2=1-1/W^2$, which is the cold unmagnetized electromagnetic branch
    $W^2=1+N^2$. The longitudinal branch remains $W=1$ in the cold fixed-ion
    limit, so its zero group velocity is recovered as well.

    At high frequency, $W -> infinity$, every susceptibility term scales as
    $W^(-2)$ or faster away from a resonance. Thus $N^2 -> 1$ and
    $omega -> c k$: the plasma becomes transparent to the wave. At a cutoff,
    solve $N^2=0$; the resulting finite frequency is a zero-wave-number
    endpoint. At a resonance, a denominator such as
    $omega(omega-omega_(c,e))$ or
    $omega^2-omega_"UH"^2$ vanishes; $N^2$ becomes large and the wave
    wavelength becomes small. The cold model then predicts a singular response
    because it has no thermal spread, collisions, finite orbit width, or
    nonlinear saturation to regularize the resonance.

    For the extraordinary perpendicular branch, the two circular cutoffs and
    the upper-hybrid resonance divide the frequency axis into propagation and
    stopband intervals. The correct interval is found by evaluating the sign
    of $N_X^2$ between adjacent landmarks, not by guessing from the names of
    the modes. If density or magnetic field varies along a path, the local
    cutoff can reflect or mode-convert a wave; a WKB treatment additionally
    requires the background scale length to be long compared with the local
    wavelength.

    Finally, check the physical scale ordering. If $k lambda_D$ is not small,
    pressure and kinetic dispersion matter. If $omega$ is comparable to a
    collision frequency, the dielectric coefficients become complex. If
    $omega-k v_parallel$ is near zero for a significant particle population,
    the kinetic susceptibility and resonant damping or growth replace the
    cold-fluid response.]
  )

  #magnetized-cutoff-map

  #rechenbeispiel[
    Let $Y=omega_(c,e)/omega_(p,e)=0.30$. Determine the normalized circular
    cutoffs and upper-hybrid resonance, then classify the ordinary and
    extraordinary modes at $W=0.90$, $W=1.10$, and $W=1.30$.

    Numerical result: $W_"cut,+"=0.861$, $W_"cut,-"=1.161$, and
    $W_"UH"=1.044$. At $W=0.90$, ordinary is evanescent and extraordinary
    propagates with $N_X=0.403$; at $W=1.10$, ordinary propagates with
    $N_O=0.417$ and extraordinary is evanescent; at $W=1.30$, both propagate
    with $N_O=0.639$ and $N_X=0.565$.
  ]

  #interpretation(
    [A limit check is a physical unit test],
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
    previous: (href: "09-introduction-waves.html", title: [Introduction to waves]),
    next: (href: "11-finite-temperature-waves.html", title: [Finite-temperature waves]),
  )
]
