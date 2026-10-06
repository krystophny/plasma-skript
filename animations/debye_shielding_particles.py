"""Debye shielding emerging from electron dynamics (kin6d particle data).

Data: kin6d ``ocp_shielding_demo --export`` (case C4, see
animations/data/kin6d/debye-shielding-particles/README.md and
provenance.json).  Classical electron one-component plasma in a periodic cube
of edge L = 4 lambda_D with a uniform neutralizing background, bare Coulomb
interaction (particle-mesh Ewald, no softening), Lambda = n lambda_D^3 = 100
(N = 6400 electrons), and a fixed repulsive point charge Q at the origin of
the same sign as the electrons (nonlinear radius r_nl = kappa lambda_D,
kappa = 0.05), compensated in the background.  Plasma units: lambda_D,
omega_p, k_B T.

Left: one realization, the electrons of the slab |z| < lambda_D/2 around Q,
projected onto (x, y) (markers fade in and out at the slab faces; positions
between the exported samples, 0.2/omega_p apart, are interpolated linearly
for display).  Right: the measured density deficit -delta n_e/(kappa n_0) in
spherical shells around Q, averaged over time up to the displayed instant and
over 8 independent realizations, against the linear-response Debye reference
of the periodic box (periodic screened-Poisson Green function, bin-averaged)
and the unscreened response 1/r.  At the end the 95% Student-t interval over
realizations of the final profile is drawn.  Statistical evidence only: no
deterministic certificate, and the single-realization snapshot on the left is
not expected to show the deficit by eye.
"""

from manim import *
import numpy as np

from kin6d_data import Export
from style import (
    AXIS, AXIS_WIDTH, BG, CURVE_WIDTH, EASE, ELECTRON, FAINT, GRID, INK, ION,
    LINEAR, MUTED, THIN_WIDTH, StyledScene, axes, label, math, MATH_SMALL,
    SMALL_SIZE,
)

SLAB = 0.5              # displayed slab half-thickness in lambda_D
FADE = 0.1              # fade width at the slab faces
SIDE = 4.8              # particle panel side in Manim units
PLAY_TIME = 13.0
Y_RANGE = (-1.0, 6.0)


