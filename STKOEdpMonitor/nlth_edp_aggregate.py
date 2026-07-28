# SYNC NOTE: the aggregation code below is duplicated at
#   <opspro>/Analysis/nlth_edp_aggregate.py
# (the canonical copy, used by the batch AggregateNlthSuite command inside the
# encrypted opspro package). This copy ships on disk so the PyMpc-free viewer
# bundle can import it flatly. Keep the code identical in both — edit both, or none.
"""
nlth_edp_aggregate.py
---------------------
PURE cross-suite aggregation of the per-run ``.edp`` records the EDP observers
write (see edp_observer.py / emit_recorders.emit_edp_observer). Turns the scalar
demands of every run into the statistics the three NLTH-suite methodologies need:

  * **code** — one nominal intensity: per-EDP mean / std / median / 16-84
    fractiles + envelope over the record set.
  * **ida** — a shared grid of intensity levels (the same records scaled up):
    per-level fractiles + collapse fraction, the per-record IM-EDP "spaghetti"
    curves, and a lognormal collapse fragility.
  * **msa** — a stripe per intensity level (different records per level):
    per-stripe fractiles + collapse fraction + the same fragility fit.

The design boundary (see references/NLTH_IDA_MSA_EDP_plan.md): this module reads
ONLY the ``.edp`` records + the suite manifest (``runs.json``). WHICH producer
wrote the ``.edp`` (the run-time Tcl actor now, a ``.mpco`` post-process later)
is irrelevant here. The same ``aggregate()`` feeds both a batch report and a
future real-time monitor (called on partial records on a timer).

NO PyMpc / STKO — run the self-test headless with::

    python opspro/Analysis/nlth_edp_aggregate.py

``aggregate(records, manifest, ...)`` is the tested core; ``read_edp_records`` /
``load_manifest`` are the thin disk face (the manifest shape is what the Phase-1
suite runner must write into ``runs.json``: one entry per run with its subdir,
method, im, record_id and level_index).
"""
import json
import math
import os

# completion tolerance: a run whose last converged pseudo-time reached its
# expected end (t_last >= t_end - eps) finished; otherwise it stopped early
# (non-convergence / collapse).
_EPS_T = 1.0e-6


# --------------------------------------------------------------------------- #
# small stats (no numpy)
# --------------------------------------------------------------------------- #
def _percentile(sorted_vals, p):
    """Linear-interpolated percentile ``p`` in [0, 100] of a sorted, non-empty
    list."""
    n = len(sorted_vals)
    if n == 1:
        return sorted_vals[0]
    r = (p / 100.0) * (n - 1)
    lo = int(math.floor(r))
    hi = int(math.ceil(r))
    if lo == hi:
        return sorted_vals[lo]
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (r - lo)


def _stats(vals):
    """mean / std (population) / min / max / 16-50-84 fractiles of *vals*, or
    None when empty."""
    if not vals:
        return None
    s = sorted(float(v) for v in vals)
    n = len(s)
    mean = sum(s) / n
    var = sum((v - mean) ** 2 for v in s) / n
    return {
        "n": n,
        "mean": mean,
        "std": math.sqrt(var),
        "min": s[0],
        "max": s[-1],
        "median": _percentile(s, 50),
        "p16": _percentile(s, 16),
        "p50": _percentile(s, 50),
        "p84": _percentile(s, 84),
    }


def _norm_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


# --------------------------------------------------------------------------- #
# lognormal collapse fragility (binomial MLE, Baker 2015) — grid + refine
# --------------------------------------------------------------------------- #
def _fit_fragility(level_counts):
    """``[(im, n, z_collapsed), ...]`` -> ``{theta, beta, im, p_collapse}`` or
    None. Fits a lognormal collapse fragility by maximum likelihood of the
    per-stripe binomial counts (handles censoring naturally, unlike moment-of-
    collapse-IM). A 2-parameter (median theta, dispersion beta) coarse grid then
    a local refine — cheap and robust for the handful of levels a suite has."""
    pts = [(float(im), int(n), int(z)) for (im, n, z) in level_counts
           if im > 0.0 and n > 0]
    if len(pts) < 2:
        return None
    ims = [im for im, _n, _z in pts]
    im_lo, im_hi = min(ims), max(ims)

    def negll(theta, beta):
        ll = 0.0
        for im, n, z in pts:
            p = _norm_cdf(math.log(im / theta) / beta)
            p = min(max(p, 1e-12), 1.0 - 1e-12)
            ll += z * math.log(p) + (n - z) * math.log(1.0 - p)
        return -ll

    best = [None, im_lo, 0.4]   # [negll, theta, beta]

    def scan(t0, t1, b0, b1, nt, nb):
        for it in range(nt):
            theta = t0 * (t1 / t0) ** (it / (nt - 1))
            for ib in range(nb):
                beta = b0 + (b1 - b0) * ib / (nb - 1)
                v = negll(theta, beta)
                if best[0] is None or v < best[0]:
                    best[0], best[1], best[2] = v, theta, beta

    scan(im_lo * 0.5, im_hi * 2.0, 0.05, 1.2, 60, 40)
    scan(best[1] * 0.8, best[1] * 1.25,
         max(0.02, best[2] * 0.6), best[2] * 1.5, 40, 40)
    theta, beta = best[1], best[2]
    xs = sorted(set(ims))
    return {
        "theta": theta,
        "beta": beta,
        "im": xs,
        "p_collapse": [_norm_cdf(math.log(x / theta) / beta) for x in xs],
    }


