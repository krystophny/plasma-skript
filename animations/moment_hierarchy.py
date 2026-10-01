"""Accessible overview of the velocity-moment hierarchy.

The scene is a schematic, not dimensional data.  It shows how the full
distribution f(t, r, v) is compressed into moments and why a fluid model must
close the hierarchy when the transport equation for one moment contains the
next one:

    d_t n     contains div(n u)   (continuity),
    d_t (n u) contains div P      (momentum),
    d_t P     contains div Q      (pressure / energy),

with peculiar velocity w = v - u and heat flux q_i = (1/2) Q_ijj.
Units are Gaussian CGS and are shown next to each moment.
"""

from manim import *
import numpy as np

from style import (
    ACCENT, EASE, ELECTRON, FAINT, GREEN, INK, MUTED, ORANGE, PURPLE, SKY,
    SMALL_SIZE, StyledScene, label, math, title,
)


ROWS = [
    # name, unit, equation, color, divergence term in the next equation
    ("density", r"[\mathrm{cm^{-3}}]", r"n=\int f\,d^3v", SKY, r"\nabla\!\cdot(n\mathbf{u})"),
    ("flow", r"[\mathrm{cm\,s^{-1}}]", r"\mathbf{u}=\frac{1}{n}\int \mathbf{v}\,f\,d^3v", GREEN,
     r"\nabla\!\cdot\mathbf{P}"),
    ("pressure", r"[\mathrm{erg\,cm^{-3}}]", r"P_{ij}=m\int w_i w_j\,f\,d^3v", ORANGE,
     r"\nabla\!\cdot\mathbf{Q}"),
    ("third moment", r"[\mathrm{erg\,cm^{-2}\,s^{-1}}]", r"Q_{ijk}=m\int w_i w_j w_k\,f\,d^3v", PURPLE,
     None),
]


class MomentHierarchy(StyledScene):
    """Show the passage from a kinetic distribution to fluid moments."""

    def build(self):
        heading = title("Velocity moments")

        # Kinetic state: f and a sketch of its velocity-space samples.
        f_eq = math(r"f(t,\mathbf{r},\mathbf{v})", size=40)
        f_unit = math(r"[\mathrm{s^3\,cm^{-6}}]", color=MUTED, size=26)
        rng = np.random.default_rng(4)
        pts = rng.normal(scale=(0.42, 0.32), size=(46, 2))
        cloud = VGroup(*[Dot([x, y, 0], radius=0.045, color=ELECTRON) for x, y in pts])
        frame = VGroup(
            Line([-1.2, 0, 0], [1.2, 0, 0], color=FAINT, stroke_width=1.4),
            Line([0, -1.0, 0], [0, 1.0, 0], color=FAINT, stroke_width=1.4),
        )
        vx = math("v_x", color=MUTED, size=26).next_to(frame[0], RIGHT, buff=0.1)
        vy = math("v_y", color=MUTED, size=26).next_to(frame[1], UP, buff=0.1)
        sketch = VGroup(frame, cloud, vx, vy)
        source = VGroup(f_eq, f_unit, sketch).arrange(DOWN, buff=0.3)
        source.move_to([-4.95, 0.1, 0])

        # Moment ladder.
        ys = [2.25, 1.0, -0.25, -1.5]
        names, eqs = VGroup(), VGroup()
        for (name, unit, eq, color, _), y in zip(ROWS, ys):
            nm = VGroup(label(name, color=color, size=26),
                        math(unit, color=MUTED, size=24)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
            nm.move_to([-2.05, y, 0], aligned_edge=LEFT)
            ex = math(eq, size=32).move_to([0.6, y, 0], aligned_edge=LEFT)
            names.add(nm)
            eqs.add(ex)

        heat = math(r"q_i=\tfrac12\,Q_{ijj}", color=PURPLE, size=32)
        heat.move_to([0.6, -2.55, 0], aligned_edge=LEFT)
        heat_name = label("heat flux", color=PURPLE, size=SMALL_SIZE)
        heat_name.move_to([-2.05, -2.55, 0], aligned_edge=LEFT)
        contraction = Arrow([0.9, ys[3] - 0.38, 0], [0.9, heat.get_top()[1] + 0.06, 0], buff=0,
                            color=FAINT, stroke_width=2, max_tip_length_to_length_ratio=0.25)

        integrate = Arrow([-3.3, 0.35, 0], [-2.3, 0.35, 0], buff=0,
                          color=MUTED, stroke_width=2.5, max_tip_length_to_length_ratio=0.12)
        integrate_label = math(r"\int d^3v", color=MUTED, size=30).next_to(integrate, UP, buff=0.12)

        # Each transport equation contains the divergence of the next moment.
        arc_x = 4.85
        arcs, arc_labels = VGroup(), VGroup()
        for i in range(3):
            arc = CurvedArrow([arc_x, ys[i] - 0.05, 0], [arc_x, ys[i + 1] + 0.05, 0],
                              angle=-PI / 2, color=FAINT, stroke_width=2.2, tip_length=0.16)
            lab = math(ROWS[i][4], color=MUTED, size=28).next_to(arc, RIGHT, buff=0.12)
            arcs.add(arc)
            arc_labels.add(lab)
        closure_arc = CurvedArrow([arc_x, ys[3] - 0.05, 0], [arc_x, ys[3] - 1.2, 0],
                                  angle=-PI / 2, color=ACCENT, stroke_width=2.4, tip_length=0.16)
        closure = label("closure", color=ACCENT, size=26).next_to(closure_arc, RIGHT, buff=0.12)

        self.play(FadeIn(heading), FadeIn(source, shift=RIGHT * 0.2), run_time=1.0, rate_func=EASE)
        self.play(GrowArrow(integrate), FadeIn(integrate_label), run_time=0.6, rate_func=EASE)
        for i in range(4):
            anims = [FadeIn(names[i], shift=LEFT * 0.1), FadeIn(eqs[i], shift=LEFT * 0.1)]
            if i > 0:
                anims += [Create(arcs[i - 1]), FadeIn(arc_labels[i - 1])]
            self.play(*anims, run_time=0.7, rate_func=EASE)
        self.play(GrowArrow(contraction), FadeIn(heat), FadeIn(heat_name), run_time=0.6, rate_func=EASE)
        self.play(Create(closure_arc), FadeIn(closure), run_time=0.6, rate_func=EASE)
        self.wait(1.6)
