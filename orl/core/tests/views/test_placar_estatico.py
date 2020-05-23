from django.shortcuts import resolve_url as r
from django.test import Client, TestCase
from core.models import SubmissaoModel

view_in_test = 'core:placar_estatico'
template_get_case = 'placar_estatico.html'


class PlacarEstaticoGet_withData(TestCase):
    def setUp(self):
        cad = SubmissaoModel(equipe=1, problema=2, status='RE', tempo=5)
        cad.save()
        cad = SubmissaoModel(equipe=1, problema=1, status='RE', tempo=5)
        cad.save()
        cad = SubmissaoModel(equipe=1, problema=1, status='AC', tempo=20)
        cad.save()
        cad = SubmissaoModel(equipe=1, problema=2, status='AC', tempo=55)
        cad.save()
        cad = SubmissaoModel(equipe=1, problema=5, status='RE', tempo=10)
        cad.save()
        cad = SubmissaoModel(equipe=1, problema=5, status='AC', tempo=20)
        cad.save()
        cad = SubmissaoModel(equipe=2, problema=1, status='RE', tempo=12)
        cad.save()
        cad = SubmissaoModel(equipe=5, problema=2, status='RE', tempo=20)
        cad.save()
        cad = SubmissaoModel(equipe=7, problema=1, status='AC', tempo=12)
        cad.save()
        cad = SubmissaoModel(equipe=9, problema=1, status='AC', tempo=10)
        cad.save()
        cad = SubmissaoModel(equipe=9, problema=2, status='AC', tempo=12)
        cad.save()
        cad = SubmissaoModel(equipe=9, problema=5, status='AC', tempo=12)
        cad.save()
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
            ('Equipe ', 5),
            ('125', 1),
            ('(3, 34)', 1),
            ('(3, 125)', 1),
            ('(1, 12)', 4),
            ('(0, 0)', 43),
            ('<table', 1),
            ('<td>', 60),
            ('<tr>', 5),
            ('</tr>', 5),
            ('</td>', 60),
            ('</table>', 1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)
