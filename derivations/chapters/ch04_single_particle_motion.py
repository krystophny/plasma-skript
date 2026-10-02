# Chapter 4 · Single-particle motion (src/chapters/04-single-particle-motion.typ)
#
# Gyration, magnetic moment and its adiabatic invariance, the drifts (E x B,
# grad-B, curvature, polarization), magnetic mirrors and cyclotron resonance.
# Vector results are shown in a frame with B along z; general orientations are
# checked silently.

# %% Setup
import sympy as sp
from sympy.physics import units as u

from kinetics import rounding_rtol
from notebook import PROTON_MASS, agrees, close_to, evaluate, note, report, section, show
from si import check, eps0, k_B

m, B, t, v_perp, T_s, mu = sp.symbols("m B t v_perp T_s mu", positive=True)
q, Omega, delta = sp.symbols("q Omega delta", real=True)
e, m_e, m_p = sp.symbols("e m_e m_p", positive=True)  # filled from CODATA by evaluate()
SI_UNITS = {m: u.kilogram, B: u.tesla, t: u.second, v_perp: u.meter / u.second,
            T_s: u.kelvin, q: u.coulomb, mu: u.joule / u.tesla}
VELOCITY = u.meter / u.second
e_z = sp.Matrix([0, 0, 1])


def vec(name, **assumptions):
    sep = "," if "_" in name else "_"
    return sp.Matrix([sp.Symbol(f"{name}{sep}{axis}", **assumptions) for axis in "xyz"])


def agrees_vector(derived, printed, source, name):
    """Compare two 3-vectors; nonzero components are displayed as name_x, name_y, ..."""
    for axis, d, p in zip("xyz", derived, printed):
        if sp.simplify(p) == 0:
            assert sp.simplify(d) == 0, (name, axis, d)
        else:
            agrees(d, p, source, lhs=sp.Symbol(f"{name},{axis}"))


# %% Magnetic force does no work
section("Magnetic force does no work", "04-single-particle-motion.typ:32")
v, E, B_vec = vec("v", real=True), vec("E", real=True), vec("B", real=True)
velocity = sp.Matrix([sp.Function(f"v_{axis}")(t) for axis in "xyz"])
note("Lorentz force")
show(sp.Eq(m * velocity.diff(t), q * (E + v.cross(B_vec)).subs(dict(zip(v, velocity))),
           evaluate=False))
note("The magnetic part does no work:")
magnetic_power = v.dot(v.cross(B_vec))
show(sp.Eq(magnetic_power, sp.expand(magnetic_power), evaluate=False))
assert sp.expand(magnetic_power) == 0
note("Kinetic energy", sp.Eq(sp.Function("K")(t), m * v.dot(v) / 2), "changes only through the electric field")
agrees(sp.expand(v.dot(q * (E + v.cross(B_vec)))), q * E.dot(v), ":49",
       lhs=sp.Derivative(sp.Function("K")(t), t))

# %% Cyclotron motion
section("Cyclotron motion", "04-single-particle-motion.typ:52")
v_x, v_y = sp.Function("v_x")(t), sp.Function("v_y")(t)
force = q * sp.Matrix([v_x, v_y, 0]).cross(B * e_z)
gyrofrequency = q * B / m
note("No electric field, uniform field", B, "along z, and", sp.Eq(Omega, gyrofrequency))
check(gyrofrequency, gyrofrequency, unit=1 / u.second, units=SI_UNITS)
agrees(force[0] / m, gyrofrequency * v_y, ":59", lhs=v_x.diff(t))
agrees(force[1] / m, -gyrofrequency * v_x, ":59", lhs=v_y.diff(t))
system = [sp.Eq(v_x.diff(t), Omega * v_y), sp.Eq(v_y.diff(t), -Omega * v_x)]
note("Solve with", sp.Eq(v_x.subs(t, 0), v_perp * sp.cos(delta)), "and",
     sp.Eq(v_y.subs(t, 0), -v_perp * sp.sin(delta)))
orbit = sp.dsolve(system, ics={v_x.subs(t, 0): v_perp * sp.cos(delta),
                               v_y.subs(t, 0): -v_perp * sp.sin(delta)})
