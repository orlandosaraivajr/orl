from django.test import TestCase
from core.models import (
    CHOICES_EQUIPES, SubmissaoModel)
from core.logic import (
    Equipe, Placar)


class TestPlacar(TestCase):
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
        self.placar = Placar()

    def test_Placar_get_ranking(self):
        lista = [(1, 10), (1, 12), (0, 0), (0, 0), (1, 12),
                 (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
        equipes = self.placar.get_ranking()
        self.assertEqual(5, len(equipes))
        self.assertEqual(list, type(equipes))
        for i in range(len(equipes)):
            self.assertEqual(type(Equipe(0, lista, 0)), type(equipes[i]))

    def test_Placar__get_lista_problemas(self):
        lista_problemas = self.placar.get_lista_problemas()
        self.assertEqual(10, len(lista_problemas))
        self.assertEqual(list, type(lista_problemas))

    def test_Placar__get_lista_equipes(self):
        equipes = self.placar.get_lista_equipes()
        self.assertEqual(5, len(equipes))
        self.assertEqual(list, type(equipes))

    def test_Placar__get_lista_pontuacao_equipe(self):
        equipes = self.placar._get_lista_pontuacao_equipe(1)
        self.assertEqual(10, len(equipes))
        self.assertEqual(list, type(equipes))
        self.assertEqual(equipes[0], (2, 35))
        self.assertEqual(equipes[1], (2, 70))
        self.assertEqual(equipes[2], (0, 0))
        self.assertEqual(equipes[3], (0, 0))
        self.assertEqual(equipes[4], (2, 40))
        self.assertEqual(equipes[5], (0, 0))
        self.assertEqual(equipes[6], (0, 0))
        self.assertEqual(equipes[7], (0, 0))
        self.assertEqual(equipes[8], (0, 0))
        self.assertEqual(equipes[9], (0, 0))

    def test_Placar__prepare_classificacao_equipes(self):
        lista_equipes = self.placar.get_lista_equipes()
        classificacao = self.placar._prepare_classificacao_equipes(
            lista_equipes)
        self.assertEqual(5, len(classificacao))
        self.assertEqual(list, type(classificacao))
        self.assertEqual(classificacao[0][2], 3)
        self.assertEqual(classificacao[0][3], 34)
        self.assertEqual(classificacao[1][2], 3)
        self.assertEqual(classificacao[1][3], 145)
        self.assertEqual(classificacao[2][2], 1)
        self.assertEqual(classificacao[2][3], 12)
        self.assertEqual(classificacao[3][2], 0)
        self.assertEqual(classificacao[3][3], 0)
        self.assertEqual(classificacao[4][2], 0)
        self.assertEqual(classificacao[4][3], 0)

    def test_Placar__prepare_ranking(self):
        lista_equipes = self.placar.get_lista_equipes()
        classificacao = self.placar._prepare_classificacao_equipes(
            lista_equipes)
        equipes = self.placar._prepare_ranking(classificacao)
        lista = [(1, 10), (1, 12), (0, 0), (0, 0), (1, 12),
                 (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
        local_equipe = Equipe(0, lista, 0)
        self.assertEqual(5, len(equipes))
        self.assertEqual(list, type(equipes))
        self.assertEqual(type(local_equipe), type(equipes[0]))
        self.assertNotEqual(equipes[0].equipe, None)
        self.assertEqual(equipes[0].problema1, (1, 10))
        self.assertEqual(equipes[0].soma, (3, 34))

    def test_Placar__sum_pontuacao_equipe_01(self):
        soma = self.placar._sum_pontuacao_equipe(1)
        self.assertEqual(145, soma)
        self.assertEqual(int, type(soma))

    def test_Placar__sum_pontuacao_equipe_02(self):
        soma = self.placar._sum_pontuacao_equipe(9)
        self.assertEqual(34, soma)
        self.assertEqual(int, type(soma))

    def test_Placar__sum_acertos_equipe_01(self):
        soma = self.placar._sum_acertos_equipe(1)
        self.assertEqual(3, soma)
        self.assertEqual(int, type(soma))

    def test_Placar__sum_acertos_equipe_02(self):
        soma = self.placar._sum_acertos_equipe(5)
        self.assertEqual(0, soma)
        self.assertEqual(int, type(soma))

    def test_Placar__pontuacao_por_equipe_problema_01(self):
        pontuacao = self.placar._pontuacao_por_equipe_problema(1, 1)
        self.assertEqual((2, 35), pontuacao)
        self.assertEqual(tuple, type(pontuacao))

    def test_Placar__pontuacao_por_equipe_problema_02(self):
        pontuacao = self.placar._pontuacao_por_equipe_problema(1, 2)
        self.assertEqual((2, 70), pontuacao)
        self.assertEqual(tuple, type(pontuacao))

    def test_Placar__get_nome_equipe(self):
        for numero in range(len(CHOICES_EQUIPES)):
            nome_equipe = self.placar._get_nome_equipe(numero)
            self.assertEqual(CHOICES_EQUIPES[numero-1][1], nome_equipe)


class TestPlacarNoData(TestCase):
    def setUp(self):
        self.placar = Placar()

    def test_Placar_get_ranking(self):
        equipes = self.placar.get_ranking()
        self.assertEqual(0, len(equipes))

    def test_Placar__get_lista_problemas(self):
        lista_problemas = self.placar.get_lista_problemas()
        self.assertEqual(10, len(lista_problemas))
        self.assertEqual(list, type(lista_problemas))

    def test_Placar__get_lista_equipes(self):
        equipes = self.placar.get_lista_equipes()
        self.assertEqual(0, len(equipes))

    def test_Placar__get_lista_pontuacao_equipe(self):
        equipes = self.placar._get_lista_pontuacao_equipe(1)
        self.assertEqual(10, len(equipes))

    def test_Placar__prepare_classificacao_equipes(self):
        lista_equipes = self.placar.get_lista_equipes()
        classificacao = self.placar._prepare_classificacao_equipes(
            lista_equipes)
        self.assertEqual(0, len(classificacao))

    def test_Placar__prepare_ranking(self):
        lista_equipes = self.placar.get_lista_equipes()
        classificacao = self.placar._prepare_classificacao_equipes(
            lista_equipes)
        equipes = self.placar._prepare_ranking(classificacao)
        self.assertEqual(0, len(equipes))

    def test_Placar__sum_pontuacao_equipe_01(self):
        soma = self.placar._sum_pontuacao_equipe(1)
        self.assertEqual(0, soma)
        self.assertEqual(int, type(soma))

    def test_Placar__sum_acertos_equipe_01(self):
        soma = self.placar._sum_acertos_equipe(1)
        self.assertEqual(0, soma)
        self.assertEqual(int, type(soma))

    def test_Placar__pontuacao_por_equipe_problema_01(self):
        pontuacao = self.placar._pontuacao_por_equipe_problema(1, 1)
        self.assertEqual((0, 0), pontuacao)
        self.assertEqual(tuple, type(pontuacao))

    def test_Placar__get_nome_equipe(self):
        for numero in range(len(CHOICES_EQUIPES)):
            nome_equipe = self.placar._get_nome_equipe(numero)
            self.assertEqual(CHOICES_EQUIPES[numero-1][1], nome_equipe)


class TestEquipe(TestCase):
    def setUp(self):
        self.equipe_nome = 'Equipe 01'
        self.equipe_pontos = [(1, 10), (1, 12), (0, 0), (0, 0), (1, 12)]
        self.equipe_pontos = self.equipe_pontos + [(0, 0), (0, 0), (0, 0)]
        self.equipe_pontos = self.equipe_pontos + [(0, 0), (0, 0)]
        self.equipe_soma = 31
        self.equipe = Equipe(
            self.equipe_nome,
            self.equipe_pontos,
            self.equipe_soma
        )

    def test_nome(self):
        self.assertEqual(self.equipe.equipe, self.equipe_nome)

    def test_soma(self):
        self.assertEqual(self.equipe.soma, self.equipe_soma)

    def test_problemas(self):
        self.assertEqual(self.equipe.problema1, (1, 10))
        self.assertEqual(self.equipe.problema2, (1, 12))
        self.assertEqual(self.equipe.problema3, (0, 0))
        self.assertEqual(self.equipe.problema4, (0, 0))
        self.assertEqual(self.equipe.problema5, (1, 12))
        self.assertEqual(self.equipe.problema6, (0, 0))
        self.assertEqual(self.equipe.problema7, (0, 0))
        self.assertEqual(self.equipe.problema8, (0, 0))
        self.assertEqual(self.equipe.problema9, (0, 0))
        self.assertEqual(self.equipe.problema10, (0, 0))


class TestEquipeFail(TestCase):
    def setUp(self):
        self.equipe_nome = 'Equipe 01'
        self.equipe_pontos = [(1, 10), (1, 12), (0, 0), (0, 0), (1, 12)]
        self.equipe_soma = 31
        self.equipe = Equipe(
            self.equipe_nome,
            self.equipe_pontos,
            self.equipe_soma
        )

    def test_nome(self):
        self.assertEqual(self.equipe.equipe, self.equipe_nome)

    def test_soma(self):
        self.assertEqual(self.equipe.soma, self.equipe_soma)

    def test_problemas(self):
        self.assertEqual(self.equipe.problema1, (1, 10))
        self.assertEqual(self.equipe.problema2, (1, 12))
        self.assertEqual(self.equipe.problema3, (0, 0))
        self.assertEqual(self.equipe.problema4, (0, 0))
        self.assertEqual(self.equipe.problema5, (1, 12))
        self.assertEqual(self.equipe.problema6, None)
        self.assertEqual(self.equipe.problema7, None)
        self.assertEqual(self.equipe.problema8, None)
        self.assertEqual(self.equipe.problema9, None)
        self.assertEqual(self.equipe.problema10, None)
