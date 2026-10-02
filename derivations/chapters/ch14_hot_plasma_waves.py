# Chapter 14 · Waves in hot plasmas (src/chapters/14-hot-plasma-waves.typ)
#
# Linear Vlasov response, the Maxwellian dielectric function with Z(zeta),
# Landau damping, transverse kinetic waves, the anisotropy and two-stream
# instabilities, and the gyro-orbit picture of magnetized resonances.

# %% Setup
import mpmath as mp
import numpy as np
import sympy as sp
from sympy.physics import units as u

import si
from notebook import agrees, close_to, evaluate, note, report, section, show
from si import BLUE, GRAY, ORANGE, figure, label, save
from waves import number, rounded

e, m_e, eps0, k_B, c = sp.symbols("e m_e epsilon_0 k_B c", positive=True)
I = sp.I
n0, T_e, k, v, omega, q, m, phi, E1 = sp.symbols("n_0 T_e k v omega q m phi_1 E_1", positive=True)
v_te, lambda_D, w_pe, gamma, v_g = sp.symbols("v_te lambda_D omega_pe gamma v_g", positive=True)
zeta, x, a = sp.symbols("zeta x a", positive=True)  # a = k lambda_D
Z = sp.Symbol("Z")  # value Z(zeta) of the plasma dispersion function
F = sp.Function("F")  # equilibrium marginal F_0(v) along k
f1 = sp.Symbol("f_1")

# SI units of the local symbols (gamma is a damping rate here), for si.check.
UNITS = {n0: u.meter**-3, T_e: u.kelvin, k: u.meter**-1, v: u.meter / u.second,
         omega: u.second**-1, q: u.coulomb, m: u.kilogram, v_te: u.meter / u.second,
         lambda_D: u.meter, w_pe: u.second**-1, gamma: u.second**-1,
         v_g: u.meter / u.second}
LAB = {n0: 1e16 / u.meter**3}  # example plasma of the chapter
omega_pe_sq = n0 * e**2 / (eps0 * m_e)
lambda_D_sq = eps0 * k_B * T_e / (n0 * e**2)
v_te_value = sp.sqrt(2 * k_B * T_e / m_e)


def z_function(zeta_value):
    """Causal plasma dispersion function, Z = i sqrt(pi) w(zeta) (Faddeeva)."""
    z = mp.mpc(zeta_value)
    return 1j * mp.sqrt(mp.pi) * mp.exp(-z**2) * mp.erfc(-1j * z)


# %% Linear Vlasov response
section("Linear Vlasov response", script="hot-isotropic-dispersion")
z, t = sp.symbols("z t", real=True)
f1_zt = sp.Function("f_1")(z, t)
note("Linearize about", F(v), "with", sp.Eq(sp.Symbol("k"), k * sp.Symbol("e_z")), ":")
show(sp.Eq(sp.Derivative(f1_zt, t) + v * sp.Derivative(f1_zt, z) + q / m * E1 * sp.Derivative(F(v), v), 0))
note("Plane wave:", sp.Eq(sp.Derivative(f1_zt, t), -I * omega * f1_zt), ",",
     sp.Eq(sp.Derivative(f1_zt, z), I * k * f1_zt))
vlasov = -I * omega * f1 + I * k * v * f1 + q / m * E1 * sp.diff(F(v), v)
show(sp.Eq(vlasov, 0))
assert sp.simplify(vlasov - (I * (k * v - omega) * f1 + q / m * E1 * sp.diff(F(v), v))) == 0
f1_response = sp.solve(vlasov, f1)[0]
agrees(f1_response, -I * q / m * E1 * sp.diff(F(v), v) / (omega - k * v), lhs=f1)

# %% Electrostatic dielectric function
section("Electrostatic dielectric function", script="hot-isotropic-dispersion")
note("Potential", sp.Eq(E1, -I * k * phi, evaluate=False))
f1_phi = f1_response.subs(E1, -I * k * phi)
agrees(q * f1_phi, -(q**2 * phi) / m * (k * sp.diff(F(v), v)) / (omega - k * v),
       lhs=sp.Derivative(sp.Symbol("rho_1"), v))
I_k = sp.Symbol("I_k")
show(sp.Eq(I_k, sp.Integral(k * sp.diff(F(v), v) / (omega - k * v), (v, -sp.oo, sp.oo))))
rho1 = -(q**2 * phi) / m * I_k
eps_L = sp.Symbol("epsilon_L")
note("Poisson", sp.Eq(k**2 * phi, sp.Symbol("rho_1") / eps0), "divided by", k**2 * phi,
     "; normal modes have", sp.Eq(eps_L, 0))
agrees(sp.expand(sp.simplify((k**2 * phi - rho1 / eps0) / (k**2 * phi))),
       1 + q**2 / (eps0 * m * k**2) * I_k, lhs=eps_L)

# %% Maxwellian dielectric and Z
section("Maxwellian dielectric and Z", script="hot-isotropic-dispersion")
vx, vy, vz = sp.symbols("v_x v_y v_z", real=True)
maxwellian = n0 / (sp.pi**sp.Rational(3, 2) * v_te**3) * sp.exp(-(vx**2 + vy**2 + vz**2) / v_te**2)
show(sp.Eq(sp.Symbol("f_0"), maxwellian))
marginal = sp.integrate(maxwellian, (vx, -sp.oo, sp.oo), (vy, -sp.oo, sp.oo))
agrees(marginal, n0 / (sp.sqrt(sp.pi) * v_te) * sp.exp(-vz**2 / v_te**2), lhs=F(vz))
assert sp.simplify(sp.integrate(marginal, (vz, -sp.oo, sp.oo)) - n0) == 0
note("Substitute", sp.Eq(vz, v_te * x), ",", sp.Eq(omega, k * v_te * zeta), "; partial fractions")
integrand = (k * sp.diff(marginal, vz) / (omega - k * vz)).subs(
    {vz: v_te * x, omega: k * v_te * zeta}) * v_te
parts = sp.apart(sp.simplify(integrand * sp.exp(x**2)), x)
show(sp.Eq(I_k, sp.Integral(parts * sp.exp(-x**2), (x, -sp.oo, sp.oo))))
note("The pole term defines")
show(sp.Eq(sp.Function("Z")(zeta), sp.Integral(sp.exp(-x**2) / (x - zeta), (x, -sp.oo, sp.oo))
           / sp.sqrt(sp.pi)))
