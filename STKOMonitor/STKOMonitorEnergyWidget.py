"""
The Energy Balance tab: the balance file(s) the solver writes (opspro's Energy
Balance observer, ``energyBalance on -file <name>.ebal``), drawn the Perform3D
way while the analysis runs, and read from the start on a finished one.

  * top: the energy components stacked (the dissipation per group, damping,
    strain, kinetic, then the IMPL-EX error), with the input as a line over
    them: the gap
    between the line and the stack is the balance error. Negative changes
    (strain energy released by a state that unloads) stack below zero;
  * bottom left: the error in % of the largest input;
  * bottom right: the dissipation per group at the chosen instant.

A check box per stacked component (and one for the input line) hides it; the
components left close up, so one of them alone stands on zero.

The reading is energy_balance_data.py (a copy of opspro's, keep them equal).
The tab is added to the window only once a balance file shows up, so a run
without one looks the same as before.
"""
import os

from PySide2.QtCore import Qt, QTimer, Signal
from PySide2.QtGui import QColor, QIcon, QPixmap
from PySide2.QtWidgets import (
	QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QCheckBox, QLabel, QSlider,
	QSplitter, QFrame)

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from stko_theme import apply_mpl_theme, plot_colors
from energy_balance_data import (
	EnergyBalanceData, is_energy_balance_file, label_of, SIGNATURE, GROUP_PREFIX)
from STKOMonitorPlotWidget import plotDisplayName

# one colour per solver column, the groups from a categorical list in file
# order, Other always grey
_COLUMN_COLORS = {
	'Kinetic': '#4e79a7',
	'Strain': '#59a14f',
	'RayleighAlphaM': '#9c755f',
	'RayleighBetaK': '#c9b18a',
	'Modal': '#b07aa1',
	'Viscous': '#76b7b2',
	# the IMPL-EX energy error: a bright red that no group takes, it must
	# stand out
	'Implex': '#ff1a1a',
	# the hinges, the largest band of a frame, a violet of their own
	GROUP_PREFIX + 'Hinges': '#7b4fb0',
}
_GROUP_COLORS = (
	'#f28e2b', '#edc948', '#ff9da7', '#8cd17d', '#d37295',
	'#86bcb6', '#fabfd2', '#b6992d', '#499894')
_OTHER_COLOR = '#a0a0a0'


def _colors(columns):
	# only the groups draw from the categorical list: Time, Input, Dissipated
	# and Error are no band and must not use up its first colours
	out = {}
	k = 0
	for c in columns:
		if c in _COLUMN_COLORS:
			out[c] = _COLUMN_COLORS[c]
		elif c == GROUP_PREFIX + 'Other':
			out[c] = _OTHER_COLOR
		elif c.startswith(GROUP_PREFIX):
			out[c] = _GROUP_COLORS[k % len(_GROUP_COLORS)]
			k += 1
	return out


def _swatch(color):
	pix = QPixmap(12, 12)
	pix.fill(QColor(color))
	return QIcon(pix)


