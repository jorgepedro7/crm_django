# Repository Guidelines

## Project Structure & Module Organization
- `core/` guarda configurações Django (settings, URLs, WSGI/ASGI).
- Apps funcionais ficam em `accounts/`, `contacts/`, `leads/`, `tasks/`, `users/`, `reports/`; cada um deve conter models, views, urls e signals próprios.
- `docs/` reúne contexto (overview, setup, guidelines, apps, process) e deve ser atualizado junto de qualquer entrega.
- `agents/` descreve agentes de IA para backend, frontend (templates + Tailwind) e QA/Playwright; consulte antes de acionar automações.
- `db.sqlite3` é o banco local padrão; evite comitar dumps ou dados sensíveis.

## Build, Test, and Development Commands
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
python -Wall manage.py test  # habilitar assim que testes estiverem presentes
```
Use `python manage.py createsuperuser` para gerar credenciais administrativas. Tailwind é carregado via CDN, portanto nenhum build front-end adicional é necessário.

## Coding Style & Naming Conventions
- Código em inglês; interface (templates, mensagens, labels) em português brasileiro.
- Siga PEP 8 com indentação de 4 espaços, `snake_case` para funções/variáveis e `PascalCase` para classes.
- Use aspas simples em Python e ordene imports por blocos (stdlib, terceiros, locais).
- Prefira Class-Based Views com `LoginRequiredMixin`; reutilize `base.html` e componentes Tailwind padronizados (`bg-slate-800`, gradientes azul/indigo).
- Registre signals em arquivos dedicados e mantenha validações nos models/forms para campos obrigatórios e e-mails únicos.

## Testing Guidelines
- Planejado usar `django.test.TestCase`/`pytest-django`; mantenha nomes `test_<feature>` em cada app.
- Almeje cobertura ≥70% conforme sprint final do PRD e execute `python -Wall manage.py test` antes de abrir PRs.
- Para validações end-to-end e UI, acione o agente QA que utiliza o MCP `playwright` seguindo `agents/qa_tester.md`.

## Commit & Pull Request Guidelines
- Mensagens em inglês no formato `area: breve descrição` (ex.: `leads: add status choices validation`).
- Cada PR deve incluir: resumo do problema/solução, referência a tarefas/issue, checklist de migrações e comandos executados, além de screenshots quando alterarem UI.
- Confirme que documentação (`docs/` e `agents/`) reflete qualquer mudança estrutural antes do merge e solicite validação do agente QA para features visuais ou fluxos críticos.
