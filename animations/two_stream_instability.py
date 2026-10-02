"""Schematic visualization of the cold symmetric two-stream instability.

All quantities are normalized: K = k v0/omega_p, X = x omega_p/v0,
tau = omega_p t, E0 = me v0 omega_p/e, with omega_p based on the TOTAL beam
density.  The growth curve is the cold symmetric dispersion relation
1 = (1/2)/(omega-K)^2 + (1/2)/(omega+K)^2.  The field panel shows the purely
growing linear eigenmode at K = sqrt(3/8), whose real frequency is zero.
The beam panel shows the unperturbed counter-streaming electrons (v/v0 = +1
and -1) as a fixed reference; it is not a particle-in-cell simulation.
"""

from manim import *
import numpy as np

from style import (
    ACCENT, CURVE_WIDTH, DOT_RADIUS, E_FIELD, EASE, ELECTRON, FAINT, GREEN,
    INK, LINEAR, MUTED, SMALL_SIZE, THIN_WIDTH, StyledScene, axes, label,
    math,
)


def growth_rate(k):
    """gamma/omega_p for K=k v0/omega_p; omega_p uses TOTAL beam density."""
    k = np.asarray(k)
    return np.sqrt(np.maximum(0.0, 0.5*np.sqrt(1 + 8*k*k) - k*k - 0.5))


def two_stream_amplitude(tau, k=np.sqrt(3.0/8.0), initial=0.01):
    """E amplitude / E0; tau=omega_p t, E0=me v0 omega_p/e, linear regime."""
    return initial * np.exp(growth_rate(k) * np.asarray(tau))


def two_stream_field(x, tau, k=np.sqrt(3.0/8.0), initial=0.01):
    """Purely growing eigenmode: X=x omega_p/v0; real frequency is zero."""
    return two_stream_amplitude(tau, k, initial) * np.sin(k * np.asarray(x))


K_MAX = np.sqrt(3.0 / 8.0)
WAVELENGTH = 2 * np.pi / K_MAX   # in X = x omega_p / v0
TAU_END = 6.0


class TwoStreamInstability(StyledScene):
    """Show counter-streaming beams, a growing mode and the unstable band."""

    def build(self):
        half = WAVELENGTH

        # Beam panel: v/v0 against X, one row of electrons per beam.
        beam_ax = axes([-half, half, 5], [-1.6, 1.6, 1], 6.4, 1.9,
                       y_axis_config={"include_ticks": False})
        beam_ax.move_to([-3.25, 1.3, 0])
        beam_ylab = math(r"v/v_0\ [1]", color=MUTED, size=30)
        beam_ylab.next_to(beam_ax.y_axis.get_top(), UP, buff=0.12)

        tau = ValueTracker(0.0)
        spacing = 2 * half / 14

        def beam_row(v):
            def make():
                shift = (v * tau.get_value()) % spacing
                xs = np.arange(-half + shift, half, spacing)
                return VGroup(*[Dot(beam_ax.c2p(x, v), radius=DOT_RADIUS, color=ELECTRON)
                                for x in xs])
            return always_redraw(make)

        upper, lower = beam_row(1.0), beam_row(-1.0)
        up_lab = math(r"+1", color=ELECTRON, size=30).next_to(beam_ax.c2p(half, 1.0), RIGHT, buff=0.2)
        lo_lab = math(r"-1", color=ELECTRON, size=30).next_to(beam_ax.c2p(half, -1.0), RIGHT, buff=0.2)

        # Field panel: growing standing pattern with fixed nodes.
        field_ax = axes([-half, half, 5], [-0.1, 0.1, 0.05], 6.4, 2.1,
                        y_axis_config={"include_ticks": False})
        field_ax.move_to([-3.25, -1.7, 0])
        field_ylab = math(r"E/E_0\ [1]", color=MUTED, size=30)
        field_ylab.next_to(field_ax.y_axis.get_top(), UP, buff=0.12)
        field_xlab = math(r"x\,\omega_p/v_0\ [1]", color=MUTED, size=30)
        field_xlab.next_to(field_ax, DOWN, buff=0.1).align_to(field_ax, RIGHT)

        wave = always_redraw(lambda: field_ax.plot(
            lambda x: two_stream_field(x, tau.get_value()),
            x_range=[-half, half, half / 120], color=E_FIELD, stroke_width=CURVE_WIDTH - 0.5))
        nodes = VGroup(*[Dot(field_ax.c2p(x, 0), radius=0.05, color=INK)
                         for x in np.arange(-half, half + 1e-6, half / 2)])

        # Growth-rate panel.
        g_ax = axes([0, 1.35, 0.25], [0, 0.4, 0.1], 4.8, 4.6)
        g_ax.move_to([3.85, -0.2, 0])
        g_xlab = math(r"k v_0/\omega_p\ [1]", color=MUTED, size=30)
        g_xlab.next_to(g_ax.x_axis, DOWN, buff=0.6)
        g_ylab = math(r"\gamma/\omega_p\ [1]", color=MUTED, size=30)
        g_ylab.next_to(g_ax.y_axis.get_top(), UP, buff=0.12)
        curve = g_ax.plot(growth_rate, x_range=[0.0, 1.0, 0.002], color=GREEN,
                          stroke_width=CURVE_WIDTH)
        band = g_ax.get_area(curve, x_range=[0.0, 1.0], color=GREEN, opacity=0.12)
        one_tick = math("1", color=MUTED, size=28).next_to(g_ax.c2p(1.0, 0), DOWN, buff=0.15)
        g_peak = 1 / (2 * np.sqrt(2))
        peak = Dot(g_ax.c2p(K_MAX, g_peak), radius=0.09, color=ACCENT)
        peak_guide = DashedLine(g_ax.c2p(K_MAX, 0), g_ax.c2p(K_MAX, g_peak),
                                color=FAINT, stroke_width=THIN_WIDTH, dash_length=0.08)
        peak_lab = math(r"\gamma_{\max}=\omega_p/(2\sqrt{2})", color=ACCENT, size=30)
        peak_lab.next_to(peak, UP, buff=0.18)
        k_lab = math(r"\sqrt{3/8}", color=MUTED, size=28).next_to(g_ax.c2p(K_MAX, 0), DOWN, buff=0.15)

        self.play(Create(beam_ax), Create(field_ax), Create(g_ax),
                  FadeIn(VGroup(beam_ylab, field_ylab, field_xlab, g_xlab, g_ylab)),
                  run_time=0.9, rate_func=EASE)
        self.play(FadeIn(upper), FadeIn(lower), FadeIn(up_lab), FadeIn(lo_lab),
                  Create(curve), FadeIn(band), FadeIn(one_tick),
                  run_time=1.0, rate_func=EASE)
        self.play(FadeIn(peak_guide), FadeIn(peak), FadeIn(peak_lab), FadeIn(k_lab),
                  FadeIn(wave), FadeIn(nodes), run_time=0.6, rate_func=EASE)
        self.play(tau.animate.set_value(TAU_END), run_time=7.0, rate_func=LINEAR)
        self.wait(1.5)
