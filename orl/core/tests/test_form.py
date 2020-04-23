from django.test import TestCase

from core.forms import SubmissaoForm, PreSubmissaoForm
from core.models import (
    CHOICES_PROBLEMAS, CHOICES_EQUIPES, CHOICES_CONDICAO
    )


class PreSubmissaoFormTest(TestCase):
    def test_form_has_fields(self):
        form = PreSubmissaoForm()
        expected = ['problema', 'equipe']
        self.assertSequenceEqual(expected, list(form.fields))

    def test_obrigatorio_problema(self):
        form = self.make_validated_form(problema='')
        self.assertFormErrorCode(form, 'problema', 'required')

    def test_obrigatorio_equipe(self):
        form = self.make_validated_form(equipe='')
        self.assertFormErrorCode(form, 'equipe', 'required')

    def assertFormErrorCode(self, form, field, code):
        errors = form.errors.as_data()
        errors_list = errors[field]
        exception = errors_list[0]
        self.assertEqual(code, exception.code)

    def assertFormErrorMessage(self, form, field, msg):
        errors = form.errors
        errors_list = errors[field]
        self.assertListEqual([msg], errors_list)

    def make_validated_form(self, **kwargs):
        parametro_equipe = CHOICES_EQUIPES[1][0]
        parametro_problema = CHOICES_PROBLEMAS[1][0]
        valid = dict(
            equipe=parametro_equipe,
            problema=parametro_problema,
        )
        data = dict(valid, **kwargs)
        form = PreSubmissaoForm(data)
        form.is_valid()
        return form


class SubmissaoFormTest(TestCase):
    def test_form_has_fields(self):
        form = SubmissaoForm()
        expected = ['problema', 'equipe', 'tempo', 'status']
        self.assertSequenceEqual(expected, list(form.fields))

    def test_obrigatorio_problema(self):
        form = self.make_validated_form(problema='')
        self.assertFormErrorCode(form, 'problema', 'required')

    def test_obrigatorio_equipe(self):
        form = self.make_validated_form(equipe='')
        self.assertFormErrorCode(form, 'equipe', 'required')

    def test_obrigatorio_tempo(self):
        form = self.make_validated_form(tempo='')
        self.assertFormErrorCode(form, 'tempo', 'required')

    def test_obrigatorio_status(self):
        form = self.make_validated_form(status='')
        self.assertFormErrorCode(form, 'status', 'required')

    def test_validar_tempo(self):
        form = self.make_validated_form(tempo='a')
        self.assertListEqual(['tempo'], list(form.errors))

    def test_validar_tempo_negativo(self):
        form = self.make_validated_form(tempo='-1')
        self.assertListEqual(['tempo'], list(form.errors))

    def test_validar_zerado(self):
        form = self.make_validated_form(tempo='0')
        self.assertListEqual(['tempo'], list(form.errors))

    def test_validar_tempo_acima_200(self):
        form = self.make_validated_form(tempo='201')
        self.assertListEqual(['tempo'], list(form.errors))

    def test_validar_tempo_200_minutos(self):
        form = self.make_validated_form(tempo='200')
        self.assertListEqual([], list(form.errors))

    def assertFormErrorCode(self, form, field, code):
        errors = form.errors.as_data()
        errors_list = errors[field]
        exception = errors_list[0]
        self.assertEqual(code, exception.code)

    def assertFormErrorMessage(self, form, field, msg):
        errors = form.errors
        errors_list = errors[field]
        self.assertListEqual([msg], errors_list)

    def make_validated_form(self, **kwargs):
        parametro_status = CHOICES_CONDICAO[0][0]
        parametro_equipe = CHOICES_EQUIPES[1][0]
        parametro_problema = CHOICES_PROBLEMAS[1][0]
        valid = dict(
            equipe=parametro_equipe,
            status=parametro_status,
            problema=parametro_problema,
            tempo=20,
        )
        data = dict(valid, **kwargs)
        form = SubmissaoForm(data)
        form.is_valid()
        return form
