import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

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
    permission_required = "separacao.access_separacao"


@method_decorator(ensure_csrf_cookie, name="dispatch")
class SeparacaoListView(SeparacaoPermissionMixin, ListView):
    model = Separacao
    context_object_name = "separacoes"
    paginate_by = 20
    template_name = "separacao/separacao_list.html"

    def get_queryset(self):
        return filtrar_separacoes(self.request.GET)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(contexto_listagem(self.request.GET))
        return context


class SeparacaoDetailView(SeparacaoPermissionMixin, DetailView):
    model = Separacao
    context_object_name = "separacao"
    template_name = "separacao/separacao_detail.html"


class SeparacaoCreateView(SeparacaoPermissionMixin, CreateView):
    model = Separacao
    form_class = SeparacaoForm
    permission_required = ("separacao.access_separacao", "separacao.create_record")
    template_name = "separacao/separacao_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        registrar_evento(
            self.request.user,
            EventoAuditoria.Acao.CRIACAO,
            self.object,
            f"Separacao criada: {self.object}",
            dados_auditoria(self.object),
        )
        messages.success(self.request, "Registro de separacao criado com sucesso.")
        return response


class SeparacaoUpdateView(SeparacaoPermissionMixin, UpdateView):
    model = Separacao
    form_class = SeparacaoForm
    permission_required = ("separacao.access_separacao", "separacao.edit_record")
    template_name = "separacao/separacao_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
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
    model = Separacao
    context_object_name = "separacao"
    permission_required = ("separacao.access_separacao", "separacao.delete_record")
    success_url = reverse_lazy("separacao:list")
    template_name = "separacao/separacao_confirm_delete.html"

    def form_valid(self, form):
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
    separacao = get_object_or_404(Separacao, pk=pk)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "JSON invalido."}, status=400)

    field_name = payload.get("field")
    value = payload.get("value")

    try:
        atualizar_status(separacao, field_name, value)
    except ValueError as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=400)

    registrar_evento(
        request.user,
        EventoAuditoria.Acao.EDICAO,
        separacao,
        f"Status atualizado: {field_name}",
        dados_auditoria(separacao) | {field_name: value},
    )

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
    return JsonResponse({"ok": True, "indicadores": indicadores_rapidos(request.GET)})


@login_required
@permission_required("separacao.access_separacao", raise_exception=True)
@require_GET
def busca_datatable_json(request):
    queryset = buscar_separacoes_datatable(request.GET)[:50]
    registros = [serializar_separacao_datatable(item) for item in queryset]

    return JsonResponse(
        {
            "ok": True,
            "q": request.GET.get("q", ""),
            "total": len(registros),
            "results": registros,
        }
    )
