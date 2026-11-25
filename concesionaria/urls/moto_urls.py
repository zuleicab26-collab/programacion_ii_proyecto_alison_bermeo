from django.urls import path

from concesionaria import views

urlpatterns = [
    path('motos/', views.moto_list, name='moto_list'),
    path('motos/nueva/', views.moto_create, name='moto_create'),
    path('motos/<int:pk>/', views.moto_detail, name='moto_detail'),
    path('motos/<int:pk>/editar/', views.moto_update, name='moto_update'),
    path('motos/<int:pk>/eliminar/', views.moto_delete, name='moto_delete'),
]