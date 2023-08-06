@echo off
set BootHome=%~d0%~p0
echo Tasks:
tasklist /svc
echo USB Devices:
cscript /nologo %BootHome%\listusb.vbs
echo DFU Devices:
cscript /nologo %BootHome%\finddfu.vbs
echo HID Devices:
cscript /nologo %BootHome%\findhid.vbs

