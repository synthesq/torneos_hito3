from django.contrib import admin
from .models import Juego, Torneo

@admin.register(Juego)
class JuegoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'genero', 'desarrollador', 'activo')
    list_filter = ('activo', 'genero')
    search_fields = ('nombre', 'desarrollador')

@admin.register(Torneo)
class TorneoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'juego', 'fecha_inicio', 'activo')
    list_filter = ('activo', 'juego')
    search_fields = ('nombre', 'descripcion')