from django.contrib import admin

from .models import Cita, Mascota, Propietario, Veterinario


@admin.register(Propietario)
class PropietarioAdmin(admin.ModelAdmin):
    list_display = ("nombre_completo", "telefono", "email", "fecha_registro")
    search_fields = ("nombre_completo", "telefono", "email")


@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "especie", "raza", "propietario", "fecha_registro")
    list_filter = ("especie",)
    search_fields = ("nombre", "raza", "propietario__nombre_completo")


@admin.register(Veterinario)
class VeterinarioAdmin(admin.ModelAdmin):
    list_display = ("nombre_completo", "especialidad", "activo", "email")
    list_filter = ("activo", "especialidad")
    search_fields = ("nombre_completo", "especialidad", "email")


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ("fecha", "hora", "mascota", "veterinario", "estado")
    list_filter = ("estado", "fecha", "veterinario")
    search_fields = (
        "mascota__nombre",
        "mascota__propietario__nombre_completo",
        "veterinario__nombre_completo",
        "motivo",
    )
    date_hierarchy = "fecha"
