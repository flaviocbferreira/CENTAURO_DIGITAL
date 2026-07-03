# Importa configuracoes comuns e sobrescreve apenas o que muda em producao.
from .base import *  # noqa: F403
# BASE_DIR monta caminhos; env le variaveis obrigatorias do ambiente.
from .base import BASE_DIR, env

# Ambiente de producao: DEBUG=False evita vazar erros, variaveis e paths internos.
DEBUG = False

# Chave criptografica obrigatoria em producao.
SECRET_KEY = env("SECRET_KEY")

# Dominios autorizados a servir a aplicacao em producao.
ALLOWED_HOSTS = env("ALLOWED_HOSTS")

# Banco inicial mantido em SQLite.
# Quando MySQL ou PostgreSQL for escolhido, a troca deve ficar concentrada aqui,
# sem alterar models, views ou services dos apps.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Envia o cookie CSRF apenas por HTTPS.
CSRF_COOKIE_SECURE = True

# Envia o cookie de sessao apenas por HTTPS.
SESSION_COOKIE_SECURE = True

# Redireciona todo acesso HTTP para HTTPS.
SECURE_SSL_REDIRECT = True

# Define por quanto tempo navegadores devem lembrar que o site usa HTTPS.
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=31536000)

# Aplica HSTS tambem aos subdominios.
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Permite incluir o dominio na lista de preload HSTS dos navegadores.
SECURE_HSTS_PRELOAD = True

# Impede que o site seja aberto dentro de iframes.
X_FRAME_OPTIONS = "DENY"

# Bloqueia interpretacao indevida de tipos de conteudo pelo navegador.
SECURE_CONTENT_TYPE_NOSNIFF = True
