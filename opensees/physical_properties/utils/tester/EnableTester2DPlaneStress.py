## @package EnableTester2DPlaneStress
# The EnableTester2DPlaneStress module can be used in all 2DPlaneStress materials by simply adding 1 import line to
# enable the tester
#
# from opensees.physical_properties.utils.tester.EnableTester2DPlaneStress import *

from opensees.physical_properties.utils.tester.TesterND import NDTraits, TesterNDWidget

class Tester2DPlaneStressGuiGlobals:
	# stores a reference to the gui generated for this object
	gui = None

def __removeGui():
	if Tester2DPlaneStressGuiGlobals.gui is not None:
		Tester2DPlaneStressGuiGlobals.gui.setParent(None)
		Tester2DPlaneStressGuiGlobals.gui.deleteLater()
		Tester2DPlaneStressGuiGlobals.gui = None

def onEditorClosing(editor, xobj):
	__removeGui()

def onEditFinished(editor, xobj):
	if Tester2DPlaneStressGuiGlobals.gui is not None:
		Tester2DPlaneStressGuiGlobals.gui.onEditFinished()

def onEditBegin(editor, xobj):
	__removeGui()
	Tester2DPlaneStressGuiGlobals.gui = TesterNDWidget(NDTraits.D2_PSTRESS, editor, xobj)
