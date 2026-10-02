# Appendix · Mathematical toolkit (src/appendices/mathematical-toolkit.typ)
#
# Energy moments of the kinetic equation, fluid energy balances (shown in one
# dimension, checked in three), and vector operators in orthogonal coordinates.

# %% Setup
import itertools

import sympy as sp
from sympy.physics import units as u

from kinetics import maxwellian, velocity_integral
from notebook import agrees, close_to, evaluate, note, report, section, show
from si import check

m, n = sp.symbols("m_s n_s", positive=True)
q = sp.Symbol("q_s", real=True)
U3 = sp.symbols("u_x u_y u_z", real=True)
C3 = sp.symbols("c_x c_y c_z", real=True)
P = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"P_{min(i, j) + 1}{max(i, j) + 1}"))  # symmetric
T3 = {}  # third central moments, the integral of c_i c_j c_k f
div, curl, grad, laplacian = (sp.Function(name) for name in ("div", "curl", "grad", "Delta"))


def moment(poly):
    """Velocity integral of poly(c) f, using only the moment definitions."""
    poly = sp.Poly(sp.expand(poly), *C3)
    out = 0
    for powers, coeff in poly.terms():
        k = sum(powers)
        if k == 0:
            val = n  # int f = n_s
        elif k == 1:
            val = 0  # int c f = 0 by definition of u_s
        elif k == 2:
            i, j = [ix for ix, p in enumerate(powers) for _ in range(p)]
            val = P[i, j] / m  # P_s = m int c c f
        elif k == 3:
            key = tuple(sorted(ix for ix, p in enumerate(powers) for _ in range(p)))
            val = T3.setdefault(key, sp.Symbol("T_" + "".join(map(str, key))))
        else:
            raise ValueError(powers)
        out += coeff * val
    return sp.expand(out)


def over_c(weight):
    """Unevaluated velocity integral of weight * f_s over the random velocity c, for display."""
    return sp.Integral(weight * sp.Function("f_s")(*C3), *[(c, -sp.oo, sp.oo) for c in C3])


# %% Energy moments
section("Energy moments", "mathematical-toolkit.typ:72")
u_vec, c_vec = sp.Matrix(U3), sp.Matrix(C3)
v_vec = u_vec + c_vec
K, U_int, p = sp.symbols("K_s U_s p")
c_x, c_y, c_z = C3
note("With", sp.Eq(sp.Symbol("v"), sp.Symbol("u_s") + sp.Symbol("c_s")), "the moments are defined by")
show(sp.Eq(over_c(1), n))
show(sp.Eq(over_c(c_x), 0))
show(sp.Eq(m * over_c(c_x * c_y), P[0, 1]))
K_expr = show(sp.Eq(K, m * n * u_vec.dot(u_vec) / 2)).rhs
U_expr = show(sp.Eq(U_int, P.trace() / 2)).rhs
second_moment = moment(m * v_vec.dot(v_vec) / 2)
agrees(second_moment - K_expr - U_expr + K + U_int, K + U_int, ":91", lhs=m / 2 * over_c(v_vec.dot(v_vec)))
assert sp.expand(second_moment - (K_expr + U_expr)) == 0
note("Isotropic pressure,", sp.Eq(sp.Symbol("P_s"), p * sp.Symbol("I")))
agrees((p * sp.eye(3)).trace() / 2, sp.Rational(3, 2) * p, ":239", lhs=U_int)
rho, speed = sp.symbols("rho u", positive=True)
check(rho * speed**2 / 2, rho * speed**2 / 2, unit=u.joule / u.meter**3,
      units={rho: u.kilogram / u.meter**3, speed: u.meter / u.second})

