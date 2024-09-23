@echo off

:start
IF "%2"=="" GOTO params1
python %~dp0..\converter.py %1 -s eur -t jpy --%2
GOTO done

:params1
python %~dp0..\converter.py %1 -s eur -t jpy
GOTO done

:done