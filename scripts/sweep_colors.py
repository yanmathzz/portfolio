"""Tira as cores cravadas a mao dos <style> inline das paginas.

Varios blocos inline escreviam o teal antigo direto (#0F766E, rgba(15,118,110,...))
em vez de usar os tokens. Como vinham depois do design.css na cascata, venciam o
tema novo e deixavam icones e bordas na cor velha mesmo apos a troca de paleta.

Aqui cada literal vira o token correspondente, entao a proxima troca de
identidade so precisa mexer no :root do design.css.

    python scripts/sweep_colors.py
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# literal antigo -> token. Ordem importa: rgba( antes dos hex soltos.
SWAPS = [
    # accent do tema claro
    ("rgba(15,118,110", "rgba(var(--accent-rgb)"),
    ("#0F766E", "var(--accent-color)"),
    ("#0f766e", "var(--accent-color)"),
    # accent do tema escuro
    ("rgba(73,163,155", "rgba(var(--accent-soft-rgb)"),
    ("#49A39B", "var(--accent-soft)"),
    ("#49a39b", "var(--accent-soft)"),
    # neutros: escala zinc antiga -> nova, levemente azulada
    ("#71717a", "#767c8f"),
    ("#52525b", "#565c6e"),
    ("#a1a1aa", "#9ba1b4"),
]


def main() -> None:
    pages = sorted(ROOT.glob("*.html")) + sorted((ROOT / "en").glob("*.html"))
    total = 0
    for page in pages:
        html = page.read_text(encoding="utf-8")
        before = html
        n = 0
        for old, new in SWAPS:
            n += html.count(old)
            html = html.replace(old, new)
        if html != before:
            page.write_text(html, encoding="utf-8")
            print(f"  {page.relative_to(ROOT).as_posix()}: {n} substituicao(oes)")
            total += n
    print(f"\ntotal: {total}")


if __name__ == "__main__":
    main()
