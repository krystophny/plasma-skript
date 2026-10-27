"""Full-orbit models for the drift and mirror animations (numpy only).

Normalized units: |q_alpha| = 1, B_0 = 1, ion mass m_i = 1 (omega_ci = 1) and
the reduced mass ratio m_i/m_e = 16 of the gyration scenes (|omega_ce| = 16),
equal temperatures T_i = T_e, so v_perp,e = 4 v_perp,i.  Lengths are in
units of the ion Larmor radius rho_Li at B_0, time in 1/omega_ci.  E = 0 in the
grad-B, curvature and mirror models; the models after them add E or g.

Orbits come from the Boris push of the Lorentz force dv/dt = (q/m) v x B
(second-order, energy-conserving, no field gradient assumed).  The
guiding centre is R = x + (m_alpha/q_alpha) v x B/B^2 evaluated with the local field,
and the drift speed is the slope of a least-squares line through R(t); it
is compared with the first-order drift formulae.  scripts/check-physics.py
repeats these checks independently.
"""

import numpy as np

MASS_RATIO = 16.0
QM_ION = 1.0                    # q/m [omega_ci/B_0]
QM_ELECTRON = -MASS_RATIO       # q/m, opposite charge, 16 times lighter


def boris(field, qm, x0, v0, dt, steps):
    """Boris push in a static magnetic field; returns t, x (n,3), v (n,3)."""
    x = np.zeros((steps + 1, 3))
    v = np.zeros((steps + 1, 3))
    x[0], v[0] = x0, v0
    # leapfrog: v is staggered by half a step; start with a half-step rotation
    for i in range(steps):
        b = field(x[i])
        t = 0.5 * qm * dt * b
        s = 2 * t / (1 + t @ t)
        vp = v[i] + np.cross(v[i], t)
        v[i + 1] = v[i] + np.cross(vp, s)
        x[i + 1] = x[i] + dt * v[i + 1]
    return np.arange(steps + 1) * dt, x, v


def guiding_centre(field, qm, x, v):
    """R = x + (m/q) v x B/B^2 for arrays x, v of shape (n, 3)."""
    b = np.array([field(p) for p in x])
    return x + np.cross(v, b) / (qm * np.sum(b * b, axis=1))[:, None]


def drift_speed(t, centre):
    """Least-squares slope of the guiding centre for each component."""
    return np.polyfit(t, centre, 1)[0]


# --- grad-B: B = (1 + y/L) e_z -------------------------------------------
GRAD_B_L = 10.0                 # gradient length L/rho_Li [1]


def grad_b_field(p, length=GRAD_B_L):
    return np.array([0.0, 0.0, 1.0 + p[1] / length])


def grad_b_formula(qm, v_perp, length=GRAD_B_L, y=0.0):
    """v_x = (m v_perp^2/2)/(q B) * (-B'/B), from B x grad B along -e_x."""
    b = 1.0 + y / length
    mu_over_q = 0.5 * v_perp**2 / (qm * b)          # (m/q) v_perp^2/(2B) = mu/q
    return -mu_over_q * (1.0 / length) / b


def grad_b_orbit(qm, v_perp, periods=8, steps_per_turn=400, length=GRAD_B_L):
    """Orbit starting with guiding centre at the origin."""
    omega = abs(qm)
    r_l = v_perp / omega
    # v = v_perp e_y, force q v x B along +e_x for q > 0: centre sits at +e_x*sign(q)
    x0 = np.array([-np.sign(qm) * r_l, 0.0, 0.0])
    v0 = np.array([0.0, v_perp, 0.0])
    dt = 2 * np.pi / omega / steps_per_turn
    steps = int(periods * 2 * np.pi / dt)
    field = lambda p: grad_b_field(p, length)
    t, x, v = boris(field, qm, x0, v0, dt, steps)
    return t, x, v, guiding_centre(field, qm, x, v)


# --- toroidal vacuum field: B = B_0 R_0/R e_phi ---------------------------
TORUS_R0 = 40.0                 # major radius R_0/rho_Li [1]