regular = sum(term for term in sp.Add.make_args(parts) if not term.has(1 / (x - zeta)))
pole = sp.simplify((parts - regular) * (x - zeta))
integral = sp.integrate(regular * sp.exp(-x**2), (x, -sp.oo, sp.oo)) + pole * sp.sqrt(sp.pi) * Z
show(sp.Eq(I_k, sp.factor(integral)))
note("Electrons", sp.Eq(q, -e, evaluate=False), ",", sp.Eq(v_te**2, v_te_value**2))
eps_maxwell = (1 + e**2 / (eps0 * m_e * k**2) * integral).subs(v_te, v_te_value)
agrees(eps_maxwell, 1 + (1 + zeta * Z) / (k**2 * lambda_D_sq), lhs=eps_L)
EPS_L_MAXWELL = 1 + (1 + zeta * Z) / a**2  # with a = k lambda_D
si.check((1 + (1 + zeta * Z) / (k**2 * lambda_D_sq)).subs(k, a / sp.sqrt(lambda_D_sq)), EPS_L_MAXWELL)
show(sp.Eq(eps_L, EPS_L_MAXWELL))
si.check(sp.sqrt(lambda_D_sq), sp.sqrt(eps0 * k_B * T_e / (n0 * e**2)), unit=u.meter, units=UNITS)

# %% Cold limit
section("Cold limit", script="hot-isotropic-dispersion")
w = sp.Symbol("v", real=True)
note("Integrated form with a cold marginal", sp.Eq(F(w), n0 * sp.DiracDelta(w)))
cold_integral = sp.integrate(n0 * sp.DiracDelta(w) / (w - omega / k) ** 2, (w, -sp.oo, sp.oo))
show(sp.Eq(sp.Integral(F(w) / (w - omega / k) ** 2, (w, -sp.oo, sp.oo)), cold_integral))
agrees(1 - e**2 / (eps0 * m_e * k**2) * cold_integral, 1 - omega_pe_sq / omega**2, lhs=eps_L)

# %% Imaginary part of Z
section("Imaginary part of Z", script="landau-damping-growth")
note("Plemelj: the causal contour adds", I * sp.pi, "times the integrand at the pole")
gaussian = sp.exp(-x**2) / sp.sqrt(sp.pi)
agrees(sp.pi * gaussian.subs(x, zeta), sp.sqrt(sp.pi) * sp.exp(-zeta**2), lhs=sp.im(sp.Function("Z")(zeta)))
for zeta_value in (0.5, 1.7, 3.0):  # against the Faddeeva closed form
    exact = float(mp.im(z_function(zeta_value)))
    assert abs(exact - float(sp.sqrt(sp.pi) * sp.exp(-zeta_value**2))) <= 1e-12 * abs(exact)

# %% Asymptotic Z
section("Asymptotic Z", script="hot-isotropic-dispersion")
note("For", sp.Gt(zeta, 1), "expand the denominator,")
show(sp.Eq(1 / (x - zeta), -sp.Sum(x**sp.Symbol("n") / zeta ** (sp.Symbol("n") + 1),
                                   (sp.Symbol("n"), 0, sp.oo))))
note("and integrate term by term against the Gaussian (odd moments vanish):")
series = -sum(sp.integrate(x**n * sp.exp(-x**2), (x, -sp.oo, sp.oo)) / sp.sqrt(sp.pi)
              / zeta ** (n + 1) for n in range(6))
Z_asymptotic = -1 / zeta - 1 / (2 * zeta**3) - 3 / (4 * zeta**5)
agrees(series, Z_asymptotic, lhs=sp.re(sp.Function("Z")(zeta)))
exact = float(mp.re(z_function(8.0)))
assert abs(exact - float(Z_asymptotic.subs(zeta, 8))) <= 2e-5 * abs(exact)  # at zeta = 8

# %% Kinetic Bohm-Gross root
section("Kinetic Bohm-Gross root", script="hot-isotropic-dispersion")
W_sq, small = sp.symbols("W varepsilon", positive=True)  # W = omega^2, small = bookkeeping
note("Insert the asymptotic", sp.re(sp.Function("Z")(zeta)), "into", eps_L)
eps_asymptotic = show(sp.Eq(eps_L, 1 + sp.expand(1 + zeta * Z_asymptotic) / (k**2 * lambda_D_sq))).rhs
eps_omega = sp.expand(eps_asymptotic.subs(zeta, sp.sqrt(W_sq) / (k * v_te_value)))
note("Keep terms to relative order", k**2, ", clear denominators:")
eps_omega = sum(term for term in sp.Add.make_args(eps_omega)
                if sp.degree(term.as_numer_denom()[1], W_sq) <= 2)
quadratic = sp.numer(sp.together(eps_omega))
show(sp.Eq(quadratic.subs(W_sq, omega**2), 0))
roots = sp.solve(quadratic, W_sq)
root = [r for r in roots if sp.limit(r.subs(k, 0), k, 0) != 0][0]
bohm_gross = sp.series(root.subs(k, small * k), small, 0, 3).removeO().subs(small, 1)
agrees(bohm_gross, omega_pe_sq + 3 * k**2 * k_B * T_e / m_e, lhs=omega**2)
si.check(bohm_gross, omega_pe_sq + 3 * k**2 * k_B * T_e / m_e, unit=u.second**-2, units=UNITS)
stated_499 = omega_pe_sq * (1 + 3 * k**2 * lambda_D_sq)
si.check(bohm_gross, stated_499)
W_BOHM_GROSS = sp.sqrt(1 + 3 * a**2)  # omega_r / omega_pe
agrees(sp.sqrt(stated_499.subs(k, a / sp.sqrt(lambda_D_sq)) / omega_pe_sq), W_BOHM_GROSS,
       lhs=sp.Symbol("omega_r") / w_pe)

