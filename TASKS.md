## Lista de tarefas

### Sprint 1: Setup Inicial e Autenticação (Semana 1-2) [X]
- [X] Configurar projeto Django base
  - [X] Criar virtualenv e instalar Django 5.x via pip.
  - [X] Executar `django-admin startproject core .` e ajustar settings.py para apps (accounts, contacts, core, leads, profiles, tasks, users, reports).
  - [X] Configurar LANGUAGE_CODE='pt-br' e TIME_ZONE='America/Sao_Paulo' em settings.py.
  - [X] Adicionar apps instalados em INSTALLED_APPS.
- [X] Customizar modelo User para e-mail
  - [X] Em users/models.py, subclass AbstractUser com USERNAME_FIELD='email' e REQUIRED_FIELDS=[].
  - [X] Em users/admin.py, registrar User customizado.
  - [X] Criar migração inicial com `python manage.py makemigrations users` e `migrate`.
- [X] Implementar views e templates de autenticação
  - [X] Em users/views.py, criar CBV LoginView e SignupView usando CreateView para User.
  - [X] Configurar urls.py em core e users para /login/, /signup/, /logout/.
  - [X] Criar templates base.html com Tailwind CDN, header e footer escuros.
  - [X] Criar login.html e signup.html com forms em PT-BR, inputs Tailwind e botão gradiente.
- [X] Site público
  - [X] Em core/views.py, criar TemplateView para home pública com links para login/signup.
  - [X] Template home.html com hero gradiente e chamadas para ação.

### Sprint 2: Perfis e Dashboard Básico (Semana 3) [X]
- [X] Modelo Profile
  - [X] Em profiles/models.py, criar Profile com OneToOneField para User, full_name, photo.
  - [X] Adicionar created_at/updated_at via mixin ou auto_now.
  - [X] Makemigrations e migrate para profiles.
- [X] Signal para criar Profile automático
  - [X] Em profiles/signals.py, post_save para User criando Profile.
  - [X] Em profiles/apps.py, importar signals em ready().
- [X] Dashboard View
  - [X] Em core/views.py, LoginRequiredMixin + TemplateView para /dashboard/.
  - [X] Template dashboard.html com grid Tailwind, seções para leads, conversões e gráficos interativos.
  - [X] Adicionar menu sidebar com links para seções futuras.

### Sprint 3: Contas (Semana 4) [X]
- [X] Modelo Account
  - [X] Em accounts/models.py, Account com ForeignKey User, name, industry, city, website.
  - [X] Adicionar created_at/updated_at.
  - [X] Makemigrations e migrate.
- [X] Admin para Account
  - [X] Em accounts/admin.py, registrar Account com list_display e filters.
- [X] CRUD Views para Accounts
  - [X] Em accounts/views.py, ListView, CreateView, UpdateView, DeleteView com LoginRequiredMixin.
  - [X] Forms em forms.py com ModelForm, validações.
  - [X] Urls em accounts/urls.py.
  - [X] Templates: account_list.html (tabela Tailwind), form.html genérico com inputs.
- [X] Integrar no Dashboard
  - [X] Query para total de contas em dashboard view.

### Sprint 4: Contatos (Semana 5) [X]
- [X] Modelo Contact
  - [X] Em contacts/models.py, Contact com FK User e Account, name, email, phone, position.
  - [X] created_at/updated_at.
  - [X] Makemigrations e migrate.
- [X] Admin para Contact
  - [X] Registrar em admin.py com filters por account.
- [X] CRUD Views
  - [X] Similar a Accounts: List/Create/Update/Delete CBVs.
  - [X] Template com vinculação a conta via dropdown.
- [X] Sidebar link para /contacts/.

### Sprint 5: Leads e Pipeline (Semana 6) [X]
- [X] Modelo Lead
  - [X] Em leads/models.py, Lead com FKs para User/Account/Contact (opcionais), name, email, phone, source, status.
  - [X] created_at/updated_at.
  - [X] Makemigrations e migrate.
- [X] Admin para Lead
  - [X] Registrar com inline para Account/Contact.
- [X] CRUD Views
  - [X] ListView com filtro por status e origem; Create/Update/Delete.
  - [X] Form com choices populados para status (novo, qualificado, convertido, perdido).
- [X] Conversão de Lead
  - [X] Botão "Converter" que cria Account e Contact a partir do Lead.
  - [X] Signal para mudar status Lead para "convertido".
- [X] Integrar no Dashboard
  - [X] Query para total de leads e últimas 10 conversões.
  - [X] Gráfico de funil por estágio.

### Sprint 6: Tarefas (Semana 7) [X]
- [X] Modelo Task
  - [X] Em tasks/models.py, Task com FKs para User/Lead/Contact, title, description, due_date, status.
  - [X] created_at/updated_at.
  - [X] Makemigrations e migrate.
- [X] Admin para Task
  - [X] Registrar com filters por status e data.
- [X] CRUD Views
  - [X] ListView com filtro por status; Create/Update/Delete.
  - [X] Form com vinculação opcional a lead ou contato.
