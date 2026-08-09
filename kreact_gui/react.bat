@echo off
setlocal enabledelayedexpansion

set "directory=%~1"
set "project_name=%~2"
if "%directory%" == "" (
    echo Error: Failed to create the project. Please pass in a directory.
    echo Syntax: react $project-directory $project-name[ ...optionals.template: ts ^| react.default]
    exit /b 1
)
if "%project_name%" == "" (
    echo Error: Please pass in a project name.
    echo Syntax: react $project-directory $project-name[ ...optionals.template: ts ^| react.default]
    exit /b 1
)

call npm -v >nul 2>&1
if !errorlevel! neq 0 (
    echo NPM is not installed. Trying to install it.
    set "NODE_LOCAL_SETUP_DIRECTORY=%~dp0kreact_source\node.msi"
    if exist "!NODE_LOCAL_SETUP_DIRECTORY!" (
        echo An installation window will appear
        call "!NODE_LOCAL_SETUP_DIRECTORY!"
    ) else (
        echo Installation started in the background [will likely fail if you don't have an internet access]
        winget install -e --id OpenJS.NodeJS --silent --accept-package-agreements --accept-source-agreements
    )
    set "INSTALL_STATUS=!errorlevel!"
    timeout /t 10
    if !INSTALL_STATUS! neq 0 (
        echo Failed to install Node.js. Please install it manually.
        exit /b !INSTALL_STATUS!
    ) else (
        echo Node.js installed successfully! 
        echo Please restart your terminal to use NPM and run this script again.
        exit /b 0
    )
)

set "template=react"
if "%~3" == "ts" (
    set "template=react-ts"
)

set "TARGET_DIR=%directory%\%project_name%"
if not exist "%TARGET_DIR%" md "%TARGET_DIR%"
if not exist "%TARGET_DIR%" (
    echo Failed to create the project. Couldn't initialize the project directory structure.
    exit /b 1
)

cd /d "%TARGET_DIR%"

echo "y" | call npm create vite@latest . -- --template "%template%"

set "SOURCE_DIR=%~dp0kreact_source"
if not exist "%SOURCE_DIR%" (
    echo Source folder does not exist. Abort.
    exit /b 1
)

xcopy "%SOURCE_DIR%" "src" /s /e /i /q /y /b
if exist "src\node.msi" (
    del "src\node.msi"
)
if exist "src\scripts\" (
    rmdir /s /q "src\scripts\"
)
if exist "src\node_scripts\" (
    rmdir /s /q "src\node_scripts\"
)
if exist "%SOURCE_DIR%\kreact.exe" (
    copy "%SOURCE_DIR%\kreact.exe" "kreact.exe" >nul
)
if exist "%SOURCE_DIR%\scripts" (
    xcopy "%SOURCE_DIR%\scripts" "." /s /e /i /q /y /b
)

call npm install react-router-dom tailwindcss @tailwindcss/vite

if exist "kreact.exe" (
    kreact.exe
)

where code >nul 2>&1
if !errorlevel! neq 0 (
    echo VS Code is not installed. Skipping editor launch.
) else (
    echo Opening in VS Code...
    start "" code .
)
echo Starting development server...

start "" "http://localhost:5173/"
start npm run dev

endlocal