"""Propaga o tema novo para as 12 paginas (PT e EN).

Tres trocas mecanicas que seriam pura repeticao a mao:

1. O config do Tailwind estava embutido em cada pagina. Passa a vir de
   theme.js, entao a identidade visual mora num arquivo so.
2. `bg-[#080808]` (preto puro, escrito direto no markup) vira `bg-zinc-950`,
   que o theme.js mapeia para o carvao azulado. Tira cor fixa do HTML.
3. Remove as redefinicoes de `.bg-dot-*` dos <style> inline. Elas vinham
   DEPOIS do design.css na cascata e sobrescreviam o fundo novo, trazendo os
   pontinhos de volta.

    python scripts/apply_theme.py
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = [ROOT / f"{n}.html" for n in ("index", "about", "articles", "projects", "uses", "hire")]
PAGES += [ROOT / "en" / f"{n}.html" for n in ("index", "about", "articles", "projects", "uses", "hire")]

INLINE_CONFIG = re.compile(r"<script>\s*tailwind\.config\s*=\s*\{[^<]*\}\s*</script>")
DOT_RULES = re.compile(r"\s*\.bg-dot-(?:white|black)\s*\{[^}]*\}")


def main() -> None:
    for page in PAGES:
        prefix = "../" if page.parent.name == "en" else "./"
        html = page.read_text(encoding="utf-8")
        before = html

        html = INLINE_CONFIG.sub(f'<script src="{prefix}theme.js"></script>', html)
        html = html.replace("bg-[#080808]", "bg-zinc-950")
        html = DOT_RULES.sub("", html)

        if html != before:
            page.write_text(html, encoding="utf-8")
            rel = page.relative_to(ROOT).as_posix()
            print(f"  atualizado: {rel}")


if __name__ == "__main__":
    main()