# --------------------------------------------------------------------------- #
# the aggregator (pure)
# --------------------------------------------------------------------------- #
def aggregate(records, manifest, *, edp="IDR", collapse_drift=0.10):
    """Cross-suite aggregation.

    *records*  : ``{subdir: {"edps": {name: value}, "t_last": float,
                 "t_end": float}}`` — one merged record per run (all its
                 ``.edp`` files folded together).
    *manifest* : ``{subdir: {"im": float, "method": "code"|"ida"|"msa",
                 "record_id": int, "level_index": int, "set_name": str}}``.

    *edp* drives the collapse test and the IDA curves (default 'IDR'); a run is
    'collapsed' when it did not complete (t_last < t_end) OR its *edp* reached
    *collapse_drift*. EDP statistics are conditioned on NON-collapse; collapse is
    carried separately in ``collapse_fraction`` and the fragility fit. Returns a
    single dict (see the module docstring / the plan for the schema)."""
    warnings = []
    runs = []
    edp_names = set()
    for subdir, meta in manifest.items():
        rec = records.get(subdir)
        if rec is None:
            warnings.append("run '{}' has no .edp record -> dropped".format(subdir))
            continue
        edps = dict(rec.get("edps", {}) or {})
        edp_names.update(edps.keys())
        t_last = float(rec.get("t_last", 0.0) or 0.0)
        t_end = float(rec.get("t_end", 0.0) or 0.0)
        completed = (t_end <= 0.0) or (t_last >= t_end - _EPS_T)
        drive = edps.get(edp)
        collapsed = (not completed) or (drive is not None
                                        and float(drive) >= collapse_drift)
        im = meta.get("im", meta.get("level", meta.get("total_factor", 1.0)))
        runs.append({
            "subdir": subdir,
            "im": float(im if im is not None else 1.0),
            "method": meta.get("method", "code"),
            "record_id": meta.get("record_id"),
            "level_index": meta.get("level_index"),
            "set_name": meta.get("set_name", ""),
            "edps": edps,
            "completed": completed,
            "collapsed": collapsed,
        })
    edp_names = sorted(edp_names)
    method = runs[0]["method"] if runs else "code"

    # --- per-IM-level cross-sectional stats (the shared kernel) -------------
    by_im = {}
    for r in runs:
        by_im.setdefault(round(r["im"], 9), []).append(r)
    levels = []
    for im in sorted(by_im):
        grp = by_im[im]
        n = len(grp)
        ncol = sum(1 for r in grp if r["collapsed"])
        stats = {}
        for name in edp_names:
            vals = [r["edps"][name] for r in grp
                    if (not r["collapsed"]) and name in r["edps"]]
            st = _stats(vals)
            if st is not None:
                stats[name] = st
        levels.append({
            "im": im, "n": n, "n_collapsed": ncol,
            "collapse_fraction": (ncol / n) if n else 0.0,
            "edp_stats": stats,
        })

    out = {
        "method": method, "edp": edp, "edp_names": edp_names,
        "collapse_drift": collapse_drift, "n_runs": len(runs),
        "levels": levels, "curves": None, "fragility": None,
        "warnings": warnings,
    }

    # --- IDA spaghetti: one IM-EDP curve per record, across its levels ------
    if method == "ida":
        by_rec = {}
        for r in runs:
            by_rec.setdefault(r["record_id"], []).append(r)
        curves = []
        for rid in sorted(by_rec, key=lambda x: (x is None, x)):
            pts = sorted(by_rec[rid], key=lambda r: r["im"])
            collapse_im = next((r["im"] for r in pts if r["collapsed"]), None)
            curves.append({
                "record_id": rid,
                "set_name": pts[0]["set_name"] if pts else "",
                "points": [dict({"im": r["im"]},
                                **{n: r["edps"].get(n) for n in edp_names})
                           for r in pts],
                "collapse_im": collapse_im,
            })
        out["curves"] = curves

    # --- collapse fragility (ida / msa) -------------------------------------
    if method in ("ida", "msa"):
        total_col = sum(l["n_collapsed"] for l in levels)
        total_n = sum(l["n"] for l in levels)
        if total_col == 0:
            warnings.append("no run collapsed -> no fragility fit (raise the "
                            "intensity or lower collapse_drift)")
        elif total_col == total_n:
            warnings.append("every run collapsed -> no fragility fit")
        else:
            frag = _fit_fragility([(l["im"], l["n"], l["n_collapsed"])
                                   for l in levels])
            if frag is None:
                warnings.append("fragility fit needs >= 2 IM levels")
            out["fragility"] = frag
    return out