def torus_field(p, r0=TORUS_R0):
    """B = r0/R^2 (-y, x, 0): purely toroidal, |B| = r0/R."""
    rr2 = p[0] ** 2 + p[1] ** 2
    return r0 / rr2 * np.array([-p[1], p[0], 0.0])


def torus_formula(qm, v_par, v_perp, r0=TORUS_R0):
    """v_Z = (m/(q B R)) (v_par^2 + v_perp^2/2) with B R = B_0 R_0 = r0."""
    return (v_par**2 + 0.5 * v_perp**2) / (qm * r0)


def torus_orbit(qm, v_par, v_perp, t_total, steps_per_turn=200, r0=TORUS_R0):
    """Start at R = R_0, Z = 0, phi = 0 (x = R_0); v_par along +phi (+y).

    The particle has its guiding centre at R_0 on the midplane.  Returns
    t, x, v, guiding centre; R = hypot(x, y), Z = z.
    """
    omega = abs(qm)
    r_l = v_perp / omega
    # perpendicular velocity along Z; B along +y: v x B = e_z x e_y... sign handled by centre
    v0 = np.array([0.0, v_par, v_perp])
    b0 = torus_field(np.array([r0, 0.0, 0.0]), r0)
    # centre = x + v x B/(qm B^2) = (r0, 0, 0)  =>  x = centre - v x B/(qm B^2)
    x0 = np.array([r0, 0.0, 0.0]) - np.cross(v0, b0) / (qm * (b0 @ b0))
    dt = 2 * np.pi / omega / steps_per_turn
    steps = int(t_total / dt)
    field = lambda p: torus_field(p, r0)
    t, x, v = boris(field, qm, x0, v0, dt, steps)
    return t, x, v, guiding_centre(field, qm, x, v)


# --- magnetic mirror: B_z = 1 + (R_m - 1)(z/L)^2, B_r = -(r/2) dB_z/dz ----
MIRROR_RATIO = 4.0              # R_m [1]
MIRROR_L = 10.0                 # coil-to-midplane distance L [1] = 30 rho_L0
MIRROR_OMEGA = 3.0              # omega_c0 = q B_0/m [1]; speed v = 1, rho_L0 = v/omega_c0 = 1/3
PITCH_DEG = (18.0, 26.0, 29.0, 31.0, 45.0, 70.0)    # midplane pitch angles


def mirror_field(p, ratio=MIRROR_RATIO, length=MIRROR_L):
    x, y, z = p
    dbz = 2 * (ratio - 1) * z / length**2
    return np.array([-0.5 * x * dbz, -0.5 * y * dbz, 1.0 + (ratio - 1) * (z / length) ** 2])


def loss_cone_angle(ratio=MIRROR_RATIO):
    """Midplane pitch angle [deg] with sin^2(theta) = 1/R_m."""
    return np.degrees(np.arcsin(np.sqrt(1.0 / ratio)))


