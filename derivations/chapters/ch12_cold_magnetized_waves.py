# Chapter 12 · Cold magnetized waves (src/chapters/12-cold-magnetized-waves.typ)
#
# Cold dielectric tensor, parallel (circular) and perpendicular (O, X) modes,
# the oblique Appleton-Hartree roots and the normalized landmarks.
# `python ch12_cold_magnetized_waves.py` prints every step; `# %%` cells run one by one.

# %% Setup
import numpy as np
import sympy as sp
from sympy.physics import units as u

import si
from notebook import agrees, close_to, evaluate, note, report, section, show
from si import BLUE, GRAY, ORANGE, figure, label, save
from waves import matmul, number

e, m_e, eps0, mu0, c = sp.symbols("e m_e epsilon_0 mu_0 c", positive=True)
w, k, B0, n0 = sp.symbols("omega k B_0 n_0", positive=True)
wpe, wce = sp.symbols("omega_pe omega_ce", positive=True)
N, theta = sp.symbols("N theta", positive=True)
Ex, Ey, Ez = sp.symbols("E_x E_y E_z")
E = sp.Matrix([Ex, Ey, Ez])
S, D, P = sp.symbols(r"\epsilon_\perp \epsilon_\times \epsilon_\parallel")  # tensor entries
s = sp.Symbol("s")  # circular label s = +1 or -1
W, Y, K = sp.symbols("W Y K", positive=True)  # omega/omega_pe, omega_ce/omega_pe, kc/omega_pe
I = sp.I
M_sym = sp.MatrixSymbol("M", 3, 3)  # name of the displayed wave matrix

UNITS = {w: u.second**-1, k: u.meter**-1, B0: u.tesla, n0: u.meter**-3,
         wpe: u.second**-1, wce: u.second**-1}
NORM = {w: W * wpe, wce: Y * wpe}  # normalize by omega_pe
TENSOR = sp.Matrix([[S, -I * D, 0], [I * D, S, 0], [0, 0, P]])  # cold tensor, :78


def momentum(q, m, Om):
    """Plane-wave cold momentum equations -i w u = (q/m) E + Om u x e_z."""
    ux, uy, uz = sp.symbols("u_x u_y u_z")
    lhs = -I * w * sp.Matrix([ux, uy, uz])
    rhs = q / m * E + Om * sp.Matrix([ux, uy, uz]).cross(sp.Matrix([0, 0, 1]))
    return [sp.Eq(a, b) for a, b in zip(lhs, rhs)], (ux, uy, uz)


def susceptibility(q, m, n, Om):
    """chi = sigma/(-i w eps0) of one cold species with gyrofrequency Om = q B0/m."""
    eqs, vel = momentum(q, m, Om)
    sol = sp.solve(eqs, vel, dict=True)[0]
    j = [q * n * sol[v] for v in vel]
    sigma = sp.Matrix(3, 3, lambda a, b: sp.diff(j[a], E[b]))
    return sigma / (-I * w * eps0)


def eps_electron():
    """Electron tensor with Omega_e = -omega_ce and omega_pe^2 inserted."""
    chi = susceptibility(-e, m_e, n0, -wce).subs(n0, wpe**2 * eps0 * m_e / e**2)
    return (sp.eye(3) + chi).applyfunc(sp.simplify)


def wave_matrix(eps, th, sc=None):
    """Normalized wave matrix N^2 (n n - 1) + eps for k = k (sin th, 0, cos th).

    Pass sc = (a, b) to use symbols for (sin th, cos th).
    """
    sn, cs = sc if sc else (sp.sin(th), sp.cos(th))
    nhat = sp.Matrix([sn, 0, cs])
    geo = N**2 * (nhat * nhat.T - sp.eye(3))
    return (geo + eps).applyfunc(sp.expand if sc else sp.simplify)


EPS = eps_electron()
S_e, D_e, P_e = EPS[0, 0], EPS[1, 0] / I, EPS[2, 2]  # one electron species
N_CIRC2 = 1 - wpe**2 / (w * (w + s * wce))  # N_s^2, :348
N_O2 = 1 - wpe**2 / w**2  # ordinary mode, :539
N_X2 = 1 - (wpe**2 * (w**2 - wpe**2)) / (w**2 * (w**2 - wpe**2 - wce**2))  # :570

# %% Cold velocity response
section("Cold magnetized velocity response", "12-cold-magnetized-waves.typ:142")
q, m = sp.symbols("q_s m_s", real=True)
Om = sp.Symbol("Omega_s")
note("Cold species in", sp.Eq(sp.Symbol("B"), B0 * sp.Symbol("e_z")), "with",
     sp.Eq(Om, q * B0 / m))
eqs, (ux, uy, uz) = momentum(q, m, Om)
for eq in eqs:
    show(eq)
velocity = sp.solve(eqs, [ux, uy, uz], dict=True)[0]
denominator = m * (w**2 - Om**2)
agrees(sp.simplify(velocity[ux]), I * q * w / denominator * Ex - q * Om / denominator * Ey,
       ":142", lhs=ux)
agrees(sp.simplify(velocity[uy]), q * Om / denominator * Ex + I * q * w / denominator * Ey,
       ":148", lhs=uy)
agrees(velocity[uz], (q / m) * Ez / (-I * w), ":137", lhs=uz)

