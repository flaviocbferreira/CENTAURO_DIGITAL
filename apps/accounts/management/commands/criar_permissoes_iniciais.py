# Group e Permission sao models nativos do Django para autorizacao.
from django.contrib.auth.models import Group, Permission
# BaseCommand e a classe base para comandos chamados com python manage.py <comando>.
from django.core.management.base import BaseCommand


# Mapa de perfis iniciais do sistema.
# Cada grupo recebe uma lista de codenames de permissoes ja criadas pelas migrations.
GROUP_PERMISSIONS = {
    "Administrador": [
        "access_dashboard",
        "access_separacao",
        "create_record",
        "edit_record",
        "delete_record",
        "add_separacao",
        "change_separacao",
        "delete_separacao",
        "view_auditoria",
        "export_data",
    ],
    "Supervisor": [
        "access_dashboard",
        "access_separacao",
        "create_record",
        "edit_record",
        "add_separacao",
        "change_separacao",
        "view_auditoria",
        "export_data",
    ],
    "Operador": [
        "access_dashboard",
        "access_separacao",
        "create_record",
        "edit_record",
        "add_separacao",
        "change_separacao",
    ],
    "Auditor": [
        "access_dashboard",
        "view_auditoria",
        "export_data",
    ],
}


class Command(BaseCommand):
    # help aparece quando rodamos python manage.py help criar_permissoes_iniciais.
    help = "Cria grupos e associa as permissoes iniciais do sistema."

    def handle(self, *args, **options):
        # Busca no banco todas as permissoes necessarias e monta um dict por codename.
        permissions = {
            permission.codename: permission
            for permission in Permission.objects.filter(
                codename__in={
                    codename
                    for codenames in GROUP_PERMISSIONS.values()
                    for codename in codenames
                }
            )
        }

        # Verifica se alguma permissao esperada ainda nao existe.
        # Isso normalmente acontece quando as migrations nao foram aplicadas.
        missing = sorted(
            {
                codename
                for codenames in GROUP_PERMISSIONS.values()
                for codename in codenames
                if codename not in permissions
            }
        )
        if missing:
            # stderr indica mensagem de erro/alerta no terminal.
            self.stderr.write(
                "Permissoes nao encontradas. Execute as migracoes antes: "
                + ", ".join(missing)
            )
            return

        # Para cada perfil, cria o grupo se necessario e sincroniza suas permissoes.
        for group_name, codenames in GROUP_PERMISSIONS.items():
            group, created = Group.objects.get_or_create(name=group_name)
            # set substitui as permissoes do grupo pela lista oficial do mapa acima.
            group.permissions.set([permissions[codename] for codename in codenames])
            action = "criado" if created else "atualizado"
            # SUCCESS colore a mensagem em terminais que suportam estilo.
            self.stdout.write(self.style.SUCCESS(f"Grupo {group_name} {action}."))
