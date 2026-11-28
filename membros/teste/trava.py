# -*- coding: utf-8 -*-
"""Trava do teste grátis de 7 dias da MaestrIA.

Só age em computador com licença de TESTE (licenca.json com "teste": true).
Licença paga: não faz nada, nunca.

Roda como gancho do Claude Code, antes de cada pedido com /maestria e antes de
cada ferramenta da MaestrIA. Enquanto o teste vale, deixa passar. Quando o teste
acaba, responde só a mensagem com o link de compra e não deixa a ferramenta rodar.
Quando a pessoa compra, a licença vira paga no servidor e a trava sai sozinha.

Uso:
  python trava.py instalar      grava os ganchos no settings.json (com cópia de segurança)
  python trava.py desinstalar   tira os ganchos
  python trava.py conferir      mostra a situação, sem travar nada
  python trava.py gancho        modo usado pelo Claude Code (lê o evento na entrada)

Envia ao servidor só o código da licença e o nome do computador. Nunca CPF, nunca
documento de cliente.
"""
import json
import os
import platform
import shutil
import socket
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

CHECKIN = "https://xiwjtgyidguhvwpveokz.supabase.co/functions/v1/device-checkin"
CLAUDE = Path(os.environ.get("MAESTRIA_RAIZ_CLAUDE") or (Path.home() / ".claude"))
ESTADO = CLAUDE / "maestria" / "teste" / "estado.json"
SETTINGS = CLAUDE / "settings.json"
CONFERIR_A_CADA = 6 * 3600       # confere no servidor no máximo a cada 6 horas
SEM_INTERNET_ATE = 24 * 3600     # sem conferir por mais de 24 horas, trava
MARCA = "maestria-teste-trava"   # identifica os ganchos desta trava no settings.json
LINK_PADRAO = "https://maestria.samurailab.com.br/"
# As ações que a trava vigia quando o teste acaba. Ler ou rodar um arquivo que não é da MaestrIA passa direto.
MATCHER_FERRAMENTAS = "Skill|SlashCommand|Read|Bash|PowerShell|Glob|Grep|NotebookRead"


def agora():
    return time.time()


def ler_json(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8-sig"))
    except Exception:
        return None


def gravar_json(p, dados):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(p)


def licencas_de_teste():
    """Os licenca.json das ferramentas instaladas (pastas de cópia de segurança ficam de fora)."""
    achadas = []
    if not CLAUDE.is_dir():
        return achadas
    for pasta in CLAUDE.iterdir():
        if not pasta.is_dir() or ".backup-" in pasta.name:
            continue
        lic = pasta / "licenca.json"
        dados = ler_json(lic) if lic.is_file() else None
        if isinstance(dados, dict) and dados.get("teste") is True and dados.get("token"):
            achadas.append((lic, dados))
    return achadas


def consultar(token, versao="trava-teste"):
    # "trava-conferir" é a conferência da instalação: o servidor não liga o relógio dos 7 dias com ela
    # (desde 28/11/2026). "trava-teste" é a pessoa usando a MaestrIA de verdade.
    corpo = json.dumps({"token": token, "hostname": socket.gethostname(),
                        "os_info": platform.platform(), "skill_version": versao}).encode("utf-8")
    pedido = urllib.request.Request(CHECKIN, data=corpo, method="POST",
                                    headers={"Content-Type": "application/json", "User-Agent": "MaestrIA-Teste/1.0"})
    try:
        with urllib.request.urlopen(pedido, timeout=12) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode("utf-8"))
        except Exception:
            return e.code, {}


def mensagem_fim(estado):
    links = (estado or {}).get("links") or {}
    if estado and estado.get("mensagem"):
        return estado["mensagem"]
    combo = links.get("combo") or LINK_PADRAO
    return ("Seu teste de 7 dias da MaestrIA acabou. Para continuar usando, garanta a sua licença aqui: "
            + combo + " . Assim que a compra for aprovada, a MaestrIA volta a funcionar neste computador, "
            "sem instalar nada de novo.")


def tirar_marca_de_teste(licencas):
    for lic, dados in licencas:
        dados.pop("teste", None)
        dados["convertida_em"] = datetime.now(timezone.utc).isoformat()
        gravar_json(lic, dados)


def situacao(forcar=False, versao="trava-teste"):
    """Devolve (pode_usar: bool, mensagem: str | None)."""
    licencas = licencas_de_teste()
    if not licencas:
        return True, None
    token = licencas[0][1]["token"]
    estado = ler_json(ESTADO) or {}
    t = agora()

    # O fim do teste vale mesmo sem internet: a data guardada na última conferência basta.
    vence = estado.get("vence_em_unix")
    if estado.get("situacao") == "expirou" or (vence and t > vence):
        if not forcar and t - estado.get("conferido_em", 0) < 900:
            return False, mensagem_fim(estado)
    elif not forcar and estado.get("situacao") == "ok" and t - estado.get("conferido_em", 0) < CONFERIR_A_CADA:
        return True, None

    try:
        cod, resp = consultar(token, versao)
    except Exception:
        cod, resp = 0, {}

    if cod == 200 and resp.get("ok"):
        if resp.get("teste") is False:
            # Comprou: a licença virou paga no servidor. A trava sai deste computador.
            tirar_marca_de_teste(licencas)
            gravar_json(ESTADO, {"situacao": "convertida", "conferido_em": t})
            return True, None
        vence_em = resp.get("vence_em")
        vence_unix = None
        if vence_em:
            try:
                vence_unix = datetime.fromisoformat(str(vence_em).replace("Z", "+00:00")).timestamp()
            except ValueError:
                vence_unix = None
        gravar_json(ESTADO, {"situacao": "ok", "conferido_em": t, "vence_em_unix": vence_unix,
                             "links": resp.get("links") or estado.get("links") or {}})
        return True, None

    if cod in (403, 404) and (resp.get("teste") or resp.get("erro") in ("licenca vencida", "licenca inativa", "licenca nao encontrada")):
        novo = {"situacao": "expirou", "conferido_em": t, "vence_em_unix": vence,
                "links": resp.get("links") or estado.get("links") or {}, "mensagem": resp.get("mensagem")}
        gravar_json(ESTADO, novo)
        return False, mensagem_fim(novo)

    # Sem resposta do servidor: segura por até 24 horas desde a última conferência boa.
    if estado.get("situacao") == "ok" and t - estado.get("conferido_em", 0) < SEM_INTERNET_ATE and not (vence and t > vence):
        return True, None
    if (vence and t > vence) or estado.get("situacao") == "expirou":
        return False, mensagem_fim(estado)
    return False, ("A MaestrIA em teste precisa de internet para conferir o seu teste. "
                   "Confira a conexão e tente de novo em instantes.")


