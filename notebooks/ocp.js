// Live Debye shielding: the model of animations/debye_shielding_particles.py
// (kin6d case C4) at browser resolution. Classical electrons in a periodic cube
// of edge L with a uniform neutralizing background and a fixed point charge of
// the electron sign at the origin, nu = 4 pi kappa electrons per n_0 lambda_D0^3,
// so that linear response gives delta n_e/n_0 = -kappa e^(-r)/r at T = T_0.
// Particle-mesh Poisson solver (cloud-in-cell, spectral), Langevin thermostat
// (BAOAB splitting) at the slider temperature T.
// Units: lambda_D0, 1/omega_p, k_B T_0 (T is k_B T_e/k_B T_0), Phi in k_B T_0/e:
//   lap Phi = delta n/n_0 + nu delta(r),   dv/dt = grad Phi.

// Radix-2 FFT tables per length n: bit reversal and twiddles.
const tables = new Map();
function table(n) {
  if (!tables.has(n)) {
    const rev = new Uint32Array(n);
    for (let i = 1, j = 0; i < n; i++) {
      let bit = n >> 1;
      for (; j & bit; bit >>= 1) j ^= bit;
      j ^= bit;
      rev[i] = j;
    }
    const cos = new Float64Array(n / 2), sin = new Float64Array(n / 2);
    for (let k = 0; k < n / 2; k++) { cos[k] = Math.cos(2 * Math.PI * k / n); sin[k] = Math.sin(2 * Math.PI * k / n); }
    tables.set(n, {rev, cos, sin, lr: new Float64Array(n), li: new Float64Array(n)});
  }
  return tables.get(n);
}

function fft1(re, im, n, sign, t) {
  const {rev, cos, sin} = t;
  for (let i = 1; i < n; i++) {
    const j = rev[i];
    if (i < j) {
      let x = re[i]; re[i] = re[j]; re[j] = x;
      x = im[i]; im[i] = im[j]; im[j] = x;
    }
  }
  for (let len = 2; len <= n; len <<= 1) {
    const half = len >> 1, stride = n / len;
    for (let i = 0; i < n; i += len) {
      for (let k = 0; k < half; k++) {
        const wr = cos[k * stride], wi = sign * sin[k * stride];
        const a = i + k, b = a + half;
        const tr = re[b] * wr - im[b] * wi, ti = re[b] * wi + im[b] * wr;
        re[b] = re[a] - tr; im[b] = im[a] - ti;
        re[a] += tr; im[a] += ti;
      }
    }
  }
}

// In-place 3D FFT of an n^3 grid stored as idx = (i n + j) n + k; the inverse is normalized.
export function fft3(re, im, n, inverse = false) {
  const t = table(n), {lr, li} = t, sign = inverse ? 1 : -1;
  for (const stride of [1, n, n * n]) {
    for (let a = 0; a < n * n; a++) {
      // Lines along the axis of this stride start at every base with index 0 on that axis.
      const base = stride === 1 ? a * n : stride === n ? Math.floor(a / n) * n * n + (a % n) : a;
      for (let m = 0; m < n; m++) { lr[m] = re[base + m * stride]; li[m] = im[base + m * stride]; }
      fft1(lr, li, n, sign, t);
      for (let m = 0; m < n; m++) { re[base + m * stride] = lr[m]; im[base + m * stride] = li[m]; }
    }
  }
  if (inverse) {
    const s = 1 / (n * n * n);
    for (let i = 0; i < re.length; i++) { re[i] *= s; im[i] *= s; }
  }
}

export function rng(seed) {
  let s = seed >>> 0 || 1;
  const uniform = () => {
    s ^= s << 13; s >>>= 0; s ^= s >>> 17; s ^= s << 5; s >>>= 0;
    return (s + 0.5) / 4294967296;
  };
  let spare = null;
  const normal = () => {
    if (spare !== null) { const v = spare; spare = null; return v; }
    const u = uniform(), v = uniform();
    const r = Math.sqrt(-2 * Math.log(u));
    spare = r * Math.sin(2 * Math.PI * v);
    return r * Math.cos(2 * Math.PI * v);
  };
  return {uniform, normal};
}

const wrap = (x, L) => x - L * Math.floor(x / L + 0.5);   // into [-L/2, L/2)

