from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from concesionaria.forms import ClienteForm
from concesionaria.models import Cliente


def cliente_list(request):
    clientes = Cliente.objects.all()
    return render(
        request, 'concesionaria/clientes/lista.html', {'clientes': clientes}
    )


def cliente_detail(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    compras = cliente.compras.all()
    return render(
        request,
        'concesionaria/clientes/detalle.html',
        {'cliente': cliente, 'compras': compras},
    )


@login_required
@permission_required('concesionaria.add_cliente', raise_exception=True)
def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado exitosamente.')
            return redirect('cliente_list')
    else:
        form = ClienteForm()
    return render(request, 'concesionaria/clientes/formulario.html', {'form': form})


@login_required
@permission_required('concesionaria.change_cliente', raise_exception=True)
def cliente_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado exitosamente.')
            return redirect('cliente_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(
        request,
        'concesionaria/clientes/formulario.html',
        {'form': form, 'cliente': cliente},
    )


@login_required
@permission_required('concesionaria.delete_cliente', raise_exception=True)
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        try:
            cliente.delete()
        except ProtectedError:
            messages.error(
                request, 'No se puede eliminar: el cliente tiene compras registradas.'
            )
            return redirect('cliente_detail', pk=cliente.pk)
        messages.success(request, 'Cliente eliminado exitosamente.')
        return redirect('cliente_list')
    return render(
        request,
        'concesionaria/clientes/confirmar_eliminar.html',
        {'cliente': cliente},
    )