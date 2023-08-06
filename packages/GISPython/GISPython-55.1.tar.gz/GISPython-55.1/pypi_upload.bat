@echo off

REM Copy GISPython project files to Pip directory
REM echo d | xcopy /f /s /y ..\src GISPython
REM del GISPython\*.pyc

REM Check if directory exists and delete older distributions
IF EXIST dist (
cd dist
del * /S /Q
cd ..
) ELSE (
	mkdir dist
)

REM Create distribution
python setup.py sdist

REM Echo question about publishing on pypi
:choice
set /P c=Publish GISPython package on pypi site?(y/n)
if /I "%c%" EQU "y" goto :movespot
if /I "%c%" EQU "n" goto :exitspot
goto :choice
:movespot
echo Publishing GISPython package to pypi.python.org!

twine upload dist/*

pause
goto :endspot

:exitspot
echo Exiting without publishing!
pause
rem exit

:endspot
echo Done...