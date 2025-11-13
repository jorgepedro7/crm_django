# Guia de Interface

## Layout global
- Todos os templates herdam `templates/base.html`, que fornece:
  - Navbar fixa com logotipo, links principais e estado de autenticação.
  - Fundo em gradiente escuro (`bg-slate-950`, `bg-gradient-to-br from-indigo-600/30`).
  - Estrutura central responsiva (`max-w-5xl`, `px-6`, `py-10`).
- Sidebar do dashboard usa cards (`rounded-2xl`, `border-slate-800/70`) e quick links.

## Paleta e tipografia
- Fundo: `bg-slate-900/950`.
- Borda: `border-slate-800/70`.
- Destaques: gradientes `from-indigo-500 via-blue-500 to-cyan-400`.
- Texto principal: `text-white`, auxiliares `text-slate-400`.
- Fonte: `Inter` (carregada via Google Fonts).

## Componentes padrão
- **Cards**: `rounded-3xl border border-slate-800/70 bg-slate-900/70`.
- **Botões primários**: gradiente azul (`bg-gradient-to-r from-indigo-500 ...`) com sombra.
- **Botões secundários**: `border border-slate-700` + `hover:border-indigo-400`.
- **Inputs**: `rounded-xl border border-slate-700 bg-slate-900/60 px-4 py-3 text-slate-100 focus:ring-2`.
- **Tabelas**: wrappers com `overflow-x-auto`, `divide-y divide-slate-800` e cabeçalhos `bg-slate-950/40`.

## Capturas de tela
| Tela | Arquivo |
| --- | --- |
| Home pública | `docs/screenshots/home.png` |
| Login | `docs/screenshots/login.png` |
| Dashboard | `docs/screenshots/dashboard.png` |
| Contas | `docs/screenshots/accounts.png` |
| Contatos | `docs/screenshots/contacts.png` |
| Leads | `docs/screenshots/leads.png` |
| Tarefas | `docs/screenshots/tasks.png` |
| Relatórios | `docs/screenshots/reports.png` |

Use-as em apresentações ou PRs para comunicar mudanças visuais. Sempre capture novamente após ajustes relevantes na UI (utilize o agente QA/Playwright para consistência).
