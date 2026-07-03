"""Configuracao WSGI do projeto.

WSGI e o ponto de entrada tradicional para servir aplicacoes Django em
servidores como Gunicorn, uWSGI ou mod_wsgi.
"""

# os configura variaveis de ambiente antes de inicializar o Django.
import os

# get_wsgi_application cria o objeto chamado pelo servidor WSGI.
from django.core.wsgi import get_wsgi_application

# Settings padrao do ambiente local.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

# application e o ponto de entrada que servidores WSGI procuram.
application = get_wsgi_application()
