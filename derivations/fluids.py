"""Shared helpers for the fluid chapters 6-10.

Fields of (t, x, y, z), vector calculus on component lists, and the explicit
test distribution of Chapter 6 with its velocity integrator. Plain functions
without display: the chapter scripts show what they compute.
"""

from functools import lru_cache

import sympy as sp

t, x, y, z = sp.symbols("t x y z", real=True)
X = (x, y, z)
v = sp.symbols("v_x v_y v_z", real=True)
q_s, m_s = sp.symbols("q_s m_s", real=True)

_FIELDS = {}


def field(name, *args):
    """Undefined real function of (t, x, y, z), or of `args`, printed as `name`.

    field("rho_s") prints as rho_s instead of rho_s(t, x, y, z); a name
    containing "parallel" or "perp" prints with the parallel or perpendicular sign.
    """
    args = args or (t, x, y, z)
    if name not in _FIELDS:
        shown, terminal = _shown(name)

        def _latex(self, printer, exp=None):
            tex = printer._print(shown)
            return tex if exp is None else f"{tex}^{{{exp}}}"

        def _pretty(self, printer):
            return printer._print(terminal)

        def _sympystr(self, printer):
            return name

        _FIELDS[name] = sp.Function(name, real=True, __dict__={
            "_latex": _latex, "_pretty": _pretty, "_sympystr": _sympystr})
    return _FIELDS[name](*args)


def _shown(name):
    """LaTeX and terminal display names: "parallel" and "perp" become signs."""
    return (sp.Symbol(name.replace("parallel", r"\parallel").replace("perp", r"\perp")),
            sp.Symbol(name.replace("parallel", "∥").replace("perp", "⊥")))


class Named(sp.Symbol):
    """Symbol whose name may contain "parallel" or "perp": sigma_perp prints as a
    sigma with a perpendicular sign."""

    def _latex(self, printer, exp=None):
        tex = printer._print(_shown(self.name)[0])
        return tex if exp is None else f"{tex}^{{{exp}}}"

    def _pretty(self, printer):
        return printer._print(_shown(self.name)[1])


def vec(name):
    """Three fields: u_x, u_y, u_z for vec("u"); u_1x, ... for vec("u_1")."""
    sep = "" if "_" in name else "_"
    return [field(f"{name}{sep}{c}") for c in "xyz"]


class Partial(sp.Derivative):
    """Unevaluated derivative whose LaTeX brackets a product: d/dx (n u).

    A derivative of zero is dropped, so 1D forms print without 0 terms."""

    def __new__(cls, expr, *variables, **kw):
        if sp.sympify(expr) == 0:
            return sp.S.Zero
        return super().__new__(cls, expr, *variables, **kw)

    def _eval_expand_basic(self, **hints):
        # sp.expand (and so notebook.agrees) evaluates the derivative.
        return self.doit()

    def _latex(self, printer):
        tex = printer._print_Derivative(self)
        inner = printer._print(self.expr)
        if isinstance(self.expr, (sp.Mul, sp.Pow)) and tex.endswith(inner):
            tex = tex[: -len(inner)] + rf"\left({inner}\right)"
        return tex


def div(a):
    return sum(sp.diff(a[i], X[i]) for i in range(3))


def grad(g):
    return [sp.diff(g, xi) for xi in X]


def curl(a, d=sp.diff):
    """Curl of a component list; d=Partial keeps the derivatives unevaluated."""
    return [d(a[2], y) - d(a[1], z), d(a[0], z) - d(a[2], x), d(a[1], x) - d(a[0], y)]


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def dot(a, b):
    return sum(a[i] * b[i] for i in range(3))


def tdiv(T):
    """Divergence of a rank-two tensor: (div T)_i = sum_j d_j T_ij."""
    return [sum(sp.diff(T[i][j], X[j]) for j in range(3)) for i in range(3)]


def lap(g, d=sp.diff):
    return sum(d(g, xi, 2) for xi in X)


def first_order(expr, eps):
    """Coefficient of eps in expr (linearization)."""
    return sp.expand(sp.diff(expr, eps).subs(eps, 0))


# --- Test distribution of Chapter 6 ------------------------------------------
# A drifting anisotropic Gaussian with a Hermite skew (kappa, gives a heat
# flux) and a shear term (lambda, gives P_xy). All parameters are fields of
# (t, x, y, z); s_i = (v_i - u_i)/sigma_i is the random velocity in widths.
n = field("n_s")
U = vec("u")
SIGMA = vec("sigma")
kappa, lam = field("kappa"), field("lambda")
E, B = vec("E"), vec("B")
S = sp.symbols("s_x s_y s_z", real=True)
SHAPE = (n / ((2 * sp.pi) ** sp.Rational(3, 2) * SIGMA[0] * SIGMA[1] * SIGMA[2])
         * sp.exp(-(S[0]**2 + S[1]**2 + S[2]**2) / 2)
         * (1 + kappa * (S[0]**3 - 3 * S[0]) + lam * S[0] * S[1]))
f = SHAPE.subs({S[i]: (v[i] - U[i]) / SIGMA[i] for i in range(3)})

