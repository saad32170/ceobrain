@echo off
setlocal enabledelayedexpansion
echo ========================================
echo CEO Personal OS - Git Initialization
echo ========================================
echo.
echo Initializing git repository and connecting to:
echo https://github.com/saad32170/ceobrain
echo.

cd /d "%~dp0"

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed or not in PATH.
    echo Please install Git from https://git-scm.com/
    pause
    exit /b 1
)

REM Check if git is already initialized
git rev-parse --show-toplevel >nul 2>&1
if errorlevel 1 (
    echo Initializing git repository...
    git init
    if errorlevel 1 (
        echo ERROR: Failed to initialize git repository.
        pause
        exit /b 1
    )
    echo Git repository initialized.
    echo.
) else (
    for /f "delims=" %%i in ('git rev-parse --show-toplevel') do set GIT_ROOT=%%i
    if /i not "%GIT_ROOT%"=="%CD%" (
        echo WARNING: Git repository detected in parent directory.
        echo Re-initializing in ceo-personal-os...
        if exist ".git" (
            if not exist ".git\config" (
                del /f /q ".git" 2>nul
            )
        )
        git init
    ) else (
        echo Git repository already initialized.
        echo.
    )
)

REM Set up remote origin
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo Adding remote origin...
    git remote add origin https://github.com/saad32170/ceobrain.git
    if errorlevel 1 (
        echo ERROR: Failed to add remote origin.
        pause
        exit /b 1
    )
    echo Remote 'origin' added.
) else (
    echo Updating remote origin...
    git remote set-url origin https://github.com/saad32170/ceobrain.git
    echo Remote 'origin' updated.
)
echo.

REM Check if we need to set up branch tracking
git branch -M main 2>nul
git branch -M master 2>nul

echo ========================================
echo Git initialization complete!
echo ========================================
echo.
echo Repository: https://github.com/saad32170/ceobrain
echo.
echo Next steps:
echo 1. Make your first commit: git add . ^&^& git commit -m "Initial commit"
echo 2. Push to GitHub: git push -u origin main
echo.
echo Or just start using the app - auto-commit will handle it!
echo.
pause
