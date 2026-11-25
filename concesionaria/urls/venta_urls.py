from django.urls import path

from concesionaria import views

urlpatterns = [
    path('ventas/', views.venta_list, name='venta_list'),
    path('ventas/nueva/', views.venta_create, name='venta_create'),
    path('ventas/<int:pk>/', views.venta_detail, name='venta_detail'),
    path('ventas/<int:pk>/editar/', views.venta_update, name='venta_update'),
    path('ventas/<int:pk>/eliminar/', views.venta_delete, name='venta_delete'),
]