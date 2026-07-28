"""
edp_realtime.py
---------------
PURE realtime-classification layer that sits between the on-disk ``.edp``
records and the pure ``aggregate()`` (nlth_edp_aggregate.py) so a suite that is
still RUNNING plots correctly.

Why this layer exists
---------------------
``aggregate()`` decides a run is COLLAPSED when it did not complete
(``t_last < t_end``). That is right for a FINISHED suite, but mid-run every job
that is still integrating also has ``t_last < t_end`` — feeding those straight
into ``aggregate()`` would miscount every live job as a collapse and poison the
fractiles and the fragility fit.

A single ``.edp`` snapshot cannot tell "stopped early" from "still running": the
actor rewrites the file every sampled step, so a live run and a crashed run look
identical at one instant. The difference is only visible over TIME — a live run's
``t_last`` keeps advancing, a dead one's does not. This layer watches ``t_last``
across polling ticks and splits the runs into:

  * ``LIVE``          — not complete, but ``t_last`` advanced within the last
                        ``stale_ticks`` polls (still integrating);
  * ``DONE_OK``       — complete (``t_last >= t_end``);
  * ``DONE_COLLAPSE`` — not complete AND ``t_last`` has been unchanged for
                        ``stale_ticks`` consecutive polls (the process stopped
                        without finishing → non-convergence / collapse).

Only ``DONE_*`` runs are handed to ``aggregate()`` (so its own
collapsed/non-collapsed logic stays exactly correct — a ``DONE_COLLAPSE`` run
still has ``t_last < t_end`` and is classified as a collapse there); the
``LIVE`` runs are returned separately for a provisional overlay.

NO Qt / matplotlib / numpy — headless self-test::

    python edp_realtime.py
"""

# Same completion tolerance the aggregator uses.
_EPS_T = 1.0e-6

LIVE = "live"
DONE_OK = "done_ok"
DONE_COLLAPSE = "done_collapse"


class RealtimeState:
    """Stateful classifier over successive ``.edp`` polls.

    One instance per monitored suite directory; call :meth:`update` once per
    polling tick with the freshly-read records + manifest. It remembers each
    run's last seen ``t_last`` and a per-run stale counter so it can flip a
    stalled run to ``DONE_COLLAPSE`` after *stale_ticks* motionless polls.

    *stale_ticks* is in POLLS, not seconds: with a 1.5 s poll the default 8 ≈
    12 s of no progress before a run is called dead. Raise it for very heavy
    models whose single step can take longer than that (a slow-but-alive run
    must not be flipped to collapse); lower it to see collapses sooner."""

    def __init__(self, stale_ticks=8):
        self.stale_ticks = max(1, int(stale_ticks))
        # subdir -> {"t": last t_last, "stale": consecutive-unchanged count,
        #            "done": once True never reconsidered}
        self._seen = {}

    def reset(self):
        self._seen.clear()

    def update(self, records, manifest):
        """Classify the current poll.

        *records*  : ``{subdir: {"edps", "t_last", "t_end"}}`` (already merged
                     per run by ``read_edp_records``).
        *manifest* : ``{subdir: {"im", "method", "record_id", "level_index",
                     "set_name"}}`` (``load_manifest``).

        Returns a snapshot dict::

            {
              "finished_records":  {subdir: rec},   # DONE_OK + DONE_COLLAPSE
              "finished_manifest": {subdir: meta},  # same keys, for aggregate()
              "live":   [ {subdir, im, method, record_id, level_index,
                           set_name, edps, t_last, t_end, progress} ],
              "states": {subdir: LIVE|DONE_OK|DONE_COLLAPSE},
              "counts": {"total", "pending", "live", "done_ok",
                         "done_collapse", "collapsed"},
            }

        ``finished_records`` / ``finished_manifest`` are meant to be passed
        straight to ``aggregate()``; ``live`` is the provisional overlay; a run
        in the manifest with no ``.edp`` yet is PENDING (counted, not listed)."""
        finished_records = {}
        finished_manifest = {}
        live = []
        states = {}
        pending = 0

        for subdir, meta in manifest.items():
            rec = records.get(subdir)
            if rec is None:
                pending += 1
                continue
            t_last = float(rec.get("t_last", 0.0) or 0.0)
            t_end = float(rec.get("t_end", 0.0) or 0.0)
            completed = (t_end <= 0.0) or (t_last >= t_end - _EPS_T)

            prev = self._seen.get(subdir)
            if prev is None:
                prev = {"t": None, "stale": 0, "done": False}
                self._seen[subdir] = prev

            if prev["done"]:
                # Already decided (completed earlier, or ruled a collapse); keep
                # it in the finished set and never re-open it.
                state = prev.get("state", DONE_OK)
            elif completed:
                state = DONE_OK
                prev["done"] = True
                prev["state"] = state
            else:
                # Not complete: is t_last still advancing?
                if prev["t"] is None or t_last > prev["t"] + _EPS_T:
                    prev["stale"] = 0
                    state = LIVE
                else:
                    prev["stale"] += 1
                    if prev["stale"] >= self.stale_ticks:
                        state = DONE_COLLAPSE
                        prev["done"] = True
                        prev["state"] = state
                    else:
                        state = LIVE
            prev["t"] = t_last
            states[subdir] = state

            if state == LIVE:
                progress = (t_last / t_end) if t_end > 0.0 else 0.0
                live.append({
                    "subdir": subdir,
                    "im": float(meta.get("im", 1.0) or 1.0),
                    "method": meta.get("method", "code"),
                    "record_id": meta.get("record_id"),
                    "level_index": meta.get("level_index"),
                    "set_name": meta.get("set_name", ""),
                    "edps": dict(rec.get("edps", {}) or {}),
                    "t_last": t_last,
                    "t_end": t_end,
                    "progress": max(0.0, min(1.0, progress)),
                })
            else:
                finished_records[subdir] = rec
                finished_manifest[subdir] = meta

        done_ok = sum(1 for s in states.values() if s == DONE_OK)
        done_collapse = sum(1 for s in states.values() if s == DONE_COLLAPSE)
        return {
            "finished_records": finished_records,
            "finished_manifest": finished_manifest,
            "live": live,
            "states": states,
            "counts": {
                "total": len(manifest),
                "pending": pending,
                "live": len(live),
                "done_ok": done_ok,
                "done_collapse": done_collapse,
                # 'collapsed' here is only the STALLED runs; aggregate() may
                # additionally flag a completed run whose edp exceeded the drift
                # limit — that count lives in its per-level 'n_collapsed'.
                "collapsed": done_collapse,
            },
        }


