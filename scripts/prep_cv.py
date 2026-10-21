"""Prepara os PDFs do curriculo para publicacao no site.

Copia os originais do OneDrive para cv/ removendo a mencao a uma ferramenta que
nao deve aparecer na versao publica. A remocao e feita por redacao (redaction),
que apaga o texto do conteudo do PDF — nao apenas cobre visualmente. Uma tarja
por cima deixaria o texto extraivel por copiar-colar ou por buscador.

Ao final o script re-extrai o texto e falha se o termo ainda aparecer, para a
publicacao nunca sair de um PDF que so parece limpo.

    python scripts/prep_cv.py
"""

import shutil
import sys
from pathlib import Path

import fitz  # PyMuPDF

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = Path.home() / "OneDrive" / "Área de Trabalho" / "DocsYan"
OUT_DIR = ROOT / "cv"

# ", <termo>" para a linha fechar em "GitHub Copilot" sem virgula solta
REMOVE = [", Claude Code"]
FORBIDDEN = "claude"

FILES = {
    "Curriculo_Yan_Matheus_PTBR.pdf": "Yan-Matheus-CV-PT.pdf",
    "Curriculo_Yan_Matheus_EN.pdf": "Yan-Matheus-CV-EN.pdf",
}


def scrub(src: Path, dst: Path) -> int:
    doc = fitz.open(src)
    hits = 0
    for page in doc:
        for termo in REMOVE:
            for rect in page.search_for(termo):
                page.add_redact_annot(rect, fill=(1, 1, 1))
                hits += 1
        page.apply_redactions()
    doc.save(dst, garbage=4, deflate=True)
    doc.close()
    return hits


def verify(path: Path) -> None:
    doc = fitz.open(path)
    texto = " ".join(p.get_text() for p in doc).lower()
    doc.close()
    if FORBIDDEN in texto:
        sys.exit(f"ERRO: '{FORBIDDEN}' ainda aparece em {path.name} — nao publicar")


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    for origem, destino in FILES.items():
        src = SRC_DIR / origem
        if not src.exists():
            sys.exit(f"ERRO: nao encontrei {src}")
        dst = OUT_DIR / destino
        n = scrub(src, dst)
        verify(dst)
        kb = dst.stat().st_size / 1024
        print(f"  {destino}: {n} remocao(oes), {kb:.0f} KB, verificado")


if __name__ == "__main__":
    main()
