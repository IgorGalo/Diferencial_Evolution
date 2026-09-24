import random
from Representacao import Representacao

class Cruzamento:

    @staticmethod
    def criar_filho(pai1, pai2):
        rota1 = pai1.cromossomo
        rota2 = pai2.cromossomo
        tamanho = len(rota1)
        filho = [-1] * tamanho
        inicio, fim = sorted(random.sample(range(tamanho), 2))
        filho[inicio:fim + 1] = rota1[inicio:fim + 1]
        posicao = (fim + 1) % tamanho
        for cidade in rota2:
            if cidade not in filho:
                filho[posicao] = cidade
                posicao = (posicao + 1) % tamanho
        return Representacao(filho)

    @staticmethod
    def crossoverOrdem(pai1, pai2):
        filho1 = Cruzamento.criar_filho(pai1, pai2)
        filho2 = Cruzamento.criar_filho(pai2, pai1)
        return [filho1, filho2]

