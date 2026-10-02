"""Shared visual language for the lecture-script Manim scenes.

Every scene imports this module (Manim puts the scene file's directory on
``sys.path``), so palette, typography, stroke widths and margins stay identical
across the script.  The palette is the Okabe-Ito color-vision-safe set on the
dark video surface used by the website (``--video-surface`` in styles.css).
Color is never the only encoding: scenes pair each color with a marker shape,
line style or direct label.

Physical time is always advanced with a linear rate function so that the
displayed dynamics are not distorted; easing is reserved for entrances,
exits and camera-free emphasis.
"""

import os

from manim import (
    DOWN, LEFT, RIGHT, UP, Axes, Create, DashedVMobject, FadeIn, FadeOut,
    Line, MathTex, Scene, Text, VGroup, Write, config, rate_functions,
)
from manim.mobject.text.text_mobject import register_font


# --- palette -------------------------------------------------------------
BG = "#0F1318"          # website --video-surface
INK = "#ECE9E2"         # primary text and key objects
MUTED = "#A3ABB4"       # secondary text, axis labels
FAINT = "#68717C"       # reference curves, ticks
GRID = "#38404A"        # axes and frames

# Okabe-Ito (2008) hues, kept exact so the set stays color-vision safe.
ORANGE = "#E69F00"
SKY = "#56B4E9"
GREEN = "#009E73"
YELLOW = "#F0E442"
BLUE = "#0072B2"
VERMILION = "#D55E00"
PURPLE = "#CC79A7"

# Semantic roles shared by all scenes.
ELECTRON = SKY          # drawn as filled circles
ION = ORANGE            # drawn as triangles
E_FIELD = YELLOW
B_FIELD = PURPLE
POTENTIAL = GREEN
ACCENT = VERMILION      # resonance, highlighted reference value

# --- typography ----------------------------------------------------------
FONT = "NewComputerModern"
LABEL_SIZE = 28
SMALL_SIZE = 24         # smallest size allowed anywhere in a scene
MATH_SIZE = 34

# --- geometry ------------------------------------------------------------
MARGIN = 0.55           # free border around all content, in Manim units
AXIS_WIDTH = 1.6
CURVE_WIDTH = 4.0
THIN_WIDTH = 2.4
DOT_RADIUS = 0.075

EASE = rate_functions.ease_in_out_sine
LINEAR = rate_functions.linear


def label(text, color=MUTED, size=LABEL_SIZE, **kwargs):
    """Prose label in New Computer Modern."""
    return Text(text, color=color, font_size=size, **kwargs)


def math(tex, color=INK, size=MATH_SIZE, **kwargs):
    """LaTeX label; Computer Modern matches the New Computer Modern prose."""
    return MathTex(tex, color=color, font_size=size, **kwargs)


def axes(x_range, y_range, x_length, y_length, ticks=True, **kwargs):
    """Quiet axes: thin grey lines, short ticks, no arrow tips."""
    axis_config = {
        "color": GRID,
        "stroke_width": AXIS_WIDTH,
        "include_ticks": ticks,
        "tick_size": 0.05,
        "include_tip": False,
    }
    axis_config.update(kwargs.pop("axis_config", {}))
    return Axes(
        x_range=x_range,
        y_range=y_range,
        x_length=x_length,
        y_length=y_length,
        axis_config=axis_config,
        tips=False,
        **kwargs,
    )


def axis_labels(ax, x_tex, y_tex, size=30):
    """Math axis labels: x label under the right end, y label above the top."""
    x_lab = math(x_tex, color=MUTED, size=size)
    x_lab.next_to(ax.x_axis.get_right(), DOWN, buff=0.22).align_to(ax.x_axis.get_right(), RIGHT)
    y_lab = math(y_tex, color=MUTED, size=size)
    y_lab.next_to(ax.y_axis.get_top(), UP, buff=0.18)
    return VGroup(x_lab, y_lab)


def dashed(mob, num_dashes=40, ratio=0.55):
    return DashedVMobject(mob, num_dashes=num_dashes, dashed_ratio=ratio)


class StyledScene(Scene):
    """Scene base class: background, registered font, layout audit."""

    def construct(self):
        self.camera.background_color = BG
        font_file = os.environ["PLASMA_NEW_COMPUTER_MODERN_FONT"]
        with register_font(font_file):
            Text.set_default(font=FONT, disable_ligatures=True)
            self.build()
            self.audit_layout()

    def build(self):
        raise NotImplementedError

    def audit_layout(self):
        """Warn about text outside the margin or overlapping other text.

        Only the final frame is checked; scenes call this at intermediate
        states too when labels move.
        """
        half_w = config.frame_width / 2 - MARGIN + 0.05
        half_h = config.frame_height / 2 - MARGIN + 0.05
        texts = []
        for mob in self.mobjects:
            for sub in mob.get_family():
                if isinstance(sub, (Text, MathTex)) and sub.get_fill_opacity() > 0.05:
                    texts.append(sub)
        boxes = []
        for t in texts:
            lo, hi = t.get_corner(DOWN + LEFT), t.get_corner(UP + RIGHT)
            if lo[0] < -half_w or hi[0] > half_w or lo[1] < -half_h or hi[1] > half_h:
                print(f"LAYOUT margin: {type(t).__name__} {_name(t)}")
            boxes.append((t, lo, hi))
        for i, (a, alo, ahi) in enumerate(boxes):
            for b, blo, bhi in boxes[i + 1:]:
                if b in a.get_family() or a in b.get_family():
                    continue
                if (alo[0] < bhi[0] - 0.02 and blo[0] < ahi[0] - 0.02
                        and alo[1] < bhi[1] - 0.02 and blo[1] < ahi[1] - 0.02):
                    print(f"LAYOUT overlap: {_name(a)} <> {_name(b)}")


def _name(mob):
    return getattr(mob, "text", None) or getattr(mob, "tex_string", None) or repr(mob)
