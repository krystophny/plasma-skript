// Physics of the interactive notebooks (notebooks/*.qmd), as a plain ES module
// so that the browser (Observable JS) and the tests (node, test_notebooks.py)
// run the same code. Formulas follow derivations/chapters/ch04 and ch05 and
// animations/kernel_smoothing.py; the tests compare them with those sources.

// CODATA 2018, the values of derivations/si.py SI_VALUES and notebook.PROTON_MASS.
export const SI = {
  e: 1.602176634e-19,      // C
  m_e: 9.1093837015e-31,   // kg
  m_p: 1.67262192369e-27,  // kg
  eps0: 8.8541878128e-12,  // F/m
  k_B: 1.380649e-23,       // J/K
};

// (n_e [m^-3], k_B T_e [eV]) of the example plasmas, as derivations/si.py EXAMPLE_PLASMAS.
export const EXAMPLE_PLASMAS = [
  {name: "H II region", n: 1e9, T_eV: 1.0},
  {name: "ionosphere", n: 1e12, T_eV: 1e-1},
  {name: "solar corona", n: 1e15, T_eV: 1e2},
  {name: "Hall thruster", n: 1e18, T_eV: 2e1},
  {name: "tokamak core", n: 1e20, T_eV: 1e4},
];

// ---------------------------------------------------------------- scales
// n [m^-3], T_eV = k_B T_e/e [eV] (k_B T_e = T_eV e joule), B [T].

export function debyeLength(n, T_eV) {
  const {e, eps0} = SI;
  return Math.sqrt(eps0 * T_eV * e / (n * e * e));
}

export function plasmaFrequency(n) {
  const {e, eps0, m_e} = SI;
  return Math.sqrt(n * e * e / (eps0 * m_e));
}

export function debyeNumber(n, T_eV) {
  return 4 / 3 * Math.PI * n * debyeLength(n, T_eV) ** 3;
}

// Gamma = e^2/(4 pi eps0 a k_B T_e), mean spacing a = n^(-1/3).
export function coupling(n, T_eV) {
  const {e, eps0} = SI;
  return e * e * Math.cbrt(n) / (4 * Math.PI * eps0 * T_eV * e);
}

// |omega_c| = e B/m, f_c = |omega_c|/(2 pi), v_th = sqrt(2 k_B T/m), rho_L = v_th/|omega_c|.
export function gyroScales(mass, B, T_eV) {
  const {e} = SI;
  const omega = e * B / mass;
  const v = Math.sqrt(2 * T_eV * e / mass);
  return {omega, f: omega / (2 * Math.PI), v, rho_L: v / omega};
}

export function scales(n, T_eV, B) {
  const omega_pe = plasmaFrequency(n);
  return {
    lambda_D: debyeLength(n, T_eV), omega_pe, f_pe: omega_pe / (2 * Math.PI),
    N_D: debyeNumber(n, T_eV), Gamma: coupling(n, T_eV), a: Math.cbrt(1 / n),
    electron: gyroScales(SI.m_e, B, T_eV), proton: gyroScales(SI.m_p, B, T_eV),
  };
}

// Regime lines in the n-T plane, k_B T_e/e [V] as a function of n:
// lambda_D = L gives e n L^2/eps0; N_D = 1 gives (e/eps0) (3/(4 pi))^(2/3) n^(1/3).
export function temperatureForDebyeLength(n, L) {
  return SI.e * n * L * L / SI.eps0;
}

export function temperatureForUnitDebyeNumber(n) {
  return SI.e / SI.eps0 * (3 / (4 * Math.PI)) ** (2 / 3) * Math.cbrt(n);
}

// ---------------------------------------------------------------- Debye shielding

// Potential [V] of a charge q [C] at r [m]; lambda_D [m].
export function coulombPotential(r, q = SI.e) {
  return q / (4 * Math.PI * SI.eps0 * r);
}

export function screenedPotential(r, lambda_D, q = SI.e) {
  return coulombPotential(r, q) * Math.exp(-r / lambda_D);
}

// epsilon(k) = 1 + 1/(k lambda_D)^2; 1/epsilon = k^2/(k^2 + 1/lambda_D^2) is the
// net charge over the imposed charge of a pattern of wavenumber k.
export function dielectric(k, lambda_D) {
  return 1 + 1 / (k * lambda_D) ** 2;
}

export function survivingFraction(k, lambda_D) {
  return k * k / (k * k + 1 / lambda_D ** 2);
}

