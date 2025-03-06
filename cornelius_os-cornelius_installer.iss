cornelius_os/cornelius_installer.iss
#define MyAppName "Cornelius"
#define MyAppVersion "0.1"
#define MyAppPublisher "Your Name/Organization"
#define MyAppURL "https://www.example.com/cornelius" ; Replace with your project's URL
#define MyAppExeName "cornelius.exe" ; Change if your executable name is different
#define MyAppId "{YOUR-NEW-GUID-HERE}" ; Replace this with your own GUID
[Setup]
#define OutputDir "dist"
; (To generate a new GUID, click Tools | Generate GUID inside Inno Setup.)
AppId={#MyAppId} ; Use the defined GUID
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
OutputDir=.\dist
OutputBaseFilename=cornelius_installer
SetupIconFile=.\cornelius_icon.ico ; Optional: Replace with an icon file
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: ".\dist\cornelius\cornelius.exe"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files
Source: ".\cornelius_log.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\knowledge_base.json"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
