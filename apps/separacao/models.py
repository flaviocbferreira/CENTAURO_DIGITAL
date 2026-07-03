# settings permite referenciar AUTH_USER_MODEL sem acoplar o model a uma classe de usuario fixa.
from django.conf import settings
# models contem os tipos de campo e a classe base usada para criar tabelas no banco.
from django.db import models
# timezone fornece a data local configurada no Django, usada para comparar vencimentos.
from django.utils import timezone


class Separacao(models.Model):
    """Representa a tabela operacional de separacao no banco de dados."""

    # TextChoices cria uma lista fechada de valores para campos CharField.
    # O primeiro item e gravado no banco; o segundo e exibido para o usuario.
    class Tipo(models.TextChoices):
        NORMAL = "normal", "Normal"
        PRIORITARIA = "prioritaria", "Prioritaria"
        URGENTE = "urgente", "Urgente"

    # Status geral do registro de separacao.
    class Status(models.TextChoices):
        ABERTA = "aberta", "Aberta"
        EM_ANDAMENTO = "em_andamento", "Em andamento"
        CONCLUIDA = "concluida", "Concluida"
        CANCELADA = "cancelada", "Cancelada"

    # Status da etapa operacional, exibido e alterado diretamente na listagem.
    class StatusOperacional(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        EM_SEPARACAO = "em_separacao", "Em separacao"
        CONFERIDA = "conferida", "Conferida"
        FINALIZADA = "finalizada", "Finalizada"

    # Status documental indica se o documento esta valido, divergente ou bloqueado.
    class StatusDocumento(models.TextChoices):
        VALIDO = "valido", "Valido"
        DIVERGENTE = "divergente", "Divergente"
        BLOQUEADO = "bloqueado", "Bloqueado"

    # Status de autorizacao registra se alguma acao foi aprovada ou negada.
    class StatusAutorizacao(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        AUTORIZADO = "autorizado", "Autorizado"
        NEGADO = "negado", "Negado"

    # DateField guarda apenas data, sem hora. verbose_name e o rotulo usado no admin/forms.
    data = models.DateField(verbose_name="Data")
    # CharField guarda texto curto. max_length define o tamanho maximo no banco.
    romaneio = models.CharField(max_length=50, verbose_name="Romaneio")
    documento = models.CharField(max_length=80, verbose_name="Documento")
    grupo = models.CharField(max_length=80, verbose_name="Grupo")
    # PositiveIntegerField aceita apenas inteiros positivos, ideal para quantidades.
    quantidade = models.PositiveIntegerField(verbose_name="Quantidade")
    # null=True permite NULL no banco; blank=True permite deixar vazio em formularios.
    vencimento = models.DateField(verbose_name="Vencimento", null=True, blank=True)
    # choices limita os valores aceitos aos definidos em Tipo.
    tipo = models.CharField(
        max_length=20,
        choices=Tipo.choices,
        default=Tipo.NORMAL,
        verbose_name="Tipo",
    )
    # status representa o estado geral do registro; default define o valor inicial.
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ABERTA,
        verbose_name="Status",
    )
    # Quantidade ainda pendente dentro da separacao.
    quantidade_pendente = models.PositiveIntegerField(
        default=0,
        verbose_name="Quantidade pendente",
    )
    # Status operacional fica separado do status geral para acompanhar a execucao da separacao.
    status_operacional = models.CharField(
        max_length=30,
        choices=StatusOperacional.choices,
        default=StatusOperacional.PENDENTE,
        verbose_name="Status operacional",
    )
    # Status documental registra problemas ou validade do documento associado.
    status_documento = models.CharField(
        max_length=20,
        choices=StatusDocumento.choices,
        default=StatusDocumento.VALIDO,
        verbose_name="Status do documento",
    )
    # Quantidade conferida pode ser comparada com quantidade e quantidade_pendente.
    quantidade_conferida = models.PositiveIntegerField(
        default=0,
        verbose_name="Quantidade conferida",
    )
    # Status de autorizacao permite controlar aprovacoes futuras sem mudar o model.
    status_autorizacao = models.CharField(
        max_length=20,
        choices=StatusAutorizacao.choices,
        default=StatusAutorizacao.PENDENTE,
        verbose_name="Status da autorizacao",
    )
    # ForeignKey cria relacionamento muitos-para-um com o usuario atribuido.
    # SET_NULL preserva o registro se o usuario for removido.
    # related_name permite acessar usuario.separacoes_atribuidas.
    atribuido = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="separacoes_atribuidas",
        verbose_name="Atribuido",
    )
    # TextField guarda texto maior, como observacoes livres.
    anotacoes = models.TextField(blank=True, verbose_name="Anotacoes")
    # auto_now_add preenche a data/hora apenas na criacao do registro.
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    # auto_now atualiza a data/hora toda vez que o registro e salvo.
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        # ordering define a ordenacao padrao sempre que a query nao especificar outra.
        ordering = ["-data", "romaneio", "documento"]
        # verbose_name altera o nome singular mostrado no admin.
        verbose_name = "Separacao"
        # verbose_name_plural altera o nome plural mostrado no admin.
        verbose_name_plural = "Separacoes"
        # permissions cria permissoes customizadas usadas nas views e grupos do sistema.
        permissions = [
            ("access_separacao", "Pode acessar o modulo separacao"),
            ("create_record", "Pode criar registro"),
            ("edit_record", "Pode editar registro"),
            ("delete_record", "Pode excluir registro"),
        ]

    def __str__(self):
        # O Django usa __str__ no admin, selects e logs para representar o objeto como texto.
        return f"{self.documento} - {self.romaneio}"

    @property
    def motivo_alerta(self):
        """Resume pendencias operacionais para uso visual na tabela."""

        # Se existe vencimento e ele ja passou, o alerta principal e vencimento expirado.
        if self.vencimento and self.vencimento < timezone.localdate():
            return "Vencimento expirado"
        # Se ainda ha quantidade pendente, a listagem mostra esse motivo ao usuario.
        if self.quantidade_pendente > 0:
            return "Quantidade pendente"
        # Se o fluxo operacional nao finalizou, o alerta indica que ainda ha etapa aberta.
        if self.status_operacional != self.StatusOperacional.FINALIZADA:
            return "Operacao nao finalizada"
        return "Ver detalhes do registro"

    def get_absolute_url(self):
        # Import local evita carregar urls durante a importacao inicial dos models.
        from django.urls import reverse

        # get_absolute_url e usado por CreateView/UpdateView para saber para onde redirecionar.
        return reverse("separacao:detail", kwargs={"pk": self.pk})
