# models e importado porque permissoes customizadas sao declaradas em uma classe Model.
from django.db import models


class PermissaoSistema(models.Model):
    """Agrupa permissoes gerais que nao pertencem a um model operacional."""

    class Meta:
        # app_label força essas permissoes a pertencerem ao app accounts.
        app_label = "accounts"
        # managed=False informa que o Django nao deve criar tabela para este model.
        # Ele existe apenas para gerar permissoes gerais via migrations.
        managed = False
        # default_permissions=() impede criar add/change/delete/view para este model ficticio.
        default_permissions = ()
        # Permissoes usadas por mixins/decorators em views do sistema.
        permissions = [
            ("access_dashboard", "Pode acessar o dashboard"),
            ("view_auditoria", "Pode visualizar auditoria"),
            ("export_data", "Pode exportar dados"),
        ]
