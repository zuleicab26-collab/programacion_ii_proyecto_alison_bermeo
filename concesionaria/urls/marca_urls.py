from django.urls import path

from concesionaria import views

urlpatterns = [
    path('marcas/', views.marca_list, name='marca_list'),
    path('marcas/nueva/', views.marca_create, name='marca_create'),
    path('marcas/<int:pk>/', views.marca_detail, name='marca_detail'),
    path('marcas/<int:pk>/editar/', views.marca_update, name='marca_update'),
    path('marcas/<int:pk>/eliminar/', views.marca_delete, name='marca_delete'),
]