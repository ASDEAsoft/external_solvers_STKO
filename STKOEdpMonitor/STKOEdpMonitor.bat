echo off

REM try to use python in STKO, otherwise try installed python.
REM NOTE: the working directory is inherited from the caller (the suite root),
REM which is exactly the directory the monitor polls for .edp / runs.json.
if "%STKO_INSTALL_DIR%" == "" (
	echo "Running STKO EDP Monitor with system Python..."
	set PYEXE=python
) else (
	echo "Running STKO EDP Monitor with STKO Python..."
	set PYEXE="%STKO_INSTALL_DIR%\python.exe"
)

%PYEXE% "%~dp0\STKOEdpMonitorMain.py"
