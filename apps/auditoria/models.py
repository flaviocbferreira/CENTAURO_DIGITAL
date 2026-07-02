from django.db import models


class EventoAuditoria(models.Model):
    class Acao(models.TextChoices):
        CRIACAO = "criacao", "Criacao"
        EDICAO = "edicao", "Edicao"
        EXCLUSAO = "exclusao", "Exclusao"

    usuario = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Usuario",
    )
    acao = models.CharField(max_length=20, choices=Acao.choices, verbose_name="Acao")
    app = models.CharField(max_length=80, verbose_name="App")
    modelo = models.CharField(max_length=80, verbose_name="Modelo")
    objeto_id = models.CharField(max_length=64, verbose_name="ID do objeto")
    descricao = models.CharField(max_length=255, verbose_name="Descricao")
    dados = models.JSONField(default=dict, blank=True, verbose_name="Dados")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Evento de auditoria"
        verbose_name_plural = "Eventos de auditoria"

    def __str__(self):
        return f"{self.get_acao_display()} - {self.modelo} #{self.objeto_id}"
