from django.test import TestCase
from datetime import datetime
from core.models import (
    CHOICES_PROBLEMAS, CHOICES_EQUIPES,
    CHOICES_CONDICAO, SubmissaoModel
    )


class SubmissaoModelTest(TestCase):
    def setUp(self):
        self.status = CHOICES_CONDICAO[0][0]
        self.equipe = CHOICES_EQUIPES[1][0]
        self.problema = CHOICES_PROBLEMAS[1][0]
        self.cadastro = SubmissaoModel(
            equipe=self.equipe,
            status=self.status,
            problema=self.problema,
            tempo=20,
        )
        self.cadastro.save()

    def test_created(self):
        self.assertTrue(SubmissaoModel.objects.exists())

    def test_modificado_em(self):
        self.assertIsInstance(self.cadastro.modificado_em, datetime)

    def test_problema(self):
        problema = self.cadastro.__dict__.get('problema', '')
        self.assertEqual(problema, self.problema)

    def test_status(self):
        status = self.cadastro.__dict__.get('status', '')
        self.assertEqual(status, self.status)

    def test_equipe(self):
        equipe = self.cadastro.__dict__.get('equipe', '')
        self.assertEqual(equipe, self.equipe)

    def test_tempo(self):
        tempo = self.cadastro.__dict__.get('tempo', '')
        self.assertEqual(tempo, 20)
