@echo off
echo Starting Threat Intelligence Platform Backend...
echo.

cd backend

if not exist venv (
    echo Creating virtual environment...
    py -m venv venv
    echo.
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt
echo.

echo Starting FastAPI server on http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