# --------------------------------------------------------------------------- #
# headless self-test
# --------------------------------------------------------------------------- #
def _rec(idr, t_last, t_end=30.0):
    return {"edps": {"IDR": idr}, "t_last": t_last, "t_end": t_end}


def _selftest():
    failed = []
    total = [0]

    def check(name, cond):
        total[0] += 1
        print(("pass  " if cond else "FAIL  ") + name)
        if not cond:
            failed.append(name)

    man = {
        "r0": {"im": 1.0, "method": "ida", "record_id": 0, "level_index": 0,
               "set_name": "a"},
        "r1": {"im": 1.5, "method": "ida", "record_id": 0, "level_index": 1,
               "set_name": "a"},
    }

    # --- a completed run is DONE_OK immediately ----------------------------- #
    st = RealtimeState(stale_ticks=3)
    snap = st.update({"r0": _rec(0.01, 30.0)}, {"r0": man["r0"]})
    check("completed -> DONE_OK at once", snap["states"]["r0"] == DONE_OK)
    check("completed -> in finished set", "r0" in snap["finished_records"])
    check("completed -> not live", snap["counts"]["live"] == 0)

    # --- a run with no .edp yet is PENDING ---------------------------------- #
    st = RealtimeState(stale_ticks=3)
    snap = st.update({}, man)
    check("no record -> pending", snap["counts"]["pending"] == 2
          and snap["counts"]["total"] == 2)

    # --- an advancing run stays LIVE, never leaks into aggregate ------------ #
    st = RealtimeState(stale_ticks=3)
    st.update({"r1": _rec(0.02, 5.0)}, {"r1": man["r1"]})
    st.update({"r1": _rec(0.03, 10.0)}, {"r1": man["r1"]})
    snap = st.update({"r1": _rec(0.04, 15.0)}, {"r1": man["r1"]})
    check("advancing -> LIVE", snap["states"]["r1"] == LIVE)
    check("advancing -> not in finished", "r1" not in snap["finished_records"])
    check("advancing -> listed live with progress",
          len(snap["live"]) == 1 and abs(snap["live"][0]["progress"] - 0.5) < 1e-9)

    # --- a stalled (crashed/collapsed) run flips to DONE_COLLAPSE ----------- #
    st = RealtimeState(stale_ticks=3)
    st.update({"r1": _rec(0.09, 12.0)}, {"r1": man["r1"]})   # first sight
    s1 = st.update({"r1": _rec(0.09, 12.0)}, {"r1": man["r1"]})  # stale 1
    check("stalled once -> still LIVE", s1["states"]["r1"] == LIVE)
    st.update({"r1": _rec(0.09, 12.0)}, {"r1": man["r1"]})   # stale 2
    s3 = st.update({"r1": _rec(0.09, 12.0)}, {"r1": man["r1"]})  # stale 3 == limit
    check("stalled for stale_ticks -> DONE_COLLAPSE",
          s3["states"]["r1"] == DONE_COLLAPSE)
    check("collapsed -> in finished set (for aggregate)",
          "r1" in s3["finished_records"])
    check("collapsed -> counted", s3["counts"]["done_collapse"] == 1)

    # --- once decided, a run is never re-opened (even if it 'resumes') ------ #
    s4 = st.update({"r1": _rec(0.09, 20.0)}, {"r1": man["r1"]})
    check("decided run stays decided", s4["states"]["r1"] == DONE_COLLAPSE
          and "r1" in s4["finished_records"])

    # --- mixed poll: one live, one done, one pending ------------------------ #
    man3 = dict(man)
    man3["r2"] = {"im": 2.0, "method": "ida", "record_id": 1, "level_index": 2,
                  "set_name": "b"}
    st = RealtimeState(stale_ticks=3)
    snap = st.update({"r0": _rec(0.01, 30.0), "r1": _rec(0.02, 5.0)}, man3)
    c = snap["counts"]
    check("mixed counts", c["total"] == 3 and c["pending"] == 1
          and c["live"] == 1 and c["done_ok"] == 1)
    check("mixed: only the finished run feeds aggregate",
          set(snap["finished_records"]) == {"r0"})

    print("-" * 56)
    print("{}/{} passed".format(total[0] - len(failed), total[0]))
    if failed:
        print("FAILURES: " + ", ".join(failed))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(_selftest())