# The kinetic equation in abstract form: f and the acceleration a are
# undefined functions until on_test() inserts the test distribution and the
# Lorentz acceleration a = (q_s/m_s)(E + v x B).
F = field("f", t, x, y, z, *v)
A = [field(f"a_{c}", t, x, y, z, *v) for c in "xyz"]
LORENTZ = {A[i]: q_s / m_s * (E[i] + cross(v, B)[i]) for i in range(3)}
KINETIC = (Partial(F, t) + sum(Partial(v[j] * F, X[j]) for j in range(3))
           + sum(Partial(A[j] * F, v[j]) for j in range(3)))
VELOCITIES = [(vi, -sp.oo, sp.oo) for vi in v]
W_REL = sp.symbols("w_x w_y w_z", real=True)   # random velocity v - u, for display


class VelocityIntegral(sp.Integral):
    """Integral over all of velocity space, printed as int ... d^3v."""

    def __new__(cls, integrand, *limits, **kw):
        return super().__new__(cls, integrand, *(limits or VELOCITIES), **kw)

    def _latex(self, printer):
        return rf"\int {printer.parenthesize(self.function, 50, strict=True)}\, d^3v"

    def _pretty(self, printer):
        from sympy.printing.pretty.stringpict import prettyForm

        body = printer._print(self.function)
        if isinstance(self.function, sp.Add):
            body = prettyForm(*body.parens())
        return prettyForm(*prettyForm(*body.left("∫ ")).right(" d³v"))


def moment(weight):
    """Velocity moment int weight f d^3v of the abstract f, unevaluated."""
    return VelocityIntegral(weight * F)


def on_test(expr):
    """Insert the Lorentz acceleration, w = v - u and the test distribution; evaluate."""
    return expr.subs(LORENTZ).subs({W_REL[i]: v[i] - U[i] for i in range(3)}).subs(F, f).doit()


@lru_cache(None)
def gauss_moment(k):
    """int_R w^k exp(-w^2/(2 a^2)) dw for a > 0, done by SymPy."""
    a, w = sp.symbols("a w", positive=True)
    return sp.Lambda(a, sp.integrate(w**k * sp.exp(-w**2 / (2 * a**2)), (w, -sp.oo, sp.oo)))


def vint(expr, widths=None):
    """Integrate expr(v) over R^3. expr must be a polynomial in v times the
    Gaussian exp(-sum_i (v_i - u_i)^2 / (2 widths_i^2)) (default: sigma_i)."""
    widths = SIGMA if widths is None else widths
    w = sp.symbols("w_x w_y w_z", real=True)
    G_w = sp.exp(-sum(w[i] ** 2 / widths[i] ** 2 for i in range(3)) / 2)
    e_w = sp.expand(sp.powsimp(
        expr.subs({v[i]: U[i] + w[i] for i in range(3)}, simultaneous=True) / G_w))
    total = 0
    for term in sp.Add.make_args(e_w):
        coeff, mono = term.as_independent(*w, as_Add=False)
        powers = mono.as_powers_dict()
        k = [int(powers.get(wi, 0)) for wi in w]
        assert mono == sp.Mul(*[w[i] ** k[i] for i in range(3)]), mono
        total += coeff * sp.Mul(*[gauss_moment(k[i])(widths[i]) for i in range(3)])
    return sp.expand(total)


def integrate(integral):
    """Evaluate a velocity-space sp.Integral of the abstract f on the test distribution."""
    return vint(on_test(integral.function))


@lru_cache(None)
def moments():
    """Central moments of the test distribution: n, u, P_ij, q_i."""
    w = [v[i] - U[i] for i in range(3)]
    dens = vint(f)
    flow = [vint(v[i] * f) / dens for i in range(3)]
    P = [[m_s * vint(w[i] * w[j] * f) for j in range(3)] for i in range(3)]
    w2 = sum(wi**2 for wi in w)
    q = [m_s / 2 * vint(w2 * w[i] * f) for i in range(3)]
    return dens, flow, P, q


# Moments in compact notation. moment_values() gives their values on the test
# distribution, so a statement written with P_ij, q_i, epsilon_s, W_s and the
# raw energy flux F_i can be checked there.
P = [[field(f"P_{a}{b}") for b in "xyz"] for a in "xyz"]
q = vec("q")
eps, W = field("epsilon_s"), field("W_s")
F_W = vec("F")
EPS_DEF = (P[0][0] + P[1][1] + P[2][2]) / 2       # epsilon_s = tr(P_s)/2
W_DEF = moment(m_s * dot(v, v) / 2)               # energy density W_s


@lru_cache(None)
def moment_values():
    _, _, P_test, q_test = moments()
    values = {P[i][j]: P_test[i][j] for i in range(3) for j in range(3)}
    values.update({q[i]: q_test[i] for i in range(3)})
    values[eps] = EPS_DEF.subs(values)
    values[W] = integrate(W_DEF)
    values.update({F_W[i]: integrate(moment(m_s * dot(v, v) * v[i] / 2)) for i in range(3)})
    return values



def rounded(expr, digits=3):
    """expr with every Float rounded to `digits`, so inputs print as 2.00e+5."""
    return expr.xreplace({f: sp.Float(f, digits) for f in expr.atoms(sp.Float)})
