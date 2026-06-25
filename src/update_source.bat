@echo off
set "NEW_SOURCE_DIR=..\kreact_source"
if not exist "%NEW_SOURCE_DIR%" md "%NEW_SOURCE_DIR%"
for %%f in (*.exe *.py) do copy /y "%%f" "%NEW_SOURCE_DIR%"
if exist "pyport" xcopy "pyport" "%NEW_SOURCE_DIR%\pyport\" /s /e /i /y
if exist "scripts" xcopy "scripts" "%NEW_SOURCE_DIR%\scripts\" /s /e /i /y
if exist "node_scripts" xcopy "node_scripts" "%NEW_SOURCE_DIR%\node_scripts\" /s /e /i /y