# settings permite consultar DEBUG, MEDIA_URL e MEDIA_ROOT definidos nos settings ativos.
from django.conf import settings
# static cria rotas temporarias para servir arquivos de media durante o desenvolvimento.
from django.conf.urls.static import static
# admin expõe o painel administrativo nativo do Django em /admin/.
from django.contrib import admin
# include encaixa urls de um app dentro da url principal; path cria uma rota.
from django.urls import include, path

# Views de paginas globais do projeto, que nao pertencem a um CRUD especifico.
from .views import AuditoriaPlaceholderView, DashboardView

# urlpatterns e a tabela de rotas principal.
# O Django começa por este arquivo porque ROOT_URLCONF aponta para config.urls.
urlpatterns = [
    # Tudo que começa com /accounts/ e enviado para apps.accounts.urls.
    path("accounts/", include("apps.accounts.urls")),
    # Tudo que começa com /separacao/ e enviado para apps.separacao.urls.
    path("separacao/", include("apps.separacao.urls")),
    # Rota raiz do sistema. as_view() transforma a classe DashboardView em uma view chamavel.
    # name="dashboard" permite criar links com {% url 'dashboard' %} ou reverse("dashboard").
    path("", DashboardView.as_view(), name="dashboard"),
    # Pagina temporaria do modulo auditoria.
    # extra_context envia page_title para o template sem precisar criar outra view.
    path(
        "auditoria/",
        AuditoriaPlaceholderView.as_view(extra_context={"page_title": "Auditoria"}),
        name="auditoria",
    ),
    # Painel administrativo do Django para usuarios com permissao de staff.
    path("admin/", admin.site.urls),
]

# Em desenvolvimento, o Django pode servir arquivos enviados para MEDIA_ROOT.
# Em producao isso deve ficar com o servidor web ou storage dedicado, nao com o Django.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
