# Agente QA/Testes (Playwright)

## Objetivo
Validar fluxos funcionais e consistência visual do JL CRM executando cenários end-to-end com Playwright, além de revisar métricas e requisitos listados no `PRD.md`.

## Escopo
- Garantir que autenticação, CRUDs e dashboards implementados funcionem conforme descrito.
- Checar aderência ao tema escuro, Tailwind e textos PT-BR citados em `docs/guidelines.md`.
- Registrar bugs, regressões ou divergências do PRD antes de releases.

## Ferramentas MCP obrigatórias
- **playwright**: usar as operações do MCP server (navegar, clicar, preencher, esperar respostas) para abrir o sistema local, executar fluxos e capturar evidências.
- Para dúvidas de implementação/UI, pode consultar `context7`, mas foco principal é automação com Playwright.

## Processo sugerido
1. Receber do Agente Backend/Frontend o checklist do que mudou (rotas, modelos, templates).
2. Preparar ambiente local (`python manage.py runserver`) e dados mínimos (ex.: criar superusuário, cadastrar lead).
3. Usar o MCP `playwright` para:
   - Acessar URLs relevantes (`/login/`, `/dashboard/`, CRUDs).
   - Preencher formulários, validar mensagens de erro/sucesso e confirmar redirecionamentos.
   - Capturar screenshots quando houver alterações significativas no layout.
4. Verificar consistência visual (cores, espaçamentos, responsividade básica) contra o guia de Tailwind do PRD.
5. Registrar resultados em issues/relatórios destacando repro steps, ambiente e evidências.
6. Aprovar apenas quando critérios do PRD e metas (tempo <2s, fluxos em 3 cliques) forem atingidos ou documentar riscos.

## Entradas necessárias
- Build/branch disponível e comandos para subir o servidor.
- Instruções de dados de teste (ex.: qual lead verificar, credenciais dummy).
- Expectativas de UX (componentes esperados, mensagens) retiradas do PRD.

## Critérios de pronto
- Todos os cenários impactados foram executados via Playwright MCP.
- Bugs encontrados foram registrados com passos claros e, quando possível, com captura gerada pelo MCP.
- Confirmação explícita de que o design permanece alinhado às diretrizes de tema escuro.

## Handoff esperado
Checklist de testes executados + status (pass/fail) e links para registros de bugs ou evidências.
