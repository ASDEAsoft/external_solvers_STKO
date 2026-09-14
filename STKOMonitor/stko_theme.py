"""
STKO theme for the standalone Qt apps (STKOMonitor, STKO EDP Monitor, ...).

These apps run in their OWN process with a plain ``QApplication``. Neither the
palette STKO installs nor its style sheet can reach them: a different process,
and ``:/Style/stko_style_default`` is a Qt resource compiled into the STKO
executable. So each one themes itself, from the same tokens the application uses.

Three pieces, all next to this file:

* ``stko_theme_tokens.json`` -- the colours, generated from the application's own
  ``AsTheme`` (``As/AsWidgets/AsTheme.cpp``) by
  ``STKO/build_utils/export_theme_tokens.py``. Generated rather than re-typed:
  a hand-kept second palette is a palette that drifts.
* ``stko_style.css`` -- one style sheet for both themes, written in ``@token``
  placeholders.
* this module -- picks the theme, expands the tokens, applies style + palette.

Which theme is active arrives in the ``STKO_THEME`` environment variable, set by
``StkoApplication`` and inherited through the launcher ``.bat``/``.sh``. Absent
(the app started by hand), it falls back to light.

Usage -- right after creating the QApplication, before showing any window::

    from stko_theme import apply_theme
    apply_theme(app)

THIS IS THE MASTER COPY, in ``external_solvers/_theme/``. The per-app copies are
written by ``export_theme_tokens.py``: edit this one, then re-run it.
"""
import json
import os

from PySide2.QtGui import QColor, QPalette
from PySide2.QtWidgets import QProxyStyle, QStyle, QStyleFactory

# Fusion renders the Qt Style Sheet sub-controls (combo drop-down arrow, check
# indicator, dock buttons, ...) from the palette WITHOUT bundled PNGs, which is
# what keeps the style sheet resource-free. It is also the only style that
# honours a palette on every platform -- the native Windows style would ignore
# it and render a dark theme half-light.
_BASE_STYLE = "Fusion"
_CSS_FILE = "stko_style.css"
_TOKENS_FILE = "stko_theme_tokens.json"

_HERE = os.path.dirname(os.path.abspath(__file__))

# Last-resort values, used only if the generated JSON is missing. Deliberately
# just enough to keep a window readable, not a second copy of the palette: if
# these are ever what you see, the token file failed to ship.
_FALLBACK = {
    "light": {"windowBg": "#ffffff", "baseBg": "#ffffff", "textColor": "#000000",
              "highlight": "#1883d7", "selectedText": "#ffffff"},
    "dark": {"windowBg": "#2d303a", "baseBg": "#22242c", "textColor": "#dee0e4",
             "highlight": "#1883d7", "selectedText": "#ffffff"},
}


def theme_name():
    """'dark' or 'light' -- what STKO told us, defaulting to light."""
    value = (os.environ.get("STKO_THEME") or "").strip().lower()
    return "dark" if value == "dark" else "light"


def is_dark():
    return theme_name() == "dark"


def tokens():
    """The active theme's colours, as {name: '#rrggbb'}."""
    name = theme_name()
    try:
        with open(os.path.join(_HERE, _TOKENS_FILE), "r", encoding="utf-8") as fh:
            return json.load(fh)[name]
    except Exception:
        return dict(_FALLBACK[name])


def color(token, default="#808080"):
    """One colour, by token name. For the code that paints outside Qt --
    matplotlib figures, hand-drawn canvases -- which no style sheet reaches."""
    return tokens().get(token, default)


def expand(css, values=None):
    """Replace every ``@token`` with its colour.

    Longest name first: several tokens are prefixes of another ('borders' of
    'bordersMid'), and replacing the short one first would leave the tail behind
    as literal text. Same rule as AsTheme::expandStyleSheet on the C++ side.
    """
    values = tokens() if values is None else values
    for name in sorted(values, key=len, reverse=True):
        css = css.replace("@" + name, values[name])
    return css


def palette(values=None):
    """A QPalette for the active theme, from the same tokens."""
    values = tokens() if values is None else values

    def col(name, default="#808080"):
        return QColor(values.get(name, default))

    pal = QPalette()
    text = col("textColor")
    hl = col("highlight")
    pal.setColor(QPalette.Window, col("dialogBg", values.get("windowBg", "#ffffff")))
    pal.setColor(QPalette.WindowText, text)
    pal.setColor(QPalette.Base, col("baseBg"))
    pal.setColor(QPalette.AlternateBase, col("altBaseBg"))
    pal.setColor(QPalette.ToolTipBase, col("tooltipBg"))
    pal.setColor(QPalette.ToolTipText, text)
    pal.setColor(QPalette.Text, text)
    pal.setColor(QPalette.Button, col("buttonBg"))
    pal.setColor(QPalette.ButtonText, text)
    pal.setColor(QPalette.BrightText, col("errorText"))
    pal.setColor(QPalette.Link, hl)
    pal.setColor(QPalette.Highlight, hl)
    pal.setColor(QPalette.HighlightedText, col("selectedText"))
    disabled = col("disabledText")
    for role in (QPalette.WindowText, QPalette.Text, QPalette.ButtonText,
                 QPalette.HighlightedText):
        pal.setColor(QPalette.Disabled, role, disabled)
    return pal


