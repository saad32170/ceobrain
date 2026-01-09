@echo off
setlocal enabledelayedexpansion
echo ========================================
echo CEO Personal OS - Git Setup
echo ========================================
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

echo Git is installed.
echo.

REM Check if git is already initialized in THIS directory
git rev-parse --show-toplevel >nul 2>&1
if errorlevel 1 (
    echo Initializing git repository in ceo-personal-os...
    git init
    if errorlevel 1 (
        echo ERROR: Failed to initialize git repository.
        pause
        exit /b 1
    )
    echo Git repository initialized.
    echo.
) else (
    REM Check if the git root is this directory
    for /f "delims=" %%i in ('git rev-parse --show-toplevel') do set GIT_ROOT=%%i
    if /i "%GIT_ROOT%"=="%CD%" (
        echo Git repository already initialized in ceo-personal-os.
        echo.
    ) else (
        echo WARNING: Git repository detected in parent directory: %GIT_ROOT%
        echo This will cause issues. Initializing new repository in ceo-personal-os...
        echo.
        REM Remove any existing .git if it's a file (submodule)
        if exist ".git" (
            if not exist ".git\config" (
                del /f /q ".git" 2>nul
            )
        )
        git init
        if errorlevel 1 (
            echo ERROR: Failed to initialize git repository.
            pause
            exit /b 1
        )
        echo Git repository initialized in ceo-personal-os.
        echo.
    )
)

REM Check if remote origin is configured
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo No remote 'origin' configured.
    echo.
    echo Setting up remote to: https://github.com/saad32170/ceobrain
    git remote add origin https://github.com/saad32170/ceobrain.git
    if errorlevel 1 (
        echo ERROR: Failed to add remote origin.
        pause
        exit /b 1
    )
    echo Remote 'origin' added successfully.
    echo.
) else (
    echo Remote 'origin' is already configured.
    git remote get-url origin
    echo.
    REM Update to the correct URL if it's different
    for /f "delims=" %%i in ('git remote get-url origin') do set CURRENT_URL=%%i
    if not "!CURRENT_URL!"=="https://github.com/saad32170/ceobrain.git" (
        echo Updating remote to: https://github.com/saad32170/ceobrain.git
        git remote set-url origin https://github.com/saad32170/ceobrain.git
        echo Remote updated.
    )
    echo.
)

echo ========================================
echo Git setup complete!
echo ========================================
echo.
echo Your repository is ready for auto-commit functionality.
echo When you save or duplicate files, changes will be automatically
echo committed with message "waow" and pushed to origin.
echo.
pause
