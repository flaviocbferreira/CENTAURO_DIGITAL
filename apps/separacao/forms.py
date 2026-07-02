from django import forms
from django.contrib.auth import get_user_model

from .models import Separacao


class SeparacaoForm(forms.ModelForm):
    class Meta:
        model = Separacao
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
        widgets = {
            "data": forms.DateInput(attrs={"type": "date"}),
            "vencimento": forms.DateInput(attrs={"type": "date"}),
            "anotacoes": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["atribuido"].queryset = get_user_model().objects.order_by(
            "first_name",
            "username",
        )
        self.fields["atribuido"].empty_label = "Sem responsavel"

        base_class = (
            "w-full rounded border border-slate-300 bg-white px-3 py-2.5 text-sm "
            "text-slate-900 outline-none transition focus:border-brand-600 "
            "focus:ring-4 focus:ring-brand-50"
        )
        for field in self.fields.values():
            field.widget.attrs["class"] = base_class

    def clean(self):
        cleaned_data = super().clean()
        quantidade = cleaned_data.get("quantidade")
        quantidade_pendente = cleaned_data.get("quantidade_pendente")

        if (
            quantidade is not None
            and quantidade_pendente is not None
            and quantidade_pendente > quantidade
        ):
            self.add_error(
                "quantidade_pendente",
                "A quantidade pendente nao pode ser maior que a Qtd. Doc.",
            )

        return cleaned_data
