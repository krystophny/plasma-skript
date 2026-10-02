# Chapter 1 · Introduction (src/chapters/01-introduction.typ)
#
# Charge density and quasineutrality, thermal speed, and the electron-volt as a
# temperature. `python ch01_introduction.py` prints every step.

# %% Setup
import sympy as sp
from sympy.physics import units as u

from notebook import agrees, close_to, evaluate, note, report, section, show
from si import check, e, k_B

m_s, T_s, v, n_e, n_i, Z, q_s, n_s = sp.symbols("m_s T_s v n_e n_i Z q_s n_s", positive=True)
rho_q, eps_kin, eps_th = sp.symbols("rho_q epsilon_kin epsilon_th")
v_th = sp.Symbol("v_th", positive=True)
SI_UNITS = {m_s: u.kilogram, T_s: u.kelvin, v: u.meter / u.second, n_e: u.meter**-3,
            n_i: u.meter**-3, q_s: u.coulomb, n_s: u.meter**-3, Z: 1}

# %% Charge density and quasineutrality
section("Charge density and quasineutrality", "01-introduction.typ:71")
q_e, q_i = sp.symbols("q_e q_i")
note("Sum of", q_s * n_s, "over electrons and ions")
check(q_s * n_s, q_s * n_s, unit=u.coulomb / u.meter**3, units=SI_UNITS)
species_sum = show(sp.Eq(rho_q, q_e * n_e + q_i * n_i))
note("Electrons carry", sp.Eq(q_e, -e), "and ions of charge state", Z, "carry", sp.Eq(q_i, Z * e))
charge = show(species_sum.subs({q_e: -e, q_i: Z * e}))
agrees(charge.rhs, e * (Z * n_i - n_e), ":90", lhs=rho_q)
check(charge.rhs, e * (Z * n_i - n_e), unit=u.coulomb / u.meter**3, units=SI_UNITS)
note("Quasineutrality", sp.Eq(rho_q, 0), "fixes the electron density")
n_e_neutral = sp.solve(charge.rhs, n_e)[0]
agrees(n_e_neutral, Z * n_i, ":91", lhs=n_e)
note("Hydrogen,", sp.Eq(Z, 1))
agrees(n_e_neutral.subs(Z, 1), n_i, ":91", lhs=n_e)

# %% Thermal energy and thermal speed
section("Thermal speed", "01-introduction.typ:207")
note("Kinetic and thermal energy, both in joule")
kinetic = show(sp.Eq(eps_kin, m_s * v**2 / 2))
thermal = show(sp.Eq(eps_th, k_B * T_s))
check(kinetic.rhs, kinetic.rhs, unit=u.joule, units=SI_UNITS)
check(thermal.rhs, thermal.rhs, unit=u.joule, units=SI_UNITS)
note("Convention: the kinetic energy at the thermal speed equals", thermal.rhs)
convention = show(sp.Eq(kinetic.rhs.subs(v, v_th), thermal.rhs))
v_th_solved = sp.solve(convention, v_th)[0]
agrees(v_th_solved, sp.sqrt(2 * k_B * T_s / m_s), ":221", lhs=v_th)
check(v_th_solved, v_th_solved, unit=u.meter / u.second, units=SI_UNITS)
note("Four times the energy doubles the speed")
agrees(v_th_solved.subs(T_s, 4 * T_s) / v_th_solved, 2, ":269",
       lhs=sp.Function("v_th")(4 * T_s) / sp.Function("v_th")(T_s))

# %% Worked example: electron-volt as a temperature
section("Electron-volt in kelvin", "01-introduction.typ:233")
energy = sp.Symbol("epsilon", positive=True)
note("Temperature with", sp.Eq(k_B * T_s, energy))
kelvin_per_eV = evaluate(T_s, energy / k_B, {energy: 1 * u.electronvolt}, u.kelvin, digits=5)
close_to(kelvin_per_eV, 1.1605e4, rtol=1e-4, source=":233")
kelvin_10eV = evaluate(T_s, energy / k_B, {energy: 10 * u.electronvolt}, u.kelvin)
close_to(kelvin_10eV, 1.16e5, source=":235")

# %%
if __name__ == "__main__":
    report(__file__, "Chapter 1 · Introduction")
