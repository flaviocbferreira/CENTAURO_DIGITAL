# Resumo geral comentado do projeto Django

Este documento resume a estrutura atual do CENTAURO Digital e explica o fluxo principal do Django neste projeto.

## 1. Estrutura do projeto

```text
apps/
  accounts/      Login, logout e permissoes gerais do sistema.
  auditoria/     Registro de eventos importantes, como criacao, edicao e exclusao.
  separacao/     CRUD, filtros, datatable e endpoints JSON do modulo de separacao.
config/
  settings/      Configuracoes separadas por ambiente: base, dev e prod.
  urls.py        Arquivo de rotas principal do projeto.
  views.py       Dashboard e placeholders globais.
docs/            Documentacao de apoio.
media/           Arquivos enviados por usuarios em ambiente local.
static/          CSS e JavaScript globais.
templates/       Templates HTML globais e por modulo.
manage.py        Entrada para comandos como runserver, migrate e createsuperuser.
```

## 2. Funcao das pastas

`apps/` guarda os apps internos. Cada app concentra uma parte do sistema: models, views, urls, admin, tests e services.

`config/` representa o projeto Django principal. Ele junta settings, urls globais e pontos de entrada ASGI/WSGI.

`templates/` contem HTML reutilizavel. `base.html` define a estrutura geral, `partials/` guarda pedacos reaproveitados, e pastas como `separacao/` e `accounts/` guardam telas especificas.

`static/` contem arquivos enviados diretamente ao navegador, como `static/css/theme.css`, `static/js/separacao.js` e `static/js/dashboard.js`.

`media/` e reservado para uploads locais. Em desenvolvimento, `config/urls.py` serve essa pasta quando `DEBUG=True`.

## 3. Arquivos principais

`config/settings/base.py` contem configuracoes comuns: apps instalados, middlewares, templates, static/media, timezone e rotas de login/logout.

`config/settings/dev.py` ativa `DEBUG=True` e usa SQLite em `db.sqlite3`.

`config/settings/prod.py` desativa debug e liga configuracoes de seguranca como cookies seguros, HTTPS e HSTS.

`config/urls.py` e a primeira tabela de rotas. Ele envia `/accounts/` para o app accounts, `/separacao/` para o app separacao, `/admin/` para o admin e `/` para o dashboard.

`apps/separacao/models.py` define a tabela `Separacao`, seus campos, choices, permissoes customizadas e metodos auxiliares.

`apps/separacao/views.py` recebe requests, aplica permissoes, chama services, renderiza templates e devolve JSON para AJAX.

`apps/separacao/services.py` concentra filtros, indicadores, serializacao da datatable, atualizacao de status e dados de auditoria.

`apps/separacao/forms.py` define quais campos aparecem no formulario de criacao/edicao e valida a regra de quantidade pendente.

`apps/auditoria/models.py` define `EventoAuditoria`, tabela que guarda quem fez uma acao, em qual objeto, quando e com quais dados resumidos.

`apps/accounts/views.py` usa as views nativas do Django para login/logout.

## 4. Fluxo URL -> pagina

1. O usuario acessa uma URL, por exemplo `/separacao/`.
2. O Django procura a rota em `config/urls.py`.
3. Como a URL comeca com `separacao/`, ele inclui `apps/separacao/urls.py`.
4. A rota vazia do app chama `SeparacaoListView.as_view()`.
5. A view verifica login e permissao com `LoginRequiredMixin` e `PermissionRequiredMixin`.
6. `get_queryset()` chama `filtrar_separacoes(request.GET)`.
7. `get_context_data()` adiciona opcoes de filtros, badges, usuarios e querystring de paginacao.
8. O Django renderiza `templates/separacao/separacao_list.html`.
9. O navegador carrega o HTML, CSS e `static/js/separacao.js`.

## 5. Fluxo banco -> view -> template

O banco guarda registros no model `Separacao`. A view nao consulta tudo manualmente; ela delega para `services.py`.

`filtrar_separacoes()` devolve um QuerySet com filtros aplicados. A ListView coloca esse QuerySet paginado no contexto com o nome `separacoes`.

No template, o loop `{% for separacao in separacoes %}` cria uma linha da tabela para cada registro. Variaveis como `{{ separacao.documento }}` exibem campos do model. Metodos como `{{ separacao.get_tipo_display }}` mostram o texto amigavel das choices.

## 6. Visual com Tailwind CSS

O projeto usa Tailwind via CDN em `templates/base.html`. As classes ficam diretamente no HTML, por exemplo:

```text
rounded        bordas arredondadas
border         borda
bg-white       fundo branco
text-slate-700 cor do texto
grid/flex      organizacao do layout
hover:*        estilo ao passar o mouse
```

`static/css/theme.css` complementa o Tailwind com ajustes globais: rolagem suave, fundo da aplicacao e limite de altura da tabela.

## 7. Tabela e datatable

A tabela de separacao e renderizada primeiro pelo Django, usando registros paginados. Depois o JavaScript melhora a interacao:

`data-datatable-row` identifica cada linha pesquisavel.

`data-search` guarda texto consolidado para pesquisa local.

`data-datatable-search` identifica o input de busca.

`data-visible-rows` atualiza o contador de linhas visiveis.

O endpoint `/separacao/api/busca/` ja existe para evoluir a busca via AJAX com resultados vindos do servidor.

## 8. Filtros e pesquisa dinamica

Os filtros principais usam `method="get"`, entao ficam na URL. Isso permite paginar mantendo filtros.

`services.py` aplica filtros por data, intervalo de datas, grupo, status operacional, usuario atribuido e situacao de vencimento.

A pesquisa dinamica atual roda no navegador sobre as linhas da pagina carregada. Ela normaliza texto para minusculo e remove acentos, tornando a busca mais tolerante.

## 9. Login, permissoes e seguranca

O login usa `LoginView` do Django em `/accounts/login/`.

Logout usa POST em `/accounts/logout/confirm/`, evitando encerrar sessao apenas por clique GET.

Views internas usam `LoginRequiredMixin`, `PermissionRequiredMixin`, `login_required` e `permission_required`.

Permissoes customizadas ficam em `apps/accounts/models.py` e `apps/separacao/models.py`.

O comando `python manage.py criar_permissoes_iniciais` cria grupos como Administrador, Supervisor, Operador e Auditor.

POSTs de formulario usam `{% csrf_token %}`. O AJAX de status envia o header `X-CSRFToken`.

Em producao, `config/settings/prod.py` configura cookies seguros, HTTPS, HSTS, bloqueio de iframe e protecao contra content sniffing.

## 10. Melhorias futuras

Resolver os marcadores de conflito do `README.md` antes de versionar novas alteracoes.

Evoluir a pesquisa da datatable para usar de fato o endpoint AJAX `/separacao/api/busca/`.

Criar testes para filtros, permissoes, atualizacao de status e auditoria.

Separar Tailwind CDN para build local quando o layout estabilizar.

Adicionar paginas reais de auditoria em vez do placeholder.

Avaliar PostgreSQL ou MySQL quando o volume de dados crescer.
