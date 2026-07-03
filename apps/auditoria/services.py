from .models import EventoAuditoria


def registrar_evento(usuario, acao, objeto, descricao, dados=None):
    """Registra uma acao importante executada em um objeto do sistema."""

    # create insere uma nova linha na tabela EventoAuditoria.
    EventoAuditoria.objects.create(
        # Se usuario nao estiver autenticado, salvamos None para evitar erro.
        usuario=usuario if getattr(usuario, "is_authenticated", False) else None,
        acao=acao,
        # _meta guarda metadados do model auditado, como app_label e model_name.
        app=objeto._meta.app_label,
        modelo=objeto._meta.model_name,
        # pk e convertido para string para o campo aceitar diferentes tipos de chave.
        objeto_id=str(objeto.pk),
        descricao=descricao,
        # dados or {} evita salvar None em um JSONField que espera dict por padrao.
        dados=dados or {},
    )
