import random

class Mutacao:
    @staticmethod
    def _trocar_genes(individuo, taxa):
        rota = individuo.cromossomo
        for i in range(len(rota)):
            if random.random() <= taxa:
                j = random.randrange(len(rota))
                while j == i:
                    j = random.randrange(len(rota))
                # Troca duas posições da rota do indivíduo
                rota[i], rota[j] = (rota[j], rota[i])

    @staticmethod
    def aplicar(individuos, taxa):
        for individuo in individuos:
            Mutacao._trocar_genes(individuo, taxa)