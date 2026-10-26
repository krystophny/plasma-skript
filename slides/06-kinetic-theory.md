# Kinetic theory

No deck plan yet; this file collects the visuals prepared for the chapter.

## New visuals (2026-10-26)

Two Manim scenes from `animations/kernel_smoothing.py` (dark animation style,
MP4 and poster registered in `media/animations.json`, posters in
`media/posters/`), for the script section `kinetic-distribution`: how a smooth
density follows from a sum of delta functions. One dimension, periodic domain
of length $L=80\,\Delta$, where $\Delta$ is the mean particle spacing; lengths in
$\Delta$ [1], densities as $n\Delta$ [1] (mean 1). Particles are one ideal-gas
(Poisson) sample of a known density
$n(x)\Delta=c\,[1+0.4\sin(2\pi x/L)+1.5\,e^{-(x-52)^2/(2\cdot4^2)}]$ with
mean one, 83 particles. Kernel
$K_h(u)=e^{-u^2/2h^2}/(\sqrt{2\pi}\,h)$, periodic images included. Checked in
`scripts/check-physics.py` (`KernelSmoothingPhysics`) against an FFT
convolution of a fine particle histogram and a separate Monte Carlo.

**`kernel-smoothing`** (35 s, plays once).
- Shown, x axis $x/\Delta$ [1], y axis $n_h\Delta$ [1]:
  1. particles as dots with arrows, the Klimontovich density
     $N(x)=\sum_i\delta(x-x_i)$ (arrows stand for delta functions of weight 1);
  2. a Gaussian of width $h=1.5\,\Delta$ placed on each particle, left to right,
     and their running sum $n_h(x)=\sum_iK_h(x-x_i)$ (orange);
  3. the same result as a convolution
     $n_h=(K_h*N)(x)=\int K_h(x-x')N(x')\,dx'$: the kernel $K_h(x-x')$ (green,
     to the scale of the density axis) slides along $x$; each particle inside
     it carries a green bar $K_h(x-x_i)$; the same bars stacked at $x$ reach the
     orange curve, which is traced point by point. $K_h$ is even, so the
     flipped kernel looks the same; the slide should say so.
- Message: smoothing is a convolution of the Klimontovich density with a
  kernel; it conserves the particle number ($\int n_h\,dx=N$).

**`kernel-width`** (26 s).
- Computed: the same particles smoothed with $h$ from $0.25\Delta$ to
  $20\Delta$; true $n(x)$ dashed. Lower panel, both axes logarithmic: rms over
  $x$ of the error of $n_h\Delta$ [1] against $h/\Delta$ [1]. Noise
  $n_h-K_h*n$ from 300 independent samples (dots) against the Poisson result
  $\sqrt{\bar n/(2\sqrt\pi\,h)}$ (dashed), bias $K_h*n-n$ (exact, green line),
  total $n_h-n$ (squares); a dashed marker follows the current $h$.
- Shown: $h\ll\Delta$ gives back the spikes (values above 4 are clipped and
  marked with triangles); $h=1.5\Delta$ resolves the bump, rms noise
  $0.43\,\bar n$; $h=20\Delta$ is smooth but the bump is washed out (peak 1.06
  instead of 1.83); the least rms error lies at $h\approx6\Delta$
  (0.27 $\bar n$), where noise and bias are equal and the bump is already
  flattened to 1.31. The best width depends on what is to be resolved.
- Honest statistics: the smoothed density is an estimate. For uncorrelated
  particles its relative noise is $1/\sqrt{N_h}$ with $N_h=2\sqrt\pi\,nh$
  particles per kernel width in 1D and $N_h=n(2\sqrt\pi\,h)^3$ in 3D. The
  measured noise agrees with this to 1 % for $h\le 20\Delta$.
- Link to `thermal-charge-fluctuations` (chapter 4): there the electrons are
  smoothed with a 3D Gaussian of width $0.4\lambda_D$ at $n\lambda_D^3=30$, so
  $N_h=86$ and an uncorrelated gas would show $\delta n_e/n_0=0.11$ rms; the
  Debye-Hückel correlations of the plasma lower this to 0.099
  (`debye_hueckel_variance` in that scene).
- Optional extension, not rendered: the same operation on particle velocities
  gives a smooth $f_h(v)$; the kernel width then trades velocity resolution
  against noise in the same way.
