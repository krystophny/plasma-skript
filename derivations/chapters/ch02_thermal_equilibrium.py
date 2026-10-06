"""Entropy, reservoir weights, and hydrogen Saha equilibrium; original figures.

Constants: NIST CODATA 2022 (electron mass); exact h, k_B, e.
The adopted single-stage hydrogen model has chi=13.6 eV and gi=gn=1.
"""
import json
from pathlib import Path

import numpy as np
import sympy as sp
from notebook import agrees, report, section, show
from si import BLUE, ORANGE, GRAY, EXAMPLE_PLASMAS, figure, save, slide_width

k, h, T, E, V, N, m = sp.symbols("k_B h T E V N m", positive=True)
g, M, W, S = sp.symbols("g M W S", positive=True)

section("Counted entropy", script="thermal-microstates")
a, b = sp.symbols("a b", integer=True, positive=True)
sequence = sp.Function("W")
binary = sp.rsolve(sp.Eq(sequence(a+1),2*sequence(a)),sequence(a),{sequence(0):1})
agrees(binary,2**a,eq="thermal-binary-count")
agrees(sp.expand_log(k*sp.log(2**a*2**b), force=True),
       k*(a+b)*sp.log(2), eq="thermal-entropy")
assert [2**j for j in (1,2,3)] == [2,4,8]

section("Entropy slope and exchange", script="thermal-temperature")
ideal_entropy = k*N*sp.log(E)/2  # one quadratic degree of freedom per particle
inverse_T = sp.diff(ideal_entropy, E)
temperature = sp.solve(sp.Eq(inverse_T, 1/T), E)[0]
agrees(inverse_T.subs(E, temperature), 1/T, eq="thermal-temperature-definition")
EA, Et, CA, CB, TA, TB, dE = sp.symbols("E_A E_tot C_A C_B T_A T_B dE", positive=True)
SA, SB = sp.Function("S_A"), sp.Function("S_B")
exchange = sp.diff(SA(EA)+SB(Et-EA),EA)
exchange = exchange.subs(sp.diff(SA(EA),EA),1/TA)
exchange = exchange.replace(lambda z:isinstance(z,sp.Subs),lambda z:1/TB)
agrees(exchange*dE, (1/TA-1/TB)*dE, eq="thermal-exchange")
dS, dV, dN, dP, p, mu, flow = sp.symbols("dS dV dN dP p mu u")
entropy_diff = (dE+p*dV-mu*dN-flow*dP)/T
energy_diff = sp.solve(sp.Eq(dS,entropy_diff),dE)[0]
agrees(energy_diff,T*dS-p*dV+mu*dN+flow*dP,eq="thermal-first-law")

section("Reservoir and Maxwellian", script="thermal-boltzmann")
SR, chi = sp.symbols("S_rest chi", positive=True)
agrees(sp.exp((SR-E/T)/k),sp.exp(SR/k)*sp.exp(-E/(k*T)),eq="thermal-reservoir")
entropy = sp.Function("S_rest")
series = sp.series(entropy(Et-E), E, 0, 2).removeO().doit()
agrees(series.subs(sp.diff(entropy(Et),Et),1/T),entropy(Et)-E/T,
       eq="thermal-boltzmann-factor")
v1, v2, mean = sp.symbols("v_1 v_2 u", real=True)
kin = m*(v1*v1+v2*v2)/2
split = (m*(v1+v2))**2/(4*m) + m*((v1-mean)**2+(v2-mean)**2)/2
agrees(split.subs(mean,(v1+v2)/2),kin,eq="thermal-flow-energy")
v, u = sp.symbols("v u", real=True)
vt = sp.sqrt(2*k*T/m)
oneD = sp.exp(-(v-u)**2/vt**2)/(sp.sqrt(sp.pi)*vt)
agrees(sp.integrate(oneD,(v,-sp.oo,sp.oo)),1,eq="thermal-maxwellian")
assert sp.simplify(sp.integrate((v-u)**2*oneD,(v,-sp.oo,sp.oo))) == k*T/m

