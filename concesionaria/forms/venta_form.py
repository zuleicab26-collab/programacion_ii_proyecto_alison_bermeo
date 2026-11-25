from django import forms

from concesionaria.models import Venta


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente', 'motos', 'fecha', 'forma_pago']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'motos': forms.CheckboxSelectMultiple(),
        }