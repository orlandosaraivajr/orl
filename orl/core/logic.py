from django.db.models import Sum
from core.models import SubmissaoModel
from core.models import CHOICES_PROBLEMAS
from core.models import CHOICES_EQUIPES


class Equipe:
    def __init__(self, equipe, pontos, soma):
        self.equipe = equipe
        self.pontos = pontos
        self._validar_pontos()
        self.soma = soma

    def _validar_pontos(self):
        try:
            self.problema1 = self.pontos[0]
        except IndexError:
            self.problema1 = None
        try:
            self.problema2 = self.pontos[1]
        except IndexError:
            self.problema2 = None
        try:
            self.problema3 = self.pontos[2]
        except IndexError:
            self.problema3 = None
        try:
            self.problema4 = self.pontos[3]
        except IndexError:
            self.problema4 = None
        try:
            self.problema5 = self.pontos[4]
        except IndexError:
            self.problema5 = None
        try:
            self.problema6 = self.pontos[5]
        except IndexError:
            self.problema6 = None
        try:
            self.problema7 = self.pontos[6]
        except IndexError:
            self.problema7 = None
        try:
            self.problema8 = self.pontos[7]
        except IndexError:
            self.problema8 = None
        try:
            self.problema9 = self.pontos[8]
        except IndexError:
            self.problema9 = None
        try:
            self.problema10 = self.pontos[9]
        except IndexError:
            self.problema10 = None


class Placar:
    def __init__(self):
        pass

    def get_lista_problemas(self):
        lista_problemas = list()
        for problema in CHOICES_PROBLEMAS:
            lista_problemas.append(problema[0])
        return lista_problemas

    def get_lista_equipes(self):
        lista_equipes = set()
        equipes = SubmissaoModel.objects.values('equipe')
        for equipe in equipes:
            lista_equipes.add(equipe.get('equipe', ''))
        return list(lista_equipes)

    def get_ranking(self):
        lista_equipes = self.get_lista_equipes()
        classificacao = self._prepare_classificacao_equipes(lista_equipes)
        equipes = self._prepare_ranking(classificacao)
        return equipes

    def _prepare_ranking(self, classificacao):
        equipes = list()
        for equipe in classificacao:
            pontos = self._get_lista_pontuacao_equipe(equipe[1])
            soma = (equipe[2], equipe[3])
            equipes.append(Equipe(equipe[0], pontos, soma))
        return equipes

    def _get_lista_pontuacao_equipe(self, equipe):
        inner_list = list()
        lista_problemas = self.get_lista_problemas()
        for problema in lista_problemas:
            inner_list.append(
                self._pontuacao_por_equipe_problema(equipe, problema)
            )
        return inner_list

    def _prepare_classificacao_equipes(self, lista_equipes):
        ranking = list()
        for equipe in lista_equipes:
            ranking.append(
                [self._get_nome_equipe(equipe),
                    int(equipe),
                    self._sum_acertos_equipe(equipe),
                    self._sum_pontuacao_equipe(equipe)
                 ]
            )
        b = sorted(ranking, key=lambda x: x[3])
        ranking = sorted(b, key=lambda x: x[2], reverse=True)
        return ranking

    def _get_nome_equipe(self, equipe_id):
        return CHOICES_EQUIPES[int(equipe_id)-1][1]

    def _sum_pontuacao_equipe(self, parametro_equipe):
        lista_tempos = list()
        for problema in CHOICES_PROBLEMAS:
            n1, n2 = self._pontuacao_por_equipe_problema(
                parametro_equipe, problema[0])
            lista_tempos.append(n2)
            soma_tempo = sum(lista_tempos)
        return soma_tempo

    def _sum_acertos_equipe(self, parametro_equipe):
        submissao = SubmissaoModel.objects.filter(
            equipe=parametro_equipe
        ).filter(
            status='AC'
        )
        return submissao.count()

    def _pontuacao_por_equipe_problema(self, equipe, problema):
        submissao_rejeitadas = SubmissaoModel.objects.filter(
            equipe=equipe
        ).filter(
            problema=problema
        ).filter(
            status='RE'
        )
        submissao_aceitas = SubmissaoModel.objects.filter(
            equipe=equipe
        ).filter(
            problema=problema
        ).filter(
            status='AC'
        )
        qtd_envio_rejeitadas = submissao_rejeitadas.count()
        qtd_envio_aceitas = submissao_aceitas.count()
        qtd_envio = qtd_envio_rejeitadas + qtd_envio_aceitas
        tempo_total = 0
        if qtd_envio_aceitas > 0:
            punicao = qtd_envio_rejeitadas * SubmissaoModel().get_punicao()
            tempo_aceito = submissao_aceitas.aggregate(Sum('tempo'))
            tempo1 = tempo_aceito.get('tempo__sum', '0')
            tempo_total = punicao + tempo1
        return qtd_envio, tempo_total
