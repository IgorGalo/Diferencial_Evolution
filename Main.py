from grafo import Grafo
from Elitismo import Elitismo
from Processo import Processo
from Maquina import Maquina


def executar():

    dif = int(input("Selecione o arquivo dentre as opções -\n1 - Fácil\n2- Médio\n3- Difícil\n: ")) 
    match dif:
        case 1:
            dif = "easy.txt"
        case 2:
            dif = "medium.txt"
        case 3:
            dif = "hard.txt"

    num_tarefas, num_maquinas = lerDados(dif)
    print(f"numero de maquinas: {num_maquinas}")
    print(f"numero de tarefas: {num_tarefas}")

    maquinas = []
    if(dif == "medium.txt"):
            maquinas = Maquina().lerMaquinas(dif)
    else:
        for i in range(num_maquinas):
            maquinas.append(Maquina(id = i))

    processos = Processo().lerProcessos(dif)
    for processo in processos:
        print(processo.toString())
    
    for processo in processos:
        menor_custo = float('inf')
        maquina_escolhida = None

        for maquina in maquinas:
            custo = maquina.custo()

            if maquina.capacidade is None or len(maquina.processos) < maquina.capacidade:
                if custo < menor_custo:
                    menor_custo = custo
                    maquina_escolhida = maquina

        maquina_escolhida.processos.append(processo)

    for maquina in maquinas:
            print(maquina.toString())


    """elitismo = Elitismo(
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
"""

def lerDados(nome_arquivo):
    num_tarefas = 0
    num_maquinas = 0
    
    with open(nome_arquivo, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
        for linha in linhas:
            linha_limpa = linha.strip()
            
            if not linha_limpa:
                continue
                
            if linha_limpa.lower().startswith("número de máquinas:"):
                num_maquinas = int(linha_limpa.split(":")[1].strip())

            if linha_limpa.lower().startswith("número de tarefas:"):
                num_tarefas = int(linha_limpa.split(":")[1].strip())
                
            if num_maquinas > 0 and num_tarefas > 0:
                break
                
        return num_tarefas, num_maquinas


if __name__ == "__main__":
    executar()



    
