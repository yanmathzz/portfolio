"""Traduz o texto visivel das paginas em en/ para ingles.

As paginas PT misturam acento cru (about.html) com entidade HTML (index.html usa
&ccedil;, &atilde;...). Por isso cada frase vira um regex que aceita as duas
formas, e quebras de linha com indentacao viram \\s+ — assim um paragrafo
quebrado em varias linhas continua casando.

Toda frase nao encontrada e reportada como MISS e o script sai com erro: uma
traducao que falha em silencio deixaria portugues solto na pagina em ingles.

    python scripts/translate_en.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN = ROOT / "en"

# acentos e simbolos que podem aparecer crus ou como entidade
ENTITIES = {
    "á": "aacute", "à": "agrave", "ã": "atilde", "â": "acirc",
    "é": "eacute", "ê": "ecirc", "í": "iacute", "ó": "oacute",
    "õ": "otilde", "ô": "ocirc", "ú": "uacute", "ç": "ccedil",
    "Á": "Aacute", "À": "Agrave", "Ã": "Atilde", "É": "Eacute",
    "Í": "Iacute", "Ó": "Oacute", "Ú": "Uacute", "Ç": "Ccedil",
    "—": "mdash", "–": "ndash", "·": "middot", "º": "ordm",
    "ª": "ordf", "&": "amp", "“": "ldquo", "”": "rdquo",
}


def to_pattern(text: str) -> re.Pattern:
    out = []
    for ch in text:
        if ch.isspace():
            out.append(r"\s+")
        elif ch in ENTITIES:
            out.append(f"(?:{re.escape(ch)}|&{ENTITIES[ch]};)")
        else:
            out.append(re.escape(ch))
    # colapsa \s+ repetidos
    return re.compile(re.sub(r"(?:\\s\+)+", r"\\s+", "".join(out)))


COMMON = {
    "Todos os direitos reservados.": "All rights reserved.",
    "Alternar tema": "Toggle theme",
    "Início": "Home",
}

PAGES: dict[str, dict[str, str]] = {
    "index": {
        "Disponível para projetos": "Available for projects",
        "Desenvolvedor Full-Stack e Engenheiro de Computação baseado em Belém, Pará.":
            "Full-Stack Developer and Computer Engineer based in Belém, Brazil.",
        "Sou Yan Matheus, desenvolvedor full-stack com experiência de ponta a ponta em aplicações web, desktop e mobile — da arquitetura ao deploy, incluindo integrações com as APIs fiscais brasileiras (SEFAZ: NF-e, CT-e e MDF-e).":
            "I'm Yan Matheus, a full-stack developer with end-to-end experience in web, desktop and mobile applications — from architecture to deployment, including integrations with the Brazilian tax APIs (SEFAZ: NF-e, CT-e and MDF-e).",
        "Minha stack principal é TypeScript, React, Node.js, PostgreSQL, Docker e Electron. Venho de uma base sólida em infraestrutura e automação com Python, e fui 3º lugar no Amazon Hacking 2025 como Lead Developer.":
            "My core stack is TypeScript, React, Node.js, PostgreSQL, Docker and Electron. I come from a solid background in infrastructure and automation with Python, and placed 3rd at Amazon Hacking 2025 as Lead Developer.",
        "E-mail": "Email",
        "Como automatizei processos repetitivos com Python e AutoIt":
            "How I automated repetitive processes with Python and AutoIt",
        "10 de janeiro de 2026": "January 10, 2026",
        "Como construí RPAs que eliminaram horas de trabalho manual — da captura de tela à integração com GLPI e Microsoft 365.":
            "How I built RPAs that removed hours of manual work — from screen capture to GLPI and Microsoft 365 integration.",
        "Ler artigo": "Read article",
        "Administrando servidores Linux em ambiente corporativo":
            "Running Linux servers in a corporate environment",
        "22 de novembro de 2025": "November 22, 2025",
        "Lições práticas de gerenciar servidores Linux em produção — segurança, monitoramento e boas práticas aprendidas da maneira difícil.":
            "Practical lessons from running Linux servers in production — security, monitoring and best practices learned the hard way.",
        "Integração de Service Desk: GLPI + Microsoft 365":
            "Service desk integration: GLPI + Microsoft 365",
        "5 de outubro de 2025": "October 5, 2025",
        "Como conectei o GLPI ao Microsoft 365 para automatizar fluxos de atendimento e gerar relatórios de tickets diretamente por e-mail.":
            "How I connected GLPI to Microsoft 365 to automate support flows and send ticket reports straight by email.",
        "DHCP e DNS: guia prático para redes corporativas":
            "DHCP and DNS: a practical guide for corporate networks",
        "18 de agosto de 2025": "August 18, 2025",
        "Configuração e troubleshooting de DHCP e DNS em ambientes Windows Server, com exemplos reais e armadilhas comuns a evitar.":
            "Configuring and troubleshooting DHCP and DNS on Windows Server, with real examples and common pitfalls to avoid.",
        "Ver todos os artigos": "View all articles",
        "Contato": "Contact",
        "Vamos construir algo util.": "Let's build something useful.",
        "Se voce precisa organizar processos, integrar sistemas ou melhorar sua operacao, posso ajudar a desenhar e executar a solucao.":
            "If you need to organise processes, integrate systems or improve your operation, I can help design and deliver the solution.",
        "Falar sobre um projeto": "Discuss a project",
        "Amazon Informatica": "Amazon Informática",
        "Analista de Suporte e Automação": "Support and Automation Analyst",
        "TRT 8a Regiao": "Labour Court (TRT 8th Region)",
        "Estagiario de Suporte de TI": "IT Support Intern",
        "Bacharelado em Engenharia de Computacao": "BSc in Computer Engineering",
        "Ver experiencia completa": "See full experience",
    },
    "about": {
        "Construo aplicações web, desktop e mobile de ponta a ponta — da arquitetura ao deploy.":
            "I build web, desktop and mobile applications end to end — from architecture to deployment.",
        "Desde cedo fui atraído por tecnologia — não só pelo fascínio de como as coisas funcionam, mas pela possibilidade de fazer com que funcionem melhor. Essa curiosidade me levou à Engenharia de Computação no CESUPA, onde aprendi a pensar em sistemas, algoritmos e arquiteturas com profundidade.":
            "I was drawn to technology early on — not only by the fascination of how things work, but by the chance to make them work better. That curiosity led me to Computer Engineering at CESUPA, where I learned to think deeply about systems, algorithms and architecture.",
        "Minha trajetória começou pela infraestrutura: dois anos como estagiário de TI no Tribunal Regional do Trabalho da 8ª Região, dando suporte a cerca de 500 usuários, e depois na Amazon Informática, criando automações com Python e AutoIt, integrações com GLPI e administrando ambientes Microsoft 365. Essa base me ensinou a construir software que precisa funcionar em operação real — e que reduz trabalho manual de verdade.":
            "My path started in infrastructure: two years as an IT intern at the 8th Region Labour Court, supporting around 500 users, and later at Amazon Informática, building automations with Python and AutoIt, GLPI integrations and administering Microsoft 365 environments. That grounding taught me to build software that has to work in real operations — and that genuinely removes manual work.",
        "Hoje atuo como desenvolvedor full-stack, cuidando de todo o ciclo de vida de sistemas em produção — do levantamento de requisitos à arquitetura, deploy e suporte. Isso inclui integrações com as APIs fiscais brasileiras (SEFAZ) para emissão de NF-e, CT-e e MDF-e — um domínio que exige alta confiabilidade e conformidade regulatória.":
            "Today I work as a full-stack developer, owning the full lifecycle of systems in production — from requirements to architecture, deployment and support. That includes integrations with the Brazilian tax APIs (SEFAZ) for issuing NF-e, CT-e and MDF-e documents — a domain that demands high reliability and regulatory compliance.",
        "Também desenvolvi de forma independente o aplicativo mobile Eletransol, hoje em uso em produção, e preparo o lançamento dele como app multiplataforma na App Store e no Google Play. Minha stack principal: TypeScript, React, Node.js, PostgreSQL, Docker e Electron.":
            "I also independently built the Eletransol mobile app, now running in production, and I'm preparing its release as a cross-platform app on the App Store and Google Play. My core stack: TypeScript, React, Node.js, PostgreSQL, Docker and Electron.",
        "Fora do trabalho, contribuo com projetos open source, participo de hackathons — fui 3º lugar no Amazon Hacking 2025 como Lead Developer, em competição apoiada por Vale, Accenture e Wipro — e estudo continuamente, hoje aprofundando desenvolvimento mobile e francês (meta TCF/TEF).":
            "Outside work I contribute to open source and take part in hackathons — I placed 3rd at Amazon Hacking 2025 as Lead Developer, in a competition backed by Vale, Accenture and Wipro — and I keep studying, currently going deeper into mobile development and French (aiming for TCF/TEF).",
        "Experiência Profissional": "Professional Experience",
        "Amazon Informática — Belém, PA": "Amazon Informática — Belém, Brazil",
        "Ago 2025 – Jan 2026": "Aug 2025 – Jan 2026",
        "Analista de Suporte Computacional e Automação": "Computer Support and Automation Analyst",
        "Scripts Python para geração automatizada de relatórios e integração de dados com GLPI, reduzindo em ~35% o tempo de processamento manual.":
            "Python scripts for automated report generation and data integration with GLPI, cutting manual processing time by around 35%.",
        "Soluções de RPA com Python e AutoIt para otimização de processos internos e redução de erros operacionais.":
            "RPA solutions with Python and AutoIt to streamline internal processes and reduce operational errors.",
        "Administração de ambientes Microsoft 365 (Intune, gestão de endpoints).":
            "Administration of Microsoft 365 environments (Intune, endpoint management).",
        "Melhorias de performance e segurança em infraestrutura de TI.":
            "Performance and security improvements across IT infrastructure.",
        "TRT 8ª Região — Belém, PA": "Labour Court, 8th Region — Belém, Brazil",
        "Jul 2023 – Jul 2025": "Jul 2023 – Jul 2025",
        "Estagiário de Suporte de TI": "IT Support Intern",
        "Suporte técnico remoto e presencial para hardware, softwares e sistemas internos.":
            "Remote and on-site technical support for hardware, software and internal systems.",
        "Atendimento e resolução de chamados de suporte com gestão de tickets.":
            "Handling and resolving support requests with ticket management.",
        "Apoio à infraestrutura de eventos institucionais e colaboração em equipe.":
            "Supporting the infrastructure of institutional events and collaborating across the team.",
        "Identificação e resolução de problemas técnicos para eficiência operacional.":
            "Identifying and resolving technical problems to keep operations efficient.",
        "Educação": "Education",
        "CESUPA — Centro Universitário do Estado do Pará":
            "CESUPA — University Centre of the State of Pará",
        "Bacharelado em Engenharia de Computação": "BSc in Computer Engineering",
        "TCC: Revisão sistemática de boas práticas para a otimização da produção siderúrgica com gêmeos digitais.":
            "Thesis: a systematic review of best practices for optimising steel production with digital twins.",
        "Licenças &amp; Certificações": "Licenses &amp; Certifications",
        "Udemy · Concluído em 12/08/2025 · 26h": "Udemy · Completed 12 Aug 2025 · 26h",
        "Udemy · Concluído em 16/08/2025 · 37,5h": "Udemy · Completed 16 Aug 2025 · 37.5h",
        "Microsoft · Concluído em 08/2025": "Microsoft · Completed Aug 2025",
        "PowerShell/Bash/Python, Gestão de Contas, Backup, Restore, Troubleshooting, Windows/Linux/macOS.":
            "PowerShell/Bash/Python, account management, backup, restore, troubleshooting, Windows/Linux/macOS.",
        "Administração de Endpoints, Microsoft 365, Windows Client, Microsoft Intune.":
            "Endpoint administration, Microsoft 365, Windows Client, Microsoft Intune.",
        "Análise e Visualização de Dados com Python": "Data Analysis and Visualisation with Python",
        "Microsoft · Concluído em 2026": "Microsoft · Completed 2026",
        "Análise de dados, visualização e bibliotecas do ecossistema Python.":
            "Data analysis, visualisation and libraries from the Python ecosystem.",
        "Fundamentos de SQL, modelagem e consulta de bancos de dados relacionais.":
            "SQL fundamentals, modelling and querying relational databases.",
        "Produtividade com Excel e uso de IA (Copilot) em fluxos de trabalho.":
            "Productivity with Excel and using AI (Copilot) in day-to-day workflows.",
        "Idiomas": "Languages",
        "Português": "Portuguese",
        "· nativo": "· native",
        "Inglês": "English",
        "· proficiência profissional": "· professional working proficiency",
        "Francês": "French",
        "· básico, em estudo (meta TCF/TEF)": "· basic, currently studying (aiming for TCF/TEF)",
    },
    "projects": {
        "Projetos que conectam software, automação e infraestrutura com foco em uso real.":
            "Projects that connect software, automation and infrastructure, built for real use.",
        "Esta página reúne trabalhos que representam bem a minha forma de construir: pensar no problema, desenhar uma solução enxuta e entregar algo que funcione de verdade no contexto do usuário.":
            "This page gathers work that reflects how I build: understand the problem, design a lean solution and ship something that genuinely works in the user's context.",
        "Tem projeto de produto, ferramenta interna, automação e experimentos técnicos — sempre com atenção à clareza, manutenção e experiência final.":
            "There are product projects, internal tools, automation and technical experiments — always with an eye on clarity, maintainability and the end experience.",
        "Ver perfil no GitHub": "View GitHub profile",
        "Open source + projetos autorais": "Open source + personal projects",
        "Foco técnico": "Technical focus",
        "Interfaces úteis, automação de processos, integrações e ferramentas que ajudam operações reais.":
            "Useful interfaces, process automation, integrations and tools that support real operations.",
        "Stack recorrente": "Recurring stack",
        "TypeScript, React, Node.js, PostgreSQL, Docker e Electron — com Python para automação e dados.":
            "TypeScript, React, Node.js, PostgreSQL, Docker and Electron — with Python for automation and data.",
        "Critério": "Criteria",
        "Aqui entram projetos que mostram raciocínio, execução e capacidade de transformar ideia em produto utilizável.":
            "What makes the cut: projects that show reasoning, execution and the ability to turn an idea into a usable product.",
        "Projetos em destaque": "Featured projects",
        "Uma seleção de trabalhos que mostram bem minha combinação de produto, código e visão operacional.":
            "A selection of work that shows my mix of product thinking, code and operational awareness.",
        "Mobile app · Em produção": "Mobile app · In production",
        "Aplicativo mobile que desenvolvi de forma independente e que hoje está em uso em produção, integrado à operação diária de uma empresa. Em preparação para lançamento multiplataforma (iOS e Android) na App Store e Google Play.":
            "A mobile app I built independently, now running in production and integrated into a company's daily operation. Currently being prepared for a cross-platform release (iOS and Android) on the App Store and Google Play.",
        "Produto comercial · código privado": "Commercial product · private code",
        "Full-stack · Open source": "Full-stack · Open source",
        "Plataforma de gestão financeira pessoal com autenticação segura, dashboard interativo e visualização de dados. Aplicação full-stack totalmente containerizada com Docker, do banco ao frontend.":
            "A personal finance platform with secure authentication, an interactive dashboard and data visualisation. A full-stack application fully containerised with Docker, from database to frontend.",
        "Desktop app · Em desenvolvimento": "Desktop app · In development",
        "Sistema desktop de gestão para farmácias, com interface moderna em glassmorphism e foco em usabilidade para o operador de balcão. Reutiliza a mesma arquitetura desktop dos sistemas que mantenho em produção.":
            "A desktop management system for pharmacies, with a modern glassmorphism interface focused on counter-staff usability. It reuses the same desktop architecture as the systems I maintain in production.",
        "Em desenvolvimento ativo": "In active development",
        "Site enterprise · Em desenvolvimento": "Enterprise site · In development",
        "Site institucional B2B com hero em vídeo cinematográfico, animações de alto acabamento e apresentação para investidores. Foco em performance, SEO e posicionamento premium.":
            "A B2B corporate site with a cinematic video hero, polished animations and an investor-facing presentation. Focused on performance, SEO and premium positioning.",
        "Editor de notas em Markdown para Windows, com leitura direta do sistema de arquivos, preview em tempo real, busca instantânea e auto-save. Um projeto focado em simplicidade de uso e performance local.":
            "A Markdown note editor for Windows that reads straight from the file system, with live preview, instant search and auto-save. Built around ease of use and local performance.",
        "3º lugar · Amazon Hacking 2025": "3rd place · Amazon Hacking 2025",
        "TEP — Tokenização Empresarial Paraense": "TEP — Business Tokenisation for Pará",
        "Plataforma blockchain de tokenização de produtos da bioeconomia amazônica, voltada à inclusão financeira de micro e pequenas empresas. Atuei como Lead Developer — arquitetura técnica e desenvolvimento full-stack. Competição apoiada por Vale, Accenture e Wipro.":
            "A blockchain platform for tokenising Amazon bioeconomy products, aimed at financial inclusion for micro and small businesses. I served as Lead Developer — technical architecture and full-stack development. Competition backed by Vale, Accenture and Wipro.",
        "Recriação da interface da Netflix com consumo de API, organização por categorias e foco em experiência visual. Um estudo importante de componentização e interface orientada a conteúdo.":
            "A recreation of the Netflix interface consuming an API, organised by category and focused on visual experience. A valuable study in componentisation and content-driven UI.",
        "Análise de dados": "Data analysis",
        "Ferramenta para analisar dados do LinkedIn e transformar informações de perfil, rede ou atividade em uma visão mais clara para acompanhamento profissional.":
            "A tool that analyses LinkedIn data and turns profile, network and activity information into a clearer view for professional tracking.",
        "Análise": "Analysis",
        "Gerenciador de tarefas com visual de SaaS premium: quadro kanban, dark mode e interface construída em CSS3 puro, com backend em Flask e SQLAlchemy.":
            "A task manager with a premium SaaS look: kanban board, dark mode and an interface built in pure CSS3, backed by Flask and SQLAlchemy.",
        "Ferramenta operacional": "Operational tool",
        "Aplicação desktop em Python para acompanhar alterações em pastas, identificar arquivos novos, modificados e removidos, manter histórico em SQLite e exportar relatórios em CSV.":
            "A Python desktop application that watches folders for changes, flags new, modified and deleted files, keeps history in SQLite and exports CSV reports.",
        "Dados + automação": "Data + automation",
        "API serverless para extração de produtos da Amazon usando Puppeteer, com persistência em DynamoDB e pipeline de deploy na AWS. Um bom exemplo de automação orientada a dados.":
            "A serverless API that extracts Amazon product data using Puppeteer, persisting to DynamoDB with an AWS deployment pipeline. A solid example of data-driven automation.",
    },
    "articles": {
        "Escrevendo sobre software, infraestrutura e automacao.":
            "Writing about software, infrastructure and automation.",
        "Meus pensamentos organizados sobre tecnologia, administracao de sistemas, boas praticas de desenvolvimento e licoes aprendidas ao longo da carreira. Em formato longo, porque algumas ideias merecem mais espaco do que um tweet.":
            "My organised thoughts on technology, systems administration, development best practices and lessons learned along the way. Long form, because some ideas deserve more room than a tweet.",
        "4 artigos": "4 articles",
        "Como automatizei processos repetitivos com Python e AutoIt":
            "How I automated repetitive processes with Python and AutoIt",
        "10 de janeiro de 2026": "January 10, 2026",
        "Explorando como construí RPAs que eliminaram horas de trabalho manual — da captura de tela à integração com GLPI e Microsoft 365. Aprendi que automatizar bem exige mais entendimento do processo do que do código.":
            "Exploring how I built RPAs that removed hours of manual work — from screen capture to GLPI and Microsoft 365 integration. I learned that automating well demands more understanding of the process than of the code.",
        "Abrir leitura": "Open article",
        "10 jan 2026": "10 Jan 2026",
        "Administrando servidores Linux em ambiente corporativo":
            "Running Linux servers in a corporate environment",
        "22 de novembro de 2025": "November 22, 2025",
        "Lições práticas de gerenciar servidores Linux em produção — segurança, monitoramento e boas práticas aprendidas da maneira difícil. O que ninguém te conta antes de você colocar um servidor em produção.":
            "Practical lessons from running Linux servers in production — security, monitoring and best practices learned the hard way. What nobody tells you before you put a server live.",
        "22 nov 2025": "22 Nov 2025",
        "Integração de Service Desk: GLPI + Microsoft 365":
            "Service desk integration: GLPI + Microsoft 365",
        "5 de outubro de 2025": "October 5, 2025",
        "Como conectei o sistema de tickets GLPI com Microsoft 365 para automatizar fluxos de atendimento e gerar relatórios automáticos por e-mail. Uma integração que economizou horas de trabalho por semana.":
            "How I connected the GLPI ticketing system to Microsoft 365 to automate support flows and send automatic reports by email. An integration that saved hours of work every week.",
        "5 out 2025": "5 Oct 2025",
        "DHCP e DNS: guia prático para redes corporativas":
            "DHCP and DNS: a practical guide for corporate networks",
        "18 de agosto de 2025": "August 18, 2025",
        "Um guia direto ao ponto sobre configuração e troubleshooting de DHCP e DNS em ambientes Windows Server, baseado em experiências reais de suporte. Inclui os erros mais comuns e como resolvê-los.":
            "A straight-to-the-point guide to configuring and troubleshooting DHCP and DNS on Windows Server, based on real support experience. Includes the most common failures and how to fix them.",
        "18 ago 2025": "18 Aug 2025",
        "Comecei mapeando cada etapa manual antes de escrever uma linha de código. Isso evitou automatizar exceções, reduziu retrabalho e deixou claro quais partes precisavam de Python para regra de negócio e quais dependiam do AutoIt para interagir com sistemas legados sem API.":
            "I started by mapping every manual step before writing a line of code. That kept me from automating edge cases, cut rework and made clear which parts needed Python for business rules and which depended on AutoIt to drive legacy systems with no API.",
        "O ganho real veio quando parei de pensar em script isolado e passei a tratar o fluxo como produto interno: logs, validações, checkpoints e reexecução segura. Quando um robô falha silenciosamente, ele cria mais trabalho do que remove.":
            "The real gain came when I stopped thinking in isolated scripts and started treating the flow as an internal product: logs, validation, checkpoints and safe re-runs. A bot that fails silently creates more work than it removes.",
        "No fim, a automação funcionou porque respeitou o processo da equipe. O código foi importante, mas o diferencial foi transformar uma rotina frágil em algo previsível, auditável e simples de operar.":
            "In the end the automation worked because it respected the team's process. The code mattered, but the difference was turning a fragile routine into something predictable, auditable and simple to run.",
        "Servidor em produção raramente falha por um único motivo. Normalmente o problema nasce da combinação entre permissão mal ajustada, observabilidade fraca e uma mudança pequena que passou sem validação. Foi isso que me fez adotar checklist simples para deploy, backup e rollback.":
            "A production server rarely fails for a single reason. The problem usually grows out of a badly set permission, weak observability and one small change that slipped through unvalidated. That's what led me to adopt simple checklists for deploy, backup and rollback.",
        "Também aprendi que padronização vale mais do que heroísmo. Nome consistente de serviços, logs centralizados e monitoramento básico economizam muito mais tempo do que tentar resolver tudo no improviso quando a pressão aparece.":
            "I also learned that standardisation beats heroics. Consistent service naming, centralised logs and basic monitoring save far more time than improvising your way out once the pressure hits.",
        "Em ambiente corporativo, estabilidade comunica maturidade. Um servidor bem cuidado não chama atenção, e isso costuma ser o melhor sinal de que a infraestrutura está fazendo o trabalho dela.":
            "In a corporate setting, stability signals maturity. A well-kept server draws no attention, and that is usually the best sign the infrastructure is doing its job.",
        "Integração de service desk não é apenas conectar duas ferramentas. O desafio real foi manter o contexto do atendimento, reduzir duplicidade e garantir que o fluxo automático não escondesse informação importante para a equipe.":
            "Service desk integration is not just wiring two tools together. The real challenge was preserving the context of each request, cutting duplication and making sure the automated flow didn't hide information the team needed.",
        "Centralizei disparos e respostas em pontos claros do processo: abertura, atualização e fechamento. Isso ajudou a equipe a confiar no fluxo e criou uma trilha mais limpa para acompanhamento, relatórios e auditoria.":
            "I centralised triggers and responses at clear points in the process: opening, updating and closing. That helped the team trust the flow and left a cleaner trail for tracking, reporting and auditing.",
        "Quando integração funciona bem, ela deixa de parecer integração. O usuário percebe menos fricção, o time perde menos tempo com tarefa operacional e o service desk fica mais próximo do que deveria ser: resolução rápida e organizada.":
            "When an integration works well it stops looking like an integration. Users feel less friction, the team loses less time to operational chores, and the service desk gets closer to what it should be: fast, organised resolution.",
        "Boa parte dos chamados de rede parece complexa até você testar o básico com disciplina. Escopo de DHCP, reserva indevida, TTL mal compreendido e zona desatualizada continuam sendo fontes clássicas de falha em ambientes Windows Server.":
            "Most network tickets look complex until you test the basics with discipline. DHCP scope, a stray reservation, a misunderstood TTL and a stale zone are still classic sources of failure on Windows Server.",
        "O que mais ajuda no troubleshooting é seguir uma ordem fixa: confirmar IP recebido, gateway, resolução local, resolução externa e somente depois avançar para hipóteses maiores. Isso reduz tempo de diagnóstico e evita mexer em configuração desnecessariamente.":
            "What helps most in troubleshooting is following a fixed order: confirm the leased IP, the gateway, local resolution, external resolution — and only then move to bigger hypotheses. It shortens diagnosis and avoids changing configuration for no reason.",
        "Redes corporativas ficam muito mais saudáveis quando documentação acompanha a operação. Uma boa tabela de escopos, zonas e exceções costuma valer mais do que memória de equipe.":
            "Corporate networks get far healthier when documentation keeps pace with operations. A good table of scopes, zones and exceptions is usually worth more than team memory.",
        "Redes": "Networking",
    },
    "uses": {
        "Ferramentas, sistemas e ambientes que fazem parte do meu dia a dia.":
            "Tools, systems and environments that are part of my day to day.",
        "Um resumo direto do stack que eu realmente uso para operar infraestrutura, automatizar rotinas e desenvolver solucoes com consistencia.":
            "A straight summary of the stack I actually use to run infrastructure, automate routines and build software consistently.",
        "Minha stack": "My stack",
        "As tecnologias que eu mais uso para desenvolver, operar infraestrutura e automatizar processos no dia a dia.":
            "The technologies I reach for most when building, running infrastructure and automating processes.",
        "Sistemas": "Systems",
        "Desenvolvimento": "Development",
        "Infraestrutura": "Infrastructure",
        "Virtualização": "Virtualisation",
        "Operação": "Operations",
        "Ferramentas": "Tools",
    },
    "hire": {
        "Resposta em até 24h": "Reply within 24h",
        "Vamos construir algo útil, robusto e bem resolvido.":
            "Let's build something useful, robust and well resolved.",
        "Sou desenvolvedor full-stack e construo aplicações web, desktop e mobile de ponta a ponta — da arquitetura ao deploy, incluindo sistemas em produção com integrações fiscais SEFAZ.":
            "I'm a full-stack developer and I build web, desktop and mobile applications end to end — from architecture to deployment, including production systems with SEFAZ tax integrations.",
        "Se você precisa de um sistema completo, de uma integração fiscal (NF-e, CT-e, MDF-e), de automatizar processos ou de uma ferramenta interna sob medida, podemos conversar e entender o melhor caminho. Confortável com trabalho remoto e assíncrono.":
            "If you need a complete system, a tax integration (NF-e, CT-e, MDF-e), process automation or a bespoke internal tool, let's talk and find the best route. Comfortable with remote and async work.",
        "Contato direto": "Direct contact",
        "E-mail": "Email",
        "Escrever": "Write",
        "Ideal para propostas detalhadas, escopo do projeto e contexto técnico.":
            "Best for detailed proposals, project scope and technical context.",
        "Conversar": "Chat",
        "Melhor canal para alinhamento inicial, troca rápida e conversa objetiva.":
            "The best channel for a first alignment, quick exchanges and getting to the point.",
        "Perfil": "Profile",
        "Bom para networking, histórico profissional e contexto de atuação.":
            "Good for networking, career history and background.",
        "Como posso ajudar": "How I can help",
        "Áreas em que eu consigo contribuir com mais profundidade hoje.":
            "The areas where I can contribute most deeply today.",
        "Desenvolvimento Full-Stack": "Full-Stack Development",
        "Aplicações web, desktop (Electron) e mobile (React Native) completas — do levantamento de requisitos e modelagem de dados ao deploy com Docker e suporte em produção.":
            "Complete web, desktop (Electron) and mobile (React Native) applications — from requirements and data modelling to Docker deployment and production support.",
        "Integrações Fiscais (SEFAZ)": "Tax Integrations (SEFAZ)",
        "Emissão e gestão de documentos fiscais eletrônicos integrados aos sistemas da empresa — um domínio que exige alta confiabilidade e conformidade regulatória, e que mantenho em produção hoje.":
            "Issuing and managing electronic tax documents integrated into company systems — a domain that demands high reliability and regulatory compliance, and one I keep running in production today.",
        "Automacao de Processos": "Process Automation",
        "Estruturo automações para reduzir trabalho manual, padronizar tarefas e conectar sistemas que ainda dependem de operação repetitiva.":
            "I build automations that cut manual work, standardise tasks and connect systems still stuck on repetitive operation.",
        "Ferramentas Internas e Integracoes": "Internal Tools and Integrations",
        "Desenvolvo soluções sob medida para times que precisam ganhar velocidade com software simples, confiável e fácil de manter.":
            "I build bespoke solutions for teams that need to move faster with software that is simple, reliable and easy to maintain.",
        "Como eu gosto de trabalhar": "How I like to work",
        "Entender antes de construir": "Understand before building",
        "Começamos pelo problema real, pelo impacto no time e pelo que precisa melhorar primeiro.":
            "We start from the real problem, its impact on the team and what needs to improve first.",
        "Definir um plano enxuto": "Agree a lean plan",
        "Eu prefiro escopo claro, entregas pequenas e comunicação direta para manter ritmo e previsibilidade.":
            "I prefer clear scope, small deliveries and direct communication to keep pace and predictability.",
        "Executar com foco em manutenção": "Build for maintenance",
        "A ideia não é só entregar rápido, mas deixar algo confiável, documentado e fácil de evoluir depois.":
            "The point isn't only to ship fast, but to leave something reliable, documented and easy to evolve later.",
        "Tem algo em mente?": "Got something in mind?",
        "Me envie um resumo do que você precisa. Se eu puder ajudar, respondo com o melhor formato para seguir.":
            "Send me a summary of what you need. If I can help, I'll reply with the best way forward.",
        "Enviar e-mail": "Send email",
        "Abrir WhatsApp": "Open WhatsApp",
    },
}

# titulos das paginas (<title> e meta description)
META = {
    "index": [
        ("Yan Matheus — Desenvolvedor Full-Stack (TypeScript/JavaScript) e Engenheiro de Computação baseado em Belém, Pará. Web, desktop e mobile, da arquitetura ao deploy.",
         "Yan Matheus — Full-Stack Developer (TypeScript/JavaScript) and Computer Engineer based in Belém, Brazil. Web, desktop and mobile, from architecture to deployment."),
    ],
    "about": [
        ("About — Yan Matheus", "About — Yan Matheus"),
        ("Sobre Yan Matheus — Desenvolvedor Full-Stack (TypeScript/JavaScript) e Engenheiro de Computação. Web, desktop e mobile, da arquitetura ao deploy.",
         "About Yan Matheus — Full-Stack Developer (TypeScript/JavaScript) and Computer Engineer. Web, desktop and mobile, from architecture to deployment."),
    ],
    "projects": [
        ("Projetos de Yan Matheus em software, infraestrutura, automação e ferramentas internas.",
         "Yan Matheus's projects across software, infrastructure, automation and internal tools."),
    ],
    "articles": [
        ("Artigos de Yan Matheus sobre software, infraestrutura e automação.",
         "Articles by Yan Matheus on software, infrastructure and automation."),
    ],
    "uses": [
        ("Software e ferramentas que Yan Matheus usa no dia a dia.",
         "Software and tools Yan Matheus uses day to day."),
    ],
    "hire": [
        ("Contratar Yan Matheus — Desenvolvedor Full-Stack (TypeScript/JavaScript) disponível para projetos web, desktop e mobile, incluindo integrações fiscais SEFAZ.",
         "Hire Yan Matheus — Full-Stack Developer (TypeScript/JavaScript) available for web, desktop and mobile projects, including SEFAZ tax integrations."),
    ],
}


def main() -> None:
    misses: list[str] = []
    for page, table in PAGES.items():
        path = EN / f"{page}.html"
        html = path.read_text(encoding="utf-8")
        # COMMON e best-effort: sao rotulos que nem toda pagina tem
        pairs = [(pt, en, True) for pt, en in list(META.get(page, [])) + list(table.items())]
        pairs += [(pt, en, False) for pt, en in COMMON.items()]
        for pt, en, required in pairs:
            pat = to_pattern(pt)
            html, n = pat.subn(lambda _m, e=en: e, html)
            if n == 0 and required:
                misses.append(f"{page}: {pt[:70]}")
        path.write_text(html, encoding="utf-8")
        print(f"  traduzido: en/{page}.html")

    if misses:
        print(f"\n{len(misses)} frase(s) NAO encontradas:")
        for m in misses:
            print("  MISS", m)
        sys.exit(1)
    print("\ntodas as frases foram substituidas")


if __name__ == "__main__":
    main()
