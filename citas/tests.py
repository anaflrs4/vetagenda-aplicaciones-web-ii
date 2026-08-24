from datetime import date, time

from django.test import TestCase
from django.urls import reverse

from .forms import CitaForm
from .models import Cita, Mascota, Propietario, Veterinario


class VetAgendaDatosMixin:
    def crear_datos_base(self):
        self.propietario = Propietario.objects.create(
            nombre_completo="Ana López",
            telefono="5551234567",
            email="ana@example.com",
        )
        self.mascota = Mascota.objects.create(
            propietario=self.propietario,
            nombre="Luna",
            especie=Mascota.Especie.GATO,
            raza="Europeo",
        )
        self.veterinario = Veterinario.objects.create(
            nombre_completo="Dra. Sofía Torres",
            especialidad="Medicina general",
            activo=True,
        )


class InicioVetAgendaTests(TestCase):
    def test_la_pagina_inicial_responde(self):
        response = self.client.get(reverse("citas:inicio"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "VetAgenda")
        self.assertContains(response, "La problemática")
        self.assertContains(response, "Propietarios registrados")


class ModelosVetAgendaTests(VetAgendaDatosMixin, TestCase):
    def setUp(self):
        self.crear_datos_base()

    def test_la_cita_se_relaciona_con_mascota_y_veterinario(self):
        cita = Cita.objects.create(
            mascota=self.mascota,
            veterinario=self.veterinario,
            fecha=date(2026, 9, 10),
            hora=time(10, 30),
            motivo="Revisión general",
        )
        self.assertEqual(cita.propietario, self.propietario)
        self.assertEqual(str(cita), "2026-09-10 10:30 · Luna")

    def test_el_formulario_rechaza_horario_duplicado(self):
        Cita.objects.create(
            mascota=self.mascota,
            veterinario=self.veterinario,
            fecha=date(2026, 9, 10),
            hora=time(10, 30),
            motivo="Primera consulta",
        )
        otro_form = CitaForm(
            data={
                "mascota": self.mascota.pk,
                "veterinario": self.veterinario.pk,
                "fecha": "2026-09-10",
                "hora": "10:30",
                "motivo": "Consulta repetida",
                "estado": Cita.Estado.SOLICITADA,
                "observaciones": "",
            }
        )
        self.assertFalse(otro_form.is_valid())
        self.assertIn("ya tiene una cita", str(otro_form.errors))


class FlujoVetAgendaTests(VetAgendaDatosMixin, TestCase):
    def setUp(self):
        self.crear_datos_base()

    def test_se_puede_registrar_una_cita_desde_la_vista(self):
        response = self.client.post(
            reverse("citas:cita_nueva"),
            {
                "mascota": self.mascota.pk,
                "veterinario": self.veterinario.pk,
                "fecha": "2026-09-12",
                "hora": "11:00",
                "motivo": "Vacunación",
                "estado": Cita.Estado.CONFIRMADA,
                "observaciones": "Aplicar vacuna anual.",
            },
        )
        self.assertRedirects(response, reverse("citas:citas"))
        self.assertEqual(Cita.objects.count(), 1)
        self.assertContains(self.client.get(reverse("citas:citas")), "Vacunación")

    def test_el_listado_filtra_por_estado(self):
        Cita.objects.create(
            mascota=self.mascota,
            veterinario=self.veterinario,
            fecha=date(2026, 9, 15),
            hora=time(9, 0),
            motivo="Control",
            estado=Cita.Estado.ATENDIDA,
        )
        response = self.client.get(
            reverse("citas:citas"), {"estado": Cita.Estado.ATENDIDA}
        )
        self.assertContains(response, "Control")
        self.assertContains(response, "Atendida")

    def test_el_listado_de_mascotas_muestra_propietario(self):
        response = self.client.get(reverse("citas:mascotas"))
        self.assertContains(response, "Luna")
        self.assertContains(response, "Ana López")

    def test_las_secciones_principales_cargan(self):
        rutas = [
            "citas:inicio",
            "citas:propietarios",
            "citas:mascotas",
            "citas:veterinarios",
            "citas:citas",
            "citas:cita_nueva",
        ]
        for ruta in rutas:
            with self.subTest(ruta=ruta):
                self.assertEqual(self.client.get(reverse(ruta)).status_code, 200)
