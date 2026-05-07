@echo off
call npm -v >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo NPM is not installed. Please install Node.js.
    goto :EOF
)
echo Building the React app into the '/dist' folder...
call npm run build