# =====================================================================
#  MaestrIA | Preparador do computador (Windows)
#  Instala sozinho tudo o que o Claude Code precisa: Git, Claude Code
#  e Python. Feito pra quem nunca mexeu com isso: é só esperar.
#  Samurai Lab | maestria.samurailab.com.br
# =====================================================================

$ErrorActionPreference = "Continue"

function Tem-Comando($nome) {
    try { Get-Command $nome -ErrorAction Stop | Out-Null; return $true } catch { return $false }
}

function Tem-PythonReal {
    # o Windows traz um "python" falso que abre a loja; conferir a versão de verdade
    try {
        $saida = & python --version 2>&1 | Out-String
        return ($saida -match "Python 3")
    } catch { return $false }
}

function Recarregar-Caminhos {
    # Programa recém-instalado só aparece pra quem abre um terminal novo. Sem
    # recarregar aqui, a conferência logo abaixo diria "não instalou" mesmo
    # tendo instalado, e mandaria a pessoa pro caminho manual à toa.
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" +
                [System.Environment]::GetEnvironmentVariable("Path", "User")
}

function Destravar-LojaDaMicrosoft {
    # ⛔ O winget confere o certificado da loja da Microsoft antes de instalar
    # QUALQUER coisa, mesmo o que não vem da loja. Quando um antivírus ou a rede
    # da empresa inspeciona o tráfego, essa conferência falha com o código
    # 0x8a15005e e derruba a instalação inteira. Aconteceu com uma cliente em
    # 07/09/2026: o preparador dizia "OK, instalado" e nada tinha sido instalado.
    #
    # A MaestrIA não usa a loja em nada: Git e Python vêm da fonte "winget".
    # Então desligamos só essa conferência, e só depois dela já ter atrapalhado.
    Write-Host "   O Windows travou a conferência da loja da Microsoft. Destravando..." -ForegroundColor Yellow
    winget settings --enable BypassCertificatePinningForMicrosoftStore 2>&1 | Out-Null
}

function Instalar-ComWinget($id, $comandoParaConferir, $minutos) {
    # Devolve $true só quando o programa REALMENTE responde depois da instalação.
    # ⛔ Nunca confiar no código de saída do winget: ele volta 0 em situações em
    # que não instalou nada. Quem diz a verdade é o comando existir ou não.
    Write-Host "   Instalando ($minutos)..."
    winget install --id $id -e --source winget --accept-package-agreements --accept-source-agreements
    Recarregar-Caminhos
    if (& $comandoParaConferir) { return $true }

    # Segunda e última tentativa, agora sem a trava da loja no caminho.
    Destravar-LojaDaMicrosoft
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
Write-Host "janela do Windows pedir permissão, clique em SIM."
Write-Host ""

$temWinget = Tem-Comando "winget"
if (-not $temWinget) {
    Write-Host "[AVISO] Seu Windows está sem o instalador automático (winget)." -ForegroundColor Yellow
    Write-Host "Sem problema: vou abrir as páginas oficiais e te dizer onde clicar."
    Write-Host ""
}

# ---------- 1/3 GIT ----------
Write-Host "[1 de 3] Git (programa de apoio do Claude Code)..." -ForegroundColor Cyan
if (Tem-Comando "git") {
    Write-Host "   OK: já está instalado, nada a fazer." -ForegroundColor Green
} elseif ($temWinget -and (Instalar-ComWinget "Git.Git" { Tem-Comando "git" } "1 a 3 minutos")) {
    Write-Host "   OK: Git instalado." -ForegroundColor Green
} else {
    if ($temWinget) {
        Write-Host "   O instalador automático não conseguiu. Sem problema: dá pra" -ForegroundColor Yellow
        Write-Host "   instalar na mão, e é rápido." -ForegroundColor Yellow
    }
    Write-Host "   Abrindo a página oficial do Git no seu navegador." -ForegroundColor Yellow
    Write-Host "   Lá: clique no botão 'Click here to download', rode o arquivo"
    Write-Host "   baixado e vá clicando Next em tudo até o final. Pode confiar:"
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
        Write-Host "   OK: Claude Code instalado." -ForegroundColor Green
    } catch {
        Write-Host "   [ERRO] A instalação do Claude Code falhou: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "   Tire uma foto desta tela e mande pro suporte: maestria.samurailab.com.br/suporte.html"
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
Write-Host ""
Write-Host "==============================================" -ForegroundColor Red
Write-Host "  PRONTO! Próximos passos (2 minutos):" -ForegroundColor White
Write-Host "==============================================" -ForegroundColor Red
Write-Host ""
Write-Host "  1. FECHE esta janela e abra o PowerShell DE NOVO" -ForegroundColor White
Write-Host "     (menu Iniciar, digite powershell, Enter)."
Write-Host "  2. Digite: claude   e aperte Enter." -ForegroundColor White
Write-Host "     O navegador abre pedindo login: entre com a conta da sua"
Write-Host "     assinatura do Claude e autorize."
Write-Host "  3. Volte ao manual de instalação da MaestrIA e siga do passo 4:" -ForegroundColor White
Write-Host "     maestria.samurailab.com.br/instalacao.html"
Write-Host ""
Read-Host "Aperte Enter para fechar esta janela"
