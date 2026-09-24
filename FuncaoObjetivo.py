class FuncaoObjetivo:

    @staticmethod
    def calcular(individuo, grafo):
        rota = individuo.cromossomo
        distancia = 0
        for origem, destino in zip(rota, rota[1:] + rota[:1]):
            distancia += grafo.distancia(origem, destino)

        return distancia