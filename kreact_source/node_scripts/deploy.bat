@echo off
SETLOCAL EnableDelayedExpansion

: replace these variables with your own login data
SET "VERCEL_TOKEN="
SET "VERCEL_ORG_ID="
SET "VERCEL_PROJECT_ID="

if "%VERCEL_TOKEN%" == "" (
    echo [ERROR] Vercel token is missing.
    goto :fail
)
if "%VERCEL_ORG_ID%" == "" (
    echo [ERROR] Vercel organization ID is missing.
    goto :fail
)
if "%VERCEL_PROJECT_ID%" == "" (
    echo [ERROR] Vercel project ID is missing.
    goto :fail
)

call npm -v >nul 2>&1
if !ERRORLEVEL! neq 0 (
    echo [ERROR] Node.js/NPM is not installed or not in system PATH.
    goto :fail
)

echo Checking for Vercel CLI...
call npm list vercel --depth=0 >nul 2>&1
if !ERRORLEVEL! neq 0 (
    echo Vercel not found. Installing locally...
    call npm install vercel --no-save
    if !ERRORLEVEL! neq 0 (
        echo [ERROR] Failed to install Vercel CLI via npm.
        goto :fail
    )
)

echo Deploying Node app directly to production...
call npx vercel --prod --yes --token=%VERCEL_TOKEN%
if !ERRORLEVEL! neq 0 (
    echo [ERROR] Vercel deployment failed. Check logs above.
    goto :fail
)

echo [SUCCESS] Deployment completed!
pause
ENDLOCAL
exit /b 0

:fail
echo [FAILURE] Script aborted due to an error.
pause
ENDLOCAL
exit /b 1
