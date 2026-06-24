from django.contrib import admin
from .models import Consulta


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'categoria', 'fecha']
    list_filter = ['categoria', 'fecha']
    search_fields = ['nombre', 'email', 'mensaje']
    readonly_fields = ['fecha', 'categoria']
    ordering = ['-fecha']
