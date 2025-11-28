@echo off
REM One-step startup script for Second-Hand Marketplace
REM Run this file to start the web server instantly

cd /d "%~dp0"

echo.
echo ========================================
echo   Second-Hand Marketplace
echo ========================================
echo.

REM Check if venv exists, if not create it
if not exist ".venv" (
    echo [1/5] Creating virtual environment...
    python -m venv .venv
    echo [2/5] Installing dependencies...
    .venv\Scripts\python.exe -m pip install -q --upgrade pip
    .venv\Scripts\python.exe -m pip install -q -r requirements.txt
    echo [3/5] Setting up database...
    .venv\Scripts\python.exe scripts\create_tables_if_missing.py
    echo [4/5] Generating images...
    .venv\Scripts\python.exe scripts\generate_images.py
    echo [5/5] Adding sample products...
    .venv\Scripts\python.exe scripts\seed_products.py
    echo.
    echo Setup complete!
) else (
    echo Virtual environment already exists. Skipping setup.
)

echo.
echo Starting Flask server...
echo.
echo ========================================
echo   Server is running!
echo   Open browser: http://127.0.0.1:5000
echo   Admin Email: admin@site.com
echo   Admin Password: admin123
echo   Press Ctrl+C to stop
echo ========================================
echo.

.venv\Scripts\python.exe app.py

pause
