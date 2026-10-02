"""Independent numerical checks of the models actually used by the scenes.

Load production numerical functions without importing Manim or rendering.
The oracles are conservation laws, differential equations and independent
quadrature, rather than matching source strings or stored expected arrays.
"""

import ast
import math
from pathlib import Path
import unittest

import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def model(filename):
    """Execute only module-level numerical functions and literal constants."""
    path = ROOT / "animations" / filename
    tree = ast.parse(path.read_text(), filename=str(path))
    namespace = {"np": np, "math": math, "PI": np.pi, "TAU": 2 * np.pi}
    nodes = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            nodes.append(node)
        elif isinstance(node, ast.Assign):
            try:
                ast.literal_eval(node.value)
            except (ValueError, TypeError):
                continue
            nodes.append(node)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), "exec"), namespace)
    return namespace


class DebyePhysics(unittest.TestCase):
    def setUp(self):
        self.sphere = model("debye_potential.py")

    def test_bare_sphere_gauss_law_and_matching(self):
        potential = self.sphere["_uniform_sphere_potential"]
        radius = 0.5
        h = 1e-5
        for r in (0.12, 0.3, 0.8, 1.6):
            field = -(potential(r + h) - potential(r - h)) / (2 * h)
            enclosed = min((r / radius) ** 3, 1.0)
            self.assertAlmostEqual(float(field * r * r), enclosed, places=7)
        self.assertAlmostEqual(float(potential(0)), 3 / (2 * radius))
        self.assertAlmostEqual(float(potential(radius)), 1 / radius)

    def test_screened_sphere_yukawa_convolution(self):
        # Independently sum screened point-source kernels over the source
        # volume, including the angular integral, instead of using matching
        # coefficients from the implementation.
        p = self.sphere["_screened_sphere_potential"]
        nodes, weights = np.polynomial.legendre.leggauss(240)
        radius = 0.5
        s = radius * (nodes + 1) / 2
        radial_weight = weights * radius / 2
        rho = 3 / (4 * np.pi * radius**3)
        for r in (0.0, 0.17, 0.37, 0.7, 1.4, 3.0):
            distance = np.sqrt(r*r + s[:, None]**2 - 2*r*s[:, None]*nodes)
            kernel = np.exp(-distance) / distance
            expected = 2*np.pi*rho*np.sum(radial_weight*s*s*(kernel @ weights))
            self.assertAlmostEqual(float(p(r)), float(expected), delta=2e-4)

    def test_screened_poisson_and_boundary(self):
        p = self.sphere["_screened_sphere_potential"]
        radius = 0.5
        h = 2e-4
        for r in (0.08, 0.3, 0.8, 2.0):
            d1 = (p(r+h)-p(r-h))/(2*h)
            d2 = (p(r+h)-2*p(r)+p(r-h))/h**2
            residual = d2 + 2*d1/r - p(r)
            expected = -3/radius**3 if r < radius else 0
            self.assertAlmostEqual(float(residual), expected, delta=2e-5)
        left = (p(radius)-p(radius-h))/h
        right = (p(radius+h)-p(radius))/h
        self.assertAlmostEqual(float(left), float(right), delta=0.003)
        r = np.linspace(0, 4, 101)
        self.assertTrue(np.all(p(r) > 0))
        self.assertTrue(np.all(p(r) < self.sphere["_uniform_sphere_potential"](r)))

    def test_permeable_source_has_interior_electrons(self):
        # Same marker parameters as the scene; the check is geometric and
        # does not interpret illustrative marker density as a field solver.
        initial = self.sphere["_scattered_annulus_positions"](
            64, seed=20260917, inner_radius=0, outer_radius=1.48,
            minimum_separation=0.13,
        )
        final = self.sphere["_screening_targets"](initial)
        self.assertTrue(np.any(np.linalg.norm(initial, axis=1) < 0.5))
        self.assertTrue(np.any(np.linalg.norm(final, axis=1) < 0.5))
        self.assertTrue(np.all(np.linalg.norm(final, axis=1) < np.linalg.norm(initial, axis=1)))

    def test_periodic_poisson_sign(self):
        m = model("debye_shielding.py")
        x = np.linspace(0, 2*np.pi, 128, endpoint=False)
        k = 2*np.pi*np.fft.fftfreq(len(x), d=x[1]-x[0])
        charge = np.cos(3*x)
        potential = m["_potential"](charge, k)
        np.testing.assert_allclose(potential, charge/9, atol=1e-14)
        laplacian = m["_derivative"](m["_derivative"](potential, k), k)
        np.testing.assert_allclose(laplacian, -charge, atol=1e-12)


