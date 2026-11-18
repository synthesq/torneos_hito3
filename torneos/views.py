from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView,
)

from .forms import JuegoForm, TorneoForm
from .models import Juego, Torneo


# ---------- Juego ----------
class JuegoListView(ListView):
    model = Juego
    template_name = 'torneos/juego_list.html'
    context_object_name = 'juegos'


class JuegoDetailView(DetailView):
    model = Juego
    template_name = 'torneos/juego_detail.html'


class JuegoCreateView(SuccessMessageMixin, CreateView):
    model = Juego
    form_class = JuegoForm
    template_name = 'torneos/form.html'
    success_url = reverse_lazy('torneos:juego_list')
    success_message = 'Juego creado correctamente.'


class JuegoUpdateView(SuccessMessageMixin, UpdateView):
    model = Juego
    form_class = JuegoForm
    template_name = 'torneos/form.html'
    success_url = reverse_lazy('torneos:juego_list')
    success_message = 'Juego actualizado correctamente.'


class JuegoDeleteView(DeleteView):
    model = Juego
    template_name = 'torneos/confirm_delete.html'
    success_url = reverse_lazy('torneos:juego_list')


# ---------- Torneo ----------
class TorneoListView(ListView):
    model = Torneo
    template_name = 'torneos/torneo_list.html'
    context_object_name = 'torneos'

    def get_queryset(self):
        return Torneo.objects.select_related('juego')


class TorneoDetailView(DetailView):
    model = Torneo
    template_name = 'torneos/torneo_detail.html'


class TorneoCreateView(SuccessMessageMixin, CreateView):
    model = Torneo
    form_class = TorneoForm
    template_name = 'torneos/form.html'
    success_url = reverse_lazy('torneos:torneo_list')
    success_message = 'Torneo creado correctamente.'


class TorneoUpdateView(SuccessMessageMixin, UpdateView):
    model = Torneo
    form_class = TorneoForm
    template_name = 'torneos/form.html'
    success_url = reverse_lazy('torneos:torneo_list')
    success_message = 'Torneo actualizado correctamente.'


class TorneoDeleteView(DeleteView):
    model = Torneo
    template_name = 'torneos/confirm_delete.html'
    success_url = reverse_lazy('torneos:torneo_list')