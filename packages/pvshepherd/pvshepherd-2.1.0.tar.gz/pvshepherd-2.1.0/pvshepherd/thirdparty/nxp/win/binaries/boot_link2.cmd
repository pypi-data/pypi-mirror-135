@echo off
setlocal enabledelayedexpansion
set BootHome=%~d0%~p0
set DeviceName=LPC-Link2
set BootImageWildBridge=LPC432x_CMSIS_DAP_V*.hdr
set BootImageWildNonBridge=LPC432x_CMSIS_DAP_NB_V*.hdr
set BootImageWildSWOBridge=LPC432x_CMSIS_DAP_SWO_V*.hdr
set BootImageWildSerialOnly=LPC432x_CMSIS_DAP_SER_V*.hdr
set BootImageWildCmsisDap=LPC432x_CMSIS_DAP_V*.hdr 
set BootImageWildCmsisDapNonBridge=LPC432x_CMSIS_DAP_NB_V*.hdr
set BootImageWildCmsisDapSerialOnly=LPC432x_CMSIS_DAP_SER_V*.hdr
set DfuLog=%temp%\dfu-util.log

if /i "%1" == "help" goto :Usage

set BootImage=%1
if "%BootImage%" == "" set BootImage=CMSIS
call :getDfuVidPid
if "%DfuVidPid%" == "" goto :NoDfus
if /i "%BootImage%" == "Bridge" call :getBootImage "%BootImageWildBridge%"
if /i "%BootImage%" == "NonBridge" call :getBootImage "%BootImageWildNonBridge%"
if /i "%BootImage%" == "NB" call :getBootImage "%BootImageWildNonBridge%"
if /i "%BootImage%" == "SWO" call :getBootImage "%BootImageWildSWOBridge%"
if /i "%BootImage%" == "SER" call :getBootImage "%BootImageWildSerialOnly%"
if /i "%BootImage%" == "SERIAL" call :getBootImage "%BootImageWildSerialOnly%"
if /i "%BootImage%" == "VCOM" call :getBootImage "%BootImageWildCmsisDapSerialOnly%"
if /i "%BootImage%" == "CMSIS" call :getBootImage "%BootImageWildCmsisDap%"
if /i "%BootImage%" == "CMSISNonBridge" call :getBootImage "%BootImageWildCmsisDapNonBridge%"
if /i "%BootImage%" == "CMSISNB" call :getBootImage "%BootImageWildCmsisDapNonBridge%"
if "%BootImage%" == "" goto :NoBootImage

:DfuApp
for %%i in (%BootImage%) do set ShortBootImage=%%~nxi
echo Booting %DeviceName% with %ShortBootImage%
set boot_options=-d 0x1fc9:c -c 0 -i 0 -t 2048 -R -D %BootImage%

%BootHome%\dfu-util %boot_options% >NUL 2>%DfuLog%
if %errorlevel% equ 0 (
  echo %DeviceName% booted
) else (
  echo %DeviceName% boot failed:
  type %DfuLog%
)
goto :end

:end
endlocal
goto :eof

:NoDfus
echo Nothing to boot!
goto :end

:NoBootImage
echo No boot image found
goto :end

:getDfuVidPid
for /f "skip=6 tokens=3" %%a in ('%BootHome%dfu-util -l') do (
  set DfuVidPid=%%a
)
goto :eof

:getBootImage
set BootImage=
set /a curmajor=0
set /a curminor=0
for /r %BootHome% %%f in (%1) do (
  call :FindNewBootImage %%~nxf
  if not "!NewBootImage!" == "" set BootImage=%%f
)
goto :eof

:FindNewBootImage
set NewBootImage=
for /f "tokens=1,2,3 delims=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_." %%a in ("%1") do set ignore1=%%a&set major=%%b&set minor=%%c
if %major% GTR %curmajor% (
  set /a curmajor=%major%
  set /a curminor=%minor%
  set NewBootImage=%1
  rem echo Major %curmajor% Boot Image %1
) 
if %major% EQU %curmajor% (
  if %minor% GTR %curminor% (
    set /a curminor=%minor%
    set NewBootImage=%1
     rem echo Minor %curminor% Boot Image %1
  )
)
goto :eof

:Usage
echo Usage:
echo %0                       [Boots the default image]
echo %0 Bridge                [Boots the Bridged Probe image]
echo %0 NonBridge             [Boots the Non Bridged Probe image]
echo %0 SWO                   [Boots the SWO Trace Probe image]
echo %0 Serial                [Boots the VCOM Bridged Probe image]
echo %0 CMSIS                 [Boots the CMSIS-DAP Probe image]
goto :end
