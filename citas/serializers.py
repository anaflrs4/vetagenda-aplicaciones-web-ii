from rest_framework import serializers

from .models import Cita


class CitaSerializer(serializers.ModelSerializer):
    mascota_nombre = serializers.CharField(source="mascota.nombre", read_only=True)
    propietario_nombre = serializers.CharField(
        source="mascota.propietario.nombre_completo", read_only=True
    )
    veterinario_nombre = serializers.CharField(
        source="veterinario.nombre_completo", read_only=True
    )
    estado_etiqueta = serializers.CharField(source="get_estado_display", read_only=True)
    hora_fin = serializers.TimeField(read_only=True, format="%H:%M")

    class Meta:
        model = Cita
        fields = (
            "id",
            "mascota",
            "mascota_nombre",
            "propietario_nombre",
            "veterinario",
            "veterinario_nombre",
            "fecha",
            "hora",
            "hora_fin",
            "duracion_minutos",
            "motivo",
            "estado",
            "estado_etiqueta",
            "observaciones",
        )