# %% Cold dielectric tensor
section("Cold dielectric tensor", "12-cold-magnetized-waves.typ:78")
q1, q2 = sp.symbols("q_1 q_2", real=True)
m1, m2 = sp.symbols("m_1 m_2", positive=True)
Om1, Om2, wp1, wp2 = sp.symbols("Omega_1 Omega_2 omega_p1 omega_p2", real=True)
note("Current", sp.Eq(sp.Symbol("j"), sp.Symbol("q_s") * sp.Symbol("n_s") * sp.Symbol("u")), "and",
     sp.Eq(sp.Symbol("chi"), sp.Symbol("sigma") / (-I * w * eps0)), "with",
     sp.Eq(sp.Symbol("omega_ps") ** 2, sp.Symbol("n_s") * sp.Symbol("q_s") ** 2 / (eps0 * sp.Symbol("m_s"))))
chi1 = susceptibility(q1, m1, wp1**2 * eps0 * m1 / q1**2, Om1).applyfunc(sp.factor)
chi2 = susceptibility(q2, m2, wp2**2 * eps0 * m2 / q2**2, Om2).applyfunc(sp.factor)
for name, (row, col) in [("xx", (0, 0)), ("yx", (1, 0)), ("zz", (2, 2))]:
    show(sp.Eq(sp.Symbol(f"chi_1,{name}"), chi1[row, col]))
note("and", sp.Eq(sp.Symbol("chi_1,yy"), sp.Symbol("chi_1,xx")), ",",
     sp.Eq(sp.Symbol("chi_1,xy"), -sp.Symbol("chi_1,yx")), "; z decouples from x, y")
assert chi1[1, 1] == chi1[0, 0] and chi1[0, 1] == -chi1[1, 0]
assert all(chi1[a, b] == 0 for a, b in [(0, 2), (1, 2), (2, 0), (2, 1)])
eps = sp.eye(3) + chi1 + chi2
note("Two species,", sp.Eq(sp.Symbol("epsilon"), 1 + sp.Symbol("chi_1") + sp.Symbol("chi_2")))
e_perp = 1 - wp1**2 / (w**2 - Om1**2) - wp2**2 / (w**2 - Om2**2)
e_times = Om1 * wp1**2 / (w * (w**2 - Om1**2)) + Om2 * wp2**2 / (w * (w**2 - Om2**2))
agrees(eps[0, 0], e_perp, ":84", lhs=S)
agrees(eps[1, 0] / I, e_times, ":86", lhs=D)
agrees(eps[2, 2], 1 - wp1**2 / w**2 - wp2**2 / w**2, ":88", lhs=P)
si.check(eps[0, 1], -I * e_times)
si.check(eps[1, 1], e_perp)
for a, b in [(0, 2), (1, 2), (2, 0), (2, 1)]:
    si.check(eps[a, b], 0)
show(sp.Eq(sp.Symbol("epsilon"), sp.ImmutableMatrix(TENSOR), evaluate=False))
sigma = (chi1 + chi2) * (-I * w * eps0)
assert (eps * E - (E + I / (w * eps0) * sigma * E)).applyfunc(sp.simplify) == sp.zeros(3, 1)  # :159

# %% Magnetized wave equation
section("Magnetized wave equation", "12-cold-magnetized-waves.typ:105")
k_vec = sp.Matrix(sp.symbols("k_x k_y k_z"))
j = sp.Matrix(sp.symbols("j_x j_y j_z"))
B = k_vec.cross(E) / w  # Faraday k x E = w B
k_cross_B = -w * E / c**2 - I * mu0 * j  # Ampere
note("Faraday", sp.Eq(w * sp.Symbol("B"), sp.Symbol("k") * sp.Symbol("E")),
     "(cross product) inserted into Ampère; x component:")
k_cross_k_cross_E = k_vec.cross(k_vec.cross(E))
show(sp.Eq(k_cross_k_cross_E[0], w * k_cross_B[0]))
assert (k_cross_k_cross_E - (k_vec * k_vec.dot(E) - k_vec.dot(k_vec) * E)).applyfunc(
    sp.expand) == sp.zeros(3, 1)  # :178
assert (k_vec.cross(w * B) - k_cross_k_cross_E).applyfunc(sp.simplify) == sp.zeros(3, 1)
note("Eliminate j with", sp.Eq(sp.Symbol("epsilon") * sp.Symbol("E"),
                               sp.Symbol("E") + I * sp.Symbol("j") / (w * eps0)),
     "and", sp.Eq(mu0, 1 / (eps0 * c**2)))
eps_E = E + I / (w * eps0) * j
residual = (w * k_cross_B + w**2 / c**2 * eps_E).subs(mu0, 1 / (eps0 * c**2))
assert residual.applyfunc(sp.simplify) == sp.zeros(3, 1)  # :107
show(sp.Eq(k_cross_k_cross_E[0] + w**2 / c**2 * (TENSOR * E)[0], 0))

# %% Worked example: plasma and cyclotron frequency
section("Worked example: plasma and cyclotron frequency", "12-cold-magnetized-waves.typ:194")
omega_p = sp.sqrt(n0 * e**2 / (eps0 * m_e))
omega_c = e * B0 / m_e
assert si.same_unit(si.si_unit(omega_p, UNITS), u.second**-1)
assert si.same_unit(si.si_unit(omega_c, UNITS), u.second**-1)
example = {n0: 1e16 / u.meter**3, B0: 1e-2 * u.tesla}
note("Input", sp.Eq(n0, example[n0], evaluate=False), "and", sp.Eq(B0, example[B0], evaluate=False))
close_to(evaluate(wpe, omega_p, example, 1 / u.second), 5.64e9, source=":198")
close_to(evaluate(wce, omega_c, example, 1 / u.second), 1.76e9, source=":199")
ratio = number(omega_c / omega_p, example)
show(sp.Eq(wce / wpe, sp.Float(ratio, 3)))
close_to(ratio, 0.312, source=":200")

