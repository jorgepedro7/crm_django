# Processo, roadmap e riscos

Consolida o planejamento descrito no `PRD.md` para facilitar o acompanhamento do que já foi entregue e do que permanece aberto.

## Métricas de sucesso
- **Produto**: retenção semanal >70%, tempo médio de sessão >5min, conversão de leads >20%.
- **Usuário**: >30 usuários ativos/mês no MVP, NPS médio >7.
- **Técnicos**: páginas <2s para carregar, consultas <100ms, erros de autenticação <1%.
- **Engajamento**: >10 leads cadastrados e >5 tarefas criadas por usuário/semana.

## Principais riscos e mitigação
| Risco | Mitigação planejada |
| --- | --- |
| Vazamento de dados sensíveis | Usar autenticação Django, hashes padrão e revisão manual de código. |
| Lentidão do SQLite à medida que cresce | Otimizar queries (`select_related`), monitorar com Debug Toolbar e planejar migração para Postgres em versões futuras. |
| Design inconsistente | Template base obrigatório + revisão de PRs focada em UI. |
| Over-engineering que atrasa sprints | Escopo enxuto por sprint e priorização de MVP sem extras. |
| Baixo engajamento inicial | Onboarding guiado, e-mails de boas-vindas e acompanhamento semanal de métricas. |

## Roadmap por sprint
| Sprint | Foco | Status atual |
| --- | --- | --- |
| 1 - Setup & Auth | Criar projeto, apps, ajustar settings, iniciar custom user. | Concluído: projeto configurado, idioma/horário ajustados e autenticação via e-mail em produção. |
| 2 - Perfis & Dashboard | Model `Profile`, dashboard básico com métricas. | Concluído: Profile com signal automático e dashboard protegido online. |
| 3 - Leads (parte 1) | Modelo Lead, admin, CRUD, conversão. | Concluído: pipeline funcional com conversão para contas/contatos. |
| 4 - Contas/Contatos | CRUD completo e listas paginadas. | Concluído: módulos entregues com validações e templates Tailwind. |
| 5 - Pipeline/Integrações | Converter lead em conta/contato, atualizar dashboard. | Concluído junto ao sprint 3, dashboard atualizado com métricas reais. |
| 6 - Tarefas | Modelo Task, filtros por status, exibição no dashboard. | Concluído: CRUD de tarefas e cards no dashboard. |
| 7 - Relatórios & Polimento | View de relatórios, mensagens flash, responsividade. | Concluído nesta entrega. |
| 8 - Documentação & Entrega | README raiz, docs detalhadas, changelog e checklist. | Concluído: documentation pack e screenshots publicados. |
| 9 - Visualizações & Qualidade | Gráfico mensal, exportação CSV e testes de agregações. | Concluído nesta sprint. |
| Final - Docker/Testes | Dockerfile, docker-compose, cobertura de testes >70%. | Planejado, sem entregas. |

## Checklist imediato
- [ ] Preparar ambiente Docker + docker-compose.
- [ ] Estruturar suíte abrangente de testes (unitários + integração) visando cobertura >70%.
- [ ] Automatizar pipeline de CI (lint, tests) para os próximos releases.

## Pendências registradas para as sprints finais
- Dockerização do stack (Dockerfile + docker-compose com volume do SQLite).
- Testes unitários e de integração cobrindo autenticação, CRUDs e relatórios.
- Automatização de builds (CI) para validar Docker + testes antes do deploy.
