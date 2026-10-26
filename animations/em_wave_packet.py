"""Phase and group velocity of an electromagnetic wave packet in a plasma.

Model: transverse wave in a cold, unmagnetized electron plasma with fixed
ions, dispersion relation omega^2 = omega_pe^2 + c^2 k^2.  Normalized units:
position x omega_pe/c [1], time omega_pe t [1], wavenumber c k/omega_pe [1],
frequency omega/omega_pe [1], field E/E_0 [1] with E_0 the initial peak
amplitude.

The packet is a superposition of Fourier modes on a periodic domain of length
L = 400 c/omega_pe, each advanced with its own exact frequency omega(k), with a
Gaussian spectrum centred at k_0 = 1 omega_pe/c of width 0.1 omega_pe/c
(envelope width sigma_x = 10 c/omega_pe).  Nothing is prescribed as moving
at v_phi or v_g: a crest is followed as a local maximum of E(x, t) and the
envelope peak as the maximum of |E| of the complex (analytic) field, and both
speeds are least-squares slopes.  The check is v_phi v_g = c^2 with
v_phi = c (1 + omega_pe^2/(c^2 k_0^2))^(1/2) = 1.414 c and v_g = c^2 k_0/omega_0
= 0.707 c; scripts/check-physics.py repeats it on an independent finer grid.
"""

from manim import *
import numpy as np

from style import (
    ACCENT, BLUE, CURVE_WIDTH, E_FIELD, EASE, FAINT, GREEN, INK, LINEAR, MUTED,
    THIN_WIDTH, StyledScene, axes, axis_labels, label, math, MATH_SMALL, MATH_SIZE,
    SMALL_SIZE,
)


K0 = 1.0                # carrier wavenumber c k_0/omega_pe [1]
DK = 0.1                # spectral width [1]; envelope width 1/DK
X0 = 18.0               # initial packet centre x omega_pe/c [1]
LENGTH = 400.0          # periodic domain [1]
CELLS = 4096
T_END = 50.0            # omega_pe t at the end [1]
X_SHOW = 95.0           # visible window 0 <= x <= X_SHOW [1]


def omega(k):
    """omega/omega_pe = (1 + (c k/omega_pe)^2)^(1/2)."""
    return np.sqrt(1.0 + np.asarray(k)**2)


