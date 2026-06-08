@echo off
echo ========================================
echo  Property Management System - Frontend
echo ========================================
echo.

cd /d "%~dp0"

if not exist "node_modules" (
    echo Installing dependencies...
    pnpm install
)

echo Starting dev server...
pnpm dev
pause