# --------------------------------------------------------------------------- #
# disk face (the manifest shape is Phase-1's runs.json contract)
# --------------------------------------------------------------------------- #
def read_edp_records(out_base):
    """Scan ``out_base/<run>/`` for ``*.edp`` files and MERGE them per run
    directory into ``{subdir_basename: {"edps", "t_last", "t_end"}}`` (each
    observer writes its own ``.edp``; a run's record is their union)."""
    out = {}
    try:
        names = os.listdir(out_base)
    except OSError:
        return out
    for name in names:
        sub = os.path.join(out_base, name)
        if not os.path.isdir(sub):
            continue
        merged = {"edps": {}, "t_last": 0.0, "t_end": 0.0}
        found = False
        for f in os.listdir(sub):
            if not f.endswith(".edp"):
                continue
            try:
                with open(os.path.join(sub, f), "r") as fh:
                    rec = json.load(fh)
            except (OSError, ValueError):
                continue
            merged["edps"].update(rec.get("edps", {}) or {})
            merged["t_last"] = max(merged["t_last"], float(rec.get("t_last", 0.0) or 0.0))
            merged["t_end"] = max(merged["t_end"], float(rec.get("t_end", 0.0) or 0.0))
            found = True
        if found:
            out[name] = merged
    return out


def load_manifest(out_base):
    """Read the suite ``runs.json`` into ``{subdir_basename: meta}``. Accepts
    either a bare list of run entries or ``{"runs": [...]}``. Each entry is keyed
    by the basename of its ``subdir``; ``im`` is taken from 'im' / 'level' /
    'total_factor' (in that order), ``record_id`` from 'record_id' / 'set_index'.
    This is the contract the Phase-1 runner must satisfy when it writes
    runs.json."""
    path = os.path.join(out_base, "runs.json")
    try:
        with open(path, "r") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return {}
    entries = data.get("runs", data) if isinstance(data, dict) else data
    out = {}
    for e in (entries or []):
        if not isinstance(e, dict):
            continue
        sub = e.get("subdir", "")
        key = os.path.basename(str(sub).replace("\\", "/").rstrip("/"))
        if not key:
            continue
        im = e.get("im", e.get("level", e.get("total_factor", 1.0)))
        out[key] = {
            "im": float(im if im is not None else 1.0),
            "method": e.get("method", "code"),
            "record_id": e.get("record_id", e.get("set_index")),
            "level_index": e.get("level_index"),
            "set_name": e.get("set_name", ""),
        }
    return out


def aggregate_dir(out_base, *, edp="IDR", collapse_drift=0.10):
    """Convenience: ``aggregate`` over a suite output directory on disk."""
    return aggregate(read_edp_records(out_base), load_manifest(out_base),
                     edp=edp, collapse_drift=collapse_drift)


# --------------------------------------------------------------------------- #
# headless self-test
# --------------------------------------------------------------------------- #
def _rec(idr=None, pfa=None, t_last=30.0, t_end=30.0):
    edps = {}
    if idr is not None:
        edps["IDR"] = idr
    if pfa is not None:
        edps["PFA"] = pfa
    return {"edps": edps, "t_last": t_last, "t_end": t_end}