section("Slots and one ionization", script="thermal-saha")
ps = sp.Symbol("p_s", positive=True)
lambda_naive = h/ps
agrees(lambda_naive,h/ps,eq="thermal-mode-estimate")
pth = sp.sqrt(2*m*k*T)
agrees(lambda_naive.subs(ps,pth)/(h/sp.sqrt(2*sp.pi*m*k*T)),
       sp.sqrt(sp.pi),eq="thermal-wavelength")
px = sp.Symbol("p_x",real=True)
momentum_integral = sp.integrate(sp.exp(-px**2/(2*m*k*T)),(px,-sp.oo,sp.oo))
momentum_volume = sp.simplify(momentum_integral**3)
agrees(momentum_volume,(2*sp.pi*m*k*T)**sp.Rational(3,2),
       eq="thermal-momentum-volume")
lambda_th_s = h/sp.sqrt(2*sp.pi*m*k*T)
agrees(lambda_th_s,h/(sp.sqrt(sp.pi)*m*vt),eq="thermal-wavelength")
slots = g*V/h**3*momentum_volume
agrees(slots,g*V/lambda_th_s**3,eq="thermal-slots")
ns = sp.Symbol("n_s",positive=True)
agrees(slots/(ns*V),g/(ns*lambda_th_s**3),eq="thermal-slots")
naive_slots = g*V/lambda_naive.subs(ps,pth)**3
agrees(slots/naive_slots,sp.pi**sp.Rational(3,2),
       eq="thermal-slot-volume-correction")
population = sp.Symbol("N_s",integer=True,positive=True)
count = M**population/sp.factorial(population)
# Fermion and boson slot counts have the same dilute leading coefficient.
for particles in range(1,7):
    for exact in (sp.prod(M-j for j in range(particles)),
                  sp.prod(M+j for j in range(particles))):
        leading=sp.Poly(sp.expand(exact/sp.factorial(particles)),M).LC()
        agrees(leading*M**particles,count.subs(population,particles),eq="thermal-dilute-count")
addition = sp.simplify(count.subs(population,population+1)/count)
removal = sp.simplify(count.subs(population,population-1)/count)
agrees(addition,M/(population+1),
       eq="thermal-add-remove")
agrees(removal,population/M,
       eq="thermal-remove")
nn, ni, ne, gn, gi, ge, ln, li, le = sp.symbols(
    "n_n n_i n_e g_n g_i g_e lambda_th_n lambda_th_i lambda_th_e",positive=True)
exact_ratio = (removal.subs({M:gn*V/ln**3,population:nn*V}) *
               addition.subs({M:gi*V/li**3,population:ni*V}) *
               addition.subs({M:ge*V/le**3,population:ne*V}))
R = sp.limit(exact_ratio,V,sp.oo)*sp.exp(-chi/(k*T))
agrees(R, (nn*ln**3/gn)*(gi/(ni*li**3))*(ge/(ne*le**3))*sp.exp(-chi/(k*T)),
       eq="thermal-ionization-ratio")
heavy_state_factor=(ln/li)**3*gi/gn
agrees(heavy_state_factor.subs({ln:li,gi:1,gn:1}),1,
       eq="thermal-translational-cancellation")
heavy_cancel = sp.simplify(R.subs({ln:li,ge:2}))
agrees(heavy_cancel,2*nn*gi/(gn*ni*ne*le**3)*sp.exp(-chi/(k*T)),eq="thermal-heavy-cancellation")
balance = sp.solve(sp.Eq(heavy_cancel,1),ni)[0]*ne/nn
agrees(balance,2*gi/(gn*le**3)*sp.exp(-chi/(k*T)),eq="thermal-saha-equation")
me = sp.Symbol("m_e",positive=True)
expanded_saha = balance.subs({gi:1,gn:1,le:h/sp.sqrt(2*sp.pi*me*k*T)})
agrees(expanded_saha,
       2*(2*sp.pi*me*k*T/h**2)**sp.Rational(3,2)*sp.exp(-chi/(k*T)),
       eq="thermal-saha-electron-mass")