# %% First-derivative and integrated forms
section("First-derivative and integrated forms", script="hot-resonant-particles")
a_res = sp.Symbol("a")  # a = omega/k
agrees(sp.factor(k * sp.diff(F(v), v) / (omega - k * v)), -sp.diff(F(v), v) / (v - omega / k),
       lhs=k * sp.diff(F(v), v) / (omega - k * v))
note("Integrate by parts with", sp.Eq(a_res, omega / k), "; the boundary term vanishes:")
by_parts = sp.diff(F(v) / (v - a_res), v)
show(sp.Eq(sp.Derivative(F(v) / (v - a_res), v), by_parts))
assert sp.simplify(sp.diff(F(v), v) / (v - a_res) - by_parts - F(v) / (v - a_res) ** 2) == 0
show(sp.Eq(sp.Integral(sp.diff(F(v), v) / (v - a_res), (v, -sp.oo, sp.oo)),
           sp.Integral(F(v) / (v - a_res) ** 2, (v, -sp.oo, sp.oo))))
a_complex = mp.mpc(0.7, 0.4)  # numerical check, Gaussian F and Im a > 0
left = mp.quad(lambda t: -2 * t * mp.exp(-t**2) / (t - a_complex), [-mp.inf, 0, mp.inf])
right = mp.quad(lambda t: mp.exp(-t**2) / (t - a_complex) ** 2, [-mp.inf, 0, mp.inf])
assert abs(left - right) < 1e-10

# %% Resonant imaginary part
section("Resonant imaginary part", script="hot-resonant-particles")
v_res, eta = 0.8, 1e-6  # numerical Plemelj check
shifted = lambda t: mp.exp(-(t - 0.3) ** 2)  # noqa: E731
boundary = mp.quad(lambda t: shifted(t) / (t - v_res - 1j * eta),
                   [-mp.inf, v_res - 1, v_res, v_res + 1, mp.inf])
assert abs(float(mp.im(boundary)) - float(mp.pi * shifted(v_res))) <= 1e-4 * float(mp.pi * shifted(v_res))
S, PV = sp.symbols("S PV", real=True)  # S = F'(v_res), PV = principal value
note("Plemelj with slope", sp.Eq(S, sp.Symbol("F'(v_res)")), "and principal value", PV)
eps_plemelj = show(sp.Eq(eps_L, 1 - q**2 / (eps0 * m * k**2) * (PV + I * sp.pi * S))).rhs
agrees(sp.im(eps_plemelj), -(sp.pi * q**2) / (eps0 * m * k**2) * S, lhs=sp.im(eps_L))

# %% Weak-rate relation
section("Weak-rate relation", script="landau-damping-growth")
eps_r, eps_i, rate = sp.symbols("epsilon_r epsilon_i gamma", real=True)
slope = sp.Symbol("epsilon_r'", real=True)
note("Taylor expand at", sp.Symbol("omega_r") + I * rate, "with",
     sp.Eq(slope, sp.Derivative(sp.Function("epsilon_r")(omega), omega)), "; drop", rate,
     "times the small", eps_i)
expansion = eps_r + I * eps_i + I * rate * slope
show(sp.Eq(sp.Function("epsilon_L")(sp.Symbol("omega_r") + I * rate), expansion))
assert sp.simplify(expansion - (eps_r + I * eps_i + I * rate * slope)) == 0
assert sp.re(expansion) == eps_r  # real part: eps_r(omega_r) = 0
agrees(sp.solve(sp.im(expansion), rate)[0], -eps_i / slope, lhs=rate)

# %% Landau damping rate
section("Landau damping rate", script="landau-damping-growth")
si.check(sp.sqrt(2) * sp.sqrt(omega_pe_sq) * sp.sqrt(lambda_D_sq), v_te_value,
         unit=u.meter / u.second, units=UNITS)  # v_te = sqrt(2) omega_pe lambda_D
w = sp.Symbol("omega", positive=True)
note("With", sp.Eq(v_te, sp.sqrt(2) * w_pe * lambda_D), ":", sp.Eq(zeta, w / (sp.sqrt(2) * a * w_pe)))
eps_real = 1 + (1 + zeta * Z_asymptotic) / a**2
eps_imag = zeta * sp.sqrt(sp.pi) * sp.exp(-zeta**2) / a**2
agrees(eps_imag, sp.sqrt(sp.pi) * zeta * sp.exp(-zeta**2) / a**2, lhs=eps_i)
slope_value = sp.limit(sp.diff(eps_real.subs(zeta, w / (sp.sqrt(2) * a * w_pe)), w).subs(w, w_pe), a, 0)
agrees(slope_value, 2 / w_pe, lhs=slope)
zeta_sq = sp.expand(w_pe**2 * (1 + 3 * a**2) / (2 * a**2 * w_pe**2))
agrees(zeta_sq, 1 / (2 * a**2) + sp.Rational(3, 2), lhs=zeta**2)
note("Prefactor with", sp.Eq(zeta, 1 / (sp.sqrt(2) * a)), "; weak-rate relation", sp.Eq(gamma, -eps_i / slope, evaluate=False))
prefactor = (sp.sqrt(sp.pi) * zeta / a**2).subs(zeta, 1 / (sp.sqrt(2) * a))
landau = -prefactor * sp.exp(-zeta_sq) / slope_value / w_pe
GAMMA_LANDAU = -sp.sqrt(sp.pi / 8) * a ** (-3) * sp.exp(-1 / (2 * a**2) - sp.Rational(3, 2))
agrees(landau, GAMMA_LANDAU, lhs=gamma / w_pe)
si.check(landau * w_pe, -sp.sqrt(sp.pi / 8) * w_pe * sp.exp(-sp.Rational(3, 2)) * a ** (-3)
         * sp.exp(-1 / (2 * a**2)))


def kinetic_root(a_value, guess):
    """Complex root W = omega/omega_pe of EPS_L_MAXWELL = 0 at k lambda_D = a."""
    eps = sp.lambdify((zeta, Z, a), EPS_L_MAXWELL, "mpmath")
    a_mp = mp.mpf(a_value)

    def dispersion(W):
        zeta_value = W / (mp.sqrt(2) * a_mp)  # zeta = omega/(k v_te)
        return eps(zeta_value, z_function(zeta_value), a_mp)

    return mp.findroot(dispersion, guess)