# %% Worked example: cold dielectric coefficients
section("Worked example: cold dielectric coefficients", "12-cold-magnetized-waves.typ:205")
drive = {w: 1.00e10, wpe: 5.64e9, wce: 1.76e9}
note("Frequencies in 1/s:", sp.Eq(w, sp.Float(drive[w], 3)), ",",
     sp.Eq(wpe, sp.Float(drive[wpe], 3)), ",", sp.Eq(wce, sp.Float(drive[wce], 3)))
for symbol, expr, printed, line in [(S, S_e, 0.672, ":214"), (D, D_e, -5.78e-2, ":215"),
                                    (P, P_e, 0.682, ":216")]:
    value = number(expr, drive)
    show(sp.Eq(symbol, sp.Float(value, 3)))
    close_to(value, printed, source=line)

# %% Parallel wave matrix
section("Parallel wave matrix", "12-cold-magnetized-waves.typ:323")
note("Wave equation divided by", w**2 / c**2, "with", sp.Eq(N, k * c / w), "and",
     sp.Eq(theta, 0, evaluate=False))
M_parallel = wave_matrix(TENSOR, 0)
show(sp.Eq(matmul(M_parallel, E), sp.ImmutableMatrix(sp.zeros(3, 1)), evaluate=False))
stated = sp.Matrix([[S_e - N**2, -I * D_e, 0], [I * D_e, S_e - N**2, 0], [0, 0, P_e]])
assert (wave_matrix(EPS, 0) - stated).applyfunc(sp.simplify) == sp.zeros(3, 3)  # :323
note("Transverse block: a nonzero field needs a vanishing determinant")
det = sp.factor(M_parallel[:2, :2].det())
agrees(det, (S - N**2) ** 2 - D**2, ":332", lhs=sp.Determinant(sp.ImmutableMatrix(M_parallel[:2, :2])))
roots = sp.solve(det, N**2)
assert set(roots) == {S + D, S - D}  # :336
show(sp.Eq(N**2, roots[0]))
show(sp.Eq(N**2, roots[1]))

# %% Circular eigenmodes
section("Circular eigenmodes", "12-cold-magnetized-waves.typ:348")
note("One electron species,", sp.Eq(sp.Symbol("Omega_e"), -wce), ":")
show(sp.Eq(S, S_e))
show(sp.Eq(D, D_e))
for sv in (1, -1):
    N_s2 = sp.factor(S_e - sv * D_e)
    agrees(N_s2, N_CIRC2.subs(s, sv), ":348", lhs=sp.Symbol(f"N_{'+' if sv > 0 else '-'}") ** 2)
    eigenvector = sp.Matrix([1, -I * sv])  # E_y = -i s E_x, :344
    assert (wave_matrix(EPS, 0)[:2, :2].subs(N**2, N_s2) * eigenvector).applyfunc(
        sp.simplify) == sp.zeros(2, 1)
note("Eigenvectors", sp.Eq(Ey, -I * s * Ex), "; resonance of", sp.Eq(s, -1), "at", sp.Eq(w, wce))
assert sp.solve(sp.denom(sp.together(N_CIRC2.subs(s, -1))), w) == [wce]  # :296

# %% Parallel cutoffs
section("Parallel cutoffs", "12-cold-magnetized-waves.typ:313")
assert sp.solve(P_e, w) == [wpe]  # longitudinal branch, :309
note("Longitudinal branch", sp.Eq(P, 0), "at", sp.Eq(w, wpe), "; circular cutoffs", sp.Eq(N, 0, evaluate=False))
cutoff = sp.numer(sp.together(N_CIRC2 * w * (w + s * wce)))
agrees(cutoff, w**2 + s * wce * w - wpe**2, ":353", lhs=sp.S.Zero)
for sv in (1, -1):
    roots = sp.solve(N_CIRC2.subs(s, sv), w)
    stated = (sp.sqrt(wce**2 + 4 * wpe**2) - sv * wce) / 2
    root = [r for r in roots if sp.simplify(r - stated) == 0][0]
    assert all(sp.simplify(r * stated).is_negative for r in roots if r != root)
    assert si.same_unit(si.si_unit(stated, UNITS), u.second**-1)
    agrees(root, stated, ":313", lhs=sp.Symbol(f"omega_cut,{'+' if sv > 0 else '-'}"))
note("The other root of each quadratic is negative")

# %% Faraday rotation
section("Faraday rotation", "12-cold-magnetized-waves.typ:368")
k_p, k_m, t, E0, L = sp.symbols("k_+ k_- t E_0 L", positive=True)
Phi, Delta = sp.symbols("Phi Delta", real=True)  # mean phase, half phase difference
note("Equal circular modes", sp.Eq(s, 1), "and", sp.Eq(s, -1), "with phases",
     Phi + Delta, "and", Phi - Delta)
