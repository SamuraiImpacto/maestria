"""Teste da trava do teste grátis (membros/teste/trava.py), sem mexer no .claude de ninguém.

Parte 1 (sempre): confere, sem internet, quais ações a trava vigia quando o teste acabou.
Parte 2 (com o token do cadastro de mentira "Teste da trava (fictício)", já vencido, em MAESTRIA_TOKEN_TRAVA):
consulta o servidor de verdade e confere a mensagem e o bloqueio.

Uso: python -I _ferramentas/testar_trava_do_teste.py
Português pt-BR. Não imprime token.
"""
import importlib.util
import json
import os
import sys
import tempfile
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
TRAVA = AQUI.parent / "membros" / "teste" / "trava.py"
falhas = []


def carregar(raiz):
    os.environ["MAESTRIA_RAIZ_CLAUDE"] = str(raiz)
    spec = importlib.util.spec_from_file_location("trava", TRAVA)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def checar(nome, ok):
    print(("OK    " if ok else "FALHOU") + " | " + nome)
    if not ok:
        falhas.append(nome)


def pasta_falsa(token):
    raiz = Path(tempfile.mkdtemp(prefix="claude-falso-"))
    for s in ("peticao-builder", "marketing-juridico", "calculo-trabalhista"):
        (raiz / s).mkdir()
        (raiz / s / "licenca.json").write_text(json.dumps({"token": token, "ativo": True, "teste": True}), encoding="utf-8")
    return raiz


# Parte 1: o que a trava vigia
raiz = pasta_falsa("00000000-0000-0000-0000-000000000000")
t = carregar(raiz)
casa = str(raiz).replace("\\", "/")
vigia = [
    ("chamar a ferramenta de petição", {"hook_event_name": "PreToolUse", "tool_name": "Skill", "tool_input": {"skill": "maestria:nova-peticao"}}),
    ("ler o roteiro da petição direto", {"hook_event_name": "PreToolUse", "tool_name": "Read", "tool_input": {"file_path": casa + "/peticao-builder/commands/nova-peticao.md"}}),
    ("ler com barra invertida do Windows", {"hook_event_name": "PreToolUse", "tool_name": "Read", "tool_input": {"file_path": str(raiz) + "\\calculo-trabalhista\\commands\\calcular-he.md"}}),
    ("rodar o script do editor no PowerShell", {"hook_event_name": "PreToolUse", "tool_name": "PowerShell", "tool_input": {"command": "python " + casa + "/marketing-juridico/scripts/editor.py"}}),
    ("procurar arquivos da MaestrIA", {"hook_event_name": "PreToolUse", "tool_name": "Glob", "tool_input": {"pattern": "**/*.md", "path": casa + "/peticao-builder"}}),
    ("digitar /maestria", {"hook_event_name": "UserPromptSubmit", "prompt": "/maestria"}),
]
deixa = [
    ("ler um arquivo do próprio advogado", {"hook_event_name": "PreToolUse", "tool_name": "Read", "tool_input": {"file_path": "C:/Users/fulano/Documents/contrato.docx"}}),
    ("rodar um comando qualquer", {"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": "ls ~/Downloads"}}),
    ("conversar sem falar da MaestrIA", {"hook_event_name": "UserPromptSubmit", "prompt": "me explica o que é tutela de urgência"}),
]
for nome, ev in vigia:
    checar("vigia: " + nome, t.eh_da_maestria(ev))
for nome, ev in deixa:
    checar("deixa passar: " + nome, not t.eh_da_maestria(ev))
checar("instalar grava o gancho com Read, Bash e PowerShell", all(x in t.MATCHER_FERRAMENTAS.split("|") for x in ("Skill", "Read", "Bash", "PowerShell")))

# Parte 2: servidor de verdade, cadastro de mentira vencido
token = os.environ.get("MAESTRIA_TOKEN_TRAVA", "").strip()
if not token:
    print("PULADO | parte 2: sem MAESTRIA_TOKEN_TRAVA")
else:
    raiz = pasta_falsa(token)
    t = carregar(raiz)
    versoes = []
    original = t.consultar
    t.consultar = lambda tok, versao="trava-teste": (versoes.append(versao), original(tok, versao))[1]
    pode, msg = t.situacao(forcar=True, versao="trava-conferir")
    checar("teste vencido: não pode usar", pode is False)
    checar("mensagem fala do que para", bool(msg) and "param" in msg)
    checar("mensagem diz que fica guardado", bool(msg) and "guardados" in msg)
    checar("mensagem traz o link da Kiwify", bool(msg) and "pay.kiwify.com.br" in msg)
    checar("mensagem sem travessão", bool(msg) and "\u2014" not in msg and "\u2013" not in msg)
    checar("conferência manda trava-conferir", versoes == ["trava-conferir"])
    print("\nMENSAGEM QUE O ADVOGADO VÊ:\n" + (msg or ""))

print("\n" + ("TUDO CERTO" if not falhas else f"{len(falhas)} FALHA(S)"))
sys.exit(1 if falhas else 0)
