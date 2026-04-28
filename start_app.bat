@echo off
setlocal
cd /d "%~dp0"

echo ====================================
echo  Knowledge Graph AI Assistant
echo ====================================
echo.

REM 1) Find available Python
set "PYTHON_EXE="
for %%C in (py python python3) do (
    if not defined PYTHON_EXE (
        %%C -c "import sys; sys.exit(0)" >nul 2>&1
        if not errorlevel 1 (
            set "PYTHON_EXE=%%C"
        )
    )
)

if not defined PYTHON_EXE (
    echo [ERROR] Python not found.
    echo.
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [OK] Python found:
%PYTHON_EXE% --version
echo.

REM 2) Install dependencies on first run
%PYTHON_EXE% -m streamlit --version >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing dependencies for the first time...
    echo.
    %PYTHON_EXE% -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [ERROR] Dependency installation failed.
        echo Please check your network connection and try again.
        pause
        exit /b 1
    )
    echo.
    echo [OK] Dependencies installed.
    echo.
)

REM 3) Check .env config file
if not exist ".env" (
    echo [WARN] .env file not found. AI features will not work.
    echo Copy .env.example to .env and fill in your API key.
    echo.
)

REM 4) Launch application
echo Starting Streamlit app. Your browser will open automatically.
echo Press Ctrl+C to stop the server.
echo.
%PYTHON_EXE% -m streamlit run streamlit_app.py

pause
endlocal
