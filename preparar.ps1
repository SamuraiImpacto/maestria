﻿# =====================================================================
#  MaestrIA | Preparador do computador (Windows)
#  Rota anterior de preparação: confere Git, Claude Code
#  e Python. Feito pra quem nunca mexeu com isso: é só esperar.
#  Samurai Lab | maestria.samurailab.com.br
# =====================================================================

$ErrorActionPreference = "Continue"

function Tem-Comando($nome) {
    try { Get-Command $nome -ErrorAction Stop | Out-Null; return $true } catch { return $false }
}

function Tem-GitReal {
    try {
        $saida = & git --version 2>&1 | Out-String
        return ($LASTEXITCODE -eq 0 -and $saida -match '^git version ')
    } catch { return $false }
}

function Tem-PythonReal {
    # O atalho da Microsoft Store não confirma que o Python está instalado.
    foreach ($nome in @('python', 'python3', 'py')) {
        $programa = Get-Command $nome -ErrorAction SilentlyContinue
        if (-not $programa -or $programa.Source -like '*\Microsoft\WindowsApps\*') { continue }
        try {
            if ($nome -eq 'py') { $saida = & $programa.Source -3 --version 2>&1 | Out-String }
            else { $saida = & $programa.Source --version 2>&1 | Out-String }
            if ($LASTEXITCODE -eq 0 -and $saida -match '^Python 3\.') { return $true }
        } catch {}
    }
    return $false
}

function Recarregar-Caminhos {
    # Programa recém-instalado só aparece pra quem abre um terminal novo. Sem
    # recarregar aqui, a conferência logo abaixo diria "não instalou" mesmo
    # tendo instalado, e mandaria a pessoa pro caminho manual à toa.
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" +
                [System.Environment]::GetEnvironmentVariable("Path", "User")
}

function Instalar-ComWinget($id, $comandoParaConferir, $minutos) {
    # Devolve $true só quando o programa REALMENTE responde depois da instalação.
    # ⛔ Nunca confiar no código de saída do winget: ele volta 0 em situações em
    # que não instalou nada. Quem diz a verdade é o comando existir ou não.
    Write-Host "   Instalando ($minutos)..."
    winget install --id $id -e --source winget --accept-package-agreements --accept-source-agreements
    Recarregar-Caminhos
    if (& $comandoParaConferir) { return $true }

    # Repete pela fonte oficial sem alterar a conferência de certificados.
    winget install --id $id -e --source winget --accept-package-agreements --accept-source-agreements
    Recarregar-Caminhos
    return (& $comandoParaConferir)
}

Write-Host ""
Write-Host "==============================================" -ForegroundColor Red
Write-Host "  MaestrIA | Preparando o seu computador" -ForegroundColor White
Write-Host "==============================================" -ForegroundColor Red
Write-Host ""
Write-Host "Vou conferir e instalar 3 programas de apoio. Pode demorar alguns"
Write-Host "minutos. Você não precisa fazer nada, só acompanhar. Se alguma"
Write-Host "janela pedir permissão, confira a origem e o que será instalado."
Write-Host ""

$temWinget = Tem-Comando "winget"
if (-not $temWinget) {
    Write-Host "[AVISO] Seu Windows está sem o instalador automático (winget)." -ForegroundColor Yellow
    Write-Host "Sem problema: vou abrir as páginas oficiais e te dizer onde clicar."
    Write-Host ""
}

# ---------- 1/3 GIT ----------
Write-Host "[1 de 3] Git (programa de apoio do Claude Code)..." -ForegroundColor Cyan
if (Tem-GitReal) {
    Write-Host "   OK: já está instalado, nada a fazer." -ForegroundColor Green
} elseif ($temWinget -and (Instalar-ComWinget "Git.Git" { Tem-GitReal } "1 a 3 minutos")) {
    Write-Host "   OK: Git instalado." -ForegroundColor Green
} else {
    if ($temWinget) {
        Write-Host "   O instalador automático não conseguiu. Sem problema: dá pra" -ForegroundColor Yellow
        Write-Host "   instalar na mão, e é rápido." -ForegroundColor Yellow
    }
    Write-Host "   Abrindo a página oficial do Git no seu navegador." -ForegroundColor Yellow
    Write-Host "   Lá: clique no botão 'Click here to download', rode o arquivo"
    Write-Host "   baixado, confira as opções e conclua a instalação:"
    Write-Host "   é o site oficial, usado no mundo inteiro."
    Start-Process "https://git-scm.com/download/win"
    Read-Host "   Quando terminar de instalar o Git, volte aqui e aperte Enter"
}

