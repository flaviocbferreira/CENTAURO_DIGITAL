# AppConfig registra metadados do app auditoria dentro do Django.
from django.apps import AppConfig


class AuditoriaConfig(AppConfig):
    # Tipo padrao das chaves primarias automaticas dos models do app.
    default_auto_field = "django.db.models.BigAutoField"
    # Caminho Python completo do app.
    name = "apps.auditoria"
