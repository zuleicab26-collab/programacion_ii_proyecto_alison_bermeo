from django.shortcuts import get_object_or_404, render

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