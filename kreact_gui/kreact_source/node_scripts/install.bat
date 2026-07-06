@echo off
setlocal enabledelayedexpansion

call npm -v >nul 2>&1
if !errorlevel! neq 0 (
    echo NPM is not installed.
    exit /b 1
)
if not exist "node_modules" (
    echo Not a valid Kreact project directory.
    echo This script belongs at the root of a Kreact project
    exit /b 1
)

call npm install %*