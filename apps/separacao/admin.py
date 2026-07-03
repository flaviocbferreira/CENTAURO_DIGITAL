# admin registra models no painel administrativo do Django.
from django.contrib import admin

from .models import Separacao


@admin.register(Separacao)
class SeparacaoAdmin(admin.ModelAdmin):
    # list_display define as colunas mostradas na listagem do admin.
    list_display = (
        "documento",
        "romaneio",
        "data",
        "grupo",
        "quantidade",
        "status",
        "status_operacional",
        "status_autorizacao",
        "atribuido",
    )
    # list_filter cria filtros laterais por campos de status/tipo.
    list_filter = (
        "status",
        "status_operacional",
        "status_documento",
        "status_autorizacao",
        "tipo",
    )
    # search_fields habilita a caixa de pesquisa do admin nesses campos.
    search_fields = ("documento", "romaneio", "grupo", "atribuido__username")
    # date_hierarchy cria navegacao por data no topo da listagem.
    date_hierarchy = "data"
    # autocomplete_fields troca select grande por campo com busca para usuario atribuido.
    autocomplete_fields = ("atribuido",)
