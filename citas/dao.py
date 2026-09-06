"""Capa de acceso a datos de VetAgenda.

Las vistas y los servicios del backend deben usar estas clases en lugar de
consultar directamente el ORM. La arquitectura queda:
View/API -> DAO -> ORM de Django -> base de datos.
"""

from django.core.exceptions import ValidationError
from django.db.models import Count, Q
from django.utils import timezone

from .models import Cita, Mascota, Propietario, Veterinario


class PropietarioDAO:
    @staticmethod
    def contar() -> int:
        return Propietario.objects.count()

    @staticmethod
    def listar(busqueda: str = ""):
        registros = Propietario.objects.prefetch_related("mascotas")
        if busqueda:
            registros = registros.filter(
                Q(nombre_completo__icontains=busqueda)
                | Q(telefono__icontains=busqueda)
                | Q(email__icontains=busqueda)
            )
        return registros

    @staticmethod
    def obtener_por_id(pk: int):
        return Propietario.objects.filter(pk=pk).first()

    @staticmethod
    def guardar(registro: Propietario) -> Propietario:
        registro.full_clean()
        registro.save()
        return registro

    @staticmethod
    def eliminar(registro: Propietario) -> None:
        registro.delete()


class MascotaDAO:
    @staticmethod
    def contar() -> int:
        return Mascota.objects.count()

    @staticmethod
    def listar(busqueda: str = ""):
        registros = Mascota.objects.select_related("propietario").annotate(
            total_citas=Count("citas")
        )
        if busqueda:
            registros = registros.filter(
                Q(nombre__icontains=busqueda)
                | Q(propietario__nombre_completo__icontains=busqueda)
                | Q(especie__icontains=busqueda)
            )
        return registros

    @staticmethod
    def obtener_por_id(pk: int):
        return Mascota.objects.select_related("propietario").filter(pk=pk).first()

    @staticmethod
    def guardar(registro: Mascota) -> Mascota:
        registro.full_clean()
        registro.save()
        return registro

    @staticmethod
    def eliminar(registro: Mascota) -> None:
        registro.delete()


class VeterinarioDAO:
    @staticmethod
    def contar_activos() -> int:
        return Veterinario.objects.filter(activo=True).count()

    @staticmethod
    def listar(busqueda: str = ""):
        registros = Veterinario.objects.annotate(total_citas=Count("citas"))
        if busqueda:
            registros = registros.filter(
                Q(nombre_completo__icontains=busqueda)
                | Q(especialidad__icontains=busqueda)
                | Q(email__icontains=busqueda)
            )
        return registros

    @staticmethod
    def listar_activos():
        return Veterinario.objects.filter(activo=True)

    @staticmethod
    def obtener_por_id(pk: int):
        return Veterinario.objects.filter(pk=pk).first()

    @staticmethod
    def guardar(registro: Veterinario) -> Veterinario:
        registro.full_clean()
        registro.save()
        return registro

    @staticmethod
    def eliminar(registro: Veterinario) -> None:
        registro.delete()


class CitaDAO:
    ESTADOS_ACTIVOS = (Cita.Estado.SOLICITADA, Cita.Estado.CONFIRMADA)
    TRANSICIONES = {
        Cita.Estado.SOLICITADA: {Cita.Estado.CONFIRMADA, Cita.Estado.CANCELADA},
        Cita.Estado.CONFIRMADA: {Cita.Estado.ATENDIDA, Cita.Estado.CANCELADA},
        Cita.Estado.ATENDIDA: set(),
        Cita.Estado.CANCELADA: set(),
    }

    @staticmethod
    def _con_relaciones():
        return Cita.objects.select_related(
            "mascota", "mascota__propietario", "veterinario"
        )

    @classmethod
    def contar(cls) -> int:
        return Cita.objects.count()

    @classmethod
    def listar(cls, busqueda: str = "", estado: str = ""):
        registros = cls._con_relaciones()
        if busqueda:
            registros = registros.filter(
                Q(mascota__nombre__icontains=busqueda)
                | Q(mascota__propietario__nombre_completo__icontains=busqueda)
                | Q(motivo__icontains=busqueda)
                | Q(veterinario__nombre_completo__icontains=busqueda)
            )
        if estado:
            registros = registros.filter(estado=estado)
        return registros

    @classmethod
    def listar_proximas(cls, limite: int = 5):
        return cls._con_relaciones().filter(
            fecha__gte=timezone.localdate()
        )[:limite]

    @classmethod
    def listar_activas(cls):
        return cls._con_relaciones().filter(estado__in=cls.ESTADOS_ACTIVOS)

    @staticmethod
    def fecha_actual():
        return timezone.localdate()

    @classmethod
    def listar_hoy(cls, veterinario_id: str = ""):
        registros = cls._con_relaciones().filter(fecha=cls.fecha_actual())
        if veterinario_id:
            registros = registros.filter(veterinario_id=veterinario_id)
        return registros

    @classmethod
    def obtener_por_id(cls, pk: int):
        return cls._con_relaciones().filter(pk=pk).first()

    @staticmethod
    def resumen_estados():
        return [
            {
                "valor": valor,
                "etiqueta": etiqueta,
                "total": Cita.objects.filter(estado=valor).count(),
            }
            for valor, etiqueta in Cita.Estado.choices
        ]

    @staticmethod
    def guardar(registro: Cita) -> Cita:
        registro.full_clean()
        registro.save()
        return registro

    @staticmethod
    def eliminar(registro: Cita) -> None:
        registro.delete()

    @classmethod
    def cambiar_estado(cls, pk: int, nuevo_estado: str) -> Cita:
        cita = cls.obtener_por_id(pk)
        if cita is None:
            raise Cita.DoesNotExist("La cita solicitada no existe.")

        estados_validos = {valor for valor, _ in Cita.Estado.choices}
        if nuevo_estado not in estados_validos:
            raise ValidationError("El estado solicitado no es válido.")
        if nuevo_estado not in cls.TRANSICIONES[cita.estado]:
            raise ValidationError(
                f"No se permite cambiar una cita de {cita.get_estado_display()} "
                f"a {dict(Cita.Estado.choices)[nuevo_estado]}."
            )

        cita.estado = nuevo_estado
        cita.full_clean()
        cita.save(update_fields=["estado", "actualizado_en"])
        return cita
