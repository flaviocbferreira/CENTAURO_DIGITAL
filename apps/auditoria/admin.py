from django.contrib import admin

from .models import EventoAuditoria


@admin.register(EventoAuditoria)
class EventoAuditoriaAdmin(admin.ModelAdmin):
    list_display = ("acao", "modelo", "objeto_id", "usuario", "criado_em")
    list_filter = ("acao", "app", "modelo", "criado_em")
    search_fields = ("descricao", "objeto_id", "usuario__username")
    readonly_fields = (
        "usuario",
        "acao",
        "app",
        "modelo",
        "objeto_id",
        "descricao",
        "dados",
        "criado_em",
    )