exact_root = kinetic_root(0.2, mp.mpc(mp.sqrt(1 + 3 * 0.2**2), -0.001))
assert abs(float(mp.im(exact_root)) - float(GAMMA_LANDAU.subs(a, 0.2))) <= 0.25 * abs(
    float(GAMMA_LANDAU.subs(a, 0.2)))  # exact Maxwellian root at a = 0.2, within 25 %
show(sp.Eq(sp.Symbol("gamma_exact") / w_pe, sp.Float(float(mp.im(exact_root)), 3)))
note("against", sp.Eq(gamma / w_pe, sp.Float(float(GAMMA_LANDAU.subs(a, 0.2)), 3), evaluate=False), "at",
     sp.Eq(a, sp.Float(0.2, 2)))

# %% Spatial damping rate
section("Spatial damping rate", script="landau-damping-growth")
k_i, k_r = sp.symbols("k_i k_r", real=True)
w_r = sp.Symbol("omega_r", positive=True)
note("Real frequency, complex wave number:")
expansion = show(sp.Eq(sp.Function("omega")(k_r + I * k_i), w_r + I * rate + I * k_i * v_g)).rhs
spatial = sp.solve(sp.im(expansion), k_i)[0]
agrees(spatial, -rate / v_g, lhs=k_i)
si.check(spatial.subs(rate, gamma), -gamma / v_g, unit=u.meter**-1, units=UNITS)

# %% Worked example: warm Langmuir root
section("Worked example: warm Langmuir root", script="hot-isotropic-dispersion")
example = {**LAB, T_e: 10 * u.electronvolt / u.boltzmann_constant}
note("Input", sp.Eq(n0, LAB[n0], evaluate=False), ",", sp.Eq(k_B * T_e, 10 * u.electronvolt, evaluate=False),
     ",", sp.Eq(a, sp.Float(0.2, 2)))
debye = evaluate(lambda_D, sp.sqrt(lambda_D_sq), example, u.meter)
close_to(debye, 2.35e-4, rtol=3e-3)
close_to(evaluate(k, a / lambda_D, {a: 0.2, lambda_D: debye * u.meter}, 1 / u.meter), 851, rtol=3e-3)
ratio = number(W_BOHM_GROSS, {a: 0.2})
show(sp.Eq(sp.Symbol("omega_r") / w_pe, sp.Float(ratio, 3)))
close_to(ratio, 1.06, rtol=5e-3)
close_to(evaluate(sp.Symbol("omega_r"), W_BOHM_GROSS * sp.sqrt(omega_pe_sq), {**LAB, a: 0.2}, 1 / u.second),
         5.97e9, rtol=3e-3)

# %% Worked example: resonant velocity
section("Worked example: resonant velocity", script="hot-resonant-particles")
close_to(evaluate(w_pe, sp.sqrt(omega_pe_sq), LAB, 1 / u.second), 5.64e9, rtol=1e-3)
note("At", sp.Eq(a, sp.Float(0.3, 2)), "; resonance at the phase velocity,",
     sp.Eq(sp.Symbol("v_res"), sp.Symbol("omega_r") / k))
ratio = number(W_BOHM_GROSS, {a: 0.3})
show(sp.Eq(sp.Symbol("omega_r") / w_pe, sp.Float(ratio, 3)))
close_to(ratio, 1.13, rtol=5e-3)
resonance = number(W_BOHM_GROSS / (sp.sqrt(2) * a), {a: 0.3})  # v_te = sqrt(2) omega_pe lambda_D
show(sp.Eq(sp.Symbol("v_res") / v_te, sp.Float(resonance, 3)))
close_to(resonance, 2.66, rtol=3e-3)

# %% Worked example: spatial damping
section("Worked example: spatial damping", script="landau-damping-growth")
damping = {rate: -1.13e8 / u.second, v_g: 1.0e6 * u.meter / u.second}
note("Input", rounded(sp.Eq(rate, damping[rate])), ",", rounded(sp.Eq(v_g, damping[v_g])))
k_i_value = evaluate(k_i, spatial, damping, 1 / u.meter)
close_to(k_i_value, 113, rtol=1e-3)
close_to(evaluate(sp.Symbol("L_amp"), 1 / spatial, damping, u.meter), 8.85e-3, rtol=1e-3)
close_to(evaluate(sp.Symbol("tau_d"), -1 / rate, damping, u.second), 8.85e-9, rtol=1e-3)

# %% Transverse Vlasov response
section("Transverse Vlasov response", script="hot-transverse-waves")
vx, vy, vz = sp.symbols("v_x v_y v_z", real=True)


class _F0(sp.Function):
    """Equilibrium f_0(v_x, v_y, v_z), typeset without its arguments."""

    def _latex(self, printer, exp=None):
        return "f_0" if exp is None else "f_0^{%s}" % exp

    def _pretty(self, printer):
        return printer._print(sp.Symbol("f_0"))


f0 = _F0(vx, vy, vz)
E_vec, k_vec, v_vec = sp.Matrix([E1, 0, 0]), sp.Matrix([0, 0, k]), sp.Matrix([vx, vy, vz])
note("Field", sp.Eq(sp.Symbol("E_1"), E1 * sp.Symbol("e_x")), "; Faraday gives")
B1 = k_vec.cross(E_vec) / omega
agrees(B1[1], k / omega * E1, lhs=sp.Symbol("B_1y"))
assert B1[0] == 0 and B1[2] == 0
force = E_vec + v_vec.cross(B1)
show(sp.Eq(sp.Symbol("F") / q, sp.ImmutableMatrix(force), evaluate=False))
grad_v = sp.Matrix([sp.diff(f0, s) for s in (vx, vy, vz)])
vlasov = -I * (omega - k * vz) * f1 + q / m * force.dot(grad_v)
agrees(vlasov, -I * (omega - k * vz) * f1 + (q / m) * E1 * (
    (1 - k * vz / omega) * sp.diff(f0, vx) + k * vx / omega * sp.diff(f0, vz)), lhs=sp.S.Zero)
f1_transverse = sp.solve(vlasov, f1)[0]
agrees(f1_transverse, (-I * q * E1) / (m * omega) * (
    (omega - k * vz) * sp.diff(f0, vx) + k * vx * sp.diff(f0, vz)) / (omega - k * vz), lhs=f1)

