"""Fabrique les guides du site (src/guides/) à partir des modes d'emploi des dépôts des apps.

    pip install markdown pillow
    python tools/build-guides.py all                 # les 4 apps, dépôts voisins du site (../bandua, ...)
    python tools/build-guides.py bandua              # une seule app
    python tools/build-guides.py lugus ../lugus-transfer
    python tools/build-guides.py all --all-images    # reconvertit aussi les images déjà faites

Chaque mode d'emploi s'écrit dans le dépôt de son app (docs/GUIDE.md, GUIDE.fr.md, GUIDE.es.md),
qui reste la seule source. Le script en tire, pour chaque langue, un fichier src/guides/<app>.<langue>.html
(sommaire + article) et convertit les captures en WebP dans public/<app>/guide/img/.
Les couleurs, descriptions et titres de page se règlent dans src/lib/apps.ts.
Ensuite : npm run dev pour vérifier, puis git commit et npm run deploy.
"""
import html, pathlib, re, sys
import markdown
from PIL import Image

SITE = pathlib.Path(__file__).resolve().parents[1]
APPS = {
    "bandua": dict(name="Bandua", repo="bandua", icon="bandua-icon.png",
                   sub={"en": "Version 0.3.0 (beta) · Windows and macOS", "fr": "Version 0.3.0 (bêta) · Windows et macOS", "es": "Versión 0.3.0 (beta) · Windows y macOS"},
                   title={"en": "Bandua user guide", "fr": "Bandua, mode d'emploi", "es": "Bandua, manual de uso"}),
    "companion": dict(name="Bandua MHL Companion", repo="bandua-mhl-companion", icon="companion-icon.png",
                   sub={"en": "Version 0.2.0 · Windows and macOS", "fr": "Version 0.2.0 · Windows et macOS", "es": "Versión 0.2.0 · Windows y macOS"},
                   title={"en": "Bandua MHL Companion user guide", "fr": "Bandua MHL Companion, mode d'emploi", "es": "Bandua MHL Companion, manual de uso"}),
    "lugus": dict(name="Lugus Transfer", repo="lugus-transfer", icon="lugus-icon.png",
                   sub={"en": "Version 0.3.0 (beta) · Windows and macOS", "fr": "Version 0.3.0 (bêta) · Windows et macOS", "es": "Versión 0.3.0 (beta) · Windows y macOS"},
                   title={"en": "Lugus Transfer user guide", "fr": "Lugus Transfer, mode d'emploi", "es": "Lugus Transfer, manual de uso"}),
    "ataecina": dict(name="Ataecina", repo="ataecina", icon="ataecina-icon.png",
                   sub={"en": "Beta 0.11.5 · Windows", "fr": "Version bêta 0.11.5 · Windows", "es": "Beta 0.11.5 · Windows"},
                   title={"en": "Ataecina user guide", "fr": "Ataecina, mode d'emploi", "es": "Ataecina, manual de uso"}),
}
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
ALL_IMAGES = "--all-images" in sys.argv
KEY = ARGS[0] if ARGS else "all"
if KEY != "all" and KEY not in APPS:
    sys.exit(f"Application inconnue : {KEY} (choix : all, {', '.join(APPS)})")
APP = APPS.get(KEY, APPS["bandua"])
SRC = pathlib.Path(ARGS[1]).resolve() if len(ARGS) > 1 else SITE.parent / APP["repo"]
OUT = SITE / "src" / "guides"
IMG = SITE / "public" / KEY / "guide" / "img"
LANGS = {"en": "GUIDE.md", "fr": "GUIDE.fr.md", "es": "GUIDE.es.md"}
N = APP["name"]
UI = {
    "en": dict(title=APP["title"]["en"], sub=APP["sub"]["en"], toc="Contents", back=f"Back to {N}",
               dl=f"Download {N}", md="This guide on GitHub", close="Close", zoom="Click an image to enlarge it."),
    "fr": dict(title=APP["title"]["fr"], sub=APP["sub"]["fr"], toc="Sommaire", back=f"Retour à {N}",
               dl=f"Télécharger {N}", md="Ce guide sur GitHub", close="Fermer", zoom="Cliquez sur une image pour l'agrandir."),
    "es": dict(title=APP["title"]["es"], sub=APP["sub"]["es"], toc="Índice", back=f"Volver a {N}",
               dl=f"Descargar {N}", md="Esta guía en GitHub", close="Cerrar", zoom="Haz clic en una imagen para ampliarla."),
}
GH = f"https://github.com/tetsujin28/{APP['repo']}/blob/main/docs/"

