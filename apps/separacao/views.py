import json

# messages permite enviar avisos de sucesso/erro para o template apos redirecionamentos.
from django.contrib import messages
# Decorators e mixins de autenticacao/permissao bloqueiam acessos indevidos.
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# JsonResponse devolve dados em JSON para chamadas AJAX/fetch.
from django.http import JsonResponse
# get_object_or_404 busca um objeto e retorna erro 404 automaticamente se nao existir.
from django.shortcuts import get_object_or_404
# reverse_lazy monta urls pelo name somente quando necessario, util em atributos de classes.
from django.urls import reverse_lazy
# method_decorator aplica decorators de function-based views em class-based views.
from django.utils.decorators import method_decorator
# ensure_csrf_cookie garante que a pagina entregue o cookie usado pelo JavaScript em POST AJAX.
from django.views.decorators.csrf import ensure_csrf_cookie
# require_GET/require_POST restringem o metodo HTTP aceito pela view.
from django.views.decorators.http import require_GET, require_POST
# Generic views implementam CRUD comum: listar, criar, detalhar, editar e excluir.
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

# Model e service de auditoria registram acoes importantes do usuario.
from apps.auditoria.models import EventoAuditoria
from apps.auditoria.services import registrar_evento

from .forms import SeparacaoForm
from .models import Separacao
from .services import (
    atualizar_status,
    buscar_separacoes_datatable,
    contexto_listagem,
    dados_auditoria,
    filtrar_separacoes,
    indicadores_rapidos,
    serializar_separacao_datatable,
)


class SeparacaoPermissionMixin(LoginRequiredMixin, PermissionRequiredMixin):
    # Mixin reutilizavel para exigir login e permissao basica do modulo separacao.
    # Views especificas podem sobrescrever permission_required para exigir permissoes extras.
    permission_required = "separacao.access_separacao"


@method_decorator(ensure_csrf_cookie, name="dispatch")
class SeparacaoListView(SeparacaoPermissionMixin, ListView):
    # model informa qual tabela sera listada.
    model = Separacao
    # context_object_name define o nome usado no template: {% for separacao in separacoes %}.
    context_object_name = "separacoes"
    # paginate_by divide a listagem em paginas de 20 registros.
    paginate_by = 20
    # template_name aponta para o HTML renderizado por esta view.
    template_name = "separacao/separacao_list.html"

    def get_queryset(self):
        # request.GET contem os filtros enviados pela URL, como ?grupo=...&status=...
        # O service aplica os filtros e devolve um QuerySet do Django.
        return filtrar_separacoes(self.request.GET)

    def get_context_data(self, **kwargs):
        # super() monta o contexto padrao da ListView: separacoes, page_obj, paginator etc.
        context = super().get_context_data(**kwargs)
        # contexto_listagem adiciona opcoes de filtros, badges e querystring de paginacao.
        context.update(contexto_listagem(self.request.GET))
        return context


class SeparacaoDetailView(SeparacaoPermissionMixin, DetailView):
    # DetailView busca um unico registro pelo pk recebido na URL.
    model = Separacao
    context_object_name = "separacao"
    template_name = "separacao/separacao_detail.html"


class SeparacaoCreateView(SeparacaoPermissionMixin, CreateView):
    # CreateView exibe o formulario em GET e salva um novo objeto em POST valido.
    model = Separacao
    form_class = SeparacaoForm
    # Para criar, o usuario precisa acessar o modulo e possuir a permissao de criacao.
    permission_required = ("separacao.access_separacao", "separacao.create_record")
    template_name = "separacao/separacao_form.html"

    def form_valid(self, form):
        # super().form_valid(form) salva o objeto e define self.object.
        response = super().form_valid(form)
        # Depois de salvar, gravamos auditoria para rastrear quem criou o registro.
        registrar_evento(
            self.request.user,
            EventoAuditoria.Acao.CRIACAO,
            self.object,
            f"Separacao criada: {self.object}",
            dados_auditoria(self.object),
        )
        # messages.success sera exibido pelo partial templates/partials/messages.html.
        messages.success(self.request, "Registro de separacao criado com sucesso.")
        return response


