import requests as http_requests

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render

from rest_framework import generics

from .forms import ContactoForm
from .models import Consulta, CATEGORIAS
from .serializers import ConsultaSerializer


# ─── Páginas públicas ─────────────────────────────────────────────────────────

def home(request):
    """Página principal con datos del clima de Buenos Aires desde Open-Meteo."""
    clima = None
    try:
        url = (
            'https://api.open-meteo.com/v1/forecast'
            '?latitude=-34.6037&longitude=-58.3816'
            '&current=temperature_2m,wind_speed_10m,weather_code'
            '&timezone=America%2FArgentina%2FBuenos_Aires'
        )
        resp = http_requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            current = data.get('current', {})
            clima = {
                'temperatura': current.get('temperature_2m'),
                'viento': current.get('wind_speed_10m'),
                'code': current.get('weather_code'),
            }
    except Exception:
        # Si falla la API, la sección simplemente no aparece
        clima = None

    return render(request, 'studio/home.html', {'clima': clima})


def proyectos(request):
    return render(request, 'studio/proyectos.html')


def nosotros(request):
    return render(request, 'studio/nosotros.html')


def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            consulta = form.save()  # categoria se asigna en el save() del modelo

            # Enviar email de confirmación al cliente (propietario del sitio)
            try:
                send_mail(
                    subject=f'[{consulta.categoria}] Nueva consulta de {consulta.nombre}',
                    message=(
                        f'Se recibió una nueva consulta desde el formulario web.\n\n'
                        f'Nombre: {consulta.nombre}\n'
                        f'Email: {consulta.email}\n'
                        f'Categoría: {consulta.categoria}\n'
                        f'Fecha: {consulta.fecha:%d/%m/%Y %H:%M}\n\n'
                        f'Mensaje:\n{consulta.mensaje}'
                    ),
                    from_email=None,   # usa default_from_email de settings
                    recipient_list=['annavillegas@live.com.ar'],
                    fail_silently=True,
                )
            except Exception:
                pass  # no interrumpe el flujo si falla el mail

            messages.success(
                request,
                'Gracias por tu consulta. Te responderemos a la brevedad.',
            )
            return redirect('contacto')
    else:
        form = ContactoForm()
    return render(request, 'studio/contacto.html', {'form': form})


# ─── Panel de administración ──────────────────────────────────────────────────

@login_required
def panel(request):
    """Panel para que el cliente visualice, edite y elimine consultas."""
    consultas = Consulta.objects.all()

    # Resumen estadístico
    total = consultas.count()
    por_categoria = {cat[0]: consultas.filter(categoria=cat[0]).count() for cat in CATEGORIAS}

    return render(request, 'studio/panel.html', {
        'consultas': consultas,
        'total': total,
        'por_categoria': por_categoria,
    })


@login_required
def panel_eliminar(request, pk):
    """Elimina una consulta."""
    consulta = get_object_or_404(Consulta, pk=pk)
    if request.method == 'POST':
        consulta.delete()
        messages.success(request, 'Consulta eliminada correctamente.')
    return redirect('panel')


@login_required
def panel_editar(request, pk):
    """Edita una consulta."""
    consulta = get_object_or_404(Consulta, pk=pk)
    if request.method == 'POST':
        form = ContactoForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Consulta actualizada correctamente.')
            return redirect('panel')
    else:
        form = ContactoForm(instance=consulta)
    return render(request, 'studio/panel_editar.html', {'form': form, 'consulta': consulta})


# ─── API ──────────────────────────────────────────────────────────────────────

class ConsultaListAPIView(generics.ListAPIView):
    """GET /api/consultas/ — Devuelve todas las consultas en formato JSON."""
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer