"""Accessible overview of the velocity-moment hierarchy.

The scene is a schematic, not dimensional data.  It shows how the full
distribution f(t, r, v) is compressed into moments and why a fluid model must
close the hierarchy when the transport equation for one moment contains the
next one.
"""

from manim import *
import numpy as np


BG = "#0B1220"
INK = "#E8EEF7"
MUTED = "#9BAAC0"
TEAL = "#72D6C9"
BLUE = "#4EA8DE"
ORANGE = "#F2A65A"
PURPLE = "#B9A0FF"
LINE = "#2A3C56"


class MomentHierarchy(Scene):
    """Show the passage from a kinetic distribution to fluid moments."""

    def construct(self):
        self.camera.background_color = BG

        title = Text("From distribution to fluid moments", color=INK, font_size=31)
        subtitle = Text(
            "schematic hierarchy; all quantities are labelled, not measured",
            color=MUTED,
            font_size=19,
        )
        heading = VGroup(title, subtitle).arrange(DOWN, buff=0.08)
        heading.to_edge(UP, buff=0.24)

        source_box = RoundedRectangle(
            width=2.9,
            height=2.55,
            corner_radius=0.16,
            stroke_color=TEAL,
            stroke_width=2,
            fill_color="#132B38",
            fill_opacity=1,
        ).move_to(LEFT * 4.75 + UP * 0.35)
        source_title = Text("full kinetic state", color=TEAL, font_size=20)
        source_title.move_to(source_box.get_center() + UP * 0.82)
        source_formula = MathTex(
            r"f(t,\boldsymbol{r},\boldsymbol{v})",
            color=INK,
            font_size=28,
        )
        source_formula.move_to(source_box.get_center() + UP * 0.35)

        rng = np.random.default_rng(5)
        cloud = VGroup()
        for x, y in rng.normal((0, 0), (0.37, 0.23), size=(24, 2)):
            cloud.add(
                Dot(
                    source_box.get_center() + RIGHT * (x + 0.02) + DOWN * (y + 0.25),
                    radius=0.045,
                    color=ORANGE,
                )
            )
        source_note = Text("position + velocity structure", color=MUTED, font_size=15)
        source_note.move_to(source_box.get_center() + DOWN * 1.02)
        source = VGroup(source_box, source_title, source_formula, cloud, source_note)

        cards = []

        def make_card(order, name, formula, note, color, y):
            box = RoundedRectangle(
                width=4.75,
                height=1.23,
                corner_radius=0.12,
                stroke_color=color,
                stroke_width=2,
                fill_color="#121D2E",
                fill_opacity=1,
            ).move_to(RIGHT * 2.1 + UP * y)
            label = Text(f"{order}: {name}", color=color, font_size=16)
            if label.width > 1.7:
                label.scale_to_fit_width(1.7)
            label.move_to(box.get_center() + UP * 0.42)
            expression = MathTex(formula, color=INK, font_size=24)
            if expression.width > 3.35:
                expression.scale_to_fit_width(3.35)
            expression.move_to(box.get_center() + UP * 0.02)
            note_text = Text(note, color=MUTED, font_size=14)
            if note_text.width > 4.2:
                note_text.scale_to_fit_width(4.2)
            note_text.move_to(box.get_center() + DOWN * 0.41)
            card = VGroup(box, label, expression, note_text)
            cards.append(card)
            return card

        make_card("0th", "density n", r"n=\int f\,d^3v", "counts particles", BLUE, 2.05)
        make_card("1st", "flow u", r"\boldsymbol{u}=n^{-1}\int\boldsymbol{v}f\,d^3v", "tracks bulk motion", TEAL, 0.65)
        make_card("2nd", "pressure P", r"\boldsymbol{P}=m\int\boldsymbol{w}\boldsymbol{w}f\,d^3v", "tracks random momentum flux", ORANGE, -0.75)
        make_card("3rd", "heat flux q", r"\boldsymbol{q}=\frac{m}{2}\int w^2\boldsymbol{w}f\,d^3v", "tracks random-energy transport", PURPLE, -2.15)

        first_arrow = Arrow(
            source_box.get_right() + RIGHT * 0.05,
            cards[0][0].get_left() + LEFT * 0.05,
            color=BLUE,
            stroke_width=3,
            buff=0,
        )
        first_label = Text("integrate over velocity", color=BLUE, font_size=16)
        first_label.next_to(first_arrow, UP, buff=0.08)

        chain_arrows = VGroup()
        for upper, lower in zip(cards[:-1], cards[1:]):
            chain_arrows.add(
                Arrow(
                    upper[0].get_bottom() + DOWN * 0.04,
                    lower[0].get_top() + UP * 0.04,
                    color=MUTED,
                    stroke_width=2.5,
                    buff=0,
                )
            )

        closure_note = Text(
            "transport of one moment introduces the next → closure is required",
            color=INK,
            font_size=18,
        )
        closure_note.to_edge(DOWN, buff=0.28)

        self.play(FadeIn(heading), FadeIn(source))
        self.play(GrowArrow(first_arrow), FadeIn(first_label), FadeIn(cards[0]))
        for arrow, card in zip(chain_arrows, cards[1:]):
            self.play(GrowArrow(arrow), FadeIn(card), run_time=0.8)
        self.play(FadeIn(closure_note))
        self.wait(1)