class SeparacaoUpdateView(SeparacaoPermissionMixin, UpdateView):
    # UpdateView carrega um objeto existente, valida o formulario e salva alteracoes.
    model = Separacao
    form_class = SeparacaoForm
    permission_required = ("separacao.access_separacao", "separacao.edit_record")
    template_name = "separacao/separacao_form.html"

    def form_valid(self, form):
        # A edicao so chega aqui quando o formulario passou pelas validacoes do form/model.
        response = super().form_valid(form)
        # Auditoria registra a alteracao com um resumo do objeto editado.
        registrar_evento(
            self.request.user,
            EventoAuditoria.Acao.EDICAO,
            self.object,
            f"Separacao editada: {self.object}",
            dados_auditoria(self.object),
        )
        messages.success(self.request, "Registro de separacao atualizado com sucesso.")
        return response


class SeparacaoDeleteView(SeparacaoPermissionMixin, DeleteView):
    # DeleteView mostra uma tela de confirmacao e exclui o objeto via POST.
    model = Separacao
    context_object_name = "separacao"
    permission_required = ("separacao.access_separacao", "separacao.delete_record")
    # success_url define para onde o usuario volta depois da exclusao.
    success_url = reverse_lazy("separacao:list")
    template_name = "separacao/separacao_confirm_delete.html"

    def form_valid(self, form):
        # A auditoria e registrada antes da exclusao para ainda termos acesso aos dados do objeto.
        registrar_evento(
            self.request.user,
            EventoAuditoria.Acao.EXCLUSAO,
            self.object,
            f"Separacao excluida: {self.object}",
            dados_auditoria(self.object),
        )
        messages.success(self.request, "Registro de separacao excluido com sucesso.")
        return super().form_valid(form)


@login_required
@permission_required(
    ("separacao.access_separacao", "separacao.edit_record"),
    raise_exception=True,
)
@require_POST
def atualizar_status_json(request, pk):
    # Endpoint AJAX chamado pelo select de status na tabela.
    # pk vem da URL /separacao/api/<pk>/status/.
    separacao = get_object_or_404(Separacao, pk=pk)

    try:
        # request.body chega como bytes; decode transforma em texto; json.loads transforma em dict.
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        # Status 400 indica erro do cliente: o corpo enviado nao era JSON valido.
        return JsonResponse({"ok": False, "error": "JSON invalido."}, status=400)

    # O JavaScript envia qual campo de status quer alterar e qual novo valor salvar.
    field_name = payload.get("field")
    value = payload.get("value")

    try:
        # O service valida se o campo e valor sao permitidos antes de salvar no banco.
        atualizar_status(separacao, field_name, value)
    except ValueError as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=400)

    # Toda alteracao de status tambem entra na trilha de auditoria.
    registrar_evento(
        request.user,
        EventoAuditoria.Acao.EDICAO,
        separacao,
        f"Status atualizado: {field_name}",
        dados_auditoria(separacao) | {field_name: value},
    )

    # Retorna JSON para o fetch atualizar a interface sem recarregar a pagina.
    return JsonResponse(
        {
            "ok": True,
            "id": separacao.pk,
            "field": field_name,
            "value": value,
            "display": getattr(separacao, f"get_{field_name}_display")(),
        }
    )


@login_required
@permission_required("separacao.access_separacao", raise_exception=True)
@require_GET
def indicadores_json(request):
    # Endpoint usado pelo JavaScript para preencher os cards numericos da listagem.
    # Ele reaproveita os filtros atuais enviados por querystring.
    return JsonResponse({"ok": True, "indicadores": indicadores_rapidos(request.GET)})


@login_required
@permission_required("separacao.access_separacao", raise_exception=True)
@require_GET
def busca_datatable_json(request):
    # Endpoint preparado para busca dinamica via AJAX.
    # A consulta e limitada a 50 itens para evitar respostas grandes.
    queryset = buscar_separacoes_datatable(request.GET)[:50]
    # Cada objeto do QuerySet e convertido em dict simples para virar JSON.
    registros = [serializar_separacao_datatable(item) for item in queryset]

    return JsonResponse(
        {
            "ok": True,
            "q": request.GET.get("q", ""),
            "total": len(registros),
            "results": registros,
        }
    )
