#!/usr/bin/env python
"""Utilitario de linha de comando do Django para tarefas administrativas."""

# os permite configurar variaveis de ambiente antes de carregar o Django.
import os
# sys fornece os argumentos digitados no terminal, como runserver, migrate e createsuperuser.
import sys


def main():
    """Executa comandos administrativos do Django."""

    # Define o settings padrao para desenvolvimento local.
    # Pode ser sobrescrito por DJANGO_SETTINGS_MODULE no ambiente.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
    try:
        # execute_from_command_line interpreta sys.argv e chama o comando correto do Django.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Erro comum quando dependencias nao foram instaladas ou a virtualenv nao esta ativa.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Entrega os argumentos do terminal para o Django executar o comando solicitado.
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    # Garante que main rode apenas quando este arquivo for executado diretamente.
    main()
