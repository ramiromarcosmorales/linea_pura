from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('validar/', views.validar_cuenta, name='validar'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