export function createOCP({L = 4, Lambda = 100, grid = 32, kappa = 0.2, gamma = 0.1,
  bins = 10, seed = 1, T = 1} = {}) {
  const N = Math.round(Lambda * L ** 3), n = grid, h = L / n, cells = n ** 3;
  const random = rng(seed);
  const pos = [new Float64Array(N), new Float64Array(N), new Float64Array(N)];
  const vel = [new Float64Array(N), new Float64Array(N), new Float64Array(N)];
  for (let p = 0; p < N; p++) {
    for (let d = 0; d < 3; d++) {
      pos[d][p] = (random.uniform() - 0.5) * L;
      vel[d][p] = Math.sqrt(T) * random.normal();
    }
  }
  const k2 = new Float64Array(cells);
  for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) for (let k = 0; k < n; k++) {
    const m = (q) => 2 * Math.PI / L * (q < n / 2 ? q : q - n);
    k2[(i * n + j) * n + k] = m(i) ** 2 + m(j) ** 2 + m(k) ** 2;
  }
  const edges = Array.from({length: bins + 1}, (_, b) => b * (L / 2) / bins);
  const sim = {N, L, Lambda, n, h, kappa, gamma, nu: 4 * Math.PI * kappa, pos, vel, k2, random,
    re: new Float64Array(cells), im: new Float64Array(cells),
    grad: [new Float64Array(cells), new Float64Array(cells), new Float64Array(cells)],
    acc: [new Float64Array(N), new Float64Array(N), new Float64Array(N)],
    edges, radii: edges.slice(0, -1).map((r, b) => (r + edges[b + 1]) / 2),
    profile: new Float64Array(bins), averaged: null, time: 0};
  forces(sim);
  return sim;
}

// Cloud-in-cell: nodes at i h - L/2; calls back with the 8 node indices and weights.
function cic(sim, x, y, z, visit) {
  const {n, h, L} = sim;
  const gx = (x + L / 2) / h, gy = (y + L / 2) / h, gz = (z + L / 2) / h;
  const i0 = Math.floor(gx), j0 = Math.floor(gy), k0 = Math.floor(gz);
  const fx = gx - i0, fy = gy - j0, fz = gz - k0;
  for (let a = 0; a < 2; a++) for (let b = 0; b < 2; b++) for (let c = 0; c < 2; c++) {
    const w = (a ? fx : 1 - fx) * (b ? fy : 1 - fy) * (c ? fz : 1 - fz);
    const i = (i0 + a + n) % n, j = (j0 + b + n) % n, k = (k0 + c + n) % n;
    visit((i * n + j) * n + k, w);
  }
}

export function forces(sim) {
  const {N, n, h, L, Lambda, pos, re, im, k2, acc, nu} = sim;
  const cells = n ** 3, perParticle = 1 / (Lambda * h ** 3);
  const [X, Y, Z] = pos;
  re.fill(-1); im.fill(0);
  for (let p = 0; p < N; p++) cic(sim, X[p], Y[p], Z[p], (q, w) => { re[q] += w * perParticle; });
  // The test charge sits on the node at the origin.
  re[((n / 2) * n + n / 2) * n + n / 2] += nu / h ** 3;
  fft3(re, im, n);
  for (let q = 1; q < cells; q++) { const g = -1 / k2[q]; re[q] *= g; im[q] *= g; }
  re[0] = 0; im[0] = 0;
  fft3(re, im, n, true);
  // grad Phi on the nodes by central differences, then interpolated to the particles.
  const [gx, gy, gz] = sim.grad, inv = 1 / (2 * h);
  for (let i = 0; i < n; i++) {
    const ip = ((i + 1) % n) * n * n, im1 = ((i + n - 1) % n) * n * n, i0 = i * n * n;
    for (let j = 0; j < n; j++) {
      const jp = ((j + 1) % n) * n, jm = ((j + n - 1) % n) * n, j0 = j * n;
      for (let k = 0; k < n; k++) {
        const kp = (k + 1) % n, km = (k + n - 1) % n, q = i0 + j0 + k;
        gx[q] = (re[ip + j0 + k] - re[im1 + j0 + k]) * inv;
        gy[q] = (re[i0 + jp + k] - re[i0 + jm + k]) * inv;
        gz[q] = (re[i0 + j0 + kp] - re[i0 + j0 + km]) * inv;
      }
    }
  }
  const [AX, AY, AZ] = acc;
  for (let p = 0; p < N; p++) {
    const fx = (X[p] + L / 2) / h, fy = (Y[p] + L / 2) / h, fz = (Z[p] + L / 2) / h;
    const i0 = Math.floor(fx), j0 = Math.floor(fy), k0 = Math.floor(fz);
    const ux = fx - i0, uy = fy - j0, uz = fz - k0;
    let ax = 0, ay = 0, az = 0;
    for (let a = 0; a < 2; a++) {
      const wa = a ? ux : 1 - ux, I = ((i0 + a + n) % n) * n * n;
      for (let b = 0; b < 2; b++) {
        const wb = wa * (b ? uy : 1 - uy), J = I + ((j0 + b + n) % n) * n;
        for (let c = 0; c < 2; c++) {
          const w = wb * (c ? uz : 1 - uz), q = J + (k0 + c + n) % n;
          ax += w * gx[q]; ay += w * gy[q]; az += w * gz[q];
        }
      }
    }
    AX[p] = ax; AY[p] = ay; AZ[p] = az;
  }
}

