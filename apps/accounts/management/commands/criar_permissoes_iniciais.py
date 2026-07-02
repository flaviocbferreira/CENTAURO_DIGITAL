from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


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
    help = "Cria grupos e associa as permissoes iniciais do sistema."

    def handle(self, *args, **options):
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

        missing = sorted(
            {
                codename
                for codenames in GROUP_PERMISSIONS.values()
                for codename in codenames
                if codename not in permissions
            }
        )
        if missing:
            self.stderr.write(
                "Permissoes nao encontradas. Execute as migracoes antes: "
                + ", ".join(missing)
            )
            return

        for group_name, codenames in GROUP_PERMISSIONS.items():
            group, created = Group.objects.get_or_create(name=group_name)
            group.permissions.set([permissions[codename] for codename in codenames])
            action = "criado" if created else "atualizado"
            self.stdout.write(self.style.SUCCESS(f"Grupo {group_name} {action}."))
