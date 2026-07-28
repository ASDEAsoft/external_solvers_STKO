"""Main window of the STKO EDP Monitor — a thin shell around the realtime plot
widget (mirrors STKOMonitorWindow). The plot widget is itself a QMainWindow
(it owns the dock areas); a QMainWindow's dock areas hug the frame, so it is
wrapped in a container whose layout margins give the breathing space around the
whole dock region."""
import os

from PySide2.QtWidgets import QMainWindow, QWidget, QVBoxLayout

from STKOEdpMonitorPlotWidget import STKOEdpMonitorPlotWidget


class STKOEdpMonitorWindow(QMainWindow):

    def __init__(self, parent=None):
        super(STKOEdpMonitorWindow, self).__init__(parent)
        self.setWindowTitle("STKO EDP Monitor - {}".format(os.getcwd()))

        container = QWidget()
        lay = QVBoxLayout(container)
        lay.setContentsMargins(6, 6, 6, 6)
        self.plot = STKOEdpMonitorPlotWidget()
        lay.addWidget(self.plot)
        self.setCentralWidget(container)

        self.resize(1000, 760)
