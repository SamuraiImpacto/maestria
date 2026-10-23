@echo off
chcp 65001 >nul
setlocal
title MaestrIA - Preparar seu computador
set "PATH=%PATH%;%LOCALAPPDATA%\Microsoft\WindowsApps"
set "FALTOU="
echo.
echo   MaestrIA: preparação do Windows
echo   Este assistente confere Git e Python e instala os que faltarem.
echo   Pode precisar de internet e de autorização do responsável pelo PC.
echo   Ele não instala a MaestrIA: depois você baixa seu pacote na área de membros.
echo.
if /I "%~1"=="/verificar" goto CONFERIR
echo   Aperte uma tecla para começar ou feche esta janela para cancelar.
pause >nul
call :TEM_GIT
if not errorlevel 1 goto PYTHON
winget --version >nul 2>&1
if errorlevel 1 goto SEM_WINGET
echo   Instalando Git pela fonte winget...
winget install --id Git.Git -e --source winget --accept-package-agreements --accept-source-agreements --silent
:PYTHON
call :TEM_PYTHON
if not errorlevel 1 goto PASTA
winget --version >nul 2>&1
if errorlevel 1 goto SEM_WINGET
echo   Instalando Python 3.13 pela fonte winget...
winget install --id Python.Python.3.13 -e --source winget --accept-package-agreements --accept-source-agreements --silent
:PASTA
if exist "%USERPROFILE%\MaestrIA-Arquivos\" goto CONFERIR
mkdir "%USERPROFILE%\MaestrIA-Arquivos"
goto CONFERIR
:SEM_WINGET
echo   O instalador do Windows não está disponível.
echo   Use os instaladores oficiais indicados no guia ou peça ajuda no grupo.
goto CONFERIR
:TEM_GIT
powershell -NoProfile -Command "$env:Path=[Environment]::GetEnvironmentVariable('Path','Machine')+';'+[Environment]::GetEnvironmentVariable('Path','User'); try { $v=(& git --version 2>&1 | Out-String); if($LASTEXITCODE -eq 0 -and $v -match '^git version '){exit 0} } catch {}; exit 1"
exit /b %errorlevel%
:TEM_PYTHON
powershell -NoProfile -Command "$env:Path=[Environment]::GetEnvironmentVariable('Path','Machine')+';'+[Environment]::GetEnvironmentVariable('Path','User'); foreach($n in @('python','python3')) { $c=Get-Command $n -ErrorAction SilentlyContinue; if($c -and $c.Source -notlike '*\Microsoft\WindowsApps\*'){try{$v=(& $c.Source --version 2>&1 | Out-String); if($LASTEXITCODE -eq 0 -and $v -match '^Python 3\.') {exit 0}}catch{}} }; $c=Get-Command py -ErrorAction SilentlyContinue; if($c){try{$v=(& $c.Source -3 --version 2>&1 | Out-String); if($LASTEXITCODE -eq 0 -and $v -match '^Python 3\.') {exit 0}}catch{}}; exit 1"
exit /b %errorlevel%
:CONFERIR
call :TEM_GIT
if errorlevel 1 set "FALTOU=Git"
call :TEM_PYTHON
if errorlevel 1 set "FALTOU=%FALTOU% Python"
if not "%FALTOU%"=="" goto PENDENTE
echo.
echo   Git e Python responderam corretamente à conferência de versão.
echo   Abra novamente o aplicativo Claude, entre em Code e escolha Este computador.
echo   Selecione sua pasta MaestrIA-Arquivos.
echo   Na área de membros, baixe seu instalador e siga o vídeo:
echo   https://maestria.samurailab.com.br/instalacao.html
if /I "%~1"=="/verificar" exit /b 0
pause
exit /b 0
:PENDENTE
echo.
echo   Preparação pendente. Não foi possível confirmar:%FALTOU%
echo   Não desative proteções nem repita a instalação indefinidamente.
echo   Git oficial: https://git-scm.com/download/win
echo   Python oficial: https://www.python.org/downloads/windows/
echo   Mande um print desta mensagem no grupo da comunidade.
echo   Em computador administrado, fale também com o responsável pela máquina.
echo   https://chat.whatsapp.com/KQcIy0D6Tp5IWtWY2WXRx7
if /I "%~1"=="/verificar" exit /b 1
pause
exit /b 1