// ---------------------------------------------------------------- orbits
// Normalized units: m_alpha = 1, |q_alpha| = 1 (sign s), reference field
// B_0 = 1 and initial v_perp = 1, so |omega_c0| t and lengths in rho_L0 [1];
// E in v_perp B_0, g in v_perp |omega_c0|.

const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const scale = (a, c) => [a[0] * c, a[1] * c, a[2] * c];
const add = (...vs) => vs.reduce((p, v) => [p[0] + v[0], p[1] + v[1], p[2] + v[2]]);
const norm = (a) => Math.sqrt(dot(a, a));

export const CONFIGS = {
  uniform: {label: "uniform B"},
  exb: {label: "E × B"},
  gravity: {label: "gravity"},
  gradb: {label: "grad-B"},
  curvature: {label: "curvature (toroidal vacuum field)"},
  mirror: {label: "magnetic mirror"},
};

// Field model {E, B, g} at r for a configuration with parameters p.
export function fieldModel(config, p) {
  const zero = [0, 0, 0];
  switch (config) {
    case "exb": return (r) => ({E: [p.E, 0, 0], B: [0, 0, 1], g: zero});
    case "gravity": return (r) => ({E: zero, B: [0, 0, 1], g: [p.g, 0, 0]});
    case "gradb": return (r) => ({E: zero, B: [0, 0, 1 + p.kappa * r[0]], g: zero});
    case "curvature": return (r) => {
      // B = B_0 R_0/R e_phi, R distance from the symmetry axis z.
      const R2 = r[0] * r[0] + r[1] * r[1];
      const c = p.R0 / R2;
      return {E: zero, B: [-r[1] * c, r[0] * c, 0], g: zero};
    };
    case "mirror": return (r) => {
      // On-axis B_z = B_0 [1 + (R_m - 1) sin^2(pi z/(2 L))], maxima R_m B_0 at z = +-L;
      // paraxial B_perp = -(r_perp/2) dB_z/dz from div B = 0.
      const k = Math.PI / (2 * p.L);
      const s = Math.sin(k * r[2]);
      const dBz = (p.Rm - 1) * k * Math.sin(2 * k * r[2]);
      return {E: zero, B: [-r[0] / 2 * dBz, -r[1] / 2 * dBz, 1 + (p.Rm - 1) * s * s], g: zero};
    };
    default: return (r) => ({E: zero, B: [0, 0, 1], g: zero});
  }
}

// Analytic guiding-centre drift [v_perp] at the start (lecture formulas, ch05):
// E x B: E x B/B^2; gravity: (m/q) g x B/B^2; grad-B: (mu/q) B x grad B/B^2;
// toroidal vacuum field: (m/(q B R_c)) (v_par^2 + v_perp^2/2) e_R x b.
export function analyticDrift(config, p) {
  const s = p.sign, vperp = 1, vpar = p.vpar;
  switch (config) {
    case "exb": return cross([p.E, 0, 0], [0, 0, 1]);
    case "gravity": return scale(cross([p.g, 0, 0], [0, 0, 1]), 1 / s);
    case "gradb": {
      const mu = vperp * vperp / 2;          // m v_perp^2/(2 B) with B = 1 at the start
      return scale(cross([0, 0, 1], [p.kappa, 0, 0]), mu / s);
    }
    case "curvature": return [0, 0, (vpar * vpar + vperp * vperp / 2) / (s * p.R0)];
    default: return [0, 0, 0];
  }
}

// Mirror: trapped if sin^2 alpha > 1/R_m, i.e. v_par/v_perp < sqrt(R_m - 1);
// mirror point where B(z_m) = B_0 (1 + v_par^2/v_perp^2).
export function mirrorPrediction(p) {
  const ratio = p.vpar * p.vpar / (p.Rm - 1);
  const trapped = ratio < 1;
  return {trapped, z_m: trapped ? 2 * p.L / Math.PI * Math.asin(Math.sqrt(ratio)) : null,
          lossConeDeg: Math.asin(1 / Math.sqrt(p.Rm)) * 180 / Math.PI,
          pitchDeg: Math.atan2(1, p.vpar) * 180 / Math.PI};
}

// Least-squares slope of y(t).
function slope(t, y) {
  const n = t.length;
  let st = 0, sy = 0;
  for (let i = 0; i < n; i++) { st += t[i]; sy += y[i]; }
  const tm = st / n, ym = sy / n;
  let num = 0, den = 0;
  for (let i = 0; i < n; i++) { num += (t[i] - tm) * (y[i] - ym); den += (t[i] - tm) ** 2; }
  return num / den;
}

