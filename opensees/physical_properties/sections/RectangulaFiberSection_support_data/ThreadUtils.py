from PySide2.QtCore import Qt, QObject, Signal, Slot, QThread, QEventLoop, QTimer
from PySide2.QtWidgets import QMessageBox, QApplication, QDialog, QLabel, QProgressBar, QVBoxLayout, QTextEdit

'''
A simple QObject that wraps a user-defined function,
and calls this function waiting for it to finish
'''
class QBlockingSlot(QObject):
	requestCall = Signal()
	done = Signal()
	def __init__(self, function, parent = None):
		super(QBlockingSlot, self).__init__(parent)
		self.requestCall.connect(self.run)
		self.function = function
	def run(self):
		self.function()
		self.done.emit()
	def call(self):
		loop = QEventLoop()
		self.done.connect(loop.quit)
		self.requestCall.emit()
		loop.exec_()

'''
Utility to run a function with a QBlockingSlot on the GUI thread
'''
def runOnMainThread(function):
	bslot = QBlockingSlot(function)
	bslot.moveToThread(QApplication.instance().thread())
	bslot.call()

'''
A simple worker dialog, with a progres bar to track
the percentage of an operation
'''
class WorkerDialog(QDialog):
	def __init__(self, parent = None):
		# call base class constructor
		super(WorkerDialog, self).__init__(parent)
		# set up this dialog with the progress bar
		self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
		self.setAttribute(Qt.WA_DeleteOnClose)
		self.setLayout(QVBoxLayout())
		self.layout().addWidget(QLabel("Work in progres. Please wait"))
		self.pbar = QProgressBar()
		self.pbar.setRange(1, 100)
		self.pbar.setTextVisible(True)
		self.layout().addWidget(self.pbar)
		self.tedit = QTextEdit()
		self.layout().addWidget(self.tedit)
		# add a timer for a delayed opacity
		self.setWindowOpacity(0.0)
		self.delay = 0.0
		self.timer = QTimer(self)
		self.timer.setInterval(25)
		self.timer.timeout.connect(self.onTimerTimeOut)
		
	def showEvent(self, event):
		# call the base class method
		super(WorkerDialog, self).showEvent(event)
		self.timer.start()
	def reject(self):
		# we don't want this dialog to close if the user
		# presses the X button or the Escape key
		pass
	
	@Slot(str)
	def addTextLine(self, text):
		self.console_text_edit.append(text)
	
	@Slot()
	def clearTextEdit(self):
		self.console_text_edit.clear()
	
	@Slot(int)
	def setPercentage(self, value):
		self.pbar.setValue(value)
	@Slot()
	def onTimerTimeOut(self):
		if self.delay < 1.0:
			self.delay += 0.05
		else:
			self.setWindowOpacity(self.windowOpacity() + 0.05)
			if self.windowOpacity() == 1.0:
				self.timer.stop()
				self.timer.timeout.disconnect(self.onTimerTimeOut)

'''
Runs worker (instance of a class derived from Worker)
on a working thread using the provided dialog. The dialog
should have the sendPercentage(int) signal defined and should
derive from QDialog
'''
def runOnWorkerThread(worker, dialog = None):
	# TODO_DEBUG_FIX
	if dialog is None:
		dialog = WorkerDialog()
	# initial checks
	if not isinstance(worker, QObject):
		raise Exception('the worker object should inherit from QObject')
	if not hasattr(worker, 'finished'):
		raise Exception('the worker object should have the finished() signal')
	if not hasattr(worker, 'sendPercentage'):
		raise Exception('the worker object should have the sendPercentage(int) signal')
	if not hasattr(worker, 'sendTextLine'):
		raise Exception('the worker object should have the sendTextLine(str) signal')
	if not hasattr(worker, 'clearTextEdit'):
		raise Exception('the worker object should have the clearTextEdit() signal')
	if not isinstance(dialog, QDialog):
		raise Exception('the dialog object should inherit from QDialog')
	if not hasattr(dialog, 'setPercentage'):
		raise Exception('the dialog object should have a method called setPercentage(int)')
	if not callable(dialog.setPercentage):
		raise Exception('the dialog object setPercentage attribute is not a callable')
		
	# create the thread, the worker, and move the worker to the thread
	thread = QThread()
	worker.moveToThread(thread)
	
	# set up worker and thread connections
	worker.finished.connect(thread.quit)
	worker.finished.connect(worker.deleteLater)
	thread.started.connect(worker.run)
	thread.finished.connect(thread.deleteLater)
	worker.sendPercentage.connect(dialog.setPercentage)
	thread.finished.connect(dialog.accept)
	worker.sendTextLine.connect(dialog.addTextLine)
	worker.clearTextEdit.connect(dialog.clearTextEdit)
	
	# start the thread
	thread.start()
	
	# run dialog event loop
	dialog.exec_()