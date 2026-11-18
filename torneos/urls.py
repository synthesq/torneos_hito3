from django.urls import path

from . import views

app_name = 'torneos'

urlpatterns = [
    # Juegos
    path('', views.JuegoListView.as_view(), name='juego_list'),
    path('juegos/nuevo/', views.JuegoCreateView.as_view(), name='juego_create'),
    path('juegos/<int:pk>/', views.JuegoDetailView.as_view(), name='juego_detail'),
    path('juegos/<int:pk>/editar/', views.JuegoUpdateView.as_view(), name='juego_update'),
    path('juegos/<int:pk>/eliminar/', views.JuegoDeleteView.as_view(), name='juego_delete'),
    # Torneos
    path('torneos/', views.TorneoListView.as_view(), name='torneo_list'),
    path('torneos/nuevo/', views.TorneoCreateView.as_view(), name='torneo_create'),
    path('torneos/<int:pk>/', views.TorneoDetailView.as_view(), name='torneo_detail'),
    path('torneos/<int:pk>/editar/', views.TorneoUpdateView.as_view(), name='torneo_update'),
    path('torneos/<int:pk>/eliminar/', views.TorneoDeleteView.as_view(), name='torneo_delete'),
]