
@echo off

:loop
python "run.py"

IF ERRORLEVEL 1 (
    echo �����������������
    goto loop
)

echo �����������н���������������...
goto loop

:exit
pause
