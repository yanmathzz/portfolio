<div align="center">
  <h1>Yan Matheus — Portfólio</h1>
  <p>Portfólio pessoal de desenvolvedor full-stack (TypeScript/JavaScript) — web, desktop e mobile, da arquitetura ao deploy.</p>

  <p>
    <img src="https://img.shields.io/badge/HTML5-estrutura-E34F26?style=flat-square&logo=html5&logoColor=white" alt="HTML5">
    <img src="https://img.shields.io/badge/CSS3-estiliza%C3%A7%C3%A3o-1572B6?style=flat-square&logo=css3&logoColor=white" alt="CSS3">
    <img src="https://img.shields.io/badge/JavaScript-intera%C3%A7%C3%B5es-F7DF1E?style=flat-square&logo=javascript&logoColor=black" alt="JavaScript">
    <img src="https://img.shields.io/badge/Tailwind-CDN-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white" alt="Tailwind CSS">
  </p>
</div>

---

## Visão geral

Este repositório contém o código-fonte do meu site pessoal, desenvolvido como uma aplicação estática para apresentar minha atuação profissional em:

- desenvolvimento full-stack (TypeScript, React, Node.js, PostgreSQL, Docker, Electron)
- aplicações web, desktop e mobile
- integrações com APIs fiscais brasileiras (SEFAZ: NF-e, CT-e, MDF-e)
- automação de processos (Python, RPA)
- projetos e artigos técnicos

O site foi pensado para funcionar como uma vitrine profissional direta, com navegação simples, identidade visual própria e organização clara do conteúdo.

---

## Seções do site

- `index.html` — apresentação principal e visão geral do perfil
- `about.html` — trajetória, experiência e contexto profissional
- `articles.html` — artigos e textos técnicos
- `projects.html` — projetos selecionados
- `uses.html` — ferramentas, ambientes e softwares que utilizo
- `hire.html` — página de contato para oportunidades e colaboração

---

## Destaques

- layout responsivo com foco em leitura e apresentação profissional
- tema visual consistente entre as páginas
- animações leves para complementar a experiência sem poluir a interface
- estrutura simples de manter e expandir
- organização voltada a portfólio técnico pessoal

---

## Stack utilizada

| Tecnologia | Função |
|---|---|
| HTML5 | Estrutura das páginas |
| CSS3 | Estilização e refinamento visual |
| JavaScript | Interações, animações e tema |
| Tailwind CSS | Utilitários visuais via CDN |

---

## Como executar localmente

Por ser um projeto estático, você pode visualizar o site de duas formas.

### Abrindo diretamente no navegador

Basta abrir o arquivo `index.html`.

### Servindo localmente

```powershell
cd C:\Users\ymath\portfolio
python -m http.server 5500
```

Depois, acesse:

```text
http://localhost:5500
```

---

## Estrutura do projeto

```text
portfolio/
├── en/                 # mesmas 6 páginas em inglês
├── images/
├── scripts/            # geradores e transformações (ver abaixo)
├── about.html
├── anim.js
├── articles.html
├── design.css          # tokens de cor e componentes
├── favicon.svg
├── hire.html
├── index.html
├── og-image.png        # cartão de compartilhamento (1200×630)
├── projects.html
├── robots.txt
├── sitemap.xml
├── theme.js            # paleta da marca (Tailwind)
├── uses.html
└── README.md
```

### Tema e cores

A identidade visual mora em dois lugares, e só neles:

- `theme.js` — remapeia as escalas de cor do Tailwind para a paleta da marca.
  As páginas seguem usando classes como `text-teal-500`; o nome é apelido
  histórico, a cor que sai é a da marca.
- `design.css` — o bloco `:root` guarda os tokens (`--accent-color`,
  `--accent-soft`, `--surface-0`…) usados pelos componentes próprios.

Trocar a identidade do site é editar esses dois arquivos. Nenhuma cor deve ser
escrita direto no HTML.

### Scripts

Rodar a partir da raiz do projeto:

| Script | Para que serve |
|---|---|
| `scripts/build_en.py` | Recria o esqueleto das páginas em inglês quando a **estrutura** das PT muda |
| `scripts/translate_en.py` | Aplica as traduções em `en/`; acusa erro se alguma frase não for encontrada |
| `scripts/make_assets.py` | Gera favicon, imagem social, `robots.txt` e `sitemap.xml` |
| `scripts/add_meta.py` | Injeta favicon e tags Open Graph nas 12 páginas |
| `scripts/apply_theme.py` | Propaga o tema (usado na migração; idempotente) |
| `scripts/sweep_colors.py` | Troca cores cravadas à mão pelos tokens |
| `scripts/update_projects.py` | Mantém a galeria de projetos em paridade entre PT e EN |

---

## Objetivo do projeto

Este portfólio foi criado para centralizar minha presença profissional na web e apresentar, de forma objetiva, minha experiência como desenvolvedor full-stack: sistemas de gestão em produção, integrações fiscais com a SEFAZ (NF-e, CT-e, MDF-e), aplicações desktop com Electron, apps mobile com React Native/Expo e automação de processos com Python.

---

## Contato

- E-mail: `ymatheus706@gmail.com`
- LinkedIn: [Yan Matheus Pinheiro Cezario](https://www.linkedin.com/in/yan-matheus-361b6b235)
- GitHub: [yanmathzz](https://github.com/yanmathzz)

---

## Observações

Este repositório representa meu portfólio pessoal e é mantido como vitrine profissional.
