from django.db import models


class UsuarioPermitido(models.Model):
    nombre = models.CharField('Nombre', max_length=100)
    email = models.EmailField('Email', unique=True)
    codigo_validacion = models.CharField('Código de validación', max_length=50)

    class Meta:
        verbose_name = 'Usuario Permitido'
        verbose_name_plural = 'Usuarios Permitidos'

    def __str__(self):
        return f'{self.nombre} ({self.email})'
