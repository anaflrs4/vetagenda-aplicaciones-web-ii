from django.core.validators import MinValueValidator
from django.db import models


class Propietario(models.Model):
    """Person responsible for one or more pets."""

    nombre_completo = models.CharField("nombre completo", max_length=120)
    telefono = models.CharField("teléfono", max_length=25)
    email = models.EmailField("correo electrónico", blank=True)
    fecha_registro = models.DateTimeField("fecha de registro", auto_now_add=True)

    class Meta:
        ordering = ["nombre_completo"]
        verbose_name = "propietario"
        verbose_name_plural = "propietarios"

    def __str__(self) -> str:
        return self.nombre_completo


class Mascota(models.Model):
    """Pet registered by a proprietor."""

    class Especie(models.TextChoices):
        PERRO = "perro", "Perro"
        GATO = "gato", "Gato"
        AVE = "ave", "Ave"
        ROEDOR = "roedor", "Roedor"
        OTRO = "otro", "Otro"

    propietario = models.ForeignKey(
        Propietario,
        on_delete=models.CASCADE,
        related_name="mascotas",
        verbose_name="propietario",
    )
    nombre = models.CharField("nombre", max_length=80)
    especie = models.CharField("especie", max_length=20, choices=Especie.choices)
    raza = models.CharField("raza", max_length=80, blank=True)
    fecha_nacimiento = models.DateField("fecha de nacimiento", blank=True, null=True)
    peso_kg = models.DecimalField(
        "peso en kg",
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    notas = models.TextField("notas", blank=True)
    fecha_registro = models.DateTimeField("fecha de registro", auto_now_add=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "mascota"
        verbose_name_plural = "mascotas"

    def __str__(self) -> str:
        return f"{self.nombre} ({self.propietario.nombre_completo})"


class Veterinario(models.Model):
    """Veterinary professional available for appointments."""

    nombre_completo = models.CharField("nombre completo", max_length=120)
    especialidad = models.CharField("especialidad", max_length=100, blank=True)
    telefono = models.CharField("teléfono", max_length=25, blank=True)
    email = models.EmailField("correo electrónico", blank=True)
    activo = models.BooleanField("activo", default=True)

    class Meta:
        ordering = ["nombre_completo"]
        verbose_name = "veterinario"
        verbose_name_plural = "veterinarios"

    def __str__(self) -> str:
        return self.nombre_completo


class Cita(models.Model):
    """Appointment between a pet and a veterinary professional."""

    class Estado(models.TextChoices):
        SOLICITADA = "solicitada", "Solicitada"
        CONFIRMADA = "confirmada", "Confirmada"
        ATENDIDA = "atendida", "Atendida"
        CANCELADA = "cancelada", "Cancelada"

    mascota = models.ForeignKey(
        Mascota,
        on_delete=models.CASCADE,
        related_name="citas",
        verbose_name="mascota",
    )
    veterinario = models.ForeignKey(
        Veterinario,
        on_delete=models.PROTECT,
        related_name="citas",
        verbose_name="veterinario",
    )
    fecha = models.DateField("fecha")
    hora = models.TimeField("hora")
    motivo = models.CharField("motivo de consulta", max_length=180)
    estado = models.CharField(
        "estado",
        max_length=20,
        choices=Estado.choices,
        default=Estado.SOLICITADA,
    )
    observaciones = models.TextField("observaciones", blank=True)
    creado_en = models.DateTimeField("creado en", auto_now_add=True)
    actualizado_en = models.DateTimeField("actualizado en", auto_now=True)

    class Meta:
        ordering = ["fecha", "hora"]
        constraints = [
            models.UniqueConstraint(
                fields=["veterinario", "fecha", "hora"],
                name="cita_unica_por_veterinario_horario",
            )
        ]
        verbose_name = "cita"
        verbose_name_plural = "citas"

    @property
    def propietario(self) -> Propietario:
        return self.mascota.propietario

    def __str__(self) -> str:
        return f"{self.fecha} {self.hora:%H:%M} · {self.mascota.nombre}"
