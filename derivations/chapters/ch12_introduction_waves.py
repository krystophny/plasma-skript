# Chapter 12 · Introduction to waves (src/chapters/12-introduction-waves.typ)
#
# Plane-wave linearization, the Langmuir and electromagnetic branches of a cold
# plasma, warm-fluid and kinetic corrections. `python ch12_introduction_waves.py`
# prints every step; `# %%` cells run one by one in VS Code, PyCharm or Spyder.

# %% Setup
import numpy as np
import sympy as sp
from sympy.physics import units as u

import si
from notebook import PROTON_MASS, agrees, close_to, evaluate, note, report, section, show
from si import BLUE, GRAY, ORANGE, figure, label, save
from waves import matmul, number, plane_wave_matrix, rounded

e, m_e, m_i, eps0, mu0, k_B, c = sp.symbols("e m_e m_i epsilon_0 mu_0 k_B c", positive=True)
omega, k, n0, T_e, T_i = sp.symbols("omega k n_0 T_e T_i", positive=True)
x, t, gamma_e, gamma_i = sp.symbols("x t gamma_e gamma_i", positive=True)
w_pe = sp.Symbol("omega_pe", positive=True)
lambda_D = sp.Symbol("lambda_D", positive=True)
n1, u1, E1 = sp.symbols("n_1 u_1 E_1")
I = sp.I
M_sym = sp.MatrixSymbol("M", 3, 3)  # name of the displayed wave matrix

# SI units of the local symbols, for si.check(..., unit=...).
UNITS = {omega: 1 / u.second, k: 1 / u.meter, n0: u.meter**-3, T_e: u.kelvin,
         T_i: u.kelvin, gamma_e: 1, gamma_i: 1, w_pe: 1 / u.second}
plane_wave = sp.exp(I * (k * x - omega * t))
omega_pe_sq = n0 * e**2 / (eps0 * m_e)
lambda_D_sq = eps0 * k_B * T_e / (n0 * e**2)
# Example plasma of the chapter: n0 = 1e16 m^-3.
LAB = {n0: 1e16 / u.meter**3}

# %% Plane-wave replacement
section("Plane-wave replacement", script="wave-linearization")
show(sp.Eq(sp.Symbol("f"), plane_wave))
note("Acting on the plane wave, each derivative becomes a factor")
d_dt = sp.simplify(sp.diff(plane_wave, t) / plane_wave)
d_dx = sp.simplify(sp.diff(plane_wave, x) / plane_wave)
agrees(d_dt * plane_wave, -I * omega * plane_wave, lhs=sp.Derivative(plane_wave, t))
agrees(d_dx * plane_wave, I * k * plane_wave, lhs=sp.Derivative(plane_wave, x))
assert d_dt == -I * omega and d_dx == I * k

# %% Linearized continuity
section("Linearized continuity", script="wave-linearization")
eps = sp.Symbol("epsilon")
n, v = sp.Function("n")(x, t), sp.Function("u")(x, t)
continuity = show(sp.Eq(sp.Derivative(n, t) + sp.Derivative(n * v, x), 0))
note("Small perturbation of a uniform plasma at rest,", sp.Lt(eps, 1))
ansatz = {n: n0 + eps * n1 * plane_wave, v: eps * u1 * plane_wave}
show(sp.Eq(n, ansatz[n]))
show(sp.Eq(v, ansatz[v]))
expanded = continuity.lhs.subs(ansatz).doit()
note("Keep the first order in", eps, "; the second order is the dropped nonlinear flux")
assert sp.diff(expanded, eps, 2).subs(eps, 0) != 0
first_order = sp.expand(sp.diff(expanded, eps).subs(eps, 0) / plane_wave)
agrees(first_order, -I * omega * n1 + I * n0 * k * u1, lhs=sp.S.Zero)

