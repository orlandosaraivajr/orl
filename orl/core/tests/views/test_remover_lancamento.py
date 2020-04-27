from django.shortcuts import resolve_url as r
from django.test import Client, TestCase

from core.forms import PreSubmissaoForm
from core.models import (
    CHOICES_PROBLEMAS, CHOICES_EQUIPES,
    CHOICES_CONDICAO, SubmissaoModel
)

view_in_test = 'core:remover_lancamento'
template_get_case = 'index.html'
template_post_in_ok_case = 'pre_lancamento.html'
template_post_in_fail_case = 'pre_lancamento.html'


class RemoverLancamentoGet(TestCase):
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


class RemoverLancamentoPostFail(TestCase):
    def setUp(self):
        self.cadastro = SubmissaoModel(
            equipe=CHOICES_EQUIPES[1][0],
            status=CHOICES_CONDICAO[0][0],
            problema=CHOICES_PROBLEMAS[1][0],
            tempo=20)
        self.cadastro.save()
        self.data = dict(
            id_lancamento=self.cadastro.pk,
        )
        self.cadastro.delete()
        self.resp = self.client.post(r(view_in_test), self.data)

    def test_template(self):
        self.assertTemplateUsed(self.resp, template_post_in_fail_case)

    def test_200_template(self):
        self.assertEqual(200, self.resp.status_code)

    def test_csrf(self):
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_context_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, PreSubmissaoForm)

    def test_context_id_lancamento(self):
        id_lancamento = self.resp.context['id_lancamento']
        self.assertIsInstance(id_lancamento, str)

    def test_html_template(self):
        tags = (
            ('Olimpíada', 1),
            ('<form', 2),
            ('</form>', 2),
            ('type="submit"', 2),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)


class EditarLancamentoPostOk(TestCase):
    def setUp(self):
        self.cadastro = SubmissaoModel(
            equipe=CHOICES_EQUIPES[1][0],
            status=CHOICES_CONDICAO[0][0],
            problema=CHOICES_PROBLEMAS[1][0],
            tempo=20)
        self.cadastro.save()
        self.data = dict(
            id_lancamento=self.cadastro.pk,
        )
        self.resp = self.client.post(r(view_in_test), self.data)

    def test_removed(self):
        self.assertFalse(SubmissaoModel.objects.exists())

    def test_template(self):
        self.assertTemplateUsed(self.resp, template_post_in_ok_case)

    def test_200_template(self):
        self.assertEqual(200, self.resp.status_code)

    def test_csrf(self):
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_context_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, PreSubmissaoForm)

    def test_html_template(self):
        tags = (
            ('Olimpíada', 1),
            ('<form', 2),
            ('</form>', 2),
            ('type="submit"', 2),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)
