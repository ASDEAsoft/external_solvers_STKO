from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt
from math import floor

import traceback
import PyMpc
import PyMpc.App

class SectionsNavigator(QtWidgets.QWidget):
	
	_debug = False
	
	def __init__(self, n_secs = 5, currSec = 0, col = 'gray', selelectedCol = '#003399', radius = 4.0, selectedRaius = 5.0, padding = 4.0, labels = None, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.setSizePolicy(
			QtWidgets.QSizePolicy.MinimumExpanding,
			QtWidgets.QSizePolicy.MinimumExpanding
		)

		# Number of sections to show
		if isinstance(n_secs, int):
			self.n_sections = n_secs
		else:
			raise TypeError('number of sections must be a int')

		self._color = col
		self._selectedColor =  selelectedCol
		self._circle_radius = radius
		self._selected_radius = selectedRaius
		self._padding = padding  # n-pixel gap around edge.
		self._currentSection = currSec
		self._lblHeight = 10
		if labels is not None:
			self._n_lines = len(labels)
			self._labels = labels
		else:
			self._n_lines = 0
			self._labels = []
			
		self._circlesSections = []
		

	def paintEvent(self, e):
		try:
			painter = QtGui.QPainter(self)

			brush = QtGui.QBrush()
			brush.setColor('white')
			brush.setStyle(Qt.SolidPattern)
			pen = QtGui.QPen()
			# rect = QtCore.QRect(0, 0, painter.device().width(), painter.device().height())
			# painter.fillRect(rect, brush)

			# Define the canvas.
			# painter.drawRect(0,0,painter.device().width()-1,painter.device().height()-1)
			# painter.drawRect(self._padding,self._padding,painter.device().width()-2*self._padding,painter.device().height()-2*self._padding)
			# for i in range(self._n_lines):
				# painter.drawRect(self._padding, self._padding + i * self._lblHeight,painter.device().width()-2*self._padding,self._lblHeight)
			# print('height: {}'.format(painter.device().height()))
			# y of the line and center of the circles
			yCenter = painter.device().height() - self._padding - (painter.device().height() - self._n_lines * self._lblHeight - 2 * self._padding) / 2.0
			# print('y line: {}'.format(yCenter))
			
			# Width of plot
			d_width = painter.device().width() - (self._circle_radius * 2) - (self._padding * 2)
			x_start = self._padding + self._circle_radius
			if self._n_lines > 0:
				d_width -= 30
				x_start += 30
			
			# Draw the circles
			step_size = (d_width - self._circle_radius) / (self.n_sections - 1)

			# n_steps_to_draw = int(pc * self.n_steps)
			brush.setColor(QtGui.QColor(self._color))
			painter.setBrush(brush)
			painter.drawLine(x_start, yCenter, x_start + d_width - self._circle_radius, yCenter) 
			pen.setStyle(Qt.SolidLine)
			painter.setPen(pen)
			#reset the list of circle sections
			self._circlesSections.clear()
			r = self._circle_radius
			for i in range(self.n_sections):
				if (i == self._currentSection) or (self._currentSection == -1):
					brush.setColor(QtGui.QColor(self._selectedColor))
					painter.setBrush(brush)
					r = self._selected_radius
				xCenter = x_start + ((i) * step_size)
				self._circlesSections.append(QtCore.QRect(QtCore.QPoint(xCenter - r, yCenter-r),QtCore.QSize(2*r,2*r)))
				painter.drawEllipse(self._circlesSections[-1])
				# painter.drawText()
				if (i == self._currentSection) or (self._currentSection == -1):
					brush.setColor(QtGui.QColor(self._color))
					painter.setBrush(brush)
					r = self._circle_radius
			yText = self._padding + (self._n_lines - 1) * self._lblHeight + self._lblHeight
			if SectionsNavigator._debug:
				print('sectionsNavigator::paintEvent\t\t\t->\tLabels to show: {} - current Section {} - number of sections {}'.format(self._labels,self._currentSection,self.n_sections))
			for il, lbl in enumerate(self._labels):
				# print(il, lbl)
				yText -= self._lblHeight
				# print('label line {} - y label: {}'.format(il,yText))
				if lbl[0]:
					font = painter.font()
					font.setPixelSize(9);
					font.setBold(False)
					painter.setFont(font);
					# show the label
					painter.drawText(QtCore.QRect(self._padding, yText, 30, self._lblHeight), Qt.AlignLeft | Qt.AlignVCenter, lbl[1])
					
					for i, sec in enumerate(lbl[2]):
						# print(i, sec)
						if i >= self.n_sections:
							break
						if (i == self._currentSection) or (self._currentSection == -1):
							font.setBold(True)
						else:
							font.setBold(False)
						painter.setFont(font);
						sec[2].setRect(self._circlesSections[i].x()-self._circlesSections[i].width()/2.0,yText,self._circlesSections[i].width()*2,self._lblHeight)
						painter.drawText(sec[2],Qt.AlignCenter, sec[0])
			painter.end()
		except:
			exdata = traceback.format_exc().splitlines()
			PyMpc.IO.write_cerr('Error:\n{}\n'.format('\n'.join(exdata)))
		
	def event(self,evt):
		if type(evt) is QtGui.QHelpEvent:
			idx = -1
			for index, c in enumerate(self._circlesSections):
				if c.contains(evt.pos()):
					font = QtGui.QFont()
					suffix = ''
					if index == self._currentSection:
						font.setBold(True)
						suffix = ' (selected)'
					QtWidgets.QToolTip.setFont(font)
					QtWidgets.QToolTip.showText(evt.globalPos(),"Section {}{}".format(index, suffix),self)
					return True
			if SectionsNavigator._debug:
				print('sectionsNavigator::paintEvent\t\t\t->\tlines to check: {}'.format(self._n_lines))
			for i_lbl, lbl in enumerate(self._labels):
				if SectionsNavigator._debug:
					print('Checking line {}'.format(lbl[1]))
				for i_sec, sec in enumerate(lbl[2]):
					if sec[2].contains(evt.pos()):
						# Trovato
						font = QtGui.QFont()
						suffix = ''
						if (i_sec == self._currentSection):
							font.setBold(True)
							suffix = ' (selected)'
						QtWidgets.QToolTip.setFont(font)
						QtWidgets.QToolTip.showText(evt.globalPos(),"{}({}):  {}{}".format(lbl[1], i_sec, sec[1], suffix),self)
						return True
		QtWidgets.QToolTip.hideText()	
		return super(SectionsNavigator,self).event(evt)

	def sizeHint(self):
		if SectionsNavigator._debug:
			print('sectionsNavigator::sizeHint\t\t\t->\tlines to plot: {}'.format(self._n_lines))
		if self._n_lines == 0:
			if SectionsNavigator._debug:
				print("     {} x {}".format(150,4*self._circle_radius+2*self._padding))
			return QtCore.QSize(150, 4*self._circle_radius+2*self._padding)
		else:
			if SectionsNavigator._debug:
				print("     {} x {}".format(150,4*self._circle_radius + 2*self._padding + self._lblHeight *self._n_lines))
			return QtCore.QSize(150, 4*self._circle_radius + 2*self._padding + self._lblHeight *self._n_lines)
			
	def minimalSizeHint(self):
		return self.sizeHint()
		
	def setCurrentSection(self,i):
		self._currentSection = i
		self.update()
		
	def setNumberOfSections(self,n_secs,currSec = 0):
		self.n_sections = n_secs
		self._currentSection = currSec
		self.update()
		
	def setColor(self, color):
		self._color = color
		self.update()
		
	def setSelectedColor(self, color):
		self._selectedColor = color
		self.update()

	def setCircleRadius(self, r):
		self._circle_radius = r
		self.update()
		
	def setSelectedCircleRadius(self, r):
		self._selected_radius = r
		self.update()
		
	def setPadding(self, p):
		self._padding = p
		self.update()
		
	def getCurrentSection(self):
		return self._currentSection
		
	def resetLabels(self):
		self._labels.clear()
		self._n_lines = 0
		self.update()
	
	def addLabels(self, description, indexes, tooltips, show = True):
		try:
			if SectionsNavigator._debug:
				print('sectionsNavigator::addLabels     {}'.format(self._n_lines))
				print('sectionsNavigator::addLabels     {}'.format(self._labels))
			secs = []
			for i, tt in zip(indexes, tooltips):
				secs.append([i,tt,QtCore.QRect()])
			self._labels.append([show, description, secs])
			if show:
				self._n_lines += 1
			if SectionsNavigator._debug:
				print('sectionsNavigator::addLabels     {}'.format(self._n_lines))
				print('sectionsNavigator::addLabels     {}'.format(self._labels))
			
			self.update()
		except:
			exdata = traceback.format_exc().splitlines()
			PyMpc.IO.write_cerr('sectionsNavigator::addLabels     Error:\n{}\n'.format('\n'.join(exdata)))