// Boris push of one particle. p: {sign, vpar, phase, turns, stepsPerTurn, ...field
// parameters}. Starts with the guiding centre at R_start, gyrophase phi:
// v = v_perp (cos phi e_1 - sin phi e_2) + v_par b, r = R + b x v_perp/omega_c.
// Returns samples (at most maxSamples) of t, r, guiding centre R = r - b x v/omega_c,
// mu/mu_0 in the frame of the force drift, and the fitted drift velocity.
export function pushOrbit(config, p, maxSamples = 2500) {
  const field = fieldModel(config, p);
  const s = p.sign;
  const start = config === "curvature" ? [p.R0, 0, 0] : [0, 0, 0];
  const f0 = field(start);
  const b = scale(f0.B, 1 / norm(f0.B));
  // e_1, e_2 perpendicular to b with e_1 x e_2 = b (b = e_z: e_1 = e_x, e_2 = e_y).
  const helper = Math.abs(b[2]) < 0.9 ? [0, 0, 1] : [1, 0, 0];
  const e2 = scale(cross(b, helper), 1 / norm(cross(b, helper)));
  const e1 = cross(e2, b);
  const phi = p.phase ?? 0;
  const vperp0 = add(scale(e1, Math.cos(phi)), scale(e2, -Math.sin(phi)));
  const omega0 = s * norm(f0.B);
  let r = add(start, scale(cross(b, vperp0), 1 / omega0));
  let v = add(vperp0, scale(b, p.vpar));
  const dt = 2 * Math.PI / (p.stepsPerTurn ?? 200);
  const vtot = norm(v);
  let tEnd = 2 * Math.PI * (p.turns ?? 30);
  if (config === "mirror") tEnd = Math.max(tEnd, 16 * p.L / vtot);
  const steps = Math.min(Math.ceil(tEnd / dt), 400000);
  const every = Math.max(1, Math.floor(steps / maxSamples));

  const forceDrift = (f) => {
    const B2 = dot(f.B, f.B);
    const force = add(scale(f.E, s), f.g);          // F/m_alpha with q/m = s
    return scale(cross(force, f.B), 1 / (s * B2));
  };
  const muOf = (f, vel) => {
    const B = norm(f.B), bb = scale(f.B, 1 / B);
    const w = add(vel, scale(forceDrift(f), -1));
    const wpar = dot(w, bb);
    return (dot(w, w) - wpar * wpar) / (2 * B);
  };
  const gcOf = (f, pos, vel) => {
    const B = norm(f.B);
    return add(pos, scale(cross(f.B, vel), -1 / (s * B * B)));  // - b x v/omega_c
  };

  const out = {t: [], x: [], y: [], z: [], X: [], Y: [], Z: [], mu: [], lost: false};
  let mu0 = null;
  let vHalf = v;   // v at t - dt/2, started from v(0)
  for (let n = 0; n <= steps; n++) {
    const t = n * dt;
    const f = field(r);
    // Boris: half electric kick, magnetic rotation, half kick.
    const a = add(scale(f.E, s), f.g);
    const vm = add(vHalf, scale(a, dt / 2));
    const h = scale(f.B, s * dt / 2);
    const vp = add(vm, cross(vm, h));
    const v2 = add(vm, scale(cross(vp, h), 2 / (1 + dot(h, h))));
    const vNew = add(v2, scale(a, dt / 2));
    if (n % every === 0) {
      const vc = scale(add(vHalf, vNew), 0.5);
      const R = gcOf(f, r, vc);
      out.t.push(t); out.x.push(r[0]); out.y.push(r[1]); out.z.push(r[2]);
      out.X.push(R[0]); out.Y.push(R[1]); out.Z.push(R[2]);
      mu0 ??= muOf(f, vc);
      out.mu.push(muOf(f, vc) / mu0);
    }
    if (config === "mirror" && Math.abs(r[2]) > 1.1 * p.L) { out.lost = true; break; }
    vHalf = vNew;
    r = add(r, scale(vNew, dt));
  }
  out.drift = [slope(out.t, out.X), slope(out.t, out.Y), slope(out.t, out.Z)];
  if (config === "curvature") {
    // Radial and toroidal components about the axis at the start point (R_0, 0, 0).
    const Rcyl = out.X.map((x, i) => Math.hypot(x, out.Y[i]));
    out.drift = [slope(out.t, Rcyl), NaN, slope(out.t, out.Z)];
  }
  out.zMax = Math.max(...out.Z.map(Math.abs));
  out.dt = dt;
  out.steps = steps;
  return out;
}

