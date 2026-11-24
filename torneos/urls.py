from django.urls import path

from . import views

urlpatterns = [
    path('', views.TorneoListView.as_view(), name='torneo_list'),
    path('torneo/exportar/', views.TorneoExportCSVView.as_view(), name='torneo_export'),
    path('torneo/nuevo/', views.TorneoCreateView.as_view(), name='torneo_create'),
    path('torneo/<int:pk>/', views.TorneoDetailView.as_view(), name='torneo_detail'),
    path('torneo/<int:pk>/editar/', views.TorneoUpdateView.as_view(), name='torneo_update'),
    path('torneo/<int:pk>/eliminar/', views.TorneoDeleteView.as_view(), name='torneo_delete'),
    path('torneo/<int:pk>/activo/', views.TorneoToggleActivoView.as_view(), name='torneo_toggle'),
]
