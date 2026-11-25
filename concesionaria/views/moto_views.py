from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from concesionaria.forms import MotoForm
from concesionaria.models import Moto


def moto_list(request):
    motos = Moto.objects.select_related('marca')
    return render(request, 'concesionaria/motos/lista.html', {'motos': motos})


def moto_detail(request, pk):
    moto = get_object_or_404(Moto, pk=pk)
    ventas = moto.ventas.all()
    return render(
        request,
        'concesionaria/motos/detalle.html',
        {'moto': moto, 'ventas': ventas},
    )


@login_required
def moto_create(request):
    if request.method == 'POST':
        form = MotoForm(request.POST)
        if form.is_valid():
            moto = form.save(commit=False)
            moto.creado_por = request.user
            moto.save()
            messages.success(request, 'Moto creada exitosamente.')
            return redirect('moto_list')
    else:
        form = MotoForm()
    return render(request, 'concesionaria/motos/formulario.html', {'form': form})


@login_required
def moto_update(request, pk):
    moto = get_object_or_404(Moto, pk=pk)
    if request.method == 'POST':
        form = MotoForm(request.POST, instance=moto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Moto actualizada exitosamente.')
            return redirect('moto_list')
    else:
        form = MotoForm(instance=moto)
    return render(
        request,
        'concesionaria/motos/formulario.html',
        {'form': form, 'moto': moto},
    )


@login_required
def moto_delete(request, pk):
    moto = get_object_or_404(Moto, pk=pk)
    if request.method == 'POST':
        moto.delete()
        messages.success(request, 'Moto eliminada exitosamente.')
        return redirect('moto_list')
    return render(
        request, 'concesionaria/motos/confirmar_eliminar.html', {'moto': moto}
    )