// Magnetic-moment ramp, as derivations/plot_mu_ramp.py: B(t)/B_0 = 3/2 + tanh(t/tau)/2
// along z, E = -(1/2) dB/dt e_z x r, start on the exact discrete circle about the axis,
// E from the field increment over each step. Returns mu_final/mu_initial - 1 and samples.
export function rampField(t, tau) {
  return 1.5 + 0.5 * Math.tanh(t / tau);
}

export function muRamp(tau, stepsPerTurn = 1600, sign = 1, maxSamples = 2500) {
  const half = 8 * tau + 40 * Math.PI;
  const dt = 2 * Math.PI / stepsPerTurn;
  const theta = 2 * Math.atan(dt / 2);
  const rad = dt / (2 * Math.sin(theta / 2));
  let x0 = rad, x1 = 0;
  let v0 = rad * (1 - Math.cos(theta)) / dt, v1 = -sign * rad * Math.sin(theta) / dt;
  const mu0 = 0.5 * (v0 * v0 + v1 * v1) / rampField(-half, tau);
  let t = -half;
  const steps = Math.ceil(2 * half / dt);
  const every = Math.max(1, Math.floor(steps / maxSamples));
  const out = {t: [], x: [], y: [], mu: [], B: []};
  for (let n = 0; n < steps; n++) {
    const b = rampField(t + dt / 2, tau);
    const bDot = (rampField(t + dt, tau) - rampField(t, tau)) / dt;
    const e0 = sign * 0.5 * bDot * x1, e1 = -sign * 0.5 * bDot * x0;   // (q/m) E
    const m0 = v0 + 0.5 * dt * e0, m1 = v1 + 0.5 * dt * e1;
    const h = sign * 0.5 * dt * b;
    const p0 = m0 + h * m1, p1 = m1 - h * m0;
    const c = 2 * h / (1 + h * h);
    v0 = m0 + c * p1 + 0.5 * dt * e0;
    v1 = m1 - c * p0 + 0.5 * dt * e1;
    x0 += dt * v0; x1 += dt * v1;
    t += dt;
    if (n % every === 0) {
      out.t.push(t); out.x.push(x0); out.y.push(x1);
      out.B.push(rampField(t, tau));
      out.mu.push(0.5 * (v0 * v0 + v1 * v1) / rampField(t, tau) / mu0);
    }
  }
  out.deltaMu = 0.5 * (v0 * v0 + v1 * v1) / rampField(t, tau) / mu0 - 1;
  return out;
}

// ---------------------------------------------------------------- kernel smoothing
// Periodic domain of length L, positions x/L [1]. True density, relative to its
// mean n_bar, as animations/kernel_smoothing.py with L = 80 Delta:
// n(x)/n_bar = c [1 + 0.4 sin(2 pi x/L) + 1.5 exp(-(x - 0.65 L)^2/(2 (0.05 L)^2))].
export const PROFILE = {wave: 0.4, bumpX: 0.65, bumpW: 0.05, bumpA: 1.5};
const IMAGES = [-2, -1, 0, 1, 2];
const NORM = 1 / (1 + PROFILE.bumpA * PROFILE.bumpW * Math.sqrt(2 * Math.PI));

const wrap = (d) => d - Math.round(d);

export function trueDensity(x) {
  const d = wrap(x - PROFILE.bumpX);
  return NORM * (1 + PROFILE.wave * Math.sin(2 * Math.PI * x)
                 + PROFILE.bumpA * Math.exp(-d * d / (2 * PROFILE.bumpW ** 2)));
}

// Kernels K_h(u) [1/L] with unit integral over the period.
export function kernel(u, h, shape = "gaussian") {
  let sum = 0;
  if (shape === "tophat") {
    for (const m of IMAGES) if (Math.abs(u + m) <= h) sum += 1 / (2 * h);
    return sum;
  }
  for (const m of IMAGES) sum += Math.exp(-((u + m) ** 2) / (2 * h * h));
  return sum / (Math.sqrt(2 * Math.PI) * h);
}

// n_h(x)/n_bar = (1/N_bar) sum_i K_h(x - x_i), N_bar = n_bar L.
export function smoothed(xs, particles, h, shape, nBar) {
  return xs.map((x) => {
    let s = 0;
    for (const xi of particles) s += kernel(x - xi, h, shape);
    return s / nBar;
  });
}