class _ComboPopupBelowStyle(QProxyStyle):
    """Fusion pops a combo box's list up CENTRED OVER the widget (a macOS-style
    menu), unlike the native Windows style which drops it below. Force the plain
    drop-down-below behaviour by pinning SH_ComboBox_Popup off; everything else
    is delegated to the wrapped Fusion style unchanged."""

    def styleHint(self, hint, option=None, widget=None, returnData=None):
        if hint == QStyle.SH_ComboBox_Popup:
            return 0
        return super(_ComboPopupBelowStyle, self).styleHint(
            hint, option, widget, returnData)


def apply_theme(app):
    """Apply the active STKO theme to *app*.

    Never raises: a missing or malformed style sheet must never stop a monitor
    from opening -- it just falls back to the un-themed default.
    """
    values = tokens()
    try:
        base = QStyleFactory.create(_BASE_STYLE)
        if base is not None:
            app.setStyle(_ComboPopupBelowStyle(base))
        else:
            app.setStyle(_BASE_STYLE)
    except Exception:
        pass
    try:
        # The palette goes on BEFORE the style sheet: an active QStyleSheetStyle
        # snapshots the palette it finds, so setting it afterwards would not
        # reach the widgets the sheet manages. It also carries the theme to
        # everything the sheet does not mention.
        app.setPalette(palette(values))
    except Exception:
        pass
    try:
        with open(os.path.join(_HERE, _CSS_FILE), "r", encoding="utf-8") as fh:
            app.setStyleSheet(expand(fh.read(), values))
    except Exception:
        pass


# ---------------------------------------------------------------------------
#  matplotlib
#
#  A figure is drawn by matplotlib, not by Qt: no style sheet and no palette
#  reaches it, so a themed window used to end up with a white rectangle in the
#  middle of it. These two helpers are the whole of the fix -- the surface from
#  apply_mpl_theme(), the data colours from plot_colors().
# ---------------------------------------------------------------------------

def plot_colors():
    """Semantic colours for plotted data.

    The LIGHT values are the literals these plots already used (navy,
    steelblue, crimson, gray), so nothing moves in light; the dark ones are
    their readable counterparts -- navy on a #22242c background is a hole, not
    a line.
    """
    t = tokens()
    dark = is_dark()
    return {
        "ink": t.get("textColor", "#000000"),        # was "black"
        "muted": t.get("hintText", "#808080"),       # was "gray" / "0.6"
        "grid": t.get("chartGrid", "#c8c8c8"),
        "axis": t.get("chartAxis", "#909090"),
        "bg": t.get("chartBg", "#ffffff"),
        "primary": "#7aa2ff" if dark else "#000080",     # was "navy"
        "secondary": "#9ecbff" if dark else "#4682b4",   # was "steelblue"
        "accent": "#ff6b6b" if dark else "#dc143c",      # was "crimson"
    }


def curve_lightness(muted=False):
    """Lightness for generated per-curve hues: a hue that reads on white is
    too dark to read on the dark canvas.

    ``muted`` asks for the subdued companion of a curve (a background or
    previous-step line). Subdued means AWAY from the ink and TOWARDS the
    canvas, so it is lighter on white and darker on the dark canvas -- the same
    offset in the same direction would make it stand out more, not less.
    """
    base = 0.62 if is_dark() else 0.45
    if not muted:
        return base
    return base - 0.20 if is_dark() else base + 0.20


def apply_mpl_theme(fig, axes=None):
    """Paint a figure's surface in the active theme. Never raises."""
    colors = plot_colors()
    try:
        fig.set_facecolor(colors["bg"])
    except Exception:
        return
    if axes is None:
        try:
            axes = fig.get_axes()
        except Exception:
            axes = []
    elif not isinstance(axes, (list, tuple)):
        axes = [axes]
    for ax in axes:
        try:
            ax.set_facecolor(colors["bg"])
            for spine in ax.spines.values():
                spine.set_color(colors["axis"])
            ax.tick_params(colors=colors["ink"], which="both")
            ax.xaxis.label.set_color(colors["ink"])
            ax.yaxis.label.set_color(colors["ink"])
            ax.title.set_color(colors["ink"])
            legend = ax.get_legend()
            if legend is not None:
                frame = legend.get_frame()
                frame.set_facecolor(colors["bg"])
                frame.set_edgecolor(colors["axis"])
                for text in legend.get_texts():
                    text.set_color(colors["ink"])
        except Exception:
            pass
