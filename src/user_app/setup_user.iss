[Setup]
AppId={{D0208-A63E-4B7C-A5D8-E0F1D1E0C001}}
AppName=Dozorniy Agent
AppVersion=1.0
AppPublisher=HypeHack
DefaultDirName={pf}\DozorniyAgent
DefaultGroupName=Dozorniy
PrivilegesRequired=admin
CreateUninstallRegKey=no
AppendDefaultGroupName=no
OutputDir=.
OutputBaseFilename=DozorniyAgent_Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\user_app\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "run_user.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "silent_run.vbs"; DestDir: "{app}"; Flags: ignoreversion

[Code]
var
  ConfigPage: TInputQueryWizardPage;

procedure InitializeWizard;
begin
  ConfigPage := CreateInputQueryPage(wpWelcome, 'Настройка', 'Введите данные', '');
  ConfigPage.Add('Имя:', False);
  ConfigPage.Add('IP:', False);
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
Filename: "schtasks"; Parameters: "/create /tn ""DozorniyAgent"" /tr ""wscript.exe '{app}\silent_run.vbs' '{app}\run_user.bat'"" /sc onlogon /rl highest /f"; Flags: runhidden
Filename: "schtasks"; Parameters: "/run /tn ""DozorniyAgent"""; Flags: runhidden

[UninstallRun]
Filename: "schtasks"; Parameters: "/delete /tn ""DozorniyAgent"" /f"; Flags: runhidden
