"""
energy_balance_data.py
----------------------
The reader of the energy balance file the solver writes (the OpenSees
``energyBalance on -file <f>`` command), PURE: no Qt, no PyMpc, no numpy.

TWO COPIES, KEEP THEM IDENTICAL: the canonical one is
``opspro/Outputs/energy_balance_data.py``, used by the ``energy_balance_report``
command; the other ships on disk with the STKOMonitor app
(``STKO/external_solvers/STKOMonitor/energy_balance_data.py``), which runs in its
own Python process and cannot import opspro. The selftest compares them when
both checkouts are side by side.

The file
--------
A CSV with a header row: ``Time, Input, Kinetic, Strain, RayleighAlphaM,
RayleighBetaK, Modal, Viscous, Implex, Dissipated, Error``, then one
``Dissipated:<group>`` column per group the writer declared and
``Dissipated:Other`` last. Every value is CUMULATED from the moment the balance
was switched on, so Kinetic and Strain are CHANGES since then and may be
negative (a balance started after gravity sees the strain energy of the
gravity state drop), and so may the dissipation of the first steps, by a
rounding amount. ``Error = Input - (all the others)``.

``Implex`` is the energy error of IMPL-EX, signed: the elements do work with
the extrapolated forces each step delivers, the materials commit their
implicit state, and the difference is kept apart from the dissipation. Zero
without IMPL-EX; absent from the files of solvers older than it, which read
the same with the column missing.

opspro names it ``<name>.ebal`` (the monitors have ``.plt``), but the user may
pick any extension: a file is a balance when its first line starts with the
three columns every balance begins with (:data:`SIGNATURE`).

The solver flushes a row per converged step while the analysis runs, so the
last line may be half written: :meth:`EnergyBalanceData.load` reads only
complete lines and resumes from where it stopped.
"""
import os

EXTENSION = '.ebal'

SIGNATURE = 'Time,Input,Kinetic'

# The stacked bands, bottom to top: the dissipation groups first, so that
# their sum stands on zero and never decreases; then the damping, then the
# recoverable state, whose swings ride on top of what is spent for good.
DAMPING_COLUMNS = ('RayleighAlphaM', 'RayleighBetaK', 'Modal', 'Viscous')
STATE_COLUMNS = ('Strain', 'Kinetic')
# At the top of the stack: the numerical error of the integration that is not
# Error, so that what is left up to the Input line is.
NUMERICAL_COLUMNS = ('Implex',)

GROUP_PREFIX = 'Dissipated:'

# Files never opened to look for the signature: the results databases are
# large, and none of these can be a balance.
_SKIP_EXTENSIONS = frozenset((
    '.mpco', '.cdata', '.h5', '.hdf5', '.plt', '.pltbg', '.stats', '.tim',
    '.tcl', '.py', '.pyc', '.bat', '.sh', '.exe', '.dll', '.log', '.json',
    '.edp', '.scd', '.cae', '.png', '.jpg', '.pdf', '.zip',
))

# Display names of the solver's columns.
LABELS = {
    'Input': 'Input',
    'Kinetic': 'Kinetic',
    'Strain': 'Strain',
    'RayleighAlphaM': 'Rayleigh αM',
    'RayleighBetaK': 'Rayleigh βK',
    'Modal': 'Modal damping',
    'Viscous': 'Viscous',
    'Implex': 'IMPL-EX error',
    'Dissipated': 'Dissipated',
    'Error': 'Error',
}


def file_name_for(name, default='STKO_energy_balance'):
    """The file the solver writes for the user's *name* (empty = *default*):
    :data:`EXTENSION` is added unless the name carries an extension of its
    own, in which case the file is told by its header."""
    name = (name or '').strip() or default
    if not os.path.splitext(name)[1]:
        name += EXTENSION
    return name


def label_of(column):
    """The display name of *column*: a group column shows its group name."""
    if column.startswith(GROUP_PREFIX):
        return column[len(GROUP_PREFIX):]
    return LABELS.get(column, column)


