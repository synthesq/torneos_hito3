from django.contrib import admin
from .models import Juego, Torneo


@admin.register(Juego)
class JuegoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'genero', 'desarrollador', 'activo')
    search_fields = ('nombre',)


@admin.register(Torneo)
class TorneoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'juego', 'fecha_inicio', 'estado')
    list_filter = ('estado', 'juego')