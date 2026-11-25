from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.models import Group, User
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

from concesionaria.models import Marca, Cliente, Moto, Venta

MARCAS = [
    ('Yamaha', 'Japón'),
    ('Honda', 'Japón'),
    ('Suzuki', 'Japón'),
    ('KTM', 'Austria'),
    ('Ducati', 'Italia'),
]

CLIENTES = [
    ('Ana Pérez', '1712345678', 'ana@correo.com', '0991111111'),
    ('Luis Mora', '1723456789', 'luis@correo.com', '0992222222'),
    ('Carla Vera', '1734567890', 'carla@correo.com', '0993333333'),
    ('Diego Salas', '1745678901', '', '0994444444'),
    ('María Toro', '1756789012', 'maria@correo.com', ''),
]

# (marca, modelo, cilindrada, año, precio, estado)
MOTOS = [
    ('Yamaha', 'R3', 321, 2024, Decimal('6500.00'), 'VEN'),
    ('Yamaha', 'MT-07', 689, 2023, Decimal('8900.00'), 'VEN'),
    ('Honda', 'CB500F', 471, 2024, Decimal('7200.00'), 'VEN'),
    ('Honda', 'XR190L', 184, 2023, Decimal('3800.00'), 'VEN'),
    ('Suzuki', 'GSX-S750', 749, 2022, Decimal('9100.00'), 'VEN'),
    ('KTM', 'Duke 390', 373, 2024, Decimal('6900.00'), 'VEN'),
    ('Ducati', 'Monster', 937, 2024, Decimal('14500.00'), 'DISP'),
    ('Suzuki', 'V-Strom 250', 248, 2023, Decimal('5400.00'), 'RES'),
]

# (índice cliente, índices de motos, forma de pago, días atrás, quién la registra)
VENTAS = [
    (0, [0], 'CON', 40, 'vendedor'),
    (1, [1, 2], 'CRE', 30, 'vendedor'),
    (2, [3], 'TAR', 20, 'gerente'),
    (3, [4], 'CON', 10, 'gerente'),
    (4, [5], 'CRE', 3, 'vendedor'),
]

USUARIOS = [
    # (usuario, correo, contraseña, grupo)
    ('gerente', 'gerente@motos.com', 'Gerente12345', 'administradores'),
    ('vendedor', 'vendedor@motos.com', 'Vendedor12345', 'vendedores'),
]


class Command(BaseCommand):
    help = 'Carga grupos, usuarios y datos de prueba. Se puede ejecutar varias veces.'

    @transaction.atomic
    def handle(self, *args, **options):
        call_command('crear_grupos')

        # Superusuario
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@motos.com', 'Admin12345')

        # Un usuario por grupo
        usuarios = {'admin': User.objects.get(username='admin')}
        for nombre, correo, clave, grupo in USUARIOS:
            usuario, creado = User.objects.get_or_create(
                username=nombre, defaults={'email': correo}
            )
            if creado:
                usuario.set_password(clave)
                usuario.save()
            usuario.groups.add(Group.objects.get(name=grupo))
            usuarios[nombre] = usuario

        # Marcas y clientes
        marcas = {}
        for nombre, pais in MARCAS:
            marcas[nombre], _ = Marca.objects.get_or_create(
                nombre=nombre, defaults={'pais_origen': pais}
            )

        clientes = []
        for nombre, cedula, email, telefono in CLIENTES:
            cliente, _ = Cliente.objects.get_or_create(
                cedula=cedula,
                defaults={'nombre': nombre, 'email': email, 'telefono': telefono},
            )
            clientes.append(cliente)

        # Motos
        motos = []
        for marca, modelo, cc, anio, precio, estado in MOTOS:
            moto, _ = Moto.objects.get_or_create(
                marca=marcas[marca],
                modelo=modelo,
                anio=anio,
                defaults={
                    'cilindrada': cc,
                    'precio': precio,
                    'estado': estado,
                    'creado_por': usuarios['admin'],
                },
            )
            motos.append(moto)

        # Ventas (solo si todavía no hay ninguna, para no duplicarlas)
        if not Venta.objects.exists():
            for idx_cliente, idx_motos, pago, dias, quien in VENTAS:
                venta = Venta.objects.create(
                    cliente=clientes[idx_cliente],
                    fecha=date.today() - timedelta(days=dias),
                    forma_pago=pago,
                    total=0,
                    creado_por=usuarios[quien],
                )
                venta.motos.set([motos[i] for i in idx_motos])
                venta.total = sum(motos[i].precio for i in idx_motos)
                venta.save(update_fields=['total'])

        self.stdout.write(self.style.SUCCESS('Datos de prueba cargados.'))
        self.stdout.write(
            f'Marcas: {Marca.objects.count()} | Clientes: {Cliente.objects.count()} | '
            f'Motos: {Moto.objects.count()} | Ventas: {Venta.objects.count()}'
        )