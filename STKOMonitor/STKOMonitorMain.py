import sys
import os

def run():
	from PySide2.QtCore import QLocale
	from PySide2.QtWidgets import QApplication
	from STKOMonitorWindow import STKOMonitorWindow
	# Create the Qt Application
	app = QApplication(sys.argv)
	# Create the english QLocale
	def_locale = QLocale(QLocale.English, QLocale.AnyCountry)
	def_locale.setNumberOptions(QLocale.OmitGroupSeparator | QLocale.RejectGroupSeparator)
	QLocale.setDefault(def_locale)
	# Create and show the form
	form = STKOMonitorWindow()
	form.show()
	sys.exit(app.exec_())

# add current direcotry
sys.path.insert(0, os.path.dirname(__file__))

# add STKO directories if we run it via STKO python
if 'STKO_INSTALL_DIR' in os.environ:
	stko_dir = os.environ['STKO_INSTALL_DIR']
	# to find extra packages as pyside2, matplotlib, etc...
	sys.path.insert(0, '{}/python_packages'.format(stko_dir))
	# to find Qt DLLs...
	path_name = 'PATH' # NOTE: valid on windows only! make it cross plat.
	path = ''
	if path_name in os.environ:
		path = os.environ[path_name]
	path = '{}{}{}'.format(stko_dir, os.pathsep, path)
	os.environ[path_name] = path

run()