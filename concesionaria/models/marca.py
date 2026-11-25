from django.db import models
from django.urls import reverse


class Marca(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    pais_origen = models.CharField(max_length=60)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'marca'
        verbose_name_plural = 'marcas'

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('marca_detail', args=[self.pk])