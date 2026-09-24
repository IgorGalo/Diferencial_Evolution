import random

class Roleta:
    @staticmethod
    def roleta(populacao):
        individuos = populacao.individuos
        pesos = []
        for individuo in individuos:
            peso = Roleta._peso(individuo)
            pesos.append(peso)
        total_pesos = sum(pesos)
        sorteio = random.random() * total_pesos
        acumulado = 0
        for individuo, peso in zip(individuos, pesos):
            acumulado += peso
            if acumulado >= sorteio:
                return individuo
        # Caso de segurança
        return individuos[-1]

    @staticmethod
    def _peso(individuo):
        return 1 / individuo.aptidao