E_x = show(sp.Eq(sp.Symbol("E_x"), sp.re(E0 / 2 * (sp.exp(I * (Phi + Delta)) + sp.exp(I * (Phi - Delta)))))).rhs
E_y = show(sp.Eq(sp.Symbol("E_y"), sp.re(E0 / 2 * (-I * sp.exp(I * (Phi + Delta))
                                                     + I * sp.exp(I * (Phi - Delta)))))).rhs
ratio = show(sp.Eq(sp.Symbol("E_y") / sp.Symbol("E_x"), sp.simplify(sp.expand_trig(E_y / E_x)))).rhs
assert sp.simplify(ratio - sp.tan(Delta)) == 0  # fixed angle Delta, independent of t
note("The polarization angle is", Delta, ", half the phase difference at", sp.Eq(sp.Symbol("z"), L))
half_phase = sp.simplify(((k_p * L - w * t) - (k_m * L - w * t)) / 2)
agrees(half_phase, (k_p - k_m) * L / 2, ":368", lhs=sp.Symbol("theta_F"))
z = sp.Symbol("z")
k_pz, k_mz = sp.Function("k_+")(z), sp.Function("k_-")(z)
note("Slowly varying plasma:", sp.Eq(sp.Symbol("theta_F"), sp.Integral(k_pz - k_mz, (z, 0, L)) / 2))
si.check(sp.diff(sp.Integral(k_pz - k_mz, (z, 0, z)) / 2, z), (k_pz - k_mz) / 2)  # :373

# %% Worked example: Faraday rotation
section("Worked example: Faraday rotation", "12-cold-magnetized-waves.typ:415")
drive = {w: 2.00e10, wpe: 5.64e9, wce: 1.76e9}
note("Frequencies in 1/s:", sp.Eq(w, sp.Float(drive[w], 3)), ",",
     sp.Eq(wpe, sp.Float(drive[wpe], 3)), ",", sp.Eq(wce, sp.Float(drive[wce], 3)),
     "; path length 10 cm")
N_p = number(sp.sqrt(N_CIRC2.subs(s, 1)), drive)
show(sp.Eq(sp.Symbol("N_+"), sp.Float(N_p, 3)))
close_to(N_p, 0.963, source=":424")
N_m = number(sp.sqrt(N_CIRC2.subs(s, -1)), drive)
show(sp.Eq(sp.Symbol("N_-"), sp.Float(N_m, 3)))
close_to(N_m, 0.955, source=":425")
theta_F = sp.Symbol("theta_F")
angle = evaluate(theta_F, (sp.Symbol("N_+") - sp.Symbol("N_-")) * w * L / (2 * c),
                 {sp.Symbol("N_+"): N_p, sp.Symbol("N_-"): N_m, w: drive[w] / u.second,
                  L: 0.10 * u.meter}, u.radian)
close_to(angle, 2.45e-2, source=":426")
close_to(evaluate(theta_F, angle * u.radian, {}, u.degree), 1.41, source=":426")

# %% Perpendicular O and X modes
section("Perpendicular O and X modes", "12-cold-magnetized-waves.typ:530")
note("Wave matrix at", sp.Eq(theta, sp.pi / 2, evaluate=False))
M_perp = wave_matrix(TENSOR, sp.pi / 2)
show(sp.Eq(matmul(M_perp, E), sp.ImmutableMatrix(sp.zeros(3, 1)), evaluate=False))
stated = sp.Matrix([[S_e, -I * D_e, 0], [I * D_e, S_e - N**2, 0], [0, 0, P_e - N**2]])
assert (wave_matrix(EPS, sp.pi / 2) - stated).applyfunc(sp.simplify) == sp.zeros(3, 3)  # :530
note("The z row decouples: ordinary mode")
N_O = sp.Symbol("N_O")
agrees(sp.solve(wave_matrix(EPS, sp.pi / 2)[2, 2], N**2)[0], N_O2, ":539", lhs=N_O**2)
note("The x-y block needs a vanishing determinant: extraordinary mode")
det = sp.expand(M_perp[:2, :2].det())
agrees(det, S * (S - N**2) - D**2, ":548", lhs=sp.Determinant(sp.ImmutableMatrix(M_perp[:2, :2])))
N_X = sp.Symbol("N_X")
N_X2_general = agrees(sp.solve(det, N**2)[0], (S**2 - D**2) / S, ":552", lhs=N_X**2)
note("With", sp.Eq(sp.Symbol("epsilon_s"), S - s * D), "the circular factors appear")
si.check(N_X2_general.subs({S: S_e, D: D_e}),
         N_CIRC2.subs(s, 1) * N_CIRC2.subs(s, -1) / S_e)  # :519, :619
show(sp.Eq(N_X**2, sp.Symbol("epsilon_+") * sp.Symbol("epsilon_-") / S))
first_row = (M_perp[0, :] * sp.Matrix([Ex, Ey, 0]))[0]
show(sp.Eq(first_row, 0))
agrees(sp.solve(first_row, Ex)[0] / Ey, I * D / S, ":587", lhs=Ex / Ey)

