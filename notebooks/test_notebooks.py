"""The browser physics of the notebooks (notebooks/plasma.js), run by node,
against the SymPy derivations of chapters 4 and 5, the mu-ramp model of the
lecture figure and the kernel-smoothing animation model."""

import json
import math
import os
import runpy
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
DERIVATIONS = ROOT / "derivations"
sys.path[:0] = [str(DERIVATIONS), str(DERIVATIONS / "chapters")]
NODE = shutil.which("node")
pytestmark = pytest.mark.skipif(NODE is None, reason="node runs notebooks/plasma.js")


def js(body):
    """Run `body` (an async function body with the module as P) in node; return its JSON result."""
    module = (ROOT / "notebooks" / "plasma.js").as_uri()
    code = (f"import * as P from {json.dumps(module)};\n"
            f"console.log(JSON.stringify(await (async () => {{ {body} }})()));")
    run = subprocess.run([NODE, "--input-type=module", "-e", code],
                         capture_output=True, text=True, check=True)
    return json.loads(run.stdout)


def chapter(name):
    """Namespace of a chapter derivation, run from derivations/ as the Makefile does."""
    import notebook

    notebook.ensure_outline()
    cwd = os.getcwd()
    os.chdir(DERIVATIONS)
    try:
        return runpy.run_path(str(DERIVATIONS / "chapters" / name), run_name="chapter")
    finally:
        os.chdir(cwd)


@pytest.fixture(scope="module")
def ch04():
    return chapter("ch04_debye_shielding.py")


@pytest.fixture(scope="module")
def ch05():
    return chapter("ch05_single_particle_motion.py")


def test_constants_and_example_plasmas():
    import si
    from notebook import PROTON_MASS
    from sympy.physics import units as u

    constants = js("return [P.SI, P.EXAMPLE_PLASMAS];")
    values, examples = constants
    for name in ("e", "m_e", "eps0", "k_B"):
        assert values[name] == si.SI_VALUES[getattr(si, name)], name
    assert values["m_p"] == float(PROTON_MASS / u.kilogram)
    assert {d["name"]: (d["n"], d["T_eV"]) for d in examples} == si.EXAMPLE_PLASMAS


def test_scales_against_chapter_4_and_5(ch04, ch05):
    """lambda_D, omega_pe, N_D of the deck table; Gamma, regime lines, gyration table."""
    rows = js("return P.EXAMPLE_PLASMAS.map((d) => P.scales(d.n, d.T_eV, 1));")
    for reference, row in zip(ch04["scale_examples"], rows):
        for key in ("lambda_D", "omega_pe", "N_D"):
            assert row[key] == pytest.approx(reference[key], rel=1e-12), (reference["name"], key)
    numeric, n0, T_e, L = ch04["numeric"], ch04["n0"], ch04["T_e"], ch04["L"]
    gamma = numeric(ch04["coupling"].subs(ch04["a"], ch04["a_expr"]), n0, T_e)
    kelvin_per_eV = ch04["kelvin_per_eV"]
    line_L, line_1 = numeric(ch04["T_line_L"], n0, L), numeric(ch04["T_line_1"], n0)
    got = js("return [1e9, 1e20, 1e28].map((n) => [P.coupling(n, 30), P.temperatureForDebyeLength(n, 1e-3),"
             " P.temperatureForUnitDebyeNumber(n), P.coupling(n, 30) * P.debyeNumber(n, 30) ** (2 / 3)]);")
    for n, (g, tl, t1, product) in zip([1e9, 1e20, 1e28], got):
        assert g == pytest.approx(float(gamma(n, 30 * kelvin_per_eV)), rel=1e-12)
        assert tl == pytest.approx(float(line_L(n, 1e-3)), rel=1e-12)
        assert t1 == pytest.approx(float(line_1(n)), rel=1e-12)
        assert product == pytest.approx((36 * math.pi) ** (-1 / 3), rel=1e-12)
    for reference in ch05["gyration_table"]:
        mass = "m_e" if reference["species"] == "e" else "m_p"
        row = js(f"return P.gyroScales(P.SI.{mass}, {reference['B']}, {reference['T_eV']});")
        for key in ("omega", "f", "v", "rho_L"):
            assert row[key] == pytest.approx(reference[key], rel=1e-12)


