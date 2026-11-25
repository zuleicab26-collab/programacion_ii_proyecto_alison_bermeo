from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from concesionaria.forms import MarcaForm
from concesionaria.models import Marca


def marca_list(request):
    marcas = Marca.objects.all()
    return render(request, 'concesionaria/marcas/lista.html', {'marcas': marcas})


def marca_detail(request, pk):
    marca = get_object_or_404(Marca, pk=pk)
    motos = marca.motos.all()
    return render(
        request,
        'concesionaria/marcas/detalle.html',
        {'marca': marca, 'motos': motos},
    )


@login_required
@permission_required('concesionaria.add_marca', raise_exception=True)
def marca_create(request):
    if request.method == 'POST':
        form = MarcaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Marca creada exitosamente.')
            return redirect('marca_list')
    else:
        form = MarcaForm()
    return render(request, 'concesionaria/marcas/formulario.html', {'form': form})


@login_required
@permission_required('concesionaria.change_marca', raise_exception=True)
def marca_update(request, pk):
    marca = get_object_or_404(Marca, pk=pk)
    if request.method == 'POST':
        form = MarcaForm(request.POST, instance=marca)
        if form.is_valid():
            form.save()
            messages.success(request, 'Marca actualizada exitosamente.')
            return redirect('marca_list')
    else:
        form = MarcaForm(instance=marca)
    return render(
        request,
        'concesionaria/marcas/formulario.html',
        {'form': form, 'marca': marca},
    )


@login_required
@permission_required('concesionaria.delete_marca', raise_exception=True)
def marca_delete(request, pk):
    marca = get_object_or_404(Marca, pk=pk)
    if request.method == 'POST':
        try:
            marca.delete()
        except ProtectedError:
            messages.error(
                request, 'No se puede eliminar: la marca tiene motos registradas.'
            )
            return redirect('marca_detail', pk=marca.pk)
        messages.success(request, 'Marca eliminada exitosamente.')
        return redirect('marca_list')
    return render(
        request, 'concesionaria/marcas/confirmar_eliminar.html', {'marca': marca}
    )