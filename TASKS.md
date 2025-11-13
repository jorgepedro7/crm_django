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

### Sprint 7: Relatórios e Polimento (Semana 8) [X]
- [X] Relatórios View
  - [X] Em core/views.py, TemplateView com filtros GET (data_inicio, data_fim).
  - [X] Query agregada por origem de lead e taxa de conversão usando annotate.
- [X] Template report.html com tabela e gráficos interativos alimentados pelo filtro de período.
- [X] Polir UX
  - [X] Adicionar mensagens flash (Django messages) em PT-BR para ações CRUD.
  - [X] Garantir responsividade em todos templates.
  - [X] Testar fluxos end-to-end manualmente.
- [X] Preparar para Sprints Finais
  - [X] Documentar pendências: Docker, testes unitários, integração dos gráficos.

### Sprint 8: Documentação e Entrega Final (Semana 9) [X]
- [X] **Documentação Técnica**
  - [X] Criar arquivo `README.md` na raiz do projeto contendo:
        - Descrição geral do sistema.
        - Requisitos mínimos (Python, Django, dependências).
        - Instruções para instalação, configuração e execução local.
        - Estrutura de diretórios e explicação de cada app.
        - Contato ou autoria do projeto.
  - [X] Adicionar instruções para migrações (`makemigrations`, `migrate`) e criação de superusuário.
  - [X] Criar seção sobre como contribuir (pull requests, convenções de commit).
  - [X] Gerar diagrama de arquitetura (via Mermaid) no README para ilustrar relação entre apps.
- [X] **Documentação de APIs e Rotas**
  - [X] Criar `docs/routes.md` descrevendo todas as URLs principais:
    - `/login/`, `/signup/`, `/logout/`, `/dashboard/`, `/accounts/`, `/contacts/`, `/leads/`, `/tasks/`, `/reports/`.
    - Métodos suportados (GET/POST/DELETE).
    - Requisitos de autenticação.
  - [X] Incluir exemplos de payloads e respostas JSON quando aplicável.
- [X] **Documentação de Modelos**
  - [X] Criar `docs/models.md` com:
    - Descrição dos modelos (User, Profile, Account, Contact, Lead, Task, Report).
    - Campos e relacionamentos (FKs, tipos, restrições).
    - Notas sobre signals (`post_save` para criação de Profile e conversão de leads).
- [X] **Guia de Estilo de Código**
  - [X] Criar `docs/conventions.md` com:
    - Convenções de nomenclatura (snake_case para variáveis, PascalCase para classes).
    - Uso de aspas simples e importações ordenadas (PEP 8).
    - Preferência por CBVs e uso de `LoginRequiredMixin`.
    - Estrutura modular de apps e uso de `signals.py` separado.
- [X] **Documentação de Interface**
  - [X] Capturar capturas de tela (screenshots) das principais telas: login, dashboard, leads, contas, contatos, tarefas.
  - [X] Criar `docs/ui.md` com:
    - Layout geral (base.html, sidebar, header, footer).
    - Paleta de cores e classes Tailwind mais usadas.
    - Padrões de formulários, botões e responsividade.
- [X] **Histórico de Versões**
  - [X] Criar `CHANGELOG.md` com:
    - Registro das principais alterações por sprint.
    - Data, descrição e autor.
  - [X] Incluir marcações de versão (ex: `v0.1.0` para MVP final).
- [X] **Checklist de Entrega**
  - [X] Verificar que todos os templates estão traduzidos para PT-BR.
  - [X] Garantir que os arquivos estáticos (CSS/JS) estão corretamente servidos.
  - [X] Confirmar que não há dados sensíveis hardcoded.
  - [X] Revisar consistência visual e tipográfica.
  - [X] Testar execução completa em ambiente limpo (sem dependências prévias).


### Sprint 9: Visualizações Avançadas e Qualidade [X]
- [X] Evoluir dashboards com gráfico de linha mensal (leads x conversões) e comparativo com metas.
- [X] Disponibilizar exportação de relatórios filtrados em CSV diretamente pela página de relatórios.
- [X] Cobrir agregações de relatórios e dashboards com testes automatizados (unitários e integração) garantindo precisão dos gráficos.
- [X] Documentar no `docs/overview.md` e `docs/guidelines.md` o padrão de uso dos gráficos e futuras extensões.