def _selftest():
    failed = []
    total = [0]

    def check(name, cond):
        total[0] += 1
        print(("pass  " if cond else "FAIL  ") + name)
        if not cond:
            failed.append(name)

    # --- code: one nominal IM, mean / envelope / no collapse ----------------
    recs = {"r0": _rec(0.010, 5.0), "r1": _rec(0.020, 7.0), "r2": _rec(0.015, 6.0)}
    man = {k: {"im": 1.0, "method": "code", "record_id": i}
           for i, k in enumerate(recs)}
    a = aggregate(recs, man)
    lv = a["levels"]
    check("code: one level", len(lv) == 1 and lv[0]["n"] == 3)
    check("code: no collapse", lv[0]["n_collapsed"] == 0)
    check("code: IDR mean", abs(lv[0]["edp_stats"]["IDR"]["mean"] - 0.015) < 1e-9)
    check("code: IDR envelope (max)", abs(lv[0]["edp_stats"]["IDR"]["max"] - 0.020) < 1e-9)
    check("code: PFA present", "PFA" in lv[0]["edp_stats"])
    check("code: no fragility", a["fragility"] is None and a["curves"] is None)

    # --- ida: 2 records x 3 levels; record 1 collapses at the top -----------
    recs = {
        "r0_L0": _rec(0.005), "r0_L1": _rec(0.020), "r0_L2": _rec(0.080),
        "r1_L0": _rec(0.006), "r1_L1": _rec(0.030),
        "r1_L2": _rec(0.090, t_last=12.0, t_end=30.0),  # stopped early -> collapse
    }
    man = {}
    for rid in (0, 1):
        for li, im in enumerate((0.5, 1.0, 1.5)):
            man["r{}_L{}".format(rid, li)] = {
                "im": im, "method": "ida", "record_id": rid, "level_index": li,
                "set_name": "rec{}".format(rid)}
    a = aggregate(recs, man, edp="IDR", collapse_drift=0.10)
    lvs = {l["im"]: l for l in a["levels"]}
    check("ida: 3 levels", set(lvs) == {0.5, 1.0, 1.5})
    check("ida: top level 1/2 collapsed",
          lvs[1.5]["n_collapsed"] == 1 and abs(lvs[1.5]["collapse_fraction"] - 0.5) < 1e-9)
    check("ida: lower levels intact",
          lvs[0.5]["n_collapsed"] == 0 and lvs[1.0]["n_collapsed"] == 0)
    check("ida: EDP stats exclude the collapsed run at top",
          lvs[1.5]["edp_stats"]["IDR"]["n"] == 1)
    curves = {c["record_id"]: c for c in a["curves"]}
    check("ida: 2 spaghetti curves", set(curves) == {0, 1})
    check("ida: record 1 collapse_im = 1.5", curves[1]["collapse_im"] == 1.5)
    check("ida: record 0 never collapses", curves[0]["collapse_im"] is None)
    check("ida: fragility fitted", a["fragility"] is not None
          and a["fragility"]["theta"] > 0.0 and a["fragility"]["beta"] > 0.0)

    # --- msa: per-stripe fractiles + fragility from stripe counts -----------
    recs, man = {}, {}
    # 3 stripes; collapse fraction rises with IM: 0/3, 1/3, 2/3
    plan = [(0.4, [0.006, 0.007, 0.008], []),
            (0.8, [0.02, 0.03], [2]),          # index 2 collapses
            (1.2, [0.05], [1, 2])]             # indices 1,2 collapse
    for si, (im, idrs, coll) in enumerate(plan):
        for ri in range(3):
            key = "s{}_r{}".format(si, ri)
            if ri in coll:
                recs[key] = _rec(0.12, t_last=10.0, t_end=30.0)
            elif ri < len(idrs):
                recs[key] = _rec(idrs[ri])
            else:
                continue
            man[key] = {"im": im, "method": "msa", "record_id": ri,
                        "level_index": si, "set_name": "s{}".format(si)}
    a = aggregate(recs, man, edp="IDR", collapse_drift=0.10)
    lvs = {l["im"]: l for l in a["levels"]}
    check("msa: 3 stripes", set(lvs) == {0.4, 0.8, 1.2})
    check("msa: collapse fractions rise",
          lvs[0.4]["n_collapsed"] == 0 and lvs[0.8]["n_collapsed"] == 1
          and lvs[1.2]["n_collapsed"] == 2)
    check("msa: no spaghetti curves", a["curves"] is None)
    check("msa: fragility fitted (theta within IM range)",
          a["fragility"] is not None
          and 0.4 <= a["fragility"]["theta"] <= 1.2 * 2.0)

    # --- missing record is warned, not fatal --------------------------------
    a = aggregate({"r0": _rec(0.01)},
                  {"r0": {"im": 1.0, "method": "code"},
                   "r1": {"im": 1.0, "method": "code"}})
    check("missing record -> warning", any("no .edp" in w for w in a["warnings"]))

    print("-" * 56)
    print("{}/{} passed".format(total[0] - len(failed), total[0]))
    if failed:
        print("FAILURES: " + ", ".join(failed))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(_selftest())
