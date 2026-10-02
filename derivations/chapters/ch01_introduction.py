"""Chapter 1, Introduction: src/chapters/01-introduction.typ.

Coverage (Typst label or line -> test):
  <intro-charge-density>        l.71      -> test_charge_density_unit
  <intro-quasineutrality>       l.90-91   -> test_quasineutrality
  <intro-thermal-energy>        l.207     -> test_thermal_energy_units
  <intro-thermal-speed>         l.221     -> test_thermal_speed
  eV <-> K conversion           l.232-235 -> test_ev_to_kelvin
  "4x energy doubles v_th"      l.269     -> test_thermal_speed_scaling

Run `python derivations/ch01_introduction.py` or `pytest derivations`.
"""

import sympy as sp
from sympy.physics import units as u

from si import Derivation, check, e, k_B

m_s, T_s, v, n_e, n_i, Z, q_s, n_s = sp.symbols("m_s T_s v n_e n_i Z q_s n_s", positive=True)
LOCAL = {m_s: u.kilogram, T_s: u.kelvin, v: u.meter / u.second,
         n_e: u.meter**-3, n_i: u.meter**-3, q_s: u.coulomb, n_s: u.meter**-3}


def close(a, b, rtol):
    assert abs(float(a) / float(b) - 1) < rtol, f"{float(a)} vs {float(b)}"


def test_charge_density_unit():
    # Definition rho_q = sum_s q_s n_s: one species term carries C m^-3.
    # src/chapters/01-introduction.typ:71
    d = Derivation("Charge density", "src/chapters/01-introduction.typ:71")
    stated = d.eq("species term", sp.Symbol("rho_q"), q_s * n_s)
    check(stated, stated, unit=u.coulomb / u.meter**3, units=LOCAL)


def test_quasineutrality():
    # Electrons carry -e, an ion of charge state Z carries +Z e.
    d = Derivation("Quasineutrality", "src/chapters/01-introduction.typ:90")
    rho = d.eq("species sum", sp.Symbol("rho_q"), (-e) * n_e + (Z * e) * n_i)
    # src/chapters/01-introduction.typ:90
    stated = e * (Z * n_i - n_e)
    check(rho, stated, unit=u.coulomb / u.meter**3, units={**LOCAL, Z: 1})
    # rho_q = 0 solved for n_e gives n_e = Z n_i (n_e = n_i for hydrogen).
    sol = d.eq("neutral", n_e, sp.solve(sp.Eq(rho, 0), n_e)[0])
    check(sol, Z * n_i)
    check(sol.subs(Z, 1), n_i)


def test_thermal_energy_units():
    d = Derivation("Kinetic and thermal energy", "src/chapters/01-introduction.typ:207")
    d.eq("kinetic", sp.Symbol("epsilon_kin"), m_s * v**2 / 2)
    d.eq("thermal", sp.Symbol("epsilon_th"), k_B * T_s)
    check(m_s * v**2 / 2, m_s * v**2 / 2, unit=u.joule, units=LOCAL)
    check(k_B * T_s, k_B * T_s, unit=u.joule, units=LOCAL)


def test_thermal_speed():
    # Convention: kinetic energy at the thermal speed equals k_B T_s.
    d = Derivation("Thermal speed", "src/chapters/01-introduction.typ:221")
    vth = sp.symbols("v_th", positive=True)
    d.step("convention", sp.Eq(m_s * vth**2 / 2, k_B * T_s))
    derived = d.eq("solve", vth, sp.solve(sp.Eq(m_s * vth**2 / 2, k_B * T_s), vth)[0])
    # src/chapters/01-introduction.typ:221
    stated = sp.sqrt(2 * k_B * T_s / m_s)
    check(derived, stated, unit=u.meter / u.second, units=LOCAL)


def test_ev_to_kelvin():
    # CODATA exact SI values (2019 redefinition).
    e_num = sp.Rational("1.602176634e-19")
    kB_num = sp.Rational("1.380649e-23")
    d = Derivation("Electron-volt in kelvin", "src/chapters/01-introduction.typ:233")
    one_eV_in_K = d.eq("1 eV in K", sp.Symbol("T_1eV"), sp.Float(e_num / kB_num, 8))
    d.eq("10 eV in K", sp.Symbol("T_10eV"), sp.Float(10 * e_num / kB_num, 8))
    # src/chapters/01-introduction.typ:233 ; 1 eV / k_B ~ 1.1605e4 K
    close(one_eV_in_K, 1.1605e4, 1e-4)
    # src/chapters/01-introduction.typ:235 ; k_B T_e = 10 eV -> ~1.16e5 K
    close(10 * one_eV_in_K, 1.16e5, 5e-3)


def test_thermal_speed_scaling():
    # v_th proportional to sqrt(k_B T): quadruple the energy, double the speed.
    d = Derivation("Thermal-speed scaling", "src/chapters/01-introduction.typ:269")
    vth = sp.sqrt(2 * k_B * T_s / m_s)
    ratio = d.eq("T to 4T", sp.Symbol("v_4T") / sp.Symbol("v_T"), sp.simplify(vth.subs(T_s, 4 * T_s) / vth))
    check(ratio, 2)


if __name__ == "__main__":
    from si import run_as_script

    run_as_script(globals())
