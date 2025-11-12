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
| 1 - Setup & Auth | Criar projeto, apps, ajustar settings, iniciar custom user. | Parcialmente concluído: projeto base criado; ajustes de idioma/user pendentes. |
| 2 - Perfis & Dashboard | Model `Profile`, dashboard básico com métricas. | Não iniciado. |
| 3 - Leads (parte 1) | Modelo Lead, admin, CRUD, conversão. | Não iniciado. |
| 4 - Contas/Contatos | CRUD completo e listas paginadas. | Não iniciado. |
| 5 - Pipeline/Integrações | Converter lead em conta/contato, atualizar dashboard. | Não iniciado. |
| 6 - Tarefas | Modelo Task, filtros por status, exibição no dashboard. | Não iniciado. |
| 7 - Relatórios & Polimento | View de relatórios, mensagens flash, responsividade. | Não iniciado. |
| 8 - Documentação & Entrega | README raiz, docs detalhadas, changelog e checklist. | Em progresso (esta pasta inicia a documentação). |
| Final - Docker/Testes | Dockerfile, docker-compose, cobertura de testes >70%. | Planejado, sem entregas. |

## Checklist imediato
- [ ] Ajustar `LANGUAGE_CODE='pt-br'` e `TIME_ZONE='America/Sao_Paulo'` em `core/settings.py`.
- [ ] Implementar `users/models.py` com `AbstractUser` baseado em e-mail e registrar no admin.
- [ ] Criar views/templates de login, signup e home pública com Tailwind conforme PRD.
- [ ] Criar modelos para leads, accounts, contacts, tasks e seus CRUDs iniciais.
- [ ] Configurar URLs dos apps no `core/urls.py` e proteger com autenticação.

Atualize esta lista sempre que concluir um item para manter o alinhamento entre o código e o plano oficial.