def convert_images():
    IMG.mkdir(parents=True, exist_ok=True)
    n = 0
    for p in sorted((SRC / "docs" / "guide").glob("*.png")):
        dest = IMG / (p.stem + ".webp")
        if ALL_IMAGES or not dest.exists() or dest.stat().st_mtime < p.stat().st_mtime:
            Image.open(p).convert("RGB").save(dest, "WEBP", quality=88, method=6)
            n += 1
    print(f"  images converties : {n}")

def body(lang):
    src = (SRC / "docs" / LANGS[lang]).read_text(encoding="utf-8")
    # retire l'en-tête HTML (logo, titre, langues) et le sommaire ; garde un éventuel encadré d'avertissement
    lines = src.split("\n")
    i = 0
    while i < len(lines) and (lines[i].startswith("<") or lines[i].startswith("  <") or not lines[i].strip()):
        i += 1
    src = "\n".join(lines[i:])
    a = src.index("\n## ") if not src.startswith("## ") else 0
    b = src.index("\n## ", a + 4)
    src = src[:a] + src[b:]
    src = src.replace("../LICENSE", f"https://github.com/tetsujin28/{APP['repo']}/blob/main/LICENSE")
    out = markdown.markdown(src, extensions=["tables", "fenced_code"])
    toc = []
    def h2(m):
        n = len(toc) + 1
        toc.append((f"{lang}-{n}", re.sub(r"<[^>]+>", "", m.group(1))))
        return f'<h2 id="{lang}-{n}">{m.group(1)}</h2>'
    out = re.sub(r"<h2>(.*?)</h2>", h2, out)
    out = re.sub(r'<p align="center"><img src="guide/([^"]+)\.png" width="(\d+)" alt="([^"]*)"></p>',
                 lambda m: f'<figure class="shot w{m.group(2)}"><img src="/{KEY}/guide/img/{m.group(1)}.webp" alt="{m.group(3)}" loading="lazy"></figure>', out)
    out = out.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    out = re.sub(r"<blockquote>\s*<p><strong>⚠", '<blockquote class="alert">\n<p><strong>⚠', out)
    # ancres internes du markdown (#3-installer-...) vers les ancres de la page (#fr-3)
    out = re.sub(r'href="#(\d+)-[^"]*"', lambda m: f'href="#{lang}-{m.group(1)}"', out)
    return out, toc

def num(t):
    return re.sub(r"^\d+\. ", "", t)

def build():
    convert_images()
    OUT.mkdir(parents=True, exist_ok=True)
    for lang in LANGS:
        b, toc = body(lang)
        u = UI[lang]
        nav = (f'<nav class="toc" data-l="{lang}" aria-label="{u["toc"]}"><p>{u["toc"]}</p><ol>'
               + "".join(f'<li><a href="#{i}">{html.escape(num(t))}</a></li>' for i, t in toc) + "</ol></nav>")
        art = (f'<article data-l="{lang}" lang="{lang}"><header class="ph"><img src="/assets/{APP["icon"]}" alt="" width="64" height="64">'
               f'<div><h1>{u["title"]}</h1><p>{u["sub"]}</p></div></header><p class="hint">{u["zoom"]}</p>{b}'
               f'<p class="links"><a class="get" href="https://github.com/tetsujin28/{APP["repo"]}/releases/latest">{u["dl"]}</a>'
               f'<a href="{GH}{LANGS[lang]}">{u["md"]}</a></p></article>')
        (OUT / f"{KEY}.{lang}.html").write_text(nav + "\n<!--ARTICLE-->\n" + art + "\n", encoding="utf-8")
        print("  écrit", OUT / f"{KEY}.{lang}.html")

if __name__ == "__main__":
    if KEY == "all":
        import subprocess
        for k in APPS:
            print(k)
            subprocess.run([sys.executable, __file__, k] + (["--all-images"] if ALL_IMAGES else []), check=True)
    else:
        build()
