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
at the respective phase speed.  The three waves run one after the other in
the same full-width row from the same phase, tau = 0 ... TAU_END, and the scene
ends on a still of all three final states stacked.
"""

from manim import *
import numpy as np

from style import (
    ACCENT, B_FIELD, CURVE_WIDTH, EASE, GRID, INK, LINEAR, MUTED, BLUE,
    THIN_WIDTH, StyledScene, label, math,
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
SCREEN_LEFT, SCALE = -3.7, 0.92   # screen x = SCREEN_LEFT + SCALE (X - X_MIN)
ROW_Y = (2.0, 0.0, -2.0)
RUN_Y = 0.0          # the single row used while a wave is running
TAU_END = 8.0
RUN_TIME = 6.0
FINAL_HOLD = 3.0


def sx(x):
    return SCREEN_LEFT + SCALE * (np.asarray(x) - X_MIN)


class MagnetosonicWaves(StyledScene):
    """Sound, shear-Alfven and fast magnetosonic waves in turn, then all three as a still."""

    def build(self):
        k = 1.25
        modes = ("sound", "shear", "fast")
        speeds = {"sound": 0.6, "shear": 1.0, "fast": np.sqrt(1.36)}
        names = {
            "sound": (r"v_s", r"\mathbf{k}\parallel\mathbf{B}_0"),
            "shear": (r"v_A", r"\mathbf{k}\parallel\mathbf{B}_0"),
            "fast": (r"v_m", r"\mathbf{k}\perp\mathbf{B}_0"),
        }
        cols = np.arange(X_MIN + 0.2, X_MAX, 0.4)
        line_x = np.linspace(X_MIN, X_MAX, 240)
        tube_cols = np.arange(X_MIN + 0.25, X_MAX, 0.5)

        def row_label(mode, y):
            speed, geom = names[mode]
            block = VGroup(
                math(speed, color=INK, size=36),
                math(geom, color=MUTED, size=28),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            return block.move_to([-5.6, y, 0], aligned_edge=LEFT)

        def baseline(y):
            return Line([sx(X_MIN), y - 0.62, 0], [sx(X_MAX), y - 0.62, 0],
                        color=GRID, stroke_width=1.2)

        def pattern(mode, y, tau):
            """The wave pattern of one mode in a row centred at y, at time tau."""
            group = VGroup()
            if mode == "sound":
                # Fluid elements (dots) displaced along x = along B0.
                for dy in (-0.33, 0.33):
                    group.add(Line([sx(X_MIN), y + dy, 0], [sx(X_MAX), y + dy, 0],
                                   color=B_FIELD, stroke_width=1.2, stroke_opacity=0.45))
                xs = cols + longitudinal_displacement(cols, tau, "sound")
                group.add(*[Dot([sx(x), y + dy, 0], radius=0.055, color=BLUE)
                            for x in xs for dy in (-0.18, 0.0, 0.18)])
            elif mode == "shear":
                # Field lines bend along y, no compression.
                disp = shear_displacement(line_x, 0.0, tau, amplitude=0.3)[1]
                for dy in (-0.3, 0.0, 0.3):
                    pts = [[sx(x), y + dy + SCALE * d, 0] for x, d in zip(line_x, disp)]
                    group.add(VMobject(color=B_FIELD, stroke_width=THIN_WIDTH + 0.4).set_points_smoothly(pts))
            else:
                # Frozen-in flux tubes (B0 out of page) move with the plasma.
                xs = tube_cols + longitudinal_displacement(tube_cols, tau, "fast")
                for x in xs:
                    for dy in (-0.22, 0.22):
                        p = [sx(x), y + dy, 0]
                        group.add(Circle(radius=0.09, color=B_FIELD, stroke_width=1.8).move_to(p),
                                  Dot(p, radius=0.03, color=B_FIELD))
            # Compression maxima: kx - wt = pi (mod 2 pi); shear crest: pi/2.
            target = np.pi / 2 if mode == "shear" else np.pi
            base = target / k + speeds[mode] * tau
            period = 2 * np.pi / k
            for n in range(-4, 5):
                x = base + n * period
                if X_MIN + 0.1 < x < X_MAX - 0.1:
                    group.add(Triangle(color=ACCENT, fill_opacity=1, stroke_width=0)
                              .scale(0.09).move_to([sx(x), y - 0.62, 0]))
            return group

        def x_label(y):
            lab = math(r"x/L_0\ [1]", color=MUTED, size=28)
            return lab.next_to([sx(X_MAX), y - 0.62, 0], DOWN, buff=0.15).align_to([sx(X_MAX), 0, 0], RIGHT)

        # Sequential runs: one row, same layout, each wave from tau = 0.
        frame = VGroup(baseline(RUN_Y), x_label(RUN_Y))
        self.play(FadeIn(frame), run_time=0.6, rate_func=EASE)
        for mode in modes:
            tau = ValueTracker(0.0)
            wave = always_redraw(lambda mode=mode, tau=tau: pattern(mode, RUN_Y, tau.get_value()))
            tag = row_label(mode, RUN_Y)
            self.play(FadeIn(tag, shift=RIGHT * 0.2), FadeIn(wave), run_time=0.6, rate_func=EASE)
            self.play(tau.animate.set_value(TAU_END), run_time=RUN_TIME, rate_func=LINEAR)
            self.wait(0.5)
            self.play(FadeOut(tag), FadeOut(wave), run_time=0.5, rate_func=EASE)

        # Still of the three final states, stacked; nothing moves.
        still = VGroup(*[VGroup(row_label(mode, y), baseline(y), pattern(mode, y, TAU_END))
                         for mode, y in zip(modes, ROW_Y)], x_label(ROW_Y[2]))
        self.play(FadeOut(frame), run_time=0.4, rate_func=EASE)
        self.play(FadeIn(still), run_time=0.6, rate_func=EASE)
        self.wait(FINAL_HOLD)
