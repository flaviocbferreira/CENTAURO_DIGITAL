from django.conf import settings
from django.db import models
from django.utils import timezone


class Separacao(models.Model):
    class Tipo(models.TextChoices):
        NORMAL = "normal", "Normal"
        PRIORITARIA = "prioritaria", "Prioritaria"
        URGENTE = "urgente", "Urgente"

    class Status(models.TextChoices):
        ABERTA = "aberta", "Aberta"
        EM_ANDAMENTO = "em_andamento", "Em andamento"
        CONCLUIDA = "concluida", "Concluida"
        CANCELADA = "cancelada", "Cancelada"

    class StatusOperacional(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        EM_SEPARACAO = "em_separacao", "Em separacao"
        CONFERIDA = "conferida", "Conferida"
        FINALIZADA = "finalizada", "Finalizada"

    class StatusDocumento(models.TextChoices):
        VALIDO = "valido", "Valido"
        DIVERGENTE = "divergente", "Divergente"
        BLOQUEADO = "bloqueado", "Bloqueado"

    class StatusAutorizacao(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        AUTORIZADO = "autorizado", "Autorizado"
        NEGADO = "negado", "Negado"

    data = models.DateField(verbose_name="Data")
    romaneio = models.CharField(max_length=50, verbose_name="Romaneio")
    documento = models.CharField(max_length=80, verbose_name="Documento")
    grupo = models.CharField(max_length=80, verbose_name="Grupo")
    quantidade = models.PositiveIntegerField(verbose_name="Quantidade")
    vencimento = models.DateField(verbose_name="Vencimento", null=True, blank=True)
    tipo = models.CharField(
        max_length=20,
        choices=Tipo.choices,
        default=Tipo.NORMAL,
        verbose_name="Tipo",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ABERTA,
        verbose_name="Status",
    )
    quantidade_pendente = models.PositiveIntegerField(
        default=0,
        verbose_name="Quantidade pendente",
    )
    status_operacional = models.CharField(
        max_length=30,
        choices=StatusOperacional.choices,
        default=StatusOperacional.PENDENTE,
        verbose_name="Status operacional",
    )
    status_documento = models.CharField(
        max_length=20,
        choices=StatusDocumento.choices,
        default=StatusDocumento.VALIDO,
        verbose_name="Status do documento",
    )
    quantidade_conferida = models.PositiveIntegerField(
        default=0,
        verbose_name="Quantidade conferida",
    )
    status_autorizacao = models.CharField(
        max_length=20,
        choices=StatusAutorizacao.choices,
        default=StatusAutorizacao.PENDENTE,
        verbose_name="Status da autorizacao",
    )
    atribuido = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="separacoes_atribuidas",
        verbose_name="Atribuido",
    )
    anotacoes = models.TextField(blank=True, verbose_name="Anotacoes")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        ordering = ["-data", "romaneio", "documento"]
        verbose_name = "Separacao"
        verbose_name_plural = "Separacoes"
        permissions = [
            ("access_separacao", "Pode acessar o modulo separacao"),
            ("create_record", "Pode criar registro"),
            ("edit_record", "Pode editar registro"),
            ("delete_record", "Pode excluir registro"),
        ]

    def __str__(self):
        return f"{self.documento} - {self.romaneio}"

    @property
    def motivo_alerta(self):
        """Resume pendencias operacionais para uso visual na tabela."""

        if self.vencimento and self.vencimento < timezone.localdate():
            return "Vencimento expirado"
        if self.quantidade_pendente > 0:
            return "Quantidade pendente"
        if self.status_operacional != self.StatusOperacional.FINALIZADA:
            return "Operacao nao finalizada"
        return "Ver detalhes do registro"

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("separacao:detail", kwargs={"pk": self.pk})
