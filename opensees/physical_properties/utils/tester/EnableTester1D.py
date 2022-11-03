## @package EnableTester1D
# The EnableTester1D module can be used in all 1D materials by simply adding 1 import line to
# enable the tester
#
# from opensees.physical_properties.utils.tester.EnableTester1D import *

from opensees.physical_properties.utils.tester.Tester1D import Tester1DWidget
from opensees.utils.override_utils import get_function_from_module

class Tester1DGuiGlobals:
	# stores a reference to the gui generated for this object
	gui = None

def __removeGui():
	if Tester1DGuiGlobals.gui is not None:
		Tester1DGuiGlobals.gui.setParent(None)
		Tester1DGuiGlobals.gui.deleteLater()
		Tester1DGuiGlobals.gui = None

_onEditorClosing = get_function_from_module(__name__, 'onEditorClosing')
def onEditorClosing(editor, xobj):
	if _onEditorClosing: _onEditorClosing(editor, xobj)
	__removeGui()

_onEditFinished = get_function_from_module(__name__, 'onEditFinished')
def onEditFinished(editor, xobj):
	if _onEditFinished: _onEditFinished(editor, xobj)
	if Tester1DGuiGlobals.gui is not None:
		Tester1DGuiGlobals.gui.onEditFinished()

_onEditBegin = get_function_from_module(__name__, 'onEditBegin')
def onEditBegin(editor, xobj):
	if _onEditBegin: _onEditBegin(editor, xobj)
	__removeGui()
	Tester1DGuiGlobals.gui = Tester1DWidget(editor, xobj)
