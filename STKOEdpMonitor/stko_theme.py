"""
STKO light-theme loader for the standalone STKO Qt apps (EDP Monitor, ...).

These apps run in their OWN process with a plain ``QApplication``: the global
stylesheet STKO installs on its C++ ``QApplication`` cannot reach them (different
process, and ``:/Style/stko_style_default`` is a Qt resource compiled into the
STKO executable). So each standalone app applies this self-contained theme on
its own.

Usage — right after creating the QApplication, before showing any window:

    from stko_theme import apply_theme
    apply_theme(app)

The ``stko_light.css`` stylesheet lives next to this module, so it is found
regardless of the process working directory.
"""
import os

from PySide2.QtWidgets import QProxyStyle, QStyle, QStyleFactory

# Fusion renders the Qt Style Sheet sub-controls (combo drop-down arrow, check
# indicator, dock buttons, ...) from the palette WITHOUT bundled PNGs, which is
# what keeps stko_light.css resource-free. Applying the same QSS on top of the
# native Windows style would blank those sub-controls, so force Fusion first.
_BASE_STYLE = "Fusion"
_CSS_FILE = "stko_light.css"


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
    """Apply the STKO light theme to *app*.

    Never raises: a missing or malformed stylesheet must never stop a monitor
    from opening — it just falls back to the un-themed default.
    """
    try:
        base = QStyleFactory.create(_BASE_STYLE)
        if base is not None:
            app.setStyle(_ComboPopupBelowStyle(base))
        else:
            app.setStyle(_BASE_STYLE)
    except Exception:
        pass
    try:
        css_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), _CSS_FILE)
        with open(css_path, "r", encoding="utf-8") as fh:
            app.setStyleSheet(fh.read())
    except Exception:
        pass
