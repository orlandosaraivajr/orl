from django.shortcuts import resolve_url as r
from django.test import Client, TestCase

view_in_test = 'core:index'
template_in_test = 'index.html'


class IndexGet(TestCase):
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
            ('Olimpíada', 1),
            ('FHO', 1),
            ('<form', 3),
            ('</form>', 3),
            ('type="submit"', 3),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)


class IndexPost(TestCase):
    def setUp(self):
        self.client = Client()
        self.resp = self.client.post(r(view_in_test))

    def test_template(self):
        self.assertTemplateUsed(self.resp, template_in_test)

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
