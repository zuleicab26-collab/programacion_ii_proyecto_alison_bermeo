from django import forms

from concesionaria.models import Moto


class MotoForm(forms.ModelForm):
    class Meta:
        model = Moto
        fields = ['marca', 'modelo', 'cilindrada', 'anio', 'precio', 'estado']