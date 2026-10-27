"""Run every chapter script top to bottom; a failed `agrees`/`close_to` fails the test.

The chapter scripts reference the Typst script only by section label
(`section(..., script="<label>")`) and equation label (`eq="<label>"`), never
by line number; the tests below keep it that way.
"""

import json
import re
import runpy
from pathlib import Path

import pytest

import notebook


def test_saha_cmod_independent_nrl():
    """NRL's rounded cgs coefficient is independent of the SI implementation."""
    import math
    import plot_saha_cmod as model

    def nrl_rhs(temperature):
        return 6.0e27 * temperature**1.5 * math.exp(-13.6 / temperature)

    temperature = model.half_ionization_temperature(1e20, model.saha_ground_rhs)
    assert abs(nrl_rhs(temperature) / 5e19 - 1) < 0.01
    assert abs(temperature * 11604.51812 - 8687) < 10
    # With the lecture's g_0=1 convention the reciprocal level population
    # has half the p=1 population (g_1=2); test the actual plotted function.
    ground = model.saha_level_population(1, temperature, 5e19, 5e19) / 2
    assert abs(ground / 5e19 - 1) < 0.01


def test_saha_cmod_measured_populations():
    """Digitized experimental populations constrain the high-level prediction."""
    import numpy as np
    import plot_saha_cmod as model

    _, levels, measured, _, row = model.load_data()
    predicted = model.saha_level_population(
        levels, float(row['kBT_e_eV']), float(row['n_e_m-3']), float(row['n_i_m-3']))
    ratios = measured[levels >= 5] / predicted[levels >= 5]
    assert len(ratios) == 6
    assert np.all((ratios >= 1.0) & (ratios <= 1.5)), ratios

def test_debye_nonlinear_poisson_boltzmann():
    """The solver solves the Poisson-Boltzmann ODE with the enclosed-charge
    boundary condition, the far field agrees with Debye-Hueckel to order
    Lambda, and e Phi = k_B T_e lies at r ~ Lambda lambda_D (Coulomb region)."""
    import numpy as np
    import plot_debye_nonlinear as model

    for lam in model.STRENGTHS:
        sol = model.solve(lam)
        assert abs(sol.sol(sol.a)[1] + lam) < 1e-8 * max(lam, 1)   # rho^2 phi' = -Lambda at a
        x = np.geomspace(2 * sol.a, 6.0, 60)
        h = 1e-4 * x
        phi, up, dn = sol.sol(x)[0], sol.sol(x + h)[0], sol.sol(x - h)[0]
        residual = (up - 2 * phi + dn) / h**2 + 2 * (up - dn) / (2 * h) / x - np.expm1(phi)
        scale = abs((up - 2 * phi + dn) / h**2) + abs(np.expm1(phi))
        assert np.max(abs(residual) / scale) < 1e-3, lam
        ratio = model.far_field_ratio(sol, lam)
        assert np.all(abs(ratio - 1) < lam), (lam, ratio)
        assert abs(model.unit_crossing(sol) / lam - 1) < 0.02, lam


def test_mu_ramp_boris_against_dop853():
    """The Boris values of mu_final/mu_initial - 1 agree with an independent
    high-order integration of the same orbit, are non-negative, and fall
    exponentially for the tanh ramp but only algebraically for the linear one."""
    import numpy as np
    from scipy.integrate import solve_ivp
    import plot_mu_ramp as model

    def reference(tau, smooth):
        def rhs(t, y):
            b = model.field(t, tau, smooth)
            if smooth:
                b_dot = 0.5 / tau / np.cosh(t / tau) ** 2
            else:
                b_dot = 0.5 / tau if abs(t) < tau else 0.0
            ex, ey = 0.5 * b_dot * y[1], -0.5 * b_dot * y[0]
            return [y[2], y[3], ex + y[3] * b, ey - y[2] * b]
        half = 8 * tau + 20 * np.pi
        cuts = [-half, half] if smooth else [-half, -tau, tau, half]
        y = [1.0, 0.0, 0.0, -1.0]
        for a, b in zip(cuts[:-1], cuts[1:]):
            y = solve_ivp(rhs, (a, b), y, method="DOP853", rtol=1e-12, atol=1e-13).y[:, -1]
        return 0.5 * (y[2] ** 2 + y[3] ** 2) / 2.0 / 0.5 - 1

    taus = np.array([1.0, 2.0, 3.0, 4.0])
    for smooth in (True, False):
        boris = model.boris(taus, smooth, steps_per_turn=800)
        exact = np.array([reference(tau, smooth) for tau in taus])
        assert np.all(boris > 0), boris
        assert np.allclose(boris, exact, rtol=2e-3), (smooth, boris, exact)
        if smooth:
            assert np.all(boris[1:] < 0.1 * boris[:-1]), boris      # a decade per unit of tau
        else:
            assert boris[3] > 0.1 * boris[1], boris                 # algebraic: less than a decade over two units


