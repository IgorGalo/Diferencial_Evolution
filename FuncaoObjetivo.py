class FuncaoObjetivo:

    @staticmethod
    def calcular(individuo, processos, maquinas):

        if not any(processo.prioridades for processo in processos):

            cargas = {}

            for maquina in maquinas:
                cargas[maquina.id] = 0

            for i, maquina_id in enumerate(
                individuo.cromossomo
            ):
                processo = processos[i]
                cargas[maquina_id] += processo.tempo

            return max(cargas.values())

        return FuncaoObjetivo.calcular_com_precedencia(
            individuo,
            processos,
            maquinas
        )

    @staticmethod
    def calcular_com_precedencia(
        individuo,
        processos,
        maquinas
    ):

        processos_por_id = {
            int(processo.id): processo
            for processo in processos
        }

        predecessoras = {
            tarefa_id: []
            for tarefa_id in processos_por_id
        }

        for processo in processos:

            id_processo = int(processo.id)

            for sucessora in processo.prioridades:

                predecessoras[int(sucessora)].append(
                    id_processo
                )

        tempo_maquina = {
            maquina.id: 0
            for maquina in maquinas
        }

        tempo_fim = {}

        pendentes = set(
            processos_por_id.keys()
        )

        while pendentes:

            tarefas_prontas = []

            for tarefa_id in pendentes:

                preds = predecessoras[tarefa_id]

                if all(
                    pred in tempo_fim
                    for pred in preds
                ):

                    processo = processos_por_id[tarefa_id]

                    maquina_id = (
                        individuo.cromossomo[tarefa_id - 1]
                    )

                    fim_predecessoras = max(
                        (
                            tempo_fim[pred]
                            for pred in preds
                        ),
                        default=0
                    )

                    inicio = max(
                        tempo_maquina[maquina_id],
                        fim_predecessoras
                    )

                    tarefas_prontas.append(
                        (
                            inicio,
                            -processo.tempo,
                            tarefa_id,
                            maquina_id
                        )
                    )

            if not tarefas_prontas:
                raise ValueError(
                    "Não foi possível respeitar as "
                    "restrições de precedência."
                )

            inicio, _, tarefa_id, maquina_id = min(
                tarefas_prontas
            )

            processo = processos_por_id[tarefa_id]

            fim = inicio + processo.tempo

            tempo_maquina[maquina_id] = fim

            tempo_fim[tarefa_id] = fim

            pendentes.remove(tarefa_id)

        return max(tempo_fim.values())
