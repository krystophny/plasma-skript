"""Electromagnetic wave at a plasma edge, below and above omega_pe (kin6d data).

Data: kin6d ``em_slab_demo --export`` (animations/data/kin6d/
em-wave-plasma-reflection/ with README.md and provenance.json).  A plane wave
of amplitude E_0 (a_0 = eE_0/(m_e omega c) = 0.01 and 0.0025) falls at normal
incidence from vacuum (x < 0) onto a cold electron plasma of uniform density
n_0 (x > 0) with fixed ions.  kin6d integrates the one-dimensional
relativistic Vlasov-Maxwell system: E_y, B_z (and E_x) on a staggered Yee
grid with absorbing ends, cold electron macroparticle sheets pushed with the
relativistic Boris scheme.  Lengths in c/omega_pe, time in 1/omega_pe, SI
otherwise.

Two runs on the same plasma, one after the other:
  omega = 0.5 omega_pe: the electrons near the surface follow the field and
  oscillate collectively; their current cancels the wave inside, which is
  reflected (|R| = 1) and decays over the skin depth
  delta = c/sqrt(omega_pe^2 - omega^2).
  omega = 2 omega_pe: the electrons are too inert to follow (displacement
  ~ eE/(m omega^2)), the wave is transmitted with
  T = 2/(1 + N), N = sqrt(1 - omega_pe^2/omega^2), and the wavelength
  2 pi c/sqrt(omega^2 - omega_pe^2).

Left: sample electron sheets within 4 c/omega_pe of the surface; each column
of dots is one sheet, displaced along y by its kin6d transverse displacement
times DISPLAY_GAIN (the second-order longitudinal motion is not drawn).
Right: E_y(x, t)/E_0 from kin6d; at the end of each run the steady
linear-theory envelope +-|E_y|/E_0 (vacuum standing wave, evanescent or
transmitted field) is overlaid.  Fields between the exported frames are
interpolated linearly in time for display.
"""

from manim import *
import numpy as np

from kin6d_data import Export
from style import (
    AXIS, AXIS_WIDTH, CURVE_WIDTH, E_FIELD, EASE, ELECTRON, FAINT, GRID, INK, ION,
    LINEAR, MUTED, THIN_WIDTH, StyledScene, axes, label, math, MATH_SMALL,
    SMALL_SIZE,
)


DATA = Export("em-wave-plasma-reflection")
X = DATA["x"]                       # display grid, x - x_edge [c/omega_pe]
X0 = DATA["x0"]                     # initial sheet positions [c/omega_pe]
AMPLITUDE = DATA.parameters["amplitude"]
RUNS = {
    "low": DATA.parameters["omega_low"],
    "high": DATA.parameters["omega_high"],
}
DISPLAY_GAIN = 30.0                 # drawn y displacement / physical displacement
SHEET_STEP = 2                      # draw every second exported sheet
ROWS = 7
E_RANGE = 2.2
# Physical time shown per run: wave arrival and steady state, then the
# envelope overlay while the run continues.
PLAY = {"low": (0.0, 72.0, 12.0, 96.0, 4.0), "high": (0.0, 48.0, 11.0, 60.0, 3.0)}


def frame_weights(run, t):
    """Bracketing frame index and linear weight for physical time t."""
    times = DATA["t_" + run]
    i = int(np.clip(np.searchsorted(times, t, side="right") - 1, 0, len(times) - 2))
    w = float(np.clip((t - times[i]) / (times[i + 1] - times[i]), 0.0, 1.0))
    return i, w


def field(run, t):
    """E_y/E_0 on the display grid X at time t (kin6d frames)."""
    i, w = frame_weights(run, t)
    ey = DATA["ey_" + run]
    return (1 - w) * ey[:, i] + w * ey[:, i + 1]


def transverse(run, t):
    """Transverse displacement y of the sample sheets at time t [c/omega_pe]."""
    i, w = frame_weights(run, t)
    y = DATA["y_" + run]
    return (1 - w) * y[:, i] + w * y[:, i + 1]


