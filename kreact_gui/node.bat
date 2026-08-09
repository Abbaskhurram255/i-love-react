@echo off
setlocal enabledelayedexpansion

set "directory=%~1"
set "project_name=%~2"
set "TARGET_DIR=%directory%\%project_name%"
set "INDEX_JS=index.js"

if "%directory%" == "" (
    echo Error: Failed to create the project. Please pass in a directory.
    echo Syntax: %~nx0 $project-directory $project-name
    exit /b 1
)
if "%project_name%" == "" (
    echo Error: Please pass in a project name.
    echo Syntax: %~nx0 $project-directory $project-name
    exit /b 1
)

call npm -v >nul 2>&1
if !errorlevel! neq 0 (
    echo NPM is not installed. Trying to install it...
    set "NODE_LOCAL_SETUP_DIRECTORY=%~dp0kreact_source\node.msi"
    if exist "!NODE_LOCAL_SETUP_DIRECTORY!" (
        echo An installation window will appear.
        call "!NODE_LOCAL_SETUP_DIRECTORY!"
    ) else (
        echo Installation started in the background [Requires Internet Access]
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

if not exist "%TARGET_DIR%" md "%TARGET_DIR%"
if not exist "%TARGET_DIR%" (
    echo Failed to create the project. Couldn't initialize the project directory structure.
    exit /b 1
)

cd /d "%TARGET_DIR%"
if not exist "package.json" (
    call npm init -y
)
call npm i express cors helmet compression
call npm i --save-dev dotenv nodemon

set "SOURCE_DIR=%~dp0kreact_source"
if exist "%SOURCE_DIR%" (
    xcopy "%SOURCE_DIR%" "%TARGET_DIR%" /s /e /i /q /y /b
    if exist "%TARGET_DIR%\node.msi" del "%TARGET_DIR%\node.msi"
    if exist "%TARGET_DIR%\scripts\" rmdir /s /q "%TARGET_DIR%\scripts\"
    if exist "%TARGET_DIR%\node_scripts\" rmdir /s /q "%TARGET_DIR%\node_scripts\"
    if exist "%SOURCE_DIR%\kreact.exe" copy "%SOURCE_DIR%\kreact.exe" "%TARGET_DIR%\kreact.exe" >nul
    if exist "%SOURCE_DIR%\node_scripts" xcopy "%SOURCE_DIR%\node_scripts" "%TARGET_DIR%" /s /e /i /q /y /b
)

call npm install
if exist "kreact.exe" (
    call kreact.exe
)

where code >nul 2>&1
if !errorlevel! neq 0 (
    echo VS Code is not installed. Skipping editor launch.
) else (
    echo Opening in VS Code...
    start "" code .
)

echo Starting development server...
if exist "kreact.exe" (
    call kreact.exe
)
start "" "http://localhost:3001/"
start npx nodemon "%INDEX_JS%"

endlocal