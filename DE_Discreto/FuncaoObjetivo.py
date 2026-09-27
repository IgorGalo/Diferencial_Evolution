class FuncaoObjetivo:

    @staticmethod
    def calcular(individuo, processos, maquinas):
        cargas = {}

        for maquina in maquinas:
            cargas[maquina.id] = 0

        for i, maquina_id in enumerate(
            individuo.cromossomo
        ):
            processo = processos[i]

            cargas[maquina_id] += processo.tempo
        makespan = max(cargas.values())

        return makespan