# %% Extraordinary mode and upper hybrid
section("Extraordinary mode and upper hybrid", "12-cold-magnetized-waves.typ:570")
agrees(S_e, 1 - wpe**2 / (w**2 - wce**2), ":556", lhs=S)
agrees(D_e, -(wce * wpe**2) / (w * (w**2 - wce**2)), ":560", lhs=D)
N_X2_electron = (S_e**2 - D_e**2) / S_e
shift = w**2 - wce**2
si.check(N_X2_electron, ((shift - wpe**2)**2 - wce**2 * wpe**4 / w**2) / (shift * (shift - wpe**2)))  # :566
show(sp.Eq(N_X**2, sp.factor(N_X2_electron)))
agrees(N_X2_electron, N_X2, ":570", lhs=N_X**2)
note("Resonance where the denominator vanishes")
pole = [r for r in sp.solve(sp.denom(sp.factor(N_X2_electron)), w) if r != 0]
upper_hybrid = sp.Symbol("omega_UH")
agrees(pole[0] ** 2, wpe**2 + wce**2, ":576", lhs=upper_hybrid**2)
si.check(pole[0] ** 2, wpe**2 + wce**2, unit=u.second**-2, units=UNITS)

# %% Worked example: perpendicular branches
section("Worked example: perpendicular branches", "12-cold-magnetized-waves.typ:593")
drive = {w: 5.50e9 / u.second, wpe: 5.64e9 / u.second, wce: 1.76e9 / u.second}
note("Frequencies in 1/s:", sp.Eq(w, sp.Float(5.50e9, 3)), ",", sp.Eq(wpe, sp.Float(5.64e9, 3)),
     ",", sp.Eq(wce, sp.Float(1.76e9, 3)))
N_O2_value = number(N_O2, drive)
assert N_O2_value < 0
show(sp.Eq(N_O**2, sp.Float(N_O2_value, 3)))
note("O mode evanescent,", sp.Eq(k, I * sp.Symbol("alpha_O"), evaluate=False))
close_to(evaluate(sp.Symbol("alpha_O"), sp.sqrt(-N_O2) * w / c, drive, 1 / u.meter), 4.17,
         source=":602")
N_X_value = number(sp.sqrt(N_X2), drive)
assert N_X_value > 0
show(sp.Eq(N_X, sp.Float(N_X_value, 3)))
close_to(N_X_value, 0.805, source=":603")
close_to(evaluate(sp.Symbol("k_X"), sp.sqrt(N_X2) * w / c, drive, 1 / u.meter), 14.8,
         source=":604")
close_to(evaluate(sp.Symbol("lambda_X"), 2 * sp.pi * c / (sp.sqrt(N_X2) * w), drive, u.meter),
         0.425, source=":605")

# %% Oblique wave matrix and quadratic
section("Oblique wave matrix and quadratic", "12-cold-magnetized-waves.typ:735")
Sx, Dx, Px, Z = sp.symbols("S D P Z")  # Stix S, D, P and Z = N^2
stix = sp.Matrix([[Sx, -I * Dx, 0], [I * Dx, Sx, 0], [0, 0, Px]])
note("Stix notation", sp.Eq(Sx, S), ",", sp.Eq(Dx, D), ",", sp.Eq(Px, P), "; k in the x-z plane")
sn, cs = sp.sin(theta), sp.cos(theta)
M_oblique = wave_matrix(stix, theta)
show(sp.Eq(matmul(wave_matrix(stix, theta, (sn, cs)), E), sp.ImmutableMatrix(sp.zeros(3, 1)),
           evaluate=False))
stated = sp.Matrix([[Sx - N**2 * cs**2, -I * Dx, N**2 * sn * cs], [I * Dx, Sx - N**2, 0],
                    [N**2 * sn * cs, 0, Px - N**2 * sn**2]])
assert (M_oblique - stated).applyfunc(sp.simplify) == sp.zeros(3, 3)  # :679
geometric = M_oblique - stix
si.check(geometric[0, 0] * Ex + geometric[0, 2] * Ez, -N**2 * cs**2 * Ex + N**2 * sn * cs * Ez)  # :722
si.check(geometric[2, 0] * Ex + geometric[2, 2] * Ez, N**2 * sn * cs * Ex - N**2 * sn**2 * Ez)  # :726
a, b = sp.symbols("a b")
note("Write", sp.Eq(a, sn), ",", sp.Eq(b, cs), ",", sp.Eq(Z, N**2), "; on the unit circle",
     sp.Eq(a**2 + b**2, 1))
M_ab = wave_matrix(stix, theta, (a, b)).subs(a**2, 1 - b**2).applyfunc(sp.expand)
on_circle = {a: sp.sqrt(1 - b**2)}
det = sp.collect(sp.expand(M_ab.det().subs(N, sp.sqrt(Z)).subs(on_circle)), Z)
stated_det = (Px - Z * a**2) * ((Sx - Z * b**2) * (Sx - Z) - Dx**2) - Z**2 * a**2 * b**2 * (Sx - Z)
agrees(det, stated_det.subs(on_circle), ":735", lhs=sp.Determinant(M_sym))
A, B_, C = sp.symbols("A B C")
coefficients = {A: Sx * a**2 + Px * b**2, B_: (Sx**2 - Dx**2) * a**2 + Px * Sx * (1 + b**2),
                C: Px * (Sx**2 - Dx**2)}
note("The", Z**3, "terms cancel; the determinant is a quadratic in", Z)
quadratic = A * Z**2 - B_ * Z + C
show(sp.Eq(sp.Determinant(M_sym), quadratic))
for symbol, value in coefficients.items():
    show(sp.Eq(symbol, value))
