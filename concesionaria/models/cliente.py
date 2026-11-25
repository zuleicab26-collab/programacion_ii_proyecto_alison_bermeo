from django.db import models
from django.urls import reverse


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=10, unique=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=15, blank=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'

    def __str__(self):
        return f'{self.nombre} ({self.cedula})'

    def get_absolute_url(self):
        return reverse('cliente_detail', args=[self.pk])