class STKOMonitorEnergyWidget(QWidget):

	# emitted with the number of balance files whenever it changes
	filesChanged = Signal(int)

	def __init__(self, parent=None):
		super(STKOMonitorEnergyWidget, self).__init__(parent)
		# path -> EnergyBalanceData
		self.data = {}
		# files already seen NOT to be balances (long enough to tell)
		self.not_balance = set()
		# the components the user unchecked, by column name ('Input' too): kept
		# across files and across the boxes being rebuilt
		self.hidden = set()
		# the columns the boxes were built for
		self.box_columns = None

		# canvas
		self.figure = Figure(figsize=(6, 5), dpi=100)
		self.canvas = FigureCanvas(self.figure)
		# the right margin holds the legend of the stacked plot
		grid = self.figure.add_gridspec(2, 2, height_ratios=(2.2, 1.0),
			hspace=0.45, wspace=0.35, left=0.08, right=0.80, top=0.95,
			bottom=0.09)
		self.ax_stack = self.figure.add_subplot(grid[0, :])
		self.ax_error = self.figure.add_subplot(grid[1, 0])
		self.ax_bars = self.figure.add_subplot(grid[1, 1])

		# controls
		self.combo = QComboBox()
		self.normalize = QCheckBox('Normalize to max |Input|')
		self.normalize.setChecked(True)
		self.slider = QSlider(Qt.Horizontal)
		self.slider.setMinimum(0)
		self.slider.setMaximum(0)
		self.time_label = QLabel()
		self.summary = QLabel()
		self.summary.setWordWrap(True)
		self.summary.setTextInteractionFlags(Qt.TextSelectableByMouse)
		self.boxes = QWidget()
		self.boxes.setLayout(QVBoxLayout())
		self.boxes.layout().setContentsMargins(0, 0, 0, 0)
		self.boxes.layout().setSpacing(2)

		left = QWidget()
		left.setLayout(QVBoxLayout())
		left.layout().addWidget(self.canvas)
		left.layout().addWidget(NavigationToolbar(self.canvas, self))
		right = QWidget()
		right.setLayout(QVBoxLayout())
		right.layout().addWidget(QLabel('Balance:'))
		right.layout().addWidget(self.combo)
		right.layout().addWidget(self.normalize)
		right.layout().addWidget(QLabel('Show:'))
		right.layout().addWidget(self.boxes)
		sep = QFrame()
		sep.setFrameShape(QFrame.HLine)
		sep.setFrameShadow(QFrame.Sunken)
		right.layout().addWidget(sep)
		right.layout().addWidget(QLabel('Dissipation at:'))
		right.layout().addWidget(self.slider)
		right.layout().addWidget(self.time_label)
		right.layout().addWidget(self.summary)
		right.layout().addStretch(1)
		splitter = QSplitter(Qt.Horizontal)
		splitter.addWidget(left)
		splitter.addWidget(right)
		splitter.setStretchFactor(0, 5)
		splitter.setStretchFactor(1, 1)
		self.setLayout(QHBoxLayout())
		self.layout().setContentsMargins(0, 0, 0, 0)
		self.layout().addWidget(splitter)

		# the slider follows the last row while it sits at the end
		self.follow = True
		self.combo.currentIndexChanged.connect(self.onCurrentChanged)
		self.normalize.toggled.connect(lambda _c: self.redraw())
		self.slider.valueChanged.connect(self.onSliderChanged)

		self.timer = QTimer(self)
		self.timer.setInterval(1000)
		self.timer.timeout.connect(self.findFiles)
		self.timer.timeout.connect(self.reload)
		self.timer.start()

	# ------------------------------------------------------------------
	# files
	# ------------------------------------------------------------------

	def findFiles(self):
		found = []
		for root, _dirs, files in os.walk(os.getcwd()):
			for name in files:
				path = os.path.join(root, name)
				if path in self.not_balance:
					continue
				if path in self.data:
					found.append(path)
					continue
				if is_energy_balance_file(path):
					found.append(path)
				else:
					try:
						# too short to tell yet: look again next time
						if os.path.getsize(path) >= len(SIGNATURE):
							self.not_balance.add(path)
					except OSError:
						pass
		changed = False
		for path in list(self.data):
			if path not in found:
				del self.data[path]
				i = self.combo.findData(path)
				if i >= 0:
					self.combo.removeItem(i)
				changed = True
		for path in sorted(found):
			if path not in self.data:
				self.data[path] = EnergyBalanceData(path)
				self.combo.addItem(plotDisplayName(path), path)
				changed = True
		if changed:
			self.filesChanged.emit(len(self.data))

	def current(self):
		return self.data.get(self.combo.currentData())

	def reload(self, force=False):
		data = self.current()
		if data is None:
			return
		try:
			added = data.load()
		except ValueError:
			# a header that is not a balance after all
			self.not_balance.add(data.path)
			return
		if added or force:
			n = data.rows()
			self.slider.blockSignals(True)
			self.slider.setMaximum(max(0, n - 1))
			if self.follow:
				self.slider.setValue(max(0, n - 1))
			self.slider.blockSignals(False)
			self.redraw()

	def onCurrentChanged(self, _index):
		self.follow = True
		self.reload(force=True)

	def onSliderChanged(self, value):
		self.follow = (value >= self.slider.maximum())
		self.redraw()

	# ------------------------------------------------------------------
	# component boxes
	# ------------------------------------------------------------------

	def syncBoxes(self, columns, palette, ink):
		# rebuilt only when the stacked columns change: a component that
		# was zero so far shows up while the analysis runs
		if self.box_columns == columns:
			return
		self.box_columns = columns
		layout = self.boxes.layout()
		while layout.count():
			w = layout.takeAt(0).widget()
			if w is not None:
				w.deleteLater()
		for c in columns:
			box = QCheckBox(label_of(c))
			box.setIcon(_swatch(ink if c == 'Input' else palette[c]))
			box.setChecked(c not in self.hidden)
			box.toggled.connect(lambda on, c=c: self.onBoxToggled(c, on))
			layout.addWidget(box)

	def onBoxToggled(self, column, on):
		if on:
			self.hidden.discard(column)
		else:
			self.hidden.add(column)
		self.redraw()

	# ------------------------------------------------------------------
	# drawing
	# ------------------------------------------------------------------

	def redraw(self):
		data = self.current()
		for ax in (self.ax_stack, self.ax_error, self.ax_bars):
			ax.clear()
		colors = plot_colors()
		if data is None or data.rows() == 0:
			self.time_label.setText('')
			self.summary.setText('')
			apply_mpl_theme(self.figure)
			self.canvas.draw()
			return
		norm = self.normalize.isChecked()
		t = data.time()
		k = min(self.slider.value(), data.rows() - 1)
		t_sel = t[k]
		palette = _colors(data.columns)
		stacked = data.stack_columns()
		self.syncBoxes(stacked + ['Input'], palette, colors['ink'])

		# stacked components + input
		ax = self.ax_stack
		shown = [c for c in stacked if c not in self.hidden]
		for c, lower, upper in data.stack(norm, shown):
			ax.fill_between(t, lower, upper, color=palette[c], linewidth=0.0,
				label=label_of(c))
		s = 1.0 / data.scale() if norm else 1.0
		if 'Input' not in self.hidden:
			ax.plot(t, [v * s for v in data.column('Input')],
				color=colors['ink'], linewidth=1.5, label='Input')
		ax.axhline(0.0, color=colors['axis'], linewidth=0.6)
		ax.axvline(t_sel, color=colors['accent'], linewidth=0.8, linestyle='--')
		ax.set_xlabel('Time')
		ax.set_ylabel('Energy / max|Input|' if norm else 'Energy')
		ax.grid(linestyle=':', color=colors['grid'])
		ax.legend(loc='upper left', bbox_to_anchor=(1.01, 1.0),
			fontsize='x-small', frameon=False)

		# error
		ax = self.ax_error
		ax.plot(t, data.error_percent(), color=colors['accent'], linewidth=1.2)
		ax.axhline(0.0, color=colors['axis'], linewidth=0.6)
		ax.axvline(t_sel, color=colors['accent'], linewidth=0.8, linestyle='--')
		ax.set_xlabel('Time')
		ax.set_ylabel('Error (% of max|Input|)')
		ax.grid(linestyle=':', color=colors['grid'])

		# dissipation per group at the chosen instant
		summary = data.summary(t_sel)
		ax = self.ax_bars
		groups = [g for g in summary['groups'] if g['value'] != 0.0]
		if groups:
			names = [g['group'] for g in groups]
			vals = [g['value'] * s for g in groups]
			bars = ax.barh(range(len(names)), vals,
				color=[palette[GROUP_PREFIX + n] for n in names])
			ax.set_yticks(range(len(names)))
			ax.set_yticklabels(names, fontsize='x-small')
			ax.invert_yaxis()
			for bar, g in zip(bars, groups):
				# a rounding-size negative share would print as -0.0 %
				share = 100.0 * g['share']
				if abs(share) < 0.05:
					share = 0.0
				ax.annotate('{:.1f} %'.format(share),
					(bar.get_width(), bar.get_y() + bar.get_height() / 2.0),
					xytext=(3, 0), textcoords='offset points', va='center',
					fontsize='x-small', color=colors['ink'])
			ax.margins(x=0.25)
		ax.set_xlabel('Dissipated / max|Input|' if norm else 'Dissipated')
		ax.set_title('Dissipation at t = {:g}'.format(t_sel), fontsize='x-small')
		ax.grid(axis='x', linestyle=':', color=colors['grid'])

		self.time_label.setText('t = {:g}  (step {} of {})'.format(
			t_sel, k + 1, data.rows()))
		cols = summary['columns']
		text = 'Input {:.4g}\nDissipated {:.4g}\nError {:.4g}\n'.format(
			cols.get('Input', 0.0), cols.get('Dissipated', 0.0),
			cols.get('Error', 0.0))
		if 'Implex' in cols:
			text += 'IMPL-EX error {:.4g}\n'.format(cols['Implex'])
		text += 'max |Error| = {:.3g} % of max |Input|'.format(
			summary['max_error_percent'])
		if 'Implex' in cols:
			text += '\nmax |IMPL-EX error| = {:.3g} %'.format(
				summary['max_implex_percent'])
		self.summary.setText(text)
		apply_mpl_theme(self.figure)
		self.canvas.draw()