vx_orbit = agrees(sp.expand_trig(orbit[0].rhs), v_perp * sp.cos(Omega * t + delta), ":84", lhs=v_x)
vy_orbit = agrees(sp.expand_trig(orbit[1].rhs), -v_perp * sp.sin(Omega * t + delta), ":84", lhs=v_y)
assert sp.simplify(vx_orbit.diff(t) - Omega * vy_orbit) == 0
assert sp.simplify(vy_orbit.diff(t) + Omega * vx_orbit) == 0
note("The magnetic force only turns the velocity:")
speed_sq = show(sp.Eq(v_x**2 + v_y**2, sp.simplify(vx_orbit**2 + vy_orbit**2)))
assert speed_sq.rhs == v_perp**2

# %% Gyroradius
section("Gyroradius", "04-single-particle-motion.typ:66")
rho = sp.Symbol("rho", positive=True)
note("Centripetal balance")
centripetal = show(sp.Eq(m * v_perp**2 / rho, sp.Abs(q) * v_perp * B))
gyroradius = agrees(sp.solve(centripetal, rho)[0], m * v_perp / (sp.Abs(q) * B), ":77", lhs=rho)
check(gyroradius, gyroradius, unit=u.meter, units=SI_UNITS)
note("Integrate the velocity along the orbit")
s = sp.Symbol("s")
x_t = show(sp.Eq(sp.Function("x")(t), sp.Integral(vx_orbit.subs(t, s), (s, 0, t)))).rhs
y_t = show(sp.Eq(sp.Function("y")(t), sp.Integral(vy_orbit.subs(t, s), (s, 0, t)))).rhs
x_t, y_t = x_t.doit(conds="none"), y_t.doit(conds="none")
centre = (v_perp / Omega * sp.sin(delta), v_perp / Omega * sp.cos(delta))
note("Radius about the centre", sp.Tuple(-centre[0], -centre[1]))
radius_sq = show(sp.Eq(rho**2, sp.simplify((x_t + centre[0]) ** 2 + (y_t + centre[1]) ** 2))).rhs
assert sp.simplify(radius_sq - v_perp**2 / Omega**2) == 0
agrees(sp.sqrt(radius_sq.subs(Omega, gyrofrequency)), gyroradius, ":77", lhs=rho)

# %% Thermal gyroradius
section("Thermal gyroradius", "04-single-particle-motion.typ:93")
rho_s, omega_c, v_th = sp.symbols("rho_s omega_c v_th", positive=True)
definitions = {v_th: sp.sqrt(2 * k_B * T_s / m), omega_c: sp.Abs(q) * B / m}
for symbol, expr in definitions.items():
    show(sp.Eq(symbol, expr))
thermal = show(sp.Eq(rho_s, v_th / omega_c))
check(definitions[omega_c], definitions[omega_c], unit=1 / u.second, units=SI_UNITS)
check(thermal.rhs.subs(definitions), thermal.rhs.subs(definitions), unit=u.meter, units=SI_UNITS)

# %% Worked examples: plasma scales at 1 T and thermonuclear scales at 5 T
section("Worked example: scales at a million kelvin and 1 T", "04-single-particle-motion.typ:115")
n, T_e, T_i, m_i = sp.symbols("n T_e T_i m_i", positive=True)
lambda_D, omega_pe, omega_ce, omega_ci, rho_e, rho_i = sp.symbols(
    "lambda_D omega_pe omega_ce omega_ci rho_e rho_i", positive=True)
scales = {lambda_D: sp.sqrt(eps0 * k_B * T_e / (n * e**2)),
          omega_pe: sp.sqrt(n * e**2 / (eps0 * m_e)),
          omega_ce: e * B / m_e, omega_ci: e * B / m_i,
          rho_e: sp.sqrt(2 * k_B * T_e / m_e) / (e * B / m_e),
          rho_i: sp.sqrt(2 * k_B * T_i / m_i) / (e * B / m_i)}
