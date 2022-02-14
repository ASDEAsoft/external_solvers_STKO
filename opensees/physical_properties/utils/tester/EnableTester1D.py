## @package EnableTester1D
# The EnableTester1D module can be used in all 1D materials by simply adding 1 import line to
# enable the tester
#
# from opensees.physical_properties.utils.tester.EnableTester1D import *

from opensees.physical_properties.utils.tester.Tester1D import Tester1DWidget

class Tester1DGuiGlobals:
	# stores a reference to the gui generated for this object
	gui = None

def __removeGui():
	if Tester1DGuiGlobals.gui is not None:
		Tester1DGuiGlobals.gui.setParent(None)
		Tester1DGuiGlobals.gui.deleteLater()
		Tester1DGuiGlobals.gui = None

def onEditorClosing(editor, xobj):
	__removeGui()

def onEditFinished(editor, xobj):
	if Tester1DGuiGlobals.gui is not None:
		Tester1DGuiGlobals.gui.onEditFinished()

def onEditBegin(editor, xobj):
	__removeGui()
	Tester1DGuiGlobals.gui = Tester1DWidget(editor, xobj)
