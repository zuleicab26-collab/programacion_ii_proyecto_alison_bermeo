from decimal import Decimal

from django.core.management import call_command
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from concesionaria.models import Venta


class ClienteURLTests(SimpleTestCase):
    def test_cliente_crud_urls_can_be_reversed(self):
        self.assertEqual(reverse('cliente_create'), '/clientes/nueva/')
        self.assertEqual(reverse('cliente_update', args=[1]), '/clientes/1/editar/')
        self.assertEqual(reverse('cliente_delete', args=[1]), '/clientes/1/eliminar/')


class CargarDatosCommandTests(TestCase):
    def test_creates_sales_with_decimal_totals(self):
        call_command('cargar_datos')

        totals = list(Venta.objects.order_by('pk').values_list('total', flat=True))

        self.assertEqual(
            totals,
            [
                Decimal('6500.00'),
                Decimal('16100.00'),
                Decimal('3800.00'),
                Decimal('9100.00'),
                Decimal('6900.00'),
            ],
        )
