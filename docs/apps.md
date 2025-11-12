# Apps Django e domínio

A estrutura já contém os apps principais. Use esta referência para saber o papel de cada um e quais modelos/campos o PRD descreve. Não implemente nada fora dessas definições sem atualizar o PRD primeiro.

## Resumo rápido
| App | Responsabilidade | Situação atual |
| --- | --- | --- |
| `core` | Configurações, URLs globais, views utilitárias (home pública, dashboard, relatórios). | Projeto criado; apenas rota do admin configurada até o momento. |
| `users` | Customização do modelo de usuário baseado em e-mail, views de login/signup/logout e perfis. | Modelos ainda não implementados; PRD pede `AbstractUser` com `USERNAME_FIELD='email'`. |
| `accounts` | Cadastros de empresas/organizações e ligação com leads/contatos. | Apenas estrutura vazia; aguardando modelos e CRUD. |
| `contacts` | Pessoas ligadas a contas (nome, email, telefone, cargo). | Modelo, admin e CRUD concluídos. |
| `leads` | Pipeline de leads, etapas e conversão para contas/contatos. | Estrutura vazia; PRD define campos e fluxos abaixo. |
| `tasks` | Atividades vinculadas a leads/contatos, incluindo status e due date. | Estrutura vazia. |
| `reports` | Telas de filtros por período e agregações simples. | Estrutura vazia. |

## Modelos esperados por domínio
Os campos abaixo vêm diretamente do PRD. Marque como concluído conforme cada modelo ganhar código e migrações.

### Users & Profiles
- `User`: herdar de `AbstractUser`, remover username, usar e-mail como credencial única. Campos essenciais: `email`, `first_name`, `last_name`, `is_staff`, `is_active`.
- `Profile`: `OneToOneField` para `User`, `full_name`, `photo` (opcional), `created_at`, `updated_at`. Pode trazer configurações de idioma futuramente.

### Accounts
- Campos: `name`, `industry`, `city`, `website`, `owner` (FK para `User`).
- Relações: `Contact` referencia `Account`; `Lead` pode ser convertido em `Account`.

### Contacts
- Campos: `full_name`, `email`, `phone`, `role`, `account` (FK), `owner` (User opcional).
- Deve aceitar ligação com `Lead` durante conversão.

### Leads
- Campos obrigatórios: `name`, `email`, `phone`, `source`, `status` (choices `novo`, `qualificado`, `convertido`, `perdido`), `owner` (User), `account`/`contact` opcionais para conversão.
- Campos automáticos: `created_at`, `updated_at`.
- Funcionalidades: filtros por status/origem, paginação, ação de conversão (gera account/contact + sinal para atualizar status).

### Tasks
- Campos: `title`, `description`, `due_date`, `status` (`pendente`, `concluida`, `cancelada`), `related_lead`, `related_contact`, `owner`.
- Dashboard deve destacar tarefas vencidas e pendentes.

### Reports
- Sem modelos específicos no PRD; use consultas agregadas via ORM para gerar resumo por período (origem de lead, taxa de conversão) e exportação CSV simples se necessário.

## Integrações previstas entre apps
- `users` ↔ `profiles`: sinal `post_save` para criar perfil automaticamente.
- `leads` ↔ `accounts/contacts`: ação de conversão cria registros e atualiza o lead.
- `tasks` ↔ `leads/contacts`: ForeignKeys opcionais permitem acompanhar follow-ups.
- `reports` ↔ todos os demais: consultas agregadas baseadas nos modelos acima.

> Atenção: até que cada modelo seja criado, mantenha as migrações vazias fora do controle de versão. Assim que implementar, gere as migrações e documente-as aqui.
