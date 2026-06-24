from django.db import models


CATEGORIAS = [
    ('Consulta Comercial', 'Consulta Comercial'),
    ('Consulta Técnica', 'Consulta Técnica'),
    ('Consulta de RRHH', 'Consulta de RRHH'),
    ('Consulta General', 'Consulta General'),
]

PALABRAS_CLAVE = {
    'Consulta Comercial': ['precio', 'costo', 'tarifa', 'compra'],
    'Consulta Técnica': ['soporte', 'error', 'problema', 'ayuda'],
    'Consulta de RRHH': ['trabajo', 'cv', 'empleo', 'linkedin'],
}


def clasificar_mensaje(mensaje):
    """Clasifica un mensaje según sus palabras clave."""
    texto = mensaje.lower()
    for categoria, palabras in PALABRAS_CLAVE.items():
        if any(p in texto for p in palabras):
            return categoria
    return 'Consulta General'


class Consulta(models.Model):
    nombre = models.CharField('Nombre', max_length=120)
    email = models.EmailField('Email')
    mensaje = models.TextField('Mensaje')
    categoria = models.CharField(
        'Categoría',
        max_length=30,
        choices=CATEGORIAS,
        blank=True,
    )
    fecha = models.DateTimeField('Fecha', auto_now_add=True)

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'

    def save(self, *args, **kwargs):
        # Calcular categoría automáticamente al guardar
        if not self.categoria:
            self.categoria = clasificar_mensaje(self.mensaje)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nombre} — {self.categoria} ({self.fecha:%d/%m/%Y})'
