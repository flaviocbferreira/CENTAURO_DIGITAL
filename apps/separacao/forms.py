# forms contem ModelForm, que cria formularios HTML a partir de models.
from django import forms
# get_user_model evita acoplar o form ao model auth.User diretamente.
from django.contrib.auth import get_user_model

from .models import Separacao


class SeparacaoForm(forms.ModelForm):
    """Formulario usado para criar e editar registros de Separacao."""

    class Meta:
        # model informa qual tabela/model este formulario representa.
        model = Separacao
        # fields define exatamente quais campos aparecem no formulario.
        # Campos fora da lista nao sao editaveis por esta tela.
        fields = [
            "data",
            "romaneio",
            "documento",
            "grupo",
            "quantidade",
            "vencimento",
            "tipo",
            "status_operacional",
            "quantidade_pendente",
            "atribuido",
            "anotacoes",
        ]
        # labels trocam os nomes exibidos ao usuario sem mudar os nomes dos campos no model.
        labels = {
            "data": "Data",
            "romaneio": "Romaneio",
            "documento": "Documento",
            "grupo": "Grupo",
            "quantidade": "Qtd. Doc",
            "vencimento": "Vencimento",
            "tipo": "Status Tipo",
            "status_operacional": "Status OP",
            "quantidade_pendente": "QTDE PEN",
            "atribuido": "Atribuido",
            "anotacoes": "Anotacoes",
        }
        # widgets personalizam o input HTML gerado para campos especificos.
        widgets = {
            # type=date abre seletor de data nos navegadores modernos.
            "data": forms.DateInput(attrs={"type": "date"}),
            "vencimento": forms.DateInput(attrs={"type": "date"}),
            # Textarea com rows=2 deixa anotacoes compactas no layout.
            "anotacoes": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        # __init__ roda quando o formulario e criado pela view.
        super().__init__(*args, **kwargs)
        # O campo atribuido e uma ForeignKey para usuario; aqui ordenamos as opcoes no select.
        self.fields["atribuido"].queryset = get_user_model().objects.order_by(
            "first_name",
            "username",
        )
        # Texto exibido quando nenhum responsavel e escolhido.
        self.fields["atribuido"].empty_label = "Sem responsavel"

        # Classes Tailwind aplicadas a todos os campos para manter o visual consistente.
        base_class = (
            "w-full rounded border border-slate-300 bg-white px-3 py-2.5 text-sm "
            "text-slate-900 outline-none transition focus:border-brand-600 "
            "focus:ring-4 focus:ring-brand-50"
        )
        # Percorre todos os campos do form e injeta a classe no widget HTML.
        for field in self.fields.values():
            field.widget.attrs["class"] = base_class

    def clean(self):
        # clean permite validar regras que dependem de mais de um campo.
        cleaned_data = super().clean()
        quantidade = cleaned_data.get("quantidade")
        quantidade_pendente = cleaned_data.get("quantidade_pendente")

        # Regra de negocio: nao faz sentido a quantidade pendente ser maior que a quantidade total.
        if (
            quantidade is not None
            and quantidade_pendente is not None
            and quantidade_pendente > quantidade
        ):
            # add_error associa a mensagem ao campo especifico no formulario.
            self.add_error(
                "quantidade_pendente",
                "A quantidade pendente nao pode ser maior que a Qtd. Doc.",
            )

        # Retornar cleaned_data mantem o fluxo normal de validacao do Django.
        return cleaned_data
