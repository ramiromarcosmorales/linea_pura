import uuid

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from .forms import LoginForm, RegistroForm, ValidacionForm
from .models import UsuarioPermitido


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            try:
                permitido = UsuarioPermitido.objects.get(email__iexact=email)
            except UsuarioPermitido.DoesNotExist:
                permitido = None

            if permitido is None:
                messages.error(
                    request,
                    'Acceso restringido. No está autorizado a utilizar este sistema.',
                )
                return render(request, 'cuentas/registro.html', {'form': form})

            # Crear usuario inactivo
            user = form.save(commit=False)
            user.username = email   # username = email para login posterior
            user.email = email
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.is_active = False  # Inactivo hasta validar
            user.save()

            # Enviar email de validación
            link_validacion = request.build_absolute_uri('/cuentas/validar/')
            try:
                send_mail(
                    subject='Validación de cuenta — Línea Pura Arquitectura',
                    message=(
                        f'Hola {user.first_name},\n\n'
                        f'Tu código de validación es: {permitido.codigo_validacion}\n\n'
                        f'Para activar tu cuenta, ingresá a:\n{link_validacion}\n\n'
                        f'Usá tu correo electrónico y el código de validación para confirmar tu cuenta.\n\n'
                        f'Línea Pura Arquitectura'
                    ),
                    from_email=None,
                    recipient_list=[email],
                    fail_silently=True,
                )
            except Exception:
                pass

            messages.info(
                request,
                'Le llegará un correo para validar su cuenta.',
            )
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'cuentas/registro.html', {'form': form})


def validar_cuenta(request):
    if request.method == 'POST':
        form = ValidacionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            codigo = form.cleaned_data['codigo']

            try:
                permitido = UsuarioPermitido.objects.get(
                    email__iexact=email,
                    codigo_validacion=codigo,
                )
            except UsuarioPermitido.DoesNotExist:
                messages.error(request, 'El código ingresado no es válido.')
                return render(request, 'cuentas/validar.html', {'form': form})

            # Activar usuario
            try:
                user = User.objects.get(email__iexact=email)
                user.is_active = True
                user.save()
                messages.success(
                    request,
                    'Cuenta validada exitosamente. Ya podés iniciar sesión.',
                )
                return redirect('login')
            except User.DoesNotExist:
                messages.error(
                    request,
                    'No se encontró un usuario registrado con ese correo.',
                )
    else:
        form = ValidacionForm()
    return render(request, 'cuentas/validar.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('panel')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('panel')
    else:
        form = LoginForm(request)
    return render(request, 'cuentas/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
