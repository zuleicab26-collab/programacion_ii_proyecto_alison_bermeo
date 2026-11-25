from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

MODELOS = ['marca', 'cliente', 'moto', 'venta']

GRUPOS = {
    'administradores': [
        f'{accion}_{modelo}'
        for accion in ('add', 'change', 'delete', 'view')
        for modelo in MODELOS
    ],
    'vendedores': (
        [f'view_{modelo}' for modelo in MODELOS]
        + ['add_cliente', 'add_venta', 'change_venta', 'delete_venta']
    ),
}

class Command(BaseCommand):
    help = 'Crea los grupos administradores y vendedores con sus permisos.'

    def handle(self, *args, **options):
        for nombre, codenames in GRUPOS.items():
            grupo, creado = Group.objects.get_or_create(name=nombre)
            permisos = Permission.objects.filter(
                content_type__app_label='concesionaria',
                codename__in=codenames,
            )
            if permisos.count() != len(codenames):
                self.stdout.write(self.style.WARNING(
                    f'{nombre}: faltan permisos. ¿Corrió migrate?'
                ))
            grupo.permissions.set(permisos)
            estado = 'creado' if creado else 'actualizado'
            self.stdout.write(self.style.SUCCESS(
                f'Grupo {nombre} {estado} con {permisos.count()} permisos.'
            ))