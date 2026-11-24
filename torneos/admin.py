from django.contrib import admin
from .models import Juego, Torneo


@admin.register(Juego)
class JuegoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'genero', 'desarrollador', 'fecha_lanzamiento', 'activo')
    list_filter = ('genero', 'activo')
    search_fields = ('nombre', 'desarrollador')


@admin.register(Torneo)
class TorneoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'juego', 'estado', 'fecha_inicio', 'fecha_fin', 'premio', 'activo')
    list_filter = ('juego', 'estado', 'activo')
    search_fields = ('nombre', 'juego__nombre')
    list_select_related = ('juego',)