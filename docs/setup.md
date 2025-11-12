# Setup e execução local

Estas instruções refletem o que já está disponível no repositório. Ajuste-as somente quando novos componentes forem adicionados.

## Pré-requisitos
- Python compatível com Django 5.2.8 (3.10 ou superior).
- Pip e virtualenv disponíveis na máquina.

## Passo a passo
1. **Criar ambiente virtual (opcional, porém recomendado)**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
   ```
2. **Instalar dependências declaradas em `requirements.txt`**
   ```bash
   pip install -r requirements.txt
   ```
3. **Aplicar migrações do Django**
   ```bash
   python manage.py migrate
   ```
   O projeto usa SQLite (`db.sqlite3`) na raiz; nenhum serviço externo é necessário.
4. **Criar um superusuário para acessar o admin** (quando o fluxo de autenticação estiver implementado)
   ```bash
   python manage.py createsuperuser
   ```
5. **Executar o servidor de desenvolvimento**
   ```bash
   python manage.py runserver
   ```
   O admin já está acessível em `http://localhost:8000/admin/`. As demais rotas serão expostas conforme cada app ganhar URLs próprias.

## Boas práticas durante o setup
- Utilize `python -Wall manage.py test` antes de abrir PRs assim que testes forem adicionados.
- Para resetar o banco em desenvolvimento, apague `db.sqlite3` e reaplique `migrate` (não faça isso em produção).
- Sempre valide que `LANGUAGE_CODE` e `TIME_ZONE` estão coerentes com o que o PRD exige antes de subir mudanças.
