# admin permite consultar eventos de auditoria pelo painel administrativo.
from django.contrib import admin

from .models import EventoAuditoria


@admin.register(EventoAuditoria)
class EventoAuditoriaAdmin(admin.ModelAdmin):
    # Colunas principais para inspecionar rapidamente cada evento.
    list_display = ("acao", "modelo", "objeto_id", "usuario", "criado_em")
    # Filtros laterais ajudam a encontrar eventos por tipo, app, model ou periodo.
    list_filter = ("acao", "app", "modelo", "criado_em")
    # search_fields habilita busca textual em descricao, id do objeto e usuario.
    search_fields = ("descricao", "objeto_id", "usuario__username")
    # Auditoria deve ser historico; por isso os campos ficam somente leitura no admin.
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
