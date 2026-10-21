"""Gera os ativos que faltavam no site: favicon, imagem social, robots e sitemap.

- favicon.svg  : monograma YM na cor da marca. SVG porque escala em qualquer
                 densidade de tela e pesa menos que um .ico.
- og-image.png : o card que aparece ao colar o link no LinkedIn ou WhatsApp.
                 Sem ele o compartilhamento vira um retangulo cinza vazio.
- robots.txt   : libera o rastreamento e aponta o sitemap.
- sitemap.xml  : as 12 paginas (PT e EN) com hreflang, para o buscador entender
                 que sao o mesmo conteudo em dois idiomas.

    python scripts/make_assets.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://portfolio-yanmatheus.vercel.app"
PAGES = ["index", "about", "articles", "projects", "uses", "hire"]

BG = (14, 16, 22)
ACCENT = (141, 162, 251)
VIOLET = (196, 167, 251)
TEXT = (230, 232, 238)
MUTED = (154, 161, 180)

# Windows: tentamos as fontes do sistema, da mais para a menos desejavel.
FONT_CANDIDATES = [
    r"C:\Windows\Fonts\segoeuib.ttf",
    r"C:\Windows\Fonts\arialbd.ttf",
    r"C:\Windows\Fonts\calibrib.ttf",
]
FONT_REGULAR = [
    r"C:\Windows\Fonts\segoeui.ttf",
    r"C:\Windows\Fonts\arial.ttf",
    r"C:\Windows\Fonts\calibri.ttf",
]


def load_font(candidates: list[str], size: int):
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def favicon() -> None:
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#8DA2FB"/>
      <stop offset="100%" stop-color="#C4A7FB"/>
    </linearGradient>
  </defs>
  <rect width="64" height="64" rx="14" fill="#0E1016"/>
  <text x="32" y="43" text-anchor="middle"
        font-family="Inter,Segoe UI,Helvetica,Arial,sans-serif"
        font-size="30" font-weight="700" fill="url(#g)">YM</text>
</svg>
"""
    (ROOT / "favicon.svg").write_text(svg, encoding="utf-8")
    print("  favicon.svg")


def og_image() -> None:
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img, "RGBA")

    # halos difusos, o mesmo tratamento de fundo do site
    for cx, cy, r, col, a in ((120, -40, 560, ACCENT, 46), (1120, 90, 460, VIOLET, 34)):
        for i in range(r, 0, -8):
            alpha = int(a * (1 - i / r) ** 2)
            d.ellipse((cx - i, cy - i, cx + i, cy + i), fill=col + (alpha,))

    d.rectangle((0, 0, 8, H), fill=ACCENT)

    nome = load_font(FONT_CANDIDATES, 76)
    papel = load_font(FONT_CANDIDATES, 34)
    corpo = load_font(FONT_REGULAR, 27)

    d.text((88, 196), "Yan Matheus", font=nome, fill=TEXT)
    d.text((88, 296), "Desenvolvedor Full-Stack", font=papel, fill=ACCENT)
    d.text((88, 352), "Engenheiro de Computação  ·  Belém, PA", font=corpo, fill=MUTED)
    d.text((88, 452), "TypeScript  ·  React  ·  Node.js  ·  PostgreSQL  ·  Docker", font=corpo, fill=MUTED)
    d.text((88, 500), "portfolio-yanmatheus.vercel.app", font=corpo, fill=ACCENT)

    img.save(ROOT / "og-image.png", "PNG", optimize=True)
    kb = (ROOT / "og-image.png").stat().st_size / 1024
    print(f"  og-image.png ({W}x{H}, {kb:.0f} KB)")


def robots() -> None:
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8"
    )
    print("  robots.txt")


def sitemap() -> None:
    entries = []
    for page in PAGES:
        pt = f"{SITE}/" if page == "index" else f"{SITE}/{page}.html"
        en = f"{SITE}/en/{page}.html"
        for loc, alt_self in ((pt, "pt-BR"), (en, "en")):
            links = (
                f'    <xhtml:link rel="alternate" hreflang="pt-BR" href="{pt}"/>\n'
                f'    <xhtml:link rel="alternate" hreflang="en" href="{en}"/>\n'
                f'    <xhtml:link rel="alternate" hreflang="x-default" href="{pt}"/>'
            )
            priority = "1.0" if (page == "index" and alt_self == "pt-BR") else "0.8"
            entries.append(
                f"  <url>\n    <loc>{loc}</loc>\n{links}\n"
                f"    <changefreq>monthly</changefreq>\n    <priority>{priority}</priority>\n  </url>"
            )

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(entries)
        + "\n</urlset>\n"
    )
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")
    print(f"  sitemap.xml ({len(entries)} URLs)")


if __name__ == "__main__":
    favicon()
    og_image()
    robots()
    sitemap()