# %% Electron plasma frequency
section("Electron plasma frequency", script="plasma-oscillations")
note("Cold electrons, immobile ions; plane-wave momentum, continuity, Poisson")
momentum = show(sp.Eq(-I * omega * m_e * u1, -e * E1))
continuity = show(sp.Eq(first_order, 0))
poisson = show(sp.Eq(I * k * E1, -e * n1 / eps0))
u1_sol = sp.solve(momentum, u1)[0]
agrees(u1_sol, -I * e * E1 / (m_e * omega), lhs=u1)
fields = [n1, u1, E1]
M = plane_wave_matrix([momentum, continuity, poisson], fields)
note("Wave matrix", M_sym)
show(sp.Eq(matmul(M, fields), sp.ImmutableMatrix(sp.zeros(3, 1)), evaluate=False))
note("A nonzero solution needs", sp.Eq(sp.Determinant(M_sym), 0))
det = show(sp.Eq(sp.factor(M.det()), 0))
omega_sq = sp.solve(det, omega)[0] ** 2
agrees(omega_sq, n0 * e**2 / (eps0 * m_e), lhs=w_pe**2)
si.check(omega_sq, omega_pe_sq, unit=u.second**-2, units=UNITS)

# %% Multi-species plasma frequency
section("Multi-species plasma frequency", script="plasma-oscillations")
q1, q2, n_1, n_2, m1, m2 = sp.symbols("q_1 q_2 n_1 n_2 m_1 m_2", positive=True)
rho1 = sp.Symbol("rho_1")
note("Each cold species responds like the electrons:",
     sp.Eq(sp.Symbol("u_s1"), I * sp.Symbol("q_s") * E1 / (sp.Symbol("m_s") * omega)))
charge = show(sp.Eq(rho1, sum(q * (n_s * k / omega) * (I * q * E1 / (m * omega))
                              for q, n_s, m in [(q1, n_1, m1), (q2, n_2, m2)])))
show(sp.Eq(I * k * E1, rho1 / eps0))
omega_sq = sp.solve(sp.Eq(I * k * E1, charge.rhs / eps0), omega)[0] ** 2
agrees(omega_sq, n_1 * q1**2 / (eps0 * m1) + n_2 * q2**2 / (eps0 * m2),
       lhs=omega**2)
note("Hydrogen: the ion term is smaller by the mass ratio")
ratio = sp.simplify((n0 * e**2 / (eps0 * m_i)) / omega_pe_sq)
agrees(ratio, m_e / m_i, lhs=sp.Symbol("omega_pi") ** 2 / w_pe**2)

# %% Worked example: linearization scales
section("Worked example: linearization scales", script="wave-linearization")
example = {**LAB, T_e: 1 * u.electronvolt / u.boltzmann_constant}
note("Input", sp.Eq(n0, example[n0], evaluate=False), "and",
     sp.Eq(k_B * T_e, 1 * u.electronvolt, evaluate=False), "; wavelength 10 cm")
lam = evaluate(lambda_D, sp.sqrt(lambda_D_sq), example, u.meter)
close_to(lam, 7.43e-5)
k_lam = number(k * sp.sqrt(lambda_D_sq), {**example, k: 2 * sp.pi / (0.10 * u.meter)})
show(sp.Eq(k * lambda_D, sp.Float(k_lam, 3)))
close_to(k_lam, 4.67e-3)
wpe = evaluate(w_pe, sp.sqrt(omega_pe_sq), example, 1 / u.second)
close_to(wpe, 5.64e9)
drive = number(omega / w_pe, {omega: 1e10 / u.second, w_pe: wpe / u.second})
show(sp.Eq(omega / w_pe, sp.Float(drive, 3)))
close_to(drive, 1.77)

# %% Worked example: plasma frequency
section("Worked example: plasma frequency", script="plasma-oscillations")
wpe = evaluate(w_pe, sp.sqrt(omega_pe_sq), LAB, 1 / u.second)
close_to(wpe, 5.64e9)
f_p = evaluate(sp.Symbol("f_p"), sp.sqrt(omega_pe_sq) / (2 * sp.pi), LAB, u.hertz)
close_to(f_p, 8.98e8)

