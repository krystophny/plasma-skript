"""Prescribed planar sheath: wall X=0, edge X=5, X=x/lambda_D.

B=-e phi/(kB Te)=a(5-X)^2 inside the edge, zero outside; a=0.12.
Boltzmann electrons and cold ions with edge Mach number M=1.5 give
ne/n0=exp(-B), ni/n0=M/sqrt(M²+2B). These share one prescribed
potential; Poisson's equation is NOT solved self-consistently.
Separate electron and ion clocks resolve their different transit times.
"""
from manim import *
import numpy as np

from style import (
    CURVE_WIDTH, DOT_RADIUS, EASE, ELECTRON, FAINT, GRID, INK, ION, LINEAR,
    MUTED, POTENTIAL, SMALL_SIZE, THIN_WIDTH, StyledScene, axes, label, math,
)

EDGE, CURVATURE, MACH, ELECTRON_ENERGY = 5.0, 0.12, 1.5, 0.9


def barrier(x):
    """Electron potential energy / kB Te, for X=x/lambda_D >= 0."""
    return CURVATURE * np.maximum(EDGE - np.asarray(x), 0.0) ** 2


def sheath_densities(x):
    b = barrier(x)
    return np.exp(-b), MACH / np.sqrt(MACH**2 + 2 * b)


def electron_position(tau):
    """X for tau=t sqrt(kB Te/me)/lambda_D, one reflection inside sheath."""
    w = np.sqrt(2 * CURVATURE)
    return EDGE - np.sqrt(ELECTRON_ENERGY / CURVATURE) * np.sin(w * tau)


def ion_position(tau):
    """X for tau=t cs/lambda_D, valid from entry until wall absorption."""
    w = np.sqrt(2 * CURVATURE)
    return EDGE - MACH / w * np.sinh(w * tau)


