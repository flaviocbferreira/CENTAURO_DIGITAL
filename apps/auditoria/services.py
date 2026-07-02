from .models import EventoAuditoria


def registrar_evento(usuario, acao, objeto, descricao, dados=None):
    """Registra uma acao importante executada em um objeto do sistema."""

    EventoAuditoria.objects.create(
        usuario=usuario if getattr(usuario, "is_authenticated", False) else None,
        acao=acao,
        app=objeto._meta.app_label,
        modelo=objeto._meta.model_name,
        objeto_id=str(objeto.pk),
        descricao=descricao,
        dados=dados or {},
    )
