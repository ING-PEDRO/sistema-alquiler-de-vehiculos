
from django import forms
from .models import Cliente


class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = [
            "tipo_documento",
            "numero_documento",
            "nombres",
            "apellidos",
            "telefono",
            "correo",
        ]

        widgets = {
            "tipo_documento": forms.Select(
                choices=[
                    ("CC", "Cédula de ciudadanía"),
                    ("CE", "Cédula de extranjería"),
                    ("TI", "Tarjeta de identidad"),
                    ("Pasaporte", "Pasaporte"),
                ],
                attrs={"class": "form-select"}
            ),
            "numero_documento": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Número de documento"
                }
            ),
            "nombres": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombres del cliente"
                }
            ),
            "apellidos": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Apellidos del cliente"
                }
            ),
            "telefono": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Número de teléfono"
                }
            ),
            "correo": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Correo electrónico"
                }
            ),
        }

    def clean_numero_documento(self):
        documento = self.cleaned_data["numero_documento"]
        return documento.strip()

    def clean_nombres(self):
        return self.cleaned_data["nombres"].strip().title()

    def clean_apellidos(self):
        return self.cleaned_data["apellidos"].strip().title()
