import random

class Representacao:
    def __init__(self, cromossomo):
        self.valor_objetivo = 0.0
        self.aptidao = 0.0
        if isinstance(cromossomo, int):
            self.cromossomo = list(range(cromossomo))
            random.shuffle(self.cromossomo)
        else:
            self.cromossomo = cromossomo.copy()

    def copiar(self):
        copia = Representacao(self.cromossomo)
        copia.valor_objetivo = self.valor_objetivo
        copia.aptidao = self.aptidao
        return copia

    def __repr__(self):
        return str(self.cromossomo)

    def imprimir(self):
        print(*self.cromossomo)