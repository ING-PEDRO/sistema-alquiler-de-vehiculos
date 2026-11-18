
from django import forms
from .models import Vehiculo


class VehiculoForm(forms.ModelForm):

    class Meta:
        model = Vehiculo

        fields = [
            "categoria",
            "placa",
            "marca",
            "modelo",
            "anio",
            "estado",
            "imagen",
        ]

        widgets = {
            "categoria": forms.Select(
                attrs={"class": "form-select"}
            ),
            "placa": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej. ABC123"
                }
            ),
            "marca": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "modelo": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "anio": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1900
                }
            ),
            "estado": forms.Select(
                attrs={"class": "form-select"}
            ),
            "imagen": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*"
                }
            ),
        }

    def clean_placa(self):
        placa = self.cleaned_data["placa"]
        return placa.upper().strip()

from .models import Categoria


class CategoriaForm(forms.ModelForm):

    class Meta:
        model = Categoria

        fields = [
            "nombre",
            "descripcion",
            "tarifa_diaria",
        ]

        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej. Automóvil económico"
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Describe las características de esta categoría"
                }
            ),
            "tarifa_diaria": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Tarifa diaria",
                    "min": "1",
                    "step": "0.01"
                }
            ),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"]
        return nombre.strip().title()

    def clean_tarifa_diaria(self):
        tarifa = self.cleaned_data["tarifa_diaria"]

        if tarifa <= 0:
            raise forms.ValidationError(
                "La tarifa diaria debe ser mayor que cero."
            )

        return tarifa