section("Ionization fraction and threshold", script="thermal-ionization")
x, A, n = sp.symbols("x A n",positive=True)
ratio = sp.simplify((ni*ne/nn).subs({ni:x*n,ne:x*n,nn:(1-x)*n})/n)
agrees(ratio,x**2/(1-x),eq="thermal-fraction-balance")
solution = 2/(1+sp.sqrt(1+4/A))
assert sp.simplify(solution**2/(1-solution)-A) == 0
agrees(solution,2*A/(A+sp.sqrt(A*A+4*A)),eq="thermal-fraction-solution")
half_balance = sp.simplify(ratio.subs(x,sp.Rational(1,2)))
assert half_balance == sp.Rational(1,2)
agrees(sp.solve(sp.Eq(2/(n*le**3)*sp.exp(-chi/(k*T)),half_balance),chi)[0],
       k*T*sp.log(4/(n*le**3)),eq="thermal-half-temperature")

# Numerical oracle: solve the logarithmic balance by bisection, then check
# against the independent closed Lambert-W solution (no scipy dependency).
H, ME, KB, EV = 6.62607015e-34, 9.1093837139e-31, 1.380649e-23, 1.602176634e-19
CHI = 13.6*EV
KELVIN_PER_EV = EV/KB


def wavelength(temp):
    return H/np.sqrt(2*np.pi*ME*KB*np.asarray(temp))


def log_balance(temp,density):
    return np.log(2/density)-3*np.log(wavelength(temp))-CHI/(KB*np.asarray(temp))


def ionization(temp,density):
    # Stable at both small and large A; large A approaches unity.
    return 2/(1+np.sqrt(1+4*np.exp(np.clip(-log_balance(temp,density),-700,700))))


def half_temperature(density):
    low,high = 100.,1e6
    for _ in range(100):
        mid=(low+high)/2
        if log_balance(mid,density)<np.log(.5): low=mid
        else: high=mid
    temp=(low+high)/2
    C=2/density*(2*np.pi*ME*KB/H**2)**1.5
    b=CHI/KB
    exact=float((2*b/3)/sp.LambertW((2*b/3)*(2*C)**(2/3)))
    np.testing.assert_allclose(temp,exact,rtol=2e-14)
    np.testing.assert_allclose(ionization(temp,density),.5,rtol=2e-14)
    return temp


rows=[]
for exponent in (6,12,18,24,26):
    temp=half_temperature(10.**exponent)
    rows.append(dict(exponent=exponent,T=temp,kT=temp/KELVIN_PER_EV,
                     log=CHI/(KB*temp)))
Path("build").mkdir(exist_ok=True)
Path("build/thermal-ionization.json").write_text(json.dumps(dict(
    constants=dict(h=H,m_e=ME,k_B=KB,e=EV,chi_eV=13.6),
    kelvin_per_eV=KELVIN_PER_EV,chi_kelvin=CHI/KB,rows=rows),indent=2))


def test_composition_conservation_and_balance():
    """Reconstruct the primitive reaction ratio, independently of the quadratic."""
    for density in (1e6,1e18,1e26):
        for factor in (.8,1.,1.2):
            temp=factor*half_temperature(density)
            fraction=ionization(temp,density)
            nuclei=density
            ni_value=ne_value=fraction*nuclei
            nn_value=(1-fraction)*nuclei
            np.testing.assert_allclose(ni_value+nn_value,nuclei,rtol=2e-15)
            lam=wavelength(temp)
            # Equal heavy-particle wavelengths cancel; a chosen reference
            # heavy wavelength still tests all three add/remove factors.
            heavy=lam/np.sqrt(1836)
            reaction=(nn_value*heavy**3)*(1/(ni_value*heavy**3))*(2/(ne_value*lam**3))*np.exp(-CHI/(KB*temp))
            np.testing.assert_allclose(reaction,1,rtol=1e-9)
    np.testing.assert_allclose(float(solution.subs(A,1)),(np.sqrt(5)-1)/2)


def test_temperature_and_density_ordering():
    temperatures=np.geomspace(1000.,30000.,100)
    assert np.all(np.diff(ionization(temperatures,1e18))>0)
    assert ionization(8000.,1e12)>ionization(8000.,1e18)>ionization(8000.,1e24)


