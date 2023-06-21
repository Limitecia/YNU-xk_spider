
@echo off

:loop
python "run.py"

IF ERRORLEVEL 1 (
    echo 程序出错，重新启动。
    goto loop
)

echo 程序正常运行结束，将重新运行...
goto loop

:exit
pause
