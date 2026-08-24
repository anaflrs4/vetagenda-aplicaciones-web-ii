from datetime import date, time

from django.core.management.base import BaseCommand

from citas.models import Cita, Mascota, Propietario, Veterinario


class Command(BaseCommand):
    help = "Carga registros ficticios para revisar el flujo inicial de VetAgenda."

    def handle(self, *args, **options):
        propietario_ana, _ = Propietario.objects.get_or_create(
            email="ana.demo@vetagenda.local",
            defaults={
                "nombre_completo": "Ana López",
                "telefono": "555 100 2000",
            },
        )
        propietario_mario, _ = Propietario.objects.get_or_create(
            email="mario.demo@vetagenda.local",
            defaults={
                "nombre_completo": "Mario Hernández",
                "telefono": "555 300 4000",
            },
        )
        luna, _ = Mascota.objects.get_or_create(
            propietario=propietario_ana,
            nombre="Luna",
            defaults={
                "especie": Mascota.Especie.GATO,
                "raza": "Europeo",
                "peso_kg": 4.2,
            },
        )
        max, _ = Mascota.objects.get_or_create(
            propietario=propietario_mario,
            nombre="Max",
            defaults={
                "especie": Mascota.Especie.PERRO,
                "raza": "Mestizo",
                "peso_kg": 12.8,
            },
        )
        dra_sofia, _ = Veterinario.objects.get_or_create(
            email="sofia.demo@vetagenda.local",
            defaults={
                "nombre_completo": "Dra. Sofía Torres",
                "especialidad": "Medicina general",
                "telefono": "555 500 6000",
                "activo": True,
            },
        )
        dr_diego, _ = Veterinario.objects.get_or_create(
            email="diego.demo@vetagenda.local",
            defaults={
                "nombre_completo": "Dr. Diego Ramírez",
                "especialidad": "Medicina preventiva",
                "telefono": "555 700 8000",
                "activo": True,
            },
        )
        Cita.objects.get_or_create(
            mascota=luna,
            veterinario=dra_sofia,
            fecha=date(2026, 9, 10),
            hora=time(10, 30),
            defaults={
                "motivo": "Revisión general",
                "estado": Cita.Estado.CONFIRMADA,
                "observaciones": "Revisar alimentación y peso.",
            },
        )
        Cita.objects.get_or_create(
            mascota=max,
            veterinario=dr_diego,
            fecha=date(2026, 9, 11),
            hora=time(12, 0),
            defaults={
                "motivo": "Vacunación anual",
                "estado": Cita.Estado.SOLICITADA,
                "observaciones": "Confirmar esquema de vacunación.",
            },
        )
        self.stdout.write(self.style.SUCCESS("Datos ficticios de VetAgenda cargados correctamente."))
