Dim colOperatingSystems
Dim objOperatingSystem
Dim Version
Dim VersionNum
Dim Present

Set oWMISrv = GetObject("winmgmts:\\.\root\cimv2")
Set colOperatingSystems = oWMISrv.ExecQuery("Select * from Win32_OperatingSystem")
For Each objOperatingSystem in colOperatingSystems
    Version = Mid(objOperatingSystem.Version, 1, 2)
    Version = Replace(Version, ".", "")
    VersionNum = CInt(Version)
Next

strComputer = "."
set objWMIService = GetObject("winmgmts:" _
& "{impersonationLevel=impersonate}!\\" & strComputer & "\root\cimv2")

set colItems = objWMIService.ExecQuery("Select * from Win32_PnPEntity" )

for each objItem in colItems
    Present = false
    if (VersionNum < 10) then ' Prior to Win10 Present field does not exist
      Present = true
    elseif iDvc.Present then
      Present = true
    End If

  if (Present) then
    arrDev = split(objItem.DeviceId, "\")
    if (arrDev(0) = "HID") then
      Wscript.Echo "Class GUID: " & objItem.ClassGuid
      Wscript.Echo "Description: " & objItem.Description
      Wscript.Echo "Device ID: " & objItem.DeviceID
      Wscript.Echo "Manufacturer: " & objItem.Manufacturer
      Wscript.Echo "Name: " & objItem.Name
      Wscript.Echo "PNP Device ID: " & objItem.PNPDeviceID
      Wscript.Echo "Service: " & objItem.Service

    end if
  end if
next

