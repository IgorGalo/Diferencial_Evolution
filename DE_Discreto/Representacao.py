import random


class Representacao:

    def __init__(
        self,
        numero_tarefas,
        numero_maquinas=None,
        processos=None,
        maquinas=None
    ):
        self.valor_objetivo = 0.0
        self.aptidao = 0.0
        if isinstance(numero_tarefas, list):
            self.cromossomo = numero_tarefas.copy()
        else:
            self.cromossomo = []

            for i in range(numero_tarefas):
                processo = processos[i]
                maquinas_validas = []

                for maquina in maquinas:
                    if (
                        maquina.capacidade is None
                        or processo.tempo <= maquina.capacidade
                    ):
                        maquinas_validas.append(maquina.id)
                maquina_escolhida = random.choice(maquinas_validas)
                self.cromossomo.append(maquina_escolhida)

    def copiar(self):
        copia = Representacao(self.cromossomo)
        copia.valor_objetivo = self.valor_objetivo
        copia.aptidao = self.aptidao

        return copia

    def __repr__(self):
        return str(self.cromossomo)