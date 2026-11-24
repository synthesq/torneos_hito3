import csv

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, Q, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView,
)

from .forms import TorneoForm
from .models import Juego, Torneo

ORDENES = {
    'recientes': ('-fecha_inicio', 'Más recientes'),
    'antiguos': ('fecha_inicio', 'Más antiguos'),
    'premio': ('-premio', 'Mayor premio'),
    'cupos': ('-max_participantes', 'Más cupos'),
    'nombre': ('nombre', 'Nombre (A-Z)'),
}


class TorneoFiltroMixin:
    """Búsqueda, filtros y orden por querystring. Lo comparten la lista y la exportación."""

    def filtrar(self, qs):
        g = self.request.GET
        q = g.get('q', '').strip()
        if q:
            qs = qs.filter(Q(nombre__icontains=q) | Q(juego__nombre__icontains=q))
        if g.get('juego', '').isdigit():
            qs = qs.filter(juego_id=int(g['juego']))
        if g.get('estado') in Torneo.Estado.values:
            qs = qs.filter(estado=g['estado'])
        if g.get('activo') in ('1', '0'):
            qs = qs.filter(activo=g['activo'] == '1')
        orden = ORDENES.get(g.get('orden'), ORDENES['recientes'])[0]
        return qs.order_by(orden, 'id')


class TorneoListView(TorneoFiltroMixin, ListView):
    model = Torneo
    template_name = 'torneos/torneo_list.html'
    context_object_name = 'torneos'
    paginate_by = 9

    def get_queryset(self):
        # select_related evita el problema N+1: trae el juego en un solo JOIN.
        qs = Torneo.objects.select_related('juego')
        return self.filtrar(qs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        g = self.request.GET
        resumen = self.object_list.aggregate(
            total=Count('id'),
            activos=Count('id', filter=Q(activo=True)),
            premio_total=Sum('premio'),
            cupos_total=Sum('max_participantes'),
        )
        resumen['premio_total'] = resumen['premio_total'] or 0
        resumen['cupos_total'] = resumen['cupos_total'] or 0
        ctx['stats'] = resumen
        ctx['juegos'] = Juego.objects.all()
        ctx['estados'] = Torneo.Estado.choices
        ctx['ordenes'] = [(k, v[1]) for k, v in ORDENES.items()]
        ctx['f'] = {
            'q': g.get('q', '').strip(),
            'juego': g.get('juego', ''),
            'estado': g.get('estado', ''),
            'activo': g.get('activo', ''),
            'orden': g.get('orden', 'recientes'),
        }
        ctx['hay_filtros'] = any(ctx['f'][k] for k in ('q', 'juego', 'estado', 'activo')) or \
            ctx['f']['orden'] not in ('', 'recientes')
        paginator = ctx.get('paginator')
        if paginator and ctx['is_paginated']:
            ctx['paginas'] = [
                {'n': n, 'ell': n == paginator.ELLIPSIS}
                for n in paginator.get_elided_page_range(
                    ctx['page_obj'].number, on_each_side=1, on_ends=1)
            ]
        return ctx


class TorneoExportCSVView(LoginRequiredMixin, TorneoFiltroMixin, View):
    """Exporta a CSV (abre en Excel) lo que muestra la lista con sus filtros."""

    def get(self, request):
        qs = self.filtrar(Torneo.objects.select_related('juego'))
        respuesta = HttpResponse(content_type='text/csv; charset=utf-8')
        respuesta['Content-Disposition'] = 'attachment; filename="torneos.csv"'
        respuesta.write('\ufeff')  # BOM para que Excel lea bien los acentos
        w = csv.writer(respuesta, delimiter=';')
        w.writerow(['ID', 'Torneo', 'Juego', 'Inicio', 'Término', 'Premio CLP',
                    'Cupos', 'Estado', 'Activo'])
        for t in qs:
            w.writerow([t.pk, t.nombre, t.juego.nombre, t.fecha_inicio.isoformat(),
                        t.fecha_fin.isoformat(), t.premio, t.max_participantes,
                        t.get_estado_display(), 'Sí' if t.activo else 'No'])
        return respuesta


class TorneoDetailView(DetailView):
    queryset = Torneo.objects.select_related('juego')
    template_name = 'torneos/torneo_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['relacionados'] = (
            Torneo.objects.select_related('juego')
            .filter(juego=self.object.juego)
            .exclude(pk=self.object.pk)[:3]
        )
        return ctx


class TorneoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Torneo
    form_class = TorneoForm
    template_name = 'torneos/form.html'
    success_url = reverse_lazy('torneo_list')
    success_message = "Torneo creado correctamente."


class TorneoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Torneo
    form_class = TorneoForm
    template_name = 'torneos/form.html'
    success_url = reverse_lazy('torneo_list')
    success_message = "Torneo actualizado correctamente."


class TorneoDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Torneo
    template_name = 'torneos/confirm_delete.html'
    success_url = reverse_lazy('torneo_list')
    success_message = "Torneo eliminado correctamente."


class TorneoToggleActivoView(LoginRequiredMixin, View):
    """Activa o desactiva un torneo con un clic (solo POST)."""
    http_method_names = ['post']

    def post(self, request, pk):
        torneo = get_object_or_404(Torneo, pk=pk)
        torneo.activo = not torneo.activo
        torneo.save(update_fields=['activo'])
        messages.success(
            request,
            f'«{torneo.nombre}» ahora está {"activo" if torneo.activo else "inactivo"}.',
        )
        destino = request.POST.get('next', '')
        if not url_has_allowed_host_and_scheme(destino, allowed_hosts={request.get_host()}):
            destino = reverse_lazy('torneo_list')
        return redirect(destino)
