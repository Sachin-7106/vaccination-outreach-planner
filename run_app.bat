@echo off
echo =======================================================================
echo  City Health Dept — Seasonal Infectious Disease Vaccination Outreach Planner
echo =======================================================================
echo.

echo [1/3] Setting up Python virtual environment / dependencies...
python -m pip install -r backend\requirements.txt

echo.
echo [2/3] Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "Vaccination Outreach Planner Backend" cmd /k "set PYTHONPATH=backend && python backend\main.py"

echo.
echo [3/3] Installing Frontend dependencies and starting Vite Dev Server ...
cd frontend
call npm install
start "Vaccination Outreach Planner Frontend" cmd /k "npm run dev"

echo.
echo =======================================================================
echo  System Started Successfully!
echo  - Frontend Dashboard: http://localhost:3000
echo  - Backend API & Docs: http://localhost:8000/docs
echo =======================================================================
pause
