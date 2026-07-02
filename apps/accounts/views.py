from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView


class AccountLoginView(LoginView):
    """Usa a autenticacao nativa do Django com template do sistema."""

    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class AccountLogoutView(LogoutView):
    """Encerra a sessao usando o fluxo nativo do Django."""

    http_method_names = ["post", "options"]


class LogoutConfirmView(LoginRequiredMixin, TemplateView):
    """Exibe uma confirmacao visual antes de encerrar a sessao."""

    template_name = "accounts/logout_confirm.html"
