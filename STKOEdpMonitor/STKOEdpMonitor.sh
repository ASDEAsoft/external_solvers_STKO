#!/bin/sh
# Run the STKO EDP Monitor. The working directory is inherited from the caller
# (the suite root) — the directory the monitor polls for .edp / runs.json.
DIR="$(cd "$(dirname "$0")" && pwd)"
# macOS: STKO sets STKO_INSTALL_DIR to the bundle's data root (Contents/Resources),
# which holds no "python": the interpreter is Contents/MacOS/python3.x beside it
# (python3.10 on Qt 5, python3.12 on Qt 6), and PySide's extension modules need the
# bundle's Qt frameworks on the loader path.
if [ "$(uname)" = "Darwin" ] && [ -n "$STKO_INSTALL_DIR" ]; then
	FW="$STKO_INSTALL_DIR/../Frameworks"
	for PY in "$STKO_INSTALL_DIR"/../MacOS/python3.*; do
		if [ -x "$PY" ]; then
			echo "Running STKO EDP Monitor with STKO Python..."
			export DYLD_FRAMEWORK_PATH="$FW${DYLD_FRAMEWORK_PATH:+:$DYLD_FRAMEWORK_PATH}"
			exec "$PY" "$DIR/STKOEdpMonitorMain.py"
		fi
	done
fi
if [ -z "$STKO_INSTALL_DIR" ]; then
	echo "Running STKO EDP Monitor with system Python..."
	PYEXE=python
else
	echo "Running STKO EDP Monitor with STKO Python..."
	PYEXE="$STKO_INSTALL_DIR/python"
fi
"$PYEXE" "$DIR/STKOEdpMonitorMain.py"
