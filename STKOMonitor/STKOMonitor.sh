#!/bin/sh
BASEDIR=$(dirname $0)
# macOS: a bare python3 is Apple's (or nothing at all) and has no PySide2. When
# started by STKO, STKO_INSTALL_DIR is the bundle's data root (Contents/Resources):
# use the bundled interpreter, and point the loader at the bundle's Qt frameworks
# that PySide2's extension modules were linked against.
if [ "$(uname)" = "Darwin" ] && [ -n "$STKO_INSTALL_DIR" ]; then
	FW="$STKO_INSTALL_DIR/../Frameworks"
	PY="$STKO_INSTALL_DIR/../MacOS/python3.10"
	if [ -x "$PY" ]; then
		export DYLD_FRAMEWORK_PATH="$FW${DYLD_FRAMEWORK_PATH:+:$DYLD_FRAMEWORK_PATH}"
		exec "$PY" "${BASEDIR}/STKOMonitorMain.py"
	fi
fi
python3 ${BASEDIR}/STKOMonitorMain.py
