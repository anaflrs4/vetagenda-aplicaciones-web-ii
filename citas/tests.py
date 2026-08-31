from datetime import date, time, timedelta
from io import StringIO

from django.contrib.auth.models import Group
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

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
                "duracion_minutos": 30,
                "motivo": "Consulta repetida",
                "estado": Cita.Estado.SOLICITADA,
                "observaciones": "",
            }
        )
        self.assertFalse(otro_form.is_valid())
        self.assertIn("solapa", str(otro_form.errors))

    def test_el_formulario_rechaza_solapamiento_parcial(self):
        Cita.objects.create(
            mascota=self.mascota,
            veterinario=self.veterinario,
            fecha=date(2026, 9, 10),
            hora=time(10, 0),
            duracion_minutos=60,
            motivo="Consulta larga",
        )
        otro_form = CitaForm(
            data={
                "mascota": self.mascota.pk,
                "veterinario": self.veterinario.pk,
                "fecha": "2026-09-10",
                "hora": "10:30",
                "duracion_minutos": 30,
                "motivo": "Consulta solapada",
                "estado": Cita.Estado.SOLICITADA,
                "observaciones": "",
            }
        )
        self.assertFalse(otro_form.is_valid())
        self.assertIn("solapa", str(otro_form.errors))


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
                "duracion_minutos": 30,
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

    def test_la_agenda_hoy_solo_muestra_la_fecha_actual(self):
        hoy = timezone.localdate()
        Cita.objects.create(
            mascota=self.mascota,
            veterinario=self.veterinario,
            fecha=hoy,
            hora=time(8, 0),
            motivo="Cita de hoy",
        )
        otra_mascota = Mascota.objects.create(
            propietario=self.propietario,
            nombre="Nube",
            especie=Mascota.Especie.PERRO,
        )
        Cita.objects.create(
            mascota=otra_mascota,
            veterinario=self.veterinario,
            fecha=hoy + timedelta(days=1),
            hora=time(9, 0),
            motivo="Cita futura",
        )
        response = self.client.get(reverse("citas:agenda_hoy"))
        self.assertContains(response, "Cita de hoy")
        self.assertNotContains(response, "Cita futura")

    def test_configurar_roles_crea_grupos_y_permisos(self):
        call_command("configurar_roles", stdout=StringIO())
        propietario = Group.objects.get(name="Propietario")
        personal = Group.objects.get(name="Personal veterinario")
        administrador = Group.objects.get(name="Administrador")
        self.assertEqual(propietario.permissions.count(), 7)
        self.assertEqual(personal.permissions.count(), 5)
        self.assertEqual(administrador.permissions.count(), 16)

    def test_el_dashboard_muestra_el_resumen_por_estado(self):
        Cita.objects.create(
            mascota=self.mascota,
            veterinario=self.veterinario,
            fecha=date(2026, 9, 20),
            hora=time(14, 0),
            motivo="Consulta confirmada",
            estado=Cita.Estado.CONFIRMADA,
        )
        response = self.client.get(reverse("citas:inicio"))
        self.assertContains(response, "Solicitada")
        self.assertContains(response, "Confirmada")
        self.assertContains(response, "Atendida")
        self.assertContains(response, "Cancelada")

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