class MotionPhysics(unittest.TestCase):
    def test_exb_orbit_satisfies_lorentz_force(self):
        p = model("exb_drift.py")["particle_position"]
        h = 1e-4
        for tau in (0.0, 0.4, 1.2, 2.7):
            velocity = (p(tau+h)-p(tau-h))/(2*h)
            acceleration = (p(tau+h)-2*p(tau)+p(tau-h))/h**2
            # Positive q, B along +z, E along +y: Omega=2,
            # guiding-center drift 0.55 => electric acceleration 1.1.
            force = [2*velocity[1], 1.1-2*velocity[0]]
            np.testing.assert_allclose(acceleration, force, atol=1e-7)

    def test_slab_field_and_force_signs(self):
        state = model("plasma_oscillation.py")["slab_state"]
        for tau in (0.0, 0.7, np.pi/2, 2.0, np.pi):
            xi, field, force = state(tau)
            self.assertAlmostEqual(field, xi)  # Gauss's law (SI): E=e n xi/epsilon_0.
            self.assertAlmostEqual(force, -field)  # Electron q=-e.
            h = 1e-4
            acceleration = (state(tau+h)[0]-2*xi+state(tau-h)[0])/h**2
            self.assertAlmostEqual(acceleration, force, delta=3e-8)

    def test_sheath_energy_and_flux(self):
        m = model("sheath_formation.py")
        b = m["barrier"]
        edge, mach, curvature = m["EDGE"], m["MACH"], m["CURVATURE"]
        h = 1e-5
        for tau in (0.1, 0.5, 1.0, 1.8):
            x = m["electron_position"](tau)
            v = (m["electron_position"](tau+h)-m["electron_position"](tau-h))/(2*h)
            self.assertAlmostEqual(v*v/2+b(x), m["ELECTRON_ENERGY"], places=8)
        wall_time = np.arcsinh(edge*np.sqrt(2*curvature)/mach)/np.sqrt(2*curvature)
        self.assertAlmostEqual(m["ion_position"](wall_time), 0, places=12)
        for tau in (0.1, 0.5, 1.0):
            x = m["ion_position"](tau)
            v = (m["ion_position"](tau+h)-m["ion_position"](tau-h))/(2*h)
            self.assertAlmostEqual(v*v/2-b(x), mach*mach/2, places=8)
            ne, ni = m["sheath_densities"](x)
            self.assertGreater(ni, ne)
            self.assertAlmostEqual(ni*abs(v), mach, places=8)

    def test_probe_continuity_and_floating_current(self):
        current = model("langmuir_probe.py")["probe_current"]
        self.assertAlmostEqual(current(np.log(0.058)), 0, places=14)
        self.assertAlmostEqual(current(-1e-9), current(1e-9), delta=2e-9)
        self.assertGreater(current(-8), 0)
        self.assertAlmostEqual(current(2), current(0))

    def test_landau_characteristic_and_wave_frame_energy(self):
        m = model("landau_resonance.py")
        t, states = m["integrate_landau"](duration=8, dt=0.005)
        x, v = states.T
        dx = np.gradient(x, t)
        np.testing.assert_allclose(dx[1:-1], v[1:-1], atol=2e-6)
        # Conserved energy for an electron in a constant-amplitude
        # prescribed traveling wave, not conservation of lab energy.
        energy = (v-0.92)**2/2 - 0.18*np.cos(x-0.92*t)
        self.assertLess(np.ptp(energy), 1e-9)

    def test_faraday_superposition_fixed_axis_at_fixed_z(self):
        modes = model("magnetized_polarization.py")["circular_modes"]
        for z in (0.0, 0.7, 3.2):
            theta = (1.2-0.8)*z/2
            axis = np.array([np.cos(theta), np.sin(theta)])
            for tau in (0, 0.8, 2.5, 5):
                plus, minus, total = modes(z, tau)
                np.testing.assert_allclose(total, plus+minus, atol=1e-14)
                self.assertAlmostEqual(total[0]*axis[1]-total[1]*axis[0], 0, places=14)
                np.testing.assert_allclose(total, np.cos(z-tau)*axis, atol=1e-14)

    def test_mhd_geometry_and_speeds(self):
        m = model("magnetosonic_waves.py")
        phase, displacement = m["wave_phase"], m["shear_displacement"]
        h, x, y, tau = 1e-5, 0.7, -0.3, 1.2
        div = ((displacement(x+h,y,tau)[0]-displacement(x-h,y,tau)[0])
               +(displacement(x,y+h,tau)[1]-displacement(x,y-h,tau)[1]))/(2*h)
        self.assertAlmostEqual(div, 0)
        speeds = {}
        for mode in ("sound", "shear", "fast"):
            k = (phase(x+h,tau,mode)-phase(x-h,tau,mode))/(2*h)
            omega = -(phase(x,tau+h,mode)-phase(x,tau-h,mode))/(2*h)
            speeds[mode] = omega/k
        self.assertAlmostEqual(speeds["fast"]**2, speeds["sound"]**2+speeds["shear"]**2, places=9)

    def test_two_stream_root_and_pure_growth(self):
        m = model("two_stream_instability.py")
        for k in (0.1, 0.3, 0.6, 0.9):
            gamma = m["growth_rate"](k)
            omega = 1j*gamma
            residual = 1 - .5/(omega-k)**2 - .5/(omega+k)**2
            self.assertLess(abs(residual), 1e-12)
            x = np.array([0.4, 1.3, 2.7])
            initial = m["two_stream_field"](x, 0, k)
            later = m["two_stream_field"](x, 1, k)
            np.testing.assert_allclose(later/initial, np.exp(gamma), atol=1e-14)
        self.assertAlmostEqual(m["growth_rate"](np.sqrt(3/8)), 1/(2*np.sqrt(2)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
