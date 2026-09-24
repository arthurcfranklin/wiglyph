#define MyAppName "WiGlyph"
#define MyAppVersion "2.0.0-dev"
#define MyAppPublisher "Arthur Franklin"
#define MyAppExeName "WiGlyph.exe"

[Setup]
AppId={{A8726D16-39F8-4E69-BE85-04B04B754CA7}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={localappdata}\Programs\{#MyAppName}
DefaultGroupName={#MyAppName}

PrivilegesRequired=lowest

OutputDir=..\..\dist\installer
OutputBaseFilename=WiGlyph-2.0.0-dev-windows-x86_64-setup

SetupIconFile=..\..\assets\icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

Compression=lzma2
SolidCompression=yes

WizardStyle=modern

ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

DisableProgramGroupPage=yes
DisableReadyPage=no

CloseApplications=yes
RestartApplications=no
RestartIfNeededByRun=no

Uninstallable=yes

[Files]
Source: "..\..\dist\WiGlyph\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\WiGlyph"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\{#MyAppExeName}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Abrir WiGlyph"; Flags: nowait postinstall skipifsilent
