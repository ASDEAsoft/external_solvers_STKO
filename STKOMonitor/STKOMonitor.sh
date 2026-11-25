#!/bin/sh
BASEDIR=$(dirname $0)
# macOS: a bare python3 is Apple's (or nothing at all) and has no PySide6. When
# started by STKO, STKO_INSTALL_DIR is the bundle's data root (Contents/Resources):
# use the bundled interpreter (python3.10 on Qt 5, python3.12 on Qt 6), and point
# the loader at the bundle's Qt frameworks that PySide6's extension modules use.
if [ "$(uname)" = "Darwin" ] && [ -n "$STKO_INSTALL_DIR" ]; then
	FW="$STKO_INSTALL_DIR/../Frameworks"
	for PY in "$STKO_INSTALL_DIR"/../MacOS/python3.*; do
		if [ -x "$PY" ]; then
			export DYLD_FRAMEWORK_PATH="$FW${DYLD_FRAMEWORK_PATH:+:$DYLD_FRAMEWORK_PATH}"
			exec "$PY" "${BASEDIR}/STKOMonitorMain.py"
		fi
	done
fi
python3 ${BASEDIR}/STKOMonitorMain.py