def mirror_orbit(pitch_deg, x_gc, steps_per_turn=60, t_end=80.0, ratio=MIRROR_RATIO,
                 length=MIRROR_L, escape=1.0):
    """Ion, speed 1, midplane pitch angle theta, guiding centre at (x_gc, 0, 0).

    The orbit stops once |z| > escape * L (reached the mirror throat z = L).
    Returns t, x, v, mu(t)/mu_start and lost; mu = v_perp^2/(2 B) about the local B,
    averaged over one gyro-period, mu_start its first full-period average.
    """
    alpha = np.radians(pitch_deg)
    v_perp, v_par = np.sin(alpha), np.cos(alpha)
    r_l = v_perp / MIRROR_OMEGA
    v0 = np.array([0.0, v_perp, v_par])
    # ion, B = e_z at the midplane: gyro-centre sits +r_l e_x from the particle
    x0 = np.array([x_gc - r_l, 0.0, 0.0])
    dt = 2 * np.pi / MIRROR_OMEGA / steps_per_turn
    steps = int(t_end / dt)
    field = lambda p: MIRROR_OMEGA * mirror_field(p, ratio, length)
    # omega_c = qm*B: qm=1 and B scaled by MIRROR_OMEGA keeps boris unchanged
    t, x, v = boris(field, 1.0, x0, v0, dt, steps)
    out = np.nonzero(np.abs(x[:, 2]) > escape * length)[0]
    n = out[0] + 1 if len(out) else len(t)
    t, x, v = t[:n], x[:n], v[:n]
    b = np.array([mirror_field(p, ratio, length) for p in x])
    bn = np.linalg.norm(b, axis=1)
    v_par_loc = np.sum(v * b, axis=1) / bn
    v_perp2 = np.sum(v * v, axis=1) - v_par_loc**2
    mu = v_perp2 / (2 * bn)
    # gyro-average over one period at the starting omega_c: v_perp about the local
    # B contains the curvature/grad-B drift velocity, which is not part of mu.
    window = max(int(round(2 * np.pi / MIRROR_OMEGA / dt)), 1)
    csum = np.concatenate([[0.0], np.cumsum(mu)])
    idx = np.arange(len(mu))
    lo, hi = np.maximum(idx - window // 2, 0), np.minimum(idx + window // 2 + 1, len(mu))
    mu_avg = (csum[hi] - csum[lo]) / (hi - lo)
    # normalise by the first full-period average; the truncated windows at
    # the start are biased by the gyro-phase.
    ref = mu_avg[min(window // 2, len(mu_avg) - 1)]
    return t, x, v, mu_avg / ref, bool(len(out))


# --- time-dependent fields: E x B frame change, gravity, polarization, mu ---
# Boris push of dv/dt = a(x, t) + (q/m) v x B(x, t) with a = (q/m) E + g, the
# non-magnetic acceleration.  x lives on integer steps t_n = t0 + n dt, v on
# half steps: v[n] is the velocity of the step from x[n-1] to x[n] (v[0] the
# step before the start); a and B are evaluated at (x[n], t_n).


def boris_em(qm, b_field, accel, x0, v_before, dt, steps, t0=0.0):
    """Returns t (n+1), x (n+1, 3), v (n+1, 3) with v on the half steps."""
    x = np.zeros((steps + 1, 3))
    v = np.zeros((steps + 1, 3))
    x[0], v[0] = x0, v_before
    for i in range(steps):
        t = t0 + i * dt
        a = accel(x[i], t)
        h = 0.5 * qm * dt * b_field(x[i], t)
        v_minus = v[i] + 0.5 * dt * a
        v_prime = v_minus + np.cross(v_minus, h)
        v_plus = v_minus + np.cross(v_prime, 2 * h / (1 + h @ h))
        v[i + 1] = v_plus + 0.5 * dt * a
        x[i + 1] = x[i] + dt * v[i + 1]
    return t0 + np.arange(steps + 1) * dt, x, v


def circle_start(qm, b, u, dt, centre, v_drift):
    """Start on the exact discrete gyro-circle of the Boris scheme, B = b e_z.

    In the frame moving with v_drift the particle sits on top of the circle
    (y = centre_y + r) with gyration speed u along +x for q > 0 (clockwise)
    and -x for q < 0.  Returns x0 and v_before (lab frame).
    """
    theta = 2 * np.arctan(0.5 * qm * b * dt)        # signed rotation per step
    r = u * dt / (2 * np.sin(abs(theta) / 2))       # discrete circle radius
    phi = np.pi / 2
    x0 = np.array([centre[0] + r * np.cos(phi), centre[1] + r * np.sin(phi), 0.0])
    x_prev = np.array([centre[0] + r * np.cos(phi + theta),
                       centre[1] + r * np.sin(phi + theta), 0.0])
    return x0, (x0 - x_prev) / dt + np.asarray(v_drift, float)


def uniform_b(b=1.0):
    return lambda x, t: np.array([0.0, 0.0, b])


# E x B frame change: ion, B = e_z out of the page, E = E e_y.
EXB_E = 0.4                     # E/B in units of the drift-frame speed u = rho_L omega_c [1]
EXB_TURNS = 3
EXB_STEPS_PER_TURN = 400


def exb_orbit(e=EXB_E, turns=EXB_TURNS, steps_per_turn=EXB_STEPS_PER_TURN):
    """Ion (q/m = 1, B = 1, u = 1, rho_L = 1), guiding centre at the origin.

    Returns t, x, v, v_D = E x B/B^2 and the drift-frame positions
    x' = x - v_D t.
    """
    e_vec = np.array([0.0, e, 0.0])
    v_d = np.cross(e_vec, [0.0, 0.0, 1.0])          # E x B/B^2
    dt = 2 * np.pi / steps_per_turn
    x0, v_before = circle_start(1.0, 1.0, 1.0, dt, (0.0, 0.0), v_d)
    t, x, v = boris_em(1.0, uniform_b(), lambda p, s: e_vec, x0, v_before, dt,
                       turns * steps_per_turn)
    return t, x, v, v_d, x - np.outer(t, v_d)


def fit_drift_and_gyration(t, x, omega):
    """Least-squares fit x(t) = c + v t + a cos(omega t) + b sin(omega t) per component.

    Returns the drift velocity v (x, y).  omega is the gyrofrequency of the
    scheme (2 arctan(omega_c dt/2)/dt for Boris).
    """
    basis = np.stack([np.ones_like(t), t, np.cos(omega * t), np.sin(omega * t)], axis=1)
    coef = np.linalg.lstsq(basis, x[:, :2], rcond=None)[0]
    return coef[1]


def drift_frame_radius(x_frame):
    """Distances of the drift-frame orbit from its least-squares circle centre."""
    p = x_frame[:, :2]
    # Kasa fit: |p|^2 = 2 c.p + k is linear in (c, k).
    basis = np.column_stack([2 * p, np.ones(len(p))])
    sol = np.linalg.lstsq(basis, np.sum(p * p, axis=1), rcond=None)[0]
    return np.linalg.norm(p - sol[:2], axis=1)


# Gravity drift: B = e_z, g = -g e_y; ion and electron at T_i = T_e.
GRAVITY_G = 0.2                 # g/(rho_Li omega_ci^2) [1]; ion drift 0.2 rho_Li omega_ci


def gravity_formula(qm, g=GRAVITY_G):
    """v_D = (m/q) g x B/B^2 with g = -g e_y, B = e_z: x component."""
    return np.cross([0.0, -g, 0.0], [0.0, 0.0, 1.0])[0] / qm


def gravity_orbit(qm, v_perp, t_end, g=GRAVITY_G, steps_per_turn=200):
    omega = abs(qm)
    dt = 2 * np.pi / omega / steps_per_turn
    v_d = np.array([gravity_formula(qm, g), 0.0, 0.0])
    x0, v_before = circle_start(qm, 1.0, v_perp, dt, (0.0, 0.0), v_d)
    t, x, v = boris_em(qm, uniform_b(), lambda p, s: np.array([0.0, -g, 0.0]), x0,
                       v_before, dt, int(round(t_end / dt)))
    return t, x, v


def averaged_drift(t, x, period):
    """Least-squares slope of the gyro-period boxcar average of x(t)."""
    n = int(round(period / (t[1] - t[0])))
    box = np.array([np.convolve(x[:, k], np.ones(n) / n, mode="valid") for k in range(2)]).T
    tt = t[n // 2:n // 2 + len(box)]
    return np.polyfit(tt, box, 1)[0]


# Polarization drift: B = e_z, E = E(t) e_y switched on smoothly.
POL_E1 = 0.75                   # final E/B in units of v_perp,i [1]
POL_RAMP = 3 * 2 * np.pi        # ramp time omega_ci T_r [1]: three ion turns
POL_T_END = 5 * 2 * np.pi       # run time [1]: ramp plus two ion turns


def pol_e(t, e1=POL_E1, ramp=POL_RAMP):
    """E_y/B(t): (1 - cos(pi t/T_r))/2 from 0 to E_1, smooth slope."""
    s = np.clip(np.asarray(t, float) / ramp, 0.0, 1.0)
    return e1 * 0.5 * (1 - np.cos(np.pi * s))


def pol_exb_shift(t, e1=POL_E1, ramp=POL_RAMP):
    """x_D(t) = integral of E_y/B dt (the E x B displacement along x)."""
    t = np.asarray(t, float)
    inside = 0.5 * e1 * (t - ramp / np.pi * np.sin(np.pi * np.minimum(t, ramp) / ramp))
    return np.where(t <= ramp, inside, 0.5 * e1 * ramp + e1 * (t - ramp))


def pol_formula(qm, t):
    """Guiding-centre shift along E: (m/(q B^2)) E(t) with B = 1."""
    return pol_e(t) / qm


def pol_orbit(qm, v_perp, steps_per_turn=200):
    """Orbit and guiding centre R = x + (m/q)(v - v_E) x B/B^2, v_E = E x B/B^2.

    v is taken at the integer steps (mean of the neighbouring half steps).
    """
    omega = abs(qm)
    dt = 2 * np.pi / omega / steps_per_turn
    x0, v_before = circle_start(qm, 1.0, v_perp, dt, (0.0, 0.0), (0.0, 0.0, 0.0))
    t, x, v = boris_em(qm, uniform_b(), lambda p, s: np.array([0.0, qm * pol_e(s), 0.0]),
                       x0, v_before, dt, int(round(POL_T_END / dt)))
    v_mid = 0.5 * (v[:-1] + v[1:])
    t, x = t[:-1], x[:-1]
    v_e = np.stack([pol_e(t), np.zeros_like(t), np.zeros_like(t)], axis=1)   # E_y e_y x e_z
    centre = x + np.cross(v_mid - v_e, [0.0, 0.0, 1.0]) / qm
    return t, x, centre


# mu in a slowly growing uniform field: the scheme of derivations/plot_mu_ramp.py
# (q = m = 1, B_0 = 1, orbit centred on the axis, E = -(1/2) dB/dt e_z x r with
# dB/dt from the field increment over each step), keeping the trajectory.
MU_TAU = 20.0                   # ramp time omega_c0 tau [1]
MU_HALF = 4 * MU_TAU            # run from -4 tau to 4 tau
MU_STEPS_PER_TURN = 1600


def mu_field(t, tau=MU_TAU):
    """B/B_0 = 3/2 + tanh(t/tau)/2."""
    return 1.5 + 0.5 * np.tanh(np.asarray(t, float) / tau)


def mu_ramp_orbit(tau=MU_TAU, half=MU_HALF, steps_per_turn=MU_STEPS_PER_TURN):
    """Returns t (from 0), B/B_0, orbit radius rho_L/rho_L0, flux/flux_0, mu/mu_0, (x, y).

    Sampled at the half steps: rho_L is the distance from the axis at the
    mean of the neighbouring positions, mu = v^2/(2B) with B at the half step.
    """
    dt = 2 * np.pi / steps_per_turn
    # Exact discrete circle of radius 1 for the field of the first step, so that
    # the orbit is centred and circular even where the window cuts the ramp.
    theta = 2 * np.arctan(mu_field(-half + dt / 2, tau) * dt / 2)
    x = np.array([1.0, 0.0])
    v = np.array([(1 - np.cos(theta)) / dt, -np.sin(theta) / dt])
    n = int(np.ceil(2 * half / dt))
    out = np.empty((n, 6))
    t = -half
    for i in range(n):
        b = mu_field(t + dt / 2, tau)
        b_dot = (mu_field(t + dt, tau) - mu_field(t, tau)) / dt
        e = -0.5 * b_dot * np.array([-x[1], x[0]])
        v_minus = v + 0.5 * dt * e
        h = 0.5 * dt * b
        v_prime = v_minus + h * np.array([v_minus[1], -v_minus[0]])
        v = v_minus + 2 * h / (1 + h * h) * np.array([v_prime[1], -v_prime[0]])
        v = v + 0.5 * dt * e
        x_new = x + dt * v
        mid = 0.5 * (x + x_new)
        out[i] = (t + dt / 2 + half, b, np.linalg.norm(mid), v @ v / (2 * b), mid[0], mid[1])
        x = x_new
        t += dt
    rho = out[:, 2] / out[0, 2]
    flux = rho**2 * out[:, 1] / out[0, 1]
    return out[:, 0], out[:, 1], rho, flux, out[:, 3] / out[0, 3], out[:, 4:6] / out[0, 2]
