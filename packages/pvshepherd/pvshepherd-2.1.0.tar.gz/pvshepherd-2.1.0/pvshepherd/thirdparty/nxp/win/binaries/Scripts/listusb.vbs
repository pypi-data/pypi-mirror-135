Option Explicit
Dim oWMISrv, collDvcs, collUSBDvcs, iUSBDvc , iDvc, sDvcID, sPID, sVID

Function ReplaceX(ByVal sValue, ByVal sPattern, ByVal sNValue)
Dim oReg : Set oReg = New RegExp
oReg.Pattern = sPattern
ReplaceX = oReg.Replace(sValue, sNValue)
Set oReg = Nothing
End Function

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

Set collDvcs = oWMISrv.ExecQuery("Select * From Win32_PnPEntity")

For Each iDvc In collDvcs
  If InStr(iDvc.PNPDeviceID, "VID_") Then ' Except keychain drives
    sDvcID = ReplaceX(iDvc.PNPDeviceID, ".*""(.*)""", "$1")
    sPID = ReplaceX(sDvcID, ".*PID_([^\\\&\+]*).*", "$1")
    sVID = ReplaceX(sDvcID, ".*VID_([^&\+]*).*", "$1")
    Present = false
    if (VersionNum < 10) then ' Prior to Win10 Present field does not exist
      Present = true
    elseif iDvc.Present then
      Present = true
    End If
    if (Present) Then
      Wscript.Echo "VID: " & sVID & " PID: " & sPID & " ("& iDvc.Description & ") " 
    End If
  End If
Next

Set collDvcs = Nothing
Set oWMISrv = Nothing
