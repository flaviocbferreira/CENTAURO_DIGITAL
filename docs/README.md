# Documentacao

Esta pasta reunira decisoes tecnicas, instrucoes operacionais e notas de evolucao do CENTAURO - DIGITAL PAINEL GERAL.

## Estrutura inicial

- `apps/`: apps Django do sistema, separados por responsabilidade.
- `config/`: configuracoes, URLs e pontos de entrada ASGI/WSGI.
- `config/settings/`: pacote de configuracoes do Django.
- `templates/`: templates globais reutilizaveis.
- `static/`: arquivos estaticos globais em desenvolvimento.
- `media/`: arquivos enviados em ambiente local.

## Banco de dados

Nesta fase, o projeto usa SQLite em `BASE_DIR / "db.sqlite3"`.

Quando a aplicacao precisar migrar para MySQL ou PostgreSQL, a troca deve ser feita em arquivos especificos dentro de `config/settings/`, mantendo apps, services, forms e templates independentes do banco escolhido.

## Settings por ambiente

- `config/settings/base.py`: configuracoes compartilhadas.
- `config/settings/dev.py`: ambiente local com `DEBUG=True` e SQLite.
- `config/settings/prod.py`: ambiente de producao com `DEBUG=False`, `ALLOWED_HOSTS` via ambiente e configuracoes de seguranca.

## Seguranca

O checklist inicial de seguranca esta em `docs/seguranca_base.md`.

## Layout

O layout visual inicial usa `templates/base.html` como estrutura principal e partials reutilizaveis em `templates/partials/`.

Componentes iniciais:

- `navbar.html`
- `messages.html`
- `card.html`
- `table.html`

## Static e media

- `static/css/`: CSS centralizado.
- `static/js/`: JavaScript separado por modulo.
- `static/img/`: imagens estaticas.
- `static/vendor/`: bibliotecas locais futuras.
- `media/`: arquivos enviados localmente.

## Autenticacao

O app `apps.accounts` concentra as rotas de login e logout usando as views nativas do Django.

## Separacao

O app `apps.separacao` contem o CRUD do processo operacional de separacao, com forms, views, urls, services e templates separados.

## Auditoria

O app `apps.auditoria` registra eventos importantes gerados pelos modulos do sistema.
