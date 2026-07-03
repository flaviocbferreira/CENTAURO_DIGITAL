# AppConfig registra metadados do app accounts dentro do Django.
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    # Tipo padrao das chaves primarias automaticas dos models do app.
    default_auto_field = "django.db.models.BigAutoField"
    # Caminho Python completo do app.
    name = "apps.accounts"
