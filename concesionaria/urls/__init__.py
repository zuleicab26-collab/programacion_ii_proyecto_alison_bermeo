from concesionaria.urls.marca_urls import urlpatterns as marca_urls
from concesionaria.urls.cliente_urls import urlpatterns as cliente_urls
from concesionaria.urls.moto_urls import urlpatterns as moto_urls
from concesionaria.urls.venta_urls import urlpatterns as venta_urls
from concesionaria.urls.auth_urls import urlpatterns as auth_urls

urlpatterns = marca_urls + cliente_urls + moto_urls + venta_urls + auth_urls