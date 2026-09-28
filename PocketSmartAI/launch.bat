@echo off
cd /d "%~dp0"
echo ============================================
echo   PocketSmart AI is starting...
echo ============================================
echo.
echo Opening browser...
start http://localhost:8000
echo.
echo Server starting on http://localhost:8000
echo Press Ctrl+C to stop
echo.
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
