from django.urls import path

from concesionaria import views

urlpatterns = [
    path('marcas/', views.marca_list, name='marca_list'),
    path('marcas/<int:pk>/', views.marca_detail, name='marca_detail'),
]