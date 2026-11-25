from decimal import Decimal

from django.core.management import call_command
from django.test import TestCase

from concesionaria.models import Venta


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
