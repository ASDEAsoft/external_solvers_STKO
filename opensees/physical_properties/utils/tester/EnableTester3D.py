## @package EnableTester3D
# The EnableTester3D module can be used in all 3D materials by simply adding 1 import line to
# enable the tester
#
# from opensees.physical_properties.utils.tester.EnableTester3D import *

from opensees.physical_properties.utils.tester.TesterND import NDTraits, TesterNDWidget
from opensees.utils.override_utils import get_function_from_module

class Tester3DGuiGlobals:
	# stores a reference to the gui generated for this object
	gui = None

def __removeGui():
	if Tester3DGuiGlobals.gui is not None:
		Tester3DGuiGlobals.gui.setParent(None)
		Tester3DGuiGlobals.gui.deleteLater()
		Tester3DGuiGlobals.gui = None

_onEditorClosing = get_function_from_module(__name__, 'onEditorClosing')
def onEditorClosing(editor, xobj):
	if _onEditorClosing: _onEditorClosing(editor, xobj)
	__removeGui()

_onEditFinished = get_function_from_module(__name__, 'onEditFinished')
def onEditFinished(editor, xobj):
	if _onEditFinished: _onEditFinished(editor, xobj)
	if Tester3DGuiGlobals.gui is not None:
		Tester3DGuiGlobals.gui.onEditFinished()

_onEditBegin = get_function_from_module(__name__, 'onEditBegin')
def onEditBegin(editor, xobj):
	if _onEditBegin: _onEditBegin(editor, xobj)
	__removeGui()
	Tester3DGuiGlobals.gui = TesterNDWidget(NDTraits.D3, editor, xobj)
