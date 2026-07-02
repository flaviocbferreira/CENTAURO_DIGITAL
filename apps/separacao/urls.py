from django.urls import path

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

app_name = "separacao"

urlpatterns = [
    path("", SeparacaoListView.as_view(), name="list"),
    path("api/busca/", busca_datatable_json, name="busca_datatable_json"),
    path("api/indicadores/", indicadores_json, name="indicadores_json"),
    path("api/<int:pk>/status/", atualizar_status_json, name="atualizar_status_json"),
    path("novo/", SeparacaoCreateView.as_view(), name="create"),
    path("<int:pk>/", SeparacaoDetailView.as_view(), name="detail"),
    path("<int:pk>/editar/", SeparacaoUpdateView.as_view(), name="update"),
    path("<int:pk>/excluir/", SeparacaoDeleteView.as_view(), name="delete"),
]
