from grafo import Grafo
from Elitismo import Elitismo


def executar():
    grafo =Grafo("dados/sgb128_dist.txt")
    elitismo = Elitismo(
        grafo,
        tamanho_populacao=200,
        geracoes=2000,
        taxa_cruzamento=0.85,
        taxa_mutacao=0.02
    )
    melhor_solucao = elitismo.executar()
    print("\nMelhor solução encontrada:")
    print(melhor_solucao)
    print(f"Custo final: {melhor_solucao.valor_objetivo:.2f}")


if __name__ == "__main__":
    executar()