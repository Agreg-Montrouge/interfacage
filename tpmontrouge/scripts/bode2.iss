; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{32DDB0AD-75A3-4AC4-AAA4-D7B72EE191D0}
AppName=TP Montrouge
AppVersion=1.5
;AppVerName=TP Montrouge 1.5
AppPublisher=Ecole Normale Sup�rieure
AppPublisherURL=https://github.com/PrepaAgregMontrouge/interfacage
AppSupportURL=https://github.com/PrepaAgregMontrouge/interfacage
AppUpdatesURL=https://github.com/PrepaAgregMontrouge/interfacage
DefaultDirName={pf}\TP_Montrouge
DisableProgramGroupPage=yes
OutputBaseFilename=setup
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\noms\pierre\tmp\tmp_build\tpmontrouge\scripts\dist\bode2\bode2.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\noms\pierre\tmp\tmp_build\tpmontrouge\scripts\dist\bode2\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{commonprograms}\TP Montrouge"; Filename: "{app}\bode2.exe"
Name: "{commondesktop}\TP Montrouge"; Filename: "{app}\bode2.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\bode2.exe"; Description: "{cm:LaunchProgram,TP Montrouge}"; Flags: nowait postinstall skipifsilent
