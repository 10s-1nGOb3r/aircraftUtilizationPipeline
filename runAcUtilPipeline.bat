@echo off
setlocal
title DEBUGGING - Aircraft Utilization Report

set SCRIPT_NAME=acUtilPipeline.py
set VENV_DIR=venv
set INPUT_DIR=input

echo [DEBUG] Checking if Python is accessible...
python --version
if %errorlevel% neq 0 (echo [FAIL] Python not found & pause & exit)

echo [DEBUG] Checking for input file...
if not exist "%INPUT_DIR%\dfsAcUtil.csv" (
    echo [FAIL] MISSING FILE: Place 'dfsAcUtil.csv' in the 'input' folder.
    pause
    exit
)

if not exist "%VENV_DIR%" (
    echo [DEBUG] Creating environment and installing pandas/numpy...
    python -m venv %VENV_DIR%
    call %VENV_DIR%\Scripts\activate
    python -m pip install --upgrade pip
    pip install pandas numpy
) else (
    call %VENV_DIR%\Scripts\activate
)

echo [DEBUG] Starting Python script...
echo ----------------------------------------------------
:: Adding 'python -u' to force unbuffered output (shows errors immediately)
python -u "%SCRIPT_NAME%"
echo ----------------------------------------------------

if %errorlevel% neq 0 (
    echo [ERROR] Python script crashed with exit code %errorlevel%.
) else (
    echo [SUCCESS] Script finished. Check your output folder.
)

pause