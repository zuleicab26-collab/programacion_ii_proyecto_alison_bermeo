from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from concesionaria.forms import VentaForm
from concesionaria.models import Venta


def _recalcular_total(venta):
    total = venta.motos.aggregate(suma=Sum('precio'))['suma'] or 0
    venta.total = total
    venta.save(update_fields=['total'])


def venta_list(request):
    ventas = Venta.objects.select_related('cliente')
    return render(request, 'concesionaria/ventas/lista.html', {'ventas': ventas})


def venta_detail(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    motos = venta.motos.select_related('marca')
    return render(
        request,
        'concesionaria/ventas/detalle.html',
        {'venta': venta, 'motos': motos},
    )


@login_required
def venta_create(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            venta.creado_por = request.user
            venta.total = 0
            venta.save()
            form.save_m2m()
            _recalcular_total(venta)
            messages.success(request, 'Venta creada exitosamente.')
            return redirect('venta_list')
    else:
        form = VentaForm()
    return render(request, 'concesionaria/ventas/formulario.html', {'form': form})


@login_required
def venta_update(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        if form.is_valid():
            venta = form.save()
            _recalcular_total(venta)
            messages.success(request, 'Venta actualizada exitosamente.')
            return redirect('venta_list')
    else:
        form = VentaForm(instance=venta)
    return render(
        request,
        'concesionaria/ventas/formulario.html',
        {'form': form, 'venta': venta},
    )


@login_required
def venta_delete(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        venta.delete()
        messages.success(request, 'Venta eliminada exitosamente.')
        return redirect('venta_list')
    return render(
        request, 'concesionaria/ventas/confirmar_eliminar.html', {'venta': venta}
    )