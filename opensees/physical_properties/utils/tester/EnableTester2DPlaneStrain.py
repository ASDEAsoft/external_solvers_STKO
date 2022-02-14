## @package EnableTester2DPlaneStrain
# The EnableTester2DPlaneStrain module can be used in all 2DPlaneStrain materials by simply adding 1 import line to
# enable the tester
#
# from opensees.physical_properties.utils.tester.EnableTester2DPlaneStrain import *

from opensees.physical_properties.utils.tester.TesterND import NDTraits, TesterNDWidget

class Tester2DPlaneStrainGuiGlobals:
	# stores a reference to the gui generated for this object
	gui = None

def __removeGui():
	if Tester2DPlaneStrainGuiGlobals.gui is not None:
		Tester2DPlaneStrainGuiGlobals.gui.setParent(None)
		Tester2DPlaneStrainGuiGlobals.gui.deleteLater()
		Tester2DPlaneStrainGuiGlobals.gui = None

def onEditorClosing(editor, xobj):
	__removeGui()

def onEditFinished(editor, xobj):
	if Tester2DPlaneStrainGuiGlobals.gui is not None:
		Tester2DPlaneStrainGuiGlobals.gui.onEditFinished()

def onEditBegin(editor, xobj):
	__removeGui()
	Tester2DPlaneStrainGuiGlobals.gui = TesterNDWidget(NDTraits.D2_PSTRAIN, editor, xobj)