# %% Energy-flux decomposition
section("Energy-flux decomposition", "mathematical-toolkit.typ:208")
heat = [moment(m * c_vec.dot(c_vec) * c_vec[k] / 2) for k in range(3)]  # q_s definition
q_x = sp.Symbol("q_x")
Q_x = sp.Symbol("Q_x")
note("Heat flux and energy flux, x components")
show(sp.Eq(q_x, m / 2 * over_c(c_vec.dot(c_vec) * c_x)))
show(sp.Eq(Q_x, m / 2 * over_c(v_vec.dot(v_vec) * v_vec[0])))
P_dot_u = P * u_vec
fluxes = [moment(m * v_vec.dot(v_vec) * v_vec[k] / 2) for k in range(3)]
in_symbols = fluxes[0] - (K_expr + U_expr) * U3[0] - heat[0] + (K + U_int) * U3[0] + q_x
agrees(in_symbols, (K + U_int) * U3[0] + P_dot_u[0] + q_x, ":223", lhs=Q_x)
for k in range(3):
    assert sp.expand(fluxes[k] - (K_expr * U3[k] + U_expr * U3[k] + P_dot_u[k] + heat[k])) == 0  # :202
    assert sp.expand(fluxes[k] - ((K_expr + U_expr) * U3[k] + P_dot_u[k] + heat[k])) == 0  # :207

# %% Lorentz work by parts
section("Lorentz work by parts", "mathematical-toolkit.typ:131")
V3 = sp.symbols("v_x v_y v_z", real=True)
E3, B3 = sp.symbols("E_x E_y E_z", real=True), sp.symbols("B_x B_y B_z", real=True)
v, E_vec, B_vec = sp.Matrix(V3), sp.Matrix(E3), sp.Matrix(B3)
f = sp.Function("f")(*V3)
a = q / m * (E_vec + v.cross(B_vec))
energy = m * v.dot(v) / 2
grad_v = lambda g: sp.Matrix([g.diff(x) for x in V3])
div_v = lambda F: sum(sp.diff(F[i], V3[i]) for i in range(3))
# Product rule (:153): eps a.df/dv = div_v(eps f a) - f a.d(eps)/dv - eps f div_v(a).
assert sp.expand(energy * a.dot(grad_v(f)) - (div_v(energy * f * a) - f * a.dot(grad_v(energy))
                                                - energy * f * div_v(a))) == 0
note("Integrate the Lorentz term by parts; the acceleration field is divergence-free in velocity:")
divergence = sp.Add(*[sp.Derivative(a[i], V3[i]) for i in range(3)], evaluate=False)
agrees(sp.expand(divergence.doit()), 0, ":169", lhs=divergence)
a_components = sp.Matrix(sp.symbols("a_x a_y a_z"))
f_value = sp.Symbol("f")
note("The remaining term", -m * f_value * a_components.dot(v), "loses its magnetic part pointwise:")
agrees(sp.expand(-m * f_value * a.dot(v)), -q * f_value * E_vec.dot(v), ":187")
note("Concrete check with a shifted Maxwellian", sp.Function("f_M")(*V3))
T, k_B = sp.symbols("T k_B", positive=True)
f_M = maxwellian(n, m, k_B * T, V3, U3)
work = velocity_integral(energy * a.dot(grad_v(f_M)), V3, U3)
f_M_sym = sp.Function("f_M")(*V3)
I_a = sp.Symbol("I_a")
show(sp.Eq(I_a, sp.Integral(energy * a_components.dot(grad_v(f_M_sym)), *[(x, -sp.oo, sp.oo) for x in V3])))
agrees(work, -q * n * E_vec.dot(u_vec), ":192", lhs=I_a)