# ---------- 2/3 CLAUDE CODE ----------
Write-Host ""
Write-Host "[2 de 3] Claude Code (onde a MaestrIA roda)..." -ForegroundColor Cyan
if (Tem-Comando "claude") {
    Write-Host "   OK: já está instalado, nada a fazer." -ForegroundColor Green
} else {
    Write-Host "   Instalando pelo instalador oficial da Anthropic (1 a 2 minutos)..."
    try {
        Invoke-RestMethod -Uri "https://claude.ai/install.ps1" -UseBasicParsing | Invoke-Expression
        Recarregar-Caminhos
        $versaoClaude = & claude --version 2>&1 | Out-String
        if ($LASTEXITCODE -eq 0 -and $versaoClaude.Trim()) {
            Write-Host "   OK: Claude Code respondeu à conferência de versão." -ForegroundColor Green
        } else { Write-Host "   Não foi possível confirmar o Claude Code." -ForegroundColor Yellow }
    } catch {
        Write-Host "   [ERRO] A instalação do Claude Code falhou: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "   Tire um print desta tela e mande no grupo da comunidade: "
        Write-Host "   https://chat.whatsapp.com/KQcIy0D6Tp5IWtWY2WXRx7"
    }
}

# ---------- 3/3 PYTHON ----------
Write-Host ""
Write-Host "[3 de 3] Python (motor de cálculo das skills)..." -ForegroundColor Cyan
if (Tem-PythonReal) {
    Write-Host "   OK: já está instalado, nada a fazer." -ForegroundColor Green
} elseif ($temWinget -and (Instalar-ComWinget "Python.Python.3.12" { Tem-PythonReal } "2 a 4 minutos")) {
    Write-Host "   OK: Python instalado." -ForegroundColor Green
} else {
    if ($temWinget) {
        Write-Host "   O instalador automático não conseguiu. Sem problema: dá pra" -ForegroundColor Yellow
        Write-Host "   instalar na mão, e é rápido." -ForegroundColor Yellow
    }
    Write-Host "   Abrindo a página oficial do Python." -ForegroundColor Yellow
    Write-Host "   Clique no botão amarelo 'Download Python', rode o arquivo e,"
    Write-Host "   IMPORTANTE: marque a caixinha 'Add python.exe to PATH' antes"
    Write-Host "   de clicar em Install Now."
    Start-Process "https://www.python.org/downloads/"
    Read-Host "   Quando terminar de instalar o Python, volte aqui e aperte Enter"
}

# ---------- RESUMO ----------
Recarregar-Caminhos
$gitOk = Tem-GitReal
$pyOk = Tem-PythonReal
Write-Host ""
if ($gitOk -and $pyOk) {
    Write-Host "Git e Python responderam corretamente à conferência de versão." -ForegroundColor Green
} else {
    $faltou = @()
    if (-not $gitOk) { $faltou += "Git" }
    if (-not $pyOk) { $faltou += "Python" }
    Write-Host ("Preparação pendente: " + ($faltou -join " e ") + ".") -ForegroundColor Yellow
    Write-Host "Mande um print no grupo, ocultando informações pessoais:"
    Write-Host "https://chat.whatsapp.com/KQcIy0D6Tp5IWtWY2WXRx7"
}
Write-Host ""
Write-Host "Abra novamente o aplicativo Claude, entre em Code e escolha Este computador."
Write-Host "Selecione uma pasta local e siga o vídeo na área de membros."
Write-Host "O aplicativo pode ser baixado em https://claude.ai/download"
Write-Host "Tutorial: https://maestria.samurailab.com.br/instalacao.html"
Write-Host "Quem já usa o terminal pode continuar no Claude Code instalado."
Read-Host "Aperte Enter para fechar esta janela"
if ($gitOk -and $pyOk) { exit 0 } else { exit 1 }
