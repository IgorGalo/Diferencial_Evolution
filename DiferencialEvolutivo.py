import random

from Representacao import Representacao
from FuncaoObjetivo import FuncaoObjetivo

class DiferencialEvolutivo:
    def __init__(
        self,
        processos,
        maquinas,
        tamanho_populacao=20,
        geracoes=50,
        F=0.8,
        CR=0.7,
        arquivo = ""
    ):
        self.processos = processos
        self.maquinas = maquinas
        self.tamanho_populacao = tamanho_populacao
        self.geracoes = geracoes
        # F = fator de mutação
        self.F = F
        # CR = taxa de crossover
        self.CR = CR
        self.numero_tarefas = len(processos)
        self.numero_maquinas = len(maquinas)
        self.arquivo = arquivo

    def criar_populacao(self):
        populacao = []

        if any(
            maquina.capacidade is not None
            for maquina in self.maquinas
        ):
            individuo_guloso = self.criar_individuo_guloso()
            individuo_guloso.valor_objetivo = FuncaoObjetivo.calcular(
                individuo_guloso,
                self.processos,
                self.maquinas
            )
            populacao.append(individuo_guloso)

        for _ in range(self.tamanho_populacao - len(populacao)):
            individuo = Representacao(
                numero_tarefas=self.numero_tarefas,
                numero_maquinas=self.numero_maquinas,
                processos=self.processos,
                maquinas=self.maquinas
            )
            individuo.valor_objetivo = FuncaoObjetivo.calcular(
                individuo,
                self.processos,
                self.maquinas
            )
            populacao.append(individuo)
        return populacao

    def criar_individuo_guloso(self):
        cromossomo = [None] * self.numero_tarefas
        cargas = {
            maquina.id: 0
            for maquina in self.maquinas
        }
        indices_tarefas = sorted(
            range(self.numero_tarefas),
            key=lambda indice: self.processos[indice].tempo,
            reverse=True
        )

        for indice in indices_tarefas:
            processo = self.processos[indice]
            maquinas_validas = [
                maquina
                for maquina in self.maquinas
                if (
                    maquina.capacidade is None
                    or processo.tempo <= maquina.capacidade
                )
            ]
            menor_carga = min(
                cargas[maquina.id]
                for maquina in maquinas_validas
            )
            maquinas_menos_carregadas = [
                maquina
                for maquina in maquinas_validas
                if cargas[maquina.id] == menor_carga
            ]
            maquina_escolhida = random.choice(
                maquinas_menos_carregadas
            )
            cromossomo[indice] = maquina_escolhida.id
            cargas[maquina_escolhida.id] += processo.tempo

        return Representacao(cromossomo)

    def mutacao(self, x1, x2, x3):
        mutante = []

        for i in range(self.numero_tarefas):
            valor = x1.cromossomo[i] + self.F * (
                x2.cromossomo[i] - x3.cromossomo[i]
            )

            valor = self.discretizacao(valor)

            mutante.append(valor)

        return Representacao(mutante)

    def mutacaoMedium(self, x1, x2, x3):

        mutante = []

        for i in range(self.numero_tarefas):

            valor = x1.cromossomo[i]

            if random.random() < self.F:

                if x2.cromossomo[i] != x3.cromossomo[i]:

                    valor = x2.cromossomo[i]

                else:

                    valor = x1.cromossomo[i]

            mutante.append(valor)

        return Representacao(mutante)

    def discretizacao(self, valor):
        valor = round(valor)

        if valor < 1:
            valor = 1
        elif valor > self.numero_maquinas:
            valor = self.numero_maquinas

        return valor

    def crossover(self, alvo, mutante):
        """
        Crossover binomial.
        Cada posição pode vir do mutante
        ou permanecer igual ao indivíduo alvo.
        """
        filho = []
        # Garante que pelo menos uma posição venha
        # do mutante
        posicao_obrigatoria = random.randrange(
            self.numero_tarefas
        )

        for i in range(self.numero_tarefas):
            if (
                random.random() < self.CR
                or i == posicao_obrigatoria
            ):
                filho.append(
                    mutante.cromossomo[i]
                )
            else:
                filho.append(
                    alvo.cromossomo[i]
                )

        return Representacao(filho)

    def avaliar(self, individuo):
        individuo.valor_objetivo = (
            FuncaoObjetivo.calcular(
                individuo,
                self.processos,
                self.maquinas
            )
        )


    def reparar(self, individuo):
        for i, maquina_id in enumerate(individuo.cromossomo):

            processo = self.processos[i]

            maquina = next(
                maquina
                for maquina in self.maquinas
                if maquina.id == maquina_id
            )

            # Verifica se a máquina consegue executar a tarefa
            if (
                maquina.capacidade is not None
                and processo.tempo > maquina.capacidade
            ):

                maquinas_validas = [
                    maquina
                    for maquina in self.maquinas
                    if (
                        maquina.capacidade is None
                        or processo.tempo <= maquina.capacidade
                    )
                ]

                nova_maquina = random.choice(maquinas_validas)

                individuo.cromossomo[i] = nova_maquina.id

        return individuo

    def executar(self):
        populacao = self.criar_populacao()
        melhor = min(
            populacao,
            key=lambda individuo:
            individuo.valor_objetivo
        )
        self.melhor_inicial = melhor.copiar()

        for geracao in range(1, self.geracoes + 1):
            nova_populacao = []
            aceitos = 0
            for i in range(self.tamanho_populacao):
                alvo = populacao[i]
                indices = list(
                    range(self.tamanho_populacao)
                )
                indices.remove(i)
                r1, r2, r3 = random.sample(
                    indices,
                    3
                )
                x1 = populacao[r1]
                x2 = populacao[r2]
                x3 = populacao[r3]
                # Mutação diferencial
                if self.arquivo == "Ex2IA_3/medium.txt":
                    mutante = self.mutacaoMedium(
                        x1,
                        x2,
                        x3
                    )
                else: 
                    mutante = self.mutacao(
                        x1,
                        x2,
                        x3
                    )
                # Crossover
                candidato = self.crossover(
                    alvo,
                    mutante
                )

                #reparo de maquinas invalidas
                candidato = self.reparar(candidato)

                # Avaliação
                self.avaliar(candidato)
                # Seleção
                if (
                    candidato.valor_objetivo
                    <= alvo.valor_objetivo
                ):
                    nova_populacao.append(candidato)
                    aceitos += 1
                else:
                    nova_populacao.append(alvo)
            populacao = nova_populacao
            melhor_geracao = min(
                populacao,
                key=lambda individuo:
                individuo.valor_objetivo
            )
            if (
                melhor_geracao.valor_objetivo
                < melhor.valor_objetivo
            ):
                melhor = melhor_geracao.copiar()
            print(
                f"Geração {geracao:3d} | "
                f"Melhor makespan: "
                f"{melhor.valor_objetivo:.0f}"
                f" | Aceitos: {aceitos}"
            )
        print("\n================================")
        print("MELHOR SOLUÇÃO ENCONTRADA")
        print("================================")
        print(
            f"Cromossomo:\n"
            f"{melhor.cromossomo}"
        )
        print(
            f"Makespan:\n"
            f"{melhor.valor_objetivo:.0f}"
        )

        return melhor