agrees(det, quadratic.subs(coefficients).subs(on_circle), ":740", lhs=sp.Determinant(M_sym))
roots = sp.solve(quadratic.subs(coefficients), Z)
discriminant = sp.sqrt(coefficients[B_]**2 - 4 * coefficients[A] * coefficients[C])
for sign in (1, -1):
    root = (coefficients[B_] + sign * discriminant) / (2 * coefficients[A])
    assert any(sp.simplify(r - root) == 0 for r in roots)  # :750
    show(sp.Eq(sp.Symbol("Z_+" if sign > 0 else "Z_-"),
               (B_ + sign * sp.sqrt(B_**2 - 4 * A * C)) / (2 * A)))

# %% S, D, P for one electron species
section("S, D, P for one electron species", "12-cold-magnetized-waves.typ:755")
X_w, Y_w = sp.symbols("X_omega Y_omega", positive=True)
to_XY = {wpe: sp.sqrt(X_w) * w, wce: Y_w * w}
note("Normalize by the wave frequency:", sp.Eq(X_w, wpe**2 / w**2), ",", sp.Eq(Y_w, wce / w))
S_XY, D_XY, P_XY = (sp.simplify(x.subs(to_XY)) for x in (S_e, D_e, P_e))
agrees(S_XY, 1 - X_w / (1 - Y_w**2), ":755", lhs=Sx)
agrees(P_XY, 1 - X_w, ":756", lhs=Px)
show(sp.Eq(Dx, sp.factor(D_XY)))
agrees(sp.factor(D_XY) ** 2, (Y_w * X_w / (1 - Y_w**2)) ** 2, ":760", lhs=Dx**2)
agrees(sp.factor(S_XY**2 - D_XY**2), ((1 - X_w)**2 - Y_w**2) / (1 - Y_w**2), ":764",
       lhs=Sx**2 - Dx**2)

# %% Appleton-Hartree roots
section("Appleton-Hartree roots", "12-cold-magnetized-waves.typ:686")
Q, T, R = sp.symbols("Q T R")
note("Appleton-Hartree form", sp.Eq(Z, 1 - X_w / Q), "with", sp.Eq(Q, 1 - T + R), "or",
     sp.Eq(Q, 1 - T - R))
T_value = Y_w**2 * a**2 / (2 * (1 - X_w))
R2_value = T_value**2 + Y_w**2 * b**2
show(sp.Eq(T, T_value))
show(sp.Eq(R**2, R2_value))
note("Both signs are the roots of")
q_poly = show(sp.Eq((Q - 1 + T)**2 - R**2, 0)).lhs.subs({T: T_value, R**2: R2_value})
appleton = sp.numer(sp.together(q_poly.subs(Q, X_w / (1 - Z)).subs(a**2, 1 - b**2)))
stix_poly = sp.numer(sp.together(quadratic.subs(coefficients).subs({Sx: S_XY, Dx: D_XY, Px: P_XY})
                                 .subs(a, sp.sqrt(1 - b**2))))
ratio = sp.factor(sp.cancel(sp.expand(appleton) / sp.expand(stix_poly)))
note("Insert", sp.Eq(Q, X_w / (1 - Z)), "; the ratio to the Stix quadratic is free of", Z)
show(sp.Eq(sp.Symbol("q_AH") / sp.Symbol("q_Stix"), ratio))
assert Z not in ratio.free_symbols, ratio  # same pair of roots

# %% Oblique endpoints
section("Oblique endpoints", "12-cold-magnetized-waves.typ:774")
note("Parallel,", sp.Eq(theta, 0, evaluate=False), ": P and the two circular modes")
agrees(sp.factor(wave_matrix(stix, 0).det()), Px * (Sx + Dx - N**2) * (Sx - Dx - N**2), ":774",
       lhs=sp.Determinant(M_sym))
note("Perpendicular,", sp.Eq(theta, sp.pi / 2, evaluate=False), ": O mode times the X block")
agrees(sp.factor(wave_matrix(stix, sp.pi / 2).det()), (Px - N**2) * (Sx * (Sx - N**2) - Dx**2),
       ":776", lhs=sp.Determinant(M_sym))

# %% Worked example: oblique Appleton-Hartree roots
section("Worked example: oblique Appleton-Hartree roots", "12-cold-magnetized-waves.typ:785")
note("Input", sp.Eq(W, sp.Float(1.5, 3)), ",", sp.Eq(Y, sp.Float(0.3, 2)), ",",
     sp.Eq(theta, sp.pi / 4, evaluate=False))
X_of_W, Y_of_W = (wpe**2 / w**2).subs(NORM), (wce / w).subs(NORM)
note("Normalized by", wpe, ":", sp.Eq(X_w, X_of_W), ",", sp.Eq(Y_w, Y_of_W))
X_value = number(X_of_W, {W: 1.5})
show(sp.Eq(X_w, sp.Float(X_value, 3)))
close_to(X_value, 0.444, source=":792")
Y_value = number(Y_of_W, {W: 1.5, Y: 0.3})
show(sp.Eq(Y_w, sp.Float(Y_value, 3)))
close_to(Y_value, 0.200, source=":793")
oblique = {X_w: X_value, Y_w: Y_value, a: sp.sin(sp.pi / 4), b: sp.cos(sp.pi / 4)}
T_num, R_num = T_value.subs(oblique), sp.sqrt(R2_value.subs(oblique))
N_plus = number(sp.sqrt(1 - X_w / (1 - T + R)), {**oblique, T: T_num, R: R_num})
N_minus = number(sp.sqrt(1 - X_w / (1 - T - R)), {**oblique, T: T_num, R: R_num})
show(sp.Eq(sp.Symbol("N_+"), sp.Float(N_plus, 3)))
close_to(N_plus, 0.778, source=":794")
show(sp.Eq(sp.Symbol("N_-"), sp.Float(N_minus, 3)))
close_to(N_minus, 0.686, source=":795")
note("Check: positive roots of the full determinant")
tensor = stix.subs({Sx: S_XY, Dx: D_XY, Px: P_XY}).subs({X_w: X_value, Y_w: Y_value})
full_roots = [float(r) for r in sp.Poly(sp.expand(wave_matrix(tensor, sp.pi / 4).det()), N).nroots()
              if r.is_real and r > 0]
