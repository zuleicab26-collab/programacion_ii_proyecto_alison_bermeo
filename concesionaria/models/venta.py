from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Venta(models.Model):
    class FormaPago(models.TextChoices):
        CONTADO = 'CON', 'Contado'
        CREDITO = 'CRE', 'Crédito'
        TARJETA = 'TAR', 'Tarjeta'

    cliente = models.ForeignKey(
        'concesionaria.Cliente', on_delete=models.PROTECT, related_name='compras'
    )
    motos = models.ManyToManyField(
        'concesionaria.Moto', related_name='ventas'
    )
    fecha = models.DateField()
    forma_pago = models.CharField(
        max_length=3, choices=FormaPago.choices, default=FormaPago.CONTADO
    )
    total = models.DecimalField(max_digits=12, decimal_places=2)
    creado_por = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='ventas_creadas'
    )

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'venta'
        verbose_name_plural = 'ventas'

    def __str__(self):
        return f'Venta #{self.pk} - {self.cliente.nombre}'

    def get_absolute_url(self):
        return reverse('venta_detail', args=[self.pk])