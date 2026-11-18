
from django import forms
from django.forms import inlineformset_factory

from .models import Alquiler, AlquilerAccesorio


class AlquilerForm(forms.ModelForm):

    class Meta:
        model = Alquiler

        fields = [
            "cliente",
            "vehiculo",
            "fecha_inicio",
            "fecha_fin",
            "estado",
        ]

        widgets = {
            "fecha_inicio": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "fecha_fin": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "cliente": forms.Select(
                attrs={"class": "form-select"}
            ),
            "vehiculo": forms.Select(
                attrs={"class": "form-select"}
            ),
            "estado": forms.Select(
                attrs={"class": "form-select"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        fecha_inicio = cleaned_data.get("fecha_inicio")
        fecha_fin = cleaned_data.get("fecha_fin")

        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            raise forms.ValidationError(
                "La fecha final no puede ser anterior a la fecha inicial."
            )

        return cleaned_data


AccesoriosFormSet = inlineformset_factory(
    Alquiler,
    AlquilerAccesorio,
    fields=("accesorio", "cantidad"),
    extra=1,
    can_delete=True,
    widgets={
        "accesorio": forms.Select(
            attrs={"class": "form-select"}
        ),
        "cantidad": forms.NumberInput(
            attrs={
                "class": "form-control",
                "min": 1,
            }
        ),
    },
)
