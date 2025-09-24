'''
This module contains the MaterialEditor class for editing material properties in STKO's OpenSees interface.
It uses PySide2 for the GUI and integrates with STKO's XObject system.
'''

from opspro.physical_properties.MaterialDetails.MaterialClass import MaterialClass

'''
Let's define a simple widget for editing the MaterialClass object.
In a Vertical layout, we will have three fields: E, v, and rho, as pairs of label and line edit.
'''

from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
from PySide2.QtCore import Qt

class MaterialEditor(QWidget):
    def __init__(self, material: MaterialClass, parent=None):
        super().__init__(parent)
        self.material = material

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        

        