// Error function from the Chebyshev fit erfcc of Numerical Recipes, |error| < 1.2e-7.
export function erf(x) {
  const z = Math.abs(x);
  const t = 1 / (1 + 0.5 * z);
  const r = t * Math.exp(-z * z - 1.26551223 + t * (1.00002368 + t * (0.37409196 + t * (0.09678418
    + t * (-0.18628806 + t * (0.27886807 + t * (-1.13520398 + t * (1.48851587
    + t * (-0.82215223 + t * 0.17087277)))))))));
  return x >= 0 ? 1 - r : r - 1;
}

// Expected n_h/n_bar = (K_h * n)/n_bar, closed form for the sine plus Gaussian profile.
export function expectedSmoothed(x, h, shape = "gaussian") {
  const k = 2 * Math.PI, w = PROFILE.bumpW;
  if (shape === "tophat") {
    const damp = Math.sin(k * h) / (k * h);
    let bump = 0;
    for (const m of IMAGES) {
      const d = x - PROFILE.bumpX + m;
      bump += w * Math.sqrt(Math.PI / 2) / (2 * h)
        * (erf((d + h) / (w * Math.SQRT2)) - erf((d - h) / (w * Math.SQRT2)));
    }
    return NORM * (1 + PROFILE.wave * damp * Math.sin(k * x) + PROFILE.bumpA * bump);
  }
  const s2 = w * w + h * h;
  let bump = 0;
  for (const m of IMAGES) bump += Math.exp(-((x - PROFILE.bumpX + m) ** 2) / (2 * s2));
  return NORM * (1 + PROFILE.wave * Math.exp(-0.5 * (k * h) ** 2) * Math.sin(k * x)
                 + PROFILE.bumpA * w / Math.sqrt(s2) * bump);
}

// Relative rms noise, averaged over x: sqrt(int K_h^2 / N_bar).
export function noiseRms(h, nBar, shape = "gaussian") {
  if (shape === "tophat") return Math.sqrt(1 / (2 * h * nBar));
  let images = 0;
  for (const m of IMAGES) images += Math.exp(-(m * m) / (4 * h * h));
  return Math.sqrt(images / (2 * Math.sqrt(Math.PI) * h * nBar));
}

// Relative rms bias, (K_h * n - n)/n_bar averaged over x.
export function biasRms(h, shape = "gaussian", points = 1600) {
  let s = 0;
  for (let i = 0; i < points; i++) {
    const x = (i + 0.5) / points;
    s += (expectedSmoothed(x, h, shape) - trueDensity(x)) ** 2;
  }
  return Math.sqrt(s / points);
}

// Seeded generator (mulberry32) for reproducible samples.
export function rng(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6D2B79F5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// Poisson number of positions (mean nBar) drawn from trueDensity by rejection.
export function samplePositions(nBar, seed) {
  const u = rng(seed);
  // Poisson count: product of uniforms for small means, normal approximation above.
  let count;
  if (nBar < 500) {
    const limit = Math.exp(-nBar);
    let k = 0, prod = u();
    while (prod > limit) { k++; prod *= u(); }
    count = k;
  } else {
    const g = Math.sqrt(-2 * Math.log(u() || 1e-300)) * Math.cos(2 * Math.PI * u());
    count = Math.max(0, Math.round(nBar + Math.sqrt(nBar) * g));
  }
  const top = NORM * (1 + PROFILE.wave + PROFILE.bumpA);
  const out = [];
  while (out.length < count) {
    const x = u();
    if (u() * top < trueDensity(x)) out.push(x);
  }
  return out.sort((a, b) => a - b);
}

// ---------------------------------------------------------------- display

const SUPERSCRIPT = {"-": "⁻", "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴",
                     "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹"};

export function superscript(k) {
  return String(k).split("").map((c) => SUPERSCRIPT[c] ?? c).join("");
}

// 7.43e-5 -> "7.43 × 10⁻⁵"; plain decimals between 1e-2 and 1e4.
export function formatSci(v, digits = 3) {
  if (!Number.isFinite(v)) return "–";
  if (v === 0) return "0";
  const a = Math.abs(v);
  if (a >= 1e-2 && a < 10 ** digits) return v.toPrecision(digits);
  let power = Math.floor(Math.log10(a));
  let mantissa = Number((v / 10 ** power).toPrecision(digits));
  if (Math.abs(mantissa) >= 10) { mantissa /= 10; power += 1; }
  return `${mantissa.toPrecision(digits)} × 10${superscript(power)}`;
}

export function powerOfTen(v) {
  return `10${superscript(Math.round(Math.log10(v)))}`;
}
