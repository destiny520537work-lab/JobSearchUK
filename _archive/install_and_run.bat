@echo off
REM Install dependencies and run LinkedIn Job Scraper (Windows)

echo.
echo ========================================
echo.   LinkedIn UK Job Scraper Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [x] Python is not installed. Please install Python 3.8 or higher.
    echo.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python found
python --version

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo [x] Failed to install dependencies
    pause
    exit /b 1
)

echo [OK] Dependencies installed

REM Create output directory
echo.
echo Creating output directory...
if not exist "output" mkdir output
echo [OK] Output directory ready

REM Run scraper
echo.
echo ========================================
echo.   Starting LinkedIn Job Scraper
echo ========================================
echo.

python scraper.py %*

pause