SCALE_UNITS = {lambda_D: u.meter, omega_pe: 1 / u.second, omega_ce: 1 / u.second,
               omega_ci: 1 / u.second, rho_e: u.meter, rho_i: u.meter}
for symbol in (lambda_D, rho_e, rho_i):
    show(sp.Eq(symbol, scales[symbol]))
note("Hydrogen ions", sp.Eq(m_i, m_p), "and", sp.Eq(n, 1e20 / u.meter**3, evaluate=False),
     ",", sp.Eq(T_e, 1e6 * u.kelvin, evaluate=False), ",", sp.Eq(B, 1 * u.tesla, evaluate=False))
plasma_1T = {n: 1e20 / u.meter**3, T_e: 1e6 * u.kelvin, T_i: 1e6 * u.kelvin,
             B: 1 * u.tesla, m_i: PROTON_MASS}
for symbol, printed, line in [(lambda_D, "6.9e-6", ":135"), (omega_pe, "5.6e11", ":135"),
                              (rho_e, "3.1e-5", ":137"), (rho_i, "1.3e-3", ":137")]:
    value = evaluate(symbol, scales[symbol], plasma_1T, SCALE_UNITS[symbol])
    close_to(value, float(printed), rtol=rounding_rtol(printed), source=line)

section("Worked example: thermonuclear scales", "04-single-particle-motion.typ:134")
note("Input", sp.Eq(T_e, 1e8 * u.kelvin, evaluate=False), ",", sp.Eq(B, 5 * u.tesla, evaluate=False),
     ", same density")
thermonuclear = {**plasma_1T, T_e: 1e8 * u.kelvin, T_i: 1e8 * u.kelvin, B: 5 * u.tesla}
thermal_energy = evaluate(k_B * T_e, k_B * T_e, thermonuclear, u.electronvolt)
close_to(thermal_energy, 8.62e3, rtol=rounding_rtol("8.62e3"), source=":156")
for symbol, printed in [(lambda_D, "6.9e-5"), (omega_pe, "5.6e11"), (omega_ce, "8.8e11"),
                        (omega_ci, "4.8e8"), (rho_e, "6.3e-5"), (rho_i, "2.7e-3")]:
    value = evaluate(symbol, scales[symbol], thermonuclear, SCALE_UNITS[symbol])
    close_to(value, float(printed), rtol=rounding_rtol(printed), source=":156-162")

# %% Parallel acceleration
section("Parallel acceleration", "04-single-particle-motion.typ:220")
note("Project the Lorentz force on the field direction z")
F_parallel = (q * (E + v.cross(B * e_z))).dot(e_z)
agrees(F_parallel, q * E.dot(e_z), ":229", lhs=sp.Symbol("F_par"))
check(F_parallel, q * E.dot(e_z), unit=u.newton, units={**SI_UNITS, E[2]: u.volt / u.meter})

# %% Homogeneous-force drift
section("Homogeneous-force drift", "04-single-particle-motion.typ:242")
F, v_D = vec("F", real=True), vec("v_D")
F_perp = sp.Matrix([F[0], F[1], 0])
note("Force balance; field", B, "along z and a perpendicular force,", sp.Eq(F[2], 0))
balance = show(sp.Eq(F_perp + q * v_D.cross(B * e_z), sp.zeros(3, 1), evaluate=False))
drift = v_D.subs(sp.solve(list(balance.lhs) + [v_D[2]], list(v_D), dict=True)[0])
agrees_vector(drift, F_perp.cross(B * e_z) / (q * B**2), ":260", "v_D")
# Any orientation of B: solvable only for F.B = 0 (eliminate F_z, generic B_z != 0).
B_sq = B_vec.dot(B_vec)
F_z = sp.solve(F.dot(B_vec), F[2])[0]
general = sp.solve([c.subs(F[2], F_z) for c in F + q * v_D.cross(B_vec)] + [v_D.dot(B_vec)],
                   list(v_D), dict=True)[0]
