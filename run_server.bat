@echo off
REM Django eCommerce - Startup Script for Windows

echo.
echo ========================================
echo  Django eCommerce Application
echo  Starting Server...
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found in PATH
    echo Please install Python or add it to your PATH
    pause
    exit /b 1
)

REM Check if Django is installed
python -c "import django; print(django.get_version())" >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Django not installed
    echo Run: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Navigate to project directory
cd /d "%~dp0"

REM Check if manage.py exists
if not exist "manage.py" (
    echo ERROR: manage.py not found!
    echo Make sure you're in the correct directory
    pause
    exit /b 1
)

echo [1/3] Running Django system check...
python manage.py check
if %errorlevel% neq 0 (
    echo ERROR: Django system check failed
    pause
    exit /b 1
)

echo [2/3] Applying any pending migrations...
python manage.py migrate --noinput
if %errorlevel% neq 0 (
    echo WARNING: Migration issue, but continuing...
)

echo [3/3] Starting development server...
echo.
echo ========================================
echo  Server running at: http://127.0.0.1:8000/
echo  Admin panel at:    http://127.0.0.1:8000/admin/
echo  Press CTRL+C to stop server
echo ========================================
echo.

python manage.py runserver 8000

