@echo off
setlocal EnableExtensions
pushd "%~dp0"

REM (Optional) auto-activate a local venv if it exists
if exist ".venv\Scripts\activate.bat" call ".venv\Scripts\activate.bat"

echo [1/3] Cleaning _build folder...
if exist "_build" rmdir /s /q "_build"

echo [2/4] Strip numbered titles from tutorials (md / ipynb)...
python -m scripts.strip_titles
if errorlevel 1 (
  echo.
  echo [FAILED] strip_titles returned %errorlevel%.
  echo.
  goto :PAUSE
)

echo [3/4] jb build .
jb build .
if errorlevel 1 (
  echo.
  echo [FAILED] jb build returned %errorlevel%.
  echo.
  goto :PAUSE
)

echo.
echo [4/4] ghp-import -n -p -f _build\html
python publish.py

echo.
echo [OK] Done.

:PAUSE
echo.
echo Press any key to close...
pause >nul

popd
endlocal
