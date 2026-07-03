# path cria cada rota deste app.
from django.urls import path

# Importamos as views que serao chamadas pelas URLs abaixo.
from .views import (
    SeparacaoCreateView,
    SeparacaoDeleteView,
    SeparacaoDetailView,
    SeparacaoListView,
    SeparacaoUpdateView,
    atualizar_status_json,
    busca_datatable_json,
    indicadores_json,
)

# app_name cria o namespace "separacao".
# Assim, no template usamos {% url 'separacao:list' %} sem conflito com outros apps.
app_name = "separacao"

urlpatterns = [
    # /separacao/ lista registros, filtros, indicadores e tabela.
    path("", SeparacaoListView.as_view(), name="list"),
    # /separacao/api/busca/ retorna resultados JSON para busca/datatable.
    path("api/busca/", busca_datatable_json, name="busca_datatable_json"),
    # /separacao/api/indicadores/ retorna contadores JSON dos cards.
    path("api/indicadores/", indicadores_json, name="indicadores_json"),
    # /separacao/api/<id>/status/ recebe POST AJAX para atualizar status do registro.
    path("api/<int:pk>/status/", atualizar_status_json, name="atualizar_status_json"),
    # /separacao/novo/ abre formulario de cadastro.
    path("novo/", SeparacaoCreateView.as_view(), name="create"),
    # /separacao/<id>/ abre detalhes do registro indicado pelo pk.
    path("<int:pk>/", SeparacaoDetailView.as_view(), name="detail"),
    # /separacao/<id>/editar/ abre formulario preenchido para edicao.
    path("<int:pk>/editar/", SeparacaoUpdateView.as_view(), name="update"),
    # /separacao/<id>/excluir/ abre confirmacao e processa exclusao.
    path("<int:pk>/excluir/", SeparacaoDeleteView.as_view(), name="delete"),
]