- [X] Dashboard de Tarefas
  - [X] Exibir tarefas vencidas e pendentes.
  - [X] Link para criar tarefa rápida.

### Sprint 7: Relatórios e Polimento (Semana 8)
- [ ] Relatórios View
  - [ ] Em core/views.py, TemplateView com filtros GET (data_inicio, data_fim).
  - [ ] Query agregada por origem de lead e taxa de conversão usando annotate.
- [ ] Template report.html com tabela e gráficos interativos alimentados pelo filtro de período.
- [ ] Polir UX
  - [ ] Adicionar mensagens flash (Django messages) em PT-BR para ações CRUD.
  - [ ] Garantir responsividade em todos templates.
  - [ ] Testar fluxos end-to-end manualmente.
- [ ] Preparar para Sprints Finais
  - [ ] Documentar pendências: Docker, testes unitários, integração dos gráficos.

### Sprint 8: Documentação e Entrega Final (Semana 9)
- [ ] **Documentação Técnica**
  - [ ] Criar arquivo `README.md` na raiz do projeto contendo:
        - Descrição geral do sistema.
        - Requisitos mínimos (Python, Django, dependências).
        - Instruções para instalação, configuração e execução local.
        - Estrutura de diretórios e explicação de cada app.
        - Contato ou autoria do projeto.
  - [ ] Adicionar instruções para migrações (`makemigrations`, `migrate`) e criação de superusuário.
  - [ ] Criar seção sobre como contribuir (pull requests, convenções de commit).
  - [ ] Gerar diagrama de arquitetura (via Mermaid) no README para ilustrar relação entre apps.
- [ ] **Documentação de APIs e Rotas**
  - [ ] Criar `docs/routes.md` descrevendo todas as URLs principais:
    - `/login/`, `/signup/`, `/logout/`, `/dashboard/`, `/accounts/`, `/contacts/`, `/leads/`, `/tasks/`, `/reports/`.
    - Métodos suportados (GET/POST/DELETE).
    - Requisitos de autenticação.
  - [ ] Incluir exemplos de payloads e respostas JSON quando aplicável.
- [ ] **Documentação de Modelos**
  - [ ] Criar `docs/models.md` com:
    - Descrição dos modelos (User, Profile, Account, Contact, Lead, Task, Report).
    - Campos e relacionamentos (FKs, tipos, restrições).
    - Notas sobre signals (`post_save` para criação de Profile e conversão de leads).
- [ ] **Guia de Estilo de Código**
  - [ ] Criar `docs/conventions.md` com:
    - Convenções de nomenclatura (snake_case para variáveis, PascalCase para classes).
    - Uso de aspas simples e importações ordenadas (PEP 8).
    - Preferência por CBVs e uso de `LoginRequiredMixin`.
    - Estrutura modular de apps e uso de `signals.py` separado.
- [ ] **Documentação de Interface**
  - [ ] Capturar capturas de tela (screenshots) das principais telas: login, dashboard, leads, contas, contatos, tarefas.
  - [ ] Criar `docs/ui.md` com:
    - Layout geral (base.html, sidebar, header, footer).
    - Paleta de cores e classes Tailwind mais usadas.
    - Padrões de formulários, botões e responsividade.
- [ ] **Histórico de Versões**
  - [ ] Criar `CHANGELOG.md` com:
    - Registro das principais alterações por sprint.
    - Data, descrição e autor.
  - [ ] Incluir marcações de versão (ex: `v0.1.0` para MVP final).
- [ ] **Checklist de Entrega**
  - [ ] Verificar que todos os templates estão traduzidos para PT-BR.
  - [ ] Garantir que os arquivos estáticos (CSS/JS) estão corretamente servidos.
  - [ ] Confirmar que não há dados sensíveis hardcoded.
  - [ ] Revisar consistência visual e tipográfica.
  - [ ] Testar execução completa em ambiente limpo (sem dependências prévias).


### Sprint 9: Visualizações Avançadas e Qualidade (Planejado)
- [ ] Evoluir dashboards com gráfico de linha mensal (leads x conversões) e comparativo com metas.
- [ ] Disponibilizar exportação de relatórios filtrados em CSV diretamente pela página de relatórios.
- [ ] Cobrir agregações de relatórios e dashboards com testes automatizados (unitários e integração) garantindo precisão dos gráficos.
- [ ] Documentar no `docs/overview.md` e `docs/guidelines.md` o padrão de uso dos gráficos e futuras extensões.


### Sprint Final: Docker e Testes (Semana 10+)
- [ ] Dockerização
  - [ ] Criar Dockerfile para Django + SQLite.
  - [ ] docker-compose.yml com volumes para db.sqlite.
- [ ] Testes Básicos
  - [ ] Em tests.py de cada app, tests para models e views (pytest ou Django TestCase).
  - [ ] Cobertura >70% para autenticação e CRUD.
> Notas: Quando metas personalizadas de conversão forem introduzidas, este cálculo deverá ser ajustado mantendo compatibilidade com os gráficos existentes.
