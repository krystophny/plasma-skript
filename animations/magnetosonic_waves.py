"""Schematic warm magnetized-wave comparison.

The scene compares three normalized patterns rather than solving a particular
boundary-value problem: a compressive sound wave (k parallel to B0), a
transverse shear Alfven wave (k parallel to B0, displacement along y), and a
compressional fast magnetosonic wave (k perpendicular to B0, B0 out of the
page). The warm-fluid speed relation for perpendicular propagation

    v_m^2 = v_A^2 + v_s^2

is shown as a model connection, not as dimensional simulation data.

Normalization: X = x/L0, tau = t/t0, displacements in L0, speeds in L0/t0
(all unit [1]): v_s = 0.6, v_A = 1, v_m = sqrt(1.36), k L0 = 1.25.
Longitudinal displacement xi_x = 0.32 sin(kx - omega t) gives the density
perturbation dn/n0 = -d xi_x/dx; in the fast wave the frozen-in flux tubes
move with the plasma, so dB/B0 = dn/n0. Small markers below each row sit at
the compression maxima (sound, fast) or displacement crests (shear) and move
at the respective phase speed.
"""

from manim import *
import numpy as np

from style import (
    ACCENT, B_FIELD, CURVE_WIDTH, EASE, GRID, INK, LINEAR, MUTED, ORANGE,
    THIN_WIDTH, StyledScene, label, math, title,
)


def wave_phase(x, tau, mode, sound_speed=0.6, alfven_speed=1.0, wave_number=1.25):
    """kx-omega*t: x/L0, tau=t/t0, speeds in L0/t0, k in 1/L0.

    Sound is parallel to B0; shear has k parallel B0 along x;
    fast magnetosonic is perpendicular to B0, with cfast²=cs²+vA².
    """
    speeds = {"sound": sound_speed, "shear": alfven_speed,
              "fast": np.sqrt(sound_speed**2 + alfven_speed**2)}
    return wave_number * (np.asarray(x) - speeds[mode] * tau)


def shear_displacement(x, y, tau, amplitude=0.18):
    """Return (xi_x,xi_y)/L0, independent of y: divergence exactly zero."""
    return np.array([np.zeros_like(np.asarray(x), dtype=float),
                     amplitude * np.sin(wave_phase(x, tau, "shear"))])


def longitudinal_displacement(x, tau, mode, amplitude=0.32):
    """xi_x/L0 for the compressive rows; dn/n0 = -d xi_x/dx."""
    return amplitude * np.sin(wave_phase(x, tau, mode))


X_MIN, X_MAX = -5.0, 5.0
SCREEN_LEFT, SCALE = -2.75, 0.92   # screen x = SCREEN_LEFT + SCALE (X - X_MIN)
ROW_Y = (1.55, -0.45, -2.45)


def sx(x):
    return SCREEN_LEFT + SCALE * (np.asarray(x) - X_MIN)


