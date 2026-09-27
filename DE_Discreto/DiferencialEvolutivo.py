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
        CR=0.7
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

    def criar_populacao(self):
        populacao = []

        for _ in range(self.tamanho_populacao):
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

    def mutacao(self, x1, x2, x3):
        """
        Mutação diferencial adaptada para representação discreta.

        Para cada tarefa:

        x1 = indivíduo base
        x2 = indivíduo diferencial 1
        x3 = indivíduo diferencial 2
        """
        mutante = []

        for i in range(self.numero_tarefas):
            valor = x1.cromossomo[i]
            # Aplica a diferença entre x2 e x3
            if random.random() < self.F:
                if x2.cromossomo[i] != x3.cromossomo[i]:
                    valor = random.choice([
                        x2.cromossomo[i],
                        x3.cromossomo[i]
                    ])
            mutante.append(valor)

        return Representacao(mutante)

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

    def executar(self):
        populacao = self.criar_populacao()
        melhor = min(
            populacao,
            key=lambda individuo:
            individuo.valor_objetivo
        )

        for geracao in range(1, self.geracoes + 1):
            nova_populacao = []
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
                # Avaliação
                self.avaliar(candidato)
                # Seleção
                if (
                    candidato.valor_objetivo
                    <= alvo.valor_objetivo
                ):
                    nova_populacao.append(candidato)
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