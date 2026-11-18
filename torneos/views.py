from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Torneo
from .forms import TorneoForm

class TorneoListView(ListView):
    model = Torneo
    template_name = 'torneos/torneo_list.html'
    context_object_name = 'torneos'
    
    def get_queryset(self):
        return Torneo.objects.select_related('juego').all()

class TorneoDetailView(DetailView):
    model = Torneo
    template_name = 'torneos/torneo_detail.html'

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