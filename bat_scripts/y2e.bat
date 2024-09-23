@echo off

:start
IF "%2"=="" GOTO params1
python %~dp0..\converter.py %1 -s jpy -t eur --%2
GOTO done

:params1
python %~dp0..\converter.py %1 -s jpy -t eur
GOTO done

:done
