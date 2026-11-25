from concesionaria.views.marca_views import marca_list, marca_detail
from concesionaria.views.cliente_views import cliente_list, cliente_detail
from concesionaria.views.moto_views import (
    moto_list, moto_detail, moto_create, moto_update, moto_delete,
)
from concesionaria.views.venta_views import (
    venta_list, venta_detail, venta_create, venta_update, venta_delete,
)
from concesionaria.views.auth_views import registro, login_view, logout_view