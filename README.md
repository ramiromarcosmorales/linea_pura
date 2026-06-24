# Línea Pura Arquitectura

Sitio web del estudio de arquitectura Línea Pura, desarrollado con Django.

## Páginas

- `/` — Home
- `/proyectos/` — Proyectos
- `/nosotros/` — Nosotros
- `/contacto/` — Contacto (formulario con validación JS y almacenamiento en BD)
- `/panel/` — Panel de administración (requiere autenticación)

## Autenticación

- `/cuentas/registro/` — Registro (acceso restringido a usuarios permitidos)
- `/cuentas/validar/` — Validación de cuenta por código
- `/cuentas/login/` — Inicio de sesión
- `/cuentas/logout/` — Cierre de sesión

## API

### API Propia (DRF)
- **`GET /api/consultas/`** — Devuelve en JSON todas las consultas recibidas desde el formulario de contacto.

### API Externa consumida
- **Open-Meteo** — `https://api.open-meteo.com/v1/forecast`
  - Muestra el clima actual en Buenos Aires (temperatura y viento) en la página principal.
  - Gratuita, sin API key requerida.
  - Documentación: https://open-meteo.com/en/docs

## Configuración

### Base de datos (PostgreSQL)

Editar `linea_pura/settings.py` con los datos de conexión:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'linea_pura_db',
        'USER': 'postgres',       # Tu usuario de PostgreSQL
        'PASSWORD': '',           # Tu contraseña
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Crear la base de datos:
```bash
createdb linea_pura_db
```

### Email SMTP

Editar `linea_pura/settings.py` con las credenciales asignadas:

```python
EMAIL_HOST_USER = 'tu_correo@dominio.com'
EMAIL_HOST_PASSWORD = 'tu_contraseña'
```

### Instalación

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Clasificación de consultas

Las consultas del formulario se clasifican automáticamente:

| Categoría         | Palabras clave                        |
|-------------------|---------------------------------------|
| Consulta Comercial | precio, costo, tarifa, compra        |
| Consulta Técnica   | soporte, error, problema, ayuda      |
| Consulta de RRHH   | trabajo, CV, empleo, linkedin        |
| Consulta General   | (sin palabras clave específicas)     |
