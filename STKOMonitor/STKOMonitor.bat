echo off

REM try to use python in STKO, otherwise try installed python
if "%STKO_INSTALL_DIR%" == "" (
	echo "Running STKO Monitor with system Python..."
	set PYEXE=python
) else (
	echo "Running STKO Monitor with STKO Python..."
	set PYEXE="%STKO_INSTALL_DIR%\python.exe"
)

%PYEXE% "%~dp0\STKOMonitorMain.py"
