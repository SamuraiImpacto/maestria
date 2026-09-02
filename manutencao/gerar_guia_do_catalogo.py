# -*- coding: utf-8 -*-
"""
Gera membros/guia-skills.js a partir dos ZIPs PUBLICADOS no catalogo.

Por que existe: o gerador antigo (peticao-builder/manutencao/pipeline-lote/gerar_guia.py)
lia da Master Copy, e a Master Copy pode estar atrasada em relacao ao que esta no ar.
A regra de release da MaestrIA e clara: a base e SEMPRE o ZIP publicado
(skill_catalog.zip_url), nunca a pasta local.

Uso:
    python manutencao/gerar_guia_do_catalogo.py

Depois de rodar, BUMPAR o ?v= de guia-skills.js em membros/index.html,
senao o navegador serve a versao em cache e a atualizacao nao chega em ninguem.
"""
import io, os, re, sys, json, glob, zipfile, urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = os.path.join(RAIZ, "membros", "guia-skills.js")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_cache_zips")

# comandos padronizados: aparecem UMA vez nos blocos fixos do app.js, nunca por skill
COMUNS = {"ativar-licenca", "atualizar-skill", "minha-licenca", "suporte",
          "listar-comandos", "menu", "atualizar-dados", "abrir",
          "configurar-pastas", "setup-rapido", "listar-casos", "economia",
          "editar-estilo", "ver-insights", "consultar-juizo",
          "contribuir-decisao", "conselheiro", "mesa"}

TRADUCOES = [
    ("em Markdown e .docx", "em Word"),
    ("Gera Markdown + Word ao final", "Gera o documento em Word ao final"),
    ("em Word (.docx)", "em Word"),
    (" (.docx)", " (Word)"),
    (".docx", "Word"),
    ("Markdown", "texto"),
    ("engine Python", "motor de cálculo embarcado"),
    ("data/indices.json", "o banco de índices da skill"),
    ("grava em o banco", "guarda no banco"),
    ("API SGS do Banco Central", "sistema oficial do Banco Central"),
    (" (MCP)", ""),
    ("MCP", "conector oficial"),
    ("AskUserQuestion", "perguntas com botões"),
    ("push pro repo central", "envio pro cofre central de modelos"),
    ("repo central", "cofre central de modelos"),
    ("frontmatter", "cabeçalho"),
    ("JSON", "arquivo de configuração"),
]


def traduzir(t):
    for de, para in TRADUCOES:
        t = t.replace(de, para)
    return re.sub(r"\s{2,}", " ", t).strip()


def carregar_env():
    env = {}
    caminho = glob.glob(os.path.expanduser("~/.samurai/maestria-core.env"))
    if not caminho:
        raise SystemExit("cofre nao encontrado: ~/.samurai/maestria-core.env")
    for linha in io.open(caminho[0], encoding="utf-8"):
        linha = linha.strip()
        if linha and not linha.startswith("#") and "=" in linha:
            k, v = linha.split("=", 1)
            env[k.replace("export ", "").strip()] = v.strip().strip('"').strip("'")
    return env


def catalogo(env):
    req = urllib.request.Request(
        env["SUPABASE_URL"] + "/rest/v1/skill_catalog?select=skill_id,versao_atual,zip_url&order=skill_id",
        headers={"apikey": env["SUPABASE_SERVICE_ROLE_KEY"],
                 "Authorization": "Bearer " + env["SUPABASE_SERVICE_ROLE_KEY"]})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode("utf-8"))


def descricao(texto):
    m = re.search(r"^---\s*\n(.*?)\n---", texto, re.DOTALL)
    if not m:
        return None
    d = re.search(r"description:\s*(.+)", m.group(1))
    if not d:
        return None
    desc = traduzir(d.group(1).strip().strip('"').strip("'"))
    if len(desc) > 300:
        corte = desc.rfind(". ", 0, 300)
        desc = desc[:corte + 1] if corte > 80 else desc[:297] + "..."
    if not desc.endswith("."):
        desc += "."
    return desc if len(desc) > 8 else None


def main():
    env = carregar_env()
    skills = catalogo(env)
    os.makedirs(CACHE, exist_ok=True)
    guia, avisos = {}, []

    for s in skills:
        sid, ver = s["skill_id"], s["versao_atual"]
        destino = os.path.join(CACHE, "%s-%s.zip" % (sid, ver))
        if not os.path.exists(destino):
            urllib.request.urlretrieve(s["zip_url"], destino)
        z = zipfile.ZipFile(destino)
        funcoes = []
        for nome in sorted(z.namelist()):
            if "/skill/commands/" not in nome or not nome.endswith(".md"):
                continue
            cmd = os.path.basename(nome)[:-3]
            if cmd in COMUNS:
                continue
            d = descricao(z.read(nome).decode("utf-8", "replace")[:3000])
            if not d:
                avisos.append("%s: %s sem description utilizavel" % (sid, cmd))
                continue
            funcoes.append({"c": cmd, "d": d})
        if funcoes:
            guia[sid] = {"funcoes": funcoes}

    # peticao-builder primeiro, como no guia anterior
    ordenado = {}
    if "peticao-builder" in guia:
        ordenado["peticao-builder"] = guia.pop("peticao-builder")
    for k in sorted(guia):
        ordenado[k] = guia[k]

    total = sum(len(v["funcoes"]) for v in ordenado.values())
    print("skills no guia: %d | funcoes especificas: %d" % (len(ordenado), total))
    for k, v in ordenado.items():
        print("  %-34s %d" % (k, len(v["funcoes"])))
    for a in avisos:
        print("  AVISO:", a)

    proibidos = [".docx", "Markdown", "frontmatter", "MCP", "Python", "engine"]
    texto = json.dumps(ordenado, ensure_ascii=False)
    vazou = [t for t in proibidos if t in texto]
    if vazou:
        print("ATENCAO tecniques remanescentes:", vazou)
    if "—" in texto or "–" in texto:
        raise SystemExit("ERRO: travessao no guia. Corrigir a description da skill de origem.")

    js = ("// Gerado automaticamente a partir dos ZIPs PUBLICADOS no catalogo (nao editar a mao).\n"
          "// Regenerar: python manutencao/gerar_guia_do_catalogo.py\n"
          "// Depois de regenerar, BUMPAR o ?v= de guia-skills.js em membros/index.html.\n"
          "window.MAESTRIA_GUIA = " + json.dumps(ordenado, ensure_ascii=False, indent=1) + ";\n")
    with io.open(SAIDA, "w", encoding="utf-8", newline="\n") as f:
        f.write(js)
    print("\ngravado: %s (%.0f KB)" % (SAIDA, os.path.getsize(SAIDA) / 1024))


if __name__ == "__main__":
    main()
