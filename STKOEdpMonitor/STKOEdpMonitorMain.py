"""
Entry point of the STKO EDP Monitor standalone app.

Run in the suite ROOT directory (the launcher ``cd``s there): the plot widget
polls ``.edp`` records + ``runs.json`` in ``os.getcwd()`` and aggregates them
live. Mirrors STKOMonitorMain: it finds PySide2 / matplotlib / numpy and the Qt
DLLs through ``STKO_INSTALL_DIR`` when started by STKO, and adds its own bundle
directory to ``sys.path`` so the flat imports (STKOEdpMonitorWindow,
nlth_edp_aggregate, edp_realtime) resolve regardless of the working directory.
"""
import os
import sys


def run():
    from PySide2.QtCore import QLocale
    from PySide2.QtWidgets import QApplication
    from STKOEdpMonitorWindow import STKOEdpMonitorWindow
    from stko_theme import apply_theme
    app = QApplication(sys.argv)
    apply_theme(app)                     # STKO light theme (stko_light.css)
    def_locale = QLocale(QLocale.English, QLocale.AnyCountry)
    def_locale.setNumberOptions(
        QLocale.OmitGroupSeparator | QLocale.RejectGroupSeparator)
    QLocale.setDefault(def_locale)
    form = STKOEdpMonitorWindow()
    form.show()
    sys.exit(app.exec_())


# the bundle directory holds the flat-imported modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# find PySide2 / matplotlib / numpy + the Qt DLLs when launched by STKO
if "STKO_INSTALL_DIR" in os.environ:
    stko_dir = os.environ["STKO_INSTALL_DIR"]
    sys.path.insert(0, "{}/python_packages".format(stko_dir))
    path_name = "PATH"
    path = os.environ.get(path_name, "")
    os.environ[path_name] = "{}{}{}".format(stko_dir, os.pathsep, path)

run()
