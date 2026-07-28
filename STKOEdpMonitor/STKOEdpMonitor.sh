#!/bin/sh
# Run the STKO EDP Monitor. The working directory is inherited from the caller
# (the suite root) — the directory the monitor polls for .edp / runs.json.
DIR="$(cd "$(dirname "$0")" && pwd)"
if [ -z "$STKO_INSTALL_DIR" ]; then
	echo "Running STKO EDP Monitor with system Python..."
	PYEXE=python
else
	echo "Running STKO EDP Monitor with STKO Python..."
	PYEXE="$STKO_INSTALL_DIR/python"
fi
"$PYEXE" "$DIR/STKOEdpMonitorMain.py"