# %% Transverse Ampère law
section("Transverse Ampère law", script="hot-transverse-waves")
J = sp.Symbol("J_1")
note("Ampère with Faraday, for", sp.Eq(sp.Symbol("J"), J * sp.Symbol("e_x")), ":")
residual = I * k_vec.cross(B1) - (sp.Matrix([J, 0, 0]) / (eps0 * c**2) - I * omega * E_vec / c**2)
ampere = show(sp.Eq(k**2 * c**2, omega**2 + I * omega * J / (eps0 * E1))).rhs
si.check(sp.solve(sp.Eq(k**2 * c**2, ampere), J)[0], sp.solve(residual[0], J)[0])
note("Insert", sp.Eq(J, sp.Integral(q * vx * f1, sp.Symbol("v"))), "; integrand per species:")
integrand = sp.simplify((ampere - omega**2).subs(J, q * vx * f1_transverse))
agrees(integrand, q**2 / (eps0 * m) * (vx * sp.diff(f0, vx) + k * vx**2 / (omega - k * vz)
                                         * sp.diff(f0, vz)), lhs=k**2 * c**2 - omega**2)

# %% Transverse integration by parts
section("Transverse integration by parts", script="hot-transverse-waves")
agrees(sp.diff(1 / (omega - k * vz), vz), k / (omega - k * vz) ** 2,
       lhs=sp.Derivative(1 / (omega - k * vz), vz))
a_x, a_y, a_z = sp.symbols("a_x a_y a_z", positive=True)
gaussian3 = n0 / (sp.pi**sp.Rational(3, 2) * a_x * a_y * a_z) * sp.exp(
    -vx**2 / a_x**2 - vy**2 / a_y**2 - vz**2 / a_z**2)
note("For an anisotropic Gaussian of density", n0, ":")
first_identity = sp.integrate(vx * sp.diff(gaussian3, vx), (vx, -sp.oo, sp.oo), (vy, -sp.oo, sp.oo),
                              (vz, -sp.oo, sp.oo))
agrees(first_identity, -n0, lhs=sp.Integral(vx * sp.Derivative(sp.Symbol("f_0"), vx), sp.Symbol("v")))
left = k * vx**2 / (omega - k * vz) * sp.diff(f0, vz)
right = -(k**2 * vx**2 * f0) / (omega - k * vz) ** 2
assert sp.simplify(left - right - sp.diff(k * vx**2 * f0 / (omega - k * vz), vz)) == 0
note("The resonant integrands differ by a total", vz, "derivative:")
show(sp.Eq(sp.Integral(left, sp.Symbol("v")), sp.Integral(right, sp.Symbol("v"))))
I_res = sp.Symbol("I_res")
show(sp.Eq(I_res, sp.Integral(vx**2 * sp.Symbol("f_0") / (omega - k * vz) ** 2, sp.Symbol("v"))))
assembled = omega**2 + q**2 / (eps0 * m) * (-n0 - k**2 * I_res)
agrees(assembled, omega**2 - n0 * q**2 / (eps0 * m) - q**2 * k**2 / (eps0 * m) * I_res,
       lhs=k**2 * c**2)

# %% Cold transverse branch
section("Cold transverse branch", script="hot-transverse-waves")
w_p = sp.Symbol("omega_p", positive=True)
cold = n0 * sp.DiracDelta(vx) * sp.DiracDelta(vy) * sp.DiracDelta(vz)
note("Cold plasma", sp.Eq(sp.Symbol("f_0"), cold))
I_cold = sp.integrate(vx**2 * cold / (omega - k * vz) ** 2, (vx, -sp.oo, sp.oo), (vy, -sp.oo, sp.oo),
                      (vz, -sp.oo, sp.oo))
show(sp.Eq(I_res, I_cold))
cold_branch = omega**2 - w_p**2 - q**2 * k**2 / (eps0 * m) * I_cold
agrees(cold_branch, omega**2 - w_p**2, lhs=k**2 * c**2)
agrees(sp.solve(sp.Eq(k**2 * c**2, cold_branch), omega**2)[0], k**2 * c**2 + w_p**2, lhs=omega**2)

# %% Anisotropic transverse instability
section("Anisotropic transverse instability", script="hot-transverse-waves")
F_perp = sp.Function("F")(vx, vy)
v_rms = sp.Symbol("v_x,rms", positive=True)
vx2 = v_rms**2  # mean square v_x of the equilibrium
note("Equilibrium", sp.Eq(sp.Symbol("f_0"), sp.DiracDelta(vz) * F_perp), "; the", vz, "integral first:")
inner = sp.integrate(vx**2 * sp.DiracDelta(vz) * F_perp / (omega - k * vz) ** 2, (vz, -sp.oo, sp.oo))
show(sp.Eq(sp.Integral(vx**2 * sp.DiracDelta(vz) * F_perp / (omega - k * vz) ** 2, (vz, -sp.oo, sp.oo)), inner))
I_aniso = sp.simplify(inner / (vx**2 * F_perp)) * n0 * vx2  # n0 <v_x^2> = int v_x^2 F
agrees(I_aniso, n0 * vx2 / omega**2, lhs=I_res)
wp_sq = n0 * e**2 / (eps0 * m_e)
to_wp = {n0: w_p**2 * eps0 * m_e / e**2}
dispersion = omega**2 - wp_sq - e**2 * k**2 / (eps0 * m_e) * I_aniso
agrees(dispersion.subs(to_wp), (omega**2 - wp_sq * (1 + k**2 * vx2 / omega**2)).subs(to_wp),
       lhs=k**2 * c**2)
quartic = sp.expand((dispersion - k**2 * c**2) * omega**2)
agrees(sp.collect(quartic.subs(to_wp), omega),
       (omega**4 - (k**2 * c**2 + wp_sq) * omega**2 - k**2 * wp_sq * vx2).subs(to_wp), lhs=sp.S.Zero)
Y = sp.Symbol("Y")  # Y = omega^2
roots = sp.solve(quartic.subs(omega, sp.sqrt(Y)), Y)
root_sum = k**2 * c**2 + wp_sq
root_disc = sp.sqrt(root_sum**2 + 4 * k**2 * wp_sq * vx2)
for r in roots:
    assert any(sp.simplify(r - (root_sum + sign * root_disc) / 2) == 0 for sign in (1, -1))
