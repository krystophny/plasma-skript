"""Shared visual language for the lecture-script Manim scenes.

Every scene imports this module (Manim puts the scene file's directory on
``sys.path``), so palette, typography, stroke widths and margins stay identical
across the script.  The palette is the Okabe-Ito color-vision-safe set on the
dark video surface of the website players (``--video-surface`` in styles.css)
and of the slides, whose animation pages are dark.  Plots and print figures
of the script stay light; only the animations use this dark surface.
Color is never the only encoding: scenes pair each color with a marker shape,
line style or direct label.

Physical time is always advanced with a linear rate function so that the
displayed dynamics are not distorted; easing is reserved for entrances,
exits and camera-free emphasis.
"""

import os
from contextlib import ExitStack

from manim import (
    DOWN, LEFT, RIGHT, UP, Axes, Create, DashedVMobject, FadeIn, FadeOut,
    Line, MathTex, Scene, Tex, TexTemplate, Text, VGroup, Write, config,
    rate_functions,
)
from manim.mobject.text.text_mobject import register_font


# --- palette -------------------------------------------------------------
# Dark video surface (website --video-surface, dark animation slide pages).
BG = "#0F1318"          # website --video-surface
INK = "#ECE9E2"         # primary text and key objects
MUTED = "#A3ABB4"       # secondary text, axis labels
FAINT = "#68717C"       # reference curves, ticks, ghosts
GRID = "#38404A"        # frames, grid and guide lines
AXIS = FAINT            # axis lines; GRID is too faint for thin axes

# Okabe-Ito (2008) hues, kept exact so the set stays color-vision safe.
ORANGE = "#E69F00"
SKY = "#56B4E9"
GREEN = "#009E73"
YELLOW = "#F0E442"
BLUE = "#0072B2"
VERMILION = "#D55E00"
PURPLE = "#CC79A7"

# Sequential colormap for densities on the dark surface: matplotlib's
# perceptually uniform "inferno" at 11 equidistant stops (dark low end next to
# BG, bright high end), interpolated linearly in RGB by density_rgb().
DENSITY_STOPS = [
    "#000004", "#160B39", "#420A68", "#6A176E", "#932667", "#BC3754",
    "#DD513A", "#F37819", "#FCA50A", "#F6D746", "#FCFFA4",
]

# Semantic roles shared by all scenes.
ELECTRON = SKY          # drawn as filled circles
ION = ORANGE            # drawn as triangles
E_FIELD = YELLOW
B_FIELD = PURPLE
POTENTIAL = GREEN
ACCENT = VERMILION      # resonance, highlighted reference value

# --- typography ----------------------------------------------------------
# STIX Two Text and STIX Two Math, the typefaces of the script, the plots and
# the slides.  Prose labels use the OTF files in fonts/ (registered with Pango
# per scene); MathTex/Tex go through latex + dvisvgm with the Type 1 fonts of
# the stix2 package (stix2-type1; texlive-fonts-extra on Debian, manimTex in
# flake.nix).
FONT = "STIX Two Text"
_HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIRS = [
    os.environ.get("PLASMA_FONT_DIR", ""),
    os.path.join(_HERE, "..", "fonts"),       # repository checkout
    os.path.join(_HERE, "fonts"),             # exported animation-sources/
]
TEX_TEMPLATE = TexTemplate(preamble=r"""
\usepackage[english]{babel}
\usepackage{amsmath}
\usepackage[T1]{fontenc}
\usepackage{stix2}
""")
MathTex.set_default(tex_template=TEX_TEMPLATE)
Tex.set_default(tex_template=TEX_TEMPLATE)

# Sizes in Manim font points.  The poster spans 10 of the 12 slide columns
# (213 mm on the A4-landscape slides); there LABEL_SIZE reads like the 18 pt
# slide body and the 10 pt labels of the derivation plots scaled by 1.8.
LABEL_SIZE = 34
SMALL_SIZE = 30         # smallest size allowed anywhere in a scene
MATH_SIZE = 44          # MathTex sets ~0.75x smaller than Text at equal size
MATH_SMALL = 40         # ticks and units; reads like SMALL_SIZE

# --- geometry ------------------------------------------------------------
MARGIN = 0.55           # free border around all content, in Manim units
AXIS_WIDTH = 1.6
CURVE_WIDTH = 4.0
THIN_WIDTH = 2.4
DOT_RADIUS = 0.075

EASE = rate_functions.ease_in_out_sine
LINEAR = rate_functions.linear


def density_rgb(level):
    """Map normalized levels in [0, 1] (array) to uint8 RGB with DENSITY_STOPS.

    Levels below 0 or not finite take the background colour BG.
    """
    import numpy as np

    stops = np.array([[int(c[i:i + 2], 16) for i in (1, 3, 5)] for c in DENSITY_STOPS], float)
    level = np.asarray(level, dtype=float)
    below = ~np.isfinite(level) | (level < 0)
    x = np.clip(np.nan_to_num(level, nan=0.0), 0.0, 1.0) * (len(stops) - 1)
    i = np.minimum(x.astype(int), len(stops) - 2)
    w = (x - i)[..., None]
    rgb = (1 - w) * stops[i] + w * stops[i + 1]
    rgb[below] = [int(BG[k:k + 2], 16) for k in (1, 3, 5)]
    return np.round(rgb).astype(np.uint8)


def label(text, color=MUTED, size=LABEL_SIZE, **kwargs):
    """Prose label in STIX Two Text."""
    return Text(text, color=color, font_size=size, **kwargs)


def math(tex, color=INK, size=MATH_SIZE, **kwargs):
    """LaTeX label in STIX Two Math (TEX_TEMPLATE)."""
    return MathTex(tex, color=color, font_size=size, **kwargs)


def axes(x_range, y_range, x_length, y_length, ticks=True, **kwargs):
    """Quiet axes: thin grey lines, short ticks, no arrow tips."""
    axis_config = {
        "color": AXIS,
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


def axis_labels(ax, x_tex, y_tex, size=MATH_SMALL):
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
        with ExitStack() as stack:
            for font_file in _font_files():
                stack.enter_context(register_font(font_file))
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


def _font_files():
    """STIX Two Text OTF files; empty when only a system install exists."""
    for folder in FONT_DIRS:
        path = os.path.join(folder, "STIXTwoText-Regular.otf") if folder else ""
        if path and os.path.isfile(path):
            return [os.path.join(folder, f) for f in sorted(os.listdir(folder))
                    if f.startswith("STIXTwoText-") and f.endswith(".otf")]
    return []


def _name(mob):
    return getattr(mob, "text", None) or getattr(mob, "tex_string", None) or repr(mob)
