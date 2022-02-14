## @package EnableTesterDistribution
# The EnableTesterDistribution module can be used in all randomVariables by simply adding 1 import line to
# enable the tester
#
# from opensees.defintions.utils.tester.EnableTesterDistribution import *

from opensees.definitions.utils.tester.TesterDistribution import TesterDistributionWidget

class TesterDistributionGuiGlobals:
	# stores a reference to the gui generated for this object
	gui = None

def __removeGui():
	if TesterDistributionGuiGlobals.gui is not None:
		TesterDistributionGuiGlobals.gui.setParent(None)
		TesterDistributionGuiGlobals.gui.deleteLater()
		TesterDistributionGuiGlobals.gui = None

def onEditorClosing(editor, xobj):
	__removeGui()

def onEditFinished(editor, xobj):
	if TesterDistributionGuiGlobals.gui is not None:
		TesterDistributionGuiGlobals.gui.onEditFinished()

def onEditBegin(editor, xobj):
	__removeGui()
	TesterDistributionGuiGlobals.gui = TesterDistributionWidget(editor, xobj)
