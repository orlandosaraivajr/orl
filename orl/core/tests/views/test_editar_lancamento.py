from django.shortcuts import resolve_url as r
from django.test import Client, TestCase

from core.forms import SubmissaoForm, PreSubmissaoForm
from core.models import (
    CHOICES_PROBLEMAS, CHOICES_EQUIPES,
    CHOICES_CONDICAO, SubmissaoModel
)

view_in_test = 'core:editar_lancamento'
template_get_case = 'index.html'
template_post_in_ok_case = 'pre_lancamento.html'
template_post_in_fail_case = 'editar_lancamento.html'


class EditarLancamentoGet(TestCase):
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


class EditarLancamentoPostFail(TestCase):
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

    def test_template(self):
        self.assertTemplateUsed(self.resp, template_post_in_fail_case)

    def test_200_template(self):
        self.assertEqual(200, self.resp.status_code)

    def test_csrf(self):
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_context_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubmissaoForm)

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
        self.cadastro.tempo = 50
        self.form = SubmissaoForm(instance=self.cadastro)
        self.data = dict(
            id_lancamento=self.cadastro.pk,
            equipe=CHOICES_EQUIPES[4][0],
            status=CHOICES_CONDICAO[1][0],
            problema=CHOICES_PROBLEMAS[6][0],
            tempo=50,
        )
        self.resp = self.client.post(r(view_in_test), self.data)

    def test_tempo_alterado(self):
        gravado = SubmissaoModel.objects.get(pk=1)
        self.assertEqual(50, gravado.tempo)
        self.assertNotEqual(20, gravado.status)

    def test_problema_status(self):
        gravado = SubmissaoModel.objects.get(pk=1)
        self.assertEqual(CHOICES_PROBLEMAS[6][0], gravado.problema)
        self.assertNotEqual(CHOICES_PROBLEMAS[1][0], gravado.problema)

    def test_status_alterado(self):
        gravado = SubmissaoModel.objects.get(pk=1)
        self.assertEqual(CHOICES_CONDICAO[1][0], gravado.status)
        self.assertNotEqual(CHOICES_CONDICAO[0][0], gravado.status)

    def test_equipe_alterado(self):
        gravado = SubmissaoModel.objects.get(pk=1)
        self.assertEqual(CHOICES_EQUIPES[4][0], gravado.equipe)

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