class SheathFormation(StyledScene):
    """Electron reflection and ion acceleration in a prescribed sheath."""

    def build(self):
        x_max = 8.0
        w = np.sqrt(2 * CURVATURE)

        pot = axes([0, x_max, 1], [0, 3.2, 1], 10.4, 2.1).move_to([0.45, 1.45, 0])
        dens = axes([0, x_max, 1], [0, 1.2, 0.5], 10.4, 1.7).move_to([0.45, -1.8, 0])
        pot_ylab = math(r"-e\phi/k_BT_e\ [1]", color=POTENTIAL, size=30)
        pot_ylab.next_to(pot.y_axis.get_top(), UP, buff=0.12).shift(RIGHT * 0.9)
        dens_ylab = math(r"n/n_0\ [1]", color=MUTED, size=30)
        dens_ylab.next_to(dens.y_axis.get_top(), UP, buff=0.12).shift(RIGHT * 0.8)
        xlab = math(r"x/\lambda_D\ [1]", color=MUTED, size=30)
        xlab.next_to(dens.x_axis.get_right(), DOWN, buff=0.18).align_to(dens.x_axis.get_right(), RIGHT)

        # Wall at X=0 (hatched bar) and sheath edge at X=5.
        x0 = pot.c2p(0, 0)[0]
        top, bottom = pot.c2p(0, 3.2)[1], dens.c2p(0, 0)[1]
        wall = Rectangle(width=0.22, height=top - bottom, stroke_width=0,
                         fill_color=GRID, fill_opacity=1).move_to([x0 - 0.11, (top + bottom) / 2, 0])
        hatch = VGroup(*[Line([x0 - 0.22, y, 0], [x0, y + 0.2, 0], color=FAINT, stroke_width=1.5)
                         for y in np.arange(bottom, top - 0.2, 0.22)])
        ex = pot.c2p(EDGE, 0)[0]
        edge = DashedLine([ex, bottom, 0], [ex, top, 0], color=FAINT,
                          stroke_width=THIN_WIDTH, dash_length=0.1)
        edge_lab = label("sheath edge", color=MUTED, size=SMALL_SIZE).next_to(edge, UP, buff=0.12)

        potential = pot.plot(barrier, x_range=[0, x_max, 0.02], color=POTENTIAL, stroke_width=CURVE_WIDTH)
        ne = dens.plot(lambda x: sheath_densities(x)[0], x_range=[0, x_max, 0.02],
                       color=ELECTRON, stroke_width=CURVE_WIDTH)
        ni = DashedVMobject(dens.plot(lambda x: sheath_densities(x)[1], x_range=[0, x_max, 0.02],
                                      color=ION, stroke_width=CURVE_WIDTH), num_dashes=60)
        ne_lab = math(r"n_e", color=ELECTRON, size=32).move_to(dens.c2p(0.75, 0.22))
        ni_lab = math(r"n_i", color=ION, size=32).move_to(dens.c2p(0.75, 0.88))

        # Particle lane between the panels.
        lane_y = 0.0
        lane = Line(pot.c2p(0, 0) * [1, 0, 0] + [0, lane_y, 0],
                    pot.c2p(x_max, 0) * [1, 0, 0] + [0, lane_y, 0], color=GRID, stroke_width=1.2)

        def lane_point(x):
            return np.array([pot.c2p(x, 0)[0], lane_y, 0])

        clock = ValueTracker(0.0)

        # Electron: total energy 0.9 kBTe, turns where the barrier equals it.
        turn = EDGE - np.sqrt(ELECTRON_ENERGY / CURVATURE)
        e_level = DashedLine(pot.c2p(turn, ELECTRON_ENERGY), pot.c2p(x_max, ELECTRON_ENERGY),
                             color=ELECTRON, stroke_width=THIN_WIDTH, dash_length=0.08)
        e_level_lab = math(r"\varepsilon_e=0.9\,k_BT_e", color=ELECTRON, size=28)
        e_level_lab.next_to(e_level.get_end(), UP, buff=0.12).align_to(e_level.get_end(), RIGHT)
        turn_mark = Dot(pot.c2p(turn, ELECTRON_ENERGY), radius=0.06, color=ELECTRON)
        e_on_level = always_redraw(lambda: Dot(
            pot.c2p(electron_position(clock.get_value()), ELECTRON_ENERGY),
            radius=DOT_RADIUS + 0.03, color=ELECTRON))
        electron = always_redraw(lambda: Dot(
            lane_point(electron_position(clock.get_value())), radius=0.11, color=ELECTRON))

        self.play(Create(pot), Create(dens), FadeIn(wall), FadeIn(hatch),
                  FadeIn(VGroup(pot_ylab, dens_ylab, xlab)), run_time=0.9, rate_func=EASE)
        self.play(Create(potential), Create(ne), Create(ni), FadeIn(edge), FadeIn(edge_lab),
                  FadeIn(ne_lab), FadeIn(ni_lab), FadeIn(lane), run_time=1.0, rate_func=EASE)
        self.play(FadeIn(e_level), FadeIn(e_level_lab), FadeIn(electron), FadeIn(e_on_level),
                  run_time=0.4, rate_func=EASE)
        self.add(turn_mark)
        self.play(clock.animate.set_value(PI / w), run_time=4.0, rate_func=LINEAR)

        # Ion: enters at the Bohm-satisfying Mach number and falls to the wall.
        arrival = np.arcsinh(EDGE * w / MACH) / w
        e_ghost = Dot(lane_point(EDGE), radius=0.11, color=ELECTRON, fill_opacity=0.35)
        ion = always_redraw(lambda: Triangle(color=ION, fill_opacity=1, stroke_width=0)
                            .scale(0.13).move_to(lane_point(ion_position(clock.get_value()))))
        mach_lab = math(r"u_{\rm edge}=1.5\,c_s", color=ION, size=28)
        mach_lab.next_to(lane_point(EDGE), DOWN, buff=0.2).shift(RIGHT * 1.3)

        self.remove(electron, e_on_level)
        self.add(e_ghost)
        clock.set_value(0.0)
        self.play(FadeIn(ion), FadeIn(mach_lab),
                  run_time=0.5, rate_func=EASE)
        self.play(clock.animate.set_value(arrival), run_time=3.5, rate_func=LINEAR)
        self.wait(1.5)
