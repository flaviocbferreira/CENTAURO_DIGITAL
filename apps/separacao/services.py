from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone

from .models import Separacao


STATUS_BADGE_CLASSES = {
    Separacao.Status.ABERTA: "bg-sky-50 text-sky-700 ring-sky-600/20",
    Separacao.Status.EM_ANDAMENTO: "bg-amber-50 text-amber-700 ring-amber-600/20",
    Separacao.Status.CONCLUIDA: "bg-emerald-50 text-emerald-700 ring-emerald-600/20",
    Separacao.Status.CANCELADA: "bg-rose-50 text-rose-700 ring-rose-600/20",
}

TIPO_BADGE_CLASSES = {
    Separacao.Tipo.NORMAL: "bg-slate-100 text-slate-700 ring-slate-500/15",
    Separacao.Tipo.PRIORITARIA: "bg-amber-50 text-amber-800 ring-amber-600/20",
    Separacao.Tipo.URGENTE: "bg-rose-50 text-rose-800 ring-rose-600/20",
}

STATUS_OPERACIONAL_BADGE_CLASSES = {
    Separacao.StatusOperacional.PENDENTE: "bg-amber-50 text-amber-800 ring-amber-600/20",
    Separacao.StatusOperacional.EM_SEPARACAO: "bg-sky-50 text-sky-800 ring-sky-600/20",
    Separacao.StatusOperacional.CONFERIDA: "bg-indigo-50 text-indigo-800 ring-indigo-600/20",
    Separacao.StatusOperacional.FINALIZADA: "bg-emerald-50 text-emerald-800 ring-emerald-600/20",
}

VENCIMENTO_OPTIONS = [
    ("", "Todos"),
    ("vencidos", "Vencidos"),
    ("hoje", "Vence hoje"),
    ("proximos", "Proximos"),
]


def montar_filtros_listagem(params):
    """Normaliza os filtros aceitos pela listagem principal."""

    return {
        "data": params.get("data", ""),
        "data_inicio": params.get("data_inicio", ""),
        "data_fim": params.get("data_fim", ""),
        "grupo": params.get("grupo", ""),
        "status_operacional": params.get("status_operacional", ""),
        "atribuido": params.get("atribuido", ""),
        "vencimento_situacao": params.get("vencimento_situacao", ""),
    }


def montar_querystring_paginacao(params):
    """Remove apenas o numero da pagina para preservar filtros na navegacao."""

    query_params = params.copy()
    query_params.pop("page", None)
    return query_params.urlencode()


def contexto_listagem(params):
    """Agrupa dados auxiliares da listagem para manter a view pequena."""

    return {
        "status_operacional_options": Separacao.StatusOperacional.choices,
        "usuarios_options": get_user_model().objects.order_by("first_name", "username"),
        "vencimento_options": VENCIMENTO_OPTIONS,
        "status_badges": {
            value: status_badge_class(value) for value, _label in Separacao.Status.choices
        },
        "tipo_badges": TIPO_BADGE_CLASSES,
        "status_operacional_badges": STATUS_OPERACIONAL_BADGE_CLASSES,
        "filters": montar_filtros_listagem(params),
        "pagination_query": montar_querystring_paginacao(params),
    }


def filtrar_separacoes(params):
    """Aplica filtros visuais da listagem sem colocar regra na view/template."""

    queryset = Separacao.objects.select_related("atribuido")
    data = params.get("data", "").strip()
    data_inicio = params.get("data_inicio", "").strip()
    data_fim = params.get("data_fim", "").strip()
    grupo = params.get("grupo", "").strip()
    status_operacional = params.get("status_operacional", "").strip()
    atribuido = params.get("atribuido", "").strip()
    vencimento_situacao = (
        params.get("vencimento_situacao", "").strip()
        or params.get("vencimento", "").strip()
    )
    hoje = timezone.localdate()

    if data:
        queryset = queryset.filter(data=data)
    if data_inicio:
        queryset = queryset.filter(data__gte=data_inicio)
    if data_fim:
        queryset = queryset.filter(data__lte=data_fim)
    if grupo:
        queryset = queryset.filter(grupo__icontains=grupo)
    if status_operacional:
        queryset = queryset.filter(status_operacional=status_operacional)
    if atribuido:
        queryset = queryset.filter(atribuido_id=atribuido)
    if vencimento_situacao == "vencidos":
        queryset = queryset.filter(vencimento__lt=hoje)
    elif vencimento_situacao == "hoje":
        queryset = queryset.filter(vencimento=hoje)
    elif vencimento_situacao == "proximos":
        queryset = queryset.filter(vencimento__gt=hoje, vencimento__lte=hoje + timedelta(days=7))

    return queryset


