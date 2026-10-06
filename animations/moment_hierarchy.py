"""Accessible overview of the velocity-moment hierarchy.

The scene is a schematic, not dimensional data.  It shows how the full
distribution f(t, r, v) is compressed into moments and why a fluid model must
close the hierarchy when the transport equation for one moment contains the
next one:

    d_t n     contains div(n u)   (continuity),
    d_t (n u) contains div P      (momentum),
    d_t P     contains div Q      (pressure / energy),

with peculiar velocity w = v - u and heat flux q_i = (1/2) Q_ijj.
Units are SI and are shown next to each moment.
"""

from manim import *
import numpy as np

from style import (
    ACCENT, EASE, ELECTRON, FAINT, GREEN, INK, MUTED, ORANGE, PURPLE, SKY,
    SMALL_SIZE, StyledScene, label, math,
    MATH_SIZE, MATH_SMALL,
)


ROWS = [
    # name, unit, equation, color, divergence term in the next equation
    ("density", r"[\mathrm{m^{-3}}]", r"n=\int f\,d^3v", SKY, r"\nabla\!\cdot(n\mathbf{u})"),
    ("flow", r"[\mathrm{m\,s^{-1}}]", r"\mathbf{u}=\frac{1}{n}\int \mathbf{v}\,f\,d^3v", GREEN,
     r"\nabla\!\cdot\mathbf{P}"),
    ("pressure", r"[\mathrm{J\,m^{-3}}]", r"P_{ij}=m\int w_i w_j\,f\,d^3v", ORANGE,
     r"\nabla\!\cdot\mathbf{Q}"),
    ("third moment", r"[\mathrm{W\,m^{-2}}]", r"Q_{ijk}=m\int w_i w_j w_k\,f\,d^3v", PURPLE,
     None),
]


class MomentHierarchy(StyledScene):
    """Show the passage from a kinetic distribution to fluid moments."""

    def build(self):
        # Kinetic state: f and a sketch of its velocity-space samples.
        f_eq = math(r"f(t,\mathbf{r},\mathbf{v})", size=MATH_SIZE)
        f_unit = math(r"[\mathrm{s^3\,m^{-6}}]", color=MUTED, size=MATH_SMALL)
        rng = np.random.default_rng(4)
        pts = rng.normal(scale=(0.42, 0.32), size=(46, 2))
        cloud = VGroup(*[Dot([x, y, 0], radius=0.045, color=ELECTRON) for x, y in pts])
        frame = VGroup(
            Line([-1.2, 0, 0], [1.2, 0, 0], color=FAINT, stroke_width=1.4),
            Line([0, -1.0, 0], [0, 1.0, 0], color=FAINT, stroke_width=1.4),
        )
        vx = math("v_x", color=MUTED, size=MATH_SMALL).next_to(frame[0], RIGHT, buff=0.1)
        vy = math("v_y", color=MUTED, size=MATH_SMALL).next_to(frame[1], UP, buff=0.1)
        sketch = VGroup(frame, cloud, vx, vy)
        source = VGroup(f_eq, f_unit, sketch).arrange(DOWN, buff=0.3)
        source.move_to([-4.95, 0.1, 0])

        # Moment ladder.
        ys = [2.75, 1.3, -0.15, -1.6]
        names, eqs = VGroup(), VGroup()
        for (name, unit, eq, color, _), y in zip(ROWS, ys):
            ex = math(eq, size=MATH_SIZE).move_to([-2.0, y, 0], aligned_edge=LEFT)
            nm = math(unit, color=color, size=MATH_SMALL).next_to(ex, RIGHT, buff=0.3)
            names.add(nm)
            eqs.add(ex)

        heat = math(r"q_i=\tfrac12\,Q_{ijj}", color=PURPLE, size=MATH_SIZE)
        heat.move_to([-2.0, -2.95, 0], aligned_edge=LEFT)
        heat_name = math(r"[\mathrm{W\,m^{-2}}]", color=PURPLE, size=MATH_SMALL)
        heat_name.next_to(heat, RIGHT, buff=0.3)
        contraction = Arrow([-1.7, ys[3] - 0.38, 0], [-1.7, heat.get_top()[1] + 0.06, 0], buff=0,
                            color=FAINT, stroke_width=2, max_tip_length_to_length_ratio=0.25)

        integrate = Arrow([-3.3, 0.55, 0], [-2.2, 0.55, 0], buff=0,
                          color=MUTED, stroke_width=2.5, max_tip_length_to_length_ratio=0.12)
        integrate_label = math(r"\int d^3v", color=MUTED, size=MATH_SMALL).next_to(integrate, UP, buff=0.12)

        # Each transport equation contains the divergence of the next moment.
        arc_x = 4.75
        arcs, arc_labels = VGroup(), VGroup()
        for i in range(3):
            arc = CurvedArrow([arc_x, ys[i] - 0.05, 0], [arc_x, ys[i + 1] + 0.05, 0],
                              angle=-PI / 2, color=FAINT, stroke_width=2.2, tip_length=0.16)
            lab = math(ROWS[i][4], color=MUTED, size=MATH_SMALL).next_to(arc, RIGHT, buff=0.12)
            arcs.add(arc)
            arc_labels.add(lab)
        closure_arc = CurvedArrow([arc_x, ys[3] - 0.05, 0], [arc_x, ys[3] - 1.2, 0],
                                  angle=-PI / 2, color=ACCENT, stroke_width=2.4, tip_length=0.16)
        closure = label("closure", color=ACCENT, size=SMALL_SIZE).next_to(closure_arc, RIGHT, buff=0.12)

        self.play(FadeIn(source, shift=RIGHT * 0.2), run_time=1.0, rate_func=EASE)
        self.play(GrowArrow(integrate), FadeIn(integrate_label), run_time=0.6, rate_func=EASE)
        for i in range(4):
            anims = [FadeIn(names[i], shift=LEFT * 0.1), FadeIn(eqs[i], shift=LEFT * 0.1)]
            if i > 0:
                anims += [Create(arcs[i - 1]), FadeIn(arc_labels[i - 1])]
            self.play(*anims, run_time=0.7, rate_func=EASE)
        self.play(GrowArrow(contraction), FadeIn(heat), FadeIn(heat_name), run_time=0.6, rate_func=EASE)
        self.play(Create(closure_arc), FadeIn(closure), run_time=0.6, rate_func=EASE)
        self.wait(1.6)
