"""Cria o esqueleto das paginas em ingles a partir das paginas em portugues.

Cuida so da parte mecanica e repetitiva: caminhos de assets (que sobem um nivel
dentro de en/), atributo lang, links de navegacao, botao de idioma invertido e
as tags hreflang. A traducao do texto e feita depois, a mao, arquivo por arquivo.

Rode de novo so quando a ESTRUTURA das paginas PT mudar — rodar por cima de
paginas ja traduzidas apaga a traducao.

    python scripts/build_en.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN = ROOT / "en"

PAGES = ["index", "about", "articles", "projects", "uses", "hire"]
SITE = "https://portfolio-yanmatheus.vercel.app"

BTN_CLASS = (
    "pointer-events-auto flex-none flex h-9 items-center justify-center rounded-full "
    "bg-white/90 px-3 text-xs font-bold tracking-wide text-zinc-600 shadow-lg "
    "shadow-zinc-800/5 ring-1 ring-zinc-900/5 backdrop-blur-md dark:bg-zinc-900/90 "
    "dark:text-zinc-300 dark:ring-white/10 transition-all hover:text-teal-500 "
    "hover:ring-teal-500/30 dark:hover:text-teal-400"
)


def pt_button(page: str) -> str:
    return (
        f'<a href="../{page}.html" aria-label="Mudar para portugues" hreflang="pt-BR"\n'
        f'              class="{BTN_CLASS}">PT</a>'
    )


def en_button(page: str) -> str:
    return (
        f'<a href="./en/{page}.html" aria-label="Switch to English" hreflang="en"\n'
        f'              class="{BTN_CLASS}">EN</a>'
    )


def alternates(page: str, current: str) -> str:
    """Diz ao Google que as duas paginas sao a mesma coisa em idiomas diferentes."""
    pt = f"{SITE}/{page}.html" if page != "index" else f"{SITE}/"
    en = f"{SITE}/en/{page}.html"
    return (
        f'  <link rel="alternate" hreflang="pt-BR" href="{pt}" />\n'
        f'  <link rel="alternate" hreflang="en" href="{en}" />\n'
        f'  <link rel="alternate" hreflang="x-default" href="{pt}" />\n'
        f'  <link rel="canonical" href="{en if current == "en" else pt}" />'
    )


def strip_alternates(html: str) -> str:
    """Remove blocos hreflang/canonical existentes.

    A pagina EN nasce de uma copia da PT, que ja recebeu esse bloco. Sem limpar
    antes, o EN acaba com o bloco duas vezes — e com dois canonical conflitantes,
    um apontando para a PT e outro para a EN, o que faz o buscador escolher a
    versao errada.
    """
    return re.sub(
        r'[ \t]*<link rel="(?:alternate|canonical)"[^>]*>\n?', "", html
    )


def to_english_skeleton(html: str, page: str) -> str:
    html = strip_alternates(html)
    # assets sobem um nivel dentro de en/
    html = html.replace('href="./design.css"', 'href="../design.css"')
    html = html.replace('src="./anim.js"', 'src="../anim.js"')
    html = html.replace('src="./images/', 'src="../images/')

    html = html.replace('<html lang="pt-BR"', '<html lang="en"')

    # botao de idioma: EN -> PT apontando de volta para a raiz
    html = re.sub(
        r'<a href="\./en/[a-z]+\.html"[^>]*>\s*EN</a>',
        pt_button(page),
        html,
        flags=re.S,
    )
    html = html.replace("<!-- Language toggle -->", "<!-- Alternador de idioma -->")

    # hreflang logo antes do </head>
    html = html.replace("</head>", alternates(page, "en") + "\n</head>", 1)
    return html


def ensure_pt_button(html: str, page: str) -> str:
    """Garante o botao EN nas paginas PT que ainda nao tem."""
    if ">EN</a>" in html:
        return html
    marker = '<button id="theme-toggle"'
    idx = html.find(marker)
    if idx == -1:
        return html
    indent = "              "
    block = f"<!-- Language toggle -->\n{indent}{en_button(page)}\n\n{indent}"
    return html[:idx] + block + html[idx:]


def main() -> None:
    EN.mkdir(exist_ok=True)
    for page in PAGES:
        src = ROOT / f"{page}.html"
        html = src.read_text(encoding="utf-8")

        # 1) pagina PT ganha o botao EN e as tags hreflang
        pt = ensure_pt_button(html, page)
        if "hreflang=\"x-default\"" not in pt:
            pt = pt.replace("</head>", alternates(page, "pt") + "\n</head>", 1)
        if pt != html:
            src.write_text(pt, encoding="utf-8")
            print(f"  PT atualizado: {page}.html")

        # 2) esqueleto EN — nunca sobrescreve uma traducao ja feita
        dst = EN / f"{page}.html"
        if dst.exists() and "--force" not in sys.argv:
            print(f"  EN ja existe, preservado: en/{page}.html")
            continue
        dst.write_text(to_english_skeleton(pt, page), encoding="utf-8")
        print(f"  EN criado: en/{page}.html")


if __name__ == "__main__":
    main()
