class FuncaoObjetivo:

    @staticmethod
    def calcular(individuo, processos, maquinas):

        # Caso normal: fácil e médio
        # Se não existem prioridades, basta calcular as cargas
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

        # Caso difícil: existem prioridades
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

        # Tarefas organizadas pelo ID
        processos_por_id = {
            int(processo.id): processo
            for processo in processos
        }

        # Guarda quem precisa terminar antes de cada tarefa
        predecessoras = {
            tarefa_id: []
            for tarefa_id in processos_por_id
        }

        # Lê as prioridades diretamente do TXT
        for processo in processos:

            id_processo = int(processo.id)

            for sucessora in processo.prioridades:

                predecessoras[int(sucessora)].append(
                    id_processo
                )

        # Momento em que cada máquina fica livre
        tempo_maquina = {
            maquina.id: 0
            for maquina in maquinas
        }

        # Momento em que cada tarefa terminou
        tempo_fim = {}

        # Tarefas que ainda não foram agendadas
        pendentes = set(
            processos_por_id.keys()
        )

        while pendentes:

            tarefas_prontas = []

            # Procura tarefas cujas predecessoras
            # já terminaram
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

                    # Quando a tarefa poderia começar
                    # considerando apenas as predecessoras
                    fim_predecessoras = max(
                        (
                            tempo_fim[pred]
                            for pred in preds
                        ),
                        default=0
                    )

                    # A máquina também precisa estar livre
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

            # Se não houver tarefa pronta, existe algum
            # problema nas precedências
            if not tarefas_prontas:
                raise ValueError(
                    "Não foi possível respeitar as "
                    "restrições de precedência."
                )

            # Escolhe a próxima tarefa
            # menor início primeiro
            inicio, _, tarefa_id, maquina_id = min(
                tarefas_prontas
            )

            processo = processos_por_id[tarefa_id]

            fim = inicio + processo.tempo

            # Atualiza máquina
            tempo_maquina[maquina_id] = fim

            # Registra término da tarefa
            tempo_fim[tarefa_id] = fim

            # Remove das pendentes
            pendentes.remove(tarefa_id)

        return max(tempo_fim.values())