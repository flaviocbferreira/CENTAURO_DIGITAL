<<<<<<< HEAD
# CENTAURO_DIGITAL
=======
# CENTAURO - DIGITAL PAINEL GERAL

Base inicial do projeto Django para o painel geral do CENTAURO Digital.

## Ambiente local no Windows

Crie a virtualenv:

```powershell
py -m venv .venv
```

Ative a virtualenv:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependencias:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Para instalar tambem as dependencias de desenvolvimento:

```powershell
python -m pip install -r requirements-dev.txt
```

## Configuracoes

Crie o arquivo `.env` a partir do exemplo:

```powershell
Copy-Item .env.example .env
```

Nunca versionar o arquivo `.env`, pois ele deve guardar configuracoes sensiveis do ambiente.

Configuracoes essenciais lidas do `.env`:

```text
SECRET_KEY
ALLOWED_HOSTS
```

A checklist de seguranca inicial esta em `docs/seguranca_base.md`.

## Banco de dados

O banco inicial do projeto e SQLite, configurado em `config/settings/dev.py` com:

```text
BASE_DIR / "db.sqlite3"
```

Essa escolha reduz a complexidade no inicio e acelera a validacao das telas, regras e modulos. A estrutura de settings foi organizada como pacote (`config/settings/`) para permitir uma migracao futura para MySQL ou PostgreSQL criando configuracoes especificas de ambiente, sem alterar as regras de negocio.

## Settings por ambiente

Por padrao, `manage.py`, `config/asgi.py` e `config/wsgi.py` usam o ambiente local:

```text
config.settings.dev
```

Arquivos disponiveis:

```text
config/settings/base.py   Configuracoes comuns
config/settings/dev.py    Desenvolvimento local com DEBUG=True e SQLite
config/settings/prod.py   Producao com DEBUG=False e seguranca reforcada
```

Para alterar o ambiente no PowerShell:

```powershell
$env:DJANGO_SETTINGS_MODULE = "config.settings.prod"
python manage.py check
```

Para voltar ao ambiente local:

```powershell
$env:DJANGO_SETTINGS_MODULE = "config.settings.dev"
```

## Executar o Django

Com a virtualenv ativa, aplique as migracoes iniciais:

```powershell
python manage.py migrate
```

Inicie o servidor local:

```powershell
python manage.py runserver
```

Depois acesse:

```text
http://127.0.0.1:8000/
```

## Estrutura

```text
apps/              Apps internos do sistema
config/            Projeto Django e rotas principais
config/settings/   Configuracoes do Django
docs/              Documentacao do projeto
media/             Uploads locais
static/            Arquivos estaticos globais
templates/         Templates globais reutilizaveis
```

## Layout

O layout base usa Tailwind CSS via CDN para acelerar o desenvolvimento inicial. A estrutura ja separa templates reutilizaveis em `templates/partials/` e estilos auxiliares em `static/css/theme.css`, deixando o projeto preparado para trocar o CDN por um build local do Tailwind no futuro.

Menu principal:

```text
Dashboard | Separacao | Auditoria | Administracao
```

## Static e media

Arquivos estaticos ficam centralizados em:

```text
static/css/      CSS do projeto
static/js/       JavaScript por modulo
static/img/      Imagens estaticas
static/vendor/   Bibliotecas locais futuras
```

Uploads locais ficam em `media/`. Em desenvolvimento, `config/urls.py` serve `MEDIA_URL` usando `MEDIA_ROOT`.

## Autenticacao

O app `accounts` usa a autenticacao nativa do Django.

Rotas principais:

```text
/accounts/login/    Login
/accounts/logout/   Confirmacao de logout
```

As telas internas usam `LoginRequiredMixin`; usuarios sem sessao ativa sao redirecionados para o login.

## Grupos e permissoes

Crie ou atualize os grupos iniciais depois de aplicar as migracoes:

```powershell
python manage.py criar_permissoes_iniciais
```

Grupos criados:

```text
Administrador
Supervisor
Operador
Auditor
```

Permissoes iniciais cobrem acesso ao dashboard, acesso ao modulo de separacao, criar/editar/excluir registros, visualizar auditoria e exportar dados futuramente.

## Modulo separacao

O CRUD de separacao esta disponivel em:

```text
/separacao/              Listagem e filtros
/separacao/novo/         Cadastro
/separacao/<id>/         Detalhe
/separacao/<id>/editar/  Edicao
/separacao/<id>/excluir/ Exclusao
```

Criacoes, edicoes e exclusoes registram eventos no app `auditoria`.

## Proximos passos

As proximas partes devem criar os apps por modulo, mantendo regras de negocio fora das views e usando services, forms e templates reutilizaveis quando necessario.
>>>>>>> 1ac4993 (Digital V.0.1.0)
