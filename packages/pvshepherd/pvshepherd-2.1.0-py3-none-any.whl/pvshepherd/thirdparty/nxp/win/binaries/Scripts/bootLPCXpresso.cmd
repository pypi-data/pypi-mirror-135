@echo off
setlocal enabledelayedexpansion
set boot_home=%~d0%~p0

call :FindDfu
if "%Dfus%" == "0" goto :NoDfus
if /i "%1" == "" goto :Continue
if /i "%1" == "hid" goto :HID
if /i "%1" == "hidfs" goto :HIDFS
if /i "%1" == "winusb" goto :WinUSB
goto :Usage

:WinUSB
set ROM=LPCXpressoWIN.enc
goto :DfuApp

:HID
set ROM=LPCXpressoHS.enc
goto :DfuApp

:HIDFS
set ROM=LPCXpressoFS.enc
goto :DfuApp

:Continue
setlocal
SET Version=Unknown

VER | FINDSTR /IL "5.0" > NUL
IF %ERRORLEVEL% EQU 0 SET Version=Win2000

VER | FINDSTR /IL "5.1." > NUL
IF %ERRORLEVEL% EQU 0 SET Version=WinXP

VER | FINDSTR /IL "5.2." > NUL
IF %ERRORLEVEL% EQU 0 SET Version=Win2003

VER | FINDSTR /IL "6.0." > NUL
IF %ERRORLEVEL% EQU 0 SET Version=WinVista

VER | FINDSTR /IL "6.1." > NUL
IF %ERRORLEVEL% EQU 0 SET Version=Win7

VER | FINDSTR /IL "6.2." > NUL
IF %ERRORLEVEL% EQU 0 SET Version=Win8

VER | FINDSTR /IL "6.3." > NUL
IF %ERRORLEVEL% EQU 0 SET Version=Win8_1

VER | FINDSTR /IL "10.0." > NUL
IF %ERRORLEVEL% EQU 0 SET Version=Win10

goto :%Version%
:Win2000
:Win2003
:Unknown
echo Not supported on this platform
goto :end

:WinXP
:Win8
:Win8_1
:Win10
set ROM=LPCXpressoWIN.enc
goto :DfuApp
:WinVista
set ROM=LPCXpressoHS.enc
goto :DfuApp
:Win7
set ROM=LPCXpressoHS.enc
goto :DfuApp

:DfuApp
echo Booting LPC-Link with %ROM%
"%BOOT_HOME%\..\dfuapp" /f "%BOOT_HOME%\..\%ROM%" /tl 250 /l dfuapp.log
goto :end

:Usage
echo Usage: %0 [hid/hidfs/winusb]
echo where
echo - hid    = use HID HighSpeed driver
echo - hidfs  = use HID FullSpeed driver
echo - winusb = use WinUSB HighSpeed driver
goto :end

:end
endlocal
goto :eof

:NoDfus
echo Nothing to boot!
goto :end

:FindDfu
:Again
set TempFile=~~%Time: =0%
:: Remove time delimiters
set TempFile=%TempFile::=%
set TempFile=%TempFile:.=%
set TempFile=%TempFile:,=%
:: Create a really large random number and append it to the prefix
for /L %%A IN (0,1,9) do SET TempFile=!TempFile!!Random!
set TempFile=%Temp%.\%TempFile%.vbs
:: If temp file with this name already exists, try again, otherwise create it now
if exist "%TempFile%" (
	goto Again
) else (
	type NUL > "%TempFile%" || set TempFile=
)
:: create a VBScript to look for DFU devices
echo strComputer = "." >> %TempFile%
echo Set objWMIService = GetObject("winmgmts:" ^& _>> %TempFile%
echo "{impersonationLevel=impersonate}!\\" ^& strComputer ^& "\root\cimv2") >> %TempFile%
echo dfus = 0 >> %TempFile%
echo Set colItems = objWMIService.ExecQuery("Select * from Win32_PnPEntity ") >> %TempFile%

echo For Each objItem in colItems >> %TempFile%
  echo if (objItem.Service = "DFU") then >> %TempFile%
    echo dfus = dfus + 1 >> %TempFile%
  echo end if >> %TempFile%

echo Next >> %TempFile%
echo wscript.quit dfus >> %TempFile%
cscript /nologo /b /h:CScript /t:60 %TempFile%
set Dfus=%ErrorLevel%
del %TempFile%
:eof