show(sp.Eq(N, sp.FiniteSet(*[sp.Float(r, 3) for r in full_roots]), evaluate=False))
assert any(abs(r - N_plus) < 1e-9 for r in full_roots)
assert any(abs(r - N_minus) < 1e-9 for r in full_roots)

# %% Normalized landmarks and limits
section("Normalized landmarks and limits", "12-cold-magnetized-waves.typ:882")
note("Normalize by", wpe, ":", sp.Eq(W, w / wpe), ",", sp.Eq(Y, wce / wpe))
eps_s = sp.simplify(N_CIRC2.subs(NORM))
show(sp.Eq(sp.Symbol("N_s") ** 2, eps_s))
for sv in (1, -1):
    roots = sp.solve(eps_s.subs(s, sv), W)
    stated = (sp.sqrt(Y**2 + 4) - sv * Y) / 2
    root = [r for r in roots if sp.simplify(r - stated) == 0][0]
    agrees(root, stated, ":884", lhs=sp.Symbol(f"W_cut,{'+' if sv > 0 else '-'}"))
upper = [r for r in sp.solve((w**2 - wpe**2 - wce**2).subs(NORM), W) if r.is_positive]
agrees(upper[0], sp.sqrt(1 + Y**2), ":886", lhs=sp.Symbol("W_UH"))
assert sp.solve(N_O2.subs(NORM), W) == [1]  # ordinary cutoff, :886
note("Ordinary cutoff at", sp.Eq(W, 1, evaluate=False), "; without magnetic field,",
     sp.Eq(Y, 0, evaluate=False), ":")
for sv in (1, -1):
    si.check(eps_s.subs(s, sv).subs(Y, 0), 1 - 1 / W**2)  # :899
show(sp.Eq(N**2, eps_s.subs(Y, 0)))
W_K = sp.solve(sp.Eq((K / W) ** 2, 1 - 1 / W**2), W)
note("With", sp.Eq(N, K / W), ":")
agrees(W_K[0] ** 2, 1 + K**2, ":904", lhs=W**2)
for branch in (eps_s.subs(s, 1), eps_s.subs(s, -1), N_X2.subs(NORM), N_O2.subs(NORM)):
    assert sp.limit(branch, W, sp.oo) == 1  # :913
show(sp.Eq(sp.Limit(sp.Symbol("N_s") ** 2, W, sp.oo), sp.limit(eps_s, W, sp.oo)))
note("and the same limit for", sp.Symbol("N_O") ** 2, "and", sp.Symbol("N_X") ** 2)

# %% Worked example: landmarks and classification
section("Worked example: landmarks and classification", "12-cold-magnetized-waves.typ:944")
Y_PLOT = 0.3  # omega_ce/omega_pe of the plots and the worked example (:946)
note("Input", sp.Eq(Y, sp.Float(Y_PLOT, 2)))
for symbol, expr, printed, line in [("W_cut,+", (sp.sqrt(Y**2 + 4) - Y) / 2, 0.861, ":953"),
                                    ("W_cut,-", (sp.sqrt(Y**2 + 4) + Y) / 2, 1.161, ":954"),
                                    ("W_UH", sp.sqrt(1 + Y**2), 1.044, ":955")]:
    value = number(expr, {Y: Y_PLOT})
    show(sp.Eq(sp.Symbol(symbol), sp.Float(value, 4)))
    close_to(value, printed, source=line)
N_O2_W, N_X2_W = (sp.simplify(x.subs(NORM).subs(Y, Y_PLOT)) for x in (N_O2, N_X2))
assert number(N_O2_W, {W: 0.90}) < 0 and number(N_X2_W, {W: 0.90}) > 0  # :956
assert number(N_O2_W, {W: 1.10}) > 0 and number(N_X2_W, {W: 1.10}) < 0  # :958
for W_value, symbol, expr, printed, line in [(0.90, "N_X", N_X2_W, 0.403, ":957"),
                                             (1.10, "N_O", N_O2_W, 0.417, ":959"),
                                             (1.30, "N_O", N_O2_W, 0.639, ":961"),
                                             (1.30, "N_X", N_X2_W, 0.565, ":962")]:
    value = number(sp.sqrt(expr), {W: W_value})
    note("At", sp.Eq(W, sp.Float(W_value, 2)))
    show(sp.Eq(sp.Symbol(symbol), sp.Float(value, 3)))
    close_to(value, printed, source=line)
note("O evanescent and X propagating at 0.90, the reverse at 1.10, both propagate at 1.30")


def normalized(expr, **subs):
    """Lambdify a branch in W at Y = Y_PLOT (omega_pe cancels)."""
    return sp.lambdify(W, sp.simplify(expr.subs(NORM).subs(Y, Y_PLOT).subs(subs)), "numpy")


