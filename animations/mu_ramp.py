"""The magnetic moment in a slowly growing uniform field.

Model: uniform B(t) e_z out of the page, B/B_0 = 3/2 + tanh(t/tau)/2 (about
B_0 -> 2 B_0) with omega_c0 tau = 20, shown from t = -4 tau to 4 tau (38
gyrations), and the induced field E = -(1/2) dB/dt e_z x r of Faraday's law.
One ion (q_alpha > 0) on a circle centred on the axis; normalized with
q_alpha = m_alpha = B_0 = 1 and the starting Larmor radius rho_L0, time
omega_c0 t [1].  The orbit is the Boris scheme of derivations/plot_mu_ramp.py
(drift_models.mu_ramp_orbit, 1600 steps per initial turn): the same numerics
as the adiabatic-invariance plot, keeping the trajectory.

The orbit shrinks as B grows.  The traces show B/B_0, the orbit radius
rho_L/rho_L0 against (B/B_0)^(-1/2), and the two invariants: the flux through
the orbit pi rho_L^2 B and mu = m_alpha v_perp^2/(2B), each relative to its
start.  The flux uses the measured orbit radius, mu the measured speed.
"""

from manim import *
import numpy as np

from drift_models import MU_TAU, mu_ramp_orbit
from style import (
    B_FIELD, CURVE_WIDTH, DOT_RADIUS, E_FIELD, FAINT, GRID as GRID_COLOR, INK, ION,
    LINEAR, MATH_SIZE, MATH_SMALL, MUTED, THIN_WIDTH, StyledScene, axes, dashed, math,
)

N_GRID = 4000
PLAY_TIME = 20.0
SCALE = 1.3                   # screen units per rho_L0
CENTRE = np.array([-0.2, 1.75, 0])


def sampled():
    t, b, rho, flux, mu, xy = mu_ramp_orbit()
    stats = {
        "rho_end": rho[-1], "b_end": b[-1] / b[0],
        "flux_dev": np.abs(flux - 1).max(), "mu_dev": np.abs(mu - 1).max(),
    }
    grid = np.linspace(0, t[-1], N_GRID)
    series = {k: np.interp(grid, t, a) for k, a in
              (("b", b / b[0]), ("rho", rho), ("flux", flux), ("mu", mu), ("x", xy[:, 0]), ("y", xy[:, 1]))}
    return grid, series, stats


def sci(value):
    """Upper bound a x 10^b (one digit, rounded up) in LaTeX."""
    expo = int(np.floor(np.log10(value)))
    mant = int(np.ceil(value / 10.0**expo - 1e-9))
    if mant == 10:
        mant, expo = 1, expo + 1
    return rf"{mant}\times10^{{{expo}}}"


