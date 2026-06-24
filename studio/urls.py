# urls de la app nomas, el include esta en linea_pura/urls
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('proyectos/', views.proyectos, name='proyectos'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('contacto/', views.contacto, name='contacto'),
    # Panel de administración
    path('panel/', views.panel, name='panel'),
    path('panel/eliminar/<int:pk>/', views.panel_eliminar, name='panel_eliminar'),
    path('panel/editar/<int:pk>/', views.panel_editar, name='panel_editar'),
    # API
    path('api/consultas/', views.ConsultaListAPIView.as_view(), name='api_consultas'),
]