assert sp.simplify(v_D.subs(general) - (F.cross(B_vec) / (q * B_sq)).subs(F[2], F_z)) == sp.zeros(3, 1)
# (v_D x B) x B = -v_D B^2 for v_D perpendicular to B, used in the text at :286.
w = vec("w")
w_perp = w - w.dot(B_vec) / B_sq * B_vec
assert sp.simplify(w_perp.cross(B_vec).cross(B_vec) + w_perp * B_sq) == sp.zeros(3, 1)
F_0, B_0 = sp.symbols("F_0 B_0", positive=True)
check(F_0 / (q * B_0), F_0 / (q * B_0), unit=VELOCITY,
      units={**SI_UNITS, F_0: u.newton, B_0: u.tesla})

# %% E x B drift
section("E x B drift", "04-single-particle-motion.typ:260")
E_perp = sp.Matrix([E[0], E[1], 0])
note("Electric force", sp.Eq(sp.Symbol("F"), q * sp.Symbol("E")), "in the force drift")
exb = F_perp.cross(B * e_z) / (q * B**2)
exb = exb.subs({F[0]: q * E[0], F[1]: q * E[1]})
agrees_vector(exb, E_perp.cross(B * e_z) / B**2, ":269", "v_E")
assert sp.simplify((q * E.cross(B_vec) / (q * B_sq)) - E.cross(B_vec) / B_sq) == sp.zeros(3, 1)
note("For every charge", q, "the Lorentz force vanishes in the drifting frame")
v_E = E_perp.cross(B * e_z) / B**2
assert sp.simplify(q * (E_perp + v_E.cross(B * e_z))) == sp.zeros(3, 1)
E_0 = sp.Symbol("E_0", positive=True)
check(E_0 / B, E_0 / B, unit=VELOCITY, units={**SI_UNITS, E_0: u.volt / u.meter})

# %% Guiding-centre split
section("Guiding-centre split", "04-single-particle-motion.typ:368")
R_x, rho_x = sp.Function("R_x")(t), sp.Function("rho_x")(t)
note("Position = guiding centre + gyration, per component")
split = show(sp.Eq(sp.Derivative(R_x + rho_x, t), (R_x + rho_x).diff(t)))
assert sp.simplify(split.lhs.doit() - R_x.diff(t) - rho_x.diff(t)) == 0  # :388

# %% Magnetic moment of a gyro-orbit
section("Magnetic moment of a gyro-orbit", "04-single-particle-motion.typ:392")
current, area = sp.symbols("I A")
note("Current of one charge per gyration period, enclosing the area", sp.Eq(area, sp.pi * rho**2))
loop_current = show(sp.Eq(current, sp.Abs(q) / (2 * sp.pi / omega_c))).rhs  # :425
moment = agrees(loop_current * sp.pi * rho**2, sp.Abs(q) * omega_c * rho**2 / 2, ":429", lhs=mu)
note("Insert", sp.Eq(omega_c, definitions[omega_c]), "and", sp.Eq(rho, v_perp / omega_c))
mu_expr = agrees(sp.simplify(moment.subs(rho, v_perp / omega_c).subs(omega_c, definitions[omega_c])),
                 m * v_perp**2 / (2 * B), ":402", lhs=mu)
check(mu_expr, mu_expr, unit=u.joule / u.tesla, units=SI_UNITS)
check(mu_expr, mu_expr, unit=u.ampere * u.meter**2, units=SI_UNITS)

# %% Adiabatic balance for mu
section("Adiabatic balance for mu", "04-single-particle-motion.typ:429")
s_t, v_par_t = sp.Function("s")(t), sp.Function("v_par")(t)
B_s, mu_t = sp.Function("B")(s_t), sp.Function("mu")(t)
note("Averaged mirror force along the field line, and motion along it")
mirror = show(sp.Eq(v_par_t.diff(t), -mu_t * sp.Derivative(B_s, s_t) / m))  # :439
streaming = show(sp.Eq(s_t.diff(t), v_par_t))
along_orbit = {mirror.lhs: mirror.rhs, streaming.lhs: streaming.rhs}
K_par = sp.Function("K_par")(t)
note("Parallel energy and magnetic energy change at rates")
dK_par = show(sp.Eq(sp.Derivative(K_par, t), sp.diff(m * v_par_t**2 / 2, t).subs(along_orbit).doit())).rhs
dmuB = show(sp.Eq(sp.Derivative(mu_t * B_s, t), sp.diff(mu_t * B_s, t).subs(along_orbit).doit())).rhs
agrees(sp.simplify(dK_par + dmuB), B_s * mu_t.diff(t), ":458",
       lhs=sp.Derivative(K_par + mu_t * B_s, t))
