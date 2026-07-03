from datetime import timedelta

# get_user_model retorna o model de usuario configurado no projeto.
from django.contrib.auth import get_user_model
# Q permite montar buscas com OR no banco de dados.
from django.db.models import Q
# reverse transforma o name de uma rota em URL, evitando escrever caminhos fixos.
from django.urls import reverse
# timezone fornece a data local para filtros de vencimento.
from django.utils import timezone

from .models import Separacao


# Dicionarios de classes Tailwind usados para pintar badges conforme o valor salvo no banco.
# A chave e o valor interno do TextChoices; o valor e a lista de classes CSS.
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

# Opcoes exibidas no select de situacao do vencimento na tela de filtros.
VENCIMENTO_OPTIONS = [
    ("", "Todos"),
    ("vencidos", "Vencidos"),
    ("hoje", "Vence hoje"),
    ("proximos", "Proximos"),
]


def montar_filtros_listagem(params):
    """Normaliza os filtros aceitos pela listagem principal."""

    # params normalmente e request.GET. Usamos get(..., "") para evitar KeyError
    # e para o template sempre receber strings, mesmo quando o filtro nao foi enviado.
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

    # Copiamos a querystring para nao alterar request.GET diretamente.
    query_params = params.copy()
    # Ao trocar de pagina, removemos page antigo para montar links page=novo corretamente.
    query_params.pop("page", None)
    return query_params.urlencode()


def contexto_listagem(params):
    """Agrupa dados auxiliares da listagem para manter a view pequena."""

    # Este contexto complementa o contexto padrao da ListView.
    # Ele alimenta selects, badges, filtros preenchidos e links de paginacao do template.
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

    # select_related("atribuido") faz JOIN com a tabela de usuario.
    # Isso evita uma consulta extra para cada linha ao exibir o responsavel no template.
    queryset = Separacao.objects.select_related("atribuido")
    # strip remove espacos acidentais enviados pelos inputs.
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

    # Cada if aplica um filtro apenas quando o usuario preencheu aquele campo.
    if data:
        queryset = queryset.filter(data=data)
    # __gte significa "maior ou igual"; usado para inicio do intervalo.
    if data_inicio:
        queryset = queryset.filter(data__gte=data_inicio)
    # __lte significa "menor ou igual"; usado para fim do intervalo.
    if data_fim:
        queryset = queryset.filter(data__lte=data_fim)
    # __icontains faz busca parcial sem diferenciar maiusculas/minusculas.
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
        # Proximos considera registros que vencem nos proximos 7 dias.
        queryset = queryset.filter(vencimento__gt=hoje, vencimento__lte=hoje + timedelta(days=7))

    # QuerySet ainda e preguiçoso: a consulta real ocorre quando a view/template iterar ou contar.
    return queryset


def buscar_separacoes_datatable(params):
    """Prepara a busca textual AJAX usando os mesmos filtros operacionais."""

    # Primeiro reaproveitamos todos os filtros da listagem para manter os resultados consistentes.
    queryset = filtrar_separacoes(params)
    termo = params.get("q", "").strip()

    if termo:
        # Q(... ) | Q(... ) cria uma busca OR em varias colunas.
        # Campos com atribuido__ acessam dados do usuario relacionado pela ForeignKey.
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

    # JSON nao consegue enviar objetos Django diretamente.
    # Por isso transformamos cada campo importante em string, numero ou dict simples.
    atribuido = ""
    if separacao.atribuido:
        # get_full_name usa first_name + last_name; se estiver vazio, usamos username.
        atribuido = separacao.atribuido.get_full_name() or separacao.atribuido.username

    return {
        # Datas sao formatadas como texto no padrao brasileiro para aparecerem direto na tabela.
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
            # Links de acao sao montados por name de rota para acompanhar mudancas futuras em urls.py.
            "detalhe": reverse("separacao:detail", kwargs={"pk": separacao.pk}),
            "editar": reverse("separacao:update", kwargs={"pk": separacao.pk}),
            "excluir": reverse("separacao:delete", kwargs={"pk": separacao.pk}),
        },
    }


def status_badge_class(status):
    # Fallback garante uma classe neutra se surgir um status sem mapeamento visual.
    return STATUS_BADGE_CLASSES.get(status, "bg-slate-50 text-slate-700 ring-slate-600/20")


# Campos que o endpoint AJAX permite alterar.
# Esse mapa evita que o usuario envie qualquer nome de campo e altere dados indevidos.
STATUS_FIELDS = {
    "status_operacional": Separacao.StatusOperacional,
    "status_documento": Separacao.StatusDocumento,
    "status_autorizacao": Separacao.StatusAutorizacao,
}


def atualizar_status(separacao, field_name, value):
    """Atualiza campos de status permitidos validando contra as choices do model."""

    # Verifica se o campo enviado pelo JavaScript esta na lista de campos permitidos.
    choices = STATUS_FIELDS.get(field_name)
    if choices is None:
        msg = "Campo de status invalido."
        raise ValueError(msg)

    # Monta o conjunto de valores internos aceitos pelas choices do model.
    valid_values = {choice.value for choice in choices}
    if value not in valid_values:
        msg = "Valor de status invalido."
        raise ValueError(msg)

    # setattr altera dinamicamente o campo informado em field_name.
    setattr(separacao, field_name, value)
    # update_fields salva apenas o campo alterado e atualizado_em, reduzindo escrita no banco.
    separacao.save(update_fields=[field_name, "atualizado_em"])
    return separacao


def indicadores_rapidos(params):
    """Calcula indicadores simples usando os mesmos filtros da listagem."""

    # Como usamos filtrar_separacoes, os cards respeitam os mesmos filtros da tabela.
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

    # Guardamos somente dados essenciais para auditoria, sem depender do objeto existir para sempre.
    return {
        "documento": separacao.documento,
        "romaneio": separacao.romaneio,
        "status": separacao.status,
        "quantidade": separacao.quantidade,
        "atribuido": separacao.atribuido_id,
    }
