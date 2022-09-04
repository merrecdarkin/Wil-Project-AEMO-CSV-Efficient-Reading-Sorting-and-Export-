@echo off
del /F /Q ".\AEMOtool.exe"
del /F /Q ".\AEMOtool.spec"
rmdir /S /Q ".\dist"
rmdir /S /Q ".\build"
pyinstaller --onefile --name AEMOtool .\GUI.py
move ".\dist\AEMOtool.exe" .
del /F /Q ".\AEMOtool.spec"
rmdir /S /Q ".\dist"
rmdir /S /Q ".\build"
echo Completed!
@pause