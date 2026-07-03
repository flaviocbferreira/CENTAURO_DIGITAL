# path cria rotas especificas do app de contas.
from django.urls import path

from .views import AccountLoginView, AccountLogoutView, LogoutConfirmView

# Namespace usado em settings.LOGIN_URL e templates: accounts:login, accounts:logout etc.
app_name = "accounts"

urlpatterns = [
    # Exibe e processa o formulario de login nativo do Django.
    path("login/", AccountLoginView.as_view(), name="login"),
    # Exibe uma tela de confirmacao antes do logout.
    path("logout/", LogoutConfirmView.as_view(), name="logout"),
    # Recebe POST e encerra a sessao do usuario.
    path("logout/confirm/", AccountLogoutView.as_view(), name="logout_confirm"),
]