class EmWavePlasmaReflection(StyledScene):
    """Reflection below and transmission above the electron plasma frequency."""

    def build(self):
        tracker = ValueTracker(0.0)
        state = {"run": "low"}

        # --- left: electron sheets near the surface -----------------------
        x_lo, x_hi = -0.6, 4.0
        left = axes([x_lo, x_hi, 1], [-1, 1, 1], 4.6, 4.2).move_to([-4.15, -0.45, 0])
        left.y_axis.set_opacity(0)
        left.x_axis.set_opacity(0)
        bottom = left.c2p(x_lo, -1)[1]
        top = left.c2p(x_lo, 1)[1]

        def lp(x, y):
            return left.c2p(x, y)

        plasma_left = Rectangle(width=lp(x_hi, 0)[0] - lp(0, 0)[0], height=top - bottom,
                                stroke_width=0, fill_color=ION, fill_opacity=0.10)
        plasma_left.move_to([(lp(x_hi, 0)[0] + lp(0, 0)[0]) / 2, (top + bottom) / 2, 0])
        x_axis_left = Line(lp(x_lo, -1), lp(x_hi, -1), color=AXIS, stroke_width=AXIS_WIDTH)
        ticks_left = VGroup()
        for v in range(0, 5):
            ticks_left.add(Line(lp(v, -1), lp(v, -1) + DOWN * 0.08, color=AXIS,
                                stroke_width=AXIS_WIDTH),
                           math(str(v), color=MUTED, size=MATH_SMALL).next_to(
                               lp(v, -1), DOWN, buff=0.14))
        x_lab_left = math(r"x\,\omega_{pe}/c\ [1]", color=MUTED, size=MATH_SMALL)
        x_lab_left.next_to(lp(x_hi, -1), DOWN, buff=0.14).align_to(
            lp(x_hi, -1), RIGHT).shift(DOWN * 0.45)
        edge_left = DashedLine(lp(0, -1), lp(0, 1), color=FAINT, stroke_width=THIN_WIDTH,
                               dash_length=0.08)
        gain_lab = math(r"y \times %d" % int(DISPLAY_GAIN), color=MUTED, size=MATH_SMALL)
        gain_lab.next_to(lp(x_lo, 1), UP, buff=0.12).align_to(lp(x_lo, 1), LEFT)
        electrons_lab = label("electrons", color=ELECTRON, size=SMALL_SIZE)
        electrons_lab.next_to(lp(x_hi, 1), UP, buff=0.12).align_to(lp(x_hi, 1), RIGHT)

        sheets = np.arange(0, len(X0), SHEET_STEP)
        rows = np.linspace(-0.6, 0.6, ROWS)
        units_per_length = (lp(1, 0)[0] - lp(0, 0)[0])
        dots = VGroup(*[Dot(lp(X0[s], r), radius=0.035, color=ELECTRON)
                        for s in sheets for r in rows])

        def update_dots(group):
            shift = transverse(state["run"], tracker.get_value())[sheets]
            k = 0
            for j, s in enumerate(sheets):
                dy = DISPLAY_GAIN * shift[j] * units_per_length
                for r in rows:
                    group[k].move_to(lp(X0[s], r) + UP * dy)
                    k += 1

        dots.add_updater(update_dots)

        # --- right: E_y(x, t) ---------------------------------------------
        ax = axes([-15, 10, 5], [-E_RANGE, E_RANGE, 1], 7.2, 4.2).move_to([2.95, -0.45, 0])
        ax.x_axis.set_opacity(0)
        x_axis = VGroup(Line(ax.c2p(-15, -E_RANGE), ax.c2p(10, -E_RANGE), color=AXIS,
                             stroke_width=AXIS_WIDTH), *[
            Line(ax.c2p(v, -E_RANGE), ax.c2p(v, -E_RANGE) + DOWN * 0.08, color=AXIS,
                 stroke_width=AXIS_WIDTH) for v in (-15, -10, -5, 0, 5, 10)])
        x_ticks = VGroup(*[
            math(str(v), color=MUTED, size=MATH_SMALL).next_to(ax.c2p(v, -E_RANGE), DOWN,
                                                              buff=0.14)
            for v in (-15, -10, -5, 0, 5, 10)])
        y_ticks = VGroup(*[
            math(str(v), color=MUTED, size=MATH_SMALL).next_to(ax.c2p(-15, v), LEFT,
                                                              buff=0.14)
            for v in (-2, 0, 2)])
        x_lab = math(r"x\,\omega_{pe}/c\ [1]", color=MUTED, size=MATH_SMALL)
        x_lab.next_to(ax.c2p(10, -E_RANGE), DOWN, buff=0.14).align_to(
            ax.c2p(10, 0), RIGHT).shift(DOWN * 0.45)
        y_lab = math(r"E_y/E_0\ [1]", color=E_FIELD, size=MATH_SMALL)
        y_lab.next_to(ax.c2p(-15, E_RANGE), UP, buff=0.12).align_to(
            ax.c2p(-15, 0), LEFT).shift(LEFT * 0.3)
        plasma_right = Rectangle(width=ax.c2p(10, 0)[0] - ax.c2p(0, 0)[0],
                                 height=ax.c2p(0, E_RANGE)[1] - ax.c2p(0, -E_RANGE)[1],
                                 stroke_width=0, fill_color=ION, fill_opacity=0.10)
        plasma_right.move_to([(ax.c2p(10, 0)[0] + ax.c2p(0, 0)[0]) / 2, ax.c2p(0, 0)[1], 0])
        edge_right = DashedLine(ax.c2p(0, -E_RANGE), ax.c2p(0, E_RANGE), color=FAINT,
                                stroke_width=THIN_WIDTH, dash_length=0.08)
        vacuum_lab = label("vacuum", color=MUTED, size=SMALL_SIZE).next_to(
            ax.c2p(-4.0, E_RANGE), UP, buff=0.12)
        plasma_lab = label("plasma", color=MUTED, size=SMALL_SIZE).next_to(
            ax.c2p(5, E_RANGE), UP, buff=0.12)

        def curve():
            values = np.clip(field(state["run"], tracker.get_value()), -E_RANGE, E_RANGE)
            return VMobject(color=E_FIELD, stroke_width=CURVE_WIDTH - 1).set_points_as_corners(
                [ax.c2p(x, v) for x, v in zip(X, values)])

        wave = always_redraw(curve)

        def envelope(run):
            env = np.clip(DATA["envelope_" + run], 0, E_RANGE)
            return VGroup(*[
                DashedVMobject(VMobject(color=INK, stroke_width=THIN_WIDTH)
                               .set_points_as_corners([ax.c2p(x, s * v) for x, v in zip(X, env)]),
                               num_dashes=70, dashed_ratio=0.55)
                for s in (1, -1)])

        theory_lab = label("linear theory", color=INK, size=SMALL_SIZE)
        theory_lab.next_to(ax.c2p(10, -E_RANGE), UP, buff=0.12).align_to(
            ax.c2p(10, 0), RIGHT).shift(LEFT * 0.1)

        clock_label = math(r"\omega_{pe}t=", color=MUTED, size=MATH_SMALL)
        clock_label.move_to([4.6, 3.05, 0])
        clock = DecimalNumber(0.0, num_decimal_places=0, color=INK, font_size=MATH_SMALL)
        clock.add_updater(lambda m: m.set_value(tracker.get_value()).next_to(
            clock_label, RIGHT, buff=0.12))
        clock.next_to(clock_label, RIGHT, buff=0.12)

        titles = {
            "low": math(r"\omega = 0.5\,\omega_{pe}\text{: reflected}", color=INK),
            "high": math(r"\omega = 2\,\omega_{pe}\text{: transmitted}", color=INK),
        }
        for t in titles.values():
            t.move_to([-2.4, 3.05, 0])

        update_dots(dots)
        self.play(FadeIn(plasma_left), Create(x_axis_left), FadeIn(ticks_left),
                  FadeIn(x_lab_left), FadeIn(edge_left), FadeIn(gain_lab),
                  FadeIn(electrons_lab), Create(ax.y_axis), FadeIn(x_axis), FadeIn(x_ticks),
                  FadeIn(y_ticks), FadeIn(x_lab), FadeIn(y_lab), FadeIn(plasma_right),
                  FadeIn(edge_right), FadeIn(vacuum_lab), FadeIn(plasma_lab),
                  run_time=1.0, rate_func=EASE)
        self.play(FadeIn(dots), FadeIn(titles["low"]), FadeIn(clock_label), FadeIn(clock),
                  run_time=0.8, rate_func=EASE)
        self.add(wave)
        for run in ("low", "high"):
            start, steady, steady_time, end, end_time = PLAY[run]
            if run == "high":
                state["run"] = run
                tracker.set_value(start)
                self.play(FadeIn(titles[run]), run_time=0.8, rate_func=EASE)
            self.play(tracker.animate.set_value(steady), run_time=steady_time,
                      rate_func=LINEAR)
            env = envelope(run)
            self.play(tracker.animate.set_value(end), FadeIn(env), FadeIn(theory_lab),
                      run_time=end_time, rate_func=LINEAR)
            self.wait(0.8)
            if run == "low":
                self.audit_layout()
                self.play(FadeOut(env), FadeOut(theory_lab), FadeOut(titles[run]),
                          run_time=0.6, rate_func=EASE)
        self.wait(1.0)
