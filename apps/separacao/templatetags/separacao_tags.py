# template permite criar filtros/tags customizados para usar nos arquivos HTML.
from django import template

# register e o objeto onde registramos filtros deste modulo.
register = template.Library()


@register.filter
def dict_get(value, key):
    # Permite buscar value[key] dentro do template.
    # Uso: {{ tipo_badges|dict_get:separacao.tipo }}.
    return value.get(key, "")
