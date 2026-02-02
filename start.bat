@echo off
REM Campus AI Chat Platform - Windows Start Script

echo Starting Campus AI Chat Platform...
echo.

REM Check if virtual environment exists
if not exist ".env\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run: python setup.py
    pause
    exit /b 1
)

REM Activate virtual environment
call .env\Scripts\activate.bat

REM Check if model exists
if not exist "models\*.gguf" (
    echo WARNING: No model found in models/ directory
    echo Please run: python scripts\download_model.py
    pause
    exit /b 1
)

REM Start server
echo.
echo Server starting at http://localhost:8080
echo Press Ctrl+C to stop the server
echo.

python server.py

REM Deactivate on exit
deactivate
