from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from concesionaria.forms import RegistroForm


def registro(request):
    if request.user.is_authenticated:
        return redirect('moto_list')
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada. Ya puede iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'concesionaria/auth/registro.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('moto_list')
    next_url = request.POST.get('next') or request.GET.get('next', '')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, f'Bienvenido, {request.user.username}.')
            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = AuthenticationForm(request)
    return render(
        request,
        'concesionaria/auth/login.html',
        {'form': form, 'next': next_url},
    )


@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect(settings.LOGOUT_REDIRECT_URL)