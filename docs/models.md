# Modelos do JL CRM

## User (`users.models.User`)
- Baseado em `AbstractUser`.
- Remove `username`, usa `email` como `USERNAME_FIELD`.
- Campos principais: `email`, `first_name`, `last_name`, `is_staff`, `is_active`.

## Profile (`profiles.models.Profile`)
- `user`: `OneToOneField` para `User`.
- `full_name`: `CharField`.
- `photo`: `ImageField` opcional.
- `created_at`, `updated_at`: timestamps automáticos.
- Criado automaticamente via signal `post_save`.

## Account (`accounts.models.Account`)
- `owner`: `ForeignKey` para `User`.
- `name`, `industry`, `city`, `website`.
- `created_at`, `updated_at`.
- `unique_together = (owner, name)` garante nome único por usuário.

## Contact (`contacts.models.Contact`)
- `owner`: `ForeignKey` para `User`.
- `account`: `ForeignKey` para `Account`.
- `name`, `email`, `phone`, `position`.
- `created_at`, `updated_at`.
- `unique_together = (owner, email)` evita e-mails repetidos na mesma carteira.

## Lead (`leads.models.Lead`)
- `owner`: `ForeignKey` para `User`.
- `account`: `ForeignKey` opcional para `Account`.
- `contact`: `ForeignKey` opcional para `Contact`.
- `name`, `email`, `phone`.
- `source`: choices (`inbound`, `outbound`, `indicacao`, `evento`, `outro`).
- `status`: choices (`novo`, `qualificado`, `convertido`, `perdido`).
- `notes`: texto opcional.
- `created_at`, `updated_at`.
- `unique_together = (owner, email)` para deduplicar leads.
- Signal `lead_converted` força o status `convertido`.

## Task (`tasks.models.Task`)
- `owner`: `ForeignKey` para `User`.
- `lead`: `ForeignKey` opcional para `Lead`.
- `contact`: `ForeignKey` opcional para `Contact`.
- `title`, `description`, `due_date`.
- `status`: choices (`pendente`, `concluida`, `cancelada`).
- `created_at`, `updated_at`.
- Propriedade `is_overdue` identifica pendências vencidas.

## Relatórios
- Não há modelo dedicado. A view em `core.views.ReportsView` utiliza agregações (`annotate`, `Count`) sobre `Lead` com filtros por data.
