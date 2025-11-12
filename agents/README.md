# Agentes de IA do JL CRM

Este diretório descreve os agentes especializados que auxiliam o time nas entregas do JL CRM, sempre alinhados ao `PRD.md` e aos guias em `docs/`. Cada agente atua apenas dentro do escopo já implementado/planejado; não extrapole funcionalidades não previstas.

## Índice
1. [Agente Backend Django](backend_django.md)
2. [Agente Frontend Templates & Tailwind](frontend_templates.md)
3. [Agente QA/Testes](qa_tester.md)

## Quando acionar cada agente
- **Backend Django**: use quando precisar criar/alterar modelos, signals, views, URLs ou regras de negócio nos apps `users`, `leads`, `accounts`, `contacts`, `tasks` ou `reports`. Este agente deve consultar o MCP `context7` para buscar documentação atualizada de Django (ORM, auth, CBVs) antes de implementar qualquer mudança.
- **Frontend Templates & Tailwind**: escolha este agente para páginas HTML, componentes e estilos dentro do tema escuro descrito no PRD. Ele deve usar o MCP `context7` para referenciar a doc de TailwindCSS e Django Template Language, garantindo aderência ao design system.
- **QA/Testes (Playwright)**: convoque após mudanças funcionais ou visuais para validar fluxos fim a fim e o design. Este agente opera o MCP `playwright` para navegar no sistema, executar cenários e capturar evidências, sinalizando desvios do PRD.

## Uso recomendado
1. **Planeje a tarefa** consultando `docs/overview.md` e `docs/apps.md` para entender o estado atual.
2. **Acione o agente adequado** conforme a natureza da alteração (backend, frontend ou QA).
3. **Garanta o handoff**: cada agente registra insumos/resultados esperados descritos nos arquivos individuais, facilitando a passagem para o próximo estágio do fluxo.
