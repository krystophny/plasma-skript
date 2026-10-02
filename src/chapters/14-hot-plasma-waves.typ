#import "../theme.typ": *
#import "../figures.typ": hot-isotropic-dispersion, hot-velocity-space-slopes, two-stream-growth, hot-magnetized-resonance
#import "@preview/physica:0.9.8": div, grad, pdv, dv, curl
#import "@preview/unify:0.8.1": qty, unit

#let chapter = [
  #page-title(number: 14)[Waves in hot plasmas] <hot-plasma-waves>

  #lead[
    A fluid closure retains only a few velocity moments. A hot plasma wave
    can depend on the particles that move nearly with the wave, so the full
    distribution function becomes part of the response. This chapter builds
    that kinetic response from the Vlasov equation, identifies resonant
    particles, derives collisionless damping and two-stream growth, and then
    extends the resonance picture to a magnetized plasma, following the hot-
    plasma treatment in @bittencourt2004. Here “hot” means that the velocity
    distribution matters for the wave response; it is not an absolute
    temperature threshold.
  ]

  #callout(
    [Distribution slope at the phase velocity],
    [A hot-plasma dispersion relation is not specified by density and
    temperature alone. The slope of the velocity distribution projected along
    the wave helps decide whether resonant particles absorb energy from it or
    supply energy to it.]
  )

  #section-title[Hot isotropic plasma dispersion] <hot-isotropic-dispersion>

  #lead[
    A kinetic wave calculation starts with an equilibrium distribution.
    Perturb it weakly and solve the Vlasov equation along the
    unperturbed particle trajectories. The resulting susceptibility contains
    a resonant denominator that a finite set of fluid moments cannot reproduce.
  ]

  #objectives((
    [write the collisionless Vlasov equation and its linear perturbation],
    [derive the electrostatic kinetic dispersion relation from Poisson's equation],
    [recover the cold plasma frequency and warm long-wave correction as limits],
    [define the plasma dispersion function and state its contour prescription],
  ))

  #unit-ledger[
    The distribution $f_s$ is a phase-space density with units
    #unit("m^-6 s^3"). The plasma dispersion function, $k lambda_D$, and
    $omega/omega_(p,e)$ are dimensionless.
  ]

  #assumption(
    [Collisionless isotropic equilibrium],
    [Use a homogeneous unmagnetized electron plasma with fixed neutralizing
    ions, $bold(B)_0=bold(0)$, and a smooth isotropic equilibrium
    $f_(e,0)(bold(v))$. Let the perturbation be small and use the Fourier
    convention $exp(i (bold(k) dot bold(r)-omega t))$. The linear calculation
    describes normal modes; it does not describe nonlinear trapping or a
    finite-amplitude rearrangement of the distribution.]
  )

  #definition(
    [Kinetic perturbation],
    [The collisionless kinetic equation for species $s$ is
    $pdv(f_s,t)+bold(v) dot grad(f_s)+
      (q_s/m_s) (bold(E)+bold(v) times bold(B)) dot
      pdv(f_s,bold(v))=0$.
    Expand
    $f_s=f_(s,0)(bold(v))+epsilon f_(s,1)(bold(r),bold(v),t)$,
    $bold(E)=epsilon bold(E)_1$, and use
    $f_(s,1) = tilde(f)_(s,1)(bold(v))
      exp(i (bold(k) dot bold(r)-omega t))$.
    The dimensionless parameter $epsilon$ orders perturbation amplitudes.
    It is distinct from the dielectric function $epsilon_L$ below.]
  )

  #governing-law(
    [Electrostatic kinetic dispersion],
    [For a longitudinal perturbation with $bold(k) parallel bold(E)_1$,
    the allowed modes satisfy
    $epsilon_(L)(omega,bold(k))=1+
      sum_s q_s^2/(epsilon_0 m_s k^2)
      integral_(-infinity)^infinity
      [bold(k) dot pdv(f_(s,0)(bold(v)),bold(v))]/
      [omega-bold(k) dot bold(v)] dif^3 bold(v)=0$.
    The species sum includes mobile species; fixed ions supply equilibrium
    neutrality but no perturbed response. The integral uses causal analytic
    continuation from $Im(omega)>0$, with the Landau contour passing below
    the moving pole for $k>0$. For an electron Maxwellian,
    $f_(e,0)(bold(v))=n_0/(pi^(3/2) v_"te"^3)
      exp(-v^2/v_"te"^2)$,
    $v_"te"=sqrt((2 k_B T_e)/m_e)$, and
    $epsilon_L=1+1/(k^2 lambda_D^2)[1+zeta Z(zeta)]$ with
    $zeta=omega/(k v_"te")$ and
    $lambda_D^2=(epsilon_0 k_B T_e)/(n_0 e^2)$.
    Here $Z(zeta)=1/sqrt(pi) integral exp(-x^2)/(x-zeta) dif x$ is the
    plasma dispersion function on that contour from $-infinity$ to
    $infinity$; $x=v_(parallel)/v_"te"$ is a dimensionless integration
    variable.]
  )

  #details(
    [Derivation: Vlasov response, Poisson, and the Maxwellian limit],
    [#derivation-step[Linearize the Vlasov equation]
    Insert the perturbation expansion and retain first-order terms. With
    $bold(B)_0=bold(0)$, the linear equation is

    $ pdv(f_(s,1),t)+bold(v) dot grad(f_(s,1))+
      q_s/m_s bold(E)_1 dot pdv(f_(s,0),bold(v))=0 .$

    For the Fourier convention used here,

    $ pdv(f,t) -> -i omega f, quad grad(f) -> i bold(k) f .$

    Therefore

    $ i (bold(k) dot bold(v)-omega) tilde(f)_(s,1)+
      q_s/m_s bold(E)_1 dot pdv(f_(s,0),bold(v))=0 ,$

    and

    $ tilde(f)_(s,1)=(-i q_s)/m_s
      (bold(E)_1 dot pdv(f_(s,0),bold(v)))/
      (omega-bold(k) dot bold(v)) .$

    #derivation-step[Close the electrostatic response with Poisson's equation]
    For an electrostatic wave, set

    $ bold(E)_1=-i bold(k) phi_1 .$

    The perturbed charge density is

    $ rho_1=sum_s q_s integral tilde(f)_(s,1) dif^3 bold(v) .$

    Inserting the distribution response gives

    $ rho_1=-sum_s (q_s^2 phi_1)/m_s
      integral (bold(k) dot pdv(f_(s,0),bold(v)))/
      (omega-bold(k) dot bold(v)) dif^3 bold(v) .$

    Poisson's equation is

    $ div(bold(E)_1)=rho_1/epsilon_0 .$

    After the Fourier substitution, $k^2 phi_1=rho_1/epsilon_0$. A nonzero
    potential therefore requires the displayed condition $epsilon_L=0$.

    #derivation-step[Evaluate an isotropic Maxwellian]
    Choose the $z$ axis along $bold(k)$. The perpendicular velocity integrals
    reduce the response to the one-dimensional plasma-dispersion function

    $ Z(zeta)=1/sqrt(pi) integral_(-infinity)^infinity
      exp(-x^2)/(x-zeta) dif x .$

    Define the integral first for $Im(omega)>0$ and $k>0$, then continue
    causally, keeping the contour below the pole as it crosses the real axis.
    For one
    isotropic electron Maxwellian, the result is

    $ epsilon_L=1+1/(k^2 lambda_D^2)[1+zeta Z(zeta)] .$

    #derivation-step[Recover cold and warm limits]
    For a cold distribution, the integration-by-parts form reduces to

    $ epsilon_L=1-omega_(p,e)^2/omega^2 ,$

    so $omega=omega_(p,e)$. For $abs(zeta)>>1$,

    $ Z(zeta) approx -1/zeta-1/(2 zeta^3)-3/(4 zeta^5) .$

    Substitution into $epsilon_L=0$ gives

    $ omega^2 approx omega_(p,e)^2+(3 k^2 k_B T_e)/m_e .$

    The warm-fluid coefficient is the leading real kinetic correction, while
    the contour contribution contains collisionless damping omitted by the
    moment closure.]
  )

  #rechenbeispiel[
    Use $n_0=qty("1.0e16", "m^-3")$,
    $k_B T_e=qty("1.602e-18", "J")$ (that is, $qty("10", "eV")$),
    $m_e=qty("9.109e-31", "kg")$,
    $e=qty("1.602e-19", "C")$, and
    $epsilon_0=qty("8.854e-12", "F/m")$. Take
    #normalized-label[$k lambda_D=qty("0.20", "1")$] and use the
    long-wavelength warm approximation
    #normalized-label[$omega_r^2/omega_(p,e)^2 approx
      1+3(k lambda_D)^2$].
    Determine $lambda_D$, $k$, and $omega_r$.

    Numerical result: $lambda_D approx qty("2.35e-4", "m")$,
    $k approx qty("851", "m^-1")$, and
    #normalized-label[$omega_r/omega_(p,e) approx qty("1.06", "1")$] or
    $omega_r approx qty("5.97e9", "s^-1")$.
  ]

  #interpretation(
    [The kinetic correction has two parts],
    [The real part of the kinetic susceptibility shifts the wave frequency,
    while its contour contribution supplies a small imaginary part when
    resonant particles are present. The warm-fluid result can reproduce the
    long-wave real shift, but it cannot decide the sign of wave-particle
    energy exchange.]
  )

  #summary[
    The Vlasov equation plus Poisson's equation produces a dielectric function
    containing the distribution function and a resonant denominator. A cold
    delta distribution recovers $omega=omega_(p,e)$; a Maxwellian gives the
    plasma-dispersion function and the warm long-wave shift
    $omega^2 approx omega_(p,e)^2+(3 k^2 k_B T_e)/m_e$.
  ]

  #knowledge-check((
    (
      question: [Why can a finite set of fluid moments miss a hot-plasma wave effect?],
      answer: [The moment hierarchy compresses velocity space. A resonant denominator samples the distribution at a particular velocity, so the local slope and contour contribution are not determined by a finite density, momentum, and pressure set alone.]
    ),
    (
      question: [What role does the Landau contour play in the electrostatic dielectric function?],
      answer: [It specifies how the velocity integral bypasses the pole at the wave phase velocity. That analytic prescription supplies the imaginary contribution associated with resonant particles.]
    ),
    (
      question: [Which limit recovers the cold electron plasma frequency?],
      answer: [Taking the equilibrium distribution toward a cold velocity-space delta function, or taking the long-wave thermal correction to zero, gives $epsilon_L=1-omega_(p,e)^2/omega^2$ and $omega=omega_(p,e)$.]
    ),
    (
      question: [What does the coefficient three in the warm Langmuir correction represent?],
      answer: [For an isotropic Maxwellian and a long-wavelength expansion, the second velocity moment enters the real susceptibility and gives the coefficient $(3 k_B T_e)/m_e$. A different closure or distribution must be stated before changing it.]
    ),
  ))

  #section-title[Resonant particles and velocity-space response] <hot-resonant-particles>

  #lead[
    The strongest resonant response comes from particles near the phase
    velocity $v_"phi"=omega_r/k$, which selects a narrow region of velocity
    space. The
    denominator $omega-k v$ becomes small there, so the slope of the
    equilibrium distribution near $v_"phi"$ controls the direction of the
    resonant energy exchange.
  ]

  #objectives((
    [define the phase velocity and resonant velocity for a longitudinal wave],
    [locate the pole in the velocity integral and explain its contour treatment],
    [relate the sign of the velocity-space slope to damping or growth],
    [distinguish a smooth resonance from nonlinear particle trapping],
  ))

  #unit-ledger[
    The phase velocity $v_"phi"$ and thermal speed $v_"te"$ are in
    #unit("m/s"). The resonant velocity $v_"res"$ is in #unit("m/s"),
    $omega_r$ and the weak rate $gamma$ are in #unit("s^-1"), and $k$ is in
    #unit("m^-1"). The one-dimensional marginal $F_(s,0)$ is in
    #unit("m^-4 s"), and its slope $dv(F_(s,0),v)$ is in
    #unit("m^-5 s^2"). The ratios $v_"phi"/v_"te"$ and
    $gamma/omega_(p,e)$ are dimensionless.
  ]

  #assumption(
    [Weak, smooth, collisionless resonance],
    [Assume a smooth equilibrium and a small complex correction to a real
    wave root, $omega=omega_r+i gamma$ with $abs(gamma)<<omega_r$. The
    perturbation remains linear, so resonant trapping width and nonlinear
    plateau formation are outside this section.]
  )

  #definition(
    [Velocity marginal along the wave],
    [For $bold(k)=k bold(e)_z$ with $k>0$, write $v=v_z$ and integrate out
    the perpendicular velocities:
    $F_(s,0)(v)=integral_(RR^2) f_(s,0)(v_x,v_y,v) dif v_x dif v_y$,
    so $integral_(-infinity)^infinity F_(s,0)(v) dif v=n_(s,0)$.
    This is a marginal distribution, not a slice at $v_x=v_y=0$.
    For the isotropic Maxwellian,
    $F_(e,0)(v)=(n_0/(sqrt(pi) v_"te")) exp(-v^2/v_"te"^2)$.]
  )

  #definition(
    [Phase and resonant velocity],
    [For a forward longitudinal wave, define
    $v_"phi"=omega_r/k$ and
    $v_"res"=v_"phi"$. The pole of the response is at
    $omega_r-k v_"res"=0$ in the real-frequency limit. For a marginal that varies slowly across the
    resonant layer, only its local derivative
    $dv(F_(s,0),v)$ evaluated at $v=v_"res"$ is needed for the leading sign of the
    collisionless energy exchange.]
  )

  #governing-law(
    [Slope criterion],
    [For a weakly damped or growing root,
    $gamma=-(Im(epsilon_(L)(omega_(r),k)))/
      (pdv(Re(epsilon_(L)(omega,k)),omega))$.
    The derivative in the denominator is evaluated at
    $omega=omega_(r)$.
    With the present Fourier convention, $gamma<0$ means temporal damping and
    $gamma>0$ means temporal growth. For the usual positive-frequency branch,
    with positive $pdv(Re(epsilon_(L)),omega)$, a Maxwellian marginal slope
    $dv(F_(e,0),v)<0$ gives damping, while a positive
    bump-on-tail slope can give growth. The sign is a physical statement only
    after the Fourier convention and propagation direction are fixed.]
  )

  #details(
    [Derivation: pole, contour, and local slope],
    [#derivation-step[Expose the resonant denominator]
    Choose $bold(k)=k bold(e)_z$ with $k>0$. Integrate the three-dimensional
    response over $v_x,v_y$ before integrating by parts in $v$:

    $ epsilon_L=1-sum_s q_s^2/(epsilon_0 m_s k^2)
      integral_(-infinity)^infinity
      (dv(F_(s,0),v))/(v-omega/k) dif v .$

    The boundary term $F_(s,0)(v)/(v-omega/k)$ vanishes at infinity.
    Since $dv(1/(v-omega/k),v)=-1/(v-omega/k)^2$, this becomes

    $ epsilon_L=1-
      sum_s q_s^2/(epsilon_0 m_s k^2)
      integral_(-infinity)^infinity
      F_(s,0)(v)/(v-omega/k)^2 dif v .$

    The contour prescription is unchanged. The equivalent first-derivative
    form is useful because the pole contribution is directly proportional to
    $dv(F_(s,0),v)$ at $v=omega_r/k$.

    #derivation-step[Take the causal boundary value]
    Start in $Im(omega)>0$ and continue toward the real axis. For a smooth
    test function $g(v)$, the boundary value is

    $ integral (g(v))/(v-v_"res"-i 0) dif v
      =upright("PV") integral (g(v))/(v-v_"res") dif v+i pi g(v_"res") .$

    Here $upright("PV")$ denotes the Cauchy principal value. Consequently,

    $ Im(epsilon_(L)(omega_r,k))=
      -sum_s (pi q_s^2)/(epsilon_0 m_s k^2)
        dv(F_(s,0),v) .$

    Each derivative on the right is evaluated at $v=omega_r/k$.

    A negative electron marginal slope therefore gives positive
    $Im(epsilon_L)$. On the Langmuir branch the real-frequency derivative
    is positive, so the weak-rate relation gives damping. The following
    section derives that relation and its Maxwellian asymptote.]
  )

  #hot-velocity-space-slopes

  #rechenbeispiel[
    For $n_0=qty("1.0e16", "m^-3")$ and
    $k_B T_e=qty("1.602e-18", "J")$, use
    $lambda_D=qty("2.35e-4", "m")$ and
    $omega_(p,e)=qty("5.64e9", "s^-1")$. At
    #normalized-label[$k lambda_D=qty("0.30", "1")$], estimate
    #normalized-label[$omega_r/omega_(p,e)$] from the long-wave real root,
    and locate the resonance using $v_"te"=sqrt(2) omega_(p,e) lambda_D$.

    Numerical result: #normalized-label[$omega_r/omega_(p,e)
      approx qty("1.13", "1")$],
    #normalized-label[$v_"res"/v_"te" approx qty("2.66", "1")$].
    The Maxwellian marginal slope there is negative.
  ]

  #interpretation(
    [Resonance is not the same as trapping],
    [The linear theory identifies the particles that exchange energy with the
    wave. At larger amplitude those particles can become trapped in the wave
    potential, flatten the distribution near $v_"phi"$, and change the rate.
    The slope criterion is therefore a linear diagnostic.]
  )

  #summary[
    The resonant velocity is the phase velocity for an unmagnetized
    longitudinal wave. The Landau contour converts the local slope of
    $F_(e,0)(v)$ into an imaginary frequency correction: negative slope damps the
    positive-frequency Maxwellian branch, while a positive slope can drive it.
  ]

  #knowledge-check((
    (
      question: [Which particles are selected by a longitudinal Landau resonance?],
      answer: [Particles with velocity near the wave phase velocity satisfy $omega_r-k v approx 0$. They are the particles for which the wave and particle remain in phase long enough for a coherent energy exchange.]
    ),
    (
      question: [Why does the slope of $F_(e,0)$ matter more than its value at the resonance?],
      answer: [The contour contribution compares particles just below and just above the resonant velocity. Their imbalance is represented by the local derivative, which determines the net direction of energy transfer.]
    ),
    (
      question: [What does $gamma<0$ mean with the convention $exp(i (k x-omega t))$?],
      answer: [Since $omega=omega_r+i gamma$, the time factor contains $exp(gamma t)$. Therefore $gamma<0$ is temporal damping and $gamma>0$ is temporal growth.]
    ),
    (
      question: [When should the weak-damping estimate be replaced by a complex root calculation?],
      answer: [Solve the full complex dispersion relation when the rate is not small compared with the real frequency or when coupled resonances defeat the weak-rate expansion. A nonsmooth distribution needs its own integral treatment. Nonlinear trapping requires a nonlinear model, not just a more accurate linear root.]
    ),
  ))

  #section-title[Landau damping and wave growth] <landau-damping-growth>

  #lead[
    The resonant-particle argument becomes quantitative when the complex root
    is separated into an oscillation frequency and a rate. Landau damping is
    collisionless attenuation caused by phase-correlated particles, whereas
    growth occurs when a non-equilibrium distribution has a free-energy slope
    that reverses the exchange.
  ]

  #objectives((
    [separate the real frequency and temporal rate of a complex root],
    [derive the weak-rate formula and follow energy into velocity-space structure],
    [interpret collisionless damping as wave--particle energy exchange],
    [convert a temporal rate to a spatial attenuation scale when appropriate],
  ))

  #unit-ledger[
    The real frequency $omega_r$, temporal rate $gamma$, and plasma frequency
    $omega_(p,e)$ are in #unit("s^-1"). The wave number $k$ is in
    #unit("m^-1"), the group velocity is in #unit("m/s"), and the temporal
    and spatial e-folding scales are in #unit("s") and #unit("m"). Rates
    normalized by $omega_(p,e)$ and wave numbers normalized by $lambda_D$ are
    dimensionless.
  ]

  #assumption(
    [Weak complex-frequency correction],
    [Let the real part of the kinetic dispersion relation have a simple root
    $omega_(r)(k)$. Assume $abs(gamma)<<omega_(r)$, a collisionless plasma, and a
    contour prescription that is causal for the chosen initial-value problem.
    The mode is followed before nonlinear saturation or strong collisional
    broadening occurs.]
  )

  #definition(
    [Temporal and spatial damping scales],
    [With $omega=omega_r+i gamma$, the time factor is
    $exp(-i omega t)=exp(-i omega_r t) exp(gamma t)$.
    A damping time is $tau_"d"=1/abs(gamma)$ for $gamma<0$. For a forward
    packet with group velocity $v_"g">0$, the corresponding spatial rate is
    $k_i approx -gamma/v_"g"$ and the amplitude attenuation length is
    $L_"amp"=1/k_i$. These are distinct from the intensity e-folding length,
    which is $1/(2 k_i)$.]
  )

  #governing-law(
    [Landau damping estimate],
    [The general weak-rate relation is
    $gamma=-Im(epsilon_(L)(omega_(r),k))/
      (pdv(Re(epsilon_(L)(omega,k)),omega))$.
    For a Maxwellian Langmuir branch at $k lambda_D << 1$,
    $gamma approx -sqrt(pi/8) omega_(p,e) exp(-3/2)
      (k lambda_D)^(-3) exp[-1/(2(k lambda_D)^2)]$.
    This is collisionless damping: no collision frequency appears. A positive
    velocity-space slope changes the sign of the resonant contribution and can
    turn damping into growth.]
  )

  #details(
    [Derivation: complex root and energy exchange],
    [#derivation-step[Expand the complex dispersion relation]
    Write

    $ epsilon_(L)(omega,k)=epsilon_(r)(omega,k)+i epsilon_(i)(omega,k) ,$

    and let $omega=omega_(r)+i gamma$. To first order in $gamma$,

    $ 0 approx epsilon_(r)(omega_(r),k)+i epsilon_(i)(omega_(r),k)+
      i gamma pdv(epsilon_(r)(omega,k),omega) .$

    Separating real and imaginary parts gives

    $ epsilon_(r)(omega_(r),k)=0, quad
      gamma=-epsilon_(i)(omega_(r),k)/
      (pdv(epsilon_(r)(omega,k),omega)) .$

    #derivation-step[Evaluate the Maxwellian contour contribution]
    Causal continuation gives

    $ Im(Z(zeta))=sqrt(pi) exp(-zeta^2) $

    for real positive $zeta$, while

    $ Re(Z(zeta)) approx -1/zeta-1/(2 zeta^3)-... .$

    The imaginary contribution near a positive phase velocity is therefore
    proportional to $zeta exp(-zeta^2)$. The real expansion supplies

    $ omega_r^2 approx omega_(p,e)^2[1+3(k lambda_D)^2] .$

    Put $a=k lambda_D$. Then $zeta=omega_r/(sqrt(2) a omega_(p,e))$,
    $epsilon_i=(sqrt(pi) zeta exp(-zeta^2))/a^2$, and
    $pdv(epsilon_r,omega) approx 2/omega_(p,e)$ at leading order.
    Use $zeta approx 1/(sqrt(2) a)$ in the prefactor but retain
    $zeta^2 approx 1/(2 a^2)+3/2$ in the exponential. The weak-rate
    formula then gives

    $ gamma/omega_(p,e) approx
      -sqrt(pi/8) a^(-3) exp(-1/(2 a^2)-3/2) .$

    #derivation-step[Interpret the sign by energy exchange]
    The field establishes correlations between particle phase and velocity.
    An ensemble with negative marginal slope at positive $v_"phi"$ absorbs
    net wave energy on this branch. The familiar slower/faster particle
    picture describes that phase-correlated ensemble exchange: an individual
    particle's instantaneous gain or loss also depends on its wave phase.
    A bump-on-tail can reverse the net exchange. Collisionless streaming
    transfers the perturbation into progressively finer velocity-space
    structure, allowing the coherent field to decay without collisional loss
    of the total particle-plus-field energy.

    #derivation-step[Relate temporal and spatial descriptions]
    Expand a real-frequency dispersion relation around a temporal root:

    $ omega(k_r+i k_i) approx omega_r+i gamma+i k_i v_"g" .$

    Holding $omega$ real requires $gamma+k_i v_"g"=0$, hence

    $ k_i=-gamma/v_"g" .$

    This relation applies to a simple branch with small damping and nonzero
    group velocity.]
  )

  #hot-isotropic-dispersion

  #animation(
    "../media/landau-resonance.mp4",
    "The left panel follows one integrated electron characteristic in a prescribed traveling wave, plotted in wave-frame position and velocity. Dashed curves mark its trapping geometry. The right panel marks the negative slope of a normalized Maxwellian marginal at the phase velocity. The particle orbit illustrates resonance and trapping; it does not simulate ensemble Landau damping or wave feedback.",
    caption: [
      Landau damping is a phase-correlated exchange between a wave and
      particles near its phase velocity. The orbit panel instead follows one
      finite-amplitude test electron without wave feedback, using
      $X=x/L_0$, $V=v/v_0$, $tau=(t v_0)/L_0$,
      $dv(X,tau)=V$, and $dv(V,tau)=-0.18 sin(X-0.92 tau)$.
      It starts at $X=-1.4$, $V=1.12$ and displays
      $X-0.92 tau$ and $V-0.92$. The field scale is
      $E_0=(m_e v_0^2)/(e L_0)$; $L_0$ and $v_0$ are reference length
      and speed. In the distribution panel $v_0=v_"te"$;
      the plotted $f_0$ is the marginal $F_(e,0)$ defined above, with
      $(F_(e,0) v_0)/n_0=exp(-V^2)/sqrt(pi)$.
    ],
    poster: "../media/landau-resonance.png",
  )

  #rechenbeispiel[
    For a forward packet use a temporal rate
    $gamma=-qty("1.13e8", "s^-1")$ and group velocity
    $v_"g"=qty("1.00e6", "m/s")$. Use the weak-rate
    conversion $k_i approx (-gamma)/v_"g"$, with
    $L_"amp"=1/k_i$ and $tau_"d"=1/abs(gamma)$. Determine the spatial
    attenuation rate, amplitude attenuation length, and temporal damping time.

    Numerical result: $k_i approx qty("113", "m^-1")$,
    $L_"amp" approx qty("8.85e-3", "m")$, and
    $tau_"d" approx qty("8.85e-9", "s")$.
  ]

  #interpretation(
    [Damping is a collective collisionless process],
    [Landau damping does not require binary collisions or entropy production
    through a collisional operator. The phase mixing of a reversible Vlasov
    system moves perturbation energy into fine velocity-space structure. A
    coarse-grained field measurement sees attenuation even though the
    underlying collisionless equation is Hamiltonian.]
  )

  #summary[
    A complex kinetic root has a real oscillation frequency and an imaginary
    rate. On the declared convention $gamma<0$ damps the wave. The rate is
    fixed by the imaginary resonant response divided by the slope of the real
    dispersion function; for a forward Maxwellian Langmuir wave this is the
    familiar Landau-damping asymptote.
  ]

  #knowledge-check((
    (
      question: [Why is Landau damping called collisionless damping?],
      answer: [Its rate comes from the resonant contour contribution of the Vlasov response, not from a binary-collision frequency. Phase mixing transfers coherent wave energy into fine velocity-space structure.]
    ),
    (
      question: [How are temporal and spatial attenuation related for a forward packet?],
      answer: [For small rates and group velocity $v_"g">0$, the fixed-frequency spatial rate is $k_i approx -gamma/v_"g"$. Thus temporal damping with $gamma<0$ gives positive spatial attenuation.]
    ),
    (
      question: [What must be true for the weak-rate expansion to be reliable?],
      answer: [The complex correction must be small compared with the real frequency, the real root must be simple, and the distribution and contour contribution must vary smoothly enough for a first-order expansion.]
    ),
    (
      question: [How can a collisionless wave grow instead of damp?],
      answer: [A non-equilibrium distribution can have a positive slope at the resonant velocity. Then resonant particles lose net energy to the wave, making $gamma>0$ on the present convention.]
    ),
  ))

  #section-title[Transverse kinetic waves] <hot-transverse-waves>

  #lead[
    The kinetic response is not restricted to electrostatic oscillations. For
    a transverse electromagnetic wave, the magnetic part of the wave force
    acts on an anisotropic equilibrium distribution even when the
    equilibrium field is zero. For isotropic $f_(s,0)$ its velocity gradient
    is parallel to $bold(v)$, so the magnetic force dotted into that gradient
    vanishes. The resulting dispersion relation recovers the cold plasma cutoff,
    while an anisotropic distribution can turn the transverse branch unstable.
  ]

  #objectives((
    [derive the transverse kinetic response from the Vlasov and Maxwell equations],
    [recover the cold unmagnetized electromagnetic dispersion relation],
    [identify the pole that can produce transverse wave damping or growth],
    [show how a perpendicular velocity-space anisotropy supplies free energy],
  ))

  #unit-ledger[
    The phase-space density $f_(s,0)$ is in #unit("m^-6 s^3"). The ratios $k
    c/omega_(p,s)$, $omega/omega_(p,s)$, and $v_x^2/c^2$ are dimensionless.
  ]

  #assumption(
    [Unmagnetized transverse plane wave],
    [Use a homogeneous collisionless plasma with
    $bold(B)_0=bold(0)$ and a small wave with
    $bold(k)=k bold(e)_z$ and $bold(E)_1=E_(1,x) bold(e)_x$.
    Then $bold(k) dot bold(E)_1=0$ and the wave magnetic field is determined
    by Faraday's law. The equilibrium can be isotropic for the ordinary
    branch or anisotropic when testing a free-energy-driven instability.
    Require reflection symmetry separately in $v_x$ and $v_y$ with these
    axes as principal directions. Then the response driven by $E_(1,x)$ is
    odd in $v_x$ and even in $v_y$, so its density, $J_(1,y)$, and
    $J_(1,z)$ vanish. This decouples the scalar transverse dispersion;
    a general anisotropic equilibrium requires the full dielectric matrix.]
  )

  #definition(
    [Transverse polarization],
    [A transverse mode has its electric field perpendicular to the propagation
    direction. With the stated geometry, Faraday's law gives
    $bold(B)_1=k/omega E_(1,x) bold(e)_y$.
    The perturbed current is obtained from the first velocity moment of
    $f_(s,1)$, so the kinetic dielectric response depends on the full
    equilibrium distribution rather than on density and temperature alone.]
  )

  #governing-law(
    [Transverse kinetic dispersion relation],
    [For a species equilibrium $f_(s,0)(bold(v))$, the transverse normal modes
    satisfy
    $k^2 c^2=omega^2+
      sum_s q_s^2/(epsilon_0 m_s)
      integral_(RR^3) [
        v_x pdv(f_(s,0)(bold(v)),v_x)+
        (k v_x^2)/(omega-k v_z)
          pdv(f_(s,0)(bold(v)),v_z)
      ] dif^3 bold(v)$.
    If the distribution decays at velocity-space infinity, integration by
    parts gives the equivalent form
    $k^2 c^2=omega^2-
      sum_s omega_(p,s)^2-
      sum_s (q_s^2 k^2)/(epsilon_0 m_s)
      integral_(RR^3) [
        (v_x^2 f_(s,0)(bold(v)))/((omega-k v_z)^2)
      ] dif^3 bold(v)$,
    where $omega_(p,s)^2=(n_s q_s^2)/(epsilon_0 m_s)$. The velocity integral uses
    the causal contour when the pole $omega-k v_z=0$ lies on the integration
    path.]
  )

  #details(
    [Derivation: transverse current and cold limit],
    [#derivation-step[Linearize and solve the transverse Vlasov equation]
    For the Fourier convention $exp(i (k z-omega t))$, the linearized Vlasov
    equation for the transverse geometry is

    $ -i(omega-k v_z) f_(s,1)+
        (q_s/m_s) E_(1,x) [
          (1-(k v_z)/omega) pdv(f_(s,0),v_x)+
          (k v_x)/omega pdv(f_(s,0),v_z)
        ] = 0 .$

    Solving for the distribution perturbation gives

    $ f_(s,1)=(-i q_s E_(1,x))/(m_s omega)
        [
          (omega-k v_z) pdv(f_(s,0),v_x)+
          k v_x pdv(f_(s,0),v_z)
        ]/(omega-k v_z) .$

    #derivation-step[Insert the distribution into the current]
    The transverse current is

    $ J_(1,x)=sum_s q_s integral_(RR^3) v_x f_(s,1) dif^3 bold(v) .$

    Substitution into the transverse component of Ampere's law gives

    $ k^2 c^2=omega^2+
        sum_s q_s^2/(epsilon_0 m_s) integral_(RR^3) [
          v_x pdv(f_(s,0),v_x)+
          (k v_x^2)/(omega-k v_z) pdv(f_(s,0),v_z)
        ] dif^3 bold(v) .$

    #derivation-step[Integrate the velocity derivative by parts]
    To integrate the second term by parts, use

    $ pdv((1)/(omega-k v_z),v_z)=k/((omega-k v_z)^2) .$

    The boundary terms vanish for a decaying distribution. The two needed
    identities are

    $ integral_(RR^3) v_x pdv(f_(s,0),v_x) dif^3 bold(v)=-n_s $

    and

    $ integral_(RR^3) (k v_x^2)/(omega-k v_z)
        pdv(f_(s,0),v_z) dif^3 bold(v)=
        -integral_(RR^3) [
          (k^2 v_x^2 f_(s,0))/((omega-k v_z)^2)
        ] dif^3 bold(v) .$

    These identities produce the equivalent governing law

    $ k^2 c^2=omega^2-sum_s omega_(p,s)^2-
        sum_s (q_s^2 k^2)/(epsilon_0 m_s)
        integral_(RR^3) [
          (v_x^2 f_(s,0))/((omega-k v_z)^2)
        ] dif^3 bold(v) .$

    #derivation-step[Recover the cold electromagnetic branch]
    For a cold equilibrium

    $ f_(s,0)=n_s delta(v_x) delta(v_y) delta(v_z) ,$

    the resonant integral containing $v_x^2$ vanishes in the distributional
    limit. Therefore

    $ k^2 c^2=omega^2-sum_s omega_(p,s)^2 ,$

    or

    $ omega^2=k^2 c^2+sum_s omega_(p,s)^2 .$

    This is the cold electromagnetic cutoff already obtained from the fluid
    model.]
  )

  #governing-law(
    [Anisotropic transverse instability],
    [For an electron population with fixed neutralizing ions, take an
    equilibrium of the form
    $f_(0)(bold(v))=delta(v_z) F(v_x,v_y)$ with
    $n_0=integral_(RR^2) F(v_x,v_y) dif v_x dif v_y$ and
    $⟨v_x^2⟩=(1/n_0) integral_(RR^2) v_x^2 F(v_x,v_y)
      dif v_x dif v_y$.
    The transverse relation becomes
    $k^2 c^2=omega^2-omega_p^2 [1+(k^2 ⟨v_x^2⟩)/(omega^2)]$.
    Equivalently,
    $omega^4-(k^2 c^2+omega_p^2)omega^2-
      k^2 omega_p^2 ⟨v_x^2⟩=0$.
    The lower value of $omega^2$ is negative whenever
    $k != 0$ and $⟨v_x^2⟩>0$, so this idealized anisotropy contains a growing transverse
    mode. The instability is powered by the anisotropic velocity-space free
    energy.]
  )

  #details(
    [Derivation: the negative transverse branch],
    [#derivation-step[Evaluate the kinetic correction]
    For the stated equilibrium, the pole denominator is independent of the
    nonzero perpendicular velocities because $v_z=0$. The integrated form of
    the dispersion relation therefore gives

    $ integral_(RR^3) [
        (v_x^2 f_(0)(bold(v)))/((omega-k v_z)^2)
      ] dif^3 bold(v)=n_0 ⟨v_x^2⟩/omega^2 .$

    Inserting this result together with

    $ omega_p^2=(n_0 e^2)/(epsilon_0 m_e) $

    yields the quartic governing the transverse branch.

    #derivation-step[Solve the quartic as a quadratic in frequency squared]
    Set $Y=omega^2$. The two roots are

    $ Y_±=[(k^2 c^2+omega_p^2) ±
        sqrt((k^2 c^2+omega_p^2)^2+
          4 k^2 omega_p^2 ⟨v_x^2⟩)]/2 .$

    Since the square root is larger than $k^2 c^2+omega_p^2$ when
    $k != 0$ and $⟨v_x^2⟩>0$, the lower root satisfies $Y_-<0$.

    #derivation-step[Convert the negative root to a growth rate]
    Writing $omega=i gamma$ on the growing member gives

    $ gamma^2=[sqrt((k^2 c^2+omega_p^2)^2+
          4 k^2 omega_p^2 ⟨v_x^2⟩)-
        (k^2 c^2+omega_p^2)]/2 .$

    Thus the idealized anisotropy produces exponential growth. A finite
    parallel temperature, collisions, magnetic field, or nonlinear
    redistribution changes this branch and must be included before applying
    the formula to a particular plasma.]
  )

  #rechenbeispiel[
    Use an electron plasma with $n_0=qty("1.0e16", "m^-3")$,
    $e=qty("1.602e-19", "C")$,
    $m_e=qty("9.109e-31", "kg")$,
    $epsilon_0=qty("8.854e-12", "F/m")$, and
    $c=qty("2.998e8", "m/s")$. Let
    #normalized-label[$(k c)/omega_p=qty("0.50", "1")$] and
    #normalized-label[ $⟨v_x^2⟩/c^2=qty("1.00e-2", "1")$ ].
    Determine $k$, the wavelength, and the positive growth rate of the
    anisotropic transverse branch.

    Numerical result: $omega_p approx qty("5.64e9", "s^-1")$,
    $k approx qty("9.41", "m^-1")$,
    $lambda approx qty("0.668", "m")$,
    #normalized-label[$gamma/omega_p approx qty("4.47e-2", "1")$], and
    $gamma approx qty("2.52e8", "s^-1")$.
  ]

  #interpretation(
    [Velocity spread in the transverse response],
    [The cold cutoff depends only on the total plasma frequency. The kinetic
    correction samples perpendicular velocity spread and the pole at the
    parallel phase velocity. An isotropic distribution usually leaves the
    ordinary high-frequency branch stable in the nonrelativistic model, while
    anisotropy can release free energy into a transverse perturbation.]
  )

  #summary[
    A transverse kinetic wave follows from the Vlasov response together with
    Maxwell's equations. Its cold limit is
    $omega^2=k^2 c^2+sum_s omega_(p,s)^2$; finite velocity spread adds a
    resonant integral. An anisotropic distribution can make the lower
    transverse branch have $omega^2<0$, producing growth from velocity-space
    free energy.
  ]

  #knowledge-check((
    (
      question: [What distinguishes a transverse kinetic wave from the longitudinal calculation?],
      answer: [The electric field is perpendicular to $bold(k)$, so the wave magnetic field contributes to the Lorentz force and the current must be coupled to Maxwell's transverse wave equation rather than only to Poisson's equation.]
    ),
    (
      question: [Which limit gives the cold electromagnetic cutoff?],
      answer: [Taking each equilibrium toward a cold velocity-space delta distribution removes the finite-velocity integral and gives $omega^2=k^2 c^2+sum_s omega_(p,s)^2$.]
    ),
    (
      question: [Why does the transverse kinetic response contain a squared resonant denominator after integration by parts?],
      answer: [Integration by parts moves the velocity derivative from the distribution to $1/(omega-k v_z)$, producing $k/((omega-k v_z)^2)$. This is the same response in an equivalent form; it retains the original causal contour prescription.]
    ),
    (
      question: [What supplies the free energy in the anisotropic transverse example?],
      answer: [The unequal velocity-space spread, represented here by a finite perpendicular second moment and a cold parallel direction, stores free energy that can be transferred to the growing transverse field.]
    ),
  ))

  #section-title[Two-stream instability] <two-stream-instability>

  #lead[
    A distribution with two separated beams is unstable to electrostatic
    perturbations. The electrostatic field couples the streams, and for a range of
    wavelengths the two real oscillatory branches merge into a complex pair.
    The negative value of $omega^2$ on the lower branch is the algebraic signal
    of exponential growth.
  ]

  #objectives((
    [construct the cold symmetric two-stream distribution],
    [derive its longitudinal dispersion relation and solve for $omega^2$],
    [identify the unstable wave-number interval],
    [locate the maximum normalized growth rate],
  ))

  #unit-ledger[
    The total density $n_0$ is in #unit("m^-3"), beam speed $v_0$ and the
    light speed $c$ are in #unit("m/s"), $k$ is in #unit("m^-1"), and
    $omega$, $gamma$, and $omega_p$ are in #unit("s^-1"). The wavelength is
    in #unit("m"). The normalized variables
    $(k v_0)/omega_p$, $omega/omega_p$, and $gamma/omega_p$ are dimensionless.
  ]

  #assumption(
    [Cold symmetric electron beams],
    [Use two equal electron beams with densities $n_0/2$ and velocities
    $+v_0$ and $-v_0$ along $bold(e)_z$. Ions form a fixed neutralizing
    background, the plasma is unmagnetized and collisionless, and the wave is
    one-dimensional and electrostatic. The total electron plasma frequency is
    $omega_p^2=(n_0 e^2)/(epsilon_0 m_e)$.]
  )

  #definition(
    [Two-stream equilibrium],
    [The one-dimensional equilibrium can be written
    $F_(e,0)(v)=(n_0/2) [delta(v-v_0)+delta(v+v_0)]$,
    the marginal along the beams, with units #unit("m^-4 s") and
    $integral F_(e,0)(v) dif v=n_0$.
    The delta functions idealize cold beams. A finite beam temperature replaces
    them by narrow distributions and introduces thermal spreading, resonant
    damping, and additional kinetic structure.]
  )

  #governing-law(
    [Cold two-stream dispersion],
    [With $x=((k v_0)/omega_p)^2$, the dispersion relation is
    $D(omega,k)=1-(omega_p^2)/(2(omega-k v_0)^2)-
      (omega_p^2)/(2(omega+k v_0)^2)=0$.
    Its two values of $omega^2$ are
    $omega^2/omega_p^2=x+1/2 ± (sqrt(1+8x))/2$.
    The lower branch is negative when $0<x<1$, so
    $gamma/omega_p=[(sqrt(1+8x))/2-x-1/2]^(1/2)$ in that interval.
    The maximum occurs at $x=3/8$ and has
    $gamma_"max"/omega_p=1/(2 sqrt(2))$.]
  )

  #details(
    [Derivation: symmetric beams and the unstable branch],
    [#derivation-step[Write the response of the two cold beams]
    For the two delta-function beams, insert the equilibrium into the
    first-derivative form of the electrostatic susceptibility. Equivalently,
    each cold beam responds as a cold fluid whose equilibrium drift shifts the
    frequency to $omega-k v_0$ or $omega+k v_0$. The total response is

    $ D(omega,k)=1-(omega_p^2)/(2(omega-k v_0)^2)-
        (omega_p^2)/(2(omega+k v_0)^2) .$

    #derivation-step[Clear the beam denominators]
    Multiply by $(omega^2-k^2 v_0^2)^2$ and collect powers of $omega^2$:

    $ omega^4-(2 k^2 v_(0)^(2)+omega_p^2)omega^2+
        k^2 v_(0)^(2) (k^2 v_(0)^(2)-omega_p^2)=0 .$

    Define the dimensionless variables

    $ x=(k^2 v_0^2)/(omega_p^2), quad
      y=omega^2/omega_p^2 .$

    Dividing by $omega_p^4$ gives

    $ y^2-(2x+1)y+x(x-1)=0 .$

    The quadratic formula yields

    $ y_±=x+1/2 ± (sqrt(1+8x))/2 .$

    #derivation-step[Identify the unstable interval]
    The upper branch is positive for all $x>=0$. For the lower branch,
    $y_-<0$ precisely when

    $ sqrt(1+8x)>1+2x .$

    Both sides are nonnegative, so squaring gives

    $ 1+8x>1+4x+4x^2 ,$

    or $0<x<1$. In that interval write $omega=i gamma$ and obtain

    $ gamma/omega_p=sqrt(-y_-) .$

    #derivation-step[Locate the maximum growth rate]
    To locate the maximum, differentiate

    $ gamma^2/omega_p^2=(sqrt(1+8x))/2-x-1/2 .$

    The derivative vanishes when $2/sqrt(1+8x)=1$, so $x=3/8$.
    Substitution gives

    $ gamma^2/omega_p^2=1/8 ,$

    and therefore

    $ gamma_"max"/omega_p=1/(2 sqrt(2)) .$

    The instability draws on the relative drift energy. Beam temperature,
    collisions, boundaries, and nonlinear trapping all modify this ideal
    result.]
  )

  #two-stream-growth

  #animation(
    "../media/two-stream-instability.mp4",
    "Two cold beams are marked at v/v0 equal to plus and minus one. A separate normalized field axis shows a sinusoid with fixed spatial phase and exponentially growing amplitude. Beside it, the growth-rate curve vanishes at the unstable-band boundaries and marks its maximum. This is a prescribed linear eigenmode, not a particle-in-cell simulation.",
    caption: [
      Counter-streaming beams can convert directed kinetic energy into an
      electrostatic wave. The growth curve is the cold symmetric two-stream
      result in normalized variables. The field uses
      $X=(x omega_p)/v_0$, $tau=omega_p t$, and
      $E_0=(m_e v_0 omega_p)/e$, with $omega_p$ based on total beam density.
      At $K=(k v_0)/omega_p=sqrt(3/8)$ it is
      $E/E_0=0.01 exp(tau/(2 sqrt(2))) sin(K X)$: its real frequency is zero.
    ],
    poster: "../media/two-stream-instability.png",
  )

  #rechenbeispiel[
    Let $n_0=qty("1.0e16", "m^-3")$,
    #normalized-label[$v_0/c=qty("0.10", "1")$] with
    $c=qty("2.998e8", "m/s")$, and choose
    #normalized-label[$(k v_0)/omega_p=qty("0.50", "1")$]. Use
    $e=qty("1.602e-19", "C")$,
    $m_e=qty("9.109e-31", "kg")$, and
    $epsilon_0=qty("8.854e-12", "F/m")$. Determine $k$, the wavelength, and the
    positive growth rate.

    Numerical result: $omega_p approx qty("5.64e9", "s^-1")$,
    $k approx qty("94.1", "m^-1")$,
    $lambda approx qty("6.68e-2", "m")$,
    #normalized-label[$gamma/omega_p approx qty("0.341", "1")$], and
    $gamma approx qty("1.92e9", "s^-1")$.
  ]

  #interpretation(
    [A negative squared frequency gives growth and decay],
    [At short wavelengths the two beams support ordinary oscillatory roots. In
    the unstable band, the lower root crosses through $omega=0$ and becomes a
    purely imaginary pair. One member grows and the other decays; the physical
    initial-value problem selects their combination from the initial
    perturbation.]
  )

  #summary[
    The cold symmetric two-stream model has a finite unstable band
    $0<(abs(k v_0))/omega_p<1$. The maximum growth rate is
    $omega_p/(2 sqrt(2))$, reached at
    $(abs(k v_0))/omega_p=sqrt(3/8)$. Finite temperature and kinetic phase
    mixing determine how this ideal beam instability is modified.
  ]

  #knowledge-check((
    (
      question: [What supplies the free energy in the two-stream instability?],
      answer: [The relative directed kinetic energy of the counter-streaming beams supplies free energy. The electrostatic perturbation extracts it when the beam response makes the lower branch have negative $omega^2$.]
    ),
    (
      question: [Why is the unstable interval finite in wave number?],
      answer: [For $(abs(k v_0))/omega_p>1$, both squared-frequency branches are positive. The lower branch reaches zero at the boundary and becomes negative only for $0<(abs(k v_0))/omega_p<1$. Thus the boundary itself is marginal, not oscillatory.]
    ),
    (
      question: [What does a positive imaginary frequency mean here?],
      answer: [With $exp(-i omega t)$, a root $omega=i gamma$ with $gamma>0$ gives $exp(gamma t)$, so its amplitude grows exponentially in time.]
    ),
    (
      question: [Which idealization is most directly relaxed by giving the beams a finite temperature?],
      answer: [The delta-function velocity distributions become narrow but smooth profiles. Thermal spread then introduces phase mixing and resonant corrections that can reduce, shift, or reshape the cold growth band.]
    ),
  ))

  #section-title[Hot magnetized waves and branch interpretation] <hot-magnetized-waves>

  #lead[
    A magnetic field adds another way for particles to stay in phase with a
    perturbation. They stream along the field while gyrating across it, so the
    resonance condition contains both a Doppler shift and an integer cyclotron
    harmonic. Cold-fluid branches provide reference limits for interpreting
    the kinetic spectrum, while Landau and cyclotron resonances explain how
    velocity spread changes the response.
  ]

  #objectives((
    [state the equilibrium condition for a gyrotropic distribution],
    [expand the perturbed distribution into gyroangle harmonics],
    [derive the Doppler-shifted cyclotron resonance condition],
    [connect hot magnetized branch changes to velocity-space gradients],
  ))

  #unit-ledger[
    For a characteristic perpendicular speed $v_(perp,"s")$, define the
    thermal gyroradius $rho_s=v_(perp,"s")/abs(Omega_s)$, which is in
    #unit("m"). Harmonic number $n$, $k_perp rho_s$, $omega/abs(Omega_s)$, and
    the resonance condition after division by a frequency are dimensionless.
    The individual orbit radius $r_(L,s)=v_perp/abs(Omega_s)$ is in #unit("m")
    and varies across the velocity integral; it differs from the thermal scale
    $rho_s$.
  ]

  #assumption(
    [Homogeneous gyrotropic magnetized equilibrium],
    [Use a collisionless homogeneous plasma with
    $bold(B)_0=B_0 bold(e)_z$ and an equilibrium
    $f_(s,0)(v_(parallel),v_(perp))$ independent of gyroangle. Begin with
    parallel propagation to expose the harmonic denominators; finite
    $k_perp rho_s$ introduces Bessel factors and finite-Larmor-radius effects.
    For thermal estimates, take $v_(perp,"s")$ to be the characteristic
    perpendicular thermal speed of species $s$.]
  )

  #definition(
    [Gyroangle harmonic response],
    [Define the signed gyrofrequency
    $Omega_s=(q_s B_0)/m_s$. Choose
    $v_x=v_perp cos(theta)$ and $v_y=-v_perp sin(theta)$, so increasing
    $theta$ rotates from positive $x$ toward negative $y$ and
    $dv(theta,t)=Omega_s$. Thus $theta=-theta_"std"$, where the glossary's
    usual counterclockwise angle has $v_y=v_perp sin(theta_"std")$ and
    $dv(theta_"std",t)=-Omega_s$. These are two coordinates for the same
    physical orbit. Write the perturbed distribution as
    $f_(s,1)=sum_(n=-infinity)^infinity
      f_(s,1,n)(v_(parallel),v_(perp)) exp(i n theta)$.
    The integer $n$ counts the number of gyroangle phase windings sampled by
    the perturbation. The harmonic $n=0$ is the parallel Landau resonance;
    nonzero $n$ are cyclotron harmonics.]
  )

  #governing-law(
    [Doppler-shifted cyclotron resonance],
    [The hot magnetized response contains denominators of the form
    $omega-k_(parallel) v_(parallel)-n Omega_s$.
    Resonant particles satisfy
    $omega_r-k_(parallel) v_(parallel)-n Omega_s=0$,
    so
    $v_(parallel,"res")=(omega_r-n Omega_s)/k_(parallel)$ when
    $k_(parallel) != 0$. The harmonic weights depend on the equilibrium
    velocity-space gradients and, for oblique propagation, on
    the signed orbit argument $a_s=(k_perp v_perp)/Omega_s$ through Bessel
    functions $J_n$ of the first kind, with $abs(a_s)=k_perp r_(L,s)$.
    These weights describe how strongly an orbit couples to each harmonic.
    A branch can therefore be
    damped, amplified, or strongly refracted near a resonance even when its
    cold-fluid counterpart is smooth.]
  )

  #details(
    [Derivation: gyroangle harmonics and resonant denominators],
    [#derivation-step[Characterize the unperturbed gyro-orbit]
    The unperturbed characteristic equations in a uniform field are

    $ dv(v_(parallel),t)=0, quad
      dv(v_(perp),t)=0, quad
      dv(theta,t)=Omega_s .$

    Indeed, differentiating $v_x=v_perp cos(theta)$ and
    $v_y=-v_perp sin(theta)$ gives $dv(v_x,t)=Omega_s v_y$ and
    $dv(v_y,t)=-Omega_s v_x$, the Lorentz-force components $dv(bold(v),t)=(q_s/m_s) bold(v) times bold(B)_0$.

    A stationary gyrotropic equilibrium therefore satisfies

    $ Omega_s pdv(f_(s,0),theta)=0 ,$

    and can depend on $v_(parallel)$ and $v_(perp)$ but not on $theta$.

    #derivation-step[Expand the perturbed distribution in harmonics]
    Linearize the Vlasov equation about this equilibrium and write the
    perturbed distribution as a Fourier harmonic in time, space, and gyroangle.
    The streaming and gyroangle pieces of the operator become

    $ pdv(f,t)+v_(parallel) pdv(f,z)+Omega_s pdv(f,theta)
        -> -i(omega-k_(parallel)v_(parallel)-n Omega_s) f .$

    Define $S_(s,n)$ as the harmonic of the negative perturbed-force term,
    so $-i(omega-k_(parallel)v_(parallel)-n Omega_s)f_(s,1,n)=S_(s,n)$.
    Its response is

    $ f_(s,1,n)=(i S_(s,n))/
        [omega-k_(parallel)v_(parallel)-n Omega_s] .$

    #derivation-step[Identify the parallel and cyclotron harmonics]
    For parallel propagation, the transverse electric field decomposes into
    circular polarizations. The $n=+1$ and $n=-1$ terms are selected by the
    corresponding sense of gyromotion, while $n=0$ describes parallel motion.
    In chapter 12's circular basis $E_y=-i sigma E_x$ with $sigma=plus.minus 1$,
    $bold(E)_perp dot bold(v)_perp=E_x v_perp exp(i sigma theta)$.
    Thus that circular forcing selects $n=sigma$; for electrons the
    positive-frequency cyclotron pole has $n=-1$ because $Omega_e<0$.
    The resonance condition is therefore

    $ omega-k_(parallel)v_(parallel)-n Omega_s=0 .$

    #derivation-step[Add finite-Larmor-radius weights]
    For oblique propagation take $bold(k)_perp=k_perp bold(e)_x$. Integrating
    $dv(x,t)=v_perp cos(theta)$ with $dv(theta,t)=Omega_s$ gives
    $x=X+(v_perp/Omega_s) sin(theta)$, where $X$ is the guiding-center
    coordinate. The perpendicular phase factor along this individual orbit
    therefore expands as

    $ exp(i a_s sin(theta))=
        sum_n J_(n)(a_s) exp(i n theta), quad
      a_s=(k_perp v_perp)/Omega_s .$

    Finite-Larmor-radius physics thus supplies Bessel weights but leaves the
    same Doppler-shifted cyclotron denominator. These weights remain inside
    the velocity integral. The thermal $k_perp rho_s$ estimates their
    importance but cannot replace the individual velocity-dependent argument.

    #derivation-step[Interpret the contour contribution]
    The contour prescription around each pole gives an imaginary contribution
    proportional to the appropriate derivative of the equilibrium. In an
    isotropic Maxwellian the parallel $n=0$ resonance gives Landau damping on
    the usual positive-frequency branch. An anisotropic distribution can have
    a gradient of the opposite sign, and cyclotron harmonics can then drive
    growth or produce strong absorption. Sending $B_0 -> 0$ removes the
    harmonic spacing and recovers the unmagnetized velocity-space response.]
  )

  #hot-magnetized-resonance

  #rechenbeispiel[
    For electrons in a $B_0=qty("1.0e-2", "T")$ field use
    $omega_"ce"=qty("1.76e9", "s^-1")$ as the positive electron gyrofrequency
    magnitude and $Omega_e=-omega_"ce"$. Let
    #normalized-label[$omega/omega_"ce"=qty("0.80", "1")$] and
    #normalized-label[$(k_(parallel) v_"te")/omega_"ce"=qty("1.50", "1")$],
    with
    $v_"te"=qty("1.88e6", "m/s")$. Report the resonant parallel velocities
    for $n=0$ and $n=-1$, normalized by $v_"te"$, and give
    $k_(parallel)$ and $omega$.

    Numerical result: for $n=0$,
    #normalized-label[$v_(parallel,"res")/v_"te"=qty("0.533", "1")$]; for
    $n=-1$,
    #normalized-label[$v_(parallel,"res")/v_"te"=qty("-0.133", "1")$];
    $k_(parallel) approx qty("1.40e3", "m^-1")$ and
    $omega approx qty("1.41e9", "s^-1")$.
  ]

  #interpretation(
    [Cold branches as reference limits],
    [The cold dielectric tensor identifies the principal wave branches and
    their polarizations. The hot tensor adds orbit averaging, Doppler shifts,
    harmonic resonances, and distribution gradients. A cold cutoff or
    resonance is therefore a location at which kinetic corrections should be
    checked first.]
  )

  #summary[
    Hot magnetized waves inherit their cold branch structure but acquire
    resonant denominators $omega-k_(parallel)v_(parallel)-n Omega_s$.
    The $n=0$ harmonic is Landau-like, nonzero harmonics are cyclotron-like,
    and the sign of the velocity-space gradient determines damping or growth.
    Oblique propagation additionally weights the harmonics through
    the individual orbit argument $(k_perp v_perp)/Omega_s$; the thermal
    $k_perp rho_s$ is only an ordering scale.
  ]

  #knowledge-check((
    (
      question: [What is the difference between a signed gyrofrequency and its positive magnitude?],
      answer: [The positive magnitude $omega_"c"=(abs(q) B)/m$ is a rate, while the signed $Omega=(q B)/m$ retains the charge-dependent sense of gyromotion and enters the harmonic resonance with its sign.]
    ),
    (
      question: [Which harmonic corresponds to the parallel Landau resonance?],
      answer: [The $n=0$ harmonic removes the cyclotron shift and gives $omega-k_(parallel)v_(parallel)=0$. Nonzero $n$ add gyrofrequency multiples and are cyclotron resonances.]
    ),
    (
      question: [Why do Bessel functions appear for oblique hot-plasma waves?],
      answer: [Each perpendicular orbit samples the oblique phase periodically. Its harmonic expansion gives Bessel weights with signed argument $(k_perp v_perp)/Omega_s$, whose magnitude is $k_perp r_(L,s)$. The thermal radius only estimates the ordering; the orbit radius varies over velocity space.]
    ),
    (
      question: [What can make a cold magnetized resonance physically finite?],
      answer: [Finite temperature, orbit averaging, collisions, and the analytic contour contribution spread or regularize the ideal cold response. The correct mechanism is selected by the relevant ordering and distribution.]
    ),
  ))

  #chapter-nav(
    previous: (href: "13-finite-temperature-waves.html", title: [Finite-temperature effects]),
    next: (href: "15-sheaths-probes.html", title: [Sheaths and probes]),
  )
]
