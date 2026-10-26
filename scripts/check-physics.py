"""Independent numerical checks of the models actually used by the scenes.

Load production numerical functions without importing Manim or rendering.
The oracles are conservation laws, differential equations and independent
quadrature, rather than matching source strings or stored expected arrays.
"""

import ast
import json
import math
from pathlib import Path
import runpy
import unittest

import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def model(filename):
    """Execute numerical functions and their globals without importing Manim."""
    path = ROOT / "animations" / filename
    tree = ast.parse(path.read_text(), filename=str(path))
    namespace = {"np": np, "math": math, "PI": np.pi, "TAU": 2 * np.pi}
    if any(isinstance(node, ast.ImportFrom) and node.module == "kin6d_data" for node in tree.body):
        namespace["Export"] = runpy.run_path(str(ROOT / "animations/kin6d_data.py"))["Export"]
    for node in tree.body:
        # Numerical names imported from another scene module.
        if isinstance(node, ast.ImportFrom) and node.module and \
                (ROOT / "animations" / (node.module + ".py")).is_file() and \
                node.module not in ("style", "kin6d_data"):
            source = model(node.module + ".py")
            namespace.update({a.asname or a.name: source[a.name] for a in node.names
                              if a.name in source})
    numerical_names = set(namespace)
    nodes = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            nodes.append(node)
        elif isinstance(node, ast.Assign):
            try:
                ast.literal_eval(node.value)
            except (ValueError, TypeError):
                referenced = {n.id for n in ast.walk(node.value) if isinstance(n, ast.Name)}
                if not referenced <= numerical_names:
                    continue
            nodes.append(node)
            numerical_names.update(t.id for t in node.targets if isinstance(t, ast.Name))
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), "exec"), namespace)
    return namespace


class DebyePhysics(unittest.TestCase):
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
        scene = model("plasma_oscillation.py")
        state = scene["slab_state"]
        data, times = scene["DATA"], scene["TAU"]
        # The scene interpolates float32 samples. Its error is bounded by the
        # certified trajectory radius plus the cosine chord error, h²/8.
        tolerance = data.parameters["residual_radius"] + np.max(np.diff(times))**2 / 8 + 2e-6
        for tau in (0.0, 0.7, np.pi/2, 2.0, np.pi):
            xi, field, force = state(tau)
            self.assertAlmostEqual(field, xi)  # Gauss's law (SI): E=e n xi/epsilon_0.
            self.assertAlmostEqual(force, -field)  # Electron q=-e.
            self.assertAlmostEqual(xi, math.cos(tau), delta=tolerance)
        oracle = np.cos(times)
        self.assertTrue(np.all(data["q_lower"] - 2e-7 <= oracle))
        self.assertTrue(np.all(oracle <= data["q_upper"] + 2e-7))

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


def lorentz_rk4(sign, v0, theta_max, steps, omega=1.0):
    """Integrate dv/dt = (q/m) v x B e_z with omega_c = 1, B along +z (RK4)."""
    def rhs(state):
        x, y, z, vx, vy, vz = state
        return np.array([vx, vy, vz, sign*omega*vy, -sign*omega*vx, 0.0])
    h = theta_max/steps
    state = np.array([0.0, 0.0, 0.0, *v0])
    out = [state]
    for _ in range(steps):
        k1 = rhs(state)
        k2 = rhs(state + h/2*k1)
        k3 = rhs(state + h/2*k2)
        k4 = rhs(state + h*k3)
        state = state + h/6*(k1 + 2*k2 + 2*k3 + k4)
        out.append(state)
    return np.linspace(0, theta_max, steps + 1), np.array(out)


class GyrationPhysics(unittest.TestCase):
    """animations/gyration.py and the gyration tables of slides/05."""

    E, ME, MP = 1.602176634e-19, 9.1093837015e-31, 1.67262192369e-27

    @classmethod
    def setUpClass(cls):
        cls.m = model("gyration.py")

    def test_orbit_solves_lorentz_force(self):
        orbit, velocity = self.m["gyro_orbit"], self.m["gyro_velocity"]
        for sign in (+1, -1):
            for phase in (0.0, 0.7):
                v0 = [*velocity(0.0, sign, 1.0, phase), 0.0]
                theta, s = lorentz_rk4(sign, v0, 6*np.pi, 6000)
                start = orbit(0.0, sign, 1.0, phase)
                x, y = orbit(theta, sign, 1.0, phase)
                np.testing.assert_allclose(s[:, 0], x - start[0], atol=1e-9)
                np.testing.assert_allclose(s[:, 1], y - start[1], atol=1e-9)
                vx, vy = velocity(theta, sign, 1.0, phase)
                np.testing.assert_allclose(s[:, 3], vx, atol=1e-9)
                np.testing.assert_allclose(s[:, 4], vy, atol=1e-9)

    def test_sense_of_rotation_is_diamagnetic(self):
        # B out of the page (+z): ions clockwise, electrons counterclockwise.
        # The orbit current's moment (q/2) r x v points against B for both.
        orbit, velocity = self.m["gyro_orbit"], self.m["gyro_velocity"]
        theta = np.linspace(0, 2*np.pi, 50)
        for sign in (+1, -1):
            x, y = orbit(theta, sign)
            vx, vy = velocity(theta, sign)
            l_z = x*vy - y*vx
            self.assertTrue(np.all(-sign*l_z > 0.999), sign)
            self.assertTrue(np.all(sign*l_z/2 < 0), sign)

    def test_top_view_ratios(self):
        m = self.m
        ratio = m["MASS_RATIO"]
        self.assertAlmostEqual(m["R_ION"]/m["R_ELECTRON"], np.sqrt(ratio))
        self.assertEqual(m["frequency_ratio"](), ratio)
        self.assertEqual(m["radius_ratio"](ratio), np.sqrt(ratio))
        # The video loops: the electron completes an integer number of turns.
        self.assertEqual((ratio*m["ION_TURNS"]) % 1, 0)
        # Equal temperature: r_L = sqrt(2 m k T)/(|q| B), omega_c = |q| B/m.
        kT, B = 1.0, 1.0
        r = lambda mass: np.sqrt(2*mass*kT)/B
        self.assertAlmostEqual(r(ratio)/r(1.0), m["radius_ratio"](ratio))

    def test_helix_pitch_matches_parallel_motion(self):
        m = self.m
        pitch = m["HELIX_PITCH"]
        v_par = pitch/(2*np.pi)
        v0 = [*m["gyro_velocity"](0.0, +1), v_par]
        theta, s = lorentz_rk4(+1, v0, 6*np.pi, 6000)
        p = m["helix_point"](theta, +1)
        start = m["helix_point"](0.0, +1)
        np.testing.assert_allclose(s[:, :3], (p.T - start), atol=1e-9)
        self.assertAlmostEqual(p[2][-1] - p[2][0], 3*pitch)

    def boris_radius_period(self, mass, B, energy_ev):
        """SI Boris push of one gyration: radius and period from the orbit itself."""
        v = np.sqrt(2*energy_ev*self.E/mass)
        omega = self.E*B/mass
        dt = 2*np.pi/omega/4000
        x, vel = np.zeros(2), np.array([v, 0.0])
        xs, crossings = [], []
        t = 0.0
        for _ in range(8200):
            tq = self.E*B/mass*dt/2
            s = 2*tq/(1 + tq**2)
            v_prime = vel + tq*np.array([vel[1], -vel[0]])
            new = vel + s*np.array([v_prime[1], -v_prime[0]])
            if vel[1] < 0 <= new[1] or vel[1] > 0 >= new[1]:
                crossings.append(t)
            vel = new
            x = x + vel*dt
            t += dt
            xs.append(x.copy())
        xs = np.array(xs)
        radius = (xs[:, 0].max() - xs[:, 0].min())/2
        period = crossings[2] - crossings[0]
        return radius, period

    def test_typical_parameters_and_slide_table(self):
        path = ROOT/"derivations/build/gyration.json"
        table = json.loads(path.read_text())["table"] if path.is_file() else None
        rows = {}
        for species, mass in (("e", self.ME), ("p", self.MP)):
            for B in (1.0, 5.0):
                for T in (10.0, 1e4):
                    r, period = self.boris_radius_period(mass, B, T)
                    f_c = self.E*B/(2*np.pi*mass)
                    r_l = np.sqrt(2*T*self.E/mass)*mass/(self.E*B)
                    self.assertAlmostEqual(r/r_l, 1, delta=1e-4)
                    self.assertAlmostEqual(1/(period*f_c), 1, delta=1e-3)
                    rows[species, B, T] = (f_c, r_l)
        # Electron 1 T: f_ce = 28.0 GHz; proton 1 T: 15.2 MHz.
        self.assertAlmostEqual(rows["e", 1.0, 10.0][0]/2.7992e10, 1, delta=1e-3)
        self.assertAlmostEqual(rows["p", 1.0, 10.0][0]/1.5245e7, 1, delta=1e-3)
        self.assertAlmostEqual(rows["e", 1.0, 10.0][1]/1.066e-5, 1, delta=2e-3)
        self.assertAlmostEqual(rows["p", 5.0, 1e4][1]/2.889e-3, 1, delta=2e-3)
        if table is not None:
            for row in table:
                f_c, r_l = rows[row["species"], row["B"], row["T_eV"]]
                self.assertAlmostEqual(row["f"]/f_c, 1, delta=1e-6)
                self.assertAlmostEqual(row["rho_L"]/r_l, 1, delta=1e-6)


