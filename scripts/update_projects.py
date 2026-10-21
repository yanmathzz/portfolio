"""Atualiza a galeria de projetos nas versoes PT e EN.

Acrescenta os projetos novos (Voya, Bot de Figurinhas) e recria o card do
FinTrack sem link: o repositorio e privado e o link levava visitantes a um 404
do GitHub, entao ele vira selo de codigo privado, igual ao Eletransol.

As descricoes vieram do que esta de fato nos repositorios — rotas, dependencias
e README — e nao de suposicao.

NOTA: a primeira versao deste script usava uma regex com `.*?` e re.S para achar
o rodape do FinTrack. Lazy ou nao, `.` com DOTALL atravessa qualquer coisa: o
casamento comecou no rodape de OUTRO card e varreu tudo ate o FinTrack, apagando
cards inteiros no caminho. Por isso aqui nada e procurado no documento todo —
trabalhamos por bloco <article>, que tem limite claro.

    python scripts/update_projects.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LOCK_SVG = (
    '<svg viewBox="0 0 24 24" fill="none" class="h-4 w-4 stroke-current" stroke-width="1.5" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 '
    '2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z"/></svg>'
)

MAP_ICON = (
    '<path d="M9 6.75V15m6-6v8.25m.503 3.498l4.875-2.437c.381-.19.622-.58.622-1.006V4.82c0-.836-.88-1.38-1.628-1.006'
    'l-3.869 1.934c-.317.159-.69.159-1.006 0L9.503 3.252a1.125 1.125 0 00-1.006 0L3.622 5.689C3.24 5.88 3 6.27 3 '
    '6.695V19.18c0 .836.88 1.38 1.628 1.006l3.869-1.934c.317-.159.69-.159 1.006 0l4.994 2.497c.317.158.69.158 1.006 0z"/>'
)
CHART_ICON = (
    '<path d="M2.25 18L9 11.25l4.306 4.307a11.95 11.95 0 015.814-5.519l2.74-1.22m0 0l-5.94-2.28m5.94 2.28l-2.28 5.941"/>'
)
CHAT_ICON = (
    '<path d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 '
    '01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 '
    '8.25a9.764 9.764 0 01-2.555-.337A5.972 5.972 0 015.41 20.97a5.969 5.969 0 01-.474-.065 4.48 4.48 0 '
    '00.978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25z"/>'
)


def card(icon, kicker, title, desc, tags, footer):
    tag_html = "\n                    ".join(f'<span class="project-tag">{t}</span>' for t in tags)
    return f"""
                <article class="project-card fade-up">
                  <div class="project-icon relative z-10">
                    <svg viewBox="0 0 24 24" fill="none" class="h-5 w-5 stroke-current" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{icon}</svg>
                  </div>
                  <div class="relative z-10">
                    <p class="project-kicker">{kicker}</p>
                    <h3 class="mt-3 text-xl font-semibold tracking-tight text-zinc-900 dark:text-zinc-100">{title}</h3>
                    <p class="mt-4 text-sm leading-7 text-zinc-600 dark:text-zinc-400">{desc}</p>
                  </div>
                  <div class="relative z-10 project-meta">
                    {tag_html}
                  </div>
                  <div class="relative z-10 project-repo">
                    {LOCK_SVG}
                    <span>{footer}</span>
                  </div>
                </article>"""


CONTENT = {
    "pt": {
        "private": "C&oacute;digo privado",
        "voya": ("Mobile app &middot; Em desenvolvimento", "Voya",
                 "Aplicativo de viagens em React Native: onboarding, autentica&ccedil;&atilde;o, explora&ccedil;&atilde;o de destinos, "
                 "montagem de roteiros e perfil do viajante. Dados no Firebase, monitoramento de erros com Sentry "
                 "e distribui&ccedil;&atilde;o de builds via EAS."),
        "fintrack": ("Full-stack &middot; Finan&ccedil;as pessoais", "FinTrack",
                     "Plataforma de gest&atilde;o financeira pessoal com autentica&ccedil;&atilde;o segura, dashboard interativo e "
                     "visualiza&ccedil;&atilde;o de dados. Aplica&ccedil;&atilde;o full-stack totalmente containerizada com Docker, do "
                     "banco ao frontend."),
        "bot": ("Automa&ccedil;&atilde;o &middot; Projeto pessoal", "Bot de Figurinhas",
                "Bot de WhatsApp que transforma imagens em figurinhas automaticamente. Conecta por QR code, roda "
                "localmente e processa as imagens com Sharp &mdash; pequeno, mas com instala&ccedil;&atilde;o pensada para quem "
                "n&atilde;o &eacute; t&eacute;cnico."),
    },
    "en": {
        "private": "Private code",
        "voya": ("Mobile app &middot; In development", "Voya",
                 "A travel app built in React Native: onboarding, authentication, destination browsing, itinerary "
                 "building and traveller profile. Data on Firebase, error monitoring with Sentry and build "
                 "distribution through EAS."),
        "fintrack": ("Full-stack &middot; Personal finance", "FinTrack",
                     "A personal finance platform with secure authentication, an interactive dashboard and data "
                     "visualisation. A full-stack application fully containerised with Docker, from database to "
                     "frontend."),
        "bot": ("Automation &middot; Personal project", "Sticker Bot",
                "A WhatsApp bot that turns images into stickers automatically. Pairs over QR code, runs locally "
                "and processes images with Sharp &mdash; small, but packaged so a non-technical person can install it."),
    },
}

TAGS = {
    "voya": ["React Native", "Expo", "TypeScript", "Firebase"],
    "fintrack": ["TypeScript", "React", "Node.js", "PostgreSQL", "Docker"],
    "bot": ["Node.js", "whatsapp-web.js", "Sharp"],
}
ICONS = {"voya": MAP_ICON, "fintrack": CHART_ICON, "bot": CHAT_ICON}


def build(lang, key):
    kicker, title, desc = CONTENT[lang][key]
    return card(ICONS[key], kicker, title, desc, TAGS[key], CONTENT[lang]["private"])


def main() -> None:
    for lang, path in (("pt", ROOT / "projects.html"), ("en", ROOT / "en" / "projects.html")):
        html = path.read_text(encoding="utf-8")
        added = []

        # Topo da grade: logo depois do primeiro card, para agrupar o trabalho mais forte.
        anchor = html.find('<div class="project-grid mt-10">')
        if anchor == -1:
            sys.exit(f"erro: grade de projetos nao encontrada em {path}")
        first_end = html.find("</article>", anchor) + len("</article>")

        top = ""
        for key in ("voya", "fintrack"):
            title = CONTENT[lang][key][1]
            if f">{title}</h3>" not in html:
                top += build(lang, key)
                added.append(title)
        html = html[:first_end] + top + html[first_end:]

        # Projeto menor entra ao lado das outras ferramentas, no fim da grade.
        bot_title = CONTENT[lang]["bot"][1]
        if f">{bot_title}</h3>" not in html:
            last_end = html.rfind("</article>") + len("</article>")
            html = html[:last_end] + build(lang, "bot") + html[last_end:]
            added.append(bot_title)

        path.write_text(html, encoding="utf-8")
        rel = path.relative_to(ROOT).as_posix()
        print(f"  {rel}: {', '.join(added) if added else 'nada a fazer'}")


if __name__ == "__main__":
    main()
