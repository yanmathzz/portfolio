"""Liga favicon e cartao social (Open Graph / Twitter) nas 12 paginas.

Sem estas tags, colar o link no LinkedIn ou WhatsApp rende um retangulo cinza
sem titulo nem imagem — caro para quem usa o portfolio em candidatura.

As tags entram logo antes de </head>, reaproveitando o <title> e a meta
description que cada pagina ja tem, para o cartao falar o idioma da pagina.

    python scripts/add_meta.py
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://portfolio-yanmatheus.vercel.app"
PAGES = ["index", "about", "articles", "projects", "uses", "hire"]

MARK = "<!-- cartao social -->"


def build(title: str, desc: str, url: str, prefix: str, locale: str, alt_locale: str) -> str:
    return f"""  {MARK}
  <link rel="icon" type="image/svg+xml" href="{prefix}favicon.svg" />
  <meta name="theme-color" content="#0E1016" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Yan Matheus" />
  <meta property="og:locale" content="{locale}" />
  <meta property="og:locale:alternate" content="{alt_locale}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{SITE}/og-image.png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />
  <meta name="twitter:image" content="{SITE}/og-image.png" />
"""


def main() -> None:
    for page in PAGES:
        for lang in ("pt", "en"):
            path = ROOT / f"{page}.html" if lang == "pt" else ROOT / "en" / f"{page}.html"
            html = path.read_text(encoding="utf-8")

            if MARK in html:
                # idempotente: remove o bloco antigo antes de reescrever
                html = re.sub(rf"  {re.escape(MARK)}.*?(?=</head>)", "", html, flags=re.S)

            title = re.search(r"<title>(.*?)</title>", html, re.S)
            desc = re.search(r'name="description" content="([^"]*)"', html)
            if not title or not desc:
                print(f"  {path.name}: sem <title> ou description, pulando")
                continue

            url = (
                f"{SITE}/" if (page == "index" and lang == "pt")
                else f"{SITE}/{page}.html" if lang == "pt"
                else f"{SITE}/en/{page}.html"
            )
            prefix = "./" if lang == "pt" else "../"
            locale, alt = ("pt_BR", "en_US") if lang == "pt" else ("en_US", "pt_BR")

            block = build(title.group(1).strip(), desc.group(1), url, prefix, locale, alt)
            html = html.replace("</head>", block + "</head>", 1)
            path.write_text(html, encoding="utf-8")
            print(f"  {path.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
