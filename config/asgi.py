"""Configuracao ASGI do projeto.

ASGI e usado por servidores capazes de lidar com HTTP assincrono, WebSockets
e outras conexoes de longa duracao. Mesmo que o projeto ainda use views
sincronas comuns, manter este arquivo pronto facilita deploys futuros.
"""

# os configura variaveis de ambiente antes de inicializar o Django.
import os

# get_asgi_application cria o objeto chamado pelo servidor ASGI.
from django.core.asgi import get_asgi_application

# Settings padrao do ambiente local.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

# application e o ponto de entrada que servidores ASGI procuram.
application = get_asgi_application()
