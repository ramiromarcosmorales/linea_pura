from django.contrib import admin
from .models import UsuarioPermitido


@admin.register(UsuarioPermitido)
class UsuarioPermitidoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'codigo_validacion']
    search_fields = ['nombre', 'email']
