"""Illustrative dispersive plasma-wave packet.

The scene uses normalized coordinates and a deliberately separated carrier and
envelope:

    A(x, t) = exp(-(x - v_g t)^2 / (2 sigma^2)) cos(k (x - v_phi t))

with X = x/L0, tau = t/t0, A = E/E0, sigma/L0 = 1.15, k L0 = 5.2,
v_g t0/L0 = 0.42 and v_phi t0/L0 = 0.90 (all unit [1]). The scene runs from
tau = -5 to tau = 5, so the tracked crest X = 0.90 tau (the crest at the
envelope center at tau = 0) enters at the rear of the packet and leaves
through its front. This is a deterministic teaching illustration, not a
numerical solution of a plasma boundary-value problem or measured data.
"""

from manim import *
import numpy as np

from style import (
    PURPLE, CURVE_WIDTH, E_FIELD, EASE, FAINT, LINEAR, MUTED, BLUE,
    THIN_WIDTH, StyledScene, axes, axis_labels, math,
)


def packet_envelope(x, tau, sigma=1.15, group_speed=0.42):
    """X=x/L0, tau=t/t0, sigma/L0=1.15, vg*t0/L0=0.42."""
    return np.exp(-((np.asarray(x) - group_speed*tau)**2)/(2*sigma**2))


def packet_field(x, tau, sigma=1.15, group_speed=0.42, phase_speed=0.90, k=5.2):
    """Prescribed ansatz E/E0, not an exact dispersive-wave solution; k=kdim*L0."""
    return packet_envelope(x, tau, sigma, group_speed) * np.cos(k*(np.asarray(x) - phase_speed*tau))


TAU_START = -5.0
TAU_END = 5.0


class WavePacketPropagation(StyledScene):
    """Show a carrier crest moving faster than its wave-packet envelope."""

    def build(self):
        ax = axes([-6.0, 6.0, 1.0], [-1.3, 1.3, 0.5], 11.6, 4.6).move_to(DOWN * 0.55)
        ax_labels = axis_labels(ax, r"x/L_0\ [1]", r"E/E_0\ [1]")

        group_speed, phase_speed = 0.42, 0.90
        tracker = ValueTracker(TAU_START)
        xs = np.linspace(-6.0, 6.0, 900)

        def field_curve():
            ys = packet_field(xs, tracker.get_value())
            return VMobject(color=E_FIELD, stroke_width=CURVE_WIDTH - 0.5).set_points_smoothly(
                [ax.c2p(x, y) for x, y in zip(xs, ys)])

        def envelope_curve(sign):
            ys = sign * packet_envelope(xs, tracker.get_value())
            return VMobject(color=FAINT, stroke_width=THIN_WIDTH - 0.6).set_points_smoothly(
                [ax.c2p(x, y) for x, y in zip(xs[::6], ys[::6])])

        field = always_redraw(field_curve)
        upper = always_redraw(lambda: envelope_curve(1))
        lower = always_redraw(lambda: envelope_curve(-1))

        def group_marker():
            x = group_speed * tracker.get_value()
            return DashedLine(ax.c2p(x, -1.2), ax.c2p(x, 1.2), color=BLUE,
                              stroke_width=THIN_WIDTH, dash_length=0.12)

        def phase_marker():
            tau = tracker.get_value()
            x = phase_speed * tau
            crest = ax.c2p(x, packet_field(x, tau))
            return VGroup(
                Line(ax.c2p(x, -1.2), ax.c2p(x, 1.2), color=PURPLE, stroke_width=THIN_WIDTH),
                Dot(crest, radius=0.09, color=PURPLE),
            )

        g_mark = always_redraw(group_marker)
        p_mark = always_redraw(phase_marker)

        # Stationary key: line style plus color identifies each marker.
        key_g = VGroup(
            DashedLine(ORIGIN, RIGHT * 0.6, color=BLUE, stroke_width=THIN_WIDTH, dash_length=0.1),
            math(r"v_g", color=BLUE, size=32),
        ).arrange(RIGHT, buff=0.2)
        key_p = VGroup(
            Line(ORIGIN, RIGHT * 0.6, color=PURPLE, stroke_width=THIN_WIDTH),
            math(r"v_\varphi", color=PURPLE, size=32),
        ).arrange(RIGHT, buff=0.2)
        key = VGroup(key_g, key_p).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        key.to_corner(UR, buff=0.55)

        self.play(Create(ax), FadeIn(ax_labels), run_time=0.8, rate_func=EASE)
        self.play(FadeIn(upper), FadeIn(lower), Create(field), run_time=0.8, rate_func=EASE)
        self.play(FadeIn(g_mark), FadeIn(p_mark), FadeIn(key), run_time=0.5, rate_func=EASE)
        self.play(tracker.animate.set_value(TAU_END), run_time=8.0, rate_func=LINEAR)
        self.wait(1.4)