# %% Fluid energy balances: setup
# Each balance is displayed in one dimension (fields of t and x, P = P_xx);
# the three-dimensional identity with tensor P is asserted silently.
t, x, y, z = sp.symbols("t x y z", real=True)
R3 = (x, y, z)
field = lambda name: sp.Function(name)(t, x, y, z)
rho_f, n_f, U_f, Q_f = field("rho"), field("n"), field("U"), field("Q")
u_f, q_f, E_f, B_f, R_f = (sp.Matrix([field(f"{name}_{c}") for c in "xyz"]) for name in "uqEBR")
P_f = sp.Matrix(3, 3, lambda i, j: field(f"P_{min(i, j) + 1}{max(i, j) + 1}"))
div3 = lambda vec: sum(sp.diff(vec[i], R3[i]) for i in range(3))
div_tensor = lambda T: sp.Matrix([sum(sp.diff(T[j, i], R3[j]) for j in range(3)) for i in range(3)])
P_grad_u = sum(P_f[i, j] * sp.diff(u_f[i], R3[j]) for i in range(3) for j in range(3))
K_f = rho_f * u_f.dot(u_f) / 2
momentum_3d = (sp.diff(rho_f * u_f, t) + div_tensor(rho_f * u_f * u_f.T + P_f)
               - (q * n_f * (E_f + u_f.cross(B_f)) + R_f))
continuity_3d = sp.diff(rho_f, t) + div3(rho_f * u_f)
bulk_3d = sp.diff(K_f, t) + div3(K_f * u_f) - (q * n_f * E_f.dot(u_f) - u_f.dot(div_tensor(P_f)) + u_f.dot(R_f))
total_3d = (sp.diff(K_f + U_f, t) + div3((K_f + U_f) * u_f + P_f * u_f + q_f)
            - q * n_f * E_f.dot(u_f) - Q_f)  # :91
internal_3d = sp.diff(U_f, t) + div3(U_f * u_f + q_f) - (-P_grad_u + Q_f - u_f.dot(R_f))  # :216
one_d = lambda name: sp.Function(name)(t, x)
rho1, u1, P1, n1, E1, R1, U1, q1, Q1 = (one_d(name) for name in ("rho", "u", "P", "n", "E", "R", "U", "q", "Q"))
K1 = rho1 * u1**2 / 2

# %% Bulk kinetic-energy equation
section("Bulk kinetic-energy equation", "mathematical-toolkit.typ:248")
note("Momentum balance and continuity in one dimension (the magnetic force has no x component)")
momentum = show(sp.Eq(sp.Derivative(rho1 * u1, t) + sp.Derivative(rho1 * u1**2 + P1, x), q * n1 * E1 + R1))
continuity = show(sp.Eq(sp.Derivative(rho1, t) + sp.Derivative(rho1 * u1, x), 0))
note("Multiply the momentum balance by", u1, "and subtract", u1**2 / 2, "times continuity:")
residuals = u1 * (momentum.lhs - momentum.rhs).doit() - u1**2 / 2 * continuity.lhs.doit()
bulk = sp.Derivative(K1, t) + sp.Derivative(K1 * u1, x)
agrees(sp.expand(bulk.doit() - residuals), q * n1 * E1 * u1 - u1 * P1.diff(x) + u1 * R1, ":258", lhs=bulk)
assert sp.expand(u_f.dot(momentum_3d) - u_f.dot(u_f) / 2 * continuity_3d - bulk_3d) == 0

# %% Pressure work
section("Pressure-work identity", "mathematical-toolkit.typ:270")
pressure_flux = sp.Derivative(P1 * u1, x)
agrees(pressure_flux.doit(), u1 * P1.diff(x) + P1 * u1.diff(x), ":274", lhs=pressure_flux)
assert sp.expand(div3(P_f * u_f) - (u_f.dot(div_tensor(P_f)) + P_grad_u)) == 0
p_f = field("p")
note("For isotropic pressure", sp.Eq(sp.Symbol("P"), p_f * sp.Symbol("I")), "the pressure work",
     "P:grad u in three dimensions is")
isotropic = sum((p_f * sp.eye(3))[i, j] * sp.diff(u_f[i], R3[j]) for i in range(3) for j in range(3))
agrees(isotropic, p_f * div3(u_f), ":281")

