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
-- the app started by hand from its own launcher, with no STKO above it to
inherit from -- the setting STKO saved is read directly, and only then does it
fall back to light.

Usage -- right after creating the QApplication, before showing any window::

    from stko_theme import apply_theme
    apply_theme(app)

THIS IS THE MASTER COPY, in ``external_solvers/_theme/``. The per-app copies are
written by ``export_theme_tokens.py``: edit this one, then re-run it.
"""
import json
import os

from PySide2.QtCore import QPointF, QRectF, Qt
from PySide2.QtGui import QColor, QPainter, QPainterPath, QPalette, QPolygonF
from PySide2.QtWidgets import (QProxyStyle, QStyle, QStyleFactory, QStyleOptionHeader,
                               QStyleOptionTab, QStyleOptionTabBarBase,
                               QStyleOptionTabWidgetFrame, QTabBar)

# Fusion renders the Qt Style Sheet sub-controls (combo drop-down arrow, check
# indicator, dock buttons, ...) from the palette WITHOUT bundled PNGs, which is
# what keeps the style sheet resource-free. It is also the only style that
# honours a palette on every platform -- the native Windows style would ignore
# it and render a dark theme half-light.
_BASE_STYLE = "Fusion"
_CSS_FILE = "stko_style.css"
_TOKENS_FILE = "stko_theme_tokens.json"

_HERE = os.path.dirname(os.path.abspath(__file__))

# Where STKO keeps the theme, for when there is no environment variable to read.
# Same three strings StkoTheme uses: STKO_APP_ORGNAME and STKO_APP_NAME from
# StkoApplicationConfig.h, and the group/key from StkoThemeManager.cpp.
#
# The PRO name, and only that one: STKO_HAS_DARK_THEME is gated on
# __STKO_PRO_VERSION__, so the standard flavour has no dark theme and never
# writes this key. Reading the one name that can hold "dark" is the whole job.
_SETTINGS_ORG = "ASDEA Software Technology"
_SETTINGS_APP = "STKO Pro"
_SETTINGS_KEY = "STKOApplication/Theme"

# Resolved once and kept: the theme is fixed for the life of a process, which is
# what STKO does too (StkoTheme::current() locks on first call).
_resolved_theme = None

# Last-resort values, used only if the generated JSON is missing. Deliberately
# just enough to keep a window readable, not a second copy of the palette: if
# these are ever what you see, the token file failed to ship.
_FALLBACK = {
    "light": {"windowBg": "#ffffff", "baseBg": "#ffffff", "textColor": "#000000",
              "highlight": "#1883d7", "selectionBg": "#cde5f7",
              "selectedText": "#000000"},
    "dark": {"windowBg": "#2e3b4c", "baseBg": "#26323d", "textColor": "#dee0e4",
             "highlight": "#1883d7", "selectionBg": "#41546c",
             "selectedText": "#dee0e4"},
}


def _saved_theme():
    """The theme STKO has stored, or None if it never has.

    QSettings with the format, scope, organisation and application spelled out,
    because this process is not STKO and has none of them set on its
    QCoreApplication. On Windows that is the same registry key STKO writes; on
    macOS QSettings identifies the organisation by DOMAIN rather than by name,
    and STKO happens to set both to the same string, so this resolves there too.

    Reading a setting rather than a live value is not a compromise here: STKO
    asks for a restart to change theme, so what is stored IS what any STKO on
    this machine is running or will run next.
    """
    try:
        from PySide2.QtCore import QSettings
        settings = QSettings(QSettings.NativeFormat, QSettings.UserScope,
                             _SETTINGS_ORG, _SETTINGS_APP)
        value = settings.value(_SETTINGS_KEY)
        return str(value).strip().lower() if value is not None else None
    except Exception:
        # No PySide2 yet, no registry access, a locked-down user profile: the
        # theme is a detail, and none of them is worth failing a launch over.
        return None


def theme_name():
    """'dark' or 'light': what STKO told us, else what it saved, else light."""
    global _resolved_theme
    if _resolved_theme is None:
        value = (os.environ.get("STKO_THEME") or "").strip().lower()
        if value not in ("dark", "light"):
            value = _saved_theme() or ""
        _resolved_theme = "dark" if value == "dark" else "light"
    return _resolved_theme


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
    # The selection is a wash, not the accent: see AsTheme::selectionBg.
    pal.setColor(QPalette.Highlight, col("selectionBg", values.get("highlight", "#1883d7")))
    pal.setColor(QPalette.HighlightedText, col("selectedText"))
    disabled = col("disabledText")
    for role in (QPalette.WindowText, QPalette.Text, QPalette.ButtonText,
                 QPalette.HighlightedText):
        pal.setColor(QPalette.Disabled, role, disabled)
    return pal


class _StkoStyle(QProxyStyle):
    """The handful of controls STKO does not leave to Fusion.

    A SECOND implementation of what ``STKO/StkoStyle.cpp`` draws, and said so
    plainly: a check box's tick, a radio button's dot, a table header, the
    shape of a tab. There is no way to share the first one -- these monitors are
    separate processes running PySide2's own build of Qt, so the C++ style
    cannot be loaded into them at any price.

    What CAN be shared is shared already: the colours come from the same
    generated tokens, so the two drift in shape, never in colour. Anything
    changed in the C++ counterpart belongs here too; each method names the
    element it mirrors.

    Everything not listed here is Fusion's, exactly as in STKO.
    """

    def __init__(self, base, values):
        super(_StkoStyle, self).__init__(base)
        self._values = values

    def _color(self, name, default="#808080"):
        return QColor(self._values.get(name, default))

    def styleHint(self, hint, option=None, widget=None, returnData=None):
        # Fusion pops a combo box's list up CENTRED OVER the widget, the way a
        # macOS menu does. Dropping it below is what every other control in
        # these windows leads you to expect; STKO keeps Fusion's behaviour, so
        # this is the one place the two deliberately differ.
        if hint == QStyle.SH_ComboBox_Popup:
            return 0
        return super(_StkoStyle, self).styleHint(hint, option, widget, returnData)

    # -- primitives ---------------------------------------------------------

    def drawPrimitive(self, element, option, painter, widget=None):
        if element == QStyle.PE_IndicatorCheckBox:
            self._draw_check_box(option, painter)
            return
        if element == QStyle.PE_IndicatorRadioButton:
            self._draw_radio_button(option, painter)
            return
        if element == QStyle.PE_FrameTabWidget and self._draw_tab_frame(option, painter):
            return
        if element == QStyle.PE_FrameTabBarBase and self._draw_tab_base(option, painter):
            return
        super(_StkoStyle, self).drawPrimitive(element, option, painter, widget)

    def drawControl(self, element, option, painter, widget=None):
        if element in (QStyle.CE_HeaderSection, QStyle.CE_HeaderEmptyArea):
            self._draw_header(element, option, painter)
            return
        if element == QStyle.CE_TabBarTabShape and self._draw_tab(option, painter):
            return
        super(_StkoStyle, self).drawControl(element, option, painter, widget)

    # -- StkoStyle.cpp, PE_IndicatorCheckBox ---------------------------------

    def _draw_check_box(self, option, painter):
        """A filled accent box with a white tick, instead of Fusion's outlined
        box with a dark tick where on and off differ by a few pixels."""
        enabled = bool(option.state & QStyle.State_Enabled)
        on = bool(option.state & QStyle.State_On)
        partial = bool(option.state & QStyle.State_NoChange)
        hover = enabled and bool(option.state & QStyle.State_MouseOver)

        # Square and centred: the rect Fusion hands over can be a pixel taller
        # than wide. The half-pixel inset puts the 1px outline ON the grid.
        side = min(option.rect.width(), option.rect.height())
        box = QRectF(0, 0, side, side)
        box.moveCenter(QRectF(option.rect).center())
        outline = box.adjusted(0.5, 0.5, -0.5, -0.5)

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)
        if on or partial:
            fill = self._color("highlight") if enabled else self._color("disabledText")
            painter.setPen(fill)
            painter.setBrush(fill)
            painter.drawRoundedRect(outline, 2.0, 2.0)

            # White in BOTH themes: it sits on the accent, not on the surface.
            pen = painter.pen()
            pen.setColor(QColor(255, 255, 255))
            pen.setWidthF(max(1.5, side / 8.0))
            pen.setCapStyle(Qt.RoundCap)
            pen.setJoinStyle(Qt.RoundJoin)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            if partial:
                painter.drawLine(QPointF(box.left() + side * 0.26, box.center().y() + 0.5),
                                 QPointF(box.right() - side * 0.26, box.center().y() + 0.5))
            else:
                tick = QPolygonF([QPointF(box.left() + side * 0.24, box.top() + side * 0.52),
                                  QPointF(box.left() + side * 0.42, box.top() + side * 0.71),
                                  QPointF(box.left() + side * 0.76, box.top() + side * 0.29)])
                painter.drawPolyline(tick)
        else:
            painter.setBrush(self._color("baseBg") if enabled else self._color("dialogBg"))
            painter.setPen(self._color("highlight") if hover else self._color("bordersStrong"))
            painter.drawRoundedRect(outline, 2.0, 2.0)
        painter.restore()

    # -- StkoStyle.cpp, PE_IndicatorRadioButton ------------------------------

    def _draw_radio_button(self, option, painter):
        """The same answer made round: a filled accent disc with a white dot."""
        enabled = bool(option.state & QStyle.State_Enabled)
        on = bool(option.state & QStyle.State_On)
        hover = enabled and bool(option.state & QStyle.State_MouseOver)

        side = min(option.rect.width(), option.rect.height())
        box = QRectF(0, 0, side, side)
        box.moveCenter(QRectF(option.rect).center())
        outline = box.adjusted(0.5, 0.5, -0.5, -0.5)

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)
        if on:
            fill = self._color("highlight") if enabled else self._color("disabledText")
            painter.setPen(fill)
            painter.setBrush(fill)
            painter.drawEllipse(outline)
            # Three eighths of the disc: the tick's weight, read as an area.
            dot = side * 0.375
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(255, 255, 255))
            painter.drawEllipse(QRectF(box.center().x() + 0.5 - dot / 2.0,
                                       box.center().y() + 0.5 - dot / 2.0, dot, dot))
        else:
            painter.setBrush(self._color("baseBg") if enabled else self._color("dialogBg"))
            painter.setPen(self._color("highlight") if hover else self._color("bordersStrong"))
            painter.drawEllipse(outline)
        painter.restore()

    # -- StkoStyle.cpp, CE_HeaderSection / CE_HeaderEmptyArea -----------------

    def _draw_header(self, element, option, painter):
        """A flat strip closed by ONE line, not a row of raised keys.

        The empty area past the last section comes with a plain QStyleOption and
        states its orientation in State_Horizontal -- QHeaderView does that for
        exactly this case.
        """
        header = option if isinstance(option, QStyleOptionHeader) else None
        if header is not None:
            horizontal = header.orientation == Qt.Horizontal
        else:
            horizontal = bool(option.state & QStyle.State_Horizontal)
        r = option.rect

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, False)
        painter.fillRect(r, self._color("buttonBg"))
        painter.setPen(self._color("borders"))
        if horizontal:
            painter.drawLine(r.left(), r.bottom(), r.right(), r.bottom())
        else:
            painter.drawLine(r.right(), r.top(), r.right(), r.bottom())
        # The seam between two sections; never after the last one, never in the
        # empty area, which has no sections to separate.
        if header is not None and header.position not in (QStyleOptionHeader.End,
                                                          QStyleOptionHeader.OnlyOneSection):
            if horizontal:
                painter.drawLine(r.right(), r.top(), r.right(), r.bottom() - 1)
            else:
                painter.drawLine(r.left(), r.bottom(), r.right() - 1, r.bottom())
        painter.restore()

    # -- StkoStyle.cpp, CE_TabBarTabShape ------------------------------------

    def _draw_tab(self, option, painter):
        """The current tab IS the colour of the page it opens onto; the others
        sit half a shade back. Fusion's tab is a gradient over a colour taken
        from Button or from Window depending on whether the tab widget has a
        frame, so two tab bars in one window came out two different off-whites.

        Returns False for shapes this does not handle, so they fall through.
        """
        if not isinstance(option, QStyleOptionTab):
            return False
        north = option.shape == QTabBar.RoundedNorth
        south = option.shape == QTabBar.RoundedSouth
        if not (north or south):
            return False

        selected = bool(option.state & QStyle.State_Selected)
        hover = not selected and bool(option.state & QStyle.State_MouseOver)
        rtl = option.direction == Qt.RightToLeft
        last = (option.position == QStyleOptionTab.OnlyOneTab
                or (not rtl and option.position == QStyleOptionTab.End)
                or (rtl and option.position == QStyleOptionTab.Beginning))
        overlap = 0 if last else self.pixelMetric(QStyle.PM_TabBarTabOverlap, option)

        # Where the page's edge falls INSIDE the strip: Fusion answers 2, and
        # the page is pushed up under the tab bar by the same amount.
        base = self.pixelMetric(QStyle.PM_TabBarBaseOverlap, option)
        edge = (option.rect.bottom() - base + 1) if north else (option.rect.top() + base - 1)

        rect = option.rect.adjusted(0, 0, overlap, 0)
        if not selected:
            rect.adjust(0, 2 if north else base, 0, -base if north else -2)

        # The rounded end is the one AWAY from the page, so the path is grown
        # past the clip on the page side where its rounding is cut off unseen.
        grow = 4.0
        if north:
            shape_rect = QRectF(rect.left() + 0.5, rect.top() + 0.5,
                                rect.width() - 1.0, rect.height() - 1.0 + grow)
        else:
            shape_rect = QRectF(rect.left() + 0.5, rect.top() + 0.5 - grow,
                                rect.width() - 1.0, rect.height() - 1.0 + grow)
        shape = QPainterPath()
        shape.addRoundedRect(shape_rect, 2.0, 2.0)

        page_bg = self._color("windowBg")
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.save()
        # The open tab stops ON the page's edge row, not past it: its rect is
        # the whole strip, base overlap included.
        clip = rect
        if selected:
            if north:
                clip.setBottom(edge)
            else:
                clip.setTop(edge)
        painter.setClipRect(clip)
        painter.fillPath(shape, page_bg if (selected or hover)
                         else self._color("tabInactiveBg"))
        painter.strokePath(shape, self._color("borders"))
        painter.restore()

        if not selected:
            # The page's edge carried across this tab, so the whole strip reads
            # as one line stopping at the two sides of the open one. WITHOUT
            # antialiasing: a 1px pen on an integer y would spread over two rows.
            painter.setRenderHint(QPainter.Antialiasing, False)
            painter.setPen(self._color("borders"))
            painter.drawLine(rect.left(), edge, rect.right(), edge)
        painter.restore()
        return True

    # -- StkoStyle.cpp, PE_FrameTabWidget ------------------------------------

    def _draw_tab_frame(self, option, painter):
        """The page under the tabs, in the colour the current tab is, with the
        tab-side edge broken under that tab -- and the gap is what makes the
        open tab read as part of the page.

        It has to be drawn here and not in PE_FrameTabBarBase because
        QTabWidget::setTabBar() calls setDrawBase(false) on its tab bar, so
        inside a tab widget that primitive is never asked for.
        """
        frame = option if isinstance(option, QStyleOptionTabWidgetFrame) else None
        north = frame is None or frame.shape == QTabBar.RoundedNorth
        sided = frame is not None and frame.shape not in (QTabBar.RoundedNorth,
                                                          QTabBar.RoundedSouth)
        r = option.rect

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, False)
        painter.fillRect(r, self._color("windowBg"))
        painter.setPen(self._color("borders"))
        painter.setBrush(Qt.NoBrush)
        if sided:
            # drawRect takes width and height rather than corners, so it closes
            # at right()+1: this is the one call that wants the shrunk rect.
            painter.drawRect(r.adjusted(0, 0, -1, -1))
        else:
            painter.drawLine(r.topLeft(), r.bottomLeft())
            painter.drawLine(r.topRight(), r.bottomRight())
            if north:
                painter.drawLine(r.bottomLeft(), r.bottomRight())
            else:
                painter.drawLine(r.topLeft(), r.topRight())
            y = r.top() if north else r.bottom()
            sel = frame.selectedTabRect if frame is not None else None
            if sel is not None and sel.isValid() and sel.width() > 0:
                if sel.left() - 1 >= r.left():
                    painter.drawLine(r.left(), y, sel.left() - 1, y)
                if sel.right() + 1 <= r.right():
                    painter.drawLine(sel.right() + 1, y, r.right(), y)
            else:
                painter.drawLine(r.left(), y, r.right(), y)
        painter.restore()
        return True

    # -- StkoStyle.cpp, PE_FrameTabBarBase -----------------------------------

    def _draw_tab_base(self, option, painter):
        """The same line for a tab bar that is NOT inside a tab widget, whose
        bar does draw its base. QTabBar hands over only the overlap rows, so the
        page's edge is the side of that band facing the page."""
        base = option if isinstance(option, QStyleOptionTabBarBase) else None
        if base is None or base.shape not in (QTabBar.RoundedNorth, QTabBar.RoundedSouth):
            return False
        north = base.shape == QTabBar.RoundedNorth
        y = option.rect.top() if north else option.rect.bottom()
        sel = base.selectedTabRect

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, False)
        painter.setPen(self._color("borders"))
        if sel.isValid() and sel.width() > 0:
            painter.drawLine(option.rect.left(), y, sel.left() - 1, y)
            painter.drawLine(sel.right() + 1, y, option.rect.right(), y)
        else:
            painter.drawLine(option.rect.left(), y, option.rect.right(), y)
        painter.restore()
        return True


def apply_theme(app):
    """Apply the active STKO theme to *app*.

    Never raises: a missing or malformed style sheet must never stop a monitor
    from opening -- it just falls back to the un-themed default.
    """
    values = tokens()
    try:
        base = QStyleFactory.create(_BASE_STYLE)
        if base is not None:
            app.setStyle(_StkoStyle(base, values))
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
