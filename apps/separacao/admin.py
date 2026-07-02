from django.contrib import admin

from .models import Separacao


@admin.register(Separacao)
class SeparacaoAdmin(admin.ModelAdmin):
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
    list_filter = (
        "status",
        "status_operacional",
        "status_documento",
        "status_autorizacao",
        "tipo",
    )
    search_fields = ("documento", "romaneio", "grupo", "atribuido__username")
    date_hierarchy = "data"
    autocomplete_fields = ("atribuido",)