# %% Cold electromagnetic branch
section("Cold electromagnetic branch", script="wave-dispersion")
E = sp.Matrix(sp.symbols("E_x E_y E_z"))
k_vec = sp.Matrix([0, 0, k])
note("Cold electron velocity and current, with", sp.Eq(sp.Symbol("u"), -I * e * sp.Symbol("E") / (m_e * omega)))
current = -e * n0 * (-I * e * E / (m_e * omega))
agrees(current[0], I * n0 * e**2 * E[0] / (m_e * omega), lhs=sp.Symbol("j_x"))
wave = k_vec.cross(k_vec.cross(E)) + omega**2 / c**2 * E + I * omega * mu0 * current
note("Faraday and Ampère give the wave matrix", M_sym, "with", sp.Eq(mu0, 1 / (eps0 * c**2)), "and", sp.Eq(w_pe**2, omega_pe_sq))
to_wpe = {mu0: 1 / (eps0 * c**2), n0: w_pe**2 * eps0 * m_e / e**2}
M = sp.ImmutableMatrix(wave.jacobian(E).subs(to_wpe).applyfunc(sp.expand))
show(sp.Eq(matmul(M, E), sp.ImmutableMatrix(sp.zeros(3, 1)), evaluate=False))
note("A nonzero field needs", sp.Eq(sp.Determinant(M_sym), 0))
det = show(sp.Eq(sp.factor(M.det()), 0))
branches = {sp.simplify(r**2) for r in sp.solve(det.lhs, omega)}
assert any(sp.simplify(b - w_pe**2) == 0 for b in branches)  # longitudinal
transverse = (w_pe**2 + c**2 * k**2).subs(w_pe**2, omega_pe_sq)
assert any(sp.simplify(b.subs(w_pe**2, omega_pe_sq) - transverse) == 0 for b in branches)
note("Longitudinal root", sp.Eq(omega, w_pe), "; transverse root")
agrees(transverse, n0 * e**2 / (eps0 * m_e) + c**2 * k**2, lhs=omega**2)
k_sq = sp.solve(sp.Eq(omega**2, transverse), k)[0] ** 2
agrees(sp.expand(c**2 * k_sq / omega**2), 1 - omega_pe_sq / omega**2,
       lhs=c**2 * k**2 / omega**2)

# %% Phase and group velocity
section("Phase and group velocity", script="wave-dispersion")
branch = show(sp.Eq(omega, sp.sqrt(w_pe**2 + c**2 * k**2)))
v_phi, v_g = sp.symbols("v_phi v_g")
phase = branch.rhs / k
group = sp.diff(branch.rhs, k)
show(sp.Eq(v_g, sp.Derivative(branch.rhs, k)))
agrees(phase, c * sp.sqrt(1 + w_pe**2 / (c**2 * k**2)), lhs=v_phi)
agrees(group, c**2 * k / branch.rhs, lhs=v_g)
si.check(phase, c * sp.sqrt(1 + w_pe**2 / (c**2 * k**2)), unit=u.meter / u.second, units=UNITS)
si.check(group, c**2 * k / branch.rhs, unit=u.meter / u.second, units=UNITS)
agrees(sp.simplify(phase * group), c**2, lhs=v_phi * v_g)

# %% Worked example: electromagnetic branch
section("Worked example: electromagnetic branch", script="wave-dispersion")
K, W = sp.symbols('K omega_hat', positive=True)
note("Drive at", sp.Eq(W, 2), "with", rounded(sp.Eq(w_pe, 5.64e9 / u.second)))
K_value = number(sp.sqrt(W**2 - 1), {W: 2})
show(sp.Eq(K, sp.Float(K_value, 4)))
close_to(K_value, 1.732)
phase_ratio = number(W / K, {W: 2, K: K_value})
show(sp.Eq(v_phi / c, sp.Float(phase_ratio, 4)))
close_to(phase_ratio, 1.155)
group_ratio = number(K / W, {W: 2, K: K_value})
show(sp.Eq(v_g / c, sp.Float(group_ratio, 4)))
close_to(group_ratio, 0.866)
drive = {K: K_value, w_pe: 5.64e9 / u.second}
k_value = evaluate(k, K * w_pe / c, drive, 1 / u.meter)
close_to(k_value, 32.6)
close_to(evaluate(sp.Symbol("lambda"), 2 * sp.pi * c / (K * w_pe), drive, u.meter),
         0.193)