def buscar_separacoes_datatable(params):
    """Prepara a busca textual AJAX usando os mesmos filtros operacionais."""

    queryset = filtrar_separacoes(params)
    termo = params.get("q", "").strip()

    if termo:
        queryset = queryset.filter(
            Q(romaneio__icontains=termo)
            | Q(documento__icontains=termo)
            | Q(grupo__icontains=termo)
            | Q(status_operacional__icontains=termo)
            | Q(atribuido__username__icontains=termo)
            | Q(atribuido__first_name__icontains=termo)
            | Q(atribuido__last_name__icontains=termo)
            | Q(anotacoes__icontains=termo)
        )

    return queryset


def serializar_separacao_datatable(separacao):
    """Serializa um registro com as colunas exibidas no DataTable operacional."""

    atribuido = ""
    if separacao.atribuido:
        atribuido = separacao.atribuido.get_full_name() or separacao.atribuido.username

    return {
        "data": separacao.data.strftime("%d/%m/%Y"),
        "romaneio": separacao.romaneio,
        "documento": separacao.documento,
        "grupo": separacao.grupo,
        "qtd_doc": separacao.quantidade,
        "vencimento": separacao.vencimento.strftime("%d/%m/%Y")
        if separacao.vencimento
        else "",
        "status_tipo": separacao.get_tipo_display(),
        "status_op": separacao.get_status_operacional_display(),
        "qtde_pen": separacao.quantidade_pendente,
        "atribuido": atribuido,
        "anotacoes": separacao.anotacoes,
        "acoes": {
            "detalhe": reverse("separacao:detail", kwargs={"pk": separacao.pk}),
            "editar": reverse("separacao:update", kwargs={"pk": separacao.pk}),
            "excluir": reverse("separacao:delete", kwargs={"pk": separacao.pk}),
        },
    }


def status_badge_class(status):
    return STATUS_BADGE_CLASSES.get(status, "bg-slate-50 text-slate-700 ring-slate-600/20")


STATUS_FIELDS = {
    "status_operacional": Separacao.StatusOperacional,
    "status_documento": Separacao.StatusDocumento,
    "status_autorizacao": Separacao.StatusAutorizacao,
}


def atualizar_status(separacao, field_name, value):
    """Atualiza campos de status permitidos validando contra as choices do model."""

    choices = STATUS_FIELDS.get(field_name)
    if choices is None:
        msg = "Campo de status invalido."
        raise ValueError(msg)

    valid_values = {choice.value for choice in choices}
    if value not in valid_values:
        msg = "Valor de status invalido."
        raise ValueError(msg)

    setattr(separacao, field_name, value)
    separacao.save(update_fields=[field_name, "atualizado_em"])
    return separacao


def indicadores_rapidos(params):
    """Calcula indicadores simples usando os mesmos filtros da listagem."""

    queryset = filtrar_separacoes(params)
    return {
        "total": queryset.count(),
        "abertas": queryset.filter(status=Separacao.Status.ABERTA).count(),
        "em_andamento": queryset.filter(status=Separacao.Status.EM_ANDAMENTO).count(),
        "concluidas": queryset.filter(status=Separacao.Status.CONCLUIDA).count(),
        "pendentes_operacionais": queryset.filter(
            status_operacional=Separacao.StatusOperacional.PENDENTE,
        ).count(),
    }


def dados_auditoria(separacao):
    """Monta um resumo estavel do registro para gravacao em auditoria."""

    return {
        "documento": separacao.documento,
        "romaneio": separacao.romaneio,
        "status": separacao.status,
        "quantidade": separacao.quantidade,
        "atribuido": separacao.atribuido_id,
    }
