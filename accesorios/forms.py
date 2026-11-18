
from django import forms
from .models import Accesorio


class AccesorioForm(forms.ModelForm):

    class Meta:
        model = Accesorio

        fields = [
            "nombre",
            "descripcion",
            "precio_dia",
            "stock",
        ]

        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre del accesorio"
                }
            ),

            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Descripción del accesorio"
                }
            ),

            "precio_dia": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Precio por día",
                    "min": "0",
                    "step": "0.01"
                }
            ),

            "stock": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Cantidad disponible",
                    "min": "0"
                }
            ),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"]
        return nombre.strip().title()

    def clean_precio_dia(self):
        precio = self.cleaned_data["precio_dia"]

        if precio <= 0:
            raise forms.ValidationError(
                "El precio diario debe ser mayor que cero."
            )

        return precio
