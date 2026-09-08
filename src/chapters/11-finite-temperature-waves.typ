#import "../theme.typ": *
#import "../figures.typ": collisional-wave-response, ion-wave-branches, warm-longitudinal-modes, mhd-wave-speeds, warm-wave-ordering
#import "@preview/physica:0.9.8": div, grad, pdv, curl
#import "@preview/unify:0.8.1": qty, unit

#let chapter = [
  #page-title[11. Collisions, ions, and finite-temperature effects on magnetized waves] <finite-temperature-waves>

  #lead[
    The cold magnetized response is a useful organizing limit, not a universal
    endpoint. Collisions make the response complex, ion inertia opens
    low-frequency branches, and pressure gives longitudinal waves a spatial
    dispersion. This chapter adds those effects in a controlled order and
    connects the resulting two-fluid branches to warm MHD.
  ]

  #callout(
    [Relax one ordering at a time],
    [A reliable extension of a cold-plasma result starts by naming the small
    parameter that is being released. Compare $nu/omega$, $omega/omega_(c,i)$,
    and $k lambda_D$ before choosing a collisional, two-fluid, warm-fluid, or
    kinetic description.]
  )

  #section-title[Collisional response and wave attenuation] <collisional-waves>

  #lead[
    What changes when particles lose momentum between wave cycles? A simple
    linear drag term is enough to show the essential effect: the cold
    susceptibility becomes complex, the refractive index becomes complex, and
    a propagating wave acquires spatial attenuation.
  ]

  #objectives((
    [insert a linear collision frequency into the time-harmonic momentum equation],
    [interpret the collision term as a complex effective mass],
    [identify the real and imaginary parts of a collisional wave number],
    [state why the effective-mass shortcut fails near a strong resonance],
  ))

  #unit-ledger[
    Gaussian CGS is active. The collision frequency $nu$, wave frequency
    $omega$, and damping rate are in #unit("s^-1"). Masses are in #unit("g"),
    $bold(E)$ is in statvolt per #unit("cm"), $bold(B)$ is in #unit("G"),
    and wave numbers $k_r$ and $k_i$ are in #unit("cm^-1"). The effective
    mass has units #unit("g"), while $N$ and $m_"eff"/m$ are dimensionless.
  ]

  #assumption(
    [Linear drag as a collisional model],
    [Use a homogeneous, cold, magnetized equilibrium and the Fourier convention
    $exp(i (bold(k) dot bold(r)-omega t))$. Represent collisions by a
    velocity-independent drag $-m_s nu_s bold(u)_1$. This is a deliberately
    simple momentum-transfer model; energy exchange, velocity-dependent
    Coulomb operators, and boundary collisions require a more detailed
    kinetic treatment.]
  )

  #definition(
    [Complex effective mass],
    [With the drag term included, write the time-harmonic momentum equation as
    $-i omega m_(s) bold(u)_(s,1)=q_(s)(
      bold(E)_1+(bold(u)_(s,1) times bold(B)_(0))/c)
      -m_(s) nu_s bold(u)_(s,1)$.
    Moving the drag to the left gives
    $-i omega m_"eff",s bold(u)_(s,1)
      =q_(s)(bold(E)_1+(bold(u)_(s,1) times bold(B)_(0))/c)$
    with $m_"eff",s=m_(s)(1+i nu_s/omega)$. The sign of the imaginary part
    follows the stated Fourier convention.]
  )

  #collisional-wave-response

  #governing-law(
    [Complex refractive index],
    [The cold tensor formulas can be reused with $m_s$ replaced by
    $m_"eff",s$ when the drag model is valid. For the
    cyclotron-sensitive electron circular branch, one convenient convention is
    $N_"RH"^2=1-
      omega_(p,e)^2/(omega(omega-omega_(c,e)+i nu_e))$.
    In a homogeneous medium write $N=N_r+i N_i$ and
    $k=(omega N)/c=k_r+i k_i$. The field factor is
    $exp(i k z-i omega t)=exp(i k_r z-i omega t) exp(-k_i z)$,
    so $k_i>0$ is amplitude attenuation and $1/(2 k_i)$ is the intensity
    attenuation length.]
  )

  #rechenbeispiel[
    Use $omega_(p,e)=qty("5.64e9", "s^-1")$,
    $omega=qty("2.00e10", "s^-1")$, and a constant
    $nu_e=qty("1.00e9", "s^-1")$. In the high-frequency weak-collision
    approximation, estimate $k_r$, $k_i$, and the amplitude attenuation length
    for the unmagnetized branch.

    Numerical result: $N approx 0.959+i 2.07 dot 10^(-3)$,
    $k_r approx 6.40 dot 10^(-1) #unit("cm^-1")$,
    $k_i approx 1.38 dot 10^(-3) #unit("cm^-1")$, and the amplitude
    attenuation length is approximately $7.25 dot 10^2 #unit("cm")$.
  ]

  #details(
    [Derivation: drag, complex susceptibility, and attenuation],
    [Start from the linearized momentum equation with drag:
    $-i omega m_(s) bold(u)_(s,1)
      =q_(s)(bold(E)_1+(bold(u)_(s,1) times bold(B)_(0))/c)
      -m_(s) nu_s bold(u)_(s,1)$.
    Add $m_s nu_s bold(u)_(s,1)$ to both sides:
    $(-i omega m_(s)+m_(s) nu_s)bold(u)_(s,1)
      =q_(s)(bold(E)_1+(bold(u)_(s,1) times bold(B)_(0))/c)$.
    Factor the coefficient as
    $-i omega m_(s)(1+i nu_s/omega)
      =-i omega m_"eff",s$.
    Thus the collisional equation has the same algebraic form as the
    collisionless equation with $m_s$ replaced by
    $m_"eff",s=m_(s)(1+i nu_s/omega)$.

    The species plasma-frequency factor becomes
    $(4 pi n_(s,0)q_s^2)/m_"eff",s$, and the signed gyrofrequency becomes
    $(q_s B_0)/(m_"eff",s c)$. Insert both into the cold transverse response.
    For the electron branch whose collisionless denominator is
    $omega(omega-omega_(c,e))$, the two substitutions combine:
    $[omega_(p,e)^2/(1+i nu_e/omega)]/
      [omega(omega-omega_(c,e)/(1+i nu_e/omega))]
      =omega_(p,e)^2/
      [omega(omega-omega_(c,e)+i nu_e)]$.
    This gives the stated collisional circular response.

    Away from resonances and for $nu_e/omega << 1$, the unmagnetized
    susceptibility is
    $omega_(p,e)^2/(omega(omega+i nu_e))
      approx omega_(p,e)^2/omega^2
      (1-i nu_e/omega)$.
    Therefore $N^2$ has a positive imaginary part in the chosen convention.
    Taking the square root gives $N=N_r+i N_i$ with $N_i>0$.
    Since $k=omega N/c$, the plane-wave factor is
    $exp(i(k_r+i k_i)z-i omega t)
      =exp(i k_r z-i omega t)exp(-k_i z)$.
    The amplitude falls by $e^(-1)$ after $1/k_i$, while intensity,
    proportional to amplitude squared, falls by $e^(-1)$ after
    $1/(2k_i)$.

    The shortcut does not determine the collision operator's energy balance
    or velocity dependence. Near a cyclotron or cutoff resonance, the
    denominator is small and even a small $nu_s$ can control the response.
    There the full collisional dielectric tensor, and often a kinetic model,
    must be derived rather than inserted as a perturbative mass replacement.]
  )

  #interpretation(
    [Damping is part of the response],
    [A complex dielectric coefficient does not merely append an after-the-fact
    loss term. It changes phase velocity, polarization, cutoff structure, and
    energy absorption together. The sign of the imaginary part must always be
    read with the declared Fourier convention.]
  )

  #summary[
    Linear drag can be represented by $m_"eff"=m(1+i nu/omega)$ in a
    time-harmonic cold response. The resulting $N$ and $k$ are complex:
    $k_r$ controls phase advance and $k_i$ controls spatial attenuation.
    Near resonances, the shortcut must be replaced by a collision model with
    the correct velocity and energy dependence.
  ]

  #knowledge-check((
    (
      question: [Why does a collision frequency make the refractive index complex?],
      answer: [The drag term changes the coefficient of the time-harmonic velocity from $-i omega m$ to $-i omega m_"eff"$ with complex $m_"eff"$. The susceptibility and therefore the dielectric coefficient acquire an imaginary part.]
    ),
    (
      question: [What determines whether a complex wave number attenuates or grows in space?],
      answer: [With $exp(i k z-i omega t)$ and $k=k_r+i k_i$, the spatial factor is $exp(-k_i z)$. Positive $k_i$ attenuates the forward wave; the sign must be interpreted together with the chosen propagation and Fourier conventions.]
    ),
    (
      question: [Why are collisions especially important near a cyclotron resonance?],
      answer: [The collisionless susceptibility denominator becomes small there. The collisional term then competes directly with the small detuning and can set both the phase and absorption instead of being a small correction.]
    ),
    (
      question: [What information is missing from a constant-drag model?],
      answer: [A constant drag does not describe velocity-dependent scattering, energy exchange, conservation constraints, or kinetic resonances. Those effects require an appropriate collision operator and often a kinetic dielectric calculation.]
    ),
  ))

  #section-title[Ion inertia and low-frequency branches] <ion-magnetized-waves>

  #lead[
    Fixed ions hide the low-frequency part of the spectrum. Once ions are
    allowed to move, their opposite charge and much larger mass add a second
    cyclotron scale. The two circular branches then connect the cold
    electromagnetic modes to shear-Alfvén, whistler-like, and ion-cyclotron
    behavior.
  ]

  #objectives((
    [add ion inertia to the magnetized dielectric response],
    [write the two circular parallel branches for an electron--ion plasma],
    [derive the low-frequency Alfvén limit],
    [explain how ion-cyclotron and whistler continuations arise],
  ))

  #unit-ledger[
    Densities are in #unit("cm^-3"), masses in #unit("g"), and $B_0$ in
    #unit("G"). The positive gyrofrequencies $omega_(c,e)$ and
    $omega_(c,i)$ are in #unit("s^-1"). The Alfvén, sound, and wave phase
    speeds are in #unit("cm/s"); $k$ is in #unit("cm^-1") and wavelengths are
    in #unit("cm"). All refractive indices are dimensionless.
  ]

  #assumption(
    [Two-fluid electron--ion response],
    [Use a neutral, homogeneous hydrogen plasma with $n_(e,0)=n_(i,0)=n_0$,
    no pressure and no collisions for the first branch calculation. Retain
    both electron and ion inertia, use $m_e/m_i << 1$, and keep
    $bold(B)_0=B_0 bold(e)_z$. The labels RH and LH follow the present
    Fourier and viewing convention; they denote circular eigenvalues, not
    universal labels independent of convention.]
  )

  #definition(
    [Two-fluid dielectric coefficients],
    [The species sum gives
    $epsilon_(perp)=1-
      [omega_(p,e)^2/(omega^2-omega_(c,e)^2)
      +omega_(p,i)^2/(omega^2-omega_(c,i)^2)]$,
    $epsilon_(times)=
      -(omega_(c,e) omega_(p,e)^2)/(omega (omega^2-omega_(c,e)^2))
      +(omega_(c,i) omega_(p,i)^2)/(omega (omega^2-omega_(c,i)^2))$,
    and
    $epsilon_(parallel)=1-
      [omega_(p,e)^2+omega_(p,i)^2]/omega^2$.
    This is the signed-$Omega_s$ convention from the previous chapter: for
    $bold(B)_0$ along positive $z$, the electron contribution is negative and
    the ion contribution is positive. Charge neutrality and singly charged
    species imply
    $omega_(p,i)^2/omega_(p,e)^2=m_e/m_i
      =omega_(c,i)/omega_(c,e)$.]
  )

  #ion-wave-branches

  #governing-law(
    [Circular branches and the Alfvén limit],
    [For parallel propagation, the two circular branches can be written,
    to leading order in $m_e/m_i$, as
    $N_"RH"^2 approx 1-
      omega_(p,e)^2/
      ((omega+omega_(c,i))(omega-omega_(c,e)))$
    and
    $N_"LH"^2 approx 1-
      omega_(p,e)^2/
      ((omega-omega_(c,i))(omega+omega_(c,e)))$.
    For $omega << omega_(c,i)$ both approach
    $N^2 approx 1+
      omega_(p,e)^2/(omega_(c,e)omega_(c,i))
      =c^2/v_A^2$,
    where
    $v_A=B_0/sqrt(4 pi rho_0)
      =(c sqrt(omega_(c,e) omega_(c,i)))/omega_(p,e)$
    and $rho_0 approx n_0 m_i$. Thus $omega approx k v_A$ at low
    frequency.]
  )

  #rechenbeispiel[
    For a hydrogen plasma use $n_0=qty("1.0e10", "cm^-3")$,
    $B_0=qty("100", "G")$, $m_i=qty("1.673e-24", "g")$,
    and $e=qty("4.803e-10", "statcoulomb")$. Consider a parallel
    low-frequency wave at $omega=0.10 omega_(c,i)$. Determine
    $omega_(c,i)$, $v_A$, $k approx omega/v_A$, and the wavelength.

    Numerical result: $omega_(c,i)=9.58 dot 10^5 #unit("s^-1")$,
    $v_A=2.18 dot 10^8 #unit("cm/s")$,
    $k=4.40 dot 10^(-4) #unit("cm^-1")$, and
    $lambda=1.43 dot 10^4 #unit("cm")$.
  ]

  #details(
    [Derivation: species sum, circular factors, and low frequency],
    [For each species, the cold transverse velocity response from the previous
    chapter is inserted into $bold(j)_1=q_s n_(s,0) bold(u)_(s,1)$.
    For electrons use the positive magnitude $omega_(c,e)$ and for ions use
    $omega_(c,i)>0$. The transverse current sum gives
    $epsilon_(perp)$ and $epsilon_(times)$ with the electron and ion terms
    carrying opposite signs in the off-diagonal coefficient. Parallel motion
    has no magnetic force, so the parallel response is the sum of the two
    unmagnetized susceptibilities.

    For parallel propagation the transverse determinant factors as
    $N^2=epsilon_(perp)+epsilon_(times)$ or
    $N^2=epsilon_(perp)-epsilon_(times)$.
    Combine the electron and ion terms in either factor. For example, the
    branch with an electron denominator $(omega-omega_(c,e))$ has the exact
    species-sum structure
    $1-
      omega_(p,e)^2/[omega(omega-omega_(c,e))]
      -omega_(p,i)^2/[omega(omega+omega_(c,i))]$.
    Use
    $omega_(p,i)^2/omega_(p,e)^2
      =omega_(c,i)/omega_(c,e)$ and put the terms over a common denominator.
    The numerator is
    $omega_(p,e)^2(1+omega_(c,i)/omega_(c,e))$.
    Since $omega_(c,i)/omega_(c,e)=m_e/m_i$ is small, retaining the
    ion factors in the denominator while dropping this small numerator
    correction gives
    $N_"RH"^2 approx 1-
      omega_(p,e)^2/
      ((omega+omega_(c,i))(omega-omega_(c,e)))$.
    Interchanging the two circular senses gives the LH expression.

    In the limit $omega << omega_(c,i) << omega_(c,e)$, both denominators
    have the leading product $-omega_(c,e)omega_(c,i)$. Therefore
    $N^2 approx 1+
      omega_(p,e)^2/(omega_(c,e) omega_(c,i))$.
    In a dense nonrelativistic plasma this term is much larger than one.
    Use
    $(omega_(c,e)omega_(c,i))/(omega_(p,e)^2)
      =B_0^2/(4 pi n_0m_i c^2)$
    to identify
    $N^2 approx c^2/[B_0^2/(4 pi n_0m_i)]
      =c^2/v_A^2$.
    Since $N=(k c)/omega$, this gives $omega/k approx v_A$.

    The RH branch is regular through the positive ion-cyclotron frequency
    under this convention and develops a whistler-like continuation as the
    frequency rises. The LH branch has a denominator that vanishes at
    $omega=omega_(c,i)$ and therefore supports an ion-cyclotron-sensitive
    continuation. At frequencies far above both cyclotron scales, the ion
    correction becomes negligible and the fixed-ion electron branches are
    recovered.]
  )

  #interpretation(
    [Low-frequency circular modes can become linear],
    [The two circular eigenvalues remain the convenient algebraic basis, but
    their low-frequency indices become nearly equal. Equal counter-rotating
    components can therefore combine into a linearly polarized shear-Alfvén
    perturbation. Ion inertia is the physics that makes this low-frequency
    branch possible.]
  )

  #summary[
    Mobile ions add $omega_(c,i)$ and $omega_(p,i)$ to the dielectric response.
    The parallel circular branches approach $omega=k v_A$ at low frequency,
    then separate into whistler-like and ion-cyclotron continuations. The
    fixed-ion cold result is recovered only above the ion-inertia scale.
  ]

  #knowledge-check((
    (
      question: [Why do ions matter at frequencies far below the electron cyclotron frequency?],
      answer: [Their response is controlled by the much smaller ion gyrofrequency. At frequencies comparable to or below $omega_(c,i)$, ion inertia and ion current are no longer negligible in the transverse dielectric tensor.]
    ),
    (
      question: [How does the Alfvén speed arise from the parallel circular dispersion?],
      answer: [In the low-frequency limit the circular refractive index becomes $N^2 approx c^2/v_A^2$. Combining this with $N=(k c)/omega$ gives the nondispersive relation $omega=k v_A$.]
    ),
    (
      question: [What distinguishes the ion-cyclotron and whistler-like continuations?],
      answer: [Their circular denominators contain opposite ion and electron cyclotron factors. One branch is sensitive to the positive ion-cyclotron resonance, while the other continues smoothly into a whistler-like branch under the chosen convention.]
    ),
    (
      question: [Why can the RH and LH labels not be used without a convention?],
      answer: [Handedness depends on the Fourier sign, propagation direction, and viewing direction. The physical eigenvalues are invariant, but the names assigned to the two circular polarizations can exchange.]
    ),
  ))

  #section-title[Finite-temperature longitudinal waves] <warm-longitudinal-waves>

  #lead[
    Pressure gradients are invisible to a perfectly cold plasma. Restoring a
    finite temperature makes density perturbations communicate through the
    fluid, so plasma oscillations acquire a $k$-dependent frequency and a
    low-frequency ion-acoustic branch appears when both species move.
  ]

  #objectives((
    [insert an adiabatic or isothermal pressure closure into the linear response],
    [derive the warm longitudinal dielectric coefficient],
    [recover the warm plasma-oscillation dispersion relation],
    [derive the low-frequency ion-acoustic speed from the two-fluid response],
  ))

  #unit-ledger[
    Temperature is represented by the energy $k_B T$ in #unit("erg");
    number density is in #unit("cm^-3"), Debye length $lambda_D$ is in
    #unit("cm"), thermal or sound speeds are in #unit("cm/s"), $k$ is in
    #unit("cm^-1"), and frequencies are in #unit("s^-1"). The normalized
    combination $k lambda_D$ and the ratio $omega/omega_p$ are dimensionless.
  ]

  #assumption(
    [Warm-fluid pressure closure],
    [Use a homogeneous unmagnetized or principal-direction perturbation with
    $p_(s,1)=gamma_s k_B T_s n_(s,1)$. Define
    $c_s^2=(gamma_s k_B T_s)/m_s$. The closure is local and fluid-like; it
    requires $k lambda_D$ to remain small enough that kinetic phase mixing is
    not the leading correction.]
  )

  #definition(
    [Warm longitudinal response],
    [For a longitudinal perturbation, the pressure-corrected susceptibility is
    $epsilon_(parallel)=1-
      sum_s omega_(p,s)^2/
      (omega^2-k^2 c_s^2)$.
    For fixed ions and warm electrons this gives
    $omega^2=omega_(p,e)^2+k^2 c_(s,e)^2
      =omega_(p,e)^2(1+gamma_e k^2 lambda_(D,e)^2)$,
    with
    $lambda_(D,e)^2=(k_B T_e)/(4 pi n_0e^2)$ for an isothermal electron
    reference.]
  )

  #warm-longitudinal-modes

  #governing-law(
    [Warm plasma oscillation and ion acoustic wave],
    [The fixed-ion warm branch is
    $omega^2=omega_(p,e)^2+k^2 c_(s,e)^2$.
    When both species move, the longitudinal condition is
    $1-
      omega_(p,e)^2/(omega^2-k^2 c_(s,e)^2)
      -omega_(p,i)^2/(omega^2-k^2 c_(s,i)^2)=0$.
    Its low-frequency root has
    $omega^2 approx
      (k^2 (omega_(p,e)^2 c_(s,i)^2
      +omega_(p,i)^2 c_(s,e)^2))/
      (omega_(p,e)^2+omega_(p,i)^2)$.
    For a hydrogen plasma this is approximately
    $omega^2=(k^2 gamma k_(B)(T_e+T_i))/m_i$ when the same adiabatic
    convention is used for both species.]
  )

  #rechenbeispiel[
    Let $n_0=qty("1.0e10", "cm^-3")$, $T_e=10 #unit("eV")$,
    $gamma_e=1$, and use the electron constants from the earlier examples.
    At $k lambda_(D,e)=0.80$, determine $lambda_(D,e)$, $k$, and the
    normalized warm plasma-oscillation frequency.

    Numerical result: $lambda_(D,e)=2.35 dot 10^(-2) #unit("cm")$,
    $k=3.40 dot 10^1 #unit("cm^-1")$, and
    $omega/omega_(p,e)=1.28$.
  ]

  #details(
    [Derivation: pressure response and the two longitudinal roots],
    [The linearized continuity equation is
    $pdv(n_(s,1),t)+n_(s,0) div_(bold(r))(bold(u)_(s,1))=0$.
    For a plane wave with longitudinal velocity, it becomes
    $-i omega n_(s,1)+i n_(s,0) k u_(s,1)=0$,
    hence
    $n_(s,1)/n_(s,0)=(k u_(s,1))/omega$.

    The pressure perturbation is
    $p_(s,1)=gamma_s k_B T_s n_(s,1)$, so the longitudinal momentum equation is
    $-i omega m_s u_(s,1)
      =q_s E_1-(i k gamma_s k_B T_s n_(s,1))/n_(s,0)$.
    Substitute the continuity relation:
    $-i omega m_s u_(s,1)
      =q_s E_1-i (k^2 m_s c_s^2 u_(s,1))/omega$.
    Move the pressure term to the left and multiply by $i$:
    $m_(s)(omega-(k^2 c_s^2)/omega)u_(s,1)
      =i q_s E_1$.
    Therefore
    $u_(s,1)=(i q_s omega E_1)/
      [m_(s)(omega^2-k^2c_s^2)]$.

    The current or charge response is proportional to
    $q_s n_(s,0)u_(s,1)$. Inserting it into
    $bold(epsilon) dot bold(E)=bold(E)+((4 pi i)/omega)bold(j)$
    gives the species susceptibility
    $-omega_(p,s)^2/(omega^2-k^2c_s^2)$.
    Summing species yields the displayed $epsilon_(parallel)$.

    For fixed ions, set the electron-only coefficient to zero:
    $1-omega_(p,e)^2/(omega^2-k^2c_(s,e)^2)=0$.
    Multiply by the denominator:
    $omega^2-k^2c_(s,e)^2-omega_(p,e)^2=0$.
    This is the warm plasma-oscillation branch. Using
    $lambda_(D,e)^2=(k_B T_e)/(4 pi n_0e^2)$ and
    $c_(s,e)^2=(gamma_e k_B T_e)/m_e$ gives
    $c_(s,e)^2/omega_(p,e)^2=gamma_e lambda_(D,e)^2$.

    For two species, multiply the longitudinal condition by both
    denominators:
    $(omega^2-k^2c_(s,e)^2)(omega^2-k^2c_(s,i)^2)
      -omega_(p,e)^2(omega^2-k^2c_(s,i)^2)
      -omega_(p,i)^2(omega^2-k^2c_(s,e)^2)=0$.
    This is a quadratic equation in $omega^2$.
    For the low-frequency root, terms of order $k^4c_(s,e)^2c_(s,i)^2$
    are smaller than the plasma-frequency terms. Retain the terms of order
    $omega^2$ and $k^2$:
    $-(omega_(p,e)^2+omega_(p,i)^2)omega^2
      +k^2[omega_(p,e)^2c_(s,i)^2
      +omega_(p,i)^2c_(s,e)^2] approx 0$.
    Solving gives the displayed ion-acoustic speed. Charge neutrality gives
    $omega_(p,i)^2/omega_(p,e)^2=m_e/m_i$, so
    $c_"ia"^2 approx c_(s,i)^2+(m_e/m_i)c_(s,e)^2
      =(gamma_i k_B T_i)/m_i+(gamma_e k_B T_e)/m_i$.
    The high-frequency root approaches the electron plasma-oscillation
    branch.]
  )

  #interpretation(
    [Temperature creates a communication length],
    [The cold plasma frequency is local because pressure is absent. The warm
    term couples neighboring density elements over a Debye-scale wavelength.
    Once $k lambda_D$ is not small, the fluid branch must be compared with
    kinetic phase mixing rather than extrapolated indefinitely.]
  )

  #summary[
    A pressure closure changes the longitudinal response from
    $omega=omega_p$ to $omega^2=omega_p^2+k^2c_s^2$. With mobile ions, the
    same response contains a low-frequency ion-acoustic root. The relevant
    ordering is measured by $k lambda_D$ and by the ratio of electron and ion
    plasma frequencies.
  ]

  #knowledge-check((
    (
      question: [Why does a cold plasma oscillation have no wave-number dependence?],
      answer: [The cold momentum equation contains no pressure gradient. Without a spatial restoring term, the longitudinal charge displacement oscillates locally at the plasma frequency.]
    ),
    (
      question: [Which term gives the warm plasma-oscillation branch its dispersion?],
      answer: [The pressure perturbation $-grad p_(s,1)$ couples density variation to velocity through continuity, producing the $k^2 c_s^2$ term in the denominator.]
    ),
    (
      question: [Why does the two-fluid warm system have an ion-acoustic root?],
      answer: [Electrons and ions can move together nearly quasineutrally at low frequency. Their pressure forces provide the restoring force while the ion mass supplies most of the inertia.]
    ),
    (
      question: [When should the warm-fluid longitudinal branch be checked against kinetic theory?],
      answer: [When $k lambda_D$ is no longer small or when the phase velocity approaches a substantial particle population. Then velocity-space resonance and phase mixing can be as important as fluid pressure.]
    ),
  ))

  #section-title[Warm transverse waves and magnetosonic motion] <warm-magnetosonic-waves>

  #lead[
    Pressure also modifies transverse wave motion, but the correction depends
    on geometry. Near the upper-hybrid frequency it adds a warm spatial
    correction to the extraordinary branch. At much lower frequency, mobile
    ions and nearly ideal conductivity reorganize the wave into MHD motion:
    magnetic tension gives shear-Alfvén waves, while pressure and magnetic
    compression combine into magnetosonic waves.
  ]

  #objectives((
    [identify the warm upper-hybrid correction in perpendicular propagation],
    [derive shear-Alfvén and compressional restoring forces from warm MHD],
    [distinguish field-line tension from pressure compression],
    [connect the wave speeds to the single-fluid variables],
  ))

  #unit-ledger[
    In Gaussian CGS, $rho_0$ is in #unit("g/cm^3"), pressure is in
    #unit("dyn/cm^2"), $B_0$ is in #unit("G"), and $v_A$, $v_s$, and $v_m$
    are in #unit("cm/s"). The wave number is in #unit("cm^-1") and angular
    frequency in #unit("s^-1"). The ratios $omega/omega_(c,i)$ and
    $k lambda_D$ are dimensionless.
  ]

  #assumption(
    [Warm-fluid and ideal-MHD limits],
    [Use the warm-fluid pressure closure for the upper-hybrid correction.
    For the low-frequency MHD derivation assume quasineutrality,
    $omega << omega_(c,i)$, $k lambda_D << 1$, a single bulk velocity, and
    sufficiently large conductivity that the ideal induction law applies.
    Use an adiabatic closure $p_1=v_s^2 rho_1$ with
    $v_s^2=(gamma p_0)/rho_0$.]
  )

  #definition(
    [Alfvén, sound, and magnetosonic speeds],
    [Define
    $v_A=B_0/sqrt(4 pi rho_0)$,
    $v_s=sqrt((gamma p_0)/rho_0)$, and
    $v_m=sqrt(v_A^2+v_s^2)$
    for perpendicular compressional motion. $v_A$ is magnetic tension
    divided by mass inertia, $v_s$ is the pressure-wave speed, and $v_m$ is
    their warm perpendicular combination.]
  )

  #mhd-wave-speeds

  #animation(
    "../media/magnetosonic-waves.mp4",
    "The animation compares three normalized schematic patterns. A sound wave is shown as pressure or density compression, a shear Alfvén wave as transverse displacement of otherwise nearly parallel magnetic field lines, and a magnetosonic wave as combined pressure and magnetic compression. The patterns are illustrative and do not represent dimensional simulation data.",
    caption: [
      Warm magnetized-wave patterns: pressure compression, shear-Alfvén field
      displacement, and compressional magnetosonic motion. The animation is a
      schematic visual companion to $v_m^2=v_A^2+v_s^2$.
    ],
    poster: "../media/magnetosonic-waves.png",
  )

  #governing-law(
    [Warm upper-hybrid and MHD branches],
    [Near the perpendicular upper-hybrid branch, the warm-fluid correction
    gives the local relation
    $omega^2=omega_"UH"^2+k^2 c_(s,e)^2$
    in the simple electron pressure ordering. At low frequency, ideal MHD
    gives the shear-Alfvén branch
    $omega^2=k_"parallel"^2 v_A^2$
    and the perpendicular compressional branch
    $omega^2=k_"perp"^2(v_A^2+v_s^2)$.
    The latter is often called the magnetosonic or magnetosonic-Alfvén
    branch.]
  )

  #rechenbeispiel[
    For $n_0=qty("1.0e10", "cm^-3")$, $B_0=qty("100", "G")$,
    $T_e=T_i=10 #unit("eV")$, and isothermal
    $gamma_e=gamma_i=1$, determine $v_A$, the total-pressure sound speed
    $v_s$, and $v_m$. For $k=qty("1.0e-5", "cm^-1")$, report the parallel
    shear-Alfvén and perpendicular magnetosonic frequencies.

    Numerical result: $v_A=2.18 dot 10^8 #unit("cm/s")$,
    $v_s=4.38 dot 10^6 #unit("cm/s")$, and
    $v_m=2.18 dot 10^8 #unit("cm/s")$ to the shown precision.
    The two example frequencies are
    $omega_A=2.18 dot 10^3 #unit("s^-1")$ and
    $omega_m=2.18 dot 10^3 #unit("s^-1")$.
  ]

  #details(
    [Derivation: warm upper hybrid and magnetosonic restoring forces],
    [For a perpendicular electrostatic-scale perturbation, take
    $bold(k)=k bold(e)_x$ and retain the electron pressure term in the
    $x$ momentum equation. Continuity gives
    $n_(e,1)/n_0=(k u_(e,1,x))/omega$.
    The linear transverse momentum equations have the same Lorentz coupling
    as in the cold tensor, while the pressure term adds
    $-(i k c_(s,e)^2 n_(e,1))/n_0$
    to the $x$ equation. Eliminate $u_(e,1,y)$ using the $y$ equation and
    eliminate $n_(e,1)$ using continuity. The denominator of the
    $x$-directed susceptibility is shifted from
    $omega^2-omega_(c,e)^2$ to
    $omega^2-k^2c_(s,e)^2-omega_(c,e)^2$.
    The perpendicular charge response also contributes the electron plasma
    restoring term. Setting the warm perpendicular response to zero therefore
    gives
    $omega^2=omega_(p,e)^2+omega_(c,e)^2+k^2c_(s,e)^2
      =omega_"UH"^2+k^2c_(s,e)^2$.
    This is a warm-fluid local approximation near the upper-hybrid branch;
    the full electromagnetic warm tensor contains additional polarization
    terms.

    For the low-frequency one-fluid limit, start from continuity,
    $pdv(rho,t)+div_(bold(r))(rho bold(u))=0$,
    the ideal induction equation,
    $pdv(bold(B),t)=curl_(bold(r))(bold(u)times bold(B))$,
    and the CGS MHD momentum equation
    $rho pdv(bold(u),t)
      =-grad_(bold(r))p+
      [curl_(bold(B))times bold(B)]/(4 pi)$.
    Linearize about $rho=rho_0$, $p=p_0$, $bold(B)=B_0 bold(e)_z$,
    and take a plane wave with $bold(k)=k bold(e)_x$ and
    $bold(u)_1=u_x bold(e)_x$. Continuity gives
    $-i omega rho_1+i k rho_0u_x=0$,
    so
    $rho_1=(rho_0 k u_x)/omega$.
    The pressure closure gives
    $p_1=v_s^2rho_1$.

    The induction equation gives
    $-i omega B_(1,z)=-i k B_0u_x$,
    hence
    $B_(1,z)=(B_0 k u_x)/omega$.
    The $x$ component of the linearized momentum equation is
    $-i omega rho_0u_x
      =-i k p_1-i (k B_0B_(1,z))/(4 pi)$.
    Substitute both perturbations:
    $omega rho_(0)u_x
      =k v_s^2 rho_(0)((k u_x)/omega)
      +(k B_0)/(4 pi)((B_0 k u_x)/omega)$.
    Multiply by $omega/(rho_0u_x)$:
    $omega^2=k^2[v_s^2+B_0^2/(4 pi rho_0)]
      =k^(2) (v_s^2+v_A^2)$.
    Therefore the perpendicular compressional speed is
    $v_m=sqrt(v_A^2+v_s^2)$.

    For a shear perturbation with
    $bold(k)=k_"parallel" bold(e)_z$,
    the pressure and density perturbations vanish to first order. The
    induction and transverse momentum equations retain only magnetic tension:
    $pdv(bold(u)_perp,t,2)
      =v_A^2 pdv(bold(u)_perp,z,2)$.
    A plane wave then satisfies
    $omega^2=k_"parallel"^2v_A^2$.
    The difference between this equation and the compressional equation is
    geometric: tension bends field lines, while perpendicular compression
    changes both density and magnetic-field strength.]
  )

  #interpretation(
    [The same field can support different restoring forces],
    [Shear-Alfvén motion bends field lines with little compression. Magnetosonic
    motion compresses the field and the fluid, so thermal pressure adds to
    magnetic pressure. The appropriate branch is selected by propagation
    angle and frequency ordering, not by the presence of a magnetic field
    alone.]
  )

  #summary[
    Warm pressure shifts the upper-hybrid branch and supplies the sound speed.
    In the low-frequency ideal-MHD limit, magnetic tension gives shear-Alfvén
    waves and pressure plus magnetic compression gives
    $v_m=sqrt(v_A^2+v_s^2)$. These are controlled limits of the same
    multi-species response.
  ]

  #knowledge-check((
    (
      question: [Why does finite temperature affect the upper-hybrid branch?],
      answer: [The perpendicular density perturbation produces a pressure gradient. Continuity converts it into a $k$-dependent restoring term, shifting the cold upper-hybrid frequency by a warm-fluid contribution.]
    ),
    (
      question: [Why is the shear-Alfvén wave not strongly modified by pressure in the ideal low-frequency limit?],
      answer: [Its transverse field-line displacement is nearly incompressible, so the first-order density and pressure perturbations vanish. Magnetic tension supplies the leading restoring force.]
    ),
    (
      question: [What is added when the magnetosonic speed is formed from $v_A$ and $v_s$?],
      answer: [Magnetic compression contributes $v_A^2$ and thermal pressure contributes $v_s^2$ to the squared speed. For perpendicular compression their restoring forces add.]
    ),
    (
      question: [Which assumptions are needed to use the ideal-MHD wave equations?],
      answer: [The plasma must be quasineutral and strongly conducting, ions and electrons must share a bulk velocity, the frequency must be below the ion-inertia scale, and the perturbation must remain on fluid scales.]
    ),
  ))

  #section-title[Ordering map: from cold waves to warm MHD] <finite-temperature-ordering>

  #lead[
    The preceding sections are not competing descriptions. They are branches
    of a model-selection map. This final section collects the dimensionless
    orderings that tell us whether a cold, collisional, two-fluid, warm-fluid,
    MHD, or kinetic calculation is justified.
  ]

  #objectives((
    [define the collision, ion-inertia, thermal, and mass-ratio orderings],
    [recover the cold fixed-ion result as a controlled limit],
    [identify when a two-fluid or MHD description is preferable],
    [recognize the scale overlap that requires kinetic theory],
  ))

  #unit-ledger[
    The ordering parameters $C=nu/omega$, $I=omega/omega_(c,i)$,
    $K=k lambda_D$, and $M=m_e/m_i$ are dimensionless. Dimensional
    $nu$, $omega$, and $omega_(c,i)$ are in #unit("s^-1"); $k$ is in
    #unit("cm^-1"); and $lambda_D$ and the thermal gyroradius
    $rho_s=c_s/omega_(c,s)$ are in #unit("cm"). Particle and wave speeds are
    in #unit("cm/s").
  ]

  #assumption(
    [One model boundary at a time],
    [Use the cold magnetized response as the reference model. Release one
    ordering while holding the others explicit: collisions through $C$, ion
    motion through $I$, pressure through $K$, and species separation through
    $M$. If more than one parameter is order unity, retain all corresponding
    terms before making a branch identification.]
  )

  #definition(
    [Model-selection ordering],
    [The collisionless cold fixed-ion model requires
    $C << 1$, $I >> 1$, and $K << 1$ for the mode under study.
    If $C$ is not small, use a complex collisional response. If $I$ is not
    large, retain ion inertia and use a two-fluid or MHD reduction. If $K$
    is not small, retain pressure and test the warm-fluid result against
    kinetic scales. The small mass ratio $M<<1$ justifies electron-dominated
    plasma frequencies but does not justify removing ion motion at low
    frequency.]
  )

  #warm-wave-ordering

  #governing-law(
    [Controlled limits],
    [The branches must satisfy four checks:
    (1) $nu -> 0$ makes $N$ real and recovers the collisionless cold tensor;
    (2) $m_i -> infinity$ or $I -> infinity$ recovers the fixed-ion branches;
    (3) $T_s -> 0$ or $K -> 0$ removes the pressure correction; and
    (4) $omega << omega_(c,i)$ with high conductivity reduces the
    two-fluid system to MHD, with $v_A$ and $v_m$ as the leading speeds.
    If $k rho_s$ is not small, $omega-k_"parallel"v_(parallel)$ approaches
    zero, or the distribution is strongly non-Maxwellian, a kinetic
    susceptibility is required even when the fluid equations look closed.]
  )

  #rechenbeispiel[
    Classify two model orderings. Case A has
    $C=0.02$, $I=50$, $K=0.05$, and $M=1/1836$.
    Case B has $C=0.30$, $I=0.40$, $K=0.80$, and the same $M$.
    State the simplest justified description and the first correction to add
    in each case.

    Numerical result: Case A is collisionless cold fixed-ion to leading order;
    the first corrections are collisional damping, ion inertia, and warm
    dispersion in the displayed order. Case B requires a collisional
    two-fluid warm model; a kinetic check is recommended because all three
    primary orderings are no longer asymptotically small.
  ]

  #details(
    [Derivation: recovering the neighboring models],
    [Begin with the collisional effective mass
    $m_"eff"=m(1+i nu/omega)$. Let $nu -> 0$. Then
    $m_"eff" -> m$, every dielectric coefficient becomes real in the
    collisionless model, and the complex wave number reduces to the cold
    magnetized result.

    Next take the fixed-ion limit. For a singly charged electron--ion plasma,
    $omega_(c,i)/omega_(c,e)=m_e/m_i=M$ and
    $omega_(p,i)^2/omega_(p,e)^2=M$. At fixed $omega$ with
    $omega >> omega_(c,i)$, the ion denominators are regular and the ion
    susceptibility is smaller by $M$ than the electron susceptibility.
    Sending $M -> 0$ therefore removes the ion contribution and recovers the
    fixed-ion tensor. This argument is not valid when $omega$ is also reduced
    to the ion-cyclotron scale, because then the ion denominator is no longer
    an order-one factor.

    For the warm limit, the pressure-corrected species susceptibility contains
    $omega^2-k^2c_s^2$ instead of $omega^2$. Taking $T_s -> 0$ sends
    $c_s -> 0$ and returns the cold denominator. Conversely, if
    $k lambda_D$ becomes order unity, the pressure term changes the
    longitudinal root by an order-one amount and cannot be treated as a
    perturbation.

    Finally take $omega << omega_(c,i)$ while maintaining high conductivity
    and quasineutrality. Electron and ion transverse drifts are tied by the
    common electric field, their relative current produces the magnetic force,
    and the weighted momentum sum gives
    $rho_0 pdv(bold(u),t)
      =-grad p+[curl bold(B) times bold(B)]/(4 pi)$.
    The induction equation becomes
    $pdv(bold(B),t)=curl(bold(u)times bold(B))$.
    Linearizing these equations gives the shear-Alfvén and magnetosonic
    dispersions derived in the previous section.

    A fluid closure fails when a wave samples unresolved particle scales.
    The Debye-scale condition is $k lambda_D <<1$ for cold quasineutral
    motion. Magnetized finite-Larmor-radius corrections require
    $k_perp rho_s <<1$. Resonant kinetic corrections become important near
    $omega-k_"parallel"v_(parallel)=0$ or a cyclotron harmonic. These are
    independent checks: satisfying one does not imply that the others hold.]
  )

  #interpretation(
    [A limit is a diagnostic, not a slogan],
    [Every reduction should be reversible in a stated asymptotic limit. If a
    proposed branch does not recover its cold, fixed-ion, or MHD endpoint, the
    first suspects are a sign convention, an omitted current, or an
    inconsistent scale ordering.]
  )

  #summary[
    Collisions, ions, and temperature extend the cold magnetized spectrum in
    different directions. The dimensionless orderings $C$, $I$, and $K$ make
    those extensions explicit. The correct endpoint is selected by scale
    separation; overlapping scales require a kinetic response.
  ]

  #knowledge-check((
    (
      question: [Which limit removes collisional attenuation?],
      answer: [Taking $nu/omega -> 0$ makes the effective mass real, removes the imaginary part of the susceptibility, and recovers a real refractive index away from other resonances.]
    ),
    (
      question: [Why does the fixed-ion limit fail at low frequency?],
      answer: [Reducing the frequency to the ion-cyclotron scale makes the ion response resonant or order one even though $m_e/m_i$ is small. The small mass ratio alone does not remove ion inertia.]
    ),
    (
      question: [What does $k lambda_D$ measure in the model hierarchy?],
      answer: [It compares the perturbation wavelength with the Debye shielding length. Small $k lambda_D$ supports a cold or quasineutral fluid ordering; order-one values make pressure and kinetic dispersion important.]
    ),
    (
      question: [What is the first sign that a fluid branch needs a kinetic replacement?],
      answer: [A wave-particle or cyclotron resonance, finite-Larmor-radius scale, strong non-Maxwellian distribution, or unresolved Debye-scale structure invalidates the assumed fluid closure. The relevant condition must be checked explicitly.]
    ),
  ))

  #chapter-nav(
    previous: (href: "10-cold-magnetized-waves.html", title: [Cold magnetized waves]),
    next: (href: "12-hot-plasma-waves.html", title: [Hot plasma waves]),
  )
]