def temperature_axis(ax):
    sec=ax.secondary_xaxis("top",functions=(lambda z:z*KELVIN_PER_EV,
                                            lambda z:z/KELVIN_PER_EV))
    sec.set_xlabel(r"$T$ [K]")


def plot_saha_fraction():
    energy=np.logspace(-1.2,4.3,1000)
    fig,ax=figure(slide_width(8),2.65)
    for exp,color,ls in [(6,BLUE,"-"),(12,ORANGE,"--"),(18,GRAY,"-."),(24,"#17202a",":")]:
        ax.plot(energy,ionization(energy*KELVIN_PER_EV,10.**exp),color=color,ls=ls,
                label=rf"$n=10^{{{exp}}}$ m$^{{-3}}$")
        ax.plot(half_temperature(10.**exp)/KELVIN_PER_EV,.5,"o",color=color,ms=4)
    label_levels=(1.08,1.21,1.08,1.21,1.08)
    for j,(name,(_,temperature)) in enumerate(EXAMPLE_PLASMAS.items()):
        ax.axvline(temperature,color="0.8",ls=":",lw=.7,zorder=0)
        ax.text(temperature,label_levels[j],name,ha="center",va="bottom",fontsize=7.5)
    ax.set(xscale="log",xlim=(energy[0],energy[-1]),ylim=(0,1.38),
           xlabel=r"$k_B T$ [eV]",ylabel=r"$x=n_i/(n_i+n_n)$ [1]")
    ax.set_yticks([0,.5,1]);ax.legend(loc="lower right")
    temperature_axis(ax);save(fig,"saha_fraction")


def saha_fraction_deck():
    """Return four ionization curves on the deck's 0.1--10 eV interval."""
    energy=np.geomspace(.1,10.,500)
    densities=(1e6,1e12,1e18,1e24)
    curves={density:ionization(energy*KELVIN_PER_EV,density)
            for density in densities}
    half={density:half_temperature(density)/KELVIN_PER_EV
          for density in densities}
    return dict(energy_eV=energy,densities_m3=densities,
                curves=curves,half_energy_eV=half)


def plot_saha_fraction_deck():
    data=saha_fraction_deck()
    fig,ax=figure(slide_width(8),2.65)
    styles=[(BLUE,"-"),(ORANGE,"--"),(GRAY,"-."),("#17202a",":")]
    for density,(color,ls) in zip(data["densities_m3"],styles):
        exponent=int(np.log10(density))
        ax.plot(data["energy_eV"],data["curves"][density],color=color,ls=ls,
                label=rf"$n=10^{{{exponent}}}$ m$^{{-3}}$")
        ax.plot(data["half_energy_eV"][density],.5,"o",color=color,ms=4)
    ax.set(xscale="log",xlim=(.1,10),ylim=(0,1.08),
           xlabel=r"$k_B T$ [eV]",ylabel=r"$x=n_i/(n_i+n_n)$ [1]")
    ax.set_yticks([0,.5,1]);ax.legend(loc="lower right",fontsize=8)
    temperature_axis(ax);save(fig,"saha_fraction_deck")


def plot_slot_standing_wave():
    """Draw a normalized standing mode between walls in a one-dimensional box slice."""
    from matplotlib.patches import Rectangle

    length=4.0
    x=np.linspace(0,length,700)
    wave=np.sin(4*np.pi*x/length)
    fig,ax=figure(slide_width(6),2.2)
    ax.add_patch(Rectangle((0,-1.08),length,2.16,fill=False,
                           edgecolor=GRAY,linewidth=1.2))
    ax.plot(x,.78*wave,color=BLUE,lw=2)
    ax.text(.12,.88,r"$\psi/\psi_0$ [1]",ha="left",va="center",fontsize=9)
    ax.annotate("",xy=(2.5,1.32),xytext=(.5,1.32),
                arrowprops=dict(arrowstyle="<->",color=ORANGE,lw=1.3))
    ax.text(1.5,1.39,r"$\lambda_s=h/p_s$ [m]",ha="center",va="bottom",
            color=ORANGE,fontsize=9)
    ax.annotate("",xy=(length,-1.37),xytext=(0,-1.37),
                arrowprops=dict(arrowstyle="<->",color=GRAY,lw=1.1))
    ax.text(length/2,-1.49,r"$L$ [m]",ha="center",va="top",color=GRAY)
    ax.text(0,-1.14,"wall",ha="left",va="top",fontsize=8,color=GRAY)
    ax.text(length,-1.14,"wall",ha="right",va="top",fontsize=8,color=GRAY)
    ax.set(xlim=(-.15,length+.15),ylim=(-1.72,1.72))
    ax.axis("off")
    save(fig,"slot_standing_wave")


