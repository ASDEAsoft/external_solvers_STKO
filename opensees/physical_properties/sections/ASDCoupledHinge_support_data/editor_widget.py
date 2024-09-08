import PyMpc.IO

import sys
import numpy as np
from PyMpc import *
from math import sin, cos, pi

import traceback
	
from PySide2.QtCore import (
	QSize,
	Qt,
	QLocale,
	)
from PySide2.QtWidgets import (
	QWidget,
	QDialog,
	QDialogButtonBox,
	QAbstractItemView,
	QTreeWidget,
	QTreeWidgetItem,
	QTextEdit,
	QGridLayout,
	QVBoxLayout,
	QHBoxLayout,
	QTabWidget,
	QLabel,
	QPushButton,
	QSizePolicy,
	QSlider,
	QLineEdit,
	QToolButton,
	QComboBox,
	QTableWidget,
	QTableWidgetItem,
	QStyledItemDelegate,
	)

from PySide2.QtGui import (
	QTextDocumentFragment,
	QDoubleValidator,
	QKeySequence,
	QGuiApplication,
	)
import shiboken2
# import random

# Expressions hard coded

# defaultExpressions = 

# End expressions hard coded

_verbose = False

from enum import Enum

def formatRecentExpressionHelp(label: str, expression: str):
	''' Returns a HTML formatted string for use as a recent expression iem help
	'''
	text = '<h3>Expression {}</h3>\n<div class="description"><p>{}</p></div><h4>{}</h4><div class = "description"><pre>{}</pre></div>'.format(
		label,
		"Recently used expression.",
		"Expression",
		expression)
		
	return text

		
class ASDTextEditSingleLine(QTextEdit):
	def __init__(self, text = '', parent = None):
		super().__init__(text = text, parent = parent)
		
	def keyPressEvent(self, event):
		# Prevent entering a new line from keyboard
		if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
			return
		# In other cases insert
		QTextEdit.keyPressEvent(self, event)
		
	def insertFromMimeData(self, source):
		print('Inser from mime')
		# re-implement paste
		if source.hasText():
			cursor = self.textCursor()
			# convert html to plain text before
			if source.hasHtml():
				text = QTextDocumentFragment.fromHtml(source.html()).toPlainText()
			else:
				text = source.text()
			# make a single line
			text = ''.join(text.splitlines())
			# done
			cursor.insertText(text)
			
class ASDTreeWidget(QTreeWidget):
	
	EXPRESSION_ROLE = Qt.UserRole + 1
	HELPSTRING_ROLE = Qt.UserRole + 2
	TYPE_ROLE = Qt.UserRole + 3
	
	class ItemType(int, Enum):
		HeaderItem = 0
		ExpressionItem = 1
		FieldItem = 2
	
	def __init__(self, parent = None):
		super().__init__(parent = parent)
		self.expressionGroups = {}
		
	def registerItem(self,
		group: str,
		label: str,
		expression: str,
		helpText: str):
		item = QTreeWidgetItem()
		item.setData(0,Qt.DisplayRole, label)
		item.setData(1,ASDTreeWidget.EXPRESSION_ROLE, expression)
		item.setData(2,ASDTreeWidget.HELPSTRING_ROLE, helpText)
		item.setData(3,ASDTreeWidget.TYPE_ROLE, ASDTreeWidget.ItemType.ExpressionItem)
		
		print('Data: ')
		print(item.data(0, Qt.DisplayRole))
		print(item.data(1, Qt.UserRole))
		print(item.data(1, ASDTreeWidget.EXPRESSION_ROLE))
		
		# Look if the group exists and insert there the new function
		groupNode = self.expressionGroups.get(group)
		if groupNode is not None:
			groupNode.addChild(item)
		else:
			# The group node does not exist, create it
			groupItem = QTreeWidgetItem()
			groupItem.setData(0,Qt.DisplayRole, group)
			groupItem.setData(2,ASDTreeWidget.HELPSTRING_ROLE, helpText)
			groupItem.setData(3,ASDTreeWidget.TYPE_ROLE, ASDTreeWidget.ItemType.HeaderItem)
			# Add the new item to the tree_root
			self.addTopLevelItem(groupItem)
			self.expressionGroups[group] = groupItem
			# Insert the expression to the group
			groupItem.addChild(item)
		

class EquationEditorWidget(QDialog):
	def __init__(self, title = '', parent = None):

		# base class initialization
		super(EquationEditorWidget, self).__init__(parent)
		
		mainLayout = QVBoxLayout()
		# Create the title for the widget
		self.setWindowTitle('Equation editor')
		if len(title) > 0:
			title = f'Equation editor for {title}'
		else:
			title = 'Equation editor'
		mainLayout.addWidget(QLabel(f'<html><head/><body><p align="center"><span style=" font-sice:11pt; color:#003399;">{title}</span></p></body></html>'))
		
		# Widget containing editor on the left, tree on the center and help on the right
		# Create a slider to select N for My-Mz plot
		editorWidget = QWidget()
		editorWidget.setLayout(QHBoxLayout())
		editorWidget.layout().setContentsMargins(0,0,0,0)
		
		# Editor single line
		self.textEdit = ASDTextEditSingleLine()
		
		# Tree
		self.tree = ASDTreeWidget()
		self.tree.setHeaderHidden(True)
		
		
		# Operators
		operators = {
			'+': ' + ',
			'-': ' - ',
			'*': ' * ',
			'/': ' / '
		}
		# Populate operators
		for key, expr in operators.items():
			self.tree.registerItem('Operators',key,expr,'')

		
		# Editor Help
		self.helpEdit = QTextEdit()
		self.helpEdit.setText(formatRecentExpressionHelp('"+"','eval[1 + 3]'))
		
		editorWidget.layout().addWidget(self.textEdit)
		editorWidget.layout().addWidget(self.tree)
		editorWidget.layout().addWidget(self.helpEdit)
		
		# Add it to the main widget
		mainLayout.addWidget(editorWidget)
		
		# # Buttons
		buttonBox = QDialogButtonBox(self)
		buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
		# self.btnClose = QPushButton('Close')
		# self.btnClose.setDefault(True)
		# self.btnClose.setFocus()
		
		mainLayout.addWidget(buttonBox)
		
		# Set the main widget layout
		self.setLayout(mainLayout)
		
		# connections
		buttonBox.accepted.connect(self.accept)
		buttonBox.rejected.connect(self.reject)
		

	def onCloseClicked(self):
		self.accept()
		