PANEL = (2.6, 3.0)  # one panel of a side-by-side pair
cutoffs = [float((sp.sqrt(Y**2 + 4) - sv * Y).subs(Y, Y_PLOT) / 2) for sv in (1, -1)]
W_UH = float(upper[0].subs(Y, Y_PLOT))

# %% Plot: parallel circular branches W(K), with K = W N_s
fig, ax = figure(4.2, 3.0)
K_grid = np.linspace(0, 3, 50)
ax.plot(K_grid, K_grid, color=GRAY, ls=":", lw=1.2)
ax.axhline(Y_PLOT, color=GRAY, lw=0.8, ls="-.")
spacing = np.linspace(0, 1, 400) ** 2  # quadratic sampling resolves the cutoff
for sv, color, ls, cut in ((1, BLUE, "-", cutoffs[0]), (-1, ORANGE, "--", cutoffs[1])):
    N_s2 = normalized(N_CIRC2, s=sv)
    W_grid = cut + (3.2 - cut) * spacing
    ax.plot(W_grid * np.sqrt(np.clip(N_s2(W_grid), 0, None)), W_grid, color=color, ls=ls)
    ax.plot([0], [cut], "o", color=color, ms=4, clip_on=False, zorder=3)
N_s2 = normalized(N_CIRC2, s=-1)
W_grid = Y_PLOT * (1 - np.geomspace(1, 1e-4, 400))  # whistler, below the resonance W = Y
with np.errstate(divide="ignore", invalid="ignore"):  # K = 0 at W = 0
    ax.plot(W_grid * np.sqrt(N_s2(W_grid)), W_grid, color=ORANGE, ls="--")
label(ax, 1.0, 1.75, "$s=-1$", ORANGE, ha="right")
label(ax, 1.6, 1.35, "$s=+1$", BLUE, va="top")
label(ax, 2.95, Y_PLOT, "resonance $\\omega=\\omega_{ce}$", GRAY, ha="right")
label(ax, 2.95, Y_PLOT * 0.62, "whistler, $s=-1$", ORANGE, ha="right", va="top")
label(ax, 2.55, 2.3, "vacuum", GRAY, va="top")
ax.set(xlim=(0, 3), ylim=(0, 3), xticks=[0, 1, 2, 3], yticks=[0, Y_PLOT, *cutoffs, 2, 3],
       yticklabels=["0", f"{Y_PLOT:.1f}", f"{cutoffs[0]:.3f}", f"{cutoffs[1]:.3f}", "2", "3"],
       xlabel=r"$K=kc/\omega_{pe}$ [1]", ylabel=r"$W=\omega/\omega_{pe}$ [1]")
save(fig, "magnetized-parallel-dispersion")


def perpendicular_panel(ax):
    """Shared axes of the O- and X-mode panels: N^2 against W, evanescent band shaded."""
    ax.axhspan(-4, 0, color="#eeeeee", lw=0, zorder=0)
    ax.axhline(0, color="#333333", lw=0.6)
    ax.set(xlim=(0.6, 1.8), ylim=(-4, 3), yticks=[-4, -2, 0, 2], xticks=[0.6, 1, 1.4, 1.8],
           xlabel=r"$W=\omega/\omega_{pe}$ [1]", ylabel=r"$N^2=(kc/\omega)^2$ [1]")


# %% Plot: perpendicular ordinary mode N_O^2(W)
N_O2_plot = normalized(N_O2)
fig, ax = figure(*PANEL)
perpendicular_panel(ax)
W_grid = np.linspace(0.6, 1.8, 600)
ax.plot(W_grid, N_O2_plot(W_grid), color=ORANGE, ls="--")
ax.plot([1], [0], "o", color=ORANGE, ms=4, zorder=3)
label(ax, 1.04, -0.25, "cutoff $W=1$", ORANGE, va="top")
label(ax, 1.75, N_O2_plot(1.75) + 0.15, "O mode", ORANGE, ha="right")
label(ax, 0.63, 1.6, "propagating", GRAY)
label(ax, 0.63, -3.6, "evanescent", GRAY)
save(fig, "perpendicular-o-mode")

# %% Plot: perpendicular extraordinary mode N_X^2(W)
N_X2_plot = normalized(N_X2)
fig, ax = figure(*PANEL)
perpendicular_panel(ax)
ax.axvline(W_UH, color=GRAY, lw=0.8, ls="-.")
for lo, hi in ((0.6, W_UH - 1e-4), (W_UH + 1e-4, 1.8)):  # split at the resonance
    W_grid = np.linspace(lo, hi, 600)
    ax.plot(W_grid, N_X2_plot(W_grid), color=BLUE)
ax.plot(cutoffs, [0, 0], "o", color=BLUE, ms=4, zorder=3)
label(ax, W_UH + 0.05, 2.85, f"upper\nhybrid\n$W={W_UH:.3f}$", GRAY, va="top")
label(ax, 1.75, N_X2_plot(1.75) + 0.15, "X mode", BLUE, ha="right")
ax.set_xticks([0.6, cutoffs[0], cutoffs[1], 1.8],
              ["0.6", f"{cutoffs[0]:.3f}", f"{cutoffs[1]:.3f}", "1.8"])
save(fig, "perpendicular-x-mode")

# %%
if __name__ == "__main__":
    report(__file__, "Chapter 12 · Cold magnetized waves")