class DriftOrbitPhysics(unittest.TestCase):
    """animations/drift_models.py (grad-B, toroidal curvature, mirror scenes).

    Oracle: an independent RK4 integration of the Lorentz force and, for the
    drift, a boxcar average of the position over one gyroperiod, not the
    guiding-centre formula used by the scenes.
    """

    @classmethod
    def setUpClass(cls):
        cls.m = model("drift_models.py")

    @staticmethod
    def rk4(field, qm, x0, v0, dt, steps):
        def rhs(s):
            return np.concatenate([s[3:], qm*np.cross(s[3:], field(s[:3]))])
        s = np.concatenate([x0, v0])
        out = np.empty((steps + 1, 6))
        out[0] = s
        for i in range(steps):
            k1 = rhs(s)
            k2 = rhs(s + dt/2*k1)
            k3 = rhs(s + dt/2*k2)
            k4 = rhs(s + dt*k3)
            s = s + dt/6*(k1 + 2*k2 + 2*k3 + k4)
            out[i + 1] = s
        return out

    @staticmethod
    def averaged_slope(t, q, period, skip=1.5):
        """Slope of q averaged over one gyroperiod (centred boxcar)."""
        dt = t[1] - t[0]
        n = int(round(period/dt))
        box = np.convolve(q, np.ones(n)/n, mode="valid")
        tt = t[n//2:n//2 + len(box)]
        keep = (tt > skip*period) & (tt < tt[-1] - skip*period)
        return np.polyfit(tt[keep], box[keep], 1)[0]

    def test_grad_b_drift_matches_formula_and_flips_with_charge(self):
        m = self.m
        speeds = []
        for qm, v_perp in ((1.0, 1.0), (-16.0, 4.0)):
            omega = abs(qm)
            r_l = v_perp/omega
            dt = 2*np.pi/omega/200
            steps = int(10*2*np.pi/dt)
            x0 = np.array([-np.sign(qm)*r_l, 0.0, 0.0])
            out = self.rk4(m["grad_b_field"], qm, x0, np.array([0.0, v_perp, 0.0]), dt, steps)
            t = np.arange(steps + 1)*dt
            v_x = self.averaged_slope(t, out[:, 0], 2*np.pi/omega)
            # mu = m v_perp^2/(2B), v = mu (B x grad B)/(q B^3): independent of the scene formula
            expected = -(v_perp**2/(2*qm))*(1/m["GRAD_B_L"])
            self.assertAlmostEqual(v_x/expected, 1, delta=0.03)
            print(f"grad-B qm={qm:+g}: RK4 {v_x:+.5f} formula {expected:+.5f} ({100*(v_x/expected-1):+.2f}%)")
            speeds.append(v_x)
            # the scene's own Boris orbit agrees with the RK4 orbit
            t_b, _, _, centre = m["grad_b_orbit"](qm, v_perp, periods=10)
            self.assertAlmostEqual(m["drift_speed"](t_b, centre)[0]/v_x, 1, delta=0.03)
        self.assertLess(speeds[0], 0)
        self.assertGreater(speeds[1], 0)
        self.assertAlmostEqual(speeds[0]/-speeds[1], 1, delta=0.03)

    def test_toroidal_vertical_drift_separates_charges(self):
        m = self.m
        r0 = m["TORUS_R0"]
        drifts = []
        for qm, v in ((1.0, 1.0), (-16.0, 4.0)):
            omega = abs(qm)
            dt = 2*np.pi/omega/150
            steps = int(80/dt)
            b0 = m["torus_field"](np.array([r0, 0.0, 0.0]))
            v0 = np.array([0.0, v, v])
            x0 = np.array([r0, 0.0, 0.0]) - np.cross(v0, b0)/(qm*(b0 @ b0))
            out = self.rk4(m["torus_field"], qm, x0, v0, dt, steps)
            t = np.arange(steps + 1)*dt
            v_z = self.averaged_slope(t, out[:, 2], 2*np.pi/omega)
            # (m/q)(v_par^2 + v_perp^2/2)/(B R), B R = B_0 R_0 = r0 in these units
            expected = (v**2 + 0.5*v**2)/(qm*r0)
            self.assertAlmostEqual(v_z/expected, 1, delta=0.04)
            self.assertAlmostEqual(np.hypot(out[:, 0], out[:, 1]).mean()/r0, 1, delta=0.01)
            print(f"toroidal qm={qm:+g}: RK4 {v_z:+.5f} formula {expected:+.5f} ({100*(v_z/expected-1):+.2f}%)")
            drifts.append(v_z)
        self.assertGreater(drifts[0], 0)
        self.assertLess(drifts[1], 0)

    def test_mirror_loss_cone_and_adiabatic_invariant(self):
        m = self.m
        ratio, length = m["MIRROR_RATIO"], m["MIRROR_L"]
        self.assertAlmostEqual(m["loss_cone_angle"](), 30.0, places=6)
        for alpha, x_gc in zip(m["PITCH_DEG"], (-2, -1.2, -0.4, 0.4, 1.2, 2)):
            t, x, v, mu, lost = m["mirror_orbit"](alpha, x_gc, t_end=60.0)
            sin2 = np.sin(np.radians(alpha))**2
            self.assertEqual(lost, sin2 < 1/ratio, alpha)
            self.assertLess(abs(np.sum(v**2, axis=1) - 1).max(), 1e-9)       # |v| conserved
            if not lost:
                z_b = length*np.sqrt((1/sin2 - 1)/(ratio - 1))               # B(z_b) = B_0/sin^2
                self.assertAlmostEqual(np.abs(x[:, 2]).max()/z_b, 1, delta=0.03)
                self.assertLess(abs(mu - 1).max(), 0.01)


class FieldChangePhysics(unittest.TestCase):
    """animations/drift_models.py models with E or g (E x B frame change,
    gravity drift, polarization drift, mu in a growing field).

    Oracles: an independent RK4 integration with gyro-period averages, the
    drift formulas written out here, and the mu-ramp plot of the derivations.
    """

    @classmethod
    def setUpClass(cls):
        cls.m = model("drift_models.py")

    @staticmethod
    def rk4(accel, qm, x0, v0, dt, steps):
        """dv/dt = accel(t) + qm v x e_z in the (x, y) plane."""
        def rhs(t, s):
            a = accel(t)
            return np.array([s[2], s[3], a[0] + qm*s[3], a[1] - qm*s[2]])
        s = np.array([x0[0], x0[1], v0[0], v0[1]], float)
        out = np.empty((steps + 1, 4))
        out[0] = s
        for i in range(steps):
            t = i*dt
            k1 = rhs(t, s)
            k2 = rhs(t + dt/2, s + dt/2*k1)
            k3 = rhs(t + dt/2, s + dt/2*k2)
            k4 = rhs(t + dt, s + dt*k3)
            s = s + dt/6*(k1 + 2*k2 + 2*k3 + k4)
            out[i + 1] = s
        return np.arange(steps + 1)*dt, out

    @staticmethod
    def boxcar(t, q, period):
        n = int(round(period/(t[1] - t[0])))
        return t[n//2:n//2 + len(q) - n + 1], np.convolve(q, np.ones(n)/n, mode="valid")

    def test_exb_drift_and_circle_in_the_drift_frame(self):
        m = self.m
        e = m["EXB_E"]
        dt = 2*np.pi/400
        t, out = self.rk4(lambda s: (0.0, e), 1.0, (0.0, 1.0), (1.0 + e, 0.0), dt, 3*400)
        tt, xb = self.boxcar(t, out[:, 0], 2*np.pi)
        self.assertAlmostEqual(np.polyfit(tt, xb, 1)[0], e, delta=1e-6)       # E x B/B^2 = E e_x
        radius = np.hypot(out[:, 0] - e*t, out[:, 1])
        self.assertLess(abs(radius - 1).max(), 1e-6)
        t_s, x_s, _, v_d, frame = m["exb_orbit"]()
        omega = 2*np.arctan((t_s[1] - t_s[0])/2)/(t_s[1] - t_s[0])
        drift = m["fit_drift_and_gyration"](t_s, x_s, omega)
        self.assertAlmostEqual(drift[0], e, delta=1e-12)
        self.assertAlmostEqual(drift[1], 0, delta=1e-12)
        r = m["drift_frame_radius"](frame)
        self.assertLess((r.max() - r.min())/r.mean(), 1e-12)
        self.assertAlmostEqual(r.mean(), 1, delta=1e-4)                      # rho_L = u/omega_c to O(dt^2)
        print(f"ExB: RK4 drift {np.polyfit(tt, xb, 1)[0]:.8f}, Boris {drift[0]:.12f}, "
              f"drift-frame radius spread {(r.max() - r.min())/r.mean():.1e}")

    def test_gravity_drift_opposite_and_proportional_to_mass(self):
        m = self.m
        g = m["GRAVITY_G"]
        drifts = []
        for qm, v_perp in ((1.0, 1.0), (-16.0, 4.0)):
            omega = abs(qm)
            dt = 2*np.pi/omega/200
            steps = int(round(6*2*np.pi/dt))
            expected = -g/qm                     # (m/q) (g x B)/B^2, g = -g e_y, B = e_z
            # guiding centre at the origin: x = -(m/q) v_perp x e_z / ..., start on top
            t, out = self.rk4(lambda s: (0.0, -g), qm, (0.0, v_perp/omega), (np.sign(qm)*v_perp + expected, 0.0),
                              dt, steps)
            tt, xb = self.boxcar(t, out[:, 0], 2*np.pi/omega)
            measured = np.polyfit(tt, xb, 1)[0]
            self.assertAlmostEqual(measured/expected, 1, delta=2e-3)
            t_s, x_s, _ = m["gravity_orbit"](qm, v_perp, 6*2*np.pi)
            scene = m["averaged_drift"](t_s, x_s, 2*np.pi/omega)[0]
            self.assertAlmostEqual(scene/expected, 1, delta=2e-3)
            self.assertAlmostEqual(m["gravity_formula"](qm), expected, places=12)
            print(f"gravity qm={qm:+g}: RK4 {measured:+.6f} scene {scene:+.6f} formula {expected:+.6f}")
            drifts.append(measured)
        self.assertLess(drifts[0], 0)
        self.assertGreater(drifts[1], 0)
        self.assertAlmostEqual(-drifts[0]/drifts[1], 16, delta=0.05)

    def test_polarization_shift_follows_e(self):
        m = self.m
        e1, ramp, t_end = m["POL_E1"], m["POL_RAMP"], m["POL_T_END"]

        def e_of_t(s):
            return e1*0.5*(1 - np.cos(np.pi*min(s, ramp)/ramp))

        for qm, v_perp in ((1.0, 1.0), (-16.0, 4.0)):
            omega = abs(qm)
            dt = 2*np.pi/omega/150
            steps = int(round(t_end/dt))
            t, out = self.rk4(lambda s: (0.0, qm*e_of_t(s)), qm, (0.0, v_perp/omega), (np.sign(qm)*v_perp, 0.0),
                              dt, steps)
            tt, yb = self.boxcar(t, out[:, 1], 2*np.pi/omega)
            shift = yb[tt > ramp + np.pi/omega].mean()          # the guiding centre starts at y = 0
            expected = e1/qm                     # (m/(q B^2)) E_1
            self.assertAlmostEqual(shift/expected, 1, delta=5e-3)
            t_s, _, centre = m["pol_orbit"](qm, v_perp)
            scene = centre[t_s >= ramp, 1].mean()             # started about the origin
            self.assertAlmostEqual(scene/expected, 1, delta=5e-3)
            print(f"polarization qm={qm:+g}: RK4 shift {shift:+.5f} scene {scene:+.5f} formula {expected:+.5f}")

    def test_mu_ramp_scene_reuses_plot_numerics(self):
        m = self.m
        plot = runpy.run_path(str(ROOT/"derivations/plot_mu_ramp.py"))
        for tau in (1.0, 2.0):
            scene = m["mu_ramp_orbit"](tau=tau, half=8*tau + 40*np.pi, steps_per_turn=800)[4][-1] - 1
            reference = plot["boris"]([tau], True, steps_per_turn=800)[0]
            self.assertAlmostEqual(scene, reference, delta=1e-9)
        t, b, rho, flux, mu, xy = m["mu_ramp_orbit"]()
        b = b/b[0]
        self.assertLess(abs(mu - 1).max(), 1e-3)
        self.assertLess(abs(flux - 1).max(), 1e-3)
        self.assertAlmostEqual(rho[-1]*np.sqrt(b[-1]), 1, delta=1e-4)
        self.assertAlmostEqual(np.hypot(xy[-1, 0], xy[-1, 1]), rho[-1], delta=1e-12)
        print(f"mu ramp: max|mu-1| {abs(mu - 1).max():.1e}, max|flux-1| {abs(flux - 1).max():.1e}, "
              f"rho_end sqrt(B_end) - 1 {rho[-1]*np.sqrt(b[-1]) - 1:+.1e}")


class KernelSmoothingPhysics(unittest.TestCase):
    """animations/kernel_smoothing.py.

    Oracles: an FFT convolution of a fine particle histogram (and of the true
    density) with the Gaussian's Fourier transform, and a Monte Carlo with its
    own seed against the Poisson variance n_bar int K_h^2.
    """

    @classmethod
    def setUpClass(cls):
        cls.m = model("kernel_smoothing.py")
        cls.particles = cls.m["sample"](np.random.default_rng(cls.m["SEED"]))

    def fft_smooth(self, values, h):
        """Periodic convolution with exp(-k^2 h^2/2) on a uniform grid."""
        k = 2*np.pi*np.fft.fftfreq(len(values), d=self.m["DOMAIN"]/len(values))
        return np.real(np.fft.ifft(np.fft.fft(values)*np.exp(-0.5*(k*h)**2)))

    def test_sum_of_kernels_is_convolution_and_keeps_particle_number(self):
        m, p = self.m, self.particles
        cells = 2**14
        dx = m["DOMAIN"]/cells
        x = (np.arange(cells) + 0.5)*dx
        hist = np.bincount((p/dx).astype(int), minlength=cells)/dx
        for h in (0.5, 1.5, 20.0):
            direct = m["smoothed"](x, p, h)
            self.assertAlmostEqual(direct.sum()*dx/len(p), 1, delta=1e-9)
            ref = self.fft_smooth(hist, h)
            # the histogram puts particles at cell centres: error ~ dx/h
            self.assertLess(abs(direct - ref).max()/direct.max(), 3*dx/h)

    def test_expected_density_and_spike_limit(self):
        m = self.m
        cells = 4096
        x = (np.arange(cells) + 0.5)*m["DOMAIN"]/cells
        for h in (0.5, 4.0, 20.0):
            ref = self.fft_smooth(m["true_density"](x), h)
            self.assertLess(abs(m["smoothed_truth"](x, h) - ref).max(), 1e-9)
        # h -> 0: each particle carries weight 1 in a narrow window around it
        p = self.particles
        gaps = np.diff(np.r_[p[-1] - m["DOMAIN"], p, p[0] + m["DOMAIN"]])
        i = int(np.argmax(np.minimum(gaps[:-1], gaps[1:])))     # most isolated
        xs = np.linspace(p[i] - 0.1, p[i] + 0.1, 2001)
        weight = np.trapezoid(m["smoothed"](xs, p, 0.01), xs)
        self.assertAlmostEqual(weight, 1, delta=1e-6)

    def test_noise_follows_poisson_variance(self):
        m = self.m
        rng = np.random.default_rng(99)
        x = np.linspace(0, m["DOMAIN"], 320, endpoint=False)
        widths = (0.5, 2.0, 8.0)
        sq = np.zeros(len(widths))
        runs = 400
        for _ in range(runs):
            p = m["sample"](rng)
            for j, h in enumerate(widths):
                sq[j] += np.mean((m["smoothed"](x, p, h) - m["smoothed_truth"](x, h))**2)
        for h, s2 in zip(widths, sq/runs):
            # n_bar int K_h^2 = 1/(2 sqrt(pi) h) for n_bar Delta = 1 (images negligible)
            self.assertAlmostEqual(np.sqrt(s2)*np.sqrt(2*np.sqrt(np.pi)*h), 1, delta=0.03)
            self.assertAlmostEqual(m["noise_theory"](h)*np.sqrt(2*np.sqrt(np.pi)*h), 1, delta=1e-6)
            print(f"kernel h={h:g}: noise {np.sqrt(s2):.4f}, 1/sqrt(2 sqrt(pi) h) {1/np.sqrt(2*np.sqrt(np.pi)*h):.4f}")


class PendulumEnsemblePhysics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = model("pendulum_ensemble.py")
        m = cls.m
        theta0, p0 = m["initial_blob"]()
        cls.mean_energy = float(np.mean(m["pendulum_energy"](theta0, p0)))
        cls.temperature = m["gibbs_temperature"](cls.mean_energy)
        cls.edges = np.linspace(0.0, 6.0, 49)
        centers = 0.5 * (cls.edges[1:] + cls.edges[:-1])
        cls.gibbs = m["gibbs_energy_density"](centers, cls.temperature)
        cls.times = np.linspace(0.0, 480.0, 97)  # the scene's time span

    def l1_to_gibbs(self, theta, p):
        hist = self.m["energy_histogram"](theta, p, self.edges)
        return float(np.sum(np.abs(hist - self.gibbs)) * (self.edges[1] - self.edges[0]))

    def test_collisionless_leapfrog_conserves_energy(self):
        m = self.m
        theta, p = m["simulate_ensemble"](0.0, self.times)
        energy = m["pendulum_energy"](theta, p)
        self.assertLess(np.max(np.abs(energy - energy[0])), 3e-3)
        self.assertLess(np.max(np.abs(energy.mean(axis=1) - energy[0].mean())), 1e-3)
        self.assertTrue(np.all((theta >= -np.pi) & (theta < np.pi)))

    def test_leapfrog_period_matches_density_of_states(self):
        # g(H) inside the separatrix is the orbit period; time two upward
        # zero crossings of p for a single librating pendulum.
        m = self.m
        for h in (0.3, 1.2, 1.7, 1.9):
            theta, p = np.array([0.0]), np.array([np.sqrt(2 * h)])
            dt, t, crossings, prev = 1e-3, 0.0, [], p[0]
            while len(crossings) < 3:
                theta, p = m["leapfrog_step"](theta, p, dt)
                t += dt
                if prev < 0 <= p[0]:
                    crossings.append(t - dt * p[0] / (p[0] - prev))
                prev = p[0]
            self.assertAlmostEqual(crossings[2] - crossings[1],
                                   float(m["density_of_states"](h)), delta=2e-3)

    def test_density_of_states_against_phase_space_area(self):
        # Independent oracle: dA/dH from uniform phase-space sampling.
        rng = np.random.default_rng(7)
        theta = rng.uniform(-np.pi, np.pi, 4_000_000)
        p = rng.uniform(-4.0, 4.0, theta.size)
        energy = self.m["pendulum_energy"](theta, p)
        edges = np.array([0.4, 0.6, 1.4, 1.6, 2.6, 2.8, 4.0, 4.2])
        counts, _ = np.histogram(energy, bins=edges)
        area = counts * (2 * np.pi * 8.0) / theta.size / np.diff(edges)
        for k in (0, 2, 4, 6):
            h = np.linspace(edges[k], edges[k + 1], 201)
            expected = np.mean(self.m["density_of_states"](h))
            self.assertAlmostEqual(area[k] / expected, 1.0, delta=0.02)

    def test_gibbs_temperature_matches_canonical_energy(self):
        # Independent 2D quadrature of <H> = int H exp(-H/T) / int exp(-H/T).
        theta = np.linspace(-np.pi, np.pi, 400, endpoint=False)
        p = np.linspace(-15, 15, 3001)
        energy = self.m["pendulum_energy"](theta[:, None], p[None, :])
        weight = np.exp(-energy / self.temperature)
        self.assertAlmostEqual(float(np.sum(energy * weight) / np.sum(weight)),
                               self.mean_energy, places=6)
        h = np.linspace(1e-6, 60, 600_001)
        density = self.m["gibbs_energy_density"](h, self.temperature)
        self.assertAlmostEqual(float(np.sum(density) * (h[1] - h[0])), 1.0, delta=2e-3)

    def test_kac_collision_conserves_pair_kinetic_energy(self):
        rng = np.random.default_rng(3)
        p = rng.standard_normal(10)
        first, second = np.array([0, 4, 7]), np.array([2, 9, 1])
        angle = rng.uniform(0, 2 * np.pi, 3)
        q = self.m["kac_collide"](p, first, second, angle)
        np.testing.assert_allclose(q[first]**2 + q[second]**2,
                                   p[first]**2 + p[second]**2, rtol=1e-14)
        untouched = np.setdiff1d(np.arange(10), np.concatenate([first, second]))
        np.testing.assert_array_equal(q[untouched], p[untouched])
        self.assertGreater(np.max(np.abs(q - p)), 0.1)

    def test_collisional_run_conserves_energy_and_reaches_gibbs(self):
        m = self.m
        theta, p = m["simulate_ensemble"](m["NU_STRONG"], self.times)
        energy = m["pendulum_energy"](theta, p).mean(axis=1)
        self.assertLess(np.max(np.abs(energy - self.mean_energy)), 1e-3)
        late = self.times >= 40
        l1 = [self.l1_to_gibbs(a, b) for a, b in zip(theta[late], p[late])]
        self.assertLess(np.mean(l1), 0.15)
        self.assertLess(np.max(l1), 0.25)
        self.assertGreater(self.l1_to_gibbs(theta[0], p[0]), 1.2)

    def test_weak_run_stays_non_gibbs_at_mid_animation(self):
        m = self.m
        theta, p = m["simulate_ensemble"](m["NU_WEAK"], self.times)
        mid = int(np.searchsorted(self.times, 240.0))
        self.assertGreater(self.l1_to_gibbs(theta[mid], p[mid]), 0.6)
        # The band at the initial energies is still there, and relaxation
        # has begun by the end of the scene.
        energy = m["pendulum_energy"](theta, p)
        band = np.abs(energy - self.mean_energy) < 0.3
        self.assertGreater(band[mid].mean(), 0.5)
        self.assertLess(self.l1_to_gibbs(theta[-1], p[-1]),
                        self.l1_to_gibbs(theta[0], p[0]) - 0.5)


class CollectiveResponsePhysics(unittest.TestCase):
    def setUp(self):
        self.m = model("collective_response.py")

    def test_screened_force_is_minus_gradient_of_potential(self):
        force = self.m["screened_force"]
        h = 1e-6
        for eps in (0.0, 0.12):
            def energy(p):
                r_s = math.sqrt(p[0]**2 + p[1]**2 + eps**2)
                return -math.exp(-r_s) / r_s
            for p in ((0.3, -0.4), (1.1, 0.7), (-2.0, 0.5)):
                grad = [(energy((p[0] + h, p[1])) - energy((p[0] - h, p[1]))) / (2*h),
                        (energy((p[0], p[1] + h)) - energy((p[0], p[1] - h))) / (2*h)]
                np.testing.assert_allclose(force(np.array(p), eps), -np.array(grad), rtol=1e-6)

    def test_straight_pass_impulse_is_two_k1(self):
        # Yukawa impulse in the straight-line limit: dv = 2 K_1(b) for unit
        # coupling and speed; K_1 from its integral representation.
        s = np.linspace(0, 12, 40001)
        for b in (0.5, 1.0, 2.0):
            k1 = np.trapezoid(np.exp(-b*np.cosh(s))*np.cosh(s), s)
            coupling = 1e-5
            _, _, vel = self.m["plasma_test_path"](np.array([[0.0, b]]), start=(-30.0, 0.0),
                                                   duration=60.0, dt=0.002,
                                                   coupling=coupling, softening=0.0)
            self.assertAlmostEqual(vel[1] / coupling / (2*k1), 1.0, places=3)
            self.assertLess(abs(vel[0] - 1.0), 1e-6)

    def test_hard_sphere_events_conserve_and_do_not_overlap(self):
        m = self.m
        positions = m["particle_positions"]()
        contact = m["CONTACT"]
        events = m["hard_sphere_events"](positions)
        self.assertGreaterEqual(len(events), 2)
        pos, vel, t0 = np.array(m["GAS_START"]), np.array([1.0, 0.0]), 0.0
        struck = set()
        for (t, p, v_after, j, v_neutral) in events:
            # Straight flight with no contact with any resting sphere.
            for frac in np.linspace(0, 1, 400)[:-1]:
                q = pos + frac*(t - t0)*vel
                rest = [k for k in range(len(positions)) if k not in struck]
                self.assertGreaterEqual(np.min(np.linalg.norm(positions[rest] - q, axis=1)),
                                        contact - 1e-9)
            np.testing.assert_allclose(pos + (t - t0)*vel, p, atol=1e-12)
            self.assertAlmostEqual(np.linalg.norm(positions[j] - p), contact, places=9)
            np.testing.assert_allclose(v_after + v_neutral, vel, atol=1e-12)
            self.assertAlmostEqual(v_after @ v_after + v_neutral @ v_neutral, vel @ vel, places=12)
            pos, vel, t0 = p, v_after, t
            struck.add(j)


class ParticlesToMomentsPhysics(unittest.TestCase):
    def setUp(self):
        self.m = model("particles_to_moments.py")

    def test_moments_of_model_distribution(self):
        v = np.linspace(-14, 14, 200001)
        for x in (0.0, 0.2, 0.5, 0.85):
            f = self.m["distribution"](x, v)
            n = np.trapezoid(f, v)
            self.assertAlmostEqual(n, self.m["density"](x), places=9)
            self.assertAlmostEqual(np.trapezoid(v*f, v) / n, self.m["bulk_velocity"](x), places=9)

    def test_binned_sample_moments_within_sampling_error(self):
        m = self.m
        x, v = m["sample_particles"]()
        bins = m["N_BINS"]
        centers, n_est, u_est = m["binned_moments"](x, v, bins, 1 + m["BEAM"])
        self.assertAlmostEqual(np.sum(n_est) / bins, 1 + m["BEAM"], places=12)
        index = np.minimum((x*bins).astype(int), bins - 1)
        for k, c in enumerate(centers):
            fine = np.linspace(c - 0.5/bins, c + 0.5/bins, 2001)
            n_exact = np.mean(m["density"](fine))
            u_exact = np.mean(m["density"](fine)*m["bulk_velocity"](fine)) / n_exact
            count = np.sum(index == k)
            self.assertLess(abs(n_est[k] - n_exact), 4*n_exact/np.sqrt(count))
            self.assertLess(abs(u_est[k] - u_exact), 4*np.std(v[index == k])/np.sqrt(count))


class EmWavePlasmaPhysics(unittest.TestCase):
    """kin6d E_y and electron data of the plasma-edge wave scene."""

    @classmethod
    def setUpClass(cls):
        cls.m = model("em_wave_plasma.py")

    def test_sheets_obey_transverse_newton_law(self):
        # Nonrelativistic cold electron (a_0 <= 0.01): d^2y/dt^2 = -E_y in
        # units of c/omega_pe, 1/omega_pe and m c omega_pe/e (SI q = -e). In
        # the steady late window the omega components obey omega^2 Y = E0 E.
        m = self.m
        data, x0 = m["DATA"], m["X0"]
        inside = (x0 > 0.2) & (x0 < 3.0)
        for run, omega in m["RUNS"].items():
            times = data["t_" + run]
            t = times[times >= data.parameters["window_start_" + run]]
            basis = np.column_stack([np.cos(omega*t), np.sin(omega*t), np.ones_like(t), t])
            y = np.array([m["transverse"](run, tau) for tau in t])[:, inside]
            e = np.array([np.interp(x0[inside], m["X"], m["field"](run, tau)) for tau in t])
            y_fit = np.linalg.lstsq(basis, y, rcond=None)[0][:2]
            e_fit = np.linalg.lstsq(basis, e, rcond=None)[0][:2]
            lhs, rhs = omega**2*y_fit, m["AMPLITUDE"]*e_fit
            self.assertLess(np.linalg.norm(lhs - rhs) / np.linalg.norm(rhs), 0.01, run)

    def test_steady_envelope_is_cold_plasma_fresnel(self):
        # Independent linear theory: N^2 = 1 - omega_pe^2/omega^2,
        # R = (1 - N)/(1 + N), T = 2/(1 + N); E_y = e^{ikx} + R e^{-ikx} (x < 0),
        # T e^{i omega N x/c} (x > 0).
        m = self.m
        data, x = m["DATA"], m["X"]
        for run, omega in m["RUNS"].items():
            n = np.sqrt(complex(1 - 1/omega**2))
            r, t = (1 - n)/(1 + n), 2/(1 + n)
            theory = np.where(x < 0, np.abs(1 + r*np.exp(-2j*omega*x)),
                              np.abs(t*np.exp(1j*omega*n*np.maximum(x, 0))))
            np.testing.assert_allclose(data["envelope_" + run], theory, atol=2e-6)
            end = data.parameters["window_end_" + run]
            frames = data["t_" + run]
            last = frames[(frames > end - 2*np.pi/omega) & (frames <= end)]
            peak = np.max(np.abs([m["field"](run, tau) for tau in last]), axis=0)
            if omega < 1:
                self.assertAlmostEqual(abs(r), 1.0, places=12)
            self.assertLess(np.max(np.abs(peak - theory)), 0.02, run)


class ThermalFluctuationPhysics(unittest.TestCase):
    """Smoothed net charge density of the kin6d thermal-fluctuation scene."""

    @classmethod
    def setUpClass(cls):
        cls.m = model("thermal_charge_fluctuations.py")

    def test_lattice_is_neutral_and_vacancy_is_positive(self):
        # Simple-cubic lattice with spacing a < sigma: the Gaussian-smoothed
        # density equals n_0 up to exp(-2 pi^2 sigma^2/a^2) (Poisson
        # summation), so rho = 0. Removing the electron at the origin leaves
        # rho/(e n_0) = +1/(n_0 (2 pi sigma^2)^(3/2)) there (deficit: positive)
        # and a Gaussian of plane integral 1/(n_0 sqrt(2 pi) sigma).
        m = self.m
        box, cells, sigma = 6.0, 20, m["SIGMA"]
        a = box / cells
        axis = -box / 2 + a * np.arange(cells)
        lattice = np.array(np.meshgrid(axis, axis, axis, indexing="ij")).reshape(3, -1)
        n0 = cells ** 3 / box ** 3
        grid = 2 * cells
        np.testing.assert_allclose(m["charge_density"](lattice, box, sigma, n0, grid), 0,
                                   atol=1e-10)
        vacancy = lattice[:, np.any(lattice != 0, axis=0)]
        # Cell centres at +-box/(2 grid) straddle the origin; evaluate with the
        # lattice shifted so that a grid centre sits on the vacancy.
        shift = np.array([[box / (2 * grid)], [box / (2 * grid)], [0.0]])
        rho = m["charge_density"](vacancy + shift, box, sigma, n0, grid)
        peak = 1 / (n0 * (2 * np.pi * sigma ** 2) ** 1.5)
        self.assertAlmostEqual(rho[grid // 2, grid // 2] / peak, 1.0, places=8)
        # Plane integral of the missing Gaussian: 1/(n_0 sqrt(2 pi) sigma).
        self.assertAlmostEqual(np.mean(rho) * box ** 2 * n0 * np.sqrt(2 * np.pi) * sigma,
                               1.0, places=6)    # kernel cut at |z| < 6 sigma

    def test_fluctuations_follow_debye_hueckel(self):
        # Independent theory: <(rho/(e n_0))^2> = sum_k exp(-k^2 sigma^2) S(k)/(n_0 L^3)
        # with S = k^2/(k^2 + 1) (Debye-Hueckel) over the box modes. The kin6d
        # data must match it and exclude the uncorrelated ideal gas (S = 1),
        # which is 19% larger at sigma = 0.4 lambda_D.
        m = self.m
        data = runpy.run_path(str(ROOT / "animations/kin6d_data.py"))["Export"](
            "thermal-charge-fluctuations")
        pos, box = data["positions"], data.parameters["box"]
        n0 = data.parameters["electrons"] / box ** 3
        sigma = m["SIGMA"]
        variance = np.mean([np.var(m["charge_density"](pos[:, :, f], box, sigma, n0, 60))
                            for f in range(pos.shape[2])])
        debye = m["debye_hueckel_variance"](box, sigma, n0)
        ideal = m["debye_hueckel_variance"](box, sigma, n0, lambda k2: np.ones_like(k2))
        self.assertLess(abs(variance / debye - 1), 0.08)
        self.assertLess(variance / ideal, 0.9)


class CouplingTestParticlePhysics(unittest.TestCase):
    """Frozen one-component plasma: x in a, t in a/v_th, E in k_B T."""

    @classmethod
    def setUpClass(cls):
        cls.m = model("coupling_test_particle.py")
        cls.charges, cls.radius = cls.m["frozen_charges"]()
        cls.runs = {g: cls.m["trajectories"](g) for g in cls.m["GAMMAS"]}

    def test_neutral_density_and_gauss_background(self):
        m, charges, radius = self.m, self.charges, self.radius
        self.assertAlmostEqual(4*np.pi/3*radius**3, len(charges), places=9)
        # Uniform sphere of charge N alone: Gauss gives |a| = (Gamma/2) N (r/R)^3/r^2.
        x = np.array([[1.3, -2.0, 0.4], [0.0, 3.1, -1.7]])
        acc = m["acceleration"](x, np.empty((0, 3)), 0.7)
        r = np.linalg.norm(x, axis=1)
        gauss = -0.35*len(charges)*(r/radius)**3/r**3
        np.testing.assert_allclose(acc, gauss[:, None]*x, rtol=1e-12)

    def test_force_is_minus_half_gradient_of_energy(self):
        m = self.m
        x = np.array([[-3.5, 0.1, 0.0], [0.37, -1.21, 0.0], [2.2, 1.9, 0.3]])
        h = 1e-5
        grad = np.zeros_like(x)
        for k in range(3):
            e = np.zeros(3); e[k] = h
            grad[:, k] = (m["potential_energy"](x + e, self.charges, self.radius, 1.0)
                          - m["potential_energy"](x - e, self.charges, self.radius, 1.0))/(2*h)
        np.testing.assert_allclose(m["acceleration"](x, self.charges, 1.0), -grad/2,
                                   rtol=1e-6, atol=1e-8)

    def test_energy_conserved_and_paths_planar(self):
        m = self.m
        for gamma, (t, x, v, _) in self.runs.items():
            e = np.array([m["energy"](x[k], v[k], self.charges, self.radius, gamma)
                          for k in range(len(t))])
            self.assertLess(np.max(np.abs(e - e[0])), 1e-6, gamma)
            self.assertLess(np.max(np.abs(x[..., 2])), 1e-9, gamma)
            self.assertLess(np.max(np.linalg.norm(x, axis=2)), self.radius - 2.0, gamma)

    def test_launch_points_in_potential_valleys(self):
        m = self.m
        strong = m["GAMMAS"][0]
        x0 = self.runs[strong][1][0]
        self.assertLessEqual(np.max(m["potential_energy"](x0, self.charges, self.radius, strong)), 0.0)
        distance = np.linalg.norm(x0[:, None] - self.charges[None], axis=2)
        self.assertGreaterEqual(distance.min(), 0.5)

    def test_weak_limit_matches_straight_line_impulse(self):
        # First-order (impulse) approximation, independent direct Coulomb sum
        # along the unperturbed line; its error is O(Gamma).
        m, gamma = self.m, 1e-4
        _, _, v, _ = m["trajectories"](gamma)
        ts = np.linspace(0.0, m["T_END"], 7001)
        for j, y0 in enumerate(m["LAUNCH_Y"]):
            p = np.column_stack([m["LAUNCH_X"] + ts, np.full_like(ts, y0), np.zeros_like(ts)])
            acc = np.zeros_like(p)
            for c in np.array_split(self.charges, 8):
                d = p[:, None, :] - c[None]
                acc += np.sum(d/np.sum(d*d, axis=2)[..., None]**1.5, axis=1)
            acc = 0.5*gamma*(acc - 4*np.pi/3*p)
            dv = np.trapezoid(acc, ts, axis=0)
            error = np.linalg.norm(v[-1, j] - [1, 0, 0] - dv)/np.linalg.norm(dv)
            self.assertLess(error, 0.02, y0)

    def test_strong_coupling_deflects_much_more(self):
        m = self.m
        strong, weak = m["GAMMAS"]
        angles = {g: m["deflection_angles"](v) for g, (_, _, v, _) in self.runs.items()}
        self.assertGreater(angles[strong].mean(), 1.0)
        self.assertLess(angles[weak].mean(), 0.1)
        self.assertGreater(angles[strong].mean(), 10*angles[weak].mean())

    def test_debye_circle_holds_few_versus_many(self):
        # Gamma_e = a^2/(4 pi lambda_D^2); the drawn slab 0 < z < a has areal
        # density 1/a^2, so about pi (lambda_D/a)^2 drawn electrons are inside.
        m = self.m
        for gamma in m["GAMMAS"]:
            lam = m["debye_radius"](gamma)
            self.assertAlmostEqual(1/(4*np.pi*lam**2), gamma, places=12)
        lam_strong, lam_weak = (m["debye_radius"](g) for g in m["GAMMAS"])
        self.assertAlmostEqual(lam_strong, 1.0, delta=0.05)
        self.assertAlmostEqual(lam_weak, 3.0, delta=0.05)
        points = m["shown_charges"](self.charges)
        for gamma in m["GAMMAS"]:
            _, x, _, _ = self.runs[gamma]
            counts = [m["inside_debye_circle"](points, x[k, 0, :2], gamma).sum()
                      for k in range(0, len(x), 10)]
            expected = np.pi*m["debye_radius"](gamma)**2
            self.assertLess(abs(np.mean(counts) - expected), 0.35*expected + 1.5, gamma)



class CouplingRegionsPhysics(unittest.TestCase):
    """kin6d runs at equal density and two temperatures; test electron in a, 1/omega_p."""

    NEAREST = 5     # candidates closest to the mid-line integrated per panel

    @classmethod
    def setUpClass(cls):
        m = cls.m = model("coupling_regions.py")
        cls.runs = [m["load_run"](slug, lam) for slug, lam in m["RUNS"]]
        cls.flights = []
        for p, (pos, _) in enumerate(cls.runs):
            points, lam = pos[:, :, -1], m["RUNS"][p][1]
            cand = m["launch_candidates"](points)
            cand = cand[np.argsort(np.abs(points[1, cand]))][:cls.NEAREST]
            cls.flights.append({int(j): m["test_trajectory"](points, j, lam) for j in cand})

    def test_equal_density_and_temperature_ratio(self):
        # Gamma_e = a^2/(4 pi lambda_D^2) and lambda_D^2 = k_B T/(m omega_p^2):
        # same N in the same cube of edge 18 a, T_weak/T_strong = 9.
        m = self.m
        (strong, _), (weak, _) = self.runs
        self.assertEqual(strong.shape[1], weak.shape[1])
        self.assertAlmostEqual(strong.shape[1]/m["BOX"]**3, 1.0, places=12)
        for _, lam in m["RUNS"]:
            self.assertAlmostEqual(m["debye_length"](m["coupling"](lam)), lam, places=12)
        lams = [lam for _, lam in m["RUNS"]]
        self.assertAlmostEqual((lams[1]/lams[0])**2, 9.0)
        # Kinetic temperature of the data: <v_i^2> = k_B T/m = lambda_D^2 omega_p^2.
        for (pos, t), lam in zip(self.runs, lams):
            dx = np.diff(pos, axis=2)
            dx -= m["BOX"]*np.round(dx/m["BOX"])
            v2 = np.mean((dx/np.diff(t))**2)
            self.assertLess(abs(v2/lam**2 - 1), 0.03, lam)

    def test_fluctuations_follow_debye_hueckel(self):
        # Independent theory (thermal-fluctuation scene): variance of the
        # smoothed charge density for S = k^2/(k^2 + 1) in lambda_D units; the
        # uncorrelated ideal gas (S = 1) is excluded at both temperatures.
        m = self.m
        th = model("thermal_charge_fluctuations.py")
        for (pos, _), (_, lam) in zip(self.runs, m["RUNS"]):
            fields = m["run_fields"](pos[:, :, ::4], lam, 90)
            variance = np.mean(fields.var(axis=(0, 1)))
            box, n0, sigma = m["BOX"]/lam, lam**3, m["SIGMA_DEBYE"]
            debye = th["debye_hueckel_variance"](box, sigma, n0)
            ideal = th["debye_hueckel_variance"](box, sigma, n0, lambda k2: np.ones_like(k2))
            self.assertLess(abs(variance/debye - 1), 0.1, lam)
            self.assertLess(variance/ideal, 0.85, lam)

    def test_force_is_minus_gradient_and_energy_conserved(self):
        m = self.m
        j, (t, x, v, charges) = next(iter(self.flights[0].items()))
        h = 1e-5
        x0 = x[len(x)//2]
        grad = np.array([(m["test_energy"](x0 + h*e, np.zeros(3), charges)
                          - m["test_energy"](x0 - h*e, np.zeros(3), charges))/(2*h)
                         for e in np.eye(3)])
        np.testing.assert_allclose(m["test_acceleration"](x0, charges), -grad, rtol=1e-5,
                                   atol=1e-8)
        self.assertAlmostEqual(4*np.pi/3*m["background_radius"](charges)**3, len(charges))
        for flights in self.flights:
            for t, x, v, charges in flights.values():
                e = [m["test_energy"](x[k], v[k], charges) for k in (0, len(t)//2, len(t) - 1)]
                self.assertLess(np.max(np.abs(np.array(e) - e[0])), 1e-6)

    def test_launch_choice_and_thermal_speed(self):
        # LAUNCH: the candidate closest to y = 0 whose drawn path stays within
        # |z| < Z_LIMIT (strong: also inside the window for the whole flight).
        m = self.m
        for p, flights in enumerate(self.flights):
            points = self.runs[p][0][:, :, -1]
            chosen = None
            for j in sorted(flights, key=lambda j: abs(points[1, j])):
                t, x, v, _ = flights[j]
                n = m["drawn_samples"](x)
                ok = np.max(np.abs(x[:n, 2])) < m["Z_LIMIT"]
                if p == 0:
                    ok = ok and m["drawn_samples"](x, m["WINDOW_MARGIN"]) == len(t) \
                        and t[-1] >= m["T_TEST"] - 1e-9
                if ok:
                    chosen = j
                    break
            self.assertEqual(chosen, m["LAUNCH"][p])
            v0 = flights[chosen][2][0]
            self.assertAlmostEqual(np.linalg.norm(v0), np.sqrt(2)*m["RUNS"][p][1])

    def test_strong_coupling_deflects_much_more(self):
        m = self.m
        median = []
        for flights in self.flights:
            angles = [m["deflection"](v, m["drawn_samples"](x)) for _, x, v, _ in flights.values()]
            median.append(np.median(angles))
        self.assertGreater(median[0], 0.5)
        self.assertLess(median[1], 0.3)
        self.assertGreater(median[0], 3*median[1])

    def test_slide_still_matches_animation(self):
        stored = json.loads((ROOT/"slides/coupling-regions.json").read_text())
        record, images = self.m["still_data"]()
        self.assertEqual(stored, json.loads(json.dumps(record)))
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Pillow not available")
        for p, image in enumerate(images):
            saved = np.asarray(Image.open(ROOT/f"slides/coupling-regions-{p}.png").convert("RGB"))
            np.testing.assert_array_equal(saved, image)


class HardSphereRelaxationPhysics(unittest.TestCase):
    """animations/hard_sphere_relaxation.py: elastic hard disks relax from one
    speed to the 2D Maxwellian at the same energy.

    Oracles: the head-on elastic collision of equal masses, energy
    conservation, a Kolmogorov-Smirnov test against the Maxwellian
    cumulative distribution 1 - exp(-v^2/v_0^2), and the entropy estimator on
    an independent Maxwellian sample.
    """

    @classmethod
    def setUpClass(cls):
        cls.m = model("hard_sphere_relaxation.py")
        cls.pos, cls.vel, cls.clock = cls.m["hs_run"]()
        cls.speed = np.linalg.norm(cls.vel, axis=2)

    def test_head_on_collision_exchanges_velocities(self):
        r = self.m["HS_RADIUS"]
        pos = np.array([[0.5 - 0.99*r, 0.5], [0.5 + 0.99*r, 0.5]])
        vel = np.array([[1.0, 0.2], [-0.5, 0.0]])
        _, after, hits = self.m["hs_step"](pos, vel, dt=0.0)
        self.assertEqual(hits, 1)
        np.testing.assert_allclose(after, [[-0.5, 0.2], [1.0, 0.0]], atol=1e-14)

    def test_energy_conserved_and_initial_state_monoenergetic(self):
        e = 0.5*np.sum(self.speed**2, axis=1)
        self.assertLess(abs(self.speed[0] - 1).max(), 1e-14)
        self.assertLess(abs(e/e[0] - 1).max(), 1e-13)
        print(f"hard disks: max |E/E0 - 1| = {abs(e/e[0] - 1).max():.1e} over "
              f"{self.clock[-1]:.1f} collisions per disk")

    def test_late_speeds_follow_the_maxwellian(self):
        late = np.nonzero(self.clock >= 4.0)[0]
        frames = late[::max(1, len(late)//6)]
        worst = 0.0
        for k in frames:
            v = np.sort(self.speed[k])
            cdf = 1 - np.exp(-v**2)
            n = len(v)
            d = max(np.max(np.arange(1, n + 1)/n - cdf), np.max(cdf - np.arange(n)/n))
            worst = max(worst, d)
        self.assertLess(worst, 1.63/np.sqrt(len(self.speed[0])))        # 1 % KS level per frame
        early = self.speed[1]
        d0 = np.max(np.abs(np.arange(1, len(early) + 1)/len(early) - (1 - np.exp(-np.sort(early)**2))))
        self.assertGreater(d0, 0.2)                                       # far from Maxwellian at the start
        print(f"hard disks: KS distance to the Maxwellian, late frames <= {worst:.3f} "
              f"(1 % level {1.63/np.sqrt(len(self.speed[0])):.3f}); first stored frame {d0:.2f}")

    def test_entropy_rises_to_the_maxwellian_value(self):
        m = self.m
        s = np.array([m["velocity_entropy"](v) for v in self.speed])
        target = 1 + np.log(np.pi)
        self.assertAlmostEqual(m["HS_ENTROPY_MAXWELL"], target, places=14)
        rng = np.random.default_rng(1)
        sample = np.sqrt(-np.log(rng.random(600)))                        # inverse of 1 - exp(-v^2)
        self.assertAlmostEqual(m["velocity_entropy"](sample), target, delta=0.03)
        late = s[self.clock >= 4.0]
        self.assertLess(s[0], 0.1)
        self.assertAlmostEqual(late.mean(), target, delta=0.015)
        self.assertLess(late.std(), 0.015)
        print(f"hard disks: entropy {s[0]:.3f} at the start, late mean {late.mean():.4f} +- {late.std():.4f}, "
              f"Maxwellian 1 + ln(pi) = {target:.4f}")


class SheetOscillationPhysics(unittest.TestCase):
    """animations/sheet_oscillation.py: cold electron sheets on an ion background.

    Oracles: the field summed sheet by sheet (each sheet +-sigma/2 epsilon_0 on
    either side, background field x - pi), an independent RK4 integration
    with that field, and the crossing time of two discrete neighbouring sheets.
    """

    @classmethod
    def setUpClass(cls):
        cls.m = model("sheet_oscillation.py")

    @staticmethod
    def direct_accel(x):
        n = len(x)
        delta = 2*np.pi/n
        e = -0.5*delta*np.sign(x[:, None] - x[None, :]).sum(axis=1) + (x - np.pi)
        return -(e - (x.mean() - np.pi))          # zero-mean field, -eE/m_e

    def test_rank_field_equals_sheet_sum(self):
        rng = np.random.default_rng(4)
        x = np.mod(self.m["sheet_equilibrium"](40) + rng.normal(0, 0.4, 40), 2*np.pi)
        np.testing.assert_allclose(self.m["sheet_accel"](x), self.direct_accel(x), atol=1e-12)

    def test_small_amplitude_oscillates_at_plasma_frequency(self):
        m = self.m
        n, kv = 40, m["SMALL_KV"]
        x = m["sheet_equilibrium"](n)
        state = np.concatenate([x, kv*np.sin(x)])
        dt = 2*np.pi/400

        def rhs(s):
            return np.concatenate([s[n:], self.direct_accel(np.mod(s[:n], 2*np.pi))])

        for _ in range(400):
            k1 = rhs(state); k2 = rhs(state + dt/2*k1); k3 = rhs(state + dt/2*k2); k4 = rhs(state + dt*k3)
            state = state + dt/6*(k1 + 2*k2 + 2*k3 + k4)
        np.testing.assert_allclose(state[:n], x, atol=1e-9)              # back after one period 2 pi/omega_pe
        np.testing.assert_allclose(state[n:], kv*np.sin(x), atol=1e-9)
        t, xs, vs = m["sheet_run"](kv)
        omega = m["mode_frequency"](t, vs)
        self.assertAlmostEqual(omega, 1, delta=2e-5)                      # leapfrog: (omega dt)^2/24 = 1.0e-5
        self.assertEqual(m["first_crossing"](t, xs), np.inf)
        print(f"sheets k v0/omega_pe = {kv}: RK4 period error {abs(state[:n] - x).max():.1e}, "
              f"leapfrog omega/omega_pe = {omega:.7f}, no crossing")

    def test_large_amplitude_breaks_at_predicted_time(self):
        m = self.m
        kv, n = m["LARGE_KV"], m["SHEETS"]
        t, xs, _ = m["sheet_run"](kv)
        crossing = m["first_crossing"](t, xs)
        delta = 2*np.pi/n
        discrete = np.arcsin(delta/(2*kv*np.sin(delta/2)))
        self.assertAlmostEqual(crossing, discrete, delta=1e-3)
        self.assertAlmostEqual(discrete, np.arcsin(1/kv), delta=1e-4)
        print(f"sheets k v0/omega_pe = {kv}: first crossing omega_pe t = {crossing:.5f}, "
              f"discrete sheets {discrete:.5f}, continuum arcsin(1/(k v0)) = {np.arcsin(1/kv):.5f}")


class TwoSpeciesOscillationPhysics(unittest.TestCase):
    """derivations/plot_two_species_oscillation.py: cold electron-ion
    oscillation at omega_p^2 = omega_pe^2 + omega_pi^2 with antiphase
    displacements xi_i = -(m_e/m_i) xi_e."""

    @classmethod
    def setUpClass(cls):
        cls.m = runpy.run_path(str(ROOT/"derivations/plot_two_species_oscillation.py"))

    def test_gauss_field_of_a_displaced_layer(self):
        m = self.m
        n = 4096
        x0 = (np.arange(n) + 0.5)*2*np.pi/n
        xi = 0.01*np.sin(x0)
        x = np.concatenate([x0 + xi, x0])
        charge = np.concatenate([-np.ones(n), np.ones(n)])*2*np.pi/n
        e = m["field"](x, charge)
        # Gauss: before any crossing the field at an electron is its own displacement,
        # e E = m_e omega_pe^2 xi; linear weighting adds an O((k h)^2) = 6e-4 relative error.
        np.testing.assert_allclose(e[:n], xi, atol=1e-3*0.01)

    def test_frequency_and_amplitude_ratio(self):
        m = self.m
        for ratio in (1, 4, 100):
            t, xi_e, xi_i, v_e = m["run"](ratio)
            omega = m["measured_frequency"](t, v_e)
            self.assertAlmostEqual(omega/np.sqrt(1 + 1/ratio), 1, delta=5e-4)
            big = abs(xi_e) > 0.5*abs(xi_e).max()
            self.assertAlmostEqual(np.median(xi_i[big]/xi_e[big]), -1/ratio, delta=0.01/ratio)
            print(f"two species m_i/m_e = {ratio}: omega/omega_pe = {omega:.6f}, "
                  f"sqrt(1 + m_e/m_i) = {np.sqrt(1 + 1/ratio):.6f}, xi_i/xi_e = {np.median(xi_i[big]/xi_e[big]):+.4f}")


class BoltzmannCountingPhysics(unittest.TestCase):
    """derivations/plot_boltzmann_counting.py: P(E) of one oscillator in contact
    with an Einstein-solid reservoir.

    Oracles: brute-force enumeration of all microstates of a small solid and
    the Boltzmann factor at the reservoir temperature eps/ln 2.
    """

    @classmethod
    def setUpClass(cls):
        cls.m = runpy.run_path(str(ROOT/"derivations/plot_boltzmann_counting.py"))

    def test_counts_match_enumeration(self):
        import itertools
        for oscillators in (3, 4):
            quanta = oscillators
            counts = np.zeros(quanta + 1)
            for state in itertools.product(range(quanta + 1), repeat=oscillators + 1):
                if sum(state) == quanta:
                    counts[state[0]] += 1                        # state[0]: the small oscillator
            np.testing.assert_allclose(self.m["probability"](np.arange(quanta + 1), oscillators),
                                       counts/counts.sum(), rtol=1e-12)

    def test_large_reservoir_gives_boltzmann_factor(self):
        m = self.m
        self.assertAlmostEqual(m["temperature"](), 1/np.log(2), places=14)
        n = np.arange(5)
        devs = [np.abs(m["probability"](n, size)/m["boltzmann"](n) - 1).max() for size in (40, 400, 4000)]
        self.assertLess(devs[2], 3e-4)
        self.assertAlmostEqual(devs[0]/devs[1], 10, delta=1.0)               # 1/N convergence
        self.assertAlmostEqual(devs[1]/devs[2], 10, delta=0.5)
        self.assertAlmostEqual(m["probability"](np.arange(400 + 1), 400).sum(), 1, places=10)   # lgamma round-off
        print("Boltzmann counting: max |P/P_B - 1| for E <= 4 eps at N = 40, 400, 4000: "
              + ", ".join(f"{d:.2e}" for d in devs))


class CyclotronResonancePhysics(unittest.TestCase):
    """animations/cyclotron_resonance.py: Boris orbits in B with a rotating E.

    Oracles: an RK4 integration of dw/dt = -i omega_c w + (q/m) E_0 e^{-i s omega t},
    the closed-form |w(t)| from rest, and the resonance condition s omega = omega_c.
    """

    @classmethod
    def setUpClass(cls):
        cls.m = model("cyclotron_resonance.py")

    @staticmethod
    def rk4_speed(qm, sense, omega, t_end, steps):
        omega_c = np.sign(qm)

        def rhs(t, w):
            return -1j*omega_c*w + qm*np.exp(-1j*sense*omega*t)

        w, dt = 0j, t_end/steps
        for i in range(steps):
            t = i*dt
            k1 = rhs(t, w); k2 = rhs(t + dt/2, w + dt/2*k1); k3 = rhs(t + dt/2, w + dt/2*k2); k4 = rhs(t + dt, w + dt*k3)
            w += dt/6*(k1 + 2*k2 + 2*k3 + k4)
        return abs(w)

    def test_orbits_match_closed_form_and_rk4(self):
        m = self.m
        for run in m["CR_RUNS"] + ((-1.0, 1, 1.0),):
            t, x, speed = m["cr_orbit"](*run)
            formula = m["cr_speed_formula"](t, *run)
            dt = t[1] - t[0]
            self.assertLess(abs(speed - formula).max(), 0.6*dt)           # Boris velocity lags by dt/2 from rest
            reference = self.rk4_speed(*run, t[-1], 4000)
            self.assertAlmostEqual(reference, formula[-1], delta=1e-8)

    def test_resonance_growth_and_bounds(self):
        m = self.m
        res_i = m["cr_orbit"](1.0, 1, 1.0)
        res_e = m["cr_orbit"](-1.0, -1, 1.0)
        for t, _, speed in (res_i, res_e):
            self.assertAlmostEqual(m["cr_growth_rate"](t, speed), 1, delta=2e-4)    # dv_perp/dt = |q| E_0/m
            w = 0.5*speed**2
            late = t > 2*np.pi
            self.assertAlmostEqual(np.polyfit(np.log(t[late]), np.log(w[late]), 1)[0], 2, delta=0.01)
        detuned = m["cr_orbit"](1.0, 1, m["CR_DETUNED"])[2].max()
        self.assertAlmostEqual(detuned, 2/(1 - m["CR_DETUNED"]), delta=0.01)
        for wrong in ((1.0, -1, 1.0), (-1.0, 1, 1.0)):                    # counter-rotating for each species
            self.assertLess(m["cr_orbit"](*wrong)[2].max(), 1.0 + 1e-3)
        print(f"cyclotron resonance: dv_perp/dt = {m['cr_growth_rate'](res_i[0], res_i[2]):.5f} (ion), "
              f"{m['cr_growth_rate'](res_e[0], res_e[2]):.5f} (electron), formula 1; "
              f"detuned max {detuned:.4f} (formula {2/(1 - m['CR_DETUNED']):.4f}); "
              f"counter-rotating max {m['cr_orbit'](1.0, -1, 1.0)[2].max():.4f} (formula 1)")


# --- Chapters 7-12: upcoming-chapter visuals -------------------------------

class DiamagneticDriftPhysics(unittest.TestCase):
    """Gyrating ions with fixed guiding centres against the magnetization current."""

    @classmethod
    def setUpClass(cls):
        cls.m = model("diamagnetic_drift.py")

    def test_orbits_solve_lorentz_force_with_fixed_centre(self):
        m = self.m
        x0, y0, phase = (a[:50] for a in m["guiding_centres"]())
        t = np.linspace(0.0, 2*np.pi, 4001)
        pos, vel = m["orbit"](x0, y0, phase, t)
        dt = t[1] - t[0]
        # dx/dt = v and dv/dt = omega_c v x e_z (q_alpha > 0, B along +z).
        np.testing.assert_allclose(np.gradient(pos, dt, axis=1)[:, 1:-1], vel[:, 1:-1], atol=1e-5)
        accel = np.gradient(vel, dt, axis=1)[:, 1:-1]
        lorentz = m["OMEGA_C"]*np.stack([vel[..., 1], -vel[..., 0]], axis=-1)[:, 1:-1]
        np.testing.assert_allclose(accel, lorentz, atol=1e-5)
        centre = pos + np.stack([vel[..., 1], -vel[..., 0]], axis=-1)/m["OMEGA_C"]
        np.testing.assert_allclose(centre[..., 0], np.repeat(x0[:, None], len(t), 1), atol=1e-12)
        np.testing.assert_allclose(centre[..., 1], np.repeat(y0[:, None], len(t), 1), atol=1e-12)

    def test_sampled_density_has_the_stated_gradient(self):
        m = self.m
        _, y0, _ = m["guiding_centres"]()
        counts, edges = np.histogram(y0, np.linspace(-m["Y_FILL"], m["Y_FILL"], 9))
        mid = 0.5*(edges[1:] + edges[:-1])
        area = np.diff(edges)*2*m["X_HALF"]
        slope = np.polyfit(mid, counts/area, 1)
        self.assertAlmostEqual(slope[0], m["N0"]/m["L_GRAD"], delta=0.02*m["N0"]/m["L_GRAD"])
        self.assertAlmostEqual(slope[1], m["N0"], delta=0.02*m["N0"])

    def test_time_stepped_count_equals_geometric_count(self):
        # Over one period an ion whose circle reaches the line crosses it at
        # Y +- sqrt(rho^2 - d^2): moving right at the top (clockwise ion).
        m = self.m
        x0, y0, _ = m["guiding_centres"]()
        rho, edges = m["RHO_L"], m["BIN_EDGES"]
        net = np.zeros(len(edges) - 1)
        for line in m["LINES"]:
            d = x0 - line
            hit = np.abs(d) < rho
            s = np.sqrt(rho**2 - d[hit]**2)
            net += np.histogram(y0[hit] + s, edges)[0] - np.histogram(y0[hit] - s, edges)[0]
        stepped = m["binned_counts"](periods=1)*len(m["LINES"])
        np.testing.assert_array_equal(stepped, net)

    def test_current_matches_b_cross_grad_p(self):
        # j = B x grad p/B^2 with p = n m v_perp^2/2, B = B e_z, grad n = n_0/L e_y:
        # j_x = -(m v_perp^2/(2B)) n_0/L; in units of q n_0 v_perp: -rho_L/(2L).
        m = self.m
        expected = -0.5*m["RHO_L"]/m["L_GRAD"]
        measured = m["measured_current"]()
        self.assertAlmostEqual(np.mean(measured), expected, delta=0.02*abs(expected))
        self.assertTrue(np.all(np.abs(measured/expected - 1) < 0.2), measured)
        self.assertAlmostEqual(m["formula_current"](), expected, places=14)


class MagnetizedRandomWalkPhysics(unittest.TestCase):
    """Guiding-centre random walk against the Green-Kubo coefficient."""

    @classmethod
    def setUpClass(cls):
        cls.m = model("magnetized_random_walk.py")
        cls.d = {b: cls.m["measured_diffusion"](b) for b in cls.m["B_VALUES"]}

    def test_free_motion_between_collisions_is_a_larmor_circle(self):
        m = self.m
        t, x, centre, hits = m["single_ion"]()
        radius = np.linalg.norm(x - centre, axis=1)
        np.testing.assert_allclose(radius, m["V_PERP"], rtol=1e-12)    # rho_L = v_perp/omega_c, omega_c = 1
        k = np.searchsorted(hits, t, side="right")
        same = k[1:] == k[:-1]
        speed = np.linalg.norm(np.diff(x, axis=0), axis=1)/np.diff(t)
        np.testing.assert_allclose(speed[same], m["V_PERP"], rtol=1e-4)
        self.assertGreater(len(hits), 5)

    def test_jump_mean_square_is_two_larmor_radii_squared(self):
        m = self.m
        times, angles = m["collision_sequence"](2000)
        for b in m["B_VALUES"]:
            steps = m["jumps"](times, angles, b)
            ms = np.mean(np.sum(steps**2, axis=-1))
            self.assertAlmostEqual(ms/(2*(m["V_PERP"]/b)**2), 1.0, delta=0.02)

    def test_diffusion_matches_green_kubo_quadrature(self):
        # D = (1/2) int_0^inf <v(0).v(t)> dt with <v(0).v(t)> = v^2 exp(-nu t) cos(omega t)
        # for isotropic redirection at Poisson rate nu (two dimensions).
        m = self.m
        nu, v = m["NU"], m["V_PERP"]
        s = np.linspace(0.0, 60.0/nu, 600001)
        for b, d in self.d.items():
            integrand = v**2*np.exp(-nu*s)*np.cos(b*s)
            gk = 0.5*np.sum(0.5*(integrand[1:] + integrand[:-1])*np.diff(s))
            self.assertAlmostEqual(d/gk, 1.0, delta=0.06, msg=f"B={b}")

    def test_perpendicular_diffusion_scales_as_inverse_square_field(self):
        b = np.array(sorted(self.d))
        slope = np.polyfit(np.log(b), np.log([self.d[k] for k in b]), 1)[0]
        self.assertAlmostEqual(slope, -2.0, delta=0.08)


class FrozenFluxPhysics(unittest.TestCase):
    """Induction equation for A_z: frozen flux at R_m = 10^4, diffusion at u = 0."""

    @classmethod
    def setUpClass(cls):
        cls.m = model("frozen_flux.py")

    @staticmethod
    def fourier_value(field, point):
        """Trigonometric interpolation of a periodic grid field[y, x] on [0, 2 pi)^2."""
        n = field.shape[0]
        k = np.fft.fftfreq(n, 1.0 / n)
        coeff = np.fft.fft2(field) / n**2
        return np.real(np.exp(1j * k * point[1]) @ coeff @ np.exp(1j * k * point[0]))

    def test_large_rm_carries_flux_with_fluid(self):
        from scipy.integrate import solve_ivp
        m = self.m
        t, states, _, _ = m["solve"](1.0 / m["REYNOLDS"][0], n=128)
        start = m["tracer_start"]()

        def u(_, p):
            x, y = p
            return [np.sin(x) * np.cos(y), -np.cos(x) * np.sin(y)]

        for p0 in start[::4]:
            path = solve_ivp(u, (0, t[-1]), p0, method="DOP853", rtol=1e-10, atol=1e-12,
                             t_eval=t).y.T
            values = [self.fourier_value(s, p) for s, p in zip(states, path)]
            # A_z/A_0 on the traced field line stays at 1/2 within 3 %.
            self.assertLess(np.max(np.abs(np.array(values) / m["TRACER_LEVEL"] - 1)), 0.03)
        # O-point flux: max A_z falls only by the Gaussian diffusion estimate.
        sigma2 = m["SIGMA"] ** 2
        estimate = sigma2 / (sigma2 + 2 * t[-1] / m["REYNOLDS"][0])
        self.assertAlmostEqual(states[-1].max(), estimate, delta=0.01)
        self.assertGreater(states[-1].max(), 0.97)

    def test_small_rm_loses_the_fluid_elements(self):
        m = self.m
        _, _, _, values = m["solve"](1.0 / m["REYNOLDS"][1], n=96)
        self.assertLess(values[-1].mean() / m["TRACER_LEVEL"], 0.25)

    def test_mode_decays_on_diffusion_time(self):
        m = self.m
        for diffusivity in (0.1, 0.05):
            self.assertAlmostEqual(m["mode_decay_time"](diffusivity, mode=(2, 1)),
                                   1.0 / (diffusivity * 5), places=6)

    def test_gaussian_diffuses_without_flow(self):
        m = self.m
        diffusivity = 1.0 / m["REYNOLDS"][1]
        t, states, _, _ = m["solve"](diffusivity, flow=0.0, n=96,
                                     tracers=np.zeros((1, 2)))
        centre = (np.pi / 2 + m["OFFSET"], np.pi / 2)
        peak = np.array([self.fourier_value(s, centre) for s in states])
        sigma2 = m["SIGMA"] ** 2
        exact = sigma2 / (sigma2 + 2 * diffusivity * t)          # 2D Gaussian peak
        np.testing.assert_allclose(peak, exact, rtol=1e-4)

    def test_contours_lie_on_level(self):
        m = self.m
        x, _ = m["grid"](96)
        xx, yy = np.meshgrid(x, x)
        f = m["initial_flux"](xx, yy)
        exact_r = m["SIGMA"] * np.sqrt(-2 * np.log(0.5))
        for line in m["contour_paths"](f, 0.5, x):
            r = np.hypot(line[:, 0] - np.pi / 2 - m["OFFSET"], line[:, 1] - np.pi / 2)
            self.assertLess(np.max(np.abs(r / exact_r - 1)), 0.02)
            np.testing.assert_allclose(line[0], line[-1])          # closed loop


class AlfvenWavePhysics(unittest.TestCase):
    """Linearized shear Alfven wave on a tied field line."""

    @classmethod
    def setUpClass(cls):
        cls.m = model("alfven_wave.py")

    def test_pulse_speed_is_alfven_speed(self):
        m = self.m
        for b0, rho in ((1.0, 1.0), (1.0, 4.0), (2.0, 1.0)):
            x, t, xi = m["solve"](rho, b0)
            v_a = b0 / np.sqrt(m["MU0"] * rho)
            # Centroid of the right half of the split pulse, before any reflection.
            use = (t > 4 * m["WIDTH"] / v_a) & (m["X_PLUCK"] + v_a * t < 0.85)
            centroids = []
            for s, ti in zip(xi[use], t[use]):
                window = (x > m["X_PLUCK"] + 0.5 * v_a * ti) & (x < 1.0)
                w = np.where(s[window] > 0.05, s[window], 0.0)     # pulse body only
                centroids.append(np.sum(w * x[window]) / np.sum(w))
            speed = np.polyfit(t[use], centroids, 1)[0]
            self.assertLess(abs(speed / v_a - 1), 1e-3)
            self.assertLess(abs(m["measured_speed"](rho, b0)[0] / v_a - 1), 1e-3)

    def test_matches_dalembert_before_reflection(self):
        m = self.m
        x, t, xi = m["solve"](1.0)
        x0, w = m["X_PLUCK"], m["WIDTH"]

        def pluck(z):
            return np.exp(-(z - x0) ** 2 / (2 * w**2))

        for s, ti in zip(xi, t):
            if ti > (x0 - 5 * w):             # left pulse would reach the tied end
                break
            exact = 0.5 * (pluck(x - ti) + pluck(x + ti))
            self.assertLess(np.max(np.abs(s - exact)), 5e-3)

    def test_reflection_inverts_at_tied_end(self):
        m = self.m
        x, t, xi = m["solve"](1.0)
        last = xi[-1]
        # At t = 0.6 L/v_A the left pulse has reflected from x = 0 and travels
        # right inverted, centred at 0.6 - 0.3 = 0.3 L.
        i = np.argmin(np.abs(x - 0.3))
        self.assertLess(last[i], -0.45)
        self.assertAlmostEqual(last[0], 0.0)
        self.assertAlmostEqual(last[-1], 0.0)


class SmallAngleDeflectionPhysics(unittest.TestCase):
    """Coulomb-logarithm rate of the accumulated small-angle deflection."""

    @classmethod
    def setUpClass(cls):
        cls.m = model("small_angle_deflections.py")

    def test_rutherford_angle_from_orbit(self):
        # Integrate the repulsive Coulomb orbit, r'' = b90 v^2 r/|r|^3 in units
        # b90 = v = 1 (same |theta| as attraction), and compare the outgoing angle.
        from scipy.integrate import solve_ivp

        def rhs(_, y):
            r = np.hypot(y[0], y[1])
            return [y[2], y[3], y[0] / r**3, y[1] / r**3]

        for b in (0.3, 1.0, 3.0, 10.0):
            x0 = -2e4
            sol = solve_ivp(rhs, (0, 4e4), [x0, b, 1.0, 0.0], rtol=1e-11, atol=1e-12)
            vx, vy = sol.y[2, -1], sol.y[3, -1]
            theta = np.arctan2(vy, vx)
            # the finite start and end distance leave O(b90/|x0|) of the angle
            self.assertAlmostEqual(theta, self.m["rutherford_angle"](b), delta=3e-4)

    def test_strong_constant_by_quad(self):
        from scipy.integrate import quad
        f = lambda x: (2 * np.arctan(1 / x))**2 * 2 * x
        c = (quad(f, 0, 1)[0] + quad(lambda x: f(x) - 8 / x, 1, np.inf, limit=400)[0]) / 8
        self.assertAlmostEqual(self.m["strong_constant"](), c, places=4)
        # weak decades approach the small-angle value 8 ln 10
        self.assertAlmostEqual(self.m["bin_rate"](100.0, 1000.0), 8 * np.log(10), delta=2e-3)

    def test_production_rate_against_coulomb_logarithm(self):
        m = self.m
        s, vec, bins, _ = m["simulate"]()
        rate, _ = m["measured_rate"](s, vec)
        per = np.sum(vec[:, -1]**2, axis=1) / s[-1]
        stderr = per.std() / np.sqrt(len(per))
        exact = 8 * (np.log(m["B_MAX"]) + m["strong_constant"]())
        self.assertLess(stderr / exact, 0.02)
        self.assertLess(abs(rate - exact), 3 * stderr)
        # every weak decade (b > b_90) gives its quadrature share within three
        # standard errors of a compound Poisson sum, Var = s N_e^-1 int theta^4 dN
        edges = m["EDGES"]
        for j in range(1, len(edges) - 1):
            x = np.geomspace(edges[j], edges[j + 1], 20001)
            th = m["rutherford_angle"](x)
            moment = lambda f: np.sum((f[1:] + f[:-1]) / 2 * np.diff(x))
            second, fourth = moment(th**2 * 2 * x), moment(th**4 * 2 * x)
            rel_se = np.sqrt(s[-1] * fourth / m["N_ELECTRONS"]) / (s[-1] * second)
            self.assertLess(rel_se, 0.03)
            share = bins[j, -1] / s[-1]
            self.assertLess(abs(share / m["bin_rate"](edges[j], edges[j + 1]) - 1), 3 * rel_se)
        # strong encounters b < b_90 carry under a tenth of the sum
        self.assertLess(m["bin_rate"](0.0, 1.0) / exact, 0.1)


class AmbipolarExpansionPhysics(unittest.TestCase):
    """Drift-diffusion slab: free diffusion, conservation and D_a."""

    @classmethod
    def setUpClass(cls):
        cls.m = model("ambipolar_expansion.py")

    def test_free_diffusion_without_field(self):
        # A negligible Debye coupling turns the field off; both species must
        # then diffuse with their own coefficients (sigma^2 grows as 2 D t).
        m = self.m
        times = np.linspace(0.002, 0.01, 5)
        x, t, n_i, n_e, _ = m["simulate"](times=times, l_debye=1e-6)
        x0, _, n0 = m["initial"]()
        for n, d in ((n_i, 1.0), (n_e, m["d_electron"]())):
            slope = np.polyfit(t, m["variance"](x, n), 1)[0] / 2
            self.assertAlmostEqual(slope / d, 1, delta=2e-3)

    def test_conservation_and_ambipolar_limit(self):
        m = self.m
        times = np.linspace(0.2, 1.0, 9)
        d_a = m["d_ambipolar"]()
        self.assertAlmostEqual(d_a, (m["d_electron"]() + m["MU_RATIO"]) / (1 + m["MU_RATIO"]))
        deviation = []
        for l_debye in (10.0, 20.0):
            x, t, n_i, n_e, e_face = m["simulate"](times=times, l_debye=l_debye)
            dx = x[1] - x[0]
            self.assertAlmostEqual(n_i[-1].sum() * dx, 2.0, places=9)
            self.assertAlmostEqual(n_e[-1].sum() * dx, 2.0, places=9)
            deviation.append(abs(m["measured_diffusion"](t, x, n_i, t_from=0.2) / d_a - 1))
            # core field equals the quasi-neutral ambipolar field
            xf = 0.5 * (x[1:] + x[:-1])
            core = np.abs(xf) < 1.5
            e_a = m["ambipolar_field"](x, 0.5 * (n_i[-1] + n_e[-1]))
            self.assertLess(np.max(np.abs(e_face[-1][core] - e_a[core])) / np.max(np.abs(e_a[core])), 0.01)
        # finite Debye length is the only departure: it shrinks with lambda_De/L
        self.assertLess(deviation[1], deviation[0] / 2)
        self.assertLess(deviation[0], 0.03)
        self.assertLess(deviation[1], 0.01)


class EmWavePacketPhysics(unittest.TestCase):
    """Fourier packet of omega^2 = omega_pe^2 + c^2 k^2 (normalized, c = omega_pe = 1)."""

    @classmethod
    def setUpClass(cls):
        cls.m = model("em_wave_packet.py")

    def test_local_frequency_and_wavenumber_obey_dispersion(self):
        # Phase of the analytic field at the envelope centre on a finer,
        # longer grid than the scene: omega = -d(phase)/dt, k = d(phase)/dx.
        m, cells, length = self.m, 8192, 600.0
        t, dt = 30.0, 1e-3
        centre = m["envelope_peak"](t, cells, length)
        x = m["grid"](cells, length)
        i = int(np.argmin(abs(x - centre)))
        before, after = (m["complex_field"](s, cells, length) for s in (t - dt, t + dt))
        omega = -np.angle(after[i] / before[i]) / (2 * dt)
        now = m["complex_field"](t, cells, length)
        k = np.angle(now[i + 1] / now[i - 1]) / (x[i + 1] - x[i - 1])
        # Local values are averages over the finite spectrum: 0.5 % off.
        self.assertAlmostEqual(omega**2 - k**2, 1.0, delta=1e-2)
        self.assertAlmostEqual(k, m["K0"], delta=0.02)

    def test_measured_speeds_product_is_c_squared(self):
        vp, vg = self.m["measured_speeds"](8192, 600.0)
        self.assertGreater(vp, 1.0)          # crest faster than light
        self.assertLess(vg, 1.0)             # envelope slower
        self.assertAlmostEqual(vp, np.sqrt(2), delta=0.015 * np.sqrt(2))
        self.assertAlmostEqual(vg, 1 / np.sqrt(2), delta=0.006)
        self.assertAlmostEqual(vp * vg, 1.0, delta=0.015)

    def test_narrower_spectrum_converges(self):
        # Finite bandwidth causes the percent-level deviation: halving it
        # brings v_g closer to c^2 k_0/omega_0.
        m = self.m
        errors = []
        for dk in (0.1, 0.05):
            m["DK"] = dk
            try:
                errors.append(abs(m["measured_speeds"]()[1] - 1 / np.sqrt(2)))
            finally:
                m["DK"] = 0.1
        self.assertLess(errors[1], 0.5 * errors[0])



if __name__ == "__main__":
    unittest.main(verbosity=2)
