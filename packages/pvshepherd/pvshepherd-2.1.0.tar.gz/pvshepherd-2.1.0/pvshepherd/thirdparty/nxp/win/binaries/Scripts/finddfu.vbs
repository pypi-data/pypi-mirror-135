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
Set objWMIService = GetObject("winmgmts:" _
& "{impersonationLevel=impersonate}!\\" & strComputer & "\root\cimv2")

Set colItems = objWMIService.ExecQuery("Select * from Win32_PnPEntity ")

For Each objItem in colItems
  if (objItem.Service = "DFU") then
    Present = false
    if (VersionNum < 10) then ' Prior to Win10 Present field does not exist
      Present = true
    elseif objItem.Present then
      Present = true
    End If

    if (Present) then
      arrDev = split(objItem.DeviceId, "\") 
      Wscript.Echo "Class GUID: " & objItem.ClassGuid
      Wscript.Echo "Description: " & objItem.Description
      Wscript.Echo "Device ID: " & objItem.DeviceID
      Wscript.Echo "Manufacturer: " & objItem.Manufacturer
      Wscript.Echo "Name: " & objItem.Name
      Wscript.Echo "PNP Device ID: " & objItem.PNPDeviceID
      Wscript.Echo "Service: " & objItem.Service

    end if
  end if

Next