for sign, name in ((1, "Y_+"), (-1, "Y_-")):
    show(sp.Eq(sp.Symbol(name), ((root_sum + sign * root_disc) / 2).subs(to_wp)))
assert sp.simplify(root_disc**2 - root_sum**2 - 4 * k**2 * wp_sq * vx2) == 0  # Y_- < 0
note("Y_- is negative: purely growing", sp.Eq(omega, I * gamma, evaluate=False), ",",
     sp.Eq(gamma**2, -sp.Symbol("Y_-"), evaluate=False))
growth_sq = -(root_sum - root_disc) / 2
agrees(growth_sq.subs(to_wp), ((root_disc - root_sum) / 2).subs(to_wp), lhs=gamma**2)
si.check(growth_sq, (root_disc - root_sum) / 2, unit=u.second**-2, units={**UNITS, v_rms: u.meter / u.second})

# %% Worked example: anisotropic growth
section("Worked example: anisotropic growth", script="hot-transverse-waves")
wp_value = evaluate(w_p, sp.sqrt(wp_sq), LAB, 1 / u.second)
close_to(wp_value, 5.64e9, rtol=1e-3)
note("At", sp.Eq(k * c / w_p, sp.Float(0.5, 2)), "and", sp.Eq(vx2 / c**2, sp.Float(0.01, 2)))
plasma = {w_p: wp_value / u.second}
k_value = evaluate(k, 0.5 * w_p / c, plasma, 1 / u.meter)
close_to(k_value, 9.41, rtol=1e-3)
close_to(evaluate(sp.Symbol("lambda"), 2 * sp.pi / k, {k: k_value / u.meter}, u.meter), 0.668, rtol=2e-3)
K_sq, V_sq = sp.symbols("K^2 V^2", positive=True)  # (k c/w_p)^2, <v_x^2>/c^2
normalized_growth = sp.sqrt(growth_sq.subs(to_wp).subs({k: sp.sqrt(K_sq) * w_p / c,
                                                         v_rms: sp.sqrt(V_sq) * c}) / w_p**2)
show(sp.Eq(gamma / w_p, sp.simplify(normalized_growth)))
growth = number(normalized_growth, {K_sq: 0.25, V_sq: 0.01})
show(sp.Eq(gamma / w_p, sp.Float(growth, 3)))
close_to(growth, 4.47e-2, rtol=1e-3)
close_to(evaluate(gamma, growth * w_p, plasma, 1 / u.second), 2.52e8, rtol=2e-3)

# %% Two-stream dispersion
section("Two-stream dispersion", script="two-stream-instability")
v0 = sp.Symbol("v_0", positive=True)
w = sp.Symbol("v", real=True)
beams = n0 / 2 * (sp.DiracDelta(w - v0) + sp.DiracDelta(w + v0))
note("Two cold beams,", sp.Eq(F(w), beams))
assert sp.simplify(sp.integrate(beams, (w, -sp.oo, sp.oo)) - n0) == 0
beam_integral = sp.integrate(beams / (w - omega / k) ** 2, (w, -sp.oo, sp.oo))
show(sp.Eq(sp.Integral(F(w) / (w - omega / k) ** 2, (w, -sp.oo, sp.oo)), sp.factor(beam_integral)))
D = (1 - e**2 / (eps0 * m_e * k**2) * beam_integral).subs(to_wp)
agrees(D, 1 - w_p**2 / (2 * (omega - k * v0) ** 2) - w_p**2 / (2 * (omega + k * v0) ** 2), lhs=eps_L)

# %% Two-stream roots
section("Two-stream roots", script="two-stream-instability")
xx, yy = sp.symbols("x y", positive=True)
note("Clear denominators:")
quartic = sp.expand(sp.simplify(D * (omega**2 - k**2 * v0**2) ** 2))
agrees(quartic, omega**4 - (2 * k**2 * v0**2 + w_p**2) * omega**2 + k**2 * v0**2 * (k**2 * v0**2 - w_p**2), lhs=sp.S.Zero)
note("Normalize", sp.Eq(xx, k**2 * v0**2 / w_p**2), ",", sp.Eq(yy, omega**2 / w_p**2))
quad = sp.expand((quartic / w_p**4).subs({omega: w_p * sp.sqrt(yy), v0: w_p * sp.sqrt(xx) / k}))
agrees(quad, yy**2 - (2 * xx + 1) * yy + xx * (xx - 1), lhs=sp.S.Zero)
y_minus = xx + sp.Rational(1, 2) - sp.sqrt(1 + 8 * xx) / 2
for r in sp.solve(quad, yy):
    assert any(sp.simplify(r - (xx + sp.Rational(1, 2) + sign * sp.sqrt(1 + 8 * xx) / 2)) == 0
               for sign in (1, -1))
show(sp.Eq(sp.Symbol("y_-"), y_minus))
note("Unstable band:", sp.Lt(sp.Symbol("y_-"), 0), "exactly when", sp.Gt(1 + 8 * xx, (1 + 2 * xx) ** 2))
si.check(sp.expand((1 + 2 * xx) ** 2), 1 + 4 * xx + 4 * xx**2)
band = sp.solve_univariate_inequality(1 + 8 * xx > 1 + 4 * xx + 4 * xx**2, xx, relational=False)
assert band == sp.Interval.open(0, 1)
show(sp.Eq(sp.Symbol("x"), band, evaluate=False))
G2_TWO_STREAM = sp.sqrt(1 + 8 * xx) / 2 - xx - sp.Rational(1, 2)
agrees(-y_minus, G2_TWO_STREAM, lhs=gamma**2 / w_p**2)

