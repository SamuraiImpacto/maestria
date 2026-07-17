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
winget install --id Git.Git -e --accept-package-agreements --accept-source-agreements --silent

echo.
echo   [2 de 2] Instalando o Python. Aguarde...
echo.
winget install --id Python.Python.3.13 -e --accept-package-agreements --accept-source-agreements --silent
goto FIM

:FALLBACK
echo.
echo   Seu Windows não tem o instalador automático (winget).
echo   Sem problema: eu mesmo baixo e instalo os dois pra você.
echo   NÃO precisa clicar em nada no navegador. Só aguardar.
echo.
echo   [1 de 2] Baixando e instalando o Git...
echo.
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference='Stop'; try { $r=Invoke-RestMethod 'https://api.github.com/repos/git-for-windows/git/releases/latest' -UseBasicParsing; $u=($r.assets | Where-Object { $_.name -match '64-bit\.exe$' -and $_.name -notmatch 'Portable|Mini|arm' } | Select-Object -First 1).browser_download_url; $e=\"$env:TEMP\git-inst.exe\"; Invoke-WebRequest $u -OutFile $e -UseBasicParsing; Start-Process -Wait $e -ArgumentList '/VERYSILENT','/NORESTART','/SP-'; Write-Host '   Git instalado.' } catch { Write-Host '   Nao consegui automatico. Abrindo a pagina do Git pra voce baixar (o download comeca sozinho).'; Start-Process 'https://git-scm.com/download/win' }"

echo.
echo   [2 de 2] Baixando e instalando o Python...
echo.
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference='Stop'; try { $e=\"$env:TEMP\py-inst.exe\"; Invoke-WebRequest 'https://www.python.org/ftp/python/3.13.1/python-3.13.1-amd64.exe' -OutFile $e -UseBasicParsing; Start-Process -Wait $e -ArgumentList '/quiet','PrependPath=1','Include_test=0'; Write-Host '   Python instalado.' } catch { Write-Host '   Sem problema: o Python o Claude instala pra voce quando voce instalar a MaestrIA.' }"

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