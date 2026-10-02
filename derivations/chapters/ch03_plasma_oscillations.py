"""Chapter 3, Plasma oscillations: src/chapters/03-plasma-oscillations.typ.

Coverage (Typst label or line -> test):
  <plasma-oscillation-field>      l.47, 117  -> test_sheet_field
  <plasma-oscillation-force>      l.58, 122  -> test_oscillator
  <plasma-oscillation-frequency>  l.67, 127  -> test_oscillator
  <intro-plasma-frequency>        l.79       -> test_species_plasma_frequency
  f_p = omega_p/(2 pi)            l.83       -> test_species_plasma_frequency
  <intro-plasma-frequency-debye-relation> l.90-91 -> test_debye_relation
  d_s = c/omega_p,s               l.99       -> test_inertial_length_unit

Run `python derivations/ch03_plasma_oscillations.py` or `pytest derivations`.
"""

import sympy as sp
from sympy.physics import units as u

from si import Derivation, c, check, e, eps0, k_B, m_e

n0, xi, x, t, T_e = sp.symbols("n_0 xi x t T_e", positive=True)
n_s, q_s, m_s = sp.symbols("n_s q_s m_s", positive=True)
LOCAL = {n0: u.meter**-3, xi: u.meter, x: u.meter, t: u.second, T_e: u.kelvin,
         n_s: u.meter**-3, q_s: u.coulomb, m_s: u.kilogram}
w_pe, lam_D, v_th = sp.symbols("omega_pe lambda_D v_th", positive=True)


def test_sheet_field():
    d = Derivation("Charge-separation field", "src/chapters/03-plasma-oscillations.typ:47")
    # Shifting the electrons by +xi leaves an ion sheet (+e n0 xi) at x = 0 and
    # an electron sheet (-e n0 xi) at x = L. An infinite sheet of surface
    # charge sigma at x0 has field sigma/(2 eps0) * sign(x - x0).
    L = sp.symbols("L", positive=True)
    sigma = d.eq("sheet charge", sp.Symbol("sigma"), e * n0 * xi)
    E = lambda x0, s: s / (2 * eps0) * sp.sign(x - x0)
    E_tot = d.eq("two sheets", sp.Symbol("E"), E(0, sigma) + E(L, -sigma))
    E_between = d.eq("between sheets", sp.Symbol("E"), E_tot.subs(x, L / 2))
    stated = e * n0 * xi / eps0  # :47, :117
    check(E_between, stated, unit=u.volt / u.meter, units=LOCAL)
    # Outside the slab the two sheet fields cancel.
    check(d.eq("outside", sp.Symbol("E"), E_tot.subs(x, 2 * L)), 0)


def test_oscillator():
    d = Derivation("Electron plasma oscillation", "src/chapters/03-plasma-oscillations.typ:67")
    X = sp.Function("xi")
    E = e * n0 * X(t) / eps0
    # Newton for an electron: m_e xi'' = -e E.
    newton = d.step("Newton", sp.Eq(m_e * X(t).diff(t, 2), -e * E))
    check(newton.rhs, -(n0 * e**2) / eps0 * X(t))  # :58
    # Dividing by m_e: xi'' + omega^2 xi = 0 identifies omega_pe.
    omega_sq = d.eq("divide by mass", w_pe**2, sp.simplify(-newton.rhs / X(t) / m_e))
    stated = sp.sqrt(n0 * e**2 / (eps0 * m_e))  # :67
    check(sp.sqrt(omega_sq), stated, unit=1 / u.second, units=LOCAL)
    # dsolve gives harmonic motion at omega_pe, consistent with :127.
    sol = d.eq("dsolve", X(t), sp.dsolve(newton, X(t)).rhs)
    xi0, delta = sp.symbols("xi_0 delta")
    trial = xi0 * sp.cos(stated * t + delta)
    assert sp.simplify(m_e * trial.diff(t, 2) + e**2 * n0 / eps0 * trial) == 0
    assert sol.has(sp.sin(stated * t)) or sol.has(sp.exp(sp.I * stated * t))


def test_species_plasma_frequency():
    d = Derivation("Species plasma frequency", "src/chapters/03-plasma-oscillations.typ:79")
    # Same oscillator for species s: m_s xi'' = -(n_s q_s^2/eps0) xi.
    w = d.eq("species oscillator", sp.Symbol("omega_ps"), sp.sqrt(n_s * q_s**2 / (eps0 * m_s)))  # :79
    check(w.subs({n_s: n0, q_s: e, m_s: m_e}), sp.sqrt(n0 * e**2 / (eps0 * m_e)),
          unit=1 / u.second, units=LOCAL)
    f = d.eq("ordinary frequency", sp.Symbol("f_ps"), w / (2 * sp.pi))
    check(f, f, unit=u.hertz, units=LOCAL)  # :83


def test_debye_relation():
    d = Derivation("Plasma frequency and Debye length", "src/chapters/03-plasma-oscillations.typ:90")
    lam = d.eq("Debye length", lam_D, sp.sqrt(eps0 * k_B * T_e / (n0 * e**2)))
    wpe = d.eq("plasma frequency", w_pe, sp.sqrt(n0 * e**2 / (eps0 * m_e)))
    vth = d.eq("thermal speed", v_th, sp.sqrt(2 * k_B * T_e / m_e))
    ratio = d.eq("ratio", v_th / (w_pe * lam_D), sp.simplify(vth / (wpe * lam)))
    check(ratio, sp.sqrt(2))
    # src/chapters/03-plasma-oscillations.typ:90-91
    check(lam, vth / (sp.sqrt(2) * wpe), unit=u.meter, units=LOCAL)
    check(wpe, vth / (sp.sqrt(2) * lam), unit=1 / u.second, units=LOCAL)
    # With v_th = sqrt(k_B T/m) the factor sqrt(2) disappears (:96).
    check(lam, sp.sqrt(k_B * T_e / m_e) / wpe)


def test_inertial_length_unit():
    d = Derivation("Inertial length", "src/chapters/03-plasma-oscillations.typ:99")
    ds = d.eq("definition", sp.Symbol("d_s"), c / sp.sqrt(n_s * q_s**2 / (eps0 * m_s)))
    check(ds, ds, unit=u.meter, units=LOCAL)  # :99


if __name__ == "__main__":
    from si import run_as_script

    run_as_script(globals())