# %% Warm-fluid dispersion
section("Warm-fluid dispersion", script="wave-kinetic-limits")
q, n_s, m_s, gamma_s, T_s = sp.symbols("q_s n_s m_s gamma_s T_s", positive=True)
c_s = sp.Symbol("c_s", positive=True)  # c_s^2 = gamma_s k_B T_s / m_s
note("Adiabatic pressure", sp.Eq(sp.Symbol("p_1"), gamma_s * k_B * T_s * n1))
continuity = show(sp.Eq(-I * omega * n1 + I * k * n_s * u1, 0))
momentum = show(sp.Eq(-I * omega * m_s * u1, q * E1 - I * k * gamma_s * k_B * T_s * n1 / n_s))
response = sp.solve([continuity, momentum], [n1, u1], dict=True)[0]
note("Solve with", sp.Eq(c_s**2, gamma_s * k_B * T_s / m_s))
to_cs = {T_s: c_s**2 * m_s / (gamma_s * k_B)}
agrees(sp.factor(response[u1].subs(to_cs)),
       I * q * omega * E1 / (m_s * (omega**2 - k**2 * c_s**2)), lhs=u1)
agrees(sp.factor(response[n1].subs(to_cs)),
       I * n_s * q * k * E1 / (m_s * (omega**2 - k**2 * c_s**2)), lhs=n1)
poisson = show(sp.Eq(I * k * E1, q * n1 / eps0))
susceptibility = sp.simplify(q * response[n1].subs(to_cs) / (eps0 * I * k * E1))
agrees(susceptibility, n_s * q**2 / (eps0 * m_s * (omega**2 - k**2 * c_s**2)),
       lhs=sp.S.One)
note("Electrons only, ions fixed (Bohm-Gross)")
langmuir = sp.Eq(1, susceptibility.subs({q: -e, n_s: n0, m_s: m_e,
                                         c_s: sp.sqrt(gamma_e * k_B * T_e / m_e)}))
show(langmuir)
omega_sq = sp.solve(langmuir, omega)[0] ** 2
agrees(omega_sq, omega_pe_sq + gamma_e * k**2 * k_B * T_e / m_e, lhs=omega**2)
si.check(omega_sq, omega_pe_sq + gamma_e * k**2 * k_B * T_e / m_e, unit=u.second**-2,
         units=UNITS)

# %% Ion-acoustic limit
section("Ion-acoustic limit", script="wave-kinetic-limits")
c_e, c_i, w_pi = sp.symbols("c_e c_i omega_pi", positive=True)
sound_speeds = {c_e: sp.sqrt(gamma_e * k_B * T_e / m_e), c_i: sp.sqrt(gamma_i * k_B * T_i / m_i),
                w_pe: sp.sqrt(omega_pe_sq), w_pi: sp.sqrt(n0 * e**2 / (eps0 * m_i))}
note("Electrons and ions; electron inertia dropped,", sp.Lt(omega, k * c_e))
two_species = show(sp.Eq(1 + w_pe**2 / (k**2 * c_e**2) - w_pi**2 / (omega**2 - k**2 * c_i**2), 0))
note("Long wavelength,", sp.Lt(k * lambda_D, 1), ": the vacuum term 1 is negligible")
reduced = show(sp.Eq(two_species.lhs - 1, 0))
omega_sq = sp.solve(reduced, omega)[0] ** 2
show(sp.Eq(omega**2, omega_sq))
ion_acoustic = k**2 * (gamma_e * k_B * T_e + gamma_i * k_B * T_i) / m_i
agrees(omega_sq.subs(sound_speeds), ion_acoustic, lhs=omega**2)
si.check(omega_sq.subs(sound_speeds), ion_acoustic, unit=u.second**-2, units=UNITS)

