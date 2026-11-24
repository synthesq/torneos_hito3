from django import template

register = template.Library()


@register.filter
def clp(valor):
    """Formatea un entero con punto como separador de miles: 1500000 -> 1.500.000"""
    try:
        return f'{int(valor):,}'.replace(',', '.')
    except (TypeError, ValueError):
        return valor