def eh_da_maestria(evento):
    nome = evento.get("hook_event_name") or ""
    if nome == "UserPromptSubmit":
        texto = str(evento.get("prompt") or "").lower()
        return "maestria" in texto
    if nome == "PreToolUse":
        entrada = evento.get("tool_input") or {}
        # Além da chamada da ferramenta, vale ler os arquivos dela ou rodar os scripts direto (28/11/2026):
        # Read, Bash, PowerShell, Glob e Grep chegam aqui com o caminho em file_path, path, pattern ou command.
        alvo = " ".join(str(entrada.get(k) or "") for k in
                        ("skill", "command", "name", "file_path", "path", "pattern", "notebook_path", "args")).lower()
        alvo = alvo.replace("\\", "/")
        if "maestria" in alvo:
            return True
        # As ferramentas instaladas neste teste, seja qual for a área (cada uma tem a sua pasta com a licença).
        nomes = {"peticao-builder", "calculo-previdenciario", "quesitos-pericia", "briefing-do-caso",
                 "marketing-juridico", "auditor-previdenciario"}
        try:
            nomes.update(lic.parent.name.lower() for lic, _ in licencas_de_teste())
        except Exception:
            pass
        return any(p in alvo for p in nomes)
    return False


def gancho():
    try:
        evento = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        evento = {}
    if not eh_da_maestria(evento):
        return 0
    pode, msg = situacao()
    if pode:
        return 0
    nome = evento.get("hook_event_name")
    if nome == "UserPromptSubmit":
        print(json.dumps({"decision": "block", "reason": msg}, ensure_ascii=False))
    else:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                                 "permissionDecisionReason": msg + " Mostre exatamente esta mensagem ao advogado e não use outra ferramenta da MaestrIA."}},
                         ensure_ascii=False))
    return 0


def comando_do_gancho():
    py = sys.executable or "python3"
    script = Path(__file__).resolve()
    return f'"{py}" "{script}" gancho'


def instalar():
    dados = ler_json(SETTINGS) if SETTINGS.exists() else {}
    if dados is None:
        print("PARADO: o settings.json existe mas não é um JSON válido. Nada foi alterado.")
        return 1
    if SETTINGS.exists():
        copia = SETTINGS.with_name("settings.json.antes-do-teste-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
        shutil.copy2(SETTINGS, copia)
    hooks = dados.setdefault("hooks", {})
    cmd = comando_do_gancho()
    for evento, matcher in (("UserPromptSubmit", None), ("PreToolUse", MATCHER_FERRAMENTAS)):
        lista = [g for g in hooks.get(evento, []) if MARCA not in json.dumps(g)]
        grupo = {"hooks": [{"type": "command", "command": cmd, "timeout": 20, "statusMessage": MARCA}]}
        if matcher:
            grupo = {"matcher": matcher, **grupo}
        lista.append(grupo)
        hooks[evento] = lista
    gravar_json(SETTINGS, dados)
    conferido = ler_json(SETTINGS)
    ok = all(MARCA in json.dumps(conferido["hooks"].get(e, [])) for e in ("UserPromptSubmit", "PreToolUse"))
    print("Trava do teste instalada." if ok else "FALHOU: os ganchos não ficaram gravados.")
    return 0 if ok else 1


def desinstalar():
    dados = ler_json(SETTINGS)
    if not isinstance(dados, dict):
        return 0
    hooks = dados.get("hooks", {})
    for evento in list(hooks):
        hooks[evento] = [g for g in hooks[evento] if MARCA not in json.dumps(g)]
        if not hooks[evento]:
            del hooks[evento]
    if not hooks:
        dados.pop("hooks", None)
    gravar_json(SETTINGS, dados)
    print("Trava do teste retirada.")
    return 0


def main():
    acao = sys.argv[1] if len(sys.argv) > 1 else "conferir"
    if acao == "gancho":
        try:
            return gancho()
        except Exception:
            return 0  # defeito da trava nunca derruba o Claude da pessoa
    if acao == "instalar":
        return instalar()
    if acao == "desinstalar":
        return desinstalar()
    pode, msg = situacao(forcar=True, versao="trava-conferir")
    print(json.dumps({"licenca_de_teste": bool(licencas_de_teste()), "pode_usar": pode, "mensagem": msg}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