class DebyeShieldingParticles(StyledScene):
    """Electrons around a fixed repulsive charge; averaged deficit vs Debye."""

    def build(self):
        data = Export("debye-shielding-particles")
        pos = data["positions"]                    # (3, N, frames)
        times = data["t"]
        r = data["r"]
        kappa = data.parameters["kappa"]
        box = data.parameters["box"]
        running = -data["dn_running"] / kappa      # (bins, frames)
        interval = -data["dn_interval"] / kappa    # (bins, 3): mean, lower, upper
        periodic = -data["periodic"]
        bare = -data["bare"]
        frames = len(times)
        half = box / 2

        tracker = ValueTracker(0.0)

        def frame_pos(u):
            f = u * (frames - 1)
            i = min(int(f), frames - 2)
            return f, i, f - i

        def positions(u):
            _, i, w = frame_pos(u)
            a, b = pos[:, :, i], pos[:, :, i + 1]
            step = b - a
            step -= box * np.round(step / box)     # minimum image between samples
            p = a + w * step
            return p - box * np.round(p / box)

        # --- left: particle slab -----------------------------------------
        center = np.array([-3.85, -0.1, 0.0])

        def pp(x, y):
            return center + np.array([x, y, 0.0]) * SIDE / box

        background = Square(SIDE, stroke_width=0, fill_color=ION, fill_opacity=0.10).move_to(center)
        frame = Square(SIDE, color=GRID, stroke_width=AXIS_WIDTH).move_to(center)
        debye_circle = DashedVMobject(Circle(radius=SIDE / box, color=FAINT,
                                             stroke_width=THIN_WIDTH), num_dashes=36).move_to(center)
        charge = VGroup(
            Circle(radius=0.17, color=INK, fill_color=INK, fill_opacity=1, stroke_width=0),
            math("-", color=BG, size=34),
        ).move_to(center)
        ticks = VGroup()
        for v in (-2, -1, 0, 1, 2):
            bottom = pp(v, -half)
            left = pp(-half, v)
            ticks.add(Line(bottom, bottom + DOWN * 0.08, color=AXIS, stroke_width=AXIS_WIDTH),
                      math(str(v), color=MUTED, size=MATH_SMALL).next_to(bottom, DOWN, buff=0.12),
                      Line(left, left + LEFT * 0.08, color=AXIS, stroke_width=AXIS_WIDTH),
                      math(str(v), color=MUTED, size=MATH_SMALL).next_to(left, LEFT, buff=0.12))
        x_lab = math(r"x/\lambda_D\ [1]", color=MUTED, size=MATH_SMALL).next_to(
            frame, DOWN, buff=0.12).align_to(frame, RIGHT).shift(DOWN * 0.36)
        y_lab = math(r"y/\lambda_D\ [1]", color=MUTED, size=MATH_SMALL).next_to(
            frame, UP, buff=0.15).align_to(frame, LEFT).shift(LEFT * 0.4)

        in_slab = np.abs(pos[2]) < SLAB + 0.05
        pool = int(in_slab.sum(axis=0).max() * 1.15) + 20
        dots = VGroup(*[Dot(center, radius=0.04, color=ELECTRON, fill_opacity=0)
                        for _ in range(pool)])

        def update_dots(group):
            p = positions(tracker.get_value())
            z = np.abs(p[2])
            idx = np.nonzero(z < SLAB)[0]
            alpha = np.clip((SLAB - z[idx]) / FADE, 0.0, 1.0)
            for k, dot in enumerate(group):
                if k < len(idx):
                    j = idx[k]
                    dot.move_to(pp(p[0, j], p[1, j]))
                    dot.set_fill(opacity=alpha[k])
                else:
                    dot.set_fill(opacity=0)

        dots.add_updater(update_dots)
        update_dots(dots)

        legend = VGroup(
            VGroup(Square(0.26, stroke_width=0, fill_color=ION, fill_opacity=0.35),
                   math(r"+en_0", color=MUTED, size=MATH_SMALL)).arrange(RIGHT, buff=0.12),
            VGroup(charge.copy().scale(0.8), math("Q", color=MUTED, size=MATH_SMALL))
            .arrange(RIGHT, buff=0.12),
            VGroup(DashedLine(ORIGIN, RIGHT * 0.45, color=FAINT, stroke_width=THIN_WIDTH,
                              dash_length=0.08),
                   math(r"r=\lambda_D", color=MUTED, size=MATH_SMALL)).arrange(RIGHT, buff=0.12),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        legend.next_to(frame, RIGHT, buff=0.25).align_to(frame, UP)

        # --- right: averaged deficit profile ------------------------------
        ax = axes([0, 2, 0.5], [Y_RANGE[0], Y_RANGE[1], 1], 5.0, 4.6).move_to([3.95, -0.1, 0])
        # The r axis sits at the bottom of the plot, not at the zero line.
        ax.x_axis.set_opacity(0)
        r_axis = VGroup(Line(ax.c2p(0, Y_RANGE[0]), ax.c2p(2, Y_RANGE[0]), color=AXIS,
                             stroke_width=AXIS_WIDTH), *[
            Line(ax.c2p(v, Y_RANGE[0]), ax.c2p(v, Y_RANGE[0]) + DOWN * 0.08, color=AXIS,
                 stroke_width=AXIS_WIDTH) for v in (0, 0.5, 1, 1.5, 2)])
        ax_ticks = VGroup(*[
            math(f"{v:g}", color=MUTED, size=MATH_SMALL).next_to(ax.c2p(v, Y_RANGE[0]), DOWN, buff=0.14)
            for v in (0, 1, 2)], *[
            math(str(v), color=MUTED, size=MATH_SMALL).next_to(ax.c2p(0, v), LEFT, buff=0.14)
            for v in (0, 2, 4, 6)])
        r_lab = math(r"r/\lambda_D\ [1]", color=MUTED, size=MATH_SMALL).next_to(
            ax.c2p(2, Y_RANGE[0]), DOWN, buff=0.14).align_to(ax.c2p(2, 0), RIGHT).shift(DOWN * 0.45)
        dn_lab = math(r"-\delta n_e/(\kappa n_0)\ [1]", color=ELECTRON, size=MATH_SMALL).next_to(
            ax.y_axis.get_top(), UP, buff=0.18).align_to(ax.y_axis, LEFT).shift(LEFT * 0.3)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(2, 0), color=GRID, stroke_width=THIN_WIDTH,
                          dash_length=0.08)

        def clipped_points(values):
            pts = [(x, v) for x, v in zip(r, values) if Y_RANGE[0] <= v <= Y_RANGE[1]]
            return [ax.c2p(x, v) for x, v in pts]

        def curve(values, **style):
            return VMobject(**style).set_points_smoothly(clipped_points(values))

        debye = curve(periodic, color=INK, stroke_width=THIN_WIDTH + 0.6)
        unscreened = DashedVMobject(curve(bare, color=FAINT, stroke_width=THIN_WIDTH),
                                    num_dashes=40)
        debye_label = label("Debye", color=INK, size=SMALL_SIZE).move_to(ax.c2p(0.55, 4.6))
        bare_label = math(r"1/r", color=FAINT, size=MATH_SMALL).move_to(ax.c2p(1.6, 1.05))

        def measured():
            _, i, w = frame_pos(tracker.get_value())
            values = (1 - w) * running[:, i] + w * running[:, i + 1]
            group = VGroup()
            for x, v in zip(r, values):
                if Y_RANGE[0] <= v <= Y_RANGE[1]:
                    group.add(Dot(ax.c2p(x, v), radius=0.065, color=ELECTRON))
            return group

        points = always_redraw(measured)
        bars = VGroup(*[
            Line(ax.c2p(x, max(lo, Y_RANGE[0])), ax.c2p(x, min(hi, Y_RANGE[1])),
                 color=ELECTRON, stroke_width=THIN_WIDTH)
            for x, lo, hi in zip(r, interval[:, 1], interval[:, 2])
            if hi >= Y_RANGE[0] and lo <= Y_RANGE[1]])

        clock_label = math(r"\omega_p t=", color=MUTED, size=MATH_SMALL)
        clock_label.next_to(ax.c2p(2, Y_RANGE[1]), DOWN, buff=0.1).shift(LEFT * 1.1)
        clock = DecimalNumber(times[0], num_decimal_places=1, color=INK, font_size=MATH_SMALL)

        def place_clock(m):
            f, i, w = frame_pos(tracker.get_value())
            m.set_value(times[i] + w * (times[i + 1] - times[i]))
            m.next_to(clock_label, RIGHT, buff=0.12)

        clock.add_updater(place_clock)
        place_clock(clock)

        self.play(FadeIn(background), Create(frame), FadeIn(ticks), FadeIn(x_lab), FadeIn(y_lab),
                  Create(ax), FadeIn(r_axis), FadeIn(ax_ticks), FadeIn(r_lab), FadeIn(dn_lab), FadeIn(zero),
                  run_time=1.0, rate_func=EASE)
        self.play(FadeIn(dots), FadeIn(charge), FadeIn(debye_circle), FadeIn(legend),
                  Create(debye), Create(unscreened), FadeIn(debye_label), FadeIn(bare_label),
                  FadeIn(clock_label), FadeIn(clock), run_time=1.0, rate_func=EASE)
        self.add(points)
        self.play(tracker.animate.set_value(1.0), run_time=PLAY_TIME, rate_func=LINEAR)
        self.play(FadeIn(bars), run_time=0.6, rate_func=EASE)
        self.wait(1.6)
