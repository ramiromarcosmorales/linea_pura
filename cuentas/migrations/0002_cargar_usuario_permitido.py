from django.db import migrations


def cargar_usuario_permitido(apps, schema_editor):
    UsuarioPermitido = apps.get_model('cuentas', 'UsuarioPermitido')
    UsuarioPermitido.objects.get_or_create(
        email='annavillegas@live.com.ar',
        defaults={
            'nombre': 'Anna Villegas',
            'codigo_validacion': 'LPA2024AV',
        }
    )
    UsuarioPermitido.objects.get_or_create(
        email='ramiro.marcos.ck@gmail.com',
        defaults={
            'nombre': 'Ramiro Marcos',
            'codigo_validacion': 'LPA2024RM',
        }
    )


def revertir(apps, schema_editor):
    UsuarioPermitido = apps.get_model('cuentas', 'UsuarioPermitido')
    UsuarioPermitido.objects.filter(email='annavillegas@live.com.ar').delete()
    UsuarioPermitido.objects.filter(email='ramiro.marcos.ck@gmail.com').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('cuentas', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(cargar_usuario_permitido, revertir),
    ]
