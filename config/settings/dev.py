# Importa todas as configuracoes comuns do projeto.
from .base import *  # noqa: F403
# BASE_DIR monta o caminho do SQLite; env le variaveis do .env.
from .base import BASE_DIR, env

# Ambiente local: DEBUG=True mostra paginas detalhadas de erro e recarrega arquivos.
# Nunca use DEBUG=True em producao.
DEBUG = True

# Hosts permitidos no ambiente local, lidos do .env para manter o padrao do projeto.
ALLOWED_HOSTS = env("ALLOWED_HOSTS")

# Banco SQLite local.
# ENGINE escolhe o backend do Django; NAME define o arquivo fisico do banco.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