def is_energy_balance_file(path):
    """True if *path* is an energy balance file: a ``.ebal``, or any other
    text file whose first line starts with :data:`SIGNATURE`."""
    ext = os.path.splitext(path)[1].lower()
    if ext == EXTENSION:
        return True
    if ext in _SKIP_EXTENSIONS:
        return False
    try:
        with open(path, 'rb') as f:
            head = f.read(len(SIGNATURE))
    except OSError:
        return False
    return head == SIGNATURE.encode('ascii')


def find_files(root, recursive=True):
    """The energy balance files under *root*, sorted. Recursive by default,
    like the monitor's own ``.plt`` scan: a suite keeps one run per
    sub-directory."""
    out = []
    if not os.path.isdir(root):
        return out
    if recursive:
        for base, _dirs, files in os.walk(root):
            for name in files:
                p = os.path.join(base, name)
                if is_energy_balance_file(p):
                    out.append(p)
    else:
        for name in os.listdir(root):
            p = os.path.join(root, name)
            if os.path.isfile(p) and is_energy_balance_file(p):
                out.append(p)
    return sorted(out)


class EnergyBalanceData:
    """The columns of one balance file, read incrementally.

    ``columns`` is the header (``Time`` first); ``values[name]`` the list of
    that column's values, one per complete row read so far."""

    def __init__(self, path):
        self.path = path
        self.columns = []
        self.values = {}
        self._offset = 0     # bytes consumed: the end of the last complete line

    # ------------------------------------------------------------------
    # reading
    # ------------------------------------------------------------------

    def reset(self):
        self.columns = []
        self.values = {}
        self._offset = 0

    def load(self):
        """Read the complete lines added since the last call. Returns the
        number of rows added. A file that got SHORTER was rewritten (a new
        run): it is read again from the start. Raises ValueError on a file
        whose header is not a balance's."""
        try:
            size = os.path.getsize(self.path)
        except OSError:
            return 0
        if size < self._offset:
            self.reset()
        if size == self._offset:
            return 0
        with open(self.path, 'rb') as f:
            f.seek(self._offset)
            chunk = f.read(size - self._offset)
        end = chunk.rfind(b'\n')
        if end < 0:
            return 0     # not even one complete line yet
        self._offset += end + 1
        added = 0
        for raw in chunk[:end].split(b'\n'):
            line = raw.decode('ascii', 'replace').strip()
            if not line:
                continue
            if not self.columns:
                cols = [c.strip() for c in line.split(',')]
                if ','.join(cols[:3]) != SIGNATURE:
                    self.reset()
                    raise ValueError(
                        "'{}' is not an energy balance file: its header does "
                        "not start with {}".format(self.path, SIGNATURE))
                self.columns = cols
                self.values = {c: [] for c in cols}
                continue
            fields = line.split(',')
            if len(fields) != len(self.columns):
                continue     # a malformed row: skipped, not fatal
            try:
                row = [float(x) for x in fields]
            except ValueError:
                continue
            for c, v in zip(self.columns, row):
                self.values[c].append(v)
            added += 1
        return added

    # ------------------------------------------------------------------
    # queries
    # ------------------------------------------------------------------

    def rows(self):
        return len(self.values.get('Time', ()))

    def time(self):
        return self.values.get('Time', [])

    def column(self, name):
        return self.values.get(name, [])

    def groups(self):
        """The ``Dissipated:<group>`` columns, in file order (``Other`` is
        the solver's last)."""
        return [c for c in self.columns if c.startswith(GROUP_PREFIX)]

    def is_zero(self, name, tol=0.0):
        """True if *name* is absent or never leaves ``[-tol, tol]``."""
        return all(abs(v) <= tol for v in self.column(name))

    def max_abs_input(self):
        return max((abs(v) for v in self.column('Input')), default=0.0)

    def scale(self):
        """The normalisation of every column: the largest |Input| so far
        (1 while there is no input yet)."""
        m = self.max_abs_input()
        return m if m > 0.0 else 1.0

    def error_percent(self):
        """The Error column in % of the largest |Input| so far."""
        s = 100.0 / self.scale()
        return [v * s for v in self.column('Error')]

    def index_at(self, t):
        """The index of the last row at or before time *t* (0 if *t* is
        before the first, the last row if after the last)."""
        ts = self.time()
        if not ts:
            return -1
        lo, hi = 0, len(ts) - 1
        if t >= ts[hi]:
            return hi
        if t <= ts[0]:
            return 0
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if ts[mid] <= t:
                lo = mid
            else:
                hi = mid
        return lo

    def at(self, t=None):
        """``{column: value}`` at time *t*, linearly interpolated between the
        two rows around it; *t* None = the last row. Empty with no rows."""
        ts = self.time()
        if not ts:
            return {}
        if t is None or t >= ts[-1]:
            return {c: self.values[c][-1] for c in self.columns}
        i = self.index_at(t)
        if t <= ts[0] or i == len(ts) - 1:
            return {c: self.values[c][i] for c in self.columns}
        t0, t1 = ts[i], ts[i + 1]
        w = (t - t0) / (t1 - t0) if t1 > t0 else 0.0
        out = {c: self.values[c][i] * (1.0 - w) + self.values[c][i + 1] * w
               for c in self.columns}
        out['Time'] = t
        return out

    def stack_columns(self):
        """The columns the stacked area shows, bottom to top: the dissipation
        per group, damping, strain, kinetic, then the IMPL-EX error. A column
        that is zero everywhere is left out (no modal damping, no viscous
        mechanism, no IMPL-EX...)."""
        cols = [c for c in self.groups() if not self.is_zero(c)]
        cols += [c for c in DAMPING_COLUMNS + STATE_COLUMNS + NUMERICAL_COLUMNS
                 if c in self.values and not self.is_zero(c)]
        return cols

    def stack(self, normalize=False, columns=None):
        """The bands of the stacked area: ``[(column, lower, upper)]``, bottom
        to top. The POSITIVE parts stack upwards from zero and the NEGATIVE
        parts downwards, each column in the same order, so a negative change
        (the strain energy of a state that unloads) never eats into the band
        of another. Divided by :meth:`scale` when *normalize*. *columns*
        limits the bands to those, still in the stack's order: the others are
        left out and the shown ones close up."""
        s = 1.0 / self.scale() if normalize else 1.0
        n = self.rows()
        up = [0.0] * n
        down = [0.0] * n
        out = []
        shown = self.stack_columns()
        if columns is not None:
            keep = set(columns)
            shown = [c for c in shown if c in keep]
        for c in shown:
            vals = self.values[c]
            lower = [0.0] * n
            upper = [0.0] * n
            for k in range(n):
                v = vals[k] * s
                if v >= 0.0:
                    lower[k] = up[k]
                    up[k] += v
                    upper[k] = up[k]
                else:
                    upper[k] = down[k]
                    down[k] += v
                    lower[k] = down[k]
            out.append((c, lower, upper))
        return out

    def summary(self, t=None):
        """What a report states at time *t* (None = the last row): every
        column, the dissipation per group with its share of the total, and
        the largest |Error| and |Implex| in % of the largest |Input| up to
        then (Implex 0 for a file without the column)."""
        vals = self.at(t)
        if not vals:
            return {'rows': 0}
        t_used = vals['Time']
        last = self.index_at(t_used)
        inp = max((abs(v) for v in self.column('Input')[:last + 1]),
                  default=0.0)
        err = max((abs(v) for v in self.column('Error')[:last + 1]),
                  default=0.0)
        implex = max((abs(v) for v in self.column('Implex')[:last + 1]),
                     default=0.0)
        dissipated = vals.get('Dissipated', 0.0)
        groups = []
        for c in self.groups():
            v = vals[c]
            groups.append({
                'group': label_of(c),
                'value': v,
                'share': (v / dissipated) if dissipated != 0.0 else 0.0,
            })
        return {
            'rows': self.rows(),
            'time': t_used,
            'end_time': self.time()[-1],
            'columns': {c: vals[c] for c in self.columns
                        if c != 'Time' and not c.startswith(GROUP_PREFIX)},
            'groups': groups,
            'max_abs_input': inp,
            'max_abs_error': err,
            'max_error_percent': (100.0 * err / inp) if inp > 0.0 else 0.0,
            'max_abs_implex': implex,
            'max_implex_percent': (100.0 * implex / inp) if inp > 0.0 else 0.0,
        }
