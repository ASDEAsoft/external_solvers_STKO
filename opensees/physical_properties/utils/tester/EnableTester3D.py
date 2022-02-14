## @package EnableTester3D
# The EnableTester3D module can be used in all 3D materials by simply adding 1 import line to
# enable the tester
#
# from opensees.physical_properties.utils.tester.EnableTester3D import *

from opensees.physical_properties.utils.tester.TesterND import NDTraits, TesterNDWidget

class Tester3DGuiGlobals:
	# stores a reference to the gui generated for this object
	gui = None

def __removeGui():
	if Tester3DGuiGlobals.gui is not None:
		Tester3DGuiGlobals.gui.setParent(None)
		Tester3DGuiGlobals.gui.deleteLater()
		Tester3DGuiGlobals.gui = None

def onEditorClosing(editor, xobj):
	__removeGui()

def onEditFinished(editor, xobj):
	if Tester3DGuiGlobals.gui is not None:
		Tester3DGuiGlobals.gui.onEditFinished()

def onEditBegin(editor, xobj):
	__removeGui()
	Tester3DGuiGlobals.gui = TesterNDWidget(NDTraits.D3, editor, xobj)