def test_loss_cone_sample_against_pitch_angle():
    """The trapped/lost test from mu and energy along B(z) agrees particle by
    particle with the pitch-angle condition sin^2(theta) >= 1/R_m, and the lost
    fraction of the isotropic sample agrees with the solid angle of the two
    cones, 1 - (1 - 1/R_m)^(1/2), within four binomial standard deviations."""
    import numpy as np
    import plot_loss_cone as model

    v_par, v_perp = model.sample(20_000, seed=5)
    sin2 = v_perp**2 / (v_par**2 + v_perp**2)
    for ratio in (1.5, 4.0, 10.0):
        assert np.array_equal(model.trapped(v_par, v_perp, ratio), sin2 >= 1 / ratio)
        lost = model.lost_fraction(ratio, n=50_000, seed=7)
        p = model.lost_formula(ratio)
        assert abs(lost - p) < 4 * np.sqrt(p * (1 - p) / 50_000), (ratio, lost, p)


def test_moment_weights_against_closed_form():
    """Quadrature of the plotted integrands gives the moments of the
    core-plus-beam distribution: n = 1, u = 0.2*2.5 = 0.5,
    k_B T/m = 0.8(1 + 0.5^2) + 0.2(0.6^2 + 2^2) = 1.872 and
    q/m = [0.8(-0.5^3 - 1.5) + 0.2(2^3 + 6*0.36)]/2 = 0.366 (by hand)."""
    import plot_moment_weights as model

    got = model.numerical_moments()
    for a, b, hand in zip(got, model.analytic_moments(), (1.0, 0.5, 1.872, 0.366)):
        assert abs(a - b) < 1e-8 and abs(b - hand) < 1e-12, (a, b, hand)


def test_spitzer_coefficient_from_collision_time():
    """NRL's eta_perp = 1.03e-2 Z lnL T^-3/2 Ohm cm (= 1.15e-14 s in Gaussian
    units, times 1/(4 pi eps_0)) equals m_e/(n e^2 tau_e) with the formulary's
    tau_e, and the plotted tokamak core is a better conductor than copper."""
    import math
    import plot_spitzer_resistivity as model

    assert abs(model.NRL_PERP / model.coefficient() - 1) < 0.005
    gaussian = 1.15e-14 / (4 * math.pi * 8.8541878128e-12)
    assert abs(gaussian / model.coefficient() - 1) < 0.005
    assert model.eta_par(1e20, 1e4) < model.COPPER < model.eta_par(1e20, 1e3)
    # T^-3/2 at fixed ln Lambda: one decade in T gives 10^-1.5 in eta.
    ratio = model.eta_perp(1e20, 1e4) / model.eta_perp(1e20, 1e3)
    lnl = model.coulomb_log(1e20, 1e4) / model.coulomb_log(1e20, 1e3)
    assert abs(ratio / lnl - 10**-1.5) < 1e-12

CHAPTERS =sorted((Path(__file__).parent / "chapters").glob("ch*.py"))
LINE_REFERENCE = re.compile(r'\.typ:\d|"\d*:\d+(?:-\d+)?"')


@pytest.mark.parametrize("path", CHAPTERS, ids=[p.stem for p in CHAPTERS])
def test_chapter(path):
    notebook.reset(echo=False)
    namespace = runpy.run_path(str(path), run_name="chapter")
    for name, fn in namespace.items():
        if name.startswith("test_") and callable(fn):
            fn()


@pytest.mark.parametrize("path", CHAPTERS, ids=[p.stem for p in CHAPTERS])
def test_no_line_references(path):
    hits = [f"{path.name}:{i}: {line.strip()}"
            for i, line in enumerate(path.read_text().splitlines(), 1)
            if LINE_REFERENCE.search(line)]
    assert not hits, "line-number references to the script:\n" + "\n".join(hits)


def _used(keyword):
    pattern = re.compile(rf'\b{keyword}="([^"]+)"')
    return {label for p in CHAPTERS for label in pattern.findall(p.read_text())}


def test_section_labels_exist():
    outline = json.loads(notebook.ensure_outline().read_text())
    known = {e["label"] for e in outline["chapters"] + outline["sections"]}
    assert _used("script") <= known, sorted(_used("script") - known)


@pytest.mark.skipif(not notebook.SRC.is_dir(), reason="no script sources (exported copy)")
def test_equation_labels_exist():
    defined = set()
    for path in notebook.SRC.rglob("*.typ"):
        defined.update(re.findall(r"<([A-Za-z0-9:_.-]+)>", path.read_text()))
    used = _used("eq")
    assert used, "no equation labels used"
    assert used <= defined, sorted(used - defined)
