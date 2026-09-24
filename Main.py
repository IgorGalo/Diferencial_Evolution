from grafo import Grafo
from Elitismo import Elitismo
from processo import processo

def executar():
    """grafo =Grafo("easy.txt")"""
    num_maquinas = 0
    lendo_tabela = False
    processos = []
    nome_arquivo = 'easy.txt'
    with open(nome_arquivo, 'r', encoding = 'utf-8') as f:
        linhas = f.readlines()
        contador =0
        for linha in linhas:
            
            linhas = linha.strip()

            if linha.startswith("Número de Máquinas:"):
                num_maquinas = int(linha.split(":")[1].strip())

            elif linha.startswith("ID_Tarefa"):
                lendo_tabela = True
                continue

            elif lendo_tabela:
                processos.append(processo(
                    linha.split()[0],
                    linha.split()[1]
                ))   
                print(processos[contador].toString())
                contador = contador + 1


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