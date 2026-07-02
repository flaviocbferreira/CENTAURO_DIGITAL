from .base import *  # noqa: F403
from .base import BASE_DIR, env

# Ambiente local: debug ativo e banco SQLite para desenvolvimento rapido.
DEBUG = True

# Hosts permitidos no ambiente local, lidos do .env para manter o padrao do projeto.
ALLOWED_HOSTS = env("ALLOWED_HOSTS")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
