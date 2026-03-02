@echo off
setlocal EnableExtensions
pushd "%~dp0"

REM (Optional) auto-activate a local venv if it exists
if exist ".venv\Scripts\activate.bat" call ".venv\Scripts\activate.bat"

echo [1/2] jb build .
jb build .
if errorlevel 1 (
  echo.
  echo [FAILED] jb build returned %errorlevel%.
  echo.
  goto :PAUSE
)

echo.
echo [2/2] ghp-import -n -p -f _build\html
python publish.py

echo.
echo [OK] Done.

:PAUSE
echo.
echo Press any key to close...
pause >nul

popd
endlocal
