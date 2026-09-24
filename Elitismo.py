import random
from Populacao import Populacao
from Avaliador import Avaliador
from Roleta import Roleta
from Cruzamento import Cruzamento
from Mutacao import Mutacao

class Elitismo:
    def __init__(
        self,
        grafo,
        tamanho_populacao=100,
        geracoes=1000,
        taxa_cruzamento=0.8,
        taxa_mutacao=0.05
    ):
        self.grafo = grafo
        self.tamanho_populacao = tamanho_populacao
        self.geracoes = geracoes
        self.taxa_cruzamento = taxa_cruzamento
        self.taxa_mutacao = taxa_mutacao

    def executar(self):
        populacao = Populacao.criar(self.tamanho_populacao,self.grafo.quantidade_vertices())
        Avaliador.avaliar(populacao,self.grafo)
        for geracao in range(self.geracoes):
            melhor_da_geracao = (populacao.melhor().copiar())
            nova_populacao = []
            while len(nova_populacao) < self.tamanho_populacao - 1:
                pai1 = Roleta.roleta(populacao)
                pai2 = Roleta.roleta(populacao)
                while pai1 == pai2:
                    pai2 = Roleta.roleta(populacao)
                if random.random() <= self.taxa_cruzamento:
                    filhos = Cruzamento.crossoverOrdem(pai1, pai2)
                else:
                    filhos = [pai1.copiar(), pai2.copiar()]
                nova_populacao.extend(filhos)
            nova_populacao = nova_populacao[:self.tamanho_populacao - 1]
            Mutacao.aplicar(nova_populacao, self.taxa_mutacao)
            populacao = Populacao(nova_populacao)
            Avaliador.avaliar(populacao, self.grafo)
            populacao.adicionar(melhor_da_geracao)
            melhor = populacao.melhor()
            print(f"Geração {geracao + 1:4d}  | Custo: {melhor.valor_objetivo:.2f}")

        return populacao.melhor()