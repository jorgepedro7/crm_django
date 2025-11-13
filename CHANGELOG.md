# Changelog

# Changelog

## [Sprint 10] - 2025-11-13
- Dockerfile e `docker-compose.yml` adicionados para executar o projeto em containers com volume persistindo `db.sqlite3`.
- Suite de testes expandida (accounts, contacts, leads, tasks, users, profiles) garantindo cobertura dos fluxos de autenticação e CRUDs principais.

## [Sprint 9] - 2025-11-13
- Dashboard ganhou gráfico de linha mensal (leads vs. conversões) com comparação contra a meta e tabela detalhada.
- Pipeline utiliza percentuais reais para barras/colunas.
- Relatórios agora exportam CSV e contam com botão dedicado no header.
- Testes automatizados cobrem agregações de relatórios e estatísticas mensais do dashboard.

## [Sprint 8] - 2025-11-13
- Documentação completa: README raiz, rotas, modelos, convenções, UI e checklist.
- Novas capturas de tela das principais telas (login, dashboard, módulos e relatórios).
- `ReportsView` e dashboard atualizados com métricas reais e navegação refinada.

## [Sprint 7] - 2025-11-12
- View de relatórios com filtros por período e agregações por origem/status.
- Template `report.html` com tabelas responsivas e cards de indicadores.
- Mensagens flash para todas as operações CRUD e revisão de responsividade.

## [Sprint 6] - 2025-11-12
- Modelo `Task`, formulários e CRUD completo com filtros por status/busca.
- Cards de tarefas pendentes/vencidas no dashboard e resumo em insights.

## [Sprint 5] - 2025-11-12
- Modelo `Lead`, admin e CRUD com filtros e ação de conversão para conta/contato.
- Dashboard passou a exibir total de leads e últimas conversões.

## [Sprint 4] - 2025-11-12
- CRUD de contatos vinculados a contas, validações de e-mail e templates Tailwind.
- Navbar e dashboard atualizados com links/métricas de contatos.

## [Sprint 3] - 2025-11-12
- Modelo `Account`, admin, formulários e views (List/Create/Update/Delete).
- Integração do total de contas no dashboard.

## [Sprint 2] - 2025-11-11
- Modelo `Profile` com signal automático.
- Dashboard autenticado inicial com cards e sidebar.

## [Sprint 1] - 2025-11-10
- Projeto Django configurado com custom user baseado em e-mail.
- Templates base, login, signup e landing pública com Tailwind.
