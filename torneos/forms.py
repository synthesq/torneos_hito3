from django import forms

from .models import Juego, Torneo


class BootstrapMixin:
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


class JuegoForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Juego
        fields = ['nombre', 'genero', 'desarrollador', 'fecha_lanzamiento', 'activo']
        widgets = {
            'fecha_lanzamiento': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }


class TorneoForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Torneo
        fields = ['juego', 'nombre', 'fecha_inicio', 'fecha_fin',
                  'premio', 'max_participantes', 'estado']
        widgets = {
            'fecha_inicio': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
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