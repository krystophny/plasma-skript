"""Full-orbit models for the drift and mirror animations (numpy only).

Normalized units: |q| = 1, B_0 = 1, ion mass m_i = 1 (Omega_i = 1) and
the reduced mass ratio m_i/m_e = 16 of the gyration scenes (Omega_e = 16),
equal temperatures T_i = T_e, so v_perp,e = 4 v_perp,i.  Lengths are in
units of the ion Larmor radius at B_0, time in 1/Omega_i.  E = 0 everywhere.

Orbits come from the Boris push of the Lorentz force dv/dt = (q/m) v x B
(second-order, energy-conserving, no field gradient assumed).  The
guiding centre is R = x + (m/q) v x B/B^2 evaluated with the local field,
and the drift speed is the slope of a least-squares line through R(t); it
is compared with the first-order drift formulae.  scripts/check-physics.py
repeats these checks independently.
"""

import numpy as np

MASS_RATIO = 16.0
QM_ION = 1.0                    # q/m [Omega_i]
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
GRAD_B_L = 10.0                 # gradient length L/r_Li [1]


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
TORUS_R0 = 40.0                 # major radius R_0/r_Li [1]


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
MIRROR_L = 10.0                 # coil-to-midplane distance L [1] = 30 r_L0
MIRROR_OMEGA = 3.0              # Omega_0 = q B_0/m [1]; speed v = 1, r_L0 = v/Omega_0 = 1/3
PITCH_DEG = (18.0, 26.0, 29.0, 31.0, 45.0, 70.0)    # midplane pitch angles


def mirror_field(p, ratio=MIRROR_RATIO, length=MIRROR_L):
    x, y, z = p
    dbz = 2 * (ratio - 1) * z / length**2
    return np.array([-0.5 * x * dbz, -0.5 * y * dbz, 1.0 + (ratio - 1) * (z / length) ** 2])


def loss_cone_angle(ratio=MIRROR_RATIO):
    """Midplane pitch angle [deg] with sin^2(alpha) = 1/R_m."""
    return np.degrees(np.arcsin(np.sqrt(1.0 / ratio)))


def mirror_orbit(pitch_deg, x_gc, steps_per_turn=60, t_end=80.0, ratio=MIRROR_RATIO,
                 length=MIRROR_L, escape=1.0):
    """Ion, speed 1, midplane pitch angle alpha, guiding centre at (x_gc, 0, 0).

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
    # Omega = qm*B magnitude: qm=1 and B scaled by MIRROR_OMEGA keeps boris unchanged
    t, x, v = boris(field, 1.0, x0, v0, dt, steps)
    out = np.nonzero(np.abs(x[:, 2]) > escape * length)[0]
    n = out[0] + 1 if len(out) else len(t)
    t, x, v = t[:n], x[:n], v[:n]
    b = np.array([mirror_field(p, ratio, length) for p in x])
    bn = np.linalg.norm(b, axis=1)
    v_par_loc = np.sum(v * b, axis=1) / bn
    v_perp2 = np.sum(v * v, axis=1) - v_par_loc**2
    mu = v_perp2 / (2 * bn)
    # gyro-average over one period at the starting Omega: v_perp about the local
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
