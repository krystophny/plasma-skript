#import "../theme.typ": *
#import "../figures.typ": collisional-wave-response, ion-wave-branches, warm-longitudinal-modes, mhd-wave-speeds, warm-wave-ordering
#import "@preview/physica:0.9.8": div, grad, pdv, curl
#import "@preview/unify:0.8.1": qty, unit

#let chapter = [
  #page-title[13. Collisions, ions, and finite-temperature effects on magnetized waves] <finite-temperature-waves>

  #lead[
    The cold magnetized response is an organizing limit. Collisions make the response complex, ion inertia opens
    low-frequency branches, and pressure gives longitudinal waves a spatial
    dispersion. This chapter adds those effects in a controlled order and
    connects the resulting two-fluid branches to warm MHD, following
    @bittencourt2004.
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
    What changes when particles lose momentum between wave cycles? With a
    linear drag term, the cold susceptibility becomes complex, the refractive index becomes complex, and
    a propagating wave acquires spatial attenuation.
  ]

  #objectives((
    [insert a linear collision frequency into the time-harmonic momentum equation],
    [interpret the collision term as a complex effective mass],
    [identify the real and imaginary parts of a collisional wave number],
    [distinguish the exact drag substitution from a weak-collision expansion],
  ))

  #unit-ledger[
    The damping rate is in #unit("s^-1"), and wave numbers $k_r$ and $k_i$ are
    in #unit("m^-1"). The effective mass has units #unit("kg"), while $N$ and
    $m_"eff"/m$ are dimensionless.
  ]

  #assumption(
    [Linear drag as a collisional model],
    [Use a homogeneous, cold, magnetized equilibrium and the Fourier convention
    $exp(i (bold(k) dot bold(r)-omega t))$. Represent collisions by a
    velocity-independent drag $-m_s nu_s bold(u)_1$ against a stationary
    background. If the collision partner also moves, its velocity must enter
    the relative drag. In this momentum-transfer model, energy exchange, velocity-dependent
    Coulomb operators, and boundary collisions require a more detailed
    kinetic treatment.]
  )

  #definition(
    [Complex effective mass],
    [With the drag term included, write the time-harmonic momentum equation as
    $-i omega m_(s) bold(u)_(s,1)=q_(s)(
      bold(E)_1+bold(u)_(s,1) times bold(B)_(0))
      -m_(s) nu_s bold(u)_(s,1)$.
    Moving the drag to the left gives
    $-i omega m_("eff",s) bold(u)_(s,1)
      =q_(s)(bold(E)_1+bold(u)_(s,1) times bold(B)_(0))$
    with $m_("eff",s)=m_(s)(1+(i nu_s)/omega)$. The sign of the imaginary part
    follows the stated Fourier convention. For nonzero $omega$, this is an
    exact algebraic rewrite of the stated constant-drag equation, including
    near cyclotron resonance. The complex mass is a way to combine inertia
    and drag; the physical particle mass remains $m_s$.]
  )

  #governing-law(
    [Complex refractive index],
    [The cold tensor formulas can be reused with $m_s$ replaced by
    $m_("eff",s)$ when the drag model is valid. For the
    cyclotron-sensitive electron circular branch, one convenient convention is
    $N_"RH"^2=1-
      omega_(p,e)^2/(omega(omega-omega_(c,e)+i nu_e))$.
    For a wave driven at real positive $omega$ in a homogeneous medium,
    write $N=N_r+i N_i$ and
    $k=(omega N)/c=k_r+i k_i$. The field factor is
    $exp(i k z-i omega t)=exp(i k_r z-i omega t) exp(-k_i z)$,
    so $k_i>0$ is amplitude attenuation and $1/(2 k_i)$ is the intensity
    attenuation length along positive $z$. This describes spatial decay;
    temporal damping instead uses a complex frequency at real wave number.]
  )

  #details(
    [Derivation: drag, complex susceptibility, and attenuation],
    [#derivation-step[Introduce the effective mass]
    Start from the linearized momentum equation with drag:

    $ -i omega m_(s) bold(u)_(s,1)
        =q_(s)(bold(E)_1+bold(u)_(s,1) times bold(B)_(0))
        -m_(s) nu_s bold(u)_(s,1) .$

    Move the drag term to the left:

    $ (-i omega m_(s)+m_(s) nu_s)bold(u)_(s,1)
        =q_(s)(bold(E)_1+bold(u)_(s,1) times bold(B)_(0)) .$

    Factor the coefficient:

    $ -i omega m_(s)(1+(i nu_s)/omega)
        =-i omega m_("eff",s) ,$

    where

    $ m_("eff",s)=m_(s)(1+(i nu_s)/omega) .$

    #derivation-step[Insert the effective parameters into the cold response]
    The species plasma-frequency factor becomes
    $(n_(s,0)q_s^2)/(epsilon_0 m_("eff",s))$, and the signed gyrofrequency becomes
    $(q_s B_0)/m_("eff",s)$. Insert both into the cold transverse response.
    For the electron branch whose collisionless denominator is
    $omega(omega-omega_(c,e))$, the two substitutions combine to

    $ [omega_(p,e)^2/(1+(i nu_e)/omega)]/
        [omega(omega-omega_(c,e)/(1+(i nu_e)/omega))]
        =omega_(p,e)^2/
        [omega(omega-omega_(c,e)+i nu_e)] .$

    This gives the stated collisional circular response.

    #derivation-step[Extract weak attenuation]
    Away from resonances and for $nu_e/omega << 1$, the unmagnetized
    susceptibility is

    $ omega_(p,e)^2/(omega(omega+i nu_e))
        approx omega_(p,e)^2/omega^2
        (1-(i nu_e)/omega) .$

    Therefore $N^2$ has a positive imaginary part in the chosen convention.
    Taking the square root gives $N=N_r+i N_i$ with $N_i>0$. Since
    $k=(omega N)/c,$

    $ exp(i(k_r+i k_i)z-i omega t)
        =exp(i k_r z-i omega t)exp(-k_i z) .$

    The amplitude falls by $e^(-1)$ after $1/k_i$, while intensity, which is
    proportional to amplitude squared, falls by $e^(-1)$ after $1/(2 k_i)$.

    #derivation-step[State the validity boundary]
    The effective-mass substitution remains exact for constant linear drag.
    An expansion of the circular denominator instead requires
    $nu_e << abs(omega-omega_(c,e))$, not merely $nu_e << omega$.
    Near resonance retain the full complex denominator. Near a cutoff,
    expanding its square root also fails if the imaginary correction is
    comparable to the real $N^2$. A direct solution of the same drag tensor
    gives the same result as the effective-mass substitution. A more realistic
    collision operator is needed only when the physical model must include
    velocity dependence, energy exchange, or coupled species momentum.]
  )

  #collisional-wave-response

  #rechenbeispiel[
    Assume a homogeneous, cold, unmagnetized, weakly collisional, fixed-ion
    electron plasma with linear momentum drag and the stated Fourier
    convention. Use
    $omega_(p,e)=qty("5.64e9", "s^-1")$,
    $omega=qty("2.00e10", "s^-1")$, and a constant
    $nu_e=qty("1.00e9", "s^-1")$. In the high-frequency weak-collision
    approximation, estimate the effective-mass ratio $m_"eff",e/m_e$,
    $k_r$, $k_i$, and the amplitude attenuation length for the unmagnetized
    branch.

    Numerical result:
    #normalized-label[$m_"eff",e/m_e=qty("1.00", "1")+i qty("5.00e-2", "1")$],
    #normalized-label[$N approx qty("0.959", "1")+i qty("2.07e-3", "1")$],
    $k_r approx qty("64.0", "m^-1")$,
    $k_i approx qty("1.38e-1", "m^-1")$, and the amplitude attenuation
    length is approximately $qty("7.23", "m")$.
  ]

  #interpretation(
    [Damping is part of the response],
    [A complex dielectric coefficient does not merely append an after-the-fact
    loss term. It changes phase velocity, polarization, cutoff structure, and
    energy absorption together. The sign of the imaginary part must always be
    read with the declared Fourier convention.]
  )

  #summary[
    Linear drag can be represented by $m_"eff"=m(1+(i nu)/omega)$ in a
    time-harmonic cold response. The resulting $N$ and $k$ are complex:
    $k_r$ controls phase advance and $k_i$ controls spatial attenuation.
    Near resonances retain the full drag response; a weak-collision expansion
    can fail even though the effective-mass rewrite remains exact. The drag
    model's physical adequacy must be assessed separately.
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
    The Alfvén, sound, and wave phase speeds are in #unit("m/s"). All
    refractive indices are dimensionless.
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
      approx c^2/v_A^2$,
    where
    $v_A=B_0/sqrt(mu_0 rho_0)
      =(c sqrt(omega_(c,e) omega_(c,i)))/omega_(p,e)$
    and $rho_0 approx n_0 m_i$. The last approximation also requires
    $v_A << c$, so the added unity is negligible. In this nonrelativistic
    limit, $omega approx k v_A$ at low frequency.]
  )

  #details(
    [Derivation: species sum, circular factors, and low frequency],
    [#derivation-step[Sum the species responses]
    Insert the cold transverse velocity response from the previous chapter
    into

    $ bold(j)_1=sum_s q_s n_(s,0) bold(u)_(s,1) .$

    Use the positive magnitudes $omega_(c,e)$ and $omega_(c,i)>0$ for
    electrons and ions. The transverse current sum defines
    $epsilon_(perp)$ and $epsilon_(times)$; the two species carry opposite
    signs in the off-diagonal coefficient. Parallel motion feels no magnetic
    force, so its response is the sum of the unmagnetized susceptibilities.

    #derivation-step[Factor the parallel-propagation determinant]
    For parallel propagation, the transverse determinant factors as

    $ N^2=epsilon_(perp)+epsilon_(times) $ \
    $ N^2=epsilon_(perp)-epsilon_(times) .$

    Consider the factor with an electron denominator
    $(omega-omega_(c,e))$. Its exact species-sum structure is

    $ 1-omega_(p,e)^2/(omega (omega-omega_(c,e)))
      -omega_(p,i)^2/(omega (omega+omega_(c,i))) .$

    Use

    $ omega_(p,i)^2/omega_(p,e)^2
      =omega_(c,i)/omega_(c,e) ,$

    and put the terms over a common denominator. The numerator is

    $ omega_(p,e)^2(1+omega_(c,i)/omega_(c,e)) .$

    Since $omega_(c,i)/omega_(c,e)=m_e/m_i$ is small, retain the ion factors
    in the denominator but drop this small numerator correction:

    $ N_"RH"^2 approx 1-
      omega_(p,e)^2/((omega+omega_(c,i))(omega-omega_(c,e))) .$

    Interchanging the two circular senses gives the LH expression.

    #derivation-step[Take the low-frequency limit]
    When $omega << omega_(c,i) << omega_(c,e)$, both denominators have the
    leading product $-omega_(c,e)omega_(c,i)$. Therefore

    $ N^2 approx 1+omega_(p,e)^2/(omega_(c,e)omega_(c,i)) .$

    In a dense nonrelativistic plasma this term is much larger than one. Use

    $ (omega_(c,e)omega_(c,i))/omega_(p,e)^2
      =(epsilon_0 B_0^2)/(n_0 m_i)
      =B_0^2/(mu_0 n_0 m_i c^2) .$

    It follows that

    $ N^2 approx c^2/[B_0^2/(mu_0 n_0 m_i)]=c^2/v_A^2 .$

    Since $N=(k c)/omega$, the low-frequency phase speed is
    $omega/k approx v_A.$

    #derivation-step[Interpret the two circular branches]
    Under this convention, the RH branch is regular through the positive
    ion-cyclotron frequency and develops a whistler-like continuation as the
    frequency rises. The LH branch has a denominator that vanishes at
    $omega=omega_(c,i)$ and therefore supports an ion-cyclotron-sensitive
    continuation. Far above both cyclotron scales, the ion correction becomes
    negligible and the fixed-ion electron branches are recovered.]
  )

  #ion-wave-branches

  #rechenbeispiel[
    Assume a homogeneous, cold, collisionless, two-fluid hydrogen plasma with
    both species mobile and parallel low-frequency propagation.
    For the neutral hydrogen plasma use $n_0=qty("1.0e16", "m^-3")$,
    $B_0=qty("1.0e-2", "T")$, $m_i=qty("1.673e-27", "kg")$,
    and $e=qty("1.602e-19", "C")$. Consider a parallel
    low-frequency wave at
    #normalized-label[$omega/omega_(c,i)=qty("0.10", "1")$]. Determine
    $omega_(c,i)$, $v_A$, $k approx omega/v_A$, and the wavelength.

    Numerical result: $omega_(c,i)=qty("9.58e5", "s^-1")$,
    $v_A=qty("2.18e6", "m/s")$,
    $k=qty("4.39e-2", "m^-1")$, and
    $lambda=qty("1.43e2", "m")$.
  ]

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
    The normalized combination $k lambda_D$ and the ratio $omega/omega_p$ are
    dimensionless.
  ]

  #assumption(
    [Warm-fluid pressure closure],
    [Use a homogeneous unmagnetized longitudinal perturbation, or one with
    both $bold(k)$ and $bold(E)_1$ parallel to $bold(B)_0$, with
    $p_(s,1)=gamma_s k_B T_s n_(s,1)$. Define
    $c_s^2=(gamma_s k_B T_s)/m_s$. Here $s$ labels a species; below,
    $c_(s,e)$ and $c_(s,i)$ denote the electron and ion pressure-response
    speeds. They are distinct from the collective ion-acoustic speed.
    The closure is local and fluid-like; it
    requires $k lambda_D$ to remain small enough that kinetic phase mixing is
    not the leading correction. Small $k lambda_D$ alone does not choose
    $gamma_s$: the closure must match the thermal response. For collisionless
    Maxwellian Langmuir waves the leading warm correction has $gamma_e=3$;
    an isothermal closure is a different model. Perpendicular longitudinal
    response retains the cyclotron term derived in the next section.]
  )

  #definition(
    [Warm longitudinal response],
    [For a longitudinal perturbation, the pressure-corrected dielectric coefficient is
    $epsilon_(parallel)=1-
      sum_s omega_(p,s)^2/
      (omega^2-k^2 c_s^2)$.
    For fixed ions and warm electrons this gives
    $omega^2=omega_(p,e)^2+k^2 c_(s,e)^2
      =omega_(p,e)^2(1+gamma_e k^2 lambda_(D,e)^2)$,
    with
    $lambda_(D,e)^2=(epsilon_0 k_B T_e)/(n_0e^2)$ for an isothermal electron
    reference.]
  )

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

  #details(
    [Derivation: pressure response and the two longitudinal roots],
    [#derivation-step[Obtain the species response]
    The linearized continuity equation is

    $ pdv(n_(s,1),t)+n_(s,0) div(bold(u)_(s,1))=0 .$

    For a longitudinal plane wave it becomes

    $ -i omega n_(s,1)+i n_(s,0) k u_(s,1)=0 ,$

    hence

    $ n_(s,1)/n_(s,0)=(k u_(s,1))/omega .$

    The pressure perturbation is

    $ p_(s,1)=gamma_s k_B T_s n_(s,1) .$

    The longitudinal momentum equation is therefore

    $ -i omega m_s u_(s,1)
      =q_s E_1-(i k gamma_s k_B T_s n_(s,1))/n_(s,0) .$

    Use continuity and define
    $c_s^2=(gamma_s k_B T_s)/m_s:$

    $ -i omega m_s u_(s,1)
      =q_s E_1-i (k^2 m_s c_s^2 u_(s,1))/omega .$

    After moving the pressure term to the left and multiplying by $i$,

    $ m_s (omega-(k^2 c_s^2)/omega)u_(s,1)=i q_s E_1 .$

    Thus

    $ u_(s,1)=(i q_s omega E_1)/(m_s (omega^2-k^2 c_s^2)) .$

    #derivation-step[Construct the longitudinal susceptibility]
    The current or charge response is proportional to
    $q_s n_(s,0)u_(s,1)$. Insert it into

    $ bold(epsilon) dot bold(E)=bold(E)+(i/(epsilon_0 omega))bold(j) .$

    The contribution of species $s$ is the susceptibility

    $ -omega_(p,s)^2/(omega^2-k^2 c_s^2) .$

    Summing over species gives the displayed longitudinal dielectric response
    $epsilon_(parallel).$

    #derivation-step[Identify the fixed-ion warm branch]
    For fixed ions, set the electron-only coefficient to zero:

    $ 1-omega_(p,e)^2/(omega^2-k^2 c_(s,e)^2)=0 .$

    Multiplication by the denominator gives

    $ omega^2-k^2 c_(s,e)^2-omega_(p,e)^2=0 .$

    This is the warm plasma-oscillation branch. The definitions

    $ lambda_(D,e)^2=(epsilon_0 k_B T_e)/(n_0 e^2) $ \
    $ c_(s,e)^2=(gamma_e k_B T_e)/m_e $

    imply

    $ c_(s,e)^2/omega_(p,e)^2=gamma_e lambda_(D,e)^2 .$

    #derivation-step[Separate the two-species roots]
    For two mobile species, multiply the longitudinal condition by both
    denominators:

    $ (omega^2-k^2 c_(s,e)^2)(omega^2-k^2 c_(s,i)^2)
      -omega_(p,e)^2(omega^2-k^2 c_(s,i)^2)
      -omega_(p,i)^2(omega^2-k^2 c_(s,e)^2)=0 .$

    This is quadratic in $omega^2$. For the low-frequency root, terms of
    order $k^4 c_(s,e)^2 c_(s,i)^2$ are smaller than the plasma-frequency
    terms. Retaining the terms of order $omega^2$ and $k^2$ gives

    $ -(omega_(p,e)^2+omega_(p,i)^2)omega^2
      +k^2[omega_(p,e)^2 c_(s,i)^2
      +omega_(p,i)^2 c_(s,e)^2] approx 0 .$

    Solving gives the displayed ion-acoustic speed. Charge neutrality implies

    $ omega_(p,i)^2/omega_(p,e)^2=m_e/m_i ,$

    so

    $ c_"ia"^2 approx c_(s,i)^2+(m_e/m_i)c_(s,e)^2
      =(gamma_i k_B T_i)/m_i+(gamma_e k_B T_e)/m_i .$

    The high-frequency root approaches the electron plasma-oscillation branch.]
  )

  #warm-longitudinal-modes

  #rechenbeispiel[
    Assume a homogeneous, unmagnetized, collisionless, fixed-ion warm-fluid
    electron plasma with an isothermal closure. Use
    $n_0=qty("1.0e16", "m^-3")$,
    $k_B T_e=qty("1.602e-18", "J")$ (the same energy as
    $qty("10", "eV")$), $e=qty("1.602e-19", "C")$,
    $m_e=qty("9.109e-31", "kg")$, and $gamma_e=1$.
    This is a formal isothermal-closure calculation outside the controlled
    small-$k lambda_D$ regime; its result requires kinetic comparison before
    interpretation as a collisionless plasma wave.
    At #normalized-label[$k lambda_(D,e)=qty("0.80", "1")$], determine
    $lambda_(D,e)$, $k$, and the
    normalized warm plasma-oscillation frequency.

    Numerical result: $lambda_(D,e)=qty("2.35e-4", "m")$,
    $k=qty("3.40e3", "m^-1")$, and
    #normalized-label[$omega/omega_(p,e)=qty("1.28", "1")$].
  ]

  #interpretation(
    [Pressure couples neighboring density perturbations],
    [Without pressure, each cold-fluid density displacement oscillates at the
    same plasma frequency. The pressure gradient couples neighboring density
    perturbations and introduces wave-number dependence. Its relative
    contribution is $gamma_e k^2 lambda_(D,e)^2$ on the fixed-ion branch.
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
      answer: [The pressure perturbation $-grad(p_(s,1))$ couples density variation to velocity through continuity, producing the $k^2 c_s^2$ term in the denominator.]
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
    Pressure also modifies waves propagating across the magnetic field, but
    propagation direction and electric-field polarization must be distinguished.
    Near the upper-hybrid frequency it adds a warm spatial
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
    The speeds $v_A$, $v_s$, and $v_m$ are in #unit("m/s"). The ratios
    $omega/omega_(c,i)$ and $k lambda_D$ are dimensionless.
  ]

  #assumption(
    [Warm-fluid and ideal-MHD limits],
    [Use the warm-fluid pressure closure for the upper-hybrid correction,
    with fixed ions, $bold(k) perp bold(B)_0$, and an electrostatic
    perturbation $bold(E)_1 parallel bold(k)$. This is the longitudinal
    approximation near the extraordinary branch's upper-hybrid resonance.
    For the low-frequency MHD derivation assume quasineutrality,
    $omega << omega_(c,i)$, $k lambda_D << 1$, a single bulk velocity, and
    sufficiently large conductivity that the ideal induction law applies.
    The bulk velocity is mass-weighted. The relative drift remains through
    $bold(j)=e n (bold(u)_i-bold(u)_e)$ and Ampere's law; Hall and relative
    inertial corrections are ordered small, rather than setting the current
    to zero.
    Use an adiabatic closure $p_1=v_s^2 rho_1$ with
    $v_s^2=(gamma p_0)/rho_0$.]
  )

  #definition(
    [Alfvén, sound, and magnetosonic speeds],
    [Define
    $v_A=B_0/sqrt(mu_0 rho_0)$,
    $v_s=sqrt((gamma p_0)/rho_0)$, and
    $v_m=sqrt(v_A^2+v_s^2)$
    for perpendicular compressional motion. The square $v_A^2$ is magnetic
    tension per unit mass density, $v_s$ is the pressure-wave speed, and $v_m$ is
    their warm perpendicular combination.]
  )

  #governing-law(
    [Warm upper-hybrid and MHD branches],
    [In the perpendicular electrostatic approximation near the upper-hybrid
    branch, the warm-fluid correction gives
    $omega^2=omega_"UH"^2+k^2 c_(s,e)^2$
    in the simple electron pressure ordering. At low frequency, ideal MHD
    gives the shear-Alfvén branch
    $omega^2=k_(parallel)^2 v_A^2$
    and the perpendicular compressional branch
    $omega^2=k_(perp)^2(v_A^2+v_s^2)$.
    The latter is often called the magnetosonic or magnetosonic-Alfvén
    branch.]
  )

  #details(
    [Derivation: warm upper hybrid and magnetosonic restoring forces],
    [#derivation-step[Perpendicular warm-electron response]
    Choose $bold(k)=k bold(e)_x$, $bold(E)_1=E_(1,x) bold(e)_x$, and
    $bold(B)_0=B_0 bold(e)_z$. Continuity gives

    $ -i omega n_(e,1)+i k n_0 u_(e,1,x)=0 $ \

    and therefore

    $ n_(e,1)/n_0=(k u_(e,1,x))/omega .$

    With the signed electron gyrofrequency
    $Omega_e=-omega_(c,e)$, the transverse momentum equations are

    $ -i omega u_(e,1,x)-Omega_e u_(e,1,y)
      =(q_e/m_e) E_(1,x)-(i k c_(s,e)^2 n_(e,1))/n_0 $ \

    and

    $ Omega_e u_(e,1,x)-i omega u_(e,1,y)=0 .$

    The second equation gives

    $ u_(e,1,y)=-i (Omega_e/omega) u_(e,1,x) .$

    Insert this relation and the continuity result into the first equation.
    Collect the velocity terms and multiply by $i$:

    $ ((omega^2-Omega_e^2-k^2 c_(s,e)^2)/omega) u_(e,1,x)
      =((i q_e)/m_e) E_(1,x) .$

    Hence

    $ u_(e,1,x)=((i q_e omega)/(m_e
      (omega^2-omega_(c,e)^2-k^2 c_(s,e)^2))) E_(1,x) ,$

    and continuity gives

    $ n_(e,1)=((i n_0 q_e k)/(m_e
      (omega^2-omega_(c,e)^2-k^2 c_(s,e)^2))) E_(1,x) .$

    #derivation-step[Close the electrostatic response]
    For an electrostatic wave, Gauss's law is

    $ i k E_(1,x)=(q_e n_(e,1))/epsilon_0 .$

    Substitute the density response and cancel the nonzero factor
    $i k E_(1,x):$

    $ 1=((n_0 q_e^2)/(epsilon_0 m_e
      (omega^2-omega_(c,e)^2-k^2 c_(s,e)^2)))
      =(omega_(p,e)^2)/(omega^2-omega_(c,e)^2-k^2 c_(s,e)^2) .$

    The warm upper-hybrid branch is therefore

    $ omega^2=omega_(p,e)^2+omega_(c,e)^2+k^2 c_(s,e)^2
      =omega_"UH"^2+k^2 c_(s,e)^2 .$

    This is a local warm-fluid approximation near the upper-hybrid branch.
    The full electromagnetic warm tensor contains additional polarization
    terms.

    #derivation-step[Recover the perpendicular MHD branch]
    For the low-frequency one-fluid limit, use continuity,
    $pdv(rho,t)+div(rho bold(u))=0$, the ideal induction equation,
    $pdv(bold(B),t)=curl(bold(u)times bold(B))$, and the MHD
    momentum equation

    $ rho pdv(bold(u),t)=-grad(p)+[curl(bold(B))times bold(B)]/mu_0 .$

    This momentum equation is written to first order about a static
    equilibrium; the advective acceleration is second order in the
    perturbations. Linearize about $rho=rho_0$, $p=p_0$, and
    $bold(B)=B_0 bold(e)_z$. For $bold(k)=k bold(e)_x$ and
    $bold(u)_1=u_x bold(e)_x$, continuity gives

    $ -i omega rho_1+i k rho_0u_x=0,
      quad rho_1=(rho_0 k u_x)/omega .$

    The pressure closure is $p_1=v_s^2rho_1$. The induction equation gives

    $ -i omega B_(1,z)=-i k B_0u_x,
      quad B_(1,z)=(B_0 k u_x)/omega .$

    The $x$ component of momentum is

    $ -i omega rho_0u_x=-i k p_1-i (k B_0B_(1,z))/mu_0 .$

    Substitute the density, pressure, and magnetic perturbations, then divide
    by the nonzero factor $rho_0u_x/omega$:

    $ omega^2=k^2[v_s^2+B_0^2/(mu_0 rho_0)]
      =k^2(v_s^2+v_A^2) .$

    Thus the perpendicular compressional speed is

    $ v_m=sqrt(v_A^2+v_s^2) .$

    #derivation-step[Recover the shear-Alfvén branch]
    For a shear perturbation with
    $bold(k)=k_(parallel) bold(e)_z$, the pressure and density perturbations
    vanish to first order. Induction and transverse momentum retain only
    magnetic tension:

    $ pdv(bold(u)_perp,t,2)=v_A^2 pdv(bold(u)_perp,z,2) .$

    A plane wave then satisfies

    $ omega^2=k_(parallel)^2v_A^2 .$

    Tension bends field lines, whereas perpendicular compression changes both
    density and magnetic-field strength.]
  )

  #mhd-wave-speeds

  #animation(
    "../media/magnetosonic-waves.mp4",
    "Three normalized ideal-MHD patterns share length and time scales. Sound propagates along the background field. The shear Alfvén pattern has wave vector and background field along x, displacement along y independent of y, and zero displacement divergence. The perpendicular fast magnetosonic pattern shows density and magnetic compression and travels faster than either separate sound or Alfvén speed.",
    caption: [
      Warm magnetized-wave patterns: pressure compression, shear-Alfvén field
      displacement, and perpendicular compressional magnetosonic motion.
      All panels use $X=x/L_0$ and $tau=t/t_0$, with reference speed
      $L_0/t_0$. Their dimensionless speeds are
      $(v_s t_0)/L_0=0.6$, $(v_A t_0)/L_0=1$, and
      $(v_m t_0)/L_0=sqrt(1.36)$; the common wave number is $k L_0=1.25$.
      The prescribed linear patterns illustrate $v_m^2=v_A^2+v_s^2$;
      $L_0$ and $t_0$ are arbitrary reference length (#unit("m")) and time
      (#unit("s")).
    ],
    poster: "../media/magnetosonic-waves.png",
  )

  #rechenbeispiel[
    Assume a homogeneous, quasineutral hydrogen plasma in the low-frequency,
    strongly conducting ideal-MHD limit, with perpendicular and parallel
    propagation compared. Use
    $n_0=qty("1.0e16", "m^-3")$, $B_0=qty("1.0e-2", "T")$,
    $m_i=qty("1.673e-27", "kg")$,
    $k_B T_e=k_B T_i=qty("1.602e-18", "J")$ (10 eV), and isothermal
    $gamma_e=gamma_i=1$, determine $v_A$, the total-pressure sound speed
    $v_s$, and $v_m$. For $k=qty("1.0e-3", "m^-1")$, report the parallel
    shear-Alfvén and perpendicular magnetosonic frequencies.

    Numerical result: $v_A=qty("2.18e6", "m/s")$,
    $v_s=qty("4.38e4", "m/s")$, and
    $v_m=qty("2.18e6", "m/s")$ to the shown precision.
    The two example frequencies are
    $omega_A=qty("2.18e3", "s^-1")$ and
    $omega_m=qty("2.18e3", "s^-1")$.
  ]

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
      answer: [Use a quasineutral, strongly conducting plasma with a mass-weighted bulk velocity, frequencies below the ion-inertia scale, and fluid length scales. Retain the relative species drift as the current in Ampere's law, while ordering Hall and relative inertial corrections small. Exact equality of electron and ion velocities would incorrectly remove that current.]
    ),
  ))

  #section-title[Ordering map: from cold waves to warm MHD] <finite-temperature-ordering>

  #lead[
    The collisional, two-fluid, warm-fluid, and MHD responses of the
    preceding sections are branches of one model-selection map. Four
    dimensionless orderings decide whether a cold, collisional, two-fluid,
    warm-fluid, MHD, or kinetic calculation is justified.
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
    #unit("m^-1"); and $lambda_D$ and the pressure-response gyroradius
    $rho_s=c_s/omega_(c,s)$ are in #unit("m"). Particle and wave speeds are
    in #unit("m/s").
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

  #governing-law(
    [Controlled limits],
    [The branches must satisfy four checks:
    (1) $nu -> 0$ recovers the lossless cold tensor away from poles;
    $N$ is real on propagating branches but imaginary in stopbands;
    (2) $m_i -> infinity$ or $I -> infinity$ recovers the fixed-ion branches;
    (3) $T_s -> 0$ or $K -> 0$ removes the pressure correction; and
    (4) $omega << omega_(c,i)$ with high conductivity reduces the
    two-fluid system to MHD, with $v_A$ and $v_m$ as the leading speeds.
    If $k rho_s$ is not small, $omega-k_(parallel)v_(parallel)$ approaches
    zero, or the distribution is strongly non-Maxwellian, a kinetic
    susceptibility is required even when the fluid equations look closed.]
  )

  #details(
    [Derivation: recovering the neighboring models],
    [#derivation-step[Recover the collisionless model]
    Begin with

    $ m_"eff"=m(1+(i nu)/omega) .$

    Let $nu -> 0$ at real frequency away from poles. Then $m_"eff" -> m$
    and the cold dielectric tensor is Hermitian: its diagonal coefficients
    are real and its gyrotropic off-diagonal entries remain imaginary complex
    conjugates. Absorption vanishes, but a stopband with $N^2<0$ still has
    imaginary $k$ and spatial evanescence. Real $N$ is recovered only on
    propagating branches.

    #derivation-step[Take the fixed-ion limit]
    For a singly charged electron--ion plasma, define

    $ omega_(c,i)/omega_(c,e)=m_e/m_i=M, quad
      omega_(p,i)^2/omega_(p,e)^2=M .$

    At fixed $omega$ with $omega >> omega_(c,i)$, the ion denominators are
    regular and the ion susceptibility is smaller by $M$ than the electron
    susceptibility. Sending $M -> 0$ removes the ion contribution and
    recovers the fixed-ion tensor. This argument fails when $omega$ is also
    reduced to the ion-cyclotron scale, because the ion denominator is then no
    longer an order-one factor.

    #derivation-step[Recover the warm and cold pressure limits]
    The pressure-corrected species susceptibility contains

    $ omega^2-k^2c_s^2 $

    instead of $omega^2$. Taking $T_s -> 0$ sends $c_s -> 0$ and returns the
    cold denominator. Conversely, when $k lambda_D$ becomes order unity, the
    pressure term changes the longitudinal root by an order-one amount and
    cannot be treated as a perturbation.

    #derivation-step[Recover the MHD endpoint]
    Take $omega << omega_(c,i)$ while maintaining high conductivity and
    quasineutrality. The weighted momentum sum gives

    $ rho_0 pdv(bold(u),t)
        =-grad(p)+[curl(bold(B)) times bold(B)]/mu_0 .$

    The induction equation becomes

    $ pdv(bold(B),t)=curl(bold(u)times bold(B)) .$

    Linearizing these equations gives the shear-Alfvén and magnetosonic
    dispersions derived in the previous section.

    #derivation-step[Check the scale-ordering boundaries]
    A fluid closure fails when a wave samples unresolved particle scales. The
    independent checks are

    $ k lambda_D <<1, quad
      k_perp rho_s <<1, quad
      abs(omega/k_(parallel)) >> abs(v_(parallel)) $

    for cold quasineutral motion, finite-Larmor-radius effects, and resonant
    kinetic corrections respectively, with $v_(parallel)$ a thermal parallel
    speed. Satisfying one condition does not imply
    that the others hold.]
  )

  #warm-wave-ordering

  #rechenbeispiel[
    Classify two model orderings. Case A has
    #normalized-label[$C=qty("0.02", "1")$],
    #normalized-label[$I=qty("50", "1")$],
    #normalized-label[$K=qty("0.05", "1")$], and
    #normalized-label[$M=qty("5.45e-4", "1")$]. Case B has
    #normalized-label[$C=qty("0.30", "1")$],
    #normalized-label[$I=qty("0.40", "1")$],
    #normalized-label[$K=qty("0.80", "1")$], and the same
    #normalized-label[$M=qty("5.45e-4", "1")$].
    State the simplest justified description and the first correction to add
    in each case.

    Numerical result: Case A is collisionless cold fixed-ion to leading order;
    the first corrections are collisional damping, ion inertia, and warm
    dispersion in the displayed order. Case B requires a collisional
    two-fluid warm model; a kinetic check is recommended because all three
    primary orderings are no longer asymptotically small.
  ]

  #interpretation(
    [Limits as consistency checks],
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
      answer: [Taking $nu -> 0$ at fixed real frequency away from poles removes collisional absorption and recovers the Hermitian cold tensor. Propagating branches have real $N$, while lossless stopbands can retain imaginary $N$ and evanescence.]
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
    previous: (href: "12-cold-magnetized-waves.html", title: [Cold magnetized waves]),
    next: (href: "14-hot-plasma-waves.html", title: [Hot plasma waves]),
  )
]
