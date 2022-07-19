## @package EnableTester2DPlaneStress
# The EnableTester2DPlaneStress module can be used in all 2DPlaneStress materials by simply adding 1 import line to
# enable the tester
#
# from opensees.physical_properties.utils.tester.EnableTester2DPlaneStress import *

from opensees.physical_properties.utils.tester.TesterND import NDTraits, TesterNDWidget
from opensees.utils.override_utils import get_function_from_module

class Tester2DPlaneStressGuiGlobals:
	# stores a reference to the gui generated for this object
	gui = None

def __removeGui():
	if Tester2DPlaneStressGuiGlobals.gui is not None:
		Tester2DPlaneStressGuiGlobals.gui.setParent(None)
		Tester2DPlaneStressGuiGlobals.gui.deleteLater()
		Tester2DPlaneStressGuiGlobals.gui = None

_onEditorClosing = get_function_from_module(__name__, 'onEditorClosing')
def onEditorClosing(editor, xobj):
	if _onEditorClosing: _onEditorClosing(editor, xobj)
	__removeGui()

_onEditFinished = get_function_from_module(__name__, 'onEditFinished')
def onEditFinished(editor, xobj):
	if _onEditFinished: _onEditFinished(editor, xobj)
	if Tester2DPlaneStressGuiGlobals.gui is not None:
		Tester2DPlaneStressGuiGlobals.gui.onEditFinished()

_onEditBegin = get_function_from_module(__name__, 'onEditBegin')
def onEditBegin(editor, xobj):
	if _onEditBegin: _onEditBegin(editor, xobj)
	__removeGui()
	Tester2DPlaneStressGuiGlobals.gui = TesterNDWidget(NDTraits.D2_PSTRESS, editor, xobj)