# %% Internal-energy equation
section("Internal-energy equation", "mathematical-toolkit.typ:229")
W1 = one_d("W")
note("Total energy in one dimension, with", sp.Eq(W1, sp.Symbol("K") + U1))
total = show(sp.Eq(sp.Derivative(W1, t) + sp.Derivative(W1 * u1 + P1 * u1 + q1, x), q * n1 * E1 * u1 + Q1))
total = total.subs(W1, K1 + U1)
note("Subtract the bulk kinetic-energy equation:")
bulk_residual = (bulk - (q * n1 * E1 * u1 - u1 * P1.diff(x) + u1 * R1)).doit()
internal = sp.Derivative(U1, t) + sp.Derivative(U1 * u1 + q1, x)
agrees(sp.expand(internal.doit() - ((total.lhs - total.rhs).doit() - bulk_residual)),
       -P1 * u1.diff(x) + Q1 - u1 * R1, ":236", lhs=internal)
assert sp.expand(total_3d - bulk_3d - internal_3d) == 0
pressure_work_flux = sp.Symbol("Pu")
check(pressure_work_flux, pressure_work_flux, unit=u.watt / u.meter**2,
      units={pressure_work_flux: u.pascal * u.meter / u.second})

# %% Orthogonal coordinates: setup
r, th, ph, zc = sp.symbols("r theta phi z", positive=True)
xc, yc = sp.symbols("x y", real=True)
SYSTEMS = {
    "Cartesian": ((xc, yc, zc), sp.Matrix([xc, yc, zc]), (1, 1, 1)),
    "cylindrical": ((r, ph, zc), sp.Matrix([r * sp.cos(ph), r * sp.sin(ph), zc]), (1, r, 1)),
    "spherical": ((r, th, ph), sp.Matrix([r * sp.sin(th) * sp.cos(ph), r * sp.sin(th) * sp.sin(ph),
                                          r * sp.cos(th)]), (1, r, r * sp.sin(th))),
}  # printed scale factors, mathematical-toolkit.typ:344-353


def basis(pos, qs):
    """Unit vectors e_i = (dr/dq_i)/h_i and scale factors h_i = |dr/dq_i|."""
    cols = [pos.diff(qq) for qq in qs]
    h = [sp.simplify(sp.sqrt(sp.trigsimp(sp.expand(c.dot(c))))) for c in cols]
    h = [hh.replace(sp.Abs, lambda arg: arg) for hh in h]  # sin(theta) >= 0 for 0 <= theta <= pi
    return [sp.simplify(c / hh) for c, hh in zip(cols, h)], h


def cyc(i):
    return (i + 1) % 3, (i + 2) % 3


def grad_g(psi, qs, h):
    return [sp.diff(psi, qs[i]) / h[i] for i in range(3)]  # :363


def div_g(A, qs, h):
    H = h[0] * h[1] * h[2]
    return sum(sp.diff(h[cyc(i)[0]] * h[cyc(i)[1]] * A[i], qs[i]) for i in range(3)) / H  # :364


def curl_g(A, qs, h):
    out = []
    for i in range(3):
        j, k = cyc(i)
        out.append((sp.diff(h[k] * A[k], qs[j]) - sp.diff(h[j] * A[j], qs[k])) / (h[j] * h[k]))  # :366
    return out


def lap_g(psi, qs, h):
    H = h[0] * h[1] * h[2]
    return sum(sp.diff(h[cyc(i)[0]] * h[cyc(i)[1]] / h[i] * sp.diff(psi, qs[i]), qs[i])
               for i in range(3)) / H  # :369


def is_zero(expr):
    return sp.simplify(sp.expand_trig(sp.simplify(expr))) == 0


# %% Scale factors
section("Scale factors", "mathematical-toolkit.typ:371")
h_1, h_2, h_3 = sp.symbols("h_1 h_2 h_3")
note("Each scale factor is the length of the derivative of the position vector along its coordinate")
for name, (qs, pos, h_printed) in SYSTEMS.items():
    _, h = basis(pos, qs)
    show(sp.Eq(sp.Tuple(h_1, h_2, h_3), sp.Tuple(*h)), name)
    for derived, printed, symbol in zip(h, h_printed, (h_1, h_2, h_3)):
        if printed != 1:
            agrees(derived, printed, ":382", lhs=symbol)
        else:
            assert sp.simplify(derived - printed) == 0
    cols = [pos.diff(qq) for qq in qs]  # coordinate directions are orthogonal
    for i, j in itertools.combinations(range(3), 2):
        assert sp.simplify(cols[i].dot(cols[j])) == 0