### Sprint Final: Docker e Testes (Semana 10+) [X]
- [ ] Dockerização
  - [ ] Criar Dockerfile para Django + SQLite.
  - [ ] docker-compose.yml com volumes para db.sqlite.
- [X] Testes Básicos
  - [X] Em tests.py de cada app, tests para models e views (pytest ou Django TestCase).
  - [X] Cobertura >70% para autenticação e CRUD.


# **Sprint 10 – Implementação Completa do Kanban**

### **Objetivo Geral da Sprint**

Implementar no JL CRM um **Kanban completo**, funcional, responsivo e integrado ao design system dark + TailwindCSS. O Kanban deve permitir visualizar leads por status, arrastar e soltar cartões entre colunas, atualizar status e ordem automaticamente via AJAX e oferecer uma experiência moderna e fluida.

---

# **Sprint 10 — Backlog Completo (com caixas)**

- [X] Atualizar os modelos do módulo de leads, adicionando no modelo `LeadStatus` o campo `order` para definir a ordem das colunas.
- [X] Atualizar o modelo `Lead` adicionando o campo `position` para controlar a ordenação interna dos cards dentro de cada coluna.
- [X] Criar migrações correspondentes e aplicá-las no banco de dados SQLite.
- [X] Desenvolver a view principal `KanbanView` utilizando Class-Based Views, carregando todos os statuses ordenados e agrupando os leads por status.
- [X] Enviar os dados necessários ao template do Kanban através do contexto da view.
- [X] Criar a view `UpdateLeadPositionView` para receber payloads AJAX e processar atualizações de status e posição dos leads.
- [X] Implementar lógica para reordenar automaticamente os leads dentro de uma coluna ao mover um card.
- [X] Garantir que apenas usuários autenticados possam acessar o Kanban, utilizando `LoginRequiredMixin`.
- [X] Criar rota GET `/kanban/` para exibir o board visual.
- [X] Criar rota POST `/kanban/update/` para atualizar movimentações via AJAX.
- [X] Criar o template principal `kanban.html`, estruturado com TailwindCSS, contendo layout horizontal com scroll e colunas representando os statuses.
- [X] Exibir título do status e contador de leads em cada coluna.
- [X] Criar o componente de card de lead `partials/kanban_lead_card.html`, exibindo nome, contato e detalhes relevantes do lead.
- [X] Aplicar design escuro, gradientes e classes do design system nos cards e colunas.
- [X] Integrar a biblioteca SortableJS ao template por CDN.
- [X] Configurar instâncias de SortableJS para cada coluna do Kanban com animações, drag-and-drop e callback `onEnd`.
- [X] Implementar script JavaScript para capturar o ID do lead movido, novo status e posição após o arraste.
- [X] Enviar esses dados ao backend via `fetch()` com método POST e token CSRF incluído no header.
- [X] Implementar tratamento de respostas no frontend, exibindo feedback visual de sucesso ou falha.
- [X] Garantir responsividade completa do Kanban, com colunas de largura mínima e scroll horizontal suave no mobile.
- [X] Implementar feedback visual durante o arraste, como destaque do card selecionado e efeitos de hover.
- [X] Ajustar tipografia, cores, bordas e sombras conforme o design system definido.
- [X] Realizar testes manuais para arrastar cards entre colunas e dentro da mesma coluna.
- [X] Validar que a persistência de posição e status funciona corretamente após recarregar a página.
- [X] Testar comportamento do Kanban quando colunas estiverem vazias.
- [X] Verificar se usuários não autenticados são redirecionados corretamente ao tentar acessar `/kanban/`.
- [X] Testar o arraste em diferentes tamanhos de tela (desktop, tablet e mobile).
- [X] Validar funcionamento de múltiplos leads em colunas longas.
- [X] Revisar código conforme PEP8, uso consistente de aspas simples e boas práticas de organização.

---

# **Resultado Esperado da Sprint 10**

Ao final da Sprint 10, o JL CRM terá um **Kanban moderno, funcional e totalmente integrado**, possibilitando controle visual do pipeline de leads com drag-and-drop, atualização instantânea e experiência consistente com o design system escuro do projeto.

Essa funcionalidade ficará pronta para uso interno e preparada para expansões futuras, como Kanban de tarefas, oportunidades e workflows.

> Notas: Quando metas personalizadas de conversão forem introduzidas, este cálculo deverá ser ajustado mantendo compatibilidade com os gráficos existentes.
