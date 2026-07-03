# models fornece os campos e a classe base que viram tabela no banco.
from django.db import models


class EventoAuditoria(models.Model):
    """Tabela que registra acoes relevantes feitas pelos usuarios no sistema."""

    # Acao lista os tipos de eventos que a auditoria aceita hoje.
    class Acao(models.TextChoices):
        CRIACAO = "criacao", "Criacao"
        EDICAO = "edicao", "Edicao"
        EXCLUSAO = "exclusao", "Exclusao"

    # usuario aponta para auth.User. SET_NULL preserva o evento se o usuario for removido.
    usuario = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Usuario",
    )
    # acao guarda o tipo do evento usando as choices acima.
    acao = models.CharField(max_length=20, choices=Acao.choices, verbose_name="Acao")
    # app e modelo identificam de qual app/model veio o objeto auditado.
    app = models.CharField(max_length=80, verbose_name="App")
    modelo = models.CharField(max_length=80, verbose_name="Modelo")
    # objeto_id e texto para aceitar ids de formatos diferentes caso o projeto evolua.
    objeto_id = models.CharField(max_length=64, verbose_name="ID do objeto")
    # descricao humana do que aconteceu, exibida no admin.
    descricao = models.CharField(max_length=255, verbose_name="Descricao")
    # JSONField guarda um resumo estruturado do estado do objeto no momento da acao.
    dados = models.JSONField(default=dict, blank=True, verbose_name="Dados")
    # Momento em que o evento foi criado.
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    class Meta:
        # Eventos mais recentes aparecem primeiro.
        ordering = ["-criado_em"]
        verbose_name = "Evento de auditoria"
        verbose_name_plural = "Eventos de auditoria"

    def __str__(self):
        # Representacao textual usada no admin e em logs.
        return f"{self.get_acao_display()} - {self.modelo} #{self.objeto_id}"