def test_screening_against_chapter_4(ch04):
    r, k, lam, Q, eps0 = ch04["r"], ch04["kw"], ch04["lambda_D"], ch04["Q"], ch04["eps0"]
    values = {Q: 1.602176634e-19, eps0: 8.8541878128e-12, lam: 7.4e-5}
    screened = sp.lambdify(r, ch04["screened"].subs(values))
    bare = sp.lambdify(r, ch04["bare"].subs(values))
    epsilon = sp.lambdify(k, ch04["epsilon_k"].subs(values))
    surviving = sp.lambdify(k, ch04["surviving"].subs(values))
    radii, waves = [1e-6, 7.4e-5, 3e-4], [1e3, 1 / 7.4e-5, 1e7]
    got = js(f"return [{radii}.map((r) => [P.screenedPotential(r, 7.4e-5), P.coulombPotential(r)]),"
             f" {waves}.map((k) => [P.dielectric(k, 7.4e-5), P.survivingFraction(k, 7.4e-5)])];")
    for x, (phi, phi_bare) in zip(radii, got[0]):
        assert phi == pytest.approx(screened(x), rel=1e-12)
        assert phi_bare == pytest.approx(bare(x), rel=1e-12)
    for x, (eps, frac) in zip(waves, got[1]):
        assert eps == pytest.approx(epsilon(x), rel=1e-12)
        assert frac == pytest.approx(surviving(x), rel=1e-12)
    assert got[1][1][1] == pytest.approx(0.5, rel=1e-12)


def drift_case(config, sign, **params):
    p = {"sign": sign, "vpar": 0.5, "turns": 40, "E": 0, "g": 0, "kappa": 0, "R0": 30, "L": 30, "Rm": 4, **params}
    return js(f"const p = {json.dumps(p)}; const o = P.pushOrbit({json.dumps(config)}, p);"
              f" return {{measured: o.drift, formula: P.analyticDrift({json.dumps(config)}, p), lost: o.lost,"
              f" zMax: o.zMax, mirror: P.mirrorPrediction(p)}};")


@pytest.mark.parametrize("sign", [1, -1])
def test_boris_drifts_against_chapter_5(ch05, sign):
    """Measured guiding-centre drift of the Boris orbit and the notebook formula
    against the drift formulas derived in chapter 5 (normalized m = B_0 = v_perp = 1)."""
    E, B, q, mu, G = ch05["E"], ch05["B"], ch05["q"], ch05["mu"], ch05["G"]
    expected = {
        "exb": (ch05["exb"].subs({E[0]: 0.2, E[1]: 0, B: 1}), {"E": 0.2}, 1e-6),
        "gravity": (ch05["v_grav"](1, sign).subs({**dict(zip(ch05["g_v"], (0.2, 0, 0))), ch05["B_d"]: 1}),
                    {"g": 0.2}, 1e-6),
        "gradb": (ch05["grad_B_drift"].subs({mu: sp.Rational(1, 2), G[0]: 0.02, G[1]: 0, G[2]: 0, q: sign, B: 1}),
                  {"kappa": 0.02}, 0.01),
        "curvature": (ch05["v_sum"].subs({ch05["m_a"]: 1, ch05["q_a"]: sign, ch05["B_d"]: 1, ch05["Rc_d"]: 50,
                                          ch05["vpar_d"]: sp.Rational(1, 2), ch05["vp_d"]: 1,
                                          ch05["mu_s"]: sp.Rational(1, 2)}),
                      {"R0": 50}, 0.02),
    }
    for config, (formula, params, rtol) in expected.items():
        formula = [float(c) for c in formula]
        case = drift_case(config, sign, **params)
        # Curvature: chapter 5 places the start at (R_c, 0, 0) with e_R x b = e_z.
        components = [0, 2] if config == "curvature" else [0, 1]
        for i in components:
            assert case["formula"][i] == pytest.approx(formula[i], abs=1e-15), (config, i)
        size = max(abs(formula[i]) for i in components)
        for i in components:
            assert abs(case["measured"][i] - formula[i]) <= rtol * size, (config, i, case["measured"], formula)