# %% Kinetic susceptibility limits
section("Kinetic susceptibility limits", script="wave-kinetic-limits")
zeta, s = sp.symbols("zeta s", positive=True)
Z = sp.Function("Z")(zeta)
show(sp.Eq(Z, sp.Integral(sp.exp(-s**2) / (s - zeta), (s, -sp.oo, sp.oo)) / sp.sqrt(sp.pi)))
note("For", sp.Gt(zeta, 1), "expand the denominator")
show(sp.Eq(1 / (s - zeta), -sum(s**j / zeta**(j + 1) for j in range(5))))
note("Odd powers vanish against the Gaussian; the even moments are")
moments = [sp.integrate(s**(2 * j) * sp.exp(-s**2), (s, -sp.oo, sp.oo)) / sp.sqrt(sp.pi)
           for j in range(3)]
for j in range(3):
    show(sp.Eq(sp.Integral(s**(2 * j) * sp.exp(-s**2), (s, -sp.oo, sp.oo)) / sp.sqrt(sp.pi),
               moments[j]))
Z_series = show(sp.Eq(Z, -sum(moments[j] / zeta**(2 * j + 1) for j in range(3)))).rhs
chi_e = sp.Symbol("chi_e")
v_th2 = 2 * k_B * T_e / m_e
chi_def = show(sp.Eq(chi_e, 2 * w_pe**2 / (k**2 * sp.Symbol("v_th") ** 2) * (1 + zeta * Z)))
chi = sp.expand((2 * omega_pe_sq / (k**2 * v_th2) * (1 + zeta * Z_series))
                .subs(zeta, omega / (k * sp.sqrt(v_th2))))
note("Insert", sp.Eq(zeta, omega / (k * sp.Symbol("v_th"))), "with",
     sp.Eq(sp.Symbol("v_th") ** 2, v_th2))
show(sp.Eq(chi_e, chi))
cold = sp.limit(chi * omega**2, omega, sp.oo)
agrees(cold, -omega_pe_sq, lhs=sp.Limit(chi_e * omega**2, omega, sp.oo))
next_order = sp.limit((chi * omega**2 + omega_pe_sq) * omega**2, omega, sp.oo)
note("Next order: Bohm-Gross with", sp.Eq(gamma_e, 3))
agrees(sp.simplify(-next_order / omega_pe_sq), 3 * k**2 * k_B * T_e / m_e, lhs=k**2 * sp.Symbol("c_e") ** 2)
note("Static limit", sp.Eq(zeta * Z, 0), ": Debye screening")
agrees(sp.simplify(2 * omega_pe_sq / (k**2 * v_th2)), 1 / (k**2 * lambda_D_sq), lhs=chi_e)

# %% Worked example: ion-acoustic wave
section("Worked example: ion-acoustic wave", script="wave-kinetic-limits")
example = {**LAB, T_e: 10 * u.electronvolt / u.boltzmann_constant, m_i: PROTON_MASS}
note("Hydrogen,", sp.Eq(k_B * T_e, 10 * u.electronvolt, evaluate=False), ", cold ions,",
     sp.Eq(k, 1 / u.meter, evaluate=False))
sound = evaluate(sp.Symbol("c_s"), sp.sqrt(k_B * T_e / m_i), example, u.meter / u.second)
close_to(sound, 3.09e4)
close_to(evaluate(omega, k * sp.sqrt(k_B * T_e / m_i), {**example, k: 1 / u.meter},
                  1 / u.second), 3.09e4)
lam = evaluate(lambda_D, sp.sqrt(lambda_D_sq), example, u.meter)
close_to(lam, 2.35e-4)
k_lam = number(k * sp.sqrt(lambda_D_sq), {**example, k: 1 / u.meter})
show(sp.Eq(k * lambda_D, sp.Float(k_lam, 3)))
close_to(k_lam, 2.35e-4)