# Static B conserves K = K_par + mu B, so B dmu/dt = 0: mu is constant.

# %% Worked example: adiabatic compression
section("Worked example: adiabatic compression", "04-single-particle-motion.typ:461")
B_0, B_1, v_0, v_1 = sp.symbols("B_0 B_1 v_0 v_1", positive=True)
note("Proton", sp.Eq(m, m_p), "with", mu, "conserved while the field rises from", B_0, "to", B_1)
conserved = show(sp.Eq(m * v_0**2 / (2 * B_0), m * v_1**2 / (2 * B_1)))
v_1_expr = show(sp.Eq(v_1, sp.solve(conserved, v_1)[0])).rhs
compression = {B_0: 0.01 * u.tesla, B_1: 0.04 * u.tesla, v_0: 1e5 * u.meter / u.second}
note("Input", sp.Eq(B_0, compression[B_0], evaluate=False), ",",
     sp.Eq(B_1, compression[B_1], evaluate=False), ",", sp.Eq(v_0, compression[v_0], evaluate=False))
close_to(evaluate(v_1, v_1_expr, compression, VELOCITY), 2.00e5, rtol=rounding_rtol("2.00e5"),
         source=":481")
rho_0, rho_1 = sp.symbols("rho_0 rho_1", positive=True)
radius_0 = evaluate(rho_0, (m_p * v_0 / (e * B_0)), compression, u.meter)
close_to(radius_0, 0.104, rtol=rounding_rtol("0.104"), source=":482")
radius_1 = evaluate(rho_1, m_p * v_1_expr / (e * B_1), compression, u.meter)
close_to(radius_1, 0.0522, rtol=rounding_rtol("0.0522"), source=":482")

# %% Mirror force from the gyro-average
section("Mirror force from the gyro-average", "04-single-particle-motion.typ:536")
kappa, X, theta = sp.symbols("kappa X theta", real=True)
x_g = sp.Symbol("x")
note("Weak gradient", sp.Eq(sp.Symbol("B_z"), B_0 * (1 + kappa * x_g)), "; unperturbed orbit with",
     sp.Eq(theta, Omega * t), "and", sp.Eq(Omega, q * B_0 / m))
orbit_v = sp.Matrix([v_perp * sp.cos(theta), -v_perp * sp.sin(theta), 0])
orbit_x = show(sp.Eq(x_g, X + v_perp / (q * B_0 / m) * sp.sin(theta))).rhs
gradient_force = q * orbit_v.cross(sp.Matrix([0, 0, B_0 * kappa * orbit_x]))
note("Lorentz force of the gradient part, averaged over one gyration")
F_bar = sp.Symbol("Fbar_x")
average = show(sp.Eq(F_bar, sp.Integral(gradient_force[0], (theta, 0, 2 * sp.pi)) / (2 * sp.pi)))
averaged = sp.Matrix([sp.integrate(c, (theta, 0, 2 * sp.pi)) / (2 * sp.pi) for c in gradient_force])
mu_0 = m * v_perp**2 / (2 * B_0)
note("With", sp.Eq(mu, mu_0), "and", sp.Eq(sp.Derivative(sp.Symbol("B_z"), x_g), B_0 * kappa))
agrees(sp.simplify(average.rhs.doit()).subs(m, 2 * B_0 * mu / v_perp**2), -mu * B_0 * kappa, ":553", lhs=F_bar)
assert sp.simplify(averaged - (-mu_0 * sp.Matrix([B_0 * kappa, 0, 0]))) == sp.zeros(3, 1)

