@echo off
echo Compiling...
copy "_translate.py" "pyport\_translate.py"
copy "KL_Py.py" "pyport\KL_Py.py"
call "pyport\python.exe" "kreact_python.py"
echo Done.