def test_mirror_against_chapter_5(ch05):
    loss_cone = float(ch05["loss_cone"].subs({ch05["B_0"]: 1, ch05["B_max"]: 4}))
    boundary = 1 / math.tan(loss_cone)                     # v_par/v_perp at the loss-cone edge
    trapped = drift_case("mirror", 1, vpar=0.9 * boundary)
    lost = drift_case("mirror", 1, vpar=1.1 * boundary)
    assert trapped["mirror"]["lossConeDeg"] == pytest.approx(math.degrees(loss_cone), rel=1e-12)
    assert trapped["mirror"]["trapped"] and not trapped["lost"]
    assert not lost["mirror"]["trapped"] and lost["lost"]
    # Mirror point B(z_m) = B_0/sin^2(alpha): the measured turning point agrees.
    assert trapped["zMax"] == pytest.approx(trapped["mirror"]["z_m"], rel=0.02)


def test_mu_ramp_against_lecture_model():
    import plot_mu_ramp

    got = js("return [1, 8].map((tau) => P.muRamp(tau, 200).deltaMu);")
    for tau, value in zip([1.0, 8.0], got):
        reference = float(plot_mu_ramp.boris([tau], True, steps_per_turn=200)[0])
        assert value == pytest.approx(reference, rel=1e-6, abs=1e-14), tau
    # Lecture figure (1600 steps per turn): 3.0e-2 at |omega_c0| tau = 1, 2.0e-11 at 8.
    fine = js("return [1, 8].map((tau) => P.muRamp(tau, 1600).deltaMu);")
    assert fine[0] == pytest.approx(3.0e-2, rel=0.02)
    assert fine[1] == pytest.approx(2.0e-11, rel=0.02)


def test_kernel_smoothing_against_animation_model():
    """x/L and h/L of the notebook are x/Delta and h/Delta of the animation over L = 80 Delta."""
    from scipy.integrate import quad

    model = runpy.run_path(str(ROOT / "scripts" / "check-physics.py"), run_name="notebook_test")["model"]
    m = model("kernel_smoothing.py")
    scale = m["DOMAIN"]
    xs = np.linspace(0, 1, 41)
    particles = np.random.default_rng(3).uniform(0, 1, 50)
    got = js(f"const xs = {xs.tolist()}, h = [0.01, 0.05, 0.2];"
             f" return {{truth: xs.map(P.trueDensity),"
             f" expected: h.map((w) => xs.map((x) => P.expectedSmoothed(x, w))),"
             f" tophat: h.map((w) => xs.map((x) => P.expectedSmoothed(x, w, 'tophat'))),"
             f" noise: h.map((w) => P.noiseRms(w, 80)), bias: h.map((w) => P.biasRms(w)),"
             f" smoothed: P.smoothed(xs, {particles.tolist()}, 0.03, 'gaussian', 80)}};")
    np.testing.assert_allclose(got["truth"], m["true_density"](scale * xs), rtol=1e-12)
    for j, h in enumerate([0.01, 0.05, 0.2]):
        np.testing.assert_allclose(got["expected"][j], m["smoothed_truth"](scale * xs, scale * h), rtol=1e-12)
        assert got["noise"][j] == pytest.approx(m["noise_theory"](scale * h), rel=1e-12)
        assert got["bias"][j] == pytest.approx(m["bias_rms"](scale * h), rel=1e-12)
        # Top hat: closed form against quadrature of (1/2h) int_{x-h}^{x+h} n.
        for x, value in zip(xs[::8], got["tophat"][j][::8]):
            integral = quad(lambda y: float(m["true_density"](np.array([scale * y]))[0]), x - h, x + h,
                            limit=200)[0]
            assert value == pytest.approx(integral / (2 * h), rel=1e-6)
    np.testing.assert_allclose(got["smoothed"], m["smoothed"](scale * xs, scale * particles, scale * 0.03),
                               rtol=1e-10)