# %% Maximum two-stream growth
section("Maximum two-stream growth", script="two-stream-instability")
extrema = sp.solve(sp.diff(G2_TWO_STREAM, xx), xx)
assert extrema == [sp.Rational(3, 8)]
show(sp.Eq(sp.Derivative(gamma**2 / w_p**2, xx), sp.diff(G2_TWO_STREAM, xx)))
show(sp.Eq(xx, extrema[0]))
agrees(G2_TWO_STREAM.subs(xx, extrema[0]), sp.Rational(1, 8), lhs=gamma**2 / w_p**2)
agrees(sp.sqrt(G2_TWO_STREAM.subs(xx, extrema[0])), 1 / (2 * sp.sqrt(2)), lhs=gamma / w_p)
agrees(sp.sqrt(extrema[0]), sp.sqrt(sp.Rational(3, 8)), lhs=k * v0 / w_p)

# %% Worked example: two-stream growth
section("Worked example: two-stream growth", script="two-stream-instability")
wp_value = evaluate(w_p, sp.sqrt(wp_sq), LAB, 1 / u.second)
close_to(wp_value, 5.64e9, rtol=1e-3)
note("Beams at", sp.Eq(v0, sp.Float(0.1, 2) * c), ",", sp.Eq(k * v0 / w_p, sp.Float(0.5, 2)))
k_value = evaluate(k, 0.5 * w_p / (0.1 * c), {w_p: wp_value / u.second}, 1 / u.meter)
close_to(k_value, 94.1, rtol=1e-3)
close_to(evaluate(sp.Symbol("lambda"), 2 * sp.pi / k, {k: k_value / u.meter}, u.meter), 6.68e-2, rtol=2e-3)
growth = number(sp.sqrt(G2_TWO_STREAM), {xx: 0.25})
show(sp.Eq(gamma / w_p, sp.Float(growth, 3)))
close_to(growth, 0.341, rtol=2e-3)
close_to(evaluate(gamma, growth * w_p, {w_p: wp_value / u.second}, 1 / u.second), 1.92e9, rtol=2e-3)

# %% Gyro-orbit characteristics
section("Gyro-orbit characteristics", script="hot-magnetized-waves")
B0, v_perp, v_par = sp.symbols(r"B_0 v_\perp v_\parallel", real=True)
theta = sp.Function("theta")(t)
Omega = q * B0 / m  # signed gyrofrequency
si.check(Omega, q * B0 / m, unit=u.second**-1, units={**UNITS, B0: u.tesla})
v_orbit = sp.Matrix([v_perp * sp.cos(theta), -v_perp * sp.sin(theta), v_par])
note("Gyrating velocity with", sp.Eq(sp.Derivative(theta, t), sp.Symbol("Omega_s")), ",",
     sp.Eq(sp.Symbol("Omega_s"), Omega))
show(sp.Eq(sp.Symbol("v"), sp.ImmutableMatrix(v_orbit), evaluate=False))
dv_dt = v_orbit.diff(t).subs(sp.Derivative(theta, t), Omega)
lorentz = q / m * v_orbit.cross(sp.Matrix([0, 0, B0]))
assert sp.simplify(dv_dt - lorentz) == sp.zeros(3, 1)
show(sp.Eq(sp.ImmutableMatrix(dv_dt), sp.ImmutableMatrix(lorentz), evaluate=False))
agrees(dv_dt[0], Omega * v_orbit[1], lhs=sp.Derivative(sp.Symbol("v_x"), t))
agrees(dv_dt[1], -Omega * v_orbit[0], lhs=sp.Derivative(sp.Symbol("v_y"), t))
g = sp.Function("g")
assert sp.simplify(sp.diff(g(v_orbit[2], sp.sqrt(v_orbit[0] ** 2 + v_orbit[1] ** 2)), t)) == 0
note("Any", g(v_par, v_perp), "is constant along the orbit: a gyrotropic equilibrium")

# %% Gyroangle harmonic response
section("Gyroangle harmonic response", script="hot-magnetized-waves")
th, n_h = sp.symbols("theta n", real=True)
Om, k_par = sp.symbols(r"Omega_s k_\parallel", real=True)
harmonic = sp.exp(I * (k_par * z - omega * t + n_h * th))
note("Streaming operator", sp.Derivative(sp.Symbol("f"), t) + v_par * sp.Derivative(sp.Symbol("f"), z)
     + Om * sp.Derivative(sp.Symbol("f"), th), "on the harmonic", harmonic)
operator = sp.simplify((sp.diff(harmonic, t) + v_par * sp.diff(harmonic, z) + Om * sp.diff(harmonic, th))
                       / harmonic)
agrees(operator, -I * (omega - k_par * v_par - n_h * Om), lhs=sp.Symbol("L"))
source, f_n = sp.symbols("S_sn f_sn")
agrees(sp.solve(sp.Eq(operator * f_n, source), f_n)[0], I * source / (omega - k_par * v_par - n_h * Om), lhs=f_n)
w_r = sp.Symbol("omega_r", real=True)
note("Resonance where the denominator vanishes:")
agrees(sp.solve(w_r - k_par * v_par - n_h * Om, v_par)[0], (w_r - n_h * Om) / k_par,
       lhs=sp.Symbol("v_res"))

# %% Circular forcing
section("Circular forcing", script="hot-magnetized-waves")
E_x = sp.Symbol("E_x")
v_x, v_y = v_perp * sp.cos(th), -v_perp * sp.sin(th)
for sigma in (1, -1):
    E_y = -I * sigma * E_x  # circular basis of chapter 12
    note("Circular field", sp.Eq(sp.Symbol("E_y"), E_y))
    agrees(sp.expand((E_x * v_x + E_y * v_y).rewrite(sp.exp)), sp.expand(E_x * v_perp * sp.exp(I * sigma * th)), lhs=sp.Symbol("E") * sp.Symbol("v"))
note("so circular forcing selects the single harmonic", sp.Eq(n_h, sp.Symbol("sigma")))

# %% Finite-Larmor-radius weights
section("Finite-Larmor-radius weights", script="hot-magnetized-waves")
X0, th0 = sp.symbols("X theta_0", real=True)
Om_pos = sp.Symbol("Omega", positive=True)
theta_t = Om_pos * t + th0
x_orbit = show(sp.Eq(sp.Symbol("x"), X0 + v_perp / Om_pos * sp.sin(theta_t))).rhs
agrees(sp.diff(x_orbit, t), v_perp * sp.cos(theta_t), lhs=sp.Derivative(sp.Symbol("x"), t))
th_j, a_j = sp.symbols("theta a", real=True)
n_sum = sp.Symbol("n")
note("The phase", I * k * sp.Symbol("x"), "contains", sp.exp(I * a_j * sp.sin(th_j)), "with",
     sp.Eq(a_j, k * v_perp / Om_pos), "; Jacobi-Anger:")
