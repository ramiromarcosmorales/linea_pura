# Segundo Parcial - Programación Web II

**Alumno:** Ramiro Marcos Morales  
**Matrícula:** 149386  
**Carrera:** Tecnicatura en Programación de Sistemas  
**Materia:** Programación Web II  
**Docente:** Analía Villegas  

---

## Enlaces del Proyecto
* **Despliegue en Render:** https://linea-pura.onrender.com

---

## Estructura del Sitio y Requisitos

### Páginas
* **Home (`/`)**: Página principal.
* **Proyectos (`/proyectos/`)**: Galería de trabajos del estudio.
* **Nosotros (`/nosotros/`)**: Información sobre el estudio.
* **Contacto (`/contacto/`)**: Formulario con validaciones en JS, clasificación por palabras clave y almacenamiento en BD.

---

### Detalles Técnicos
* **Formularios:** Django Forms (`studio/forms.py`) con validaciones JS en `static/studio/js/contacto.js`.
* **Clasificación de Mensajes:** Modelo `Consulta` (`studio/models.py`) que clasifica automáticamente el mensaje en base a palabras clave (Comercial, Técnica, RRHH o General).
* **Autenticación restringida:** Registro (`/cuentas/registro/`) limitado a la tabla `UsuarioPermitido`. Envío de código de validación, confirmación en `/cuentas/validar/` y posterior inicio de sesión.
* **Panel de Administración:** Ruta protegida en `/panel/` con métricas (cantidad total y por categoría) y listado de consultas para visualizar, editar y eliminar.
* **Consumo de API Externa:** Open-Meteo API (`https://api.open-meteo.com/v1/forecast`) consultada desde el backend.
* **API REST Propia:** Endpoint `/api/consultas/` desarrollado con Django REST Framework para consultar registros en JSON.
* **SMTP Ferozo:** Envío de correos por puerto 465 SSL. Cuenta con backend personalizado en `linea_pura/email_backend.py` para ignorar la verificación estricta de SSL auto-firmado de Ferozo y `EMAIL_TIMEOUT = 5` en `settings.py` para evitar cuelgues en Render.

---

## Instalación y Ejecución Local

1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Ejecutar migraciones (crea tablas y carga usuarios autorizados):
   ```bash
   python manage.py migrate
   ```

3. Iniciar el servidor local:
   ```bash
   python manage.py runserver
   ```

---

## Cuentas y Códigos de Prueba Mock

Cuentas precargadas en la tabla `UsuarioPermitido` para validación:

| Correo Autorizado | Código de Validación |
|---------------------------|----------------------|
| `annavillegas@live.com.ar` | `LPA2024AV` |
| `ramiro.marcos.ck@gmail.com` | `LPA2024RM` |
