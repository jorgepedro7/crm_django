# Guidelines de código e UX

As regras abaixo consolidam o que já está descrito no `PRD.md`. Atualize apenas quando novas decisões forem oficialmente adotadas no projeto.

## Código e arquitetura
- Código em **inglês**, interface e mensagens em **português brasileiro**.
- Seguir PEP 8, usar `snake_case` para funções/variáveis e `PascalCase` para classes.
- Preferir **Class-Based Views** com `LoginRequiredMixin` para rotas autenticadas.
- Utilizar **aspas simples** em Python e ordenar imports (stdlib, terceiros, locais).
- Separar responsabilidades por app: modelos, forms, urls, views e `signals.py` próprios.
- Reaproveitar templates via `base.html`; manter componentes como cards, tabelas e formulários em includes reutilizáveis.
- Para queries complexas, priorizar `select_related`/`prefetch_related` e funções de agregação do ORM.

## Modelos e validações
- Campos obrigatórios em formulários devem ter validação no model e no form.
- E-mails precisam ser únicos para `User` e `Lead`.
- `Lead.status` segue os choices `novo`, `qualificado`, `convertido`, `perdido`.
- `Task.status` usa os estados `pendente`, `concluida`, `cancelada`.
- Registre sinais para:
  - Criar `Profile` automaticamente após salvar `User`.
  - Converter Lead em Account+Contact alterando o status para `convertido`.

## Frontend e experiência
- TailwindCSS via CDN em todos os templates, mantendo tema escuro (`bg-slate-800/700`, textos claros, destaques azul/indigo).
- Carregar o script do Tailwind CDN no `<head>` sem `defer` para que o runtime JIT injete os estilos antes do primeiro paint (evita páginas exibidas em HTML puro).
- Navbar superior, sidebar fixa e conteúdo central responsivo (mobile-first).
- Tipografia padrão: `font-sans`, tamanhos `text-3xl` para títulos principais e `text-base` para corpo.
- Botões com gradiente azul/indigo e estados `hover` evidentes; inputs com `focus:ring`.
- Formularios em PT-BR, com mensagens de erro claras e layout em até 3 cliques para ações críticas (meta definida no PRD).
- Gráfico mensal do dashboard usa `<svg>` com `polyline`; normalize os valores para 0-100, mantenha a quantidade de meses definida em `DashboardView.month_span` e compare conversões com `monthly_goal`.
- As barras do pipeline e colunas de conversão devem utilizar percentuais reais via `style="width: {{ step.percent }}%"` ou `style="height: calc({{ step.percent }}% + 1rem)"`, evitando dados mockados.
- A view `/reports/` precisa preservar o botão “Exportar CSV” que envia os filtros atuais (`data_inicio`, `data_fim`) na query string.

## Segurança e performance
- Autenticação nativa do Django com CSRF habilitado em todos os formulários.
- Nunca expor dados sensíveis no template; emails e senhas trafegam via HTTPS em produção.
- Consultas devem manter tempo <100ms e páginas devem carregar em <2s (objetivos do PRD).
- Utilize `messages` do Django para feedback de CRUD e valide permissões antes de acessar objetos.

## Qualidade e colaboração
- Só documente e registre funcionalidades que já existem no código-base.
- Atualize migrações junto com alterações em modelos.
- Reapresente este arquivo em PRs que façam mudanças de padrão para manter o time alinhado.
