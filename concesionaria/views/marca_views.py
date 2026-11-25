from django.shortcuts import get_object_or_404, render

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