def grid(cells=CELLS, length=LENGTH):
    """Periodic grid from -length/4, so the packet is far from the seam."""
    return (np.arange(cells) - cells // 4) * length / cells


def spectrum(cells=CELLS, length=LENGTH):
    """Wavenumbers and Fourier amplitudes of the complex initial packet."""
    k = 2 * np.pi * np.fft.fftfreq(cells, d=length / cells)
    x = grid(cells, length)
    psi0 = np.exp(-((x - X0) * DK)**2 / 2) * np.exp(1j * K0 * x)
    a = np.fft.fft(psi0)
    a[k < 0] = 0.0      # analytic signal: positive k only
    return k, a


def complex_field(t, cells=CELLS, length=LENGTH):
    """Analytic field psi(x, t); E/E_0 = Re psi and the envelope is |psi|."""
    k, a = spectrum(cells, length)
    return np.fft.ifft(a * np.exp(-1j * omega(k) * t))


def _peak(x, y, i):
    """Sub-cell position of the maximum at index i (parabola through 3 points)."""
    ym, y0, yp = y[i - 1], y[i], y[i + 1]
    return x[i] + 0.5 * (ym - yp) / (ym - 2 * y0 + yp) * (x[1] - x[0])


def envelope_peak(t, cells=CELLS, length=LENGTH):
    x = grid(cells, length)
    env = np.abs(complex_field(t, cells, length))
    return _peak(x, env, int(np.argmax(env)))


def crest_track(times, start, cells=CELLS, length=LENGTH):
    """Follow one crest (local maximum of Re psi) from x = start.

    Each step searches only the nearest maximum to the previous position, so
    the speed is measured, not assumed.
    """
    x = grid(cells, length)
    dx = x[1] - x[0]
    out, pos = [], start
    for t in times:
        e = complex_field(t, cells, length).real
        i0 = int(round((pos - x[0]) / dx))
        half = int(0.5 * np.pi / K0 / dx)          # quarter wavelength
        window = np.arange(i0 - half, i0 + half + 1)
        i = window[np.argmax(e[window])]
        pos = _peak(x, e, i)
        out.append(pos)
    return np.array(out)


def first_crest(cells=CELLS, length=LENGTH):
    """Crest 1.75 envelope widths behind the centre at t = 0, so that it
    ends about as far ahead of the envelope centre."""
    x = grid(cells, length)
    e = complex_field(0.0, cells, length).real
    target = X0 - 1.75 / DK
    peaks = [i for i in range(1, cells - 1) if e[i] > e[i - 1] and e[i] >= e[i + 1]]
    i = min(peaks, key=lambda j: abs(x[j] - target))
    return _peak(x, e, i)


def measured_speeds(cells=CELLS, length=LENGTH, samples=201):
    """(v_phi, v_g)/c from the tracked crest and the envelope peak."""
    times = np.linspace(0.0, T_END, samples)
    crest = crest_track(times, first_crest(cells, length), cells, length)
    centre = np.array([envelope_peak(t, cells, length) for t in times])
    return np.polyfit(times, crest, 1)[0], np.polyfit(times, centre, 1)[0]


def theory_speeds(k=K0):
    w = omega(k)
    return w / k, k / w


class EmWavePacket(StyledScene):
    """Crest faster than light, envelope slower, product c^2."""

    def build(self):
        x = grid()
        shown = (x >= 0) & (x <= X_SHOW)
        xs = x[shown]
        times = np.linspace(0.0, T_END, 201)
        fields = np.array([complex_field(t)[shown] for t in times])
        crest = crest_track(times, first_crest())
        centre = np.array([envelope_peak(t) for t in times])
        vp, vg = measured_speeds()
        vp_th, vg_th = theory_speeds()

        ax = axes([0, X_SHOW, 10], [-1.2, 1.2, 1], 12.4, 2.5).move_to([0.25, 1.6, 0])
        ax_lab = axis_labels(ax, r"x\,\omega_{pe}/c\ [1]", r"E/E_0\ [1]")
        ticks = VGroup(*[math(str(v), color=MUTED, size=MATH_SMALL)
                         .next_to(ax.c2p(v, -1.2), DOWN, buff=0.12) for v in (0, 30, 60)])
        ax_lab[0].next_to(ax.c2p(X_SHOW, -1.2), DOWN, buff=0.12).align_to(ax.c2p(X_SHOW, 0), RIGHT)

        tracker = ValueTracker(0.0)

        def frame(t):
            f = np.interp(t, times, np.arange(len(times)))
            i = min(int(f), len(times) - 2)
            w = f - i
            return (1 - w) * fields[i] + w * fields[i + 1]

        def at(series, t):
            return float(np.interp(t, times, series))

        def wave():
            e = frame(tracker.get_value()).real
            return VMobject(stroke_color=BLUE, stroke_width=CURVE_WIDTH - 1) \
                .set_points_smoothly([ax.c2p(a, b) for a, b in zip(xs[::2], e[::2])])

        def envelope(sign):
            env = np.abs(frame(tracker.get_value()))
            return DashedVMobject(VMobject(stroke_color=FAINT, stroke_width=THIN_WIDTH)
                                  .set_points_smoothly([ax.c2p(a, sign * b)
                                                        for a, b in zip(xs[::8], env[::8])]),
                                  num_dashes=70)

        def crest_marker():
            t = tracker.get_value()
            p = at(crest, t)
            return VGroup(
                Line(ax.c2p(p, 1.02), ax.c2p(p, 1.18), color=E_FIELD, stroke_width=3),
                Dot(ax.c2p(p, 1.18), radius=0.08, color=E_FIELD))

        def group_marker():
            p = at(centre, tracker.get_value())
            return Triangle(color=GREEN, fill_opacity=1, stroke_width=0) \
                .scale(0.13).rotate(PI).move_to(ax.c2p(p, -1.12))

        def light_marker():
            p = X0 + tracker.get_value()
            return DashedLine(ax.c2p(p, -1.2), ax.c2p(p, 1.2), color=INK,
                              stroke_width=THIN_WIDTH, dash_length=0.08)

        # Dispersion diagram of the same packet: chord slope omega/k = v_phi,
        # tangent slope d omega/dk = v_g.
        dax = axes([0, 2.2, 1], [0, 2.6, 1], 3.6, 2.55).move_to([-4.4, -1.95, 0])
        dlab = axis_labels(dax, r"c k/\omega_{pe}\ [1]", r"\omega/\omega_{pe}\ [1]")
        dlab[1].next_to(dax.y_axis.get_top(), RIGHT, buff=0.2)
        dticks = VGroup(
            *[math(str(v), color=MUTED, size=MATH_SMALL).next_to(dax.c2p(v, 0), DOWN, buff=0.12)
              for v in (1, 2)],
            *[math(str(v), color=MUTED, size=MATH_SMALL).next_to(dax.c2p(0, v), LEFT, buff=0.12)
              for v in (1, 2)])
        dlab[0].next_to(dticks[1], RIGHT, buff=0.3)
        branch = dax.plot(lambda k: np.sqrt(1 + k * k), x_range=[0, 2.2], color=BLUE,
                          stroke_width=CURVE_WIDTH - 1)
        light = DashedLine(dax.c2p(0, 0), dax.c2p(2.2, 2.2), color=FAINT,
                           stroke_width=THIN_WIDTH, dash_length=0.08)
        w0 = omega(K0)
        chord = Line(dax.c2p(0, 0), dax.c2p(1.6, 1.6 * w0), color=E_FIELD, stroke_width=3)
        tangent = DashedLine(dax.c2p(0.0, w0 - vg_th), dax.c2p(2.2, w0 + 1.2 * vg_th),
                             color=GREEN, stroke_width=3, dash_length=0.12)
        point = Dot(dax.c2p(K0, w0), radius=0.08, color=INK)

        key = VGroup(
            VGroup(Dot(radius=0.08, color=E_FIELD), math(r"\text{crest } v_\varphi = \omega/k",
                                                          color=E_FIELD, size=MATH_SMALL)).arrange(RIGHT, buff=0.25),
            VGroup(Triangle(color=GREEN, fill_opacity=1, stroke_width=0).scale(0.13).rotate(PI),
                   math(r"\text{envelope } v_g = d\omega/dk", color=GREEN, size=MATH_SMALL)).arrange(RIGHT, buff=0.25),
            VGroup(DashedLine(UP * 0.2, DOWN * 0.2, color=INK, stroke_width=THIN_WIDTH, dash_length=0.08),
                   math(r"\text{light } x = x_0 + c t", color=INK, size=MATH_SMALL)).arrange(RIGHT, buff=0.25),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        result = VGroup(
            math(rf"v_\varphi/c = {vp:.3f},\quad v_g/c = {vg:.3f}", color=INK, size=MATH_SMALL),
            math(rf"v_\varphi v_g/c^2 = {vp * vg:.3f}", color=ACCENT, size=MATH_SMALL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        relation = math(r"\omega^2 = \omega_{pe}^2 + c^2 k^2", color=MUTED, size=MATH_SIZE)
        relation.next_to(dlab[1], RIGHT, buff=0.7)
        VGroup(key, result).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to([2.9, -2.0, 0])

        clock = always_redraw(lambda: math(
            rf"\omega_{{pe}} t = {tracker.get_value():4.1f}\ [1]", color=MUTED, size=MATH_SMALL)
            .next_to(ax.c2p(X_SHOW, 1.2), UP, buff=0.18).align_to(ax.c2p(X_SHOW, 0), RIGHT))

        self.play(Create(ax), FadeIn(ax_lab), FadeIn(ticks), run_time=0.8, rate_func=EASE)
        self.play(Create(dax), FadeIn(dlab), FadeIn(dticks), Create(light), Create(branch),
                  FadeIn(relation), run_time=1.0, rate_func=EASE)
        self.play(Create(chord), Create(tangent), FadeIn(point), FadeIn(key), run_time=1.0,
                  rate_func=EASE)
        lines = VGroup(always_redraw(wave), always_redraw(lambda: envelope(1)),
                       always_redraw(lambda: envelope(-1)))
        markers = VGroup(always_redraw(light_marker), always_redraw(crest_marker),
                         always_redraw(group_marker))
        self.add(lines, markers, clock)
        self.wait(0.8)
        self.play(tracker.animate.set_value(T_END), run_time=14.0, rate_func=LINEAR)
        self.play(FadeIn(result, shift=UP * 0.1), run_time=0.8, rate_func=EASE)
        self.wait(2.5)