# %% Orthogonal-coordinate operators
section("Orthogonal-coordinate operators", "mathematical-toolkit.typ:390")
X, Y, Z = sp.symbols("X Y Z", real=True)
psi_test = X**2 * Y + Y * Z**3 + X * Z
A_test = sp.Matrix([X * Y, Y * Z**2, X**2 * Z])
note("Oracle: Cartesian operators of fixed test fields, projected on the local basis")
show(sp.Eq(sp.Symbol("psi"), psi_test))
show(sp.Eq(sp.Symbol("A"), A_test.as_immutable(), evaluate=False))
cartesian = [X, Y, Z]
grad_c = sp.Matrix([psi_test.diff(c) for c in cartesian])
div_c = sum(A_test[i].diff(cartesian[i]) for i in range(3))
curl_c = sp.Matrix([A_test[2].diff(Y) - A_test[1].diff(Z), A_test[0].diff(Z) - A_test[2].diff(X),
                    A_test[1].diff(X) - A_test[0].diff(Y)])  # Cartesian curl, :442
lap_c = sum(psi_test.diff(c, 2) for c in cartesian)  # :440
for name, (qs, pos, h) in SYSTEMS.items():
    e, _ = basis(pos, qs)
    to_cartesian = dict(zip(cartesian, pos))
    psi_q = psi_test.subs(to_cartesian)
    A_q = [A_test.subs(to_cartesian).dot(ei) for ei in e]  # physical components A_i
    gradient, rotation = grad_g(psi_q, qs, h), curl_g(A_q, qs, h)
    for i in range(3):
        assert is_zero(gradient[i] - grad_c.subs(to_cartesian).dot(e[i])), (name, "grad", i)
        assert is_zero(rotation[i] - curl_c.subs(to_cartesian).dot(e[i])), (name, "curl", i)
    assert is_zero(div_g(A_q, qs, h) - div_c.subs(to_cartesian)), (name, "div")
    assert is_zero(lap_g(psi_q, qs, h) - lap_c.subs(to_cartesian)), (name, "lap")
note("Gradient, divergence, curl and Laplacian match the oracle in Cartesian, cylindrical and",
     "spherical coordinates; the Laplacian of", sp.Symbol("psi"), "is")
show(sp.Eq(laplacian(sp.Symbol("psi")), lap_c))

# %% Cylindrical and spherical forms
section("Cylindrical and spherical forms", "mathematical-toolkit.typ:497")
psi = sp.Function("psi")
A_fn = [sp.Function(f"A_{i}") for i in (1, 2, 3)]
note("Cylindrical", sp.Tuple(r, ph, zc), ", printed at :453-456")
qs, _, h = SYSTEMS["cylindrical"]
s_c, A_c = psi(*qs), [a_i(*qs) for a_i in A_fn]
agrees(div_g(A_c, qs, h), sp.diff(r * A_c[0], r) / r + sp.diff(A_c[1], ph) / r + sp.diff(A_c[2], zc),
       ":505", lhs=div(sp.Symbol("A")))
agrees(lap_g(s_c, qs, h), sp.diff(r * sp.diff(s_c, r), r) / r + sp.diff(s_c, ph, 2) / r**2
       + sp.diff(s_c, zc, 2), ":507", lhs=laplacian(sp.Symbol("psi")))
agrees(grad_g(s_c, qs, h)[1], sp.diff(s_c, ph) / r, ":506", lhs=sp.Function("grad_phi")(sp.Symbol("psi")))
note("Spherical", sp.Tuple(r, th, ph), ", printed at :468-474")
qs, _, h = SYSTEMS["spherical"]
s_s, A_s = psi(*qs), [a_i(*qs) for a_i in A_fn]
agrees(div_g(A_s, qs, h), sp.diff(r**2 * A_s[0], r) / r**2 + sp.diff(sp.sin(th) * A_s[1], th)
       / (r * sp.sin(th)) + sp.diff(A_s[2], ph) / (r * sp.sin(th)), ":528", lhs=div(sp.Symbol("A")))
