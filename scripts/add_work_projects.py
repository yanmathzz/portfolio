"""Acrescenta os projetos profissionais e atualiza o card do app B2B.

O app deixou de ser "em preparacao": esta publicado nas duas lojas. E as duas
entregas maiores — a plataforma omnichannel e o canal de escuta — nao apareciam
em lugar nenhum, embora sejam o trabalho de maior porte do portfolio.

Numeros e stack vieram do curriculo.

    python scripts/add_work_projects.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LOCK = (
    '<svg viewBox="0 0 24 24" fill="none" class="h-4 w-4 stroke-current" stroke-width="1.5" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 '
    '2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z"/></svg>'
)
GRID_ICON = (
    '<path d="M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 '
    '2.25H6a2.25 2.25 0 01-2.25-2.25V6zM3.75 15.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 '
    '2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zM13.5 6a2.25 2.25 0 012.25-2.25H18A2.25 '
    '2.25 0 0120.25 6v2.25A2.25 2.25 0 0118 10.5h-2.25a2.25 2.25 0 01-2.25-2.25V6zM13.5 15.75a2.25 2.25 0 '
    '012.25-2.25H18a2.25 2.25 0 012.25 2.25V18A2.25 2.25 0 0118 20.25h-2.25A2.25 2.25 0 0113.5 18v-2.25z"/>'
)
SHIELD_ICON = (
    '<path d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 '
    '5.592 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 '
    '0-6.1-1.248-8.25-3.285z"/>'
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
                    {LOCK}
                    <span>{footer}</span>
                  </div>
                </article>"""


NOVOS = {
    "pt": [
        card(GRID_ICON, "Plataforma corporativa &middot; Em produ&ccedil;&atilde;o", "Plataforma Omnichannel",
             "Plataforma que re&uacute;ne atendimento por WhatsApp e e-mail em tempo real, chat interno com chamadas "
             "WebRTC e m&oacute;dulos de Comercial, Financeiro, RH e Log&iacute;stica. Constru&iacute;da do zero: 53 telas, 123 tabelas, "
             "~61 mil linhas e ~155 testes automatizados. Integrada ao ERP e &agrave; SEFAZ, com filas de trabalho no "
             "pr&oacute;prio PostgreSQL em vez de Redis.",
             ["Node.js", "Fastify", "React 19", "PostgreSQL", "Socket.io", "Docker"],
             "Sistema corporativo &middot; c&oacute;digo privado"),
        card(SHIELD_ICON, "Compliance &middot; Em produ&ccedil;&atilde;o", "Canal de Escuta e Acolhimento",
             "Canal de relatos para colaboradores com registro an&ocirc;nimo ou identificado, protocolo n&atilde;o sequencial, "
             "painel do RH com classifica&ccedil;&atilde;o por n&iacute;veis, controle de acesso por papel e o relat&oacute;rio trimestral "
             "exigido pela NR-01.",
             ["Next.js", "TypeScript", "Prisma", "PostgreSQL"],
             "Sistema corporativo &middot; c&oacute;digo privado"),
    ],
    "en": [
        card(GRID_ICON, "Corporate platform &middot; In production", "Omnichannel Platform",
             "A platform bringing together real-time WhatsApp and email support, internal chat with WebRTC calls "
             "and Sales, Finance, HR and Logistics modules. Built from scratch: 53 screens, 123 tables, ~61K lines "
             "of code and ~155 automated tests. Integrated with the ERP and SEFAZ, with job queues running on "
             "PostgreSQL itself instead of Redis.",
             ["Node.js", "Fastify", "React 19", "PostgreSQL", "Socket.io", "Docker"],
             "Corporate system &middot; private code"),
        card(SHIELD_ICON, "Compliance &middot; In production", "Employee Reporting Channel",
             "An employee reporting channel supporting anonymous or identified submissions, non-sequential case "
             "IDs, an HR dashboard with severity levels, role-based access control and the quarterly report "
             "required by Brazilian regulation NR-01.",
             ["Next.js", "TypeScript", "Prisma", "PostgreSQL"],
             "Corporate system &middot; private code"),
    ],
}

# o card do app deixa de ser "em preparacao" e ganha o nome do produto
APP = {
    "pt": [
        ("Mobile app &middot; Em produ&ccedil;&atilde;o", "App B2B &middot; Publicado nas lojas"),
        (">Eletransol</h3>", ">Eletro Transol Online</h3>"),
    ],
    "en": [
        ("Mobile app &middot; In production", "B2B app &middot; Published on the stores"),
        (">Eletransol</h3>", ">Eletro Transol Online</h3>"),
    ],
}


def main() -> None:
    for lang, path in (("pt", ROOT / "projects.html"), ("en", ROOT / "en" / "projects.html")):
        html = path.read_text(encoding="utf-8")

        for old, new in APP[lang]:
            if old in html:
                html = html.replace(old, new, 1)

        if "Omnichannel" in html:
            print(f"  {path.name}: projetos de trabalho ja presentes")
        else:
            anchor = html.find('<div class="project-grid mt-10">')
            if anchor == -1:
                sys.exit(f"erro: grade nao encontrada em {path}")
            end = html.find("</article>", anchor) + len("</article>")
            html = html[:end] + "".join(NOVOS[lang]) + html[end:]

        path.write_text(html, encoding="utf-8")
        print(f"  {path.relative_to(ROOT).as_posix()}: atualizado")


if __name__ == "__main__":
    main()
