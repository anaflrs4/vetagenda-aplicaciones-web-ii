from django.test import TestCase
from django.urls import reverse


class InicioVetAgendaTests(TestCase):
    def test_la_pagina_inicial_responde(self):
        response = self.client.get(reverse("citas:inicio"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "VetAgenda")
        self.assertContains(response, "La problemática")