# %% Normalized branch and limits
section("Normalized branch and limits", script="dispersion-limits")
note("Normalize", sp.Eq(W, omega / w_pe), "and", sp.Eq(K, k * c / w_pe))
W_sq = sp.expand(((w_pe**2 + c**2 * k**2) / w_pe**2).subs(k, K * w_pe / c))
agrees(W_sq, 1 + K**2, lhs=W**2)
W_K = sp.sqrt(W_sq)
group = sp.diff(W_K, K)
agrees(group, K / W_K, lhs=v_g / c)
assert sp.limit(W_K, K, 0) == 1 and sp.limit(group, K, 0) == 0
show(sp.Eq(sp.Limit(v_g / c, K, 0), sp.limit(group, K, 0)))
large_K = sp.limit(W_K / K, K, sp.oo)
assert large_K == 1 and sp.limit(K / W_K, K, sp.oo) == 1
show(sp.Eq(sp.Limit(v_phi / c, K, sp.oo), large_K))

# %% Evanescent branch
section("Evanescent branch", script="dispersion-limits")
below = show(sp.Eq(k**2, (omega**2 - w_pe**2) / c**2))
alpha = sp.Symbol("alpha", positive=True)
note("Below cutoff,", sp.Lt(omega, w_pe), ": write", sp.Eq(k, I * alpha, evaluate=False))
alpha_value = sp.sqrt(sp.factor(-below.rhs))
si.check((I * alpha_value) ** 2, below.rhs)
agrees(alpha_value**2, (sp.sqrt(w_pe**2 - omega**2) / c) ** 2, lhs=alpha**2)

# %% Worked example: drive classification
section("Worked example: drive classification", script="dispersion-limits")
wpe = evaluate(w_pe, sp.sqrt(omega_pe_sq), LAB, 1 / u.second)
close_to(wpe, 5.64e9)
plasma = {w_pe: wpe / u.second}
note("Lower drive", rounded(sp.Eq(omega, 4.0e9 / u.second)), ": evanescent")
close_to(evaluate(alpha, sp.sqrt(w_pe**2 - omega**2) / c,
                  {**plasma, omega: 4.0e9 / u.second}, 1 / u.meter), 13.3)
upper = {**plasma, omega: 1.13e10 / u.second}
note("Upper drive", rounded(sp.Eq(omega, upper[omega])), ": propagating")
k_value = evaluate(k, sp.sqrt(omega**2 - w_pe**2) / c, upper, 1 / u.meter)
close_to(k_value, 32.7)
upper[k] = k_value / u.meter
phase_ratio = number(omega / (k * c), upper)
show(sp.Eq(v_phi / c, sp.Float(phase_ratio, 3)))
close_to(phase_ratio, 1.15)
group_ratio = number(k * c / omega, upper)
show(sp.Eq(v_g / c, sp.Float(group_ratio, 3)))
close_to(group_ratio, 0.866)

# %% Plot: cold unmagnetized branches W(K)
transverse_W = sp.lambdify(K, sp.sqrt(W_sq), "numpy")
K_grid = np.linspace(0, 3, 200)
fig, ax = figure(4.2, 2.8)
ax.plot(K_grid, K_grid, color=GRAY, ls=":", lw=1.2)
ax.plot(K_grid, transverse_W(K_grid), color=BLUE)
ax.plot(K_grid, np.ones_like(K_grid), color=ORANGE, ls="--")
ax.plot([0], [1], "o", color=BLUE, ms=4, clip_on=False, zorder=3)
label(ax, 0.08, 1.04, "cutoff", BLUE, va="bottom")
label(ax, 1.55, 2.05, 'electromagnetic\n$\\hat{\\omega}^2=1+K^2$', BLUE, ha="right")
label(ax, 2.95, 1.05, 'electrostatic $\\hat{\\omega}=1$', ORANGE, ha="right")
label(ax, 2.6, 2.4, 'vacuum $\\hat{\\omega}=K$', GRAY, ha="left", va="top")
ax.set(xlim=(0, 3), ylim=(0, 3.2), xticks=[0, 1, 2, 3], yticks=[0, 1, 2, 3],
       xlabel=r"$K=kc/\omega_{pe}$ [1]", ylabel='$\\hat{\\omega}=\\omega/\\omega_{pe}$ [1]')
save(fig, "wave-dispersion")

# %%
if __name__ == "__main__":
    report(__file__, "Chapter 12 · Introduction to waves")