def plot_slot_momentum_cutoff():
    """Compare a sharp cutoff with the per-state Maxwellian momentum weight."""
    p_over_pth=np.linspace(0,2.5,501)
    fig,ax=figure(slide_width(6),2.35)
    ax.step(p_over_pth,(p_over_pth<=1).astype(float),where="post",
            color=BLUE,ls="--",zorder=3)
    ax.plot(p_over_pth,np.exp(-p_over_pth**2),color=ORANGE,zorder=2)
    ax.axvline(1,color=GRAY,ls=":",lw=1)
    ax.text(1.04,1.08,r"$p_{\mathrm{th},s}$",color=GRAY,ha="left",va="bottom")
    ax.text(.08,.83,"equal below",color=BLUE,fontsize=8,ha="left")
    ax.text(1.34,.23,r"$e^{-(p/p_{\mathrm{th},s})^2}$",color=ORANGE,
            fontsize=8,ha="left")
    ax.set(xlim=(0,2.5),ylim=(-.03,1.24),
           xlabel=r"$p/p_{\mathrm{th},s}$ [1]",
           ylabel="weight per momentum state [1]")
    ax.set_yticks([0,.5,1])
    save(fig,"slot_momentum_cutoff")


def plot_saha_factors():
    density=1e18
    energy=np.linspace(.25,1.4,400);temp=energy*KELVIN_PER_EV
    fig,ax=figure(slide_width(8),3.0)
    ax.plot(energy,np.log10(2/density/wavelength(temp)**3),color=BLUE,
            label=r"electron states $\log_{10}[2/(n\lambda_{\mathrm{th},e}^3)]$")
    cost=CHI/(KB*temp)/np.log(10)
    ax.plot(energy,cost,color=ORANGE,ls="--",label=r"energy cost $\chi/(k_B T\ln 10)$")
    ax.plot(energy,cost+np.log10(.5),color=GRAY,ls=":",label=r"half-ionization balance (cost $-\log_{10}2$)")
    half=half_temperature(density)/KELVIN_PER_EV
    ax.axvline(half,color=GRAY,ls="-.",lw=.8)
    ax.set(xlabel=r"$k_B T$ [eV]",ylabel="logarithm of factor [1]",xlim=(.25,1.4),ylim=(3,25))
    ax.legend(loc="upper center",bbox_to_anchor=(.5,-.23),ncol=1,
              fontsize=8,labelspacing=.2)
    temperature_axis(ax);save(fig,"saha_factors")


def test_saha_fraction_deck_window_and_root():
    data=saha_fraction_deck()
    energy=data["energy_eV"]
    assert energy[0] == .1 and energy[-1] == 10.
    assert set(data["densities_m3"]) == {1e6,1e12,1e18,1e24}
    temperature=energy*KELVIN_PER_EV
    for density,fraction in data["curves"].items():
        A=2/(density*wavelength(temperature)**3)*np.exp(-CHI/(KB*temperature))
        expected=np.array([np.clip(max(root.real for root in np.roots([1.,a,-a])),0,1)
                           for a in A])
        np.testing.assert_allclose(fraction,expected,rtol=2e-13,atol=2e-15)
        np.testing.assert_allclose(
            data["half_energy_eV"][density],half_temperature(density)/KELVIN_PER_EV)


if __name__ == "__main__":
    plot_saha_fraction();plot_saha_fraction_deck();plot_saha_factors()
    plot_slot_standing_wave();plot_slot_momentum_cutoff()
    report(__file__,"Chapter 2 · Temperature, entropy, and thermal ionization")