class MagnetosonicWaves(StyledScene):
    """Compare pressure, shear-Alfven, and magnetosonic wave patterns."""

    def build(self):
        heading = title("Sound, Alfvén and magnetosonic waves")
        formula = math(r"v_m^2 = v_A^2 + v_s^2", color=INK, size=36)
        formula.to_corner(UR, buff=0.55)

        tracker = ValueTracker(0.0)
        k = 1.25

        names = [
            ("sound", r"\mathbf{k}\parallel\mathbf{B}_0", r"v_s t_0/L_0 = 0.6\ [1]"),
            ("shear Alfvén", r"\mathbf{k}\parallel\mathbf{B}_0", r"v_A t_0/L_0 = 1\ [1]"),
            ("fast magnetosonic", r"\mathbf{k}\perp\mathbf{B}_0", r"v_m t_0/L_0 = 1.17\ [1]"),
        ]
        row_labels = VGroup()
        for (name, geom, speed), y in zip(names, ROW_Y):
            block = VGroup(
                label(name, color=INK, size=28),
                math(geom, color=MUTED, size=28),
                math(speed, color=MUTED, size=26),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            block.move_to([-6.55, y, 0], aligned_edge=LEFT)
            row_labels.add(block)

        def frame_line(y):
            return Line([sx(X_MIN), y - 0.62, 0], [sx(X_MAX), y - 0.62, 0],
                        color=GRID, stroke_width=1.2)

        baselines = VGroup(*[frame_line(y) for y in ROW_Y])

        # Row 1: sound. Fluid elements (dots) displaced along x = along B0.
        cols = np.arange(X_MIN + 0.2, X_MAX, 0.4)
        sound_y = ROW_Y[0]
        b_guides = VGroup(*[
            Line([sx(X_MIN), sound_y + dy, 0], [sx(X_MAX), sound_y + dy, 0],
                 color=B_FIELD, stroke_width=1.2, stroke_opacity=0.45)
            for dy in (-0.33, 0.33)
        ])

        def sound_dots():
            xs = cols + longitudinal_displacement(cols, tracker.get_value(), "sound")
            return VGroup(*[
                Dot([sx(x), sound_y + dy, 0], radius=0.055, color=ORANGE)
                for x in xs for dy in (-0.18, 0.0, 0.18)
            ])

        # Row 2: shear Alfven. Field lines bend along y, no compression.
        shear_y = ROW_Y[1]
        line_x = np.linspace(X_MIN, X_MAX, 240)

        def shear_lines():
            group = VGroup()
            disp = shear_displacement(line_x, 0.0, tracker.get_value(), amplitude=0.3)[1]
            for dy in (-0.3, 0.0, 0.3):
                pts = [[sx(x), shear_y + dy + SCALE * d, 0] for x, d in zip(line_x, disp)]
                group.add(VMobject(color=B_FIELD, stroke_width=THIN_WIDTH + 0.4).set_points_smoothly(pts))
            return group

        # Row 3: fast wave. Frozen-in flux tubes (B0 out of page) move with the plasma.
        fast_y = ROW_Y[2]
        tube_cols = np.arange(X_MIN + 0.25, X_MAX, 0.5)

        def fast_tubes():
            xs = tube_cols + longitudinal_displacement(tube_cols, tracker.get_value(), "fast")
            group = VGroup()
            for x in xs:
                for dy in (-0.22, 0.22):
                    p = [sx(x), fast_y + dy, 0]
                    group.add(Circle(radius=0.09, color=B_FIELD, stroke_width=1.8).move_to(p),
                              Dot(p, radius=0.03, color=B_FIELD))
            return group

        def phase_markers():
            tau = tracker.get_value()
            group = VGroup()
            # compression maxima: kx - wt = pi (mod 2 pi); shear crest: pi/2.
            for mode, y, target in (("sound", ROW_Y[0], np.pi), ("shear", ROW_Y[1], np.pi / 2),
                                    ("fast", ROW_Y[2], np.pi)):
                speed = {"sound": 0.6, "shear": 1.0, "fast": np.sqrt(1.36)}[mode]
                base = (target / k + speed * tau)
                period = 2 * np.pi / k
                for n in range(-4, 5):
                    x = base + n * period
                    if X_MIN + 0.1 < x < X_MAX - 0.1:
                        group.add(Triangle(color=ACCENT, fill_opacity=1, stroke_width=0)
                                  .scale(0.09).move_to([sx(x), y - 0.62, 0]))
            return group

        x_lab = math(r"x/L_0\ [1]", color=MUTED, size=28)
        x_lab.next_to([sx(X_MAX), ROW_Y[2] - 0.62, 0], DOWN, buff=0.15).align_to([sx(X_MAX), 0, 0], RIGHT)

        dots, lines, tubes = (always_redraw(f) for f in (sound_dots, shear_lines, fast_tubes))
        markers = always_redraw(phase_markers)

        self.play(FadeIn(heading), FadeIn(formula), run_time=0.7, rate_func=EASE)
        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in row_labels], lag_ratio=0.2),
                  FadeIn(baselines), FadeIn(x_lab), run_time=1.0, rate_func=EASE)
        self.play(FadeIn(b_guides), FadeIn(dots), Create(lines), FadeIn(tubes), FadeIn(markers),
                  run_time=0.8, rate_func=EASE)
        self.play(tracker.animate.set_value(8.0), run_time=8.0, rate_func=LINEAR)
        self.wait(1.0)
