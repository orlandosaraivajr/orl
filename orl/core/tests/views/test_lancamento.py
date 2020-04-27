from django.shortcuts import resolve_url as r
from django.test import Client, TestCase

from core.forms import SubmissaoForm
from core.models import (
    CHOICES_PROBLEMAS, CHOICES_EQUIPES,
    CHOICES_CONDICAO, SubmissaoModel
)

view_in_test = 'core:lancamento'
template_get_case = 'index.html'
template_post_in_ok_case = 'pre_lancamento.html'
template_post_in_fail_case = 'lancamento.html'


class LancamentoGet(TestCase):
    def setUp(self):
        self.client = Client()
        self.resp = self.client.get(r(view_in_test))

    def test_template(self):
        self.assertTemplateUsed(self.resp, template_get_case)

    def test_200_template(self):
        self.assertEqual(200, self.resp.status_code)

    def test_csrf(self):
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_html_template(self):
        tags = (
            ('Olimpíada', 1),
            ('FHO', 1),
            ('<form', 3),
            ('</form>', 3),
            ('type="submit"', 3),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)


class LancamentoPostOK(TestCase):
    def setUp(self):
        self.data = dict(
            problema=CHOICES_PROBLEMAS[0][0],
            equipe=CHOICES_EQUIPES[0][0],
            tempo=20,
            status=CHOICES_CONDICAO[0][0]
        )
        self.resp = self.client.post(r(view_in_test), self.data)

    def test_armazenado_problema(self):
        self.assertTrue(SubmissaoModel.objects.exists())

    def test_template(self):
        self.assertTemplateUsed(self.resp, template_post_in_ok_case)

    def test_200_template(self):
        self.assertEqual(200, self.resp.status_code)

    def test_csrf(self):
        self.assertContains(self.resp, 'csrfmiddlewaretoken')


class LancamentoPostFail(TestCase):
    def setUp(self):
        self.data = dict(
            problema=CHOICES_PROBLEMAS[0][0],
            equipe=CHOICES_EQUIPES[0][0],
            status=CHOICES_CONDICAO[0][0]
        )
        self.resp = self.client.post(r(view_in_test), self.data)

    def test_template(self):
        self.assertTemplateUsed(self.resp, template_post_in_fail_case)

    def test_200_template(self):
        self.assertEqual(200, self.resp.status_code)

    def test_csrf(self):
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubmissaoForm)