class MuRamp(StyledScene):
    """Ion orbit shrinking in B_0 -> 2B_0 with flux and mu constant."""

    def build(self):
        grid, s, stats = sampled()
        t_end = grid[-1]
        b_of_t = s["b"]
        b_dot = np.gradient(b_of_t, grid)

        tracker = ValueTracker(0.0)

        def index():
            return min(int(tracker.get_value() * (N_GRID - 1)), N_GRID - 1)

        def orbit_point(i):
            return CENTRE + SCALE * np.array([s["x"][i], s["y"][i], 0])

        ref_0 = dashed(Circle(radius=SCALE, color=FAINT, stroke_width=THIN_WIDTH).move_to(CENTRE), num_dashes=50)
        ref_1 = dashed(Circle(radius=SCALE / np.sqrt(2), color=FAINT, stroke_width=THIN_WIDTH).move_to(CENTRE),
                       num_dashes=36)
        lab_0 = math(r"\rho_{L0}", color=MUTED, size=MATH_SMALL).next_to(CENTRE + SCALE * RIGHT, RIGHT, buff=0.12)
        lab_1 = math(r"\rho_{L0}/\sqrt2", color=MUTED, size=MATH_SMALL).move_to(CENTRE + np.array([0, -0.32, 0]))
        axis_dot = Dot(CENTRE, radius=0.045, color=INK)

        def b_marks():
            size = 0.075 * b_of_t[index()] ** 0.5
            marks = VGroup()
            for k in range(4):
                a = np.pi / 4 + k * np.pi / 2
                marks.add(VGroup(Circle(radius=size, color=B_FIELD, stroke_width=1.5),
                                 Dot(radius=0.3 * size, color=B_FIELD)).move_to(CENTRE + 2.15 * np.array([np.cos(a), np.sin(a), 0])))
            return marks.set_opacity(0.6)

        def e_ring():
            frac = b_dot[index()] / b_dot.max()
            ring = VGroup()
            if frac < 0.03:
                return ring
            r = 1.32 * SCALE
            for k in range(8):
                a = k * np.pi / 4 + np.pi / 8
                p = CENTRE + r * np.array([np.cos(a), np.sin(a), 0])
                tangent = np.array([np.sin(a), -np.cos(a), 0])          # clockwise: E = -(1/2) dB/dt e_z x r
                ring.add(Arrow(p - 0.32 * frac * tangent, p + 0.32 * frac * tangent, buff=0, color=E_FIELD,
                               stroke_width=3, max_tip_length_to_length_ratio=0.35))
            return ring

        marks = always_redraw(b_marks)
        ring = always_redraw(e_ring)

        def trail():
            i = index()
            j = max(0, i - 40)
            if i - j < 2:
                return VMobject()
            pts = [orbit_point(k) for k in range(j, i + 1)]
            return VMobject().set_points_smoothly(pts).set_stroke(ION, CURVE_WIDTH - 1, opacity=[0.0, 1.0])

        orbit_trail = always_redraw(trail)
        particle = always_redraw(lambda: Dot(orbit_point(index()), radius=DOT_RADIUS * 1.6, color=ION))

        b_key = VGroup(VGroup(Circle(radius=0.11, color=B_FIELD, stroke_width=2.0),
                              Dot(radius=0.03, color=B_FIELD)),
                       math(r"\mathbf{B}(t)", color=B_FIELD, size=MATH_SIZE)).arrange(RIGHT, buff=0.15)
        e_key = VGroup(Arrow(ORIGIN, RIGHT * 0.55, buff=0, color=E_FIELD, stroke_width=3,
                             max_tip_length_to_length_ratio=0.3),
                       math(r"\mathbf{E}=-\tfrac12\dot B\,\mathbf{e}_z\times\mathbf{r}", color=E_FIELD, size=MATH_SMALL)
                       ).arrange(RIGHT, buff=0.15)
        keys = VGroup(b_key, e_key).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-5.0, 2.6, 0])
        setup = VGroup(
            math(r"B/B_0=\tfrac32+\tfrac12\tanh(t/\tau)", color=MUTED, size=MATH_SMALL),
            math(rf"\omega_{{c0}}\tau={MU_TAU:g},\ q_\alpha>0", color=MUTED, size=MATH_SMALL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(keys, DOWN, buff=0.45).align_to(keys, LEFT)

        clock_label = math(r"\omega_{c0}t=", color=MUTED, size=MATH_SMALL).move_to([4.2, 3.4, 0])
        clock = DecimalNumber(0.0, num_decimal_places=0, color=INK, font_size=MATH_SMALL)

        def place_clock(m):
            m.set_value(grid[index()])
            m.next_to(clock_label, RIGHT, buff=0.12)

        clock.add_updater(place_clock)
        place_clock(clock)
        numbers = VGroup(
            math(rf"\mathrm{{end}}{{:}}\ B/B_0={stats['b_end']:.3f}", color=MUTED, size=MATH_SMALL),
            math(rf"\rho_L/\rho_{{L0}}={stats['rho_end']:.4f}", color=MUTED, size=MATH_SMALL),
            math(rf"(B/B_0)^{{-1/2}}={stats['b_end'] ** -0.5:.4f}", color=MUTED, size=MATH_SMALL),
            math(rf"|\mu/\mu_0-1|\le{sci(stats['mu_dev'])}", color=MUTED, size=MATH_SMALL),
            math(rf"|\Phi/\Phi_0-1|\le{sci(stats['flux_dev'])}", color=MUTED, size=MATH_SMALL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        numbers.next_to([2.3, 1.65, 0], RIGHT, buff=0)

        # Traces: left B/B_0 and rho_L/rho_L0, right the invariants on a zoomed scale.
        left = axes([0, t_end, 40], [0.4, 2.1, 0.5], 5.6, 2.0, ticks=False).move_to([-3.45, -2.35, 0])
        right = axes([0, t_end, 40], [0.99, 1.01, 0.01], 5.6, 2.0, ticks=False).move_to([3.45, -2.35, 0])
        panels = VGroup()
        for ax, ticks, xs in ((left, (1.0, 2.0), (0, 80, 160)), (right, (0.99, 1.0, 1.01), (80,))):
            ax.x_axis.set_opacity(0)
            ax.y_axis.set_opacity(0)
            panels.add(Rectangle(width=ax.x_length, height=ax.y_length, color=MUTED, stroke_width=1.2
                                 ).move_to(ax.get_center()))
            for v in ticks:
                panels.add(math(f"{v:g}", color=MUTED, size=MATH_SMALL).next_to(ax.c2p(0, v), LEFT, buff=0.1))
            for v in xs:
                panels.add(math(f"{v:d}", color=MUTED, size=MATH_SMALL).next_to(ax.c2p(v, ax.y_range[0]), DOWN, buff=0.08))
        panels.add(DashedLine(right.c2p(0, 1), right.c2p(t_end, 1), color=GRID_COLOR, stroke_width=1.0, dash_length=0.06))
        x_note = math(r"\omega_{c0}t\ [1]", color=MUTED, size=MATH_SMALL).next_to(right, DOWN, buff=0.08).align_to(right, RIGHT)
        reference = dashed(left.plot(lambda u: np.interp(u, grid, b_of_t) ** -0.5, x_range=[0, t_end, t_end / 200],
                                     color=MUTED, stroke_width=THIN_WIDTH), num_dashes=45)

        def trace(ax, key, color, width, step=4, dash=False):
            def make():
                i = index()
                if i < 2:
                    return VMobject()
                pts = [ax.c2p(grid[j], np.clip(s[key][j], ax.y_range[0], ax.y_range[1])) for j in range(0, i + 1, step)]
                line = VMobject().set_points_as_corners(pts).set_stroke(color, width)
                return DashedVMobject(line, num_dashes=max(int(40 * i / N_GRID), 2)) if dash else line
            return always_redraw(make)

        tags = VGroup(
            math(r"B/B_0", color=B_FIELD, size=MATH_SMALL).next_to(left.c2p(t_end, 2.0), LEFT, buff=0.1).shift(DOWN * 0.22),
            math(r"\rho_L/\rho_{L0}", color=ION, size=MATH_SMALL).next_to(left.c2p(t_end, 0.71), LEFT, buff=0.1).shift(UP * 0.3),
            math(r"\mu/\mu_0", color=INK, size=MATH_SMALL).move_to(right.c2p(40, 1.0062)),
            math(r"\Phi/\Phi_0,\ \Phi=\pi\rho_L^2B", color=ION, size=MATH_SMALL).move_to(right.c2p(108, 1.0062)),
            math(r"\mathrm{dashed{:}}\ (B/B_0)^{-1/2}", color=MUTED, size=MATH_SMALL).move_to(left.c2p(52, 0.56)),
        )
        heads = VGroup(
            math(r"[1]", color=MUTED, size=MATH_SMALL).next_to(left, UP, buff=0.08).align_to(left, LEFT),
            math(r"[1]", color=MUTED, size=MATH_SMALL).next_to(right, UP, buff=0.08).align_to(right, LEFT),
        )

        self.add(marks, ref_0, ref_1, lab_0, lab_1, axis_dot, ring, keys, setup, clock_label, clock,
                 panels, x_note, reference, tags, heads,
                 trace(left, "b", B_FIELD, CURVE_WIDTH - 1.5), trace(left, "rho", ION, CURVE_WIDTH - 1.5),
                 trace(right, "mu", INK, CURVE_WIDTH - 1.5), trace(right, "flux", ION, CURVE_WIDTH - 2.0, dash=True),
                 orbit_trail, particle)
        self.wait(0.5)
        self.play(tracker.animate.set_value(1.0), run_time=PLAY_TIME, rate_func=LINEAR)
        self.play(FadeIn(numbers), run_time=0.5)
        self.wait(2.0)
