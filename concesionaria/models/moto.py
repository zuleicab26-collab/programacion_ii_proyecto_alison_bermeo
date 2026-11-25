from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Moto(models.Model):
    class Estado(models.TextChoices):
        DISPONIBLE = 'DISP', 'Disponible'
        RESERVADA = 'RES', 'Reservada'
        VENDIDA = 'VEN', 'Vendida'

    marca = models.ForeignKey(
        'concesionaria.Marca', on_delete=models.PROTECT, related_name='motos'
    )
    modelo = models.CharField(max_length=80)
    cilindrada = models.PositiveIntegerField(help_text='En cc')
    anio = models.PositiveSmallIntegerField('año')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(
        max_length=4, choices=Estado.choices, default=Estado.DISPONIBLE
    )
    fecha_ingreso = models.DateField(auto_now_add=True)
    creado_por = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='motos_creadas'
    )

    class Meta:
        ordering = ['marca__nombre', 'modelo']
        verbose_name = 'moto'
        verbose_name_plural = 'motos'

    def __str__(self):
        return f'{self.marca} {self.modelo} ({self.anio})'

    def get_absolute_url(self):
        return reverse('moto_detail', args=[self.pk])