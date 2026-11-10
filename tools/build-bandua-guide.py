"""Fabrique bandua/guide/index.html à partir du mode d'emploi du dépôt Bandua.

    pip install markdown pillow
    python tools/build-bandua-guide.py ../bandua

Le mode d'emploi s'écrit dans le dépôt Bandua (docs/GUIDE.md, GUIDE.fr.md, GUIDE.es.md),
qui reste la seule source. Ce script en tire la page du site et convertit les images en WebP.
"""
import html, pathlib, re, sys
import markdown
from PIL import Image

SITE = pathlib.Path(__file__).resolve().parents[1]
BANDUA = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "../bandua").resolve()
OUT = SITE / "bandua" / "guide"
IMG = OUT / "img"
LANGS = {"en": "GUIDE.md", "fr": "GUIDE.fr.md", "es": "GUIDE.es.md"}
UI = {
    "en": dict(title="Bandua user guide", sub="Version 0.2.0 (beta) · Windows and macOS", toc="Contents", back="Back to Bandua",
               dl="Download Bandua", md="This guide on GitHub", close="Close", zoom="Click an image to enlarge it."),
    "fr": dict(title="Bandua, mode d'emploi", sub="Version 0.2.0 (bêta) · Windows et macOS", toc="Sommaire", back="Retour à Bandua",
               dl="Télécharger Bandua", md="Ce guide sur GitHub", close="Fermer", zoom="Cliquez sur une image pour l'agrandir."),
    "es": dict(title="Bandua, manual de uso", sub="Versión 0.2.0 (beta) · Windows y macOS", toc="Índice", back="Volver a Bandua",
               dl="Descargar Bandua", md="Esta guía en GitHub", close="Cerrar", zoom="Haz clic en una imagen para ampliarla."),
}
GH = "https://github.com/tetsujin28/bandua/blob/main/docs/"

def convert_images():
    IMG.mkdir(parents=True, exist_ok=True)
    for p in sorted((BANDUA / "docs" / "guide").glob("*.png")):
        Image.open(p).convert("RGB").save(IMG / (p.stem + ".webp"), "WEBP", quality=88, method=6)

def body(lang):
    src = (BANDUA / "docs" / LANGS[lang]).read_text(encoding="utf-8")
    src = src[src.index("\n## ", src.index("## ") + 3):]  # retire l'en-tête HTML et le sommaire
    src = src.replace("../LICENSE", "https://github.com/tetsujin28/bandua/blob/main/LICENSE")
    out = markdown.markdown(src, extensions=["tables", "fenced_code"])
    toc = []
    def h2(m):
        n = len(toc) + 1
        toc.append((f"{lang}-{n}", re.sub(r"<[^>]+>", "", m.group(1))))
        return f'<h2 id="{lang}-{n}">{m.group(1)}</h2>'
    out = re.sub(r"<h2>(.*?)</h2>", h2, out)
    out = re.sub(r'<p align="center"><img src="guide/([^"]+)\.png" width="(\d+)" alt="([^"]*)"></p>',
                 lambda m: f'<figure class="shot w{m.group(2)}"><img src="img/{m.group(1)}.webp" alt="{m.group(3)}" loading="lazy"></figure>', out)
    out = out.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    return out, toc

def page():
    convert_images()
    arts, tocs = [], []
    for lang in LANGS:
        b, toc = body(lang)
        u = UI[lang]
        tocs.append(f'<nav class="toc" data-l="{lang}" aria-label="{u["toc"]}"><p>{u["toc"]}</p><ol>'
                    + "".join(f'<li><a href="#{i}">{html.escape(re.sub(r"^\d+\. ", "", t))}</a></li>' for i, t in toc) + "</ol></nav>")
        arts.append(f'<article data-l="{lang}" lang="{lang}"><header class="ph"><img src="../../assets/bandua-icon.png" alt="" width="64" height="64">'
                    f'<div><h1>{u["title"]}</h1><p>{u["sub"]}</p></div></header><p class="hint">{u["zoom"]}</p>{b}'
                    f'<p class="links"><a class="get" href="https://github.com/tetsujin28/bandua/releases/latest">{u["dl"]}</a>'
                    f'<a href="{GH}{LANGS[lang]}">{u["md"]}</a></p></article>')
    ui = {l: {k: UI[l][k] for k in ("back", "close")} for l in UI}
    return TEMPLATE.replace("{{TOC}}", "\n".join(tocs)).replace("{{ARTICLES}}", "\n".join(arts)).replace("{{UI}}", repr(ui).replace("'", '"'))

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bandua user guide · Mode d'emploi · Manual de uso</title>
<meta name="description" content="Complete user guide for Bandua, the free app that offloads camera cards and verifies every copy by hash. Step by step, with annotated screenshots, in English, French and Spanish.">
<meta property="og:title" content="Bandua user guide">
<meta property="og:description" content="Offload camera cards and verify every copy: the complete Bandua user guide, with annotated screenshots.">
<meta property="og:type" content="article">
<meta property="og:url" content="https://tetsujin28.github.io/bandua/guide/">
<meta property="og:image" content="https://tetsujin28.github.io/assets/og-image.jpg">
<link rel="canonical" href="https://tetsujin28.github.io/bandua/guide/">
<link rel="icon" href="../../assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,300..900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{--ink:#0d0e10;--panel:#15171a;--raise:#1c1f23;--line:#262a30;--paper:#ecebe8;--muted:#8d939c;--faint:#5d636c;--accent:#f39a3c;--ok:#35d39a;
  --sans:"Archivo",system-ui,sans-serif;--mono:"JetBrains Mono",ui-monospace,monospace;--gut:clamp(20px,4vw,48px)}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;background:var(--ink);scroll-padding-top:84px}
