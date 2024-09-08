## @package EnableTesterTIM6D
# The EnableTesterTIM6D module can be used in all TIM materials by simply adding 1 import line to
# enable the tester
#
# from opensees.physical_properties.utils.tester.EnableTesterTIM6D import *

from opensees.physical_properties.utils.tester.TesterTIM6D import TIMTraits, TesterTIM6DWidget

class TesterTIM6DGuiGlobals:
	# stores a reference to the gui generated for this object
	gui = None

def __removeGui():
	if TesterTIM6DGuiGlobals.gui is not None:
		TesterTIM6DGuiGlobals.gui.setParent(None)
		TesterTIM6DGuiGlobals.gui.deleteLater()
		TesterTIM6DGuiGlobals.gui = None

def onEditorClosing(editor, xobj):
	__removeGui()

def onEditFinished(editor, xobj):
	if TesterTIM6DGuiGlobals.gui is not None:
		TesterTIM6DGuiGlobals.gui.onEditFinished()

def onEditBegin(editor, xobj):
	__removeGui()
	TesterTIM6DGuiGlobals.gui = TesterTIM6DWidget(TIMTraits.D3, editor, xobj)
