"""
STKOEdpMonitorPlotWidget
------------------------
The realtime EDP view of the STKO EDP Monitor. A ``QTimer`` (mirroring
STKOMonitorPlotWidget) re-reads the suite directory every poll, runs the pure
realtime classifier + aggregator over what is on disk so far, and repaints the
IDA/MSA curves, the collapse fragility and the per-level statistics live.

Data flow every tick (all pure, no STKO):
    read_edp_records(cwd) + load_manifest(cwd)         # nlth_edp_aggregate
      -> RealtimeState.update(...)                      # edp_realtime
         -> aggregate(finished_records, finished_manifest, edp, collapse_drift)
    then draw: the curves + fragility plots (stacked dock panels in a left
    column) and the levels table (dock spanning the full height on the
    right), with the still-running runs drawn as hollow provisional markers.

The module is flat-imported (``from nlth_edp_aggregate import ...``): the entry
point inserts the bundle directory on ``sys.path`` exactly like STKOMonitorMain.
"""
import colorsys
import os

from PySide2.QtCore import Qt, QTimer
from PySide2.QtGui import QColor, QDoubleValidator
from PySide2.QtWidgets import (
    QMainWindow, QDockWidget, QToolBar, QWidget, QVBoxLayout, QLabel, QComboBox,
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox,
    QProgressBar)

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from nlth_edp_aggregate import aggregate, read_edp_records, load_manifest
from edp_realtime import RealtimeState

_PARAMS = {
    "legend.fontsize": "x-small",
    "axes.labelsize": "small",
    "axes.titlesize": "small",
    "xtick.labelsize": "x-small",
    "ytick.labelsize": "x-small",
}

# stable-ish colors keyed by record id, so a record keeps its color as it grows.
def _record_color(rid, lightness=0.45, sat=0.65):
    if rid is None:
        rid = -1
    h = (0.61 + 0.23 * ((int(rid) * 2654435761) % 997) / 997.0) % 1.0
    return colorsys.hls_to_rgb(h, lightness, sat)


class _Canvas(FigureCanvas):
    """A one-axes matplotlib canvas that is fully re-drawn each tick (the plot
    structure changes as records appear, so incremental line updates as in
    STKOMonitor do not apply here)."""

    def __init__(self, parent=None):
        fig = Figure(figsize=(5, 4), dpi=100)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        plt.rcParams.update(_PARAMS)
        self.figure = fig
        self.ax = fig.add_subplot(111)
        self.ax.grid(linestyle=":")

    def clear(self):
        self.ax.clear()
        self.ax.grid(linestyle=":")


