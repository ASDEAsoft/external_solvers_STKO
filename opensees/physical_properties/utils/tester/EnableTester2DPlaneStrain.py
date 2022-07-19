## @package EnableTester2DPlaneStrain
# The EnableTester2DPlaneStrain module can be used in all 2DPlaneStrain materials by simply adding 1 import line to
# enable the tester
#
# from opensees.physical_properties.utils.tester.EnableTester2DPlaneStrain import *

from opensees.physical_properties.utils.tester.TesterND import NDTraits, TesterNDWidget
from opensees.utils.override_utils import get_function_from_module

class Tester2DPlaneStrainGuiGlobals:
	# stores a reference to the gui generated for this object
	gui = None

def __removeGui():
	if Tester2DPlaneStrainGuiGlobals.gui is not None:
		Tester2DPlaneStrainGuiGlobals.gui.setParent(None)
		Tester2DPlaneStrainGuiGlobals.gui.deleteLater()
		Tester2DPlaneStrainGuiGlobals.gui = None

_onEditorClosing = get_function_from_module(__name__, 'onEditorClosing')
def onEditorClosing(editor, xobj):
	if _onEditorClosing: _onEditorClosing(editor, xobj)
	__removeGui()

_onEditFinished = get_function_from_module(__name__, 'onEditFinished')
def onEditFinished(editor, xobj):
	if _onEditFinished: _onEditFinished(editor, xobj)
	if Tester2DPlaneStrainGuiGlobals.gui is not None:
		Tester2DPlaneStrainGuiGlobals.gui.onEditFinished()

_onEditBegin = get_function_from_module(__name__, 'onEditBegin')
def onEditBegin(editor, xobj):
	if _onEditBegin: _onEditBegin(editor, xobj)
	__removeGui()
	Tester2DPlaneStrainGuiGlobals.gui = TesterNDWidget(NDTraits.D2_PSTRAIN, editor, xobj)