body{font-family:var(--sans);font-variation-settings:"wdth" 100;color:var(--paper);background:var(--ink);font-size:17px;line-height:1.65;-webkit-font-smoothing:antialiased}
a{color:inherit}
img{display:block;max-width:100%;height:auto}
:focus-visible{outline:2px solid var(--paper);outline-offset:3px;border-radius:4px}
.top{position:fixed;inset:0 0 auto;z-index:20;backdrop-filter:blur(14px);background:rgba(13,14,16,.8);border-bottom:1px solid var(--line)}
.top .in{max-width:1240px;margin:0 auto;padding:0 var(--gut);display:flex;align-items:center;gap:22px;height:64px}
.brand{font-weight:700;font-variation-settings:"wdth" 112;text-decoration:none;margin-right:auto;white-space:nowrap}
.back{color:var(--muted);text-decoration:none;font-size:15px}.back:hover{color:var(--paper)}
.lang{display:flex;border:1px solid var(--line);border-radius:8px;overflow:hidden}
.lang button{all:unset;cursor:pointer;font:500 12px var(--mono);padding:6px 10px;color:var(--faint)}
.lang button[aria-pressed="true"]{background:var(--raise);color:var(--paper)}
.wrap{max-width:1240px;margin:0 auto;padding:104px var(--gut) 80px;display:grid;grid-template-columns:250px minmax(0,1fr);gap:clamp(32px,5vw,72px)}
.toc{position:sticky;top:96px;align-self:start;font-size:14.5px}
.toc p{font:500 12px var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--faint);margin-bottom:12px}
.toc ol{list-style:none;counter-reset:t;display:grid;gap:2px;border-left:1px solid var(--line)}
.toc li{counter-increment:t}
.toc a{display:block;padding:5px 0 5px 16px;margin-left:-1px;border-left:2px solid transparent;color:var(--muted);text-decoration:none;line-height:1.35}
.toc a::before{content:counter(t) ". ";color:var(--faint);font-family:var(--mono);font-size:12px}
.toc a:hover{color:var(--paper)}
.toc a.on{color:var(--paper);border-left-color:var(--accent)}
[data-l]{display:none}
html[data-lang="en"] [data-l="en"],html[data-lang="fr"] [data-l="fr"],html[data-lang="es"] [data-l="es"]{display:block}
article{max-width:860px;min-width:0}
.ph{display:flex;gap:20px;align-items:center;margin-bottom:12px}
.ph img{width:64px;border-radius:50%}
h1{font-size:clamp(38px,5.4vw,68px);line-height:.95;font-weight:850;font-variation-settings:"wdth" 118;letter-spacing:-.035em}
.ph p{color:var(--muted);margin-top:8px;font-size:15px;font-family:var(--mono)}
.hint{color:var(--faint);font-size:14px;margin:26px 0 0}
h2{font-size:clamp(28px,3.4vw,40px);line-height:1.05;font-weight:800;font-variation-settings:"wdth" 112;letter-spacing:-.02em;margin:76px 0 20px;padding-top:28px;border-top:1px solid var(--line)}
h3{font-size:21px;font-weight:700;font-variation-settings:"wdth" 106;margin:40px 0 12px}
article p{margin:14px 0;color:#c9ccd1}
article strong{color:var(--paper);font-weight:650}
article em{color:var(--paper)}
article ul,article ol{margin:14px 0 14px 22px;color:#c9ccd1}
article li{margin:6px 0;padding-left:4px}
article li::marker{color:var(--accent)}
article a{color:var(--accent);text-underline-offset:3px}
code{font-family:var(--mono);font-size:.84em;color:var(--paper);background:var(--raise);padding:2px 6px;border-radius:5px;overflow-wrap:anywhere}
pre{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px 18px;margin:18px 0;overflow-x:auto}
pre code{background:none;padding:0;color:var(--accent);font-size:14.5px}
.tw{overflow-x:auto;margin:20px 0;border:1px solid var(--line);border-radius:12px}
table{width:100%;border-collapse:collapse;font-size:15px}
th{text-align:left;font:500 12px var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--faint);background:var(--panel);padding:11px 14px}
td{padding:11px 14px;border-top:1px solid var(--line);vertical-align:top;color:#c9ccd1}
.shot{margin:26px 0;border:1px solid var(--line);border-radius:12px;background:#000;padding:8px;cursor:zoom-in}
.shot img{border-radius:6px;margin:0 auto}
.shot.w560 img{max-width:560px}.shot.w700 img{max-width:700px}
.links{display:flex;flex-wrap:wrap;gap:18px;align-items:center;margin-top:60px!important;padding-top:32px;border-top:1px solid var(--line)}
.get{display:inline-flex;padding:13px 22px;border-radius:12px;background:var(--accent);color:#16110a!important;font-weight:700;text-decoration:none}
footer{border-top:1px solid var(--line);padding:32px var(--gut) 44px;color:var(--faint);font-size:14px;text-align:center}
dialog{border:0;padding:0;background:transparent;max-width:96vw;max-height:94vh;margin:auto}
dialog::backdrop{background:rgba(5,5,6,.92)}
dialog img{max-width:96vw;max-height:90vh;width:auto;border-radius:8px}
dialog button{all:unset;position:fixed;top:16px;right:20px;cursor:pointer;color:var(--paper);font:500 14px var(--mono);padding:8px 12px;border:1px solid var(--line);border-radius:8px;background:var(--panel)}
@media (max-width:900px){.wrap{grid-template-columns:minmax(0,1fr);gap:0}.toc{display:none!important}.back{display:none}}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
</style>
</head>
<body>
<header class="top"><div class="in">
  <a class="brand" href="../../">Domingo Olmo Martin</a>
  <a class="back" href="../../#bandua" data-t="back">Back to Bandua</a>
  <div class="lang" role="group" aria-label="Language">
    <button type="button" data-lang="en">EN</button><button type="button" data-lang="fr">FR</button><button type="button" data-lang="es">ES</button>
  </div>
</div></header>
<main class="wrap">
<div>
{{TOC}}
</div>
<div>
{{ARTICLES}}
</div>
</main>
<footer>© 2026 Domingo Olmo Martin · MIT License</footer>
<dialog id="lb"><form method="dialog"><button data-t="close">Close</button></form><img alt=""></dialog>
<script>
const UI = {{UI}};
const root = document.documentElement;
function applyLang(l){
  if (!UI[l]) l = "en";
  root.dataset.lang = l; root.lang = l;
  document.querySelectorAll(".lang button").forEach(b => b.setAttribute("aria-pressed", b.dataset.lang === l));
  document.querySelectorAll("[data-t]").forEach(e => e.textContent = UI[l][e.dataset.t]);
  try { localStorage.setItem("lang", l); } catch(e) {}
  spy();
}
document.querySelectorAll(".lang button").forEach(b => b.addEventListener("click", () => { applyLang(b.dataset.lang); scrollTo(0, 0); }));
const lb = document.getElementById("lb");
document.querySelectorAll(".shot").forEach(f => f.addEventListener("click", () => {
  const i = f.querySelector("img"); lb.querySelector("img").src = i.src; lb.querySelector("img").alt = i.alt; lb.showModal();
}));
lb.addEventListener("click", e => { if (e.target === lb) lb.close(); });
function spy(){
  const l = root.dataset.lang, hs = [...document.querySelectorAll(`article[data-l="${l}"] h2`)];
  let cur = hs[0]; for (const h of hs) if (h.getBoundingClientRect().top < 140) cur = h;
  document.querySelectorAll(".toc a").forEach(a => a.classList.toggle("on", cur && a.getAttribute("href") === "#" + cur.id));
}
addEventListener("scroll", spy, {passive:true});
const q = new URLSearchParams(location.search).get("lang");
const fromHash = (location.hash.match(/^#(en|fr|es)-/) || [])[1];
let saved = null; try { saved = localStorage.getItem("lang"); } catch(e) {}
const nav = (navigator.language || "en").slice(0, 2);
applyLang(q || fromHash || saved || (UI[nav] ? nav : "en"));
if (location.hash) document.getElementById(location.hash.slice(1))?.scrollIntoView();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(page(), encoding="utf-8")
    print("écrit", OUT / "index.html")
