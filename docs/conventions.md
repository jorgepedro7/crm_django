# Conventions & Contribution Guide

## Estilo de código
- **Linguagem**: código em inglês; interface e mensagens em PT-BR.
- **PEP 8**: indentação 4 espaços, snake_case para funções/variáveis e PascalCase para classes.
- **Aspas simples** para strings em Python.
- **Imports**: stdlib → terceiros → locais, separados por linha em branco.
- **Views**: preferir Class-Based Views com `LoginRequiredMixin` e `SuccessMessageMixin`.
- **Templates**: herdar de `base.html`, usar Tailwind via CDN (`bg-slate-*`, gradientes azul/indigo) e manter formulários acessíveis (`label`, `focus:ring`).

## Organização
- Cada app mantém seus próprios `models`, `forms`, `urls`, `views` e `signals`.
- Signals devem ser registrados em `apps.py` (`ready()`).
- Templates dos apps residem em `templates/<app>/`.
- Documentação relacionada a uma feature deve ser atualizada no mesmo PR (`docs/`).

## Fluxo de trabalho
1. Criar branch a partir de `main`.
2. Implementar feature + testes (quando disponíveis).
3. Rodar `python -Wall manage.py test`.
4. Atualizar docs relevantes (`routes`, `models`, `ui`, `CHANGELOG`).
5. Abrir PR com descrição, comandos executados e screenshots quando houver mudanças visuais.

## Commits & PRs
- Mensagens no formato `area: breve descrição` (ex.: `leads: add status filter`).
- PRs devem referenciar sprint/tarefa, incluir checklist de migrações e resultados de testes.
- Screenshots obrigatórios para alterações de UI (usar agentes QA/Playwright quando possível).
