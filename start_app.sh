#!/usr/bin/env bash

cd "$(dirname "$0")" || exit 1

echo "===================================="
echo " Knowledge Graph AI Assistant"
echo "===================================="
echo

# 1. Find available Python
PYTHON_EXE=""
for cmd in python3 python py; do
    if [ -z "$PYTHON_EXE" ] && command -v "$cmd" >/dev/null 2>&1; then
        if "$cmd" -c "import sys; sys.exit(0)" >/dev/null 2>&1; then
            PYTHON_EXE="$cmd"
        fi
    fi
done

if [ -z "$PYTHON_EXE" ]; then
    echo "[ERROR] Python not found."
    echo
    echo "Please install Python 3.8+ and try again."
    exit 1
fi

echo "[OK] Python found:"
"$PYTHON_EXE" --version
echo

# 2. Install dependencies on first run
"$PYTHON_EXE" -m streamlit --version >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "[INFO] Installing dependencies for the first time..."
    echo
    "$PYTHON_EXE" -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo
        echo "[ERROR] Dependency installation failed."
        echo "        Please check your network connection and try again."
        exit 1
    fi
    echo
    echo "[OK] Dependencies installed."
    echo
fi

# 3. Check .env config file
if [ ! -f ".env" ]; then
    echo "[WARN] .env file not found. AI features will not work."
    echo "       Copy .env.example to .env and fill in your API key."
    echo
fi

# 4. Launch application
echo "Starting Streamlit app. Your browser will open automatically."
echo "Press Ctrl+C to stop the server."
echo
"$PYTHON_EXE" -m streamlit run streamlit_app.py
