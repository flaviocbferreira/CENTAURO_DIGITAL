# LoginRequiredMixin protege views baseadas em classe para usuarios autenticados.
from django.contrib.auth.mixins import LoginRequiredMixin
# LoginView e LogoutView sao views prontas do Django para login e logout.
from django.contrib.auth.views import LoginView, LogoutView
# TemplateView renderiza uma pagina HTML sem formulario/model proprio.
from django.views.generic import TemplateView


class AccountLoginView(LoginView):
    """Usa a autenticacao nativa do Django com template do sistema."""

    # Template usado para exibir o formulario de usuario e senha.
    template_name = "accounts/login.html"
    # Se o usuario ja estiver logado, evita mostrar login novamente e redireciona.
    redirect_authenticated_user = True


class AccountLogoutView(LogoutView):
    """Encerra a sessao usando o fluxo nativo do Django."""

    # Logout deve acontecer via POST para evitar que um simples link GET encerre a sessao.
    http_method_names = ["post", "options"]


class LogoutConfirmView(LoginRequiredMixin, TemplateView):
    """Exibe uma confirmacao visual antes de encerrar a sessao."""

    # Esta tela tem o botao/formulario que faz POST para AccountLogoutView.
    template_name = "accounts/logout_confirm.html"
