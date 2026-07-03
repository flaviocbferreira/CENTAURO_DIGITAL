# Mixins de autenticacao/permissao protegem paginas internas.
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# TemplateView renderiza um template e permite adicionar contexto.
from django.views.generic import TemplateView


class DashboardView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """Renderiza a pagina inicial visual, sem regra de negocio nesta etapa."""

    # Permissao geral declarada em apps.accounts.models.PermissaoSistema.
    permission_required = "accounts.access_dashboard"
    # Template principal do dashboard.
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        # Comeca com o contexto padrao da TemplateView.
        context = super().get_context_data(**kwargs)
        # Dados temporarios usados pelo partial de tabela no dashboard.
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

    # Template generico para telas ainda sem CRUD proprio.
    template_name = "dashboard/placeholder.html"


class SeparacaoPlaceholderView(PlaceholderView):
    # Exige permissao do modulo separacao quando esta classe for usada.
    permission_required = "separacao.access_separacao"


class AuditoriaPlaceholderView(PlaceholderView):
    # Exige permissao geral para visualizar auditoria.
    permission_required = "accounts.view_auditoria"
