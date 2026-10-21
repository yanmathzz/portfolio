"""Acrescenta o cargo atual e o freelance a linha do tempo, em PT e EN.

Conteudo tirado do curriculo. Sem estas entradas o site mostrava a ultima
experiencia encerrando em jan/2026, o que para quem le hoje parece um vao de
varios meses — justamente o periodo da entrega mais substancial.

    python scripts/add_current_role.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def bloco(empresa: str, periodo: str, cargo: str, itens: list[str]) -> str:
    lis = "\n                    ".join(
        f'<li class="flex gap-2"><span class="text-teal-500 flex-shrink-0">›</span>{i}</li>' for i in itens
    )
    return f"""              <div class="tl-wrap mb-10">
                <div class="tl-dot"></div>
                <div class="glass rounded-2xl border border-zinc-100 dark:border-zinc-700/40 p-5 transition">
                  <div class="flex flex-wrap items-center justify-between gap-2 mb-1">
                    <span class="text-sm font-semibold text-zinc-900 dark:text-zinc-100">{empresa}</span>
                    <span class="mono text-xs text-zinc-400 dark:text-zinc-500 bg-zinc-100 dark:bg-white/5 px-2 py-0.5 rounded-md">{periodo}</span>
                  </div>
                  <p class="text-sm text-teal-600 dark:text-teal-400 mb-3 font-medium">{cargo}</p>
                  <ul class="space-y-1.5 text-sm text-zinc-600 dark:text-zinc-400">
                    {lis}
                  </ul>
                </div>
              </div>

"""


PT = bloco(
    "Eletro Transol Tecnologia — Belém, PA", "Jun 2026 – Atual",
    "Desenvolvedor Full-Stack (desenvolvedor único)",
    [
        "Único desenvolvedor da empresa, responsável pelo ciclo completo dos sistemas: levantamento de requisitos com as áreas de negócio, arquitetura, desenvolvimento, deploy, manutenção e suporte.",
        "Plataforma omnichannel corporativa construída do zero (Node.js/Fastify, React 19, PostgreSQL, Socket.io), em produção desde set/2026: atendimento por WhatsApp e e-mail em tempo real, chat interno com chamadas WebRTC e módulos de Comercial, Financeiro, RH e Logística — 53 telas, 123 tabelas, ~61 mil linhas e ~155 testes automatizados.",
        "Integrações com o ERP WinSAC/ENSIS (sincronização Firebird → PostgreSQL e envio de pedidos via API REST), SEFAZ com certificado A1 em TLS mútuo, Amazon SES/SNS e Qive para recebimento de NF-e, CT-e e NFS-e.",
        "Filas de trabalho sem Redis (PostgreSQL com FOR UPDATE SKIP LOCKED), autenticação sem senha com revogação instantânea de sessão, permissões por hierarquia em ambiente multiempresa e deploy com Docker Compose, Caddy e CI no GitHub Actions.",
        "Eletro Transol Online: app de e-commerce B2B em React Native publicado na App Store e no Google Play. Recebi o projeto de outro fornecedor como um frontend estático, finalizei o produto e negociei sua adoção — o que resultou na minha contratação.",
        "Canal de Escuta e Acolhimento (Next.js, TypeScript, Prisma): relatos anônimos ou identificados, protocolo não sequencial, painel do RH com classificação por níveis e relatório trimestral exigido pela NR-01.",
    ],
) + bloco(
    "Sistema de Logística Fluvial — Belém, PA", "2025 – 2026",
    "Desenvolvedor Full-Stack (freelance)",
    [
        "Sistema web para empresa de transporte hidroviário de cargas e passageiros (rotas Belém–Macapá–Santarém), desenvolvido em parceria com outro desenvolvedor.",
        "Responsável pela modelagem de dados, backend (Node.js/PostgreSQL) e frontend (React/TypeScript), incluindo gestão de viagens, embarcações e faturamento.",
    ],
)

EN = bloco(
    "Eletro Transol Tecnologia — Belém, Brazil", "Jun 2026 – Present",
    "Full-Stack Developer (sole developer)",
    [
        "Sole developer at the company, responsible for the complete system lifecycle: requirements gathering with business teams, architecture, development, deployment, maintenance and support.",
        "Corporate omnichannel platform built from scratch (Node.js/Fastify, React 19, PostgreSQL, Socket.io), in production since Sep 2026: real-time WhatsApp and email support, internal chat with WebRTC calls, and Sales, Finance, HR and Logistics modules — 53 screens, 123 tables, ~61K lines of code and ~155 automated tests.",
        "Integrations with the WinSAC/ENSIS ERP (Firebird → PostgreSQL sync and order submission over a REST API), SEFAZ using an A1 certificate with mutual TLS, Amazon SES/SNS, and Qive for receiving NF-e, CT-e and NFS-e documents.",
        "Job queues without Redis (PostgreSQL with FOR UPDATE SKIP LOCKED), passwordless authentication with instant session revocation, hierarchical permissions in a multi-company environment, and deployment with Docker Compose, Caddy and CI on GitHub Actions.",
        "Eletro Transol Online: a B2B e-commerce app in React Native published on the App Store and Google Play. I took the project over from another vendor as a static frontend, finished the product and negotiated its adoption — which led to my hiring.",
        "Employee Reporting &amp; Support Channel (Next.js, TypeScript, Prisma): anonymous or identified submissions, non-sequential case IDs, an HR dashboard with severity levels and the quarterly report required by NR-01.",
    ],
) + bloco(
    "River Logistics System — Belém, Brazil", "2025 – 2026",
    "Full-Stack Developer (freelance)",
    [
        "Web system for a cargo and passenger river transport company (Belém–Macapá–Santarém routes), developed in partnership with another developer.",
        "Responsible for data modelling, backend (Node.js/PostgreSQL) and frontend (React/TypeScript), covering trip, vessel and billing management.",
    ],
)

# marcador: a entrada seguinte na linha do tempo
ANCHOR = {"pt": "Amazon Informática — Belém, PA", "en": "Amazon Informática — Belém, Brazil"}


def main() -> None:
    for lang, path, novo in (("pt", ROOT / "about.html", PT), ("en", ROOT / "en" / "about.html", EN)):
        html = path.read_text(encoding="utf-8")
        if "Eletro Transol" in html:
            print(f"  {path.name}: ja presente, pulando")
            continue
        alvo = ANCHOR[lang]
        pos = html.find(alvo)
        if pos == -1:
            sys.exit(f"erro: ancora '{alvo}' nao encontrada em {path}")
        # recua ate o inicio do bloco que contem a ancora
        inicio = html.rfind('<div class="tl-wrap mb-10">', 0, pos)
        if inicio == -1:
            sys.exit(f"erro: bloco da linha do tempo nao encontrado em {path}")
        html = html[:inicio] + novo + html[inicio:]
        path.write_text(html, encoding="utf-8")
        print(f"  {path.relative_to(ROOT).as_posix()}: cargo atual + freelance adicionados")


if __name__ == "__main__":
    main()
