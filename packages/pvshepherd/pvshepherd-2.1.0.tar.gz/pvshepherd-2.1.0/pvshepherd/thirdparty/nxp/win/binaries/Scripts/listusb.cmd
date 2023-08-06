@echo off
set BootHome=%~d0%~p0
cscript /nologo %BootHome%\listusb.vbs | sort