class STKOEdpMonitorPlotWidget(QMainWindow):
    """The realtime view, laid out as dockable panels: the two plots
    (IDA/MSA curves + collapse fragility) stacked in a left column, the
    per-level statistics table spanning the full height on the right (given
    more room). A ``QMainWindow`` (so it owns the dock areas) — embedded as
    the central widget of STKOEdpMonitorWindow; the shared controls live in a
    top toolbar, the live status in the status bar."""

    POLL_MS = 1500

    def __init__(self, parent=None):
        super(STKOEdpMonitorPlotWidget, self).__init__(parent)
        self._dir = os.getcwd()
        self._state = RealtimeState()
        self._known_edps = []          # accumulated union, for a stable combo
        self._last_agg = None

        self.setDockNestingEnabled(True)

        # --- control toolbar ----------------------------------------------- #
        tb = QToolBar("Controls")
        tb.setMovable(False)
        tb.setFloatable(False)
        self.addToolBar(Qt.TopToolBarArea, tb)

        tb.addWidget(QLabel(" EDP: "))
        self.edp_combo = QComboBox()
        self.edp_combo.setMinimumWidth(90)
        tb.addWidget(self.edp_combo)
        tb.addSeparator()

        tb.addWidget(QLabel(" Collapse limit: "))
        self.drift_edit = QLineEdit("0.10")
        v = QDoubleValidator(0.0, 1.0e9, 9, self.drift_edit)
        v.setNotation(QDoubleValidator.StandardNotation)
        self.drift_edit.setValidator(v)
        self.drift_edit.setMaximumWidth(80)
        self.drift_edit.setToolTip(
            "A run is 'collapsed' when it stopped early (non-convergence) OR the "
            "driving EDP reached this value.")
        tb.addWidget(self.drift_edit)
        tb.addSeparator()

        self.chk_spaghetti = QCheckBox("Records")
        self.chk_spaghetti.setChecked(True)
        self.chk_spaghetti.setToolTip("Show the per-record IDA curves / MSA points")
        tb.addWidget(self.chk_spaghetti)
        self.chk_live = QCheckBox("Running")
        self.chk_live.setChecked(True)
        self.chk_live.setToolTip("Show the still-running runs as hollow markers")
        tb.addWidget(self.chk_live)

        self.status = QLabel("waiting for runs...")
        self.statusBar().addWidget(self.status, 1)
        # suite progress = finished runs + the fractional progress of the
        # still-running ones (a smooth 0..100% bar, not a per-run jump).
        self.progress = QProgressBar()
        self.progress.setRange(0, 1000)
        self.progress.setValue(0)
        self.progress.setFixedWidth(220)
        self.progress.setFormat("waiting")
        self.statusBar().addPermanentWidget(self.progress)

        # No central widget: this QMainWindow is a pure dock container, so the
        # dock area fills the whole window down to the status bar. A dummy
        # central widget — even zero-height — leaves a phantom draggable
        # separator between the dock area and the (empty) centre, sitting just
        # above the status bar; dropping it removes that stray handle, so the
        # only separators left are the ones between the three docks.
        self.setCentralWidget(None)

        # --- dock panels --------------------------------------------------- #
        self.curve_canvas = _Canvas(self)
        curves_dock = self._make_plot_dock("IDA / MSA curves", self.curve_canvas)

        self.frag_canvas = _Canvas(self)
        frag_dock = self._make_plot_dock("Collapse fragility", self.frag_canvas)

        self.table = QTableWidget(0, 0)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        levels_dock = QDockWidget("Levels", self)
        levels_dock.setObjectName("levels_dock")
        levels_holder = QWidget()
        levels_holder.setObjectName("stkoDockBody")
        ll = QVBoxLayout(levels_holder)
        ll.setContentsMargins(4, 4, 4, 4)
        ll.addWidget(self.table)
        levels_dock.setWidget(levels_holder)

        # movable + floatable but NOT closable — there is no menu to bring a
        # closed panel back, so keep all three always present.
        feats = QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable
        for d in (curves_dock, frag_dock, levels_dock):
            d.setFeatures(feats)

        # one nested dock tree: IDA (top) + Fragility (bottom) stacked in a
        # left column of equal height, Levels spanning the full height on the
        # right with more room. The FIRST splitDockWidget call fixes the root
        # splitter's orientation for the whole dock area; splitting curves
        # against levels Horizontally first makes that the root (curves |
        # levels, both full height). Only THEN splitting curves against frag
        # Vertically nests a new sub-splitter inside curves' own cell,
        # stacking it with frag — levels is untouched by that, so it keeps
        # spanning the full height on the right.
        self.addDockWidget(Qt.TopDockWidgetArea, curves_dock)
        self.splitDockWidget(curves_dock, levels_dock, Qt.Horizontal)
        self.splitDockWidget(curves_dock, frag_dock, Qt.Vertical)
        self.resizeDocks([curves_dock, frag_dock], [1, 1], Qt.Vertical)
        self.resizeDocks([curves_dock, levels_dock], [40, 60], Qt.Horizontal)

        # --- reactions ----------------------------------------------------- #
        self.edp_combo.currentIndexChanged.connect(self._refresh_views)
        self.drift_edit.editingFinished.connect(self._refresh_views)
        self.chk_spaghetti.toggled.connect(self._refresh_views)
        self.chk_live.toggled.connect(self._refresh_views)

        # --- timer --------------------------------------------------------- #
        self.timer = QTimer(self)
        self.timer.setInterval(self.POLL_MS)
        self.timer.timeout.connect(self._poll)
        self.timer.start()
        self._poll()

    # ------------------------------------------------------------------ #
    # helpers
    # ------------------------------------------------------------------ #
    def _make_plot_dock(self, title, canvas):
        """A dock holding a matplotlib canvas + its navigation toolbar."""
        dock = QDockWidget(title, self)
        dock.setObjectName(title.replace(" ", "_"))
        holder = QWidget()
        holder.setObjectName("stkoDockBody")
        lay = QVBoxLayout(holder)
        lay.setContentsMargins(4, 4, 4, 4)
        lay.setSpacing(3)
        lay.addWidget(canvas, 1)
        lay.addWidget(NavigationToolbar(canvas, holder))
        dock.setWidget(holder)
        return dock

    def _selected_edp(self):
        return self.edp_combo.currentText() or (
            self._known_edps[0] if self._known_edps else "IDR")

    def _collapse_drift(self):
        try:
            return float(self.drift_edit.text().replace(",", "."))
        except ValueError:
            return 0.10

    def _sync_edp_combo(self, names):
        """Keep the combo in sync with every EDP name ever seen, preserving the
        current selection (names only ever grow, so the index is stable)."""
        added = [n for n in names if n not in self._known_edps]
        if not added:
            return
        self._known_edps.extend(added)
        self._known_edps.sort()
        cur = self.edp_combo.currentText()
        self.edp_combo.blockSignals(True)
        self.edp_combo.clear()
        self.edp_combo.addItems(self._known_edps)
        if cur in self._known_edps:
            self.edp_combo.setCurrentIndex(self._known_edps.index(cur))
        self.edp_combo.blockSignals(False)

    # ------------------------------------------------------------------ #
    # poll + draw
    # ------------------------------------------------------------------ #
    def _poll(self):
        manifest = load_manifest(self._dir)
        if not manifest:
            self.status.setText("waiting for runs.json in {}".format(self._dir))
            self.progress.setValue(0)
            self.progress.setFormat("waiting")
            return
        records = read_edp_records(self._dir)
        self._snap = self._state.update(records, manifest)

        # discover EDP names from finished + live records
        names = set()
        for rec in self._snap["finished_records"].values():
            names.update((rec.get("edps") or {}).keys())
        for lv in self._snap["live"]:
            names.update((lv.get("edps") or {}).keys())
        if names:
            self._sync_edp_combo(sorted(names))

        self._refresh_views()

    def _refresh_views(self):
        snap = getattr(self, "_snap", None)
        if snap is None:
            return
        edp = self._selected_edp()
        drift = self._collapse_drift()
        agg = aggregate(snap["finished_records"], snap["finished_manifest"],
                        edp=edp, collapse_drift=drift)
        self._last_agg = agg
        method = self._method(agg, snap)

        c = snap["counts"]
        n_col = sum(l["n_collapsed"] for l in agg["levels"])
        done = c["done_ok"] + c["done_collapse"]
        self.status.setText(
            "{}  |  EDP {}  |  done {} (+{} collapsed) | running {} | pending {} "
            "| total {}".format(
                method.upper(), edp, done, n_col,
                c["live"], c["pending"], c["total"]))

        # smooth suite progress: finished runs + the running ones' own progress
        total = c["total"]
        live_prog = sum(lv.get("progress", 0.0) for lv in snap["live"])
        frac = ((done + live_prog) / total) if total else 0.0
        self.progress.setValue(int(round(max(0.0, min(1.0, frac)) * 1000)))
        self.progress.setFormat("{}/{} runs  {:.0f}%".format(done, total, frac * 100))

        self._draw_curves(agg, snap, edp, method)
        self._draw_fragility(agg, method)
        self._fill_table(agg, edp)

    @staticmethod
    def _method(agg, snap):
        if agg["levels"]:
            return agg["method"]
        if snap["live"]:
            return snap["live"][0].get("method", "code")
        return "code"

    # ------------------------------------------------------------------ #
    # curves
    # ------------------------------------------------------------------ #
    def _draw_curves(self, agg, snap, edp, method):
        cv = self.curve_canvas
        cv.clear()
        ax = cv.ax
        show_rec = self.chk_spaghetti.isChecked()
        show_live = self.chk_live.isChecked()

        if method == "ida":
            ax.set_xlabel(edp)
            ax.set_ylabel("Intensity measure (IM)")
            ax.set_title("IDA curves — {}".format(edp))
            if show_rec and agg["curves"]:
                for cur in agg["curves"]:
                    xs, ys = [], []
                    for p in cur["points"]:
                        val = p.get(edp)
                        if val is not None:
                            xs.append(val)
                            ys.append(p["im"])
                    if xs:
                        col = _record_color(cur["record_id"])
                        ax.plot(xs, ys, "-o", color=col, lw=1.0, ms=3,
                                alpha=0.7)
                    if cur["collapse_im"] is not None and xs:
                        ax.plot([xs[-1]], [cur["collapse_im"]], "x",
                                color="crimson", ms=8, mew=1.5)
            self._plot_fractiles(ax, agg, edp)
            if show_live:
                self._plot_live(ax, snap, edp)

        elif method == "msa":
            ax.set_xlabel(edp)
            ax.set_ylabel("Intensity measure (stripe IM)")
            ax.set_title("MSA stripes — {}".format(edp))
            for lv in agg["levels"]:
                st = lv["edp_stats"].get(edp)
                im = lv["im"]
                if show_rec:
                    # individual finished runs of this stripe
                    xs = [r["edps"][edp] for r in self._runs_at(snap, im)
                          if edp in r["edps"]]
                    ax.plot(xs, [im] * len(xs), "o", color="0.6", ms=3,
                            alpha=0.6, zorder=1)
                if st:
                    ax.plot([st["p16"], st["p84"]], [im, im], "-",
                            color="steelblue", lw=1.5, zorder=2)
                    ax.plot([st["p50"]], [im], "D", color="navy", ms=5, zorder=3)
            if show_live:
                self._plot_live(ax, snap, edp)

        else:  # code
            ax.set_xlabel("record")
            ax.set_ylabel(edp)
            ax.set_title("Record set — {}".format(edp))
            lv = agg["levels"][0] if agg["levels"] else None
            vals = []
            if lv is not None:
                for r in self._runs_at(snap, lv["im"]):
                    if edp in r["edps"]:
                        vals.append(r["edps"][edp])
            if show_rec and vals:
                ax.plot(range(1, len(vals) + 1), vals, "o", color="steelblue",
                        ms=4)
            if lv is not None:
                st = lv["edp_stats"].get(edp)
                if st:
                    ax.axhline(st["p50"], color="navy", lw=1.5, label="median")
                    ax.axhline(st["p16"], color="gray", lw=1.0, ls="--",
                               label="16-84%")
                    ax.axhline(st["p84"], color="gray", lw=1.0, ls="--")
            if show_live:
                # live code runs: draw at the far right as hollow markers
                live_vals = [lvd["edps"][edp] for lvd in snap["live"]
                             if edp in lvd["edps"]]
                if live_vals:
                    x0 = len(vals) + 1
                    ax.plot(range(x0, x0 + len(live_vals)), live_vals, "o",
                            mfc="none", mec="0.5", ms=5, label="running")
            ax.legend(loc="best")

        ax.relim()
        ax.autoscale_view()
        cv.draw()

    def _plot_fractiles(self, ax, agg, edp):
        pts = [(lv["edp_stats"][edp], lv["im"]) for lv in agg["levels"]
               if edp in lv["edp_stats"]]
        if len(pts) < 1:
            return
        pts.sort(key=lambda t: t[1])
        ims = [im for _s, im in pts]
        ax.plot([s["p50"] for s, _ in pts], ims, "-", color="black", lw=2.0,
                label="median", zorder=5)
        ax.plot([s["p16"] for s, _ in pts], ims, "--", color="black", lw=1.0,
                label="16-84%", zorder=5)
        ax.plot([s["p84"] for s, _ in pts], ims, "--", color="black", lw=1.0,
                zorder=5)
        ax.legend(loc="lower right")

    def _plot_live(self, ax, snap, edp):
        xs, ys = [], []
        for lv in snap["live"]:
            val = lv["edps"].get(edp)
            if val is not None:
                xs.append(val)
                ys.append(lv["im"])
        if xs:
            ax.plot(xs, ys, "o", mfc="none", mec="0.5", ms=5, alpha=0.8,
                    label="running", zorder=4)
            ax.legend(loc="lower right")

    @staticmethod
    def _runs_at(snap, im):
        """Finished runs (records) at intensity *im* — reconstructed from the
        finished set for per-record scatter (aggregate keeps only stats)."""
        out = []
        for sub, rec in snap["finished_records"].items():
            meta = snap["finished_manifest"].get(sub, {})
            if abs(float(meta.get("im", 1.0) or 1.0) - im) < 1e-9:
                out.append({"edps": rec.get("edps", {}) or {}})
        return out

    # ------------------------------------------------------------------ #
    # fragility
    # ------------------------------------------------------------------ #
    def _draw_fragility(self, agg, method):
        cv = self.frag_canvas
        cv.clear()
        ax = cv.ax
        ax.set_xlabel("Intensity measure (IM)")
        ax.set_ylabel("P(collapse)")
        ax.set_ylim(-0.02, 1.02)

        if method not in ("ida", "msa"):
            ax.set_title("Fragility — available for IDA / MSA only")
            cv.draw()
            return

        # empirical collapse fractions per level
        if agg["levels"]:
            ims = [lv["im"] for lv in agg["levels"]]
            fr = [lv["collapse_fraction"] for lv in agg["levels"]]
            ns = [lv["n"] for lv in agg["levels"]]
            ax.scatter(ims, fr, s=[20 + 10 * n for n in ns], color="crimson",
                       zorder=3, label="observed")

        frag = agg["fragility"]
        if frag:
            ax.plot(frag["im"], frag["p_collapse"], "-", color="navy", lw=2.0,
                    label="lognormal fit")
            ax.set_title(u"Collapse fragility — θ={:.3g}, β={:.3g}"
                         .format(frag["theta"], frag["beta"]))
        else:
            msg = "no fragility yet"
            for w in agg["warnings"]:
                if "collaps" in w or "fragility" in w:
                    msg = w
                    break
            ax.set_title("Fragility — {}".format(msg))
        ax.legend(loc="best")
        cv.draw()

    # ------------------------------------------------------------------ #
    # levels table
    # ------------------------------------------------------------------ #
    def _fill_table(self, agg, edp):
        cols = ["IM", "n", "collapsed", "coll.frac",
                "{} mean".format(edp), "{} median".format(edp),
                "{} 16%".format(edp), "{} 84%".format(edp), "{} max".format(edp)]
        self.table.setColumnCount(len(cols))
        self.table.setHorizontalHeaderLabels(cols)
        self.table.setRowCount(len(agg["levels"]))
        for r, lv in enumerate(agg["levels"]):
            st = lv["edp_stats"].get(edp)

            def cell(c, text, warn=False):
                it = QTableWidgetItem(text)
                it.setTextAlignment(Qt.AlignCenter)
                if warn:
                    it.setForeground(QColor("crimson"))
                self.table.setItem(r, c, it)

            cell(0, "{:g}".format(lv["im"]))
            cell(1, str(lv["n"]))
            cell(2, str(lv["n_collapsed"]), warn=lv["n_collapsed"] > 0)
            cell(3, "{:.0%}".format(lv["collapse_fraction"]),
                 warn=lv["collapse_fraction"] > 0)
            if st:
                cell(4, "{:.4g}".format(st["mean"]))
                cell(5, "{:.4g}".format(st["p50"]))
                cell(6, "{:.4g}".format(st["p16"]))
                cell(7, "{:.4g}".format(st["p84"]))
                cell(8, "{:.4g}".format(st["max"]))
            else:
                for c in range(4, 9):
                    cell(c, "-")
