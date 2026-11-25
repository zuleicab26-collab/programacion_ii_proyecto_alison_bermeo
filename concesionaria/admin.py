from django.contrib import admin

from concesionaria.models import Marca, Cliente, Moto, Venta


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'pais_origen']
    list_filter = ['pais_origen']
    search_fields = ['nombre', 'pais_origen']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'cedula', 'email', 'telefono']
    list_filter = ['compras__forma_pago']
    search_fields = ['nombre', 'cedula', 'email']


@admin.register(Moto)
class MotoAdmin(admin.ModelAdmin):
    list_display = ['marca', 'modelo', 'anio', 'precio', 'estado', 'creado_por']
    list_filter = ['estado', 'marca', 'anio']
    search_fields = ['modelo', 'marca__nombre']


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['pk', 'cliente', 'fecha', 'forma_pago', 'total', 'creado_por']
    list_filter = ['forma_pago', 'fecha']
    search_fields = ['cliente__nombre', 'cliente__cedula']
    filter_horizontal = ['motos']