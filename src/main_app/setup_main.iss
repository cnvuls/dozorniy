[Setup]
AppId={{D0208-A63E-4B7C-A5D8-E0F1D1E0C002}}
AppName=Dozorniy Server
AppVersion=1.0
AppPublisher=HypeHack
DefaultDirName={pf}\DozorniyServer
DefaultGroupName=Dozorniy
PrivilegesRequired=admin
OutputDir=.
OutputBaseFilename=DozorniyServer_Setup
Compression=lzma
SolidCompression=yes

[Dirs]
Name: "{app}"; Permissions: users-full

[Files]
Source: "dist\main_app\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\updater.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Dozorniy Server"; Filename: "{app}\main_app.exe"
Name: "{commondesktop}\Dozorniy Server"; Filename: "{app}\main_app.exe"
Name: "{group}\Update Server"; Filename: "{app}\updater.exe"

[Run]
Filename: "{app}\main_app.exe"; Description: "Запустить Dozorniy Server"; Flags: nowait postinstall skipifsilent
