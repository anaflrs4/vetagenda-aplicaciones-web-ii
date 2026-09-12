from datetime import date, time, timedelta
from io import StringIO
from unittest.mock import patch

from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .dao import CitaDAO, MascotaDAO, PropietarioDAO, VeterinarioDAO
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

    def test_formulario_cita_muestra_nombres_y_guia(self):
        response = self.client.get(reverse("citas:cita_nueva"))
        self.assertContains(response, "Los nombres se seleccionan de registros existentes")
        self.assertContains(response, "Luna")
        self.assertContains(response, "Dra. Sofía Torres")
        self.assertContains(response, "Registrar propietario")
        self.assertContains(response, "Registrar mascota")
        self.assertContains(response, "Registrar veterinario")


class FormularioCitaVacioTests(TestCase):
    def test_formulario_advierte_cuando_faltan_registros(self):
        response = self.client.get(reverse("citas:cita_nueva"))
        self.assertContains(response, "Aún faltan datos para completar la cita")
        self.assertContains(response, "propietario")
        self.assertContains(response, "mascota")
        self.assertContains(response, "veterinario")


class CapaDAOTests(VetAgendaDatosMixin, TestCase):
    def setUp(self):
        self.crear_datos_base()

    def crear_cita(self, **cambios):
        datos = {
            "mascota": self.mascota,
            "veterinario": self.veterinario,
            "fecha": timezone.localdate(),
            "hora": time(10, 0),
            "motivo": "Consulta DAO",
            "estado": Cita.Estado.SOLICITADA,
        }
        datos.update(cambios)
        return Cita.objects.create(**datos)

    def test_propietario_dao_realiza_crud(self):
        registro = PropietarioDAO.guardar(
            Propietario(
                nombre_completo="Carlos Ruiz",
                telefono="5550001111",
                email="carlos@example.com",
            )
        )
        self.assertIsNotNone(registro.pk)
        registro.telefono = "5550002222"
        PropietarioDAO.guardar(registro)
        self.assertEqual(
            PropietarioDAO.obtener_por_id(registro.pk).telefono,
            "5550002222",
        )
        PropietarioDAO.eliminar(registro)
        self.assertIsNone(PropietarioDAO.obtener_por_id(registro.pk))

    def test_daos_listan_relaciones_y_filtros(self):
        self.crear_cita(motivo="Vacunación DAO")
        self.assertEqual(MascotaDAO.listar("Ana López").count(), 1)
        self.assertEqual(VeterinarioDAO.listar("Sofía").count(), 1)
        self.assertEqual(CitaDAO.listar("Vacunación").count(), 1)
        self.assertEqual(CitaDAO.listar(estado=Cita.Estado.SOLICITADA).count(), 1)

    def test_cita_dao_cambia_estado_valido(self):
        cita = self.crear_cita()
        actualizada = CitaDAO.cambiar_estado(cita.pk, Cita.Estado.CONFIRMADA)
        self.assertEqual(actualizada.estado, Cita.Estado.CONFIRMADA)
        cita.refresh_from_db()
        self.assertEqual(cita.estado, Cita.Estado.CONFIRMADA)

    def test_cita_dao_rechaza_transicion_invalida(self):
        cita = self.crear_cita(estado=Cita.Estado.ATENDIDA)
        with self.assertRaises(ValidationError):
            CitaDAO.cambiar_estado(cita.pk, Cita.Estado.CONFIRMADA)

    def test_endpoint_retorna_solo_citas_activas_en_json(self):
        activa = self.crear_cita()
        self.crear_cita(
            fecha=timezone.localdate() + timedelta(days=1),
            estado=Cita.Estado.CANCELADA,
        )
        response = self.client.get(reverse("citas:api_citas_activas"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["id"], activa.pk)
        self.assertEqual(len(response.json()), 1)

    @patch("citas.views.CitaDAO.listar")
    def test_vista_de_citas_delega_la_consulta_al_dao(self, listar_mock):
        listar_mock.return_value = []
        response = self.client.get(
            reverse("citas:citas"),
            {"q": "Luna", "estado": Cita.Estado.SOLICITADA},
        )
        self.assertEqual(response.status_code, 200)
        listar_mock.assert_called_once_with("Luna", Cita.Estado.SOLICITADA)

    @patch("citas.views.CitaDAO.cambiar_estado")
    def test_vista_de_estado_delega_la_actualizacion_al_dao(self, cambiar_mock):
        cita = self.crear_cita()
        cita.estado = Cita.Estado.CONFIRMADA
        cambiar_mock.return_value = cita
        response = self.client.post(
            reverse("citas:cita_cambiar_estado", args=[cita.pk]),
            {"estado": Cita.Estado.CONFIRMADA, "regreso": "citas:agenda_hoy"},
        )
        self.assertRedirects(response, reverse("citas:agenda_hoy"))
        cambiar_mock.assert_called_once_with(cita.pk, Cita.Estado.CONFIRMADA)


class FlujoExtremoAExtremoTests(TestCase):
    """Prueba el recorrido completo del usuario desde las vistas hasta la API."""

    def test_crud_y_estado_de_cita_de_extremo_a_extremo(self):
        respuesta = self.client.post(
            reverse("citas:propietario_nuevo"),
            {
                "nombre_completo": "Laura Méndez",
                "telefono": "5558881122",
                "email": "laura@example.com",
            },
        )
        self.assertRedirects(respuesta, reverse("citas:propietarios"))
        propietario = Propietario.objects.get(email="laura@example.com")

        respuesta = self.client.post(
            reverse("citas:mascota_nueva"),
            {
                "propietario": propietario.pk,
                "nombre": "Milo",
                "especie": Mascota.Especie.PERRO,
                "raza": "Mestizo",
                "fecha_nacimiento": "2022-04-10",
                "peso_kg": "12.40",
                "notas": "Paciente de prueba E2E.",
            },
        )
        self.assertRedirects(respuesta, reverse("citas:mascotas"))
        mascota = Mascota.objects.get(nombre="Milo")

        veterinario = Veterinario.objects.create(
            nombre_completo="Dr. Luis Romero",
            especialidad="Medicina preventiva",
            activo=True,
        )
        fecha = timezone.localdate() + timedelta(days=2)
        respuesta = self.client.post(
            reverse("citas:cita_nueva"),
            {
                "mascota": mascota.pk,
                "veterinario": veterinario.pk,
                "fecha": fecha.isoformat(),
                "hora": "12:00",
                "duracion_minutos": 30,
                "motivo": "Flujo E2E",
                "estado": Cita.Estado.SOLICITADA,
                "observaciones": "Registro de prueba integral.",
            },
        )
        self.assertRedirects(respuesta, reverse("citas:citas"))
        cita = Cita.objects.get(motivo="Flujo E2E")

        respuesta = self.client.post(
            reverse("citas:cita_cambiar_estado", args=[cita.pk]),
            {"estado": Cita.Estado.CONFIRMADA, "regreso": "citas:citas"},
        )
        self.assertRedirects(respuesta, reverse("citas:citas"))
        cita.refresh_from_db()
        self.assertEqual(cita.estado, Cita.Estado.CONFIRMADA)

        respuesta_api = self.client.get(reverse("citas:api_citas_activas"))
        self.assertEqual(respuesta_api.status_code, 200)
        self.assertEqual(respuesta_api.json()[0]["mascota_nombre"], "Milo")

        respuesta = self.client.post(
            reverse("citas:cita_cambiar_estado", args=[cita.pk]),
            {"estado": Cita.Estado.ATENDIDA, "regreso": "citas:citas"},
        )
        self.assertRedirects(respuesta, reverse("citas:citas"))
        cita.refresh_from_db()
        self.assertEqual(cita.estado, Cita.Estado.ATENDIDA)
        self.assertEqual(self.client.get(reverse("citas:api_citas_activas")).json(), [])
