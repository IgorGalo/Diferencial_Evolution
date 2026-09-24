from FuncaoObjetivo import FuncaoObjetivo

class Avaliador:
    @staticmethod
    def avaliar(populacao, grafo):
        for individuo in populacao.individuos:
            custo = FuncaoObjetivo.calcular(individuo,grafo)
            individuo.valor_objetivo = custo
            individuo.aptidao = custo   