# %% Grad-B drift
section("Grad-B drift", "04-single-particle-motion.typ:546")
G = vec("G", real=True)  # G = grad B
note("Mirror force", sp.Eq(sp.Symbol("F_mu"), -mu * sp.Symbol("G")), "with", sp.Symbol("G"),
     "the gradient of the field strength, in the force drift")
grad_B_drift = (-mu * G).cross(B * e_z) / (q * B**2)
agrees_vector(grad_B_drift, mu * (B * e_z).cross(G) / (q * B**2), ":563", "v_gradB")
g = sp.Symbol("g", positive=True)
check(mu * B * g / (q * B**2), mu * g / (q * B), unit=VELOCITY, units={**SI_UNITS, g: u.tesla / u.meter})

# %% Curvature force and drift
section("Curvature force and drift", "04-single-particle-motion.typ:557")
R_c, v_par = sp.symbols("R_c v_par", positive=True)
note("Guiding centre moving at", v_par, "along a field line of radius", R_c, "feels the centrifugal force",
     -m * sp.Symbol("a"), "; the curvature vector points from it to the centre of curvature")
path = sp.Matrix([R_c * sp.cos(v_par * t / R_c), R_c * sp.sin(v_par * t / R_c), 0])
acceleration = sp.simplify(path.diff(t, 2))
agrees_vector(-m * acceleration, -m * v_par**2 * (-path) / R_c**2, ":574", "F_curv")
check(m * v_par**2 / R_c, m * v_par**2 / R_c, unit=u.newton,
      units={**SI_UNITS, R_c: u.meter, v_par: VELOCITY})
R_vec = sp.Matrix([sp.Symbol("R_x", real=True), sp.Symbol("R_y", real=True), 0])  # perpendicular to B
note("In the force drift, with the curvature vector", sp.Symbol("kappa"), "=", R_vec.as_immutable() / R_c**2)
curvature_drift = (-m * v_par**2 * R_vec / R_c**2).cross(B * e_z) / (q * B**2)
agrees_vector(curvature_drift, m * v_par**2 / (q * B) * e_z.cross(R_vec / R_c**2), ":585", "v_curv")
check(m * v_par**2 / (q * B * R_c), m * v_par**2 / (q * B * R_c), unit=VELOCITY,
      units={**SI_UNITS, R_c: u.meter, v_par: VELOCITY})

# %% Mirror energy and loss cone
section("Mirror energy and loss cone", "04-single-particle-motion.typ:614")
mu_const = {mirror.lhs: mirror.rhs.subs(mu_t, mu), streaming.lhs: streaming.rhs}
energy = show(sp.Eq(sp.Function("K")(t), m * v_par_t**2 / 2 + mu * B_s)).rhs
agrees(sp.simplify(energy.diff(t).subs(mu_const).doit()), 0, ":642",
       lhs=sp.Derivative(sp.Function("K")(t), t))
v_0, alpha_0, B_m, B_max = sp.symbols("v_0 alpha_0 B_m B_max", positive=True)
note("Pitch angle", alpha_0, "at", B_0, "; at the mirror point", sp.Eq(v_par, 0, evaluate=False))
reflection = show(sp.Eq(m * (v_0 * sp.sin(alpha_0)) ** 2 / (2 * B_0) * B_m, m * v_0**2 / 2))
B_mirror = sp.solve(reflection, B_m)[0]
agrees(B_mirror / B_0, 1 / sp.sin(alpha_0) ** 2, ":686", lhs=B_m / B_0)
note("Particles with", sp.Gt(B_mirror, B_max), "are lost; the loss-cone angle is")
alpha_c = sp.Symbol("alpha_c", positive=True)
sine = sp.Symbol("S", positive=True)  # sin(alpha_c), 0 < alpha_c < pi/2
loss_cone = show(sp.Eq(alpha_c, sp.asin(sp.solve(sp.Eq(B_mirror.subs(sp.sin(alpha_0), sine), B_max),
                                                 sine)[0]))).rhs