show(sp.Eq(sp.exp(I * a_j * sp.sin(th_j)),
           sp.Sum(sp.besselj(n_sum, a_j) * sp.exp(I * n_sum * th_j), (n_sum, -sp.oo, sp.oo))))
order = 8  # checked as a power series in a up to a^7
lhs = sp.series(sp.exp(I * a_j * sp.sin(th_j)), a_j, 0, order).removeO()
rhs = sum(sp.series(sp.besselj(n, a_j), a_j, 0, order).removeO() * sp.exp(I * n * th_j)
          for n in range(-order, order + 1))
assert sp.simplify(sp.expand((lhs - rhs).rewrite(sp.exp))) == 0

# %% Worked example: cyclotron resonances
section("Worked example: cyclotron resonances", script="hot-magnetized-waves")
w_ce = sp.Symbol("omega_ce", positive=True)
close_to(evaluate(w_ce, e * B0 / m_e, {B0: 1e-2 * u.tesla}, 1 / u.second), 1.76e9, rtol=1e-3)
close_to(evaluate(v_te, v_te_value, {T_e: 10 * u.electronvolt / u.boltzmann_constant}, u.meter / u.second),
         1.88e6, rtol=3e-3)
note("Drive", sp.Eq(omega / w_ce, sp.Float(0.8, 2)), ",", sp.Eq(k_par * v_te / w_ce, sp.Float(1.5, 2)),
     "; electrons", sp.Eq(Om, -w_ce))
drive = {w_r: 0.8, k_par: 1.5, Om: -1.0}  # in units of omega_ce and v_te
resonant = (w_r - n_h * Om) / k_par
for n_value, printed, rtol in ((0, 0.533, 1e-3), (-1, -0.133, 3e-3)):
    value = number(resonant, {**drive, n_h: n_value})
    show(sp.Eq(sp.Symbol(f"v_res,{n_value}") / v_te, sp.Float(value, 3)))
    close_to(value, printed, rtol=rtol)
close_to(evaluate(k_par, 1.5 * w_ce / v_te, {w_ce: 1.76e9 / u.second,
                                                          v_te: 1.88e6 * u.meter / u.second},
                  1 / u.meter), 1.40e3, rtol=4e-3)
close_to(evaluate(omega, 0.8 * w_ce, {w_ce: 1.76e9 / u.second}, 1 / u.second),
         1.41e9, rtol=2e-3)

# %% Plot: exact Maxwellian Langmuir root against Bohm-Gross and Landau
mp.mp.dps = 30
a_grid = np.linspace(0.12, 0.6, 97)
guess = mp.mpc(float(W_BOHM_GROSS.subs(a, a_grid[0])), float(GAMMA_LANDAU.subs(a, a_grid[0])))
exact = []
for a_value in a_grid:  # continuation in k lambda_D from the weakly damped end
    guess = kinetic_root(a_value, guess)
    exact.append(complex(guess))
mp.mp.dps = 15
exact = np.array(exact)
PANEL = (2.6, 3.0)  # one panel of a side-by-side pair

fig, ax = figure(*PANEL)
ax.plot(a_grid, exact.real, color=BLUE)
ax.plot(a_grid, sp.lambdify(a, W_BOHM_GROSS, "numpy")(a_grid), color=ORANGE, ls="--")
label(ax, 0.36, 1.45, "exact root", BLUE, ha="right")
label(ax, 0.59, 1.2, "Bohm-Gross\n$\\sqrt{1+3a^2}$", ORANGE, ha="right", va="top")
ax.set(xlim=(0.12, 0.6), ylim=(1, 1.6), xticks=[0.2, 0.4, 0.6], yticks=[1, 1.2, 1.4, 1.6],
       xlabel=r"$a=k\lambda_{De}$ [1]", ylabel=r"$\omega_r/\omega_{pe}$ [1]")
save(fig, "hot-isotropic-dispersion")

fig, ax = figure(*PANEL)
ax.plot(a_grid, -exact.imag, color=BLUE)
ax.plot(a_grid, -sp.lambdify(a, GAMMA_LANDAU, "numpy")(a_grid), color=ORANGE, ls="--")
label(ax, 0.42, 0.18, "exact root", BLUE, ha="right")
label(ax, 0.14, 0.12, "weak-damping\nasymptote", ORANGE)
ax.set(xlim=(0.12, 0.6), ylim=(0, 0.3), xticks=[0.2, 0.4, 0.6], yticks=[0, 0.1, 0.2, 0.3],
       xlabel=r"$a=k\lambda_{De}$ [1]", ylabel=r"$-\gamma/\omega_{pe}$ [1]")
save(fig, "hot-isotropic-damping")

# %% Plot: two-stream growth rate over the unstable band 0 < K < 1
growth_rate = sp.lambdify(xx, sp.sqrt(G2_TWO_STREAM), "numpy")
K_grid = np.linspace(0, 1, 300)
K_max, growth_max = float(sp.sqrt(extrema[0])), float(sp.sqrt(G2_TWO_STREAM.subs(xx, extrema[0])))
fig, ax = figure(4.2, 2.6)
ax.plot(K_grid, growth_rate(K_grid**2), color=BLUE)
ax.plot([K_max], [growth_max], "o", color=ORANGE, ms=4, zorder=3)
label(ax, K_max + 0.03, growth_max + 0.005, "max $1/(2\\sqrt{2})$ at $K=\\sqrt{3/8}$", ORANGE)
label(ax, 0.99, 0.02, "stable for $K>1$", GRAY, ha="right")
ax.set(xlim=(0, 1.1), ylim=(0, 0.42), xticks=[0, 0.25, 0.5, 0.75, 1],
       xlabel=r"$K=|k v_0|/\omega_p$ [1]", ylabel=r"$\gamma/\omega_p$ [1]")
save(fig, "two-stream-growth")

# %%
if __name__ == "__main__":
    report(__file__, "Chapter 14 · Waves in hot plasmas")
