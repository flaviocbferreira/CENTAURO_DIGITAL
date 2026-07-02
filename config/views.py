from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView


class DashboardView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """Renderiza a pagina inicial visual, sem regra de negocio nesta etapa."""

    permission_required = "accounts.access_dashboard"
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["table_headers"] = ["Modulo", "Status", "Proxima acao"]
        context["table_rows"] = [
            ["Dashboard", "Base visual pronta", "Conectar indicadores"],
            ["Separacao", "Estrutura reservada", "Criar app do modulo"],
            ["Auditoria", "Estrutura reservada", "Criar trilha de acoes"],
            ["Administracao", "Django Admin ativo", "Configurar perfis"],
        ]
        return context


class PlaceholderView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """Renderiza paginas temporarias para modulos que serao criados depois."""

    template_name = "dashboard/placeholder.html"


class SeparacaoPlaceholderView(PlaceholderView):
    permission_required = "separacao.access_separacao"


class AuditoriaPlaceholderView(PlaceholderView):
    permission_required = "accounts.view_auditoria"
