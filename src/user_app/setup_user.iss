[Setup]
AppId={{D0208-A63E-4B7C-A5D8-E0F1D1E0C001}}
AppName=Dozorniy Agent
AppVersion=1.0
AppPublisher=HypeHack
DefaultDirName={pf}\DozorniyAgent
DefaultGroupName=Dozorniy
PrivilegesRequired=admin
OutputDir=.
OutputBaseFilename=DozorniyAgent_Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "main.dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "run_user.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "nssm.exe"; DestDir: "{app}"; Flags: ignoreversion

[Code]
var
  ConfigPage: TInputQueryWizardPage;

procedure InitializeWizard;
begin
  ConfigPage := CreateInputQueryPage(wpWelcome,
    'Настройка агента', 'Введите данные для подключения',
    'Эти данные будут использоваться агентом для связи с сервером.');
  ConfigPage.Add('Имя агента:', False);
  ConfigPage.Add('IP сервера:', False);
  ConfigPage.Add('Порт:', False);
  
  ConfigPage.Values[0] := 'Agent_1';
  ConfigPage.Values[1] := '127.0.0.1';
  ConfigPage.Values[2] := '8888';
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  EnvContent: String;
begin
  if CurStep = ssPostInstall then
  begin
    EnvContent := 'AGENT_NAME=' + ConfigPage.Values[0] + #13#10 +
                  'SERVER_HOST=' + ConfigPage.Values[1] + #13#10 +
                  'SERVER_PORT=' + ConfigPage.Values[2] + #13#10 +
                  'VERSION=1.0.0' + #13#10;
    SaveStringToFile(ExpandConstant('{app}\.env'), EnvContent, False);
  end;
end;

[Run]
Filename: "{app}\nssm.exe"; Parameters: "install DozorniyAgent ""{app}\run_user.bat"""; Flags: runhidden
Filename: "{app}\nssm.exe"; Parameters: "set DozorniyAgent AppDirectory ""{app}"""; Flags: runhidden
Filename: "{app}\nssm.exe"; Parameters: "start DozorniyAgent"; Flags: runhidden

[UninstallRun]
Filename: "{app}\nssm.exe"; Parameters: "stop DozorniyAgent"; Flags: runhidden
Filename: "{app}\nssm.exe"; Parameters: "remove DozorniyAgent confirm"; Flags: runhidden
