from django.urls import path
from . import views
from .views import descargar_entidades_zip

urlpatterns = [
    path('', views.home, name='home'),  # Página principal
    path('buscar/', views.buscar_entidad, name='buscar_entidad'),
    path('buscar-indicadores/', views.buscar_indicadores, name='buscar_indicadores'),
    path('buscar-autoridades/', views.buscar_autoridades, name='buscar_autoridades'),
    path('buscar-documentos/', views.buscar_documentos, name='buscar_documentos'),
    path('descargar-documento/<str:cuit>/<str:archivo_id>/', views.descargar_documento, name='descargar_documento'),
    path('buscar-deudas/', views.buscar_deudas, name='buscar_deudas'),
    path('buscar-periodos/', views.buscar_periodos, name='buscar_periodos'),
    path("descargar/entidades/", descargar_entidades_zip, name="descargar_entidades"),
    path('descargar-indicadores-zip/', views.descargar_indicadores_zip, name='descargar_indicadores_zip'),
    path('descargar-autoridades-zip/', views.descargar_autoridades_zip, name='descargar_autoridades_zip'),
    path('descargar-empleo-zip/', views.descargar_empleo_zip, name='descargar_empleo_zip'),
]
