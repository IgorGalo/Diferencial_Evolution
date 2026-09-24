from Representacao import Representacao


class Populacao:
    def __init__(self, individuos=None):
        self.individuos = individuos or []

    @classmethod
    def criar(cls, quantidade, vertices):
        individuos = []
        for i in range(quantidade):
            individuo = Representacao(vertices)
            individuos.append(individuo)

        return cls(individuos)

    def adicionar(self, individuo):
        self.individuos.append(individuo)

    def melhor(self):
        return min(self.individuos, key=lambda individuo: individuo.aptidao)
    
    def __len__(self):
        return len(self.individuos)