mirror_ratio = {B_0: 0.01 * u.tesla, B_max: 0.05 * u.tesla}
note("Input", sp.Eq(B_0, mirror_ratio[B_0], evaluate=False), ",", sp.Eq(B_max, mirror_ratio[B_max], evaluate=False))
angle = evaluate(alpha_c, loss_cone * u.radian, mirror_ratio, u.degree)
close_to(angle, 26.6, rtol=rounding_rtol("26.6"), source=":703")

# %% Polarization drift
section("Polarization drift", "04-single-particle-motion.typ:770")
ramp = sp.Symbol("Edot", real=True)
c_0, c_1 = vec("c0"), vec("c1")
note("Linearly ramping field", sp.Eq(E[0], ramp * t), "perpendicular to", B, "along z;",
     "orbit-centre velocity linear in", t)
E_ramp = sp.Matrix([ramp * t, 0, 0])
residual = m * (c_0 + c_1 * t).diff(t) - q * (E_ramp + (c_0 + c_1 * t).cross(B * e_z))
equations = [coefficient for c in residual for coefficient in sp.Poly(c, t).all_coeffs()]
coefficients = sp.solve(equations + [c_0[2], c_1[2]], list(c_0) + list(c_1), dict=True)[0]
v_ramp = sp.simplify((c_0 + c_1 * t).subs(coefficients))
v_E_ramp = E_ramp.cross(B * e_z) / B**2  # :793
v_pol = m / (q * B**2) * E_ramp.diff(t)  # :803
agrees_vector(v_ramp, v_E_ramp + v_pol, ":789", "v_perp")
note("The y part is the E x B drift; the x part is the polarization drift")
agrees_vector(v_ramp - v_E_ramp, v_pol, ":803", "v_pol")
# Text steps :837-848: B x (A x B) = B^2 A, and m/(q B^2) B x dv_E/dt = v_pol.
A_perp = sp.Matrix([sp.Symbol("A_x"), sp.Symbol("A_y"), 0])
assert sp.simplify((B * e_z).cross(A_perp.cross(B * e_z)) - B**2 * A_perp) == sp.zeros(3, 1)
assert sp.simplify(m / (q * B**2) * (B * e_z).cross(v_E_ramp.diff(t)) - v_pol) == sp.zeros(3, 1)
E_rate = sp.Symbol("Edot_0", positive=True)
check(m * E_rate / (q * B**2), m * E_rate / (q * B**2), unit=VELOCITY,
      units={**SI_UNITS, E_rate: u.volt / u.meter / u.second})

# %% Polarization current
section("Polarization current", "04-single-particle-motion.typ:839")
n_1, n_2, m_1, m_2, q_1, q_2 = sp.symbols("n_1 n_2 m_1 m_2 q_1 q_2", positive=True)
note("Sum of", n * q * sp.Symbol("v_pol"), "over ions (charge", q_1, ") and electrons (charge", -q_2, ")")
j_pol = sum(density * charge * mass / (charge * B**2) * E_rate
            for density, charge, mass in [(n_1, q_1, m_1), (n_2, -q_2, m_2)])
j_pol = agrees(j_pol, (n_1 * m_1 + n_2 * m_2) / B**2 * E_rate, ":858", lhs=sp.Symbol("j_pol"))
check(j_pol, j_pol, unit=u.ampere / u.meter**2,
      units={B: u.tesla, n_1: u.meter**-3, n_2: u.meter**-3, m_1: u.kilogram, m_2: u.kilogram,
             E_rate: u.volt / u.meter / u.second})

# %% Worked example: electron polarization drift
section("Worked example: electron polarization drift", "04-single-particle-motion.typ:849")
omega_d, E_0 = sp.symbols("omega_d E_0", positive=True)
note("Field oscillating at", omega_d, "with amplitude", E_0, ", so the rate amplitude is", omega_d * E_0)
electron = {B: 0.01 * u.tesla, E_0: 3e4 * u.volt / u.meter, omega_d: 1e5 / u.second}
v_pol_electron = evaluate(sp.Symbol("v_pol"), m_e * omega_d * E_0 / (e * B**2), electron, VELOCITY)
close_to(v_pol_electron, 171, rtol=rounding_rtol("171"), source=":879")
note("Ordering against the electron gyrofrequency")
Omega_e = evaluate(sp.Symbol("Omega_e"), e * B / m_e, electron, 1 / u.second)
ordering = show(sp.Eq(omega_d / sp.Symbol("Omega_e"), sp.Float(1e5 / Omega_e, 3))).rhs
close_to(float(ordering), 5.69e-5, rtol=rounding_rtol("5.69e-5"), source=":880")