agrees(lap_g(s_s, qs, h), sp.diff(r**2 * sp.diff(s_s, r), r) / r**2
       + sp.diff(sp.sin(th) * sp.diff(s_s, th), th) / (r**2 * sp.sin(th))
       + sp.diff(s_s, ph, 2) / (r**2 * sp.sin(th) ** 2), ":532", lhs=laplacian(sp.Symbol("psi")))
gradient = grad_g(s_s, qs, h)
agrees(gradient[1], sp.diff(s_s, th) / r, ":526", lhs=sp.Function("grad_theta")(sp.Symbol("psi")))
agrees(gradient[2], sp.diff(s_s, ph) / (r * sp.sin(th)), ":526", lhs=sp.Function("grad_phi")(sp.Symbol("psi")))

# %% Identity checks
section("Identity checks", "mathematical-toolkit.typ:537")
note("Spherical coordinates, arbitrary", s_s, "and", sp.Tuple(*A_s))
A_sym, psi_sym = sp.Symbol("A"), sp.Symbol("psi")
agrees(sp.simplify(div_g(curl_g(A_s, qs, h), qs, h)), 0, ":544", lhs=div(curl(A_sym)))
curl_grad = [sp.simplify(component) for component in curl_g(grad_g(s_s, qs, h), qs, h)]
agrees(sp.Matrix(curl_grad).norm(), 0, ":546", lhs=curl(grad(psi_sym)))
C = sp.Symbol("C")
note("Inverse-square radial field", sp.Eq(sp.Symbol("A_r"), C / r**2))
agrees(div_g([C / r**2, 0, 0], qs, h), 0, ":548", lhs=div(A_sym))

# %% Cylindrical flux check
section("Cylindrical flux check", "mathematical-toolkit.typ:550")
L = sp.Symbol("L", positive=True)
A_r = sp.Function("A_r")(r)
Phi, volume = sp.Function("Phi")(r), sp.Function("V")(r)
note("Flux through a cylinder of radius", r, "and length", L, ", and the volume it encloses")
flux_r = show(sp.Eq(Phi, 2 * sp.pi * r * L * A_r)).rhs  # :506
shell = show(sp.Eq(sp.Derivative(volume, r), 2 * sp.pi * r * L)).rhs  # :514
flux_per_volume = sp.simplify(sp.diff(flux_r, r) / shell)
qs, _, h = SYSTEMS["cylindrical"]
agrees(flux_per_volume, div_g([A_r, 0, 0], qs, h), ":577",
       lhs=sp.Derivative(Phi, r) / sp.Derivative(volume, r))
agrees(flux_per_volume, sp.diff(r * A_r, r) / r, ":560", lhs=div(sp.Symbol("A")))

# %% Worked example: radial flux C/r
section("Worked example: radial flux C/r", "mathematical-toolkit.typ:578")
C_flux = sp.Symbol("C", positive=True)
Gamma = sp.Symbol("Gamma_r")
flux_density = show(sp.Eq(Gamma, C_flux / r)).rhs
FLUX_UNIT = 1 / (u.meter**2 * u.second)
example = {C_flux: 2e12 / (u.meter * u.second)}
note("Input", sp.Eq(C_flux, example[C_flux], evaluate=False))
for radius, printed in [(0.1 * u.meter, 2e13), (0.2 * u.meter, 1e13)]:
    value = evaluate(sp.Function("Gamma_r")(radius), flux_density, {**example, r: radius}, FLUX_UNIT)
    close_to(value, printed, rtol=1e-12, source=":591")
agrees(sp.diff(r * flux_density, r) / r, 0, ":592", lhs=div(sp.Symbol("Gamma")))

# %%
if __name__ == "__main__":
    report(__file__, "Appendix · Mathematical toolkit")
