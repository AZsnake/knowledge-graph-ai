@echo off
echo ====================================
echo Knowledge Graph AI Assistant
echo ====================================
echo.

REM Find the Python that owns the streamlit on PATH
for /f "delims=" %%S in ('where streamlit 2^>nul') do (
    set STREAMLIT_EXE=%%S
    goto :found
)
echo Error: streamlit not found. Run: pip install streamlit
pause
exit /b 1

:found
REM Derive the Python executable from streamlit's location
for %%F in ("%STREAMLIT_EXE%") do set STREAMLIT_DIR=%%~dpF
set PYTHON_EXE=%STREAMLIT_DIR%python.exe
if not exist "%PYTHON_EXE%" set PYTHON_EXE=python

REM Install / verify all dependencies using the same Python
echo Checking dependencies...
"%PYTHON_EXE%" -m pip show pyvis >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    "%PYTHON_EXE%" -m pip install -r requirements.txt
)

REM Start application
echo.
echo Starting Streamlit application...
echo.
streamlit run streamlit_app.py

pause
