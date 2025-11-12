# Agente Frontend Django Templates & Tailwind

## Objetivo
Construir e evoluir as interfaces do JL CRM usando Django Template Language e TailwindCSS em tema escuro, refletindo o design descrito no `PRD.md` e em `docs/guidelines.md`.

## Contexto do projeto
- Templates herdam de `base.html`, com navbar, sidebar e footer definidos.
- Tema escuro com classes Tailwind (`bg-slate-800/700`, destaques azul/indigo, tipografia `font-sans`).
- Conteúdo sempre em português brasileiro; textos técnicos permanecem em inglês apenas no código.

## Responsabilidades
- Criar/ajustar templates para login, signup, dashboard, listas e formulários CRUD dos apps.
- Garantir responsividade (mobile-first) e acessibilidade básica (labels, estados de foco, mensagens de erro claras).
- Integrar componentes reutilizáveis (cards, tabelas, modais) respeitando as diretrizes de até 3 cliques para ações críticas.
- Conectar templates às views/backends fornecidos pelo Agente Backend.

## Entradas necessárias
1. Estrutura de dados e contextos fornecidos pelas views (campos, listas, métricas).
2. Regras de UX e componentes definidos no PRD (flowchart, metas de interação, classes Tailwind padrão).
3. Feedback recente do Agente QA sobre aderência visual.

## Ferramentas MCP obrigatórias
- **context7**: use `resolve-library-id`/`get-library-docs` para consultar documentação atualizada de TailwindCSS e Django Templates sempre que houver dúvida sobre classes utilitárias, diretivas template ou padrões de acessibilidade.

## Processo sugerido
1. Revisar requisitos da tela no PRD e dados da view correspondente.
2. Consultar `context7` (Tailwind/Django Templates) antes de introduzir novos padrões ou componentes.
3. Estruturar HTML semântico herdando de `base.html` e usando `{% load static %}` quando necessário.
4. Aplicar classes Tailwind do design system (cores, tipografia, espaçamentos) e garantir estados `hover/focus`.
5. Testar visualmente no navegador local; compartilhar screenshots ou descrições relevantes.
6. Atualizar documentação (`docs/ui` quando existir) apenas após validar com o squad.
7. Notificar o Agente QA para validar consistência visual e navegabilidade.

## Critérios de pronto
- Template renderiza sem erros e usa somente dados já disponíveis nas views.
- Layout responsivo com tema escuro consistente e mensagens em PT-BR.
- Não há estilos inline arbitrários; tudo segue Tailwind do PRD.

## Handoff esperado
Lista das rotas/telas afetadas, variáveis de template esperadas e qualquer comportamento interativo que o QA deve exercer (ex.: estados de formulário, tooltips).
