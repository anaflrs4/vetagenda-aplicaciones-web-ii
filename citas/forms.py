from django import forms

from .models import Cita, Mascota, Propietario, Veterinario


class FormularioBase(forms.ModelForm):
    """Shared styling for the project's Bootstrap-compatible form fields."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} form-control".strip()


class PropietarioForm(FormularioBase):
    class Meta:
        model = Propietario
        fields = ["nombre_completo", "telefono", "email"]
        widgets = {
            "nombre_completo": forms.TextInput(
                attrs={"placeholder": "Ej. Ana López"}
            ),
            "telefono": forms.TextInput(
                attrs={"placeholder": "Ej. 555 123 4567"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "Ej. ana@correo.com"}
            ),
        }


class MascotaForm(FormularioBase):
    class Meta:
        model = Mascota
        fields = [
            "propietario",
            "nombre",
            "especie",
            "raza",
            "fecha_nacimiento",
            "peso_kg",
            "notas",
        ]
        widgets = {
            "fecha_nacimiento": forms.DateInput(attrs={"type": "date"}),
            "peso_kg": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "notas": forms.Textarea(attrs={"rows": 3}),
        }


class VeterinarioForm(FormularioBase):
    class Meta:
        model = Veterinario
        fields = ["nombre_completo", "especialidad", "telefono", "email", "activo"]
        widgets = {
            "email": forms.EmailInput(),
        }


class CitaForm(FormularioBase):
    class Meta:
        model = Cita
        fields = [
            "mascota",
            "veterinario",
            "fecha",
            "hora",
            "motivo",
            "estado",
            "observaciones",
        ]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "hora": forms.TimeInput(attrs={"type": "time"}),
            "motivo": forms.TextInput(
                attrs={"placeholder": "Ej. Revisión general"}
            ),
            "observaciones": forms.Textarea(attrs={"rows": 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        veterinario = cleaned_data.get("veterinario")
        fecha = cleaned_data.get("fecha")
        hora = cleaned_data.get("hora")

        if veterinario and fecha and hora:
            coincidencias = Cita.objects.filter(
                veterinario=veterinario,
                fecha=fecha,
                hora=hora,
            )
            if self.instance.pk:
                coincidencias = coincidencias.exclude(pk=self.instance.pk)
            if coincidencias.exists():
                raise forms.ValidationError(
                    "Ese veterinario ya tiene una cita registrada en ese horario."
                )
        return cleaned_data
