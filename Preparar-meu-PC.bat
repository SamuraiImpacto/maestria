@echo off
chcp 65001 >nul
title MaestrIA - Preparar seu computador

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
echo   toca nos seus arquivos. Leva de 2 a 3 minutos.
echo.
echo   Quando terminar, feche esta janela e instale o
echo   Claude Code em: claude.com/claude-code
echo.
echo   --------------------------------------------------
echo   Aperte uma tecla pra começar (ou feche pra cancelar)
echo   --------------------------------------------------
pause >nul

REM O winget é o instalador automático do Windows 10 e 11.
where winget >nul 2>&1
if errorlevel 1 goto SEM_WINGET

echo.
echo   [1 de 2] Instalando o Git. Aguarde, pode demorar um pouco...
echo.
winget install --id Git.Git -e --accept-package-agreements --accept-source-agreements --silent

echo.
echo   [2 de 2] Instalando o Python. Aguarde...
echo.
winget install --id Python.Python.3.13 -e --accept-package-agreements --accept-source-agreements --silent

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

:SEM_WINGET
echo.
echo   Seu Windows não tem o instalador automático (winget).
echo   Sem problema: vou abrir as duas páginas oficiais pra
echo   você baixar na mão. Em cada uma, é só next-next-finish.
echo.
echo   Abrindo a página do Git...
start "" "https://git-scm.com/download/win"
timeout /t 2 >nul
echo   Abrindo a página do Python...
start "" "https://www.python.org/downloads/"
echo.
echo   Depois de instalar os dois, instale o Claude Code em
echo   claude.com/claude-code e volte pra área de membros.
echo.
pause
exit /b 0
