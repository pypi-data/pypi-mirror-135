@IF EXIST "%~dp0\python.exe" (
  "%~dp0\python.exe"  "%~dp0\grewriting" %*
) ELSE (
  @SETLOCAL
  @SET PATHEXT=%PATHEXT:;.JS;=;%
  python3.exe  "%~dp0\grewriting" %*
)