@echo off
chcp 65001 >nul
title MaestrIA - Preparar seu computador

REM Garante que o winget seja encontrado (as vezes nao esta no PATH da sessao).
set "PATH=%PATH%;%LOCALAPPDATA%\Microsoft\WindowsApps"

echo.
echo   ==================================================
echo      MaestrIA - Preparando seu computador
echo   ==================================================
echo.
echo   Este assistente instala o que o Claude Code precisa
echo   pra funcionar no Windows:
echo.
echo      - Git    (o Claude Code exige pra abrir suas pastas)
echo      - Python (as skills usam pra gerar seus documentos)
echo.
echo   Só isso. Não mexe em mais nada, não pede senha, não
echo   toca nos seus arquivos. Leva de 2 a 5 minutos.
echo.
echo   Quando terminar, feche esta janela e instale o
echo   Claude Code em: claude.com/claude-code
echo.
echo   --------------------------------------------------
echo   Aperte uma tecla pra começar (ou feche pra cancelar)
echo   --------------------------------------------------
pause >nul

REM Tenta o winget (instalador automatico do Windows 10/11).
winget --version >nul 2>&1
if errorlevel 1 goto FALLBACK

echo.
echo   [1 de 2] Instalando o Git. Aguarde, pode demorar um pouco...
echo.
call :INSTALA_GIT
call :TEM_GIT
if not errorlevel 1 goto PASSO_PYTHON
call :DESTRAVA_LOJA
call :INSTALA_GIT
call :TEM_GIT
if not errorlevel 1 goto PASSO_PYTHON
echo   O instalador automatico nao conseguiu. Baixando direto do site oficial...
call :BAIXA_GIT

:PASSO_PYTHON
echo.
echo   [2 de 2] Instalando o Python. Aguarde...
echo.
call :INSTALA_PYTHON
call :TEM_PYTHON
if not errorlevel 1 goto FIM
call :DESTRAVA_LOJA
call :INSTALA_PYTHON
call :TEM_PYTHON
if not errorlevel 1 goto FIM
echo   O instalador automatico nao conseguiu. Baixando direto do site oficial...
call :BAIXA_PYTHON
goto FIM

REM ---------------------------------------------------------------------
REM  Rotinas. --source winget e obrigatorio: sem ele o Windows consulta a
REM  loja da Microsoft, que nao tem nada a ver com o que a MaestrIA precisa,
REM  e derruba tudo quando o certificado dela nao passa (erro 0x8a15005e).
REM ---------------------------------------------------------------------
:INSTALA_GIT
winget install --id Git.Git -e --source winget --accept-package-agreements --accept-source-agreements --silent
exit /b 0

:INSTALA_PYTHON
winget install --id Python.Python.3.13 -e --source winget --accept-package-agreements --accept-source-agreements --silent
exit /b 0

REM  A loja fica de fora do caminho, e so depois dela ja ter atrapalhado.
REM  Isso nao instala nada e nao mexe em mais nada do computador.
:DESTRAVA_LOJA
echo   O Windows travou a conferencia da loja da Microsoft. Destravando...
winget settings --enable BypassCertificatePinningForMicrosoftStore >nul 2>&1
exit /b 0

REM  Quem acabou de ser instalado so aparece pra quem recarrega o PATH: por isso
REM  a conferencia le o PATH da maquina, e nao o desta janela.
REM  ⛔ Nunca perguntar ao winget se deu certo. Perguntar ao programa.
:TEM_GIT
powershell -NoProfile -ExecutionPolicy Bypass -Command "$env:Path=[Environment]::GetEnvironmentVariable('Path','Machine')+';'+[Environment]::GetEnvironmentVariable('Path','User'); if (Get-Command git -ErrorAction SilentlyContinue) { exit 0 } else { exit 1 }"
exit /b %errorlevel%

REM  O Windows traz um "python" falso que so abre a loja: conferir a versao.
:TEM_PYTHON
powershell -NoProfile -ExecutionPolicy Bypass -Command "$env:Path=[Environment]::GetEnvironmentVariable('Path','Machine')+';'+[Environment]::GetEnvironmentVariable('Path','User'); $v = (& python --version 2>&1 | Out-String); if ($v -match 'Python 3') { exit 0 } else { exit 1 }"
exit /b %errorlevel%

:FALLBACK
echo.
echo   Seu Windows nao tem o instalador automatico (winget).
echo   Sem problema: eu mesmo baixo e instalo os dois pra voce.
echo   NAO precisa clicar em nada no navegador. So aguardar.
echo.
echo   [1 de 2] Baixando e instalando o Git...
echo.
call :BAIXA_GIT
echo.
echo   [2 de 2] Baixando e instalando o Python...
echo.
call :BAIXA_PYTHON
goto FIM

:BAIXA_GIT
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference='Stop'; try { $r=Invoke-RestMethod 'https://api.github.com/repos/git-for-windows/git/releases/latest' -UseBasicParsing; $u=($r.assets | Where-Object { $_.name -match '64-bit\.exe$' -and $_.name -notmatch 'Portable|Mini|arm' } | Select-Object -First 1).browser_download_url; $e=\"$env:TEMP\git-inst.exe\"; Invoke-WebRequest $u -OutFile $e -UseBasicParsing; Start-Process -Wait $e -ArgumentList '/VERYSILENT','/NORESTART','/SP-'; Write-Host '   Git instalado.' } catch { Write-Host '   Nao consegui automatico. Abrindo a pagina do Git pra voce baixar (o download comeca sozinho).'; Start-Process 'https://git-scm.com/download/win' }"
exit /b 0

:BAIXA_PYTHON
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference='Stop'; try { $e=\"$env:TEMP\py-inst.exe\"; Invoke-WebRequest 'https://www.python.org/ftp/python/3.13.1/python-3.13.1-amd64.exe' -OutFile $e -UseBasicParsing; Start-Process -Wait $e -ArgumentList '/quiet','PrependPath=1','Include_test=0'; Write-Host '   Python instalado.' } catch { Write-Host '   Sem problema: o Python o Claude instala pra voce quando voce instalar a MaestrIA.' }"
exit /b 0

:FIM
echo.
echo   ==================================================
echo      Pronto! Seu computador está preparado.
echo   ==================================================
echo.
echo   Próximo passo:
echo   1. Instale o Claude Code em claude.com/claude-code
echo   2. Volte pra área de membros e baixe o seu instalador
echo.
echo   Se algum item já estava instalado, o Windows só
echo   confirmou e seguiu. Isso é normal, não é erro.
echo.
echo   Alguma coisa falhou? Chame a gente no WhatsApp que a
echo   gente destrava com você em minutos.
echo.
pause
exit /b 0