// One BAOAB step of length dt at temperature T; updates the shell profile and
// its running average over the time `tau`.
export function step(sim, T, dt = 0.1, tau = 30) {
  const {N, L, pos, vel, acc, gamma, random} = sim;
  const c1 = Math.exp(-gamma * dt), c2 = Math.sqrt((1 - c1 * c1) * T);
  for (let d = 0; d < 3; d++) {
    const x = pos[d], v = vel[d], a = acc[d];
    for (let p = 0; p < N; p++) {
      v[p] += 0.5 * dt * a[p];
      x[p] += 0.5 * dt * v[p];
      v[p] = c1 * v[p] + c2 * random.normal();
      x[p] = wrap(x[p] + 0.5 * dt * v[p], L);
    }
  }
  forces(sim);
  for (let d = 0; d < 3; d++) {
    const v = vel[d], a = acc[d];
    for (let p = 0; p < N; p++) v[p] += 0.5 * dt * a[p];
  }
  sim.time += dt;
  measure(sim);
  if (!sim.averaged) sim.averaged = Float64Array.from(sim.profile);
  const w = Math.min(1, dt / tau);
  for (let b = 0; b < sim.profile.length; b++) sim.averaged[b] += w * (sim.profile[b] - sim.averaged[b]);
}

// delta n_e/n_0 in spherical shells around the test charge.
export function measure(sim) {
  const {N, pos, edges, Lambda, profile} = sim;
  const counts = new Float64Array(profile.length), rmax = edges.at(-1), dr = edges[1];
  for (let p = 0; p < N; p++) {
    const r = Math.hypot(pos[0][p], pos[1][p], pos[2][p]);
    if (r < rmax) counts[Math.floor(r / dr)] += 1;
  }
  for (let b = 0; b < profile.length; b++) {
    const volume = 4 / 3 * Math.PI * (edges[b + 1] ** 3 - edges[b] ** 3);
    profile[b] = counts[b] / (Lambda * volume) - 1;
  }
  return profile;
}

// k_B T_e/k_B T_0 from the kinetic energy.
export function temperature(sim) {
  let s = 0;
  for (let d = 0; d < 3; d++) for (const v of sim.vel[d]) s += v * v;
  return s / (3 * sim.N);
}

// Linear response of the same particle-mesh plasma at temperature T, shell
// averaged on the grid nodes: delta_k = -(S/T) nu/(k^2 + S^2/T), S the CIC
// assignment factor; S = 1 gives -kappa e^(-r sqrt(1/T))/r in an infinite plasma.
export function linearProfile(sim, T) {
  const {n, h, L, k2, nu, edges, radii} = sim;
  const re = new Float64Array(n ** 3), im = new Float64Array(n ** 3);
  const sinc = (x) => (x === 0 ? 1 : Math.sin(x) / x);
  const kk = (q) => 2 * Math.PI / L * (q < n / 2 ? q : q - n);
  for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) for (let k = 0; k < n; k++) {
    const q = (i * n + j) * n + k;
    if (q === 0) continue;
    const S = (sinc(kk(i) * h / 2) * sinc(kk(j) * h / 2) * sinc(kk(k) * h / 2)) ** 2;
    re[q] = -(S / T) * nu / (k2[q] + S * S / T) / h ** 3;
  }
  fft3(re, im, n, true);
  const sum = new Float64Array(radii.length), count = new Float64Array(radii.length);
  for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) for (let k = 0; k < n; k++) {
    const r = Math.hypot(wrap(i * h, L), wrap(j * h, L), wrap(k * h, L));
    const b = Math.floor(r / edges[1]);
    if (b < radii.length) { sum[b] += re[(i * n + j) * n + k]; count[b] += 1; }
  }
  return Array.from(sum, (s, b) => (count[b] ? s / count[b] : NaN));
}
