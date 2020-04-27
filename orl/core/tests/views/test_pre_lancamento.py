from django.shortcuts import resolve_url as r
from django.test import Client, TestCase

from core.forms import SubmissaoForm, PreSubmissaoForm
from core.models import (
    CHOICES_PROBLEMAS, CHOICES_EQUIPES
)

view_in_test = 'core:pre_lancamento'
template_in_test = 'pre_lancamento.html'
template_in_ok_case = 'lancamento.html'
template_in_fail_case = 'pre_lancamento.html'


class PreLancamentoGet(TestCase):
    def setUp(self):
        self.client = Client()
        self.resp = self.client.get(r(view_in_test))

    def test_template(self):
        self.assertTemplateUsed(self.resp, template_in_test)

    def test_200_template(self):
        self.assertEqual(200, self.resp.status_code)

    def test_csrf(self):
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_html_template(self):
        tags = (
            ('Olimpíada de Raciocínio Lógico', 1),
            ('Lançamento', 1),
            ('<form', 2),
            ('</form>', 2),
            ('<input', 2),
            ('<select', 2),
            ('type="submit"', 2),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)


class PreLancamentoPostOK(TestCase):
    def setUp(self):
        self.data = dict(
            problema=CHOICES_PROBLEMAS[0][0],
            equipe=CHOICES_EQUIPES[0][0],
        )
        self.resp = self.client.post(r(view_in_test), self.data)

    def test_template(self):
        self.assertTemplateUsed(self.resp, template_in_ok_case)

    def test_200_template(self):
        self.assertEqual(200, self.resp.status_code)

    def test_csrf(self):
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubmissaoForm)

    def test_html_template(self):
        tags = (
            ('Olimpíada de Raciocínio Lógico', 1),
            ('Lançamento', 2),
            ('<form', 3),
            ('</form>', 3),
            ('<input', 4),
            ('<select', 3),
            ('type="submit"', 3),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)


class PreLancamentoPostFail(TestCase):
    def setUp(self):
        self.data = dict(
            problema=CHOICES_PROBLEMAS[0][0],
        )
        self.resp = self.client.post(r(view_in_test), self.data)

    def test_template(self):
        self.assertTemplateUsed(self.resp, template_in_fail_case)

    def test_200_template(self):
        self.assertEqual(200, self.resp.status_code)

    def test_csrf(self):
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, PreSubmissaoForm)

    def test_html_template(self):
        tags = (
            ('Olimpíada de Raciocínio Lógico', 1),
            ('Lançamento', 1),
            ('<form', 2),
            ('</form>', 2),
            ('<input', 2),
            ('<select', 2),
            ('type="submit"', 2),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)
