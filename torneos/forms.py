from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Torneo


class BootstrapMixin:
    """Aplica clases Bootstrap a los widgets y marca los campos con error."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = 'form-check-input'
            elif isinstance(widget, forms.Select):
                widget.attrs['class'] = 'form-select'
            else:
                widget.attrs['class'] = 'form-control'

    def full_clean(self):
        super().full_clean()
        for nombre in (self._errors or {}):
            if nombre in self.fields:
                widget = self.fields[nombre].widget
                widget.attrs['class'] = (widget.attrs.get('class', '') + ' is-invalid').strip()


class TorneoForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Torneo
        fields = ['juego', 'nombre', 'fecha_inicio', 'fecha_fin',
                  'premio', 'max_participantes', 'estado', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej: Copa Patagonia 2026'}),
            'fecha_inicio': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'premio': forms.NumberInput(attrs={'placeholder': '0', 'min': 0}),
            'max_participantes': forms.NumberInput(attrs={'placeholder': '16', 'min': 2}),
        }

    def clean_max_participantes(self):
        valor = self.cleaned_data['max_participantes']
        if valor < 2:
            raise forms.ValidationError('Un torneo necesita al menos 2 participantes.')
        return valor

    def clean(self):
        datos = super().clean()
        inicio = datos.get('fecha_inicio')
        fin = datos.get('fecha_fin')
        if inicio and fin and fin < inicio:
            self.add_error('fecha_fin', 'La fecha de término no puede ser anterior al inicio.')
        return datos


class LoginForm(BootstrapMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Usuario', 'autofocus': True})
        self.fields['password'].widget.attrs.update({'placeholder': 'Contraseña'})
