# pathlib.Path ajuda a montar caminhos de arquivos de forma portavel.
# Assim o mesmo projeto funciona no Windows, Linux ou servidor sem trocar barras manualmente.
from pathlib import Path

# django-environ le variaveis de ambiente e arquivos .env.
# Isso separa configuracoes sensiveis, como SECRET_KEY, do codigo versionado.
import environ

# BASE_DIR aponta para a raiz do projeto, onde ficam manage.py, templates, static e db.sqlite3.
# __file__ e o caminho deste arquivo; parent.parent.parent sobe de config/settings/base.py para a raiz.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Env define os tipos e valores padrao das variaveis lidas do ambiente.
# ALLOWED_HOSTS e lido como lista; se nao existir no .env, aceita localhost para desenvolvimento.
env = environ.Env(
    ALLOWED_HOSTS=(list, ["127.0.0.1", "localhost"]),
)

# Carrega variaveis locais quando o arquivo .env existir na raiz do projeto.
# Em producao, essas variaveis podem vir direto do servidor, sem arquivo .env.
env_file = BASE_DIR / ".env"
if env_file.exists():
    environ.Env.read_env(env_file)

# SECRET_KEY assina cookies, tokens e outras estruturas internas do Django.
# Ela deve vir do .env e nunca deve ser publicada em repositorios.
SECRET_KEY = env("SECRET_KEY")

# DJANGO_APPS sao apps prontos do framework.
# admin cria o painel administrativo, auth cuida de usuarios/permissoes,
# sessions guarda sessoes de login, messages exibe avisos, staticfiles serve CSS/JS/imagens.
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# LOCAL_APPS sao os apps criados dentro deste projeto.
# Cada string aponta para um pacote Python que possui models, views, urls e outras partes do modulo.
LOCAL_APPS = [
    "apps.accounts",
    "apps.auditoria",
    "apps.separacao",
]

# INSTALLED_APPS e a lista final que o Django usa para descobrir models, migrations,
# templates de apps, comandos de management e permissoes.
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS

# MIDDLEWARE e a fila de camadas executadas em cada request e response.
# A ordem importa: seguranca vem cedo, sessao precisa vir antes de autenticacao,
# CSRF protege formularios, e messages depende de sessao.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ROOT_URLCONF informa qual arquivo contem as rotas principais do projeto.
# A partir dele o Django inclui as urls dos apps.
ROOT_URLCONF = "config.urls"

# TEMPLATES configura como o Django encontra e renderiza arquivos HTML.
TEMPLATES = [
    {
        # Backend padrao de templates do Django, com sintaxe {% %} e {{ }}.
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # DIRS aponta para a pasta global templates/ na raiz do projeto.
        "DIRS": [BASE_DIR / "templates"],
        # APP_DIRS=True tambem permite templates dentro de cada app, se existirem.
        "APP_DIRS": True,
        "OPTIONS": {
            # Context processors colocam variaveis globais nos templates.
            # request permite acessar request/perms, auth fornece user/perms,
            # messages fornece mensagens de sucesso/erro.
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI_APPLICATION aponta para o objeto usado por servidores WSGI em producao.
WSGI_APPLICATION = "config.wsgi.application"

# Cada ambiente define seu proprio banco em dev.py ou prod.py.
# Este arquivo base deixa vazio para evitar duplicacao e facilitar trocar SQLite por outro banco.
DATABASES = {}

# Validadores de senha usados pelo app django.contrib.auth.
# Eles reduzem senhas fracas, parecidas com dados do usuario, comuns ou apenas numericas.
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Localizacao padrao do projeto.
# LANGUAGE_CODE traduz partes do admin/mensagens; TIME_ZONE controla datas e horas locais.
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
# USE_I18N habilita internacionalizacao/traducao.
USE_I18N = True
# USE_TZ faz o Django armazenar datas com timezone de forma consistente.
USE_TZ = True

# Arquivos estaticos do projeto: CSS, JavaScript, imagens e bibliotecas locais.
# STATIC_URL e o prefixo publico usado nos templates com {% static %}.
STATIC_URL = "static/"
# STATICFILES_DIRS informa pastas extras onde o Django procura arquivos estaticos em desenvolvimento.
STATICFILES_DIRS = [BASE_DIR / "static"]
# STATIC_ROOT e a pasta de destino do collectstatic em producao.
STATIC_ROOT = BASE_DIR / "staticfiles"

# Arquivos enviados por usuarios em ambiente local.
# MEDIA_URL e o prefixo publico; MEDIA_ROOT e a pasta fisica onde uploads ficam salvos.
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Campo automatico padrao para chaves primarias de models que nao declaram id manualmente.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Rotas de autenticacao usadas pelos mixins e decorators nativos do Django.
# LOGIN_URL recebe usuarios anonimos; LOGIN_REDIRECT_URL e destino apos login;
# LOGOUT_REDIRECT_URL e destino apos encerrar sessao.
LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "accounts:login"
