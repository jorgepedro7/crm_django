# Rotas principais do JL CRM

| Rota | Métodos | Autenticação | Descrição |
| --- | --- | --- | --- |
| `/` | GET | Pública | Landing page com hero e CTAs de login/cadastro. |
| `/login/` | GET/POST | Pública | Formulário de autenticação baseado em e-mail. |
| `/signup/` | GET/POST | Pública | Cadastro de novos usuários. |
| `/logout/` | GET | Autenticado | Finaliza a sessão e redireciona para a landing. |
| `/dashboard/` | GET | Autenticado | Dashboard comercial com cards, pipeline e tarefas. |

## Contas

| Rota | Métodos | Autenticação | Notas |
| --- | --- | --- | --- |
| `/accounts/` | GET | Autenticado | Lista paginada de contas com busca. |
| `/accounts/nova/` | GET/POST | Autenticado | Criação de conta usando `AccountForm`. |
| `/accounts/<id>/editar/` | GET/POST | Autenticado | Atualização de uma conta do usuário. |
| `/accounts/<id>/excluir/` | GET/POST | Autenticado | Confirmação e exclusão com feedback. |

## Contatos

| Rota | Métodos | Autenticação | Notas |
| --- | --- | --- | --- |
| `/contacts/` | GET | Autenticado | Lista com busca por nome/e-mail/conta. |
| `/contacts/novo/` | GET/POST | Autenticado | Criação vinculando a uma conta do usuário. |
| `/contacts/<id>/editar/` | GET/POST | Autenticado | Edição do contato selecionado. |
| `/contacts/<id>/excluir/` | GET/POST | Autenticado | Confirmação e exclusão. |

## Leads

| Rota | Métodos | Autenticação | Notas |
| --- | --- | --- | --- |
| `/leads/` | GET | Autenticado | Lista com filtros por status/origem e busca textual. |
| `/leads/novo/` | GET/POST | Autenticado | Criação de lead com validação de e-mail único. |
| `/leads/<id>/editar/` | GET/POST | Autenticado | Atualização de um lead existente. |
| `/leads/<id>/excluir/` | GET/POST | Autenticado | Confirmação de exclusão. |
| `/leads/<id>/converter/` | POST | Autenticado | Converte o lead em conta/contato, alterando status para `convertido`. |

## Tarefas

| Rota | Métodos | Autenticação | Notas |
| --- | --- | --- | --- |
| `/tasks/` | GET | Autenticado | Lista com filtros por status e cards de vencidas/pendentes. |
| `/tasks/nova/` | GET/POST | Autenticado | Criação de tarefa vinculável a lead/contato. |
| `/tasks/<id>/editar/` | GET/POST | Autenticado | Atualização da tarefa. |
| `/tasks/<id>/excluir/` | GET/POST | Autenticado | Confirmação e exclusão. |

## Relatórios

| Rota | Métodos | Autenticação | Notas |
| --- | --- | --- | --- |
| `/reports/` | GET | Autenticado | View com filtros `data_inicio` e `data_fim`, agregações por origem e estágio. |
| `/reports/?export=csv` | GET | Autenticado | Exporta o relatório filtrado em CSV (colunas: origem, leads, convertidos, taxa). |

> Todas as rotas autenticadas usam `LoginRequiredMixin` e redirecionam para `/login/` caso a sessão expire. CSRF está habilitado por padrão em todos os formulários POST. As rotas são server-rendered (HTML), portanto não há payload JSON padrão além dos dados de formulários submetidos via POST.
