import sys
import os

def run():
	from PySide6.QtCore import QLocale
	from PySide6.QtWidgets import QApplication
	from STKOMonitorWindow import STKOMonitorWindow
	from stko_theme import apply_theme
	# Create the Qt Application
	app = QApplication(sys.argv)
	# Light or dark, from the STKO_THEME variable STKO sets before
	# launching us. This window runs in its own process, so it has to
	# theme itself -- nothing of STKO's own styling can reach it.
	apply_theme(app)
	# Create the english QLocale
	def_locale = QLocale(QLocale.English, QLocale.AnyCountry)
	def_locale.setNumberOptions(QLocale.OmitGroupSeparator | QLocale.RejectGroupSeparator)
	QLocale.setDefault(def_locale)
	# Create and show the form
	form = STKOMonitorWindow()
	form.show()
	sys.exit(app.exec())

# PySide6's own qt.conf points at the Qt a PyPI wheel carries; STKO's PySide6
# runs on STKO's Qt, so let Qt find its plugins where it really is. Must come
# before the first PySide6 import (STKO sets it too; a manual run does not).
os.environ.setdefault('PYSIDE_DISABLE_INTERNAL_QT_CONF', '1')

# add current direcotry
sys.path.insert(0, os.path.dirname(__file__))

# add STKO directories if we run it via STKO python
if 'STKO_INSTALL_DIR' in os.environ:
	stko_dir = os.environ['STKO_INSTALL_DIR']
	# to find extra packages as pyside6, matplotlib, etc...
	sys.path.insert(0, '{}/python_packages'.format(stko_dir))
	# to find Qt DLLs...
	path_name = 'PATH' # NOTE: valid on windows only! make it cross plat.
	path = ''
	if path_name in os.environ:
		path = os.environ[path_name]
	path = '{}{}{}'.format(stko_dir, os.pathsep, path)
	os.environ[path_name] = path

run()