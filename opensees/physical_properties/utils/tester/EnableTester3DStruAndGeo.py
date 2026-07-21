## @package EnableTester3DStruAndGeo
# The EnableTester3DStruAndGeo module can be used in all 3D materials by simply adding 1 import line to
# enable the tester
#
# from opensees.physical_properties.utils.tester.EnableTester3D import *

from opensees.physical_properties.utils.tester.TesterND import NDTraits, TesterNDWidget
from opensees.physical_properties.utils.tester.TesterGeotechnical import TesterGeotechnicalWidget

# TODO: replace with Jose's new implementation
# now a simple PySide2 QLabel implementation
from PySide2.QtWidgets import QTabWidget, QSplitter, QLabel
import shiboken2
from PyMpc import MpcXObjectEditorChildCode

# let's create a new class that is a QTabWidget with 2 tabs, 1 for TesterNDWidget and 1 for a simple QLabel
class Tester3DStruAndGeoGuiTabWidget(QTabWidget):
    def __init__(self, type, editor, xobj, parent = None):
        super().__init__(parent=parent)
        self.structural_tester = QLabel("Ge") #TesterNDWidget(type, editor, xobj, parent=self, embed=False)
        self.geotech_tester = TesterGeotechnicalWidget(type, editor, xobj, parent=self, embed=False)
        self.addTab(self.structural_tester, "Structural Tester")
        self.addTab(self.geotech_tester, "Geotechnical Tester")
		
        # emdbed here
        self.editor_splitter = shiboken2.wrapInstance(editor.getChildPtr(MpcXObjectEditorChildCode.MainSplitter), QSplitter)
        self.editor_splitter.addWidget(self)
        total_width = self.editor_splitter.size().width()
        width_1 = total_width//3
        self.editor_splitter.setSizes([width_1, total_width - width_1])

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
	Tester3DGuiGlobals.gui = Tester3DStruAndGeoGuiTabWidget(NDTraits.D3, editor, xobj)