# %% Circular cyclotron response
section("Circular cyclotron response", "04-single-particle-motion.typ:952")
E_x, E_y = sp.Function("E_x")(t), sp.Function("E_y")(t)
v_cw, v_ccw, E_cw, E_ccw = sp.symbols("v_cw v_ccw E_cw E_ccw")
note("Lorentz force with", B, "along z and", sp.Eq(Omega, gyrofrequency))
lorentz_x = show(sp.Eq(v_x.diff(t), q / m * E_x + Omega * v_y)).rhs
lorentz_y = show(sp.Eq(v_y.diff(t), q / m * E_y - Omega * v_x)).rhs
assert sp.expand(force[0] / m - gyrofrequency * v_y) == 0  # same equations as :59
note("Rotating components", sp.Eq(v_cw, v_x + sp.I * v_y), "and", sp.Eq(v_ccw, v_x - sp.I * v_y))
rotating = {v_x: (v_cw + v_ccw) / 2, v_y: (v_cw - v_ccw) / (2 * sp.I),
            E_x: (E_cw + E_ccw) / 2, E_y: (E_cw - E_ccw) / (2 * sp.I)}
agrees(sp.expand((lorentz_x + sp.I * lorentz_y).subs(rotating)), q / m * E_cw - sp.I * Omega * v_cw,
       ":996", lhs=sp.Derivative(sp.Function("v_cw")(t), t))
agrees(sp.expand((lorentz_x - sp.I * lorentz_y).subs(rotating)), q / m * E_ccw + sp.I * Omega * v_ccw,
       ":1019", lhs=sp.Derivative(sp.Function("v_ccw")(t), t))
omega, E_t, v_t = sp.symbols("omega E_t v_t")
note("Harmonic drive", sp.exp(-sp.I * omega * t), ": the time derivative becomes", -sp.I * omega)
co_rotating = show(sp.Eq(-sp.I * omega * v_t, q / m * E_t - sp.I * Omega * v_t))
agrees(sp.solve(co_rotating, v_t)[0], q * E_t / (sp.I * m * (Omega - omega)), ":1011", lhs=v_t)
counter_rotating = show(sp.Eq(-sp.I * omega * v_t, q / m * E_t + sp.I * Omega * v_t))
agrees(sp.solve(counter_rotating, v_t)[0], sp.I * q * E_t / (m * (omega + Omega)), ":1019", lhs=v_t)
note("Free gyration for", sp.Gt(q * B, 0), "rotates clockwise:")
free = v_perp * sp.cos(Omega * t) - sp.I * v_perp * sp.sin(Omega * t)
assert sp.simplify((free - v_perp * sp.exp(-sp.I * Omega * t)).rewrite(sp.exp)) == 0
show(sp.Eq(v_cw, v_perp * sp.exp(-sp.I * Omega * t)))

# %% Worked example: cyclotron resonance
section("Worked example: cyclotron resonance", "04-single-particle-motion.typ:1011")
note("Resonance at", sp.Eq(omega, Omega), "for", sp.Eq(B, 0.01 * u.tesla, evaluate=False))
weak_field = {B: 0.01 * u.tesla}
omega_res_e = evaluate(sp.Symbol("omega_res,e"), e * B / m_e, weak_field, 1 / u.second)
close_to(omega_res_e, 1.76e9, rtol=rounding_rtol("1.76e9"), source=":1042")
omega_res_i = evaluate(sp.Symbol("omega_res,i"), e * B / m_p, weak_field, 1 / u.second)
close_to(omega_res_i, 9.58e5, rtol=rounding_rtol("9.58e5"), source=":1042")

# %%
if __name__ == "__main__":
    report(__file__, "Chapter 4 · Single-particle motion")
