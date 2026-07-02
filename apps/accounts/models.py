from django.db import models


class PermissaoSistema(models.Model):
    """Agrupa permissoes gerais que nao pertencem a um model operacional."""

    class Meta:
        app_label = "accounts"
        managed = False
        default_permissions = ()
        permissions = [
            ("access_dashboard", "Pode acessar o dashboard"),
            ("view_auditoria", "Pode visualizar auditoria"),
            ("export_data", "Pode exportar dados"),
        ]
