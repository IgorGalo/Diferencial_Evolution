import random

from grafo import Grafo
from Elitismo import Elitismo
from Processo import Processo
from Maquina import Maquina


def executar():

    dif = int(input(
        "Selecione o arquivo dentre as opções -\n"
        "1 - Fácil\n"
        "2 - Médio\n"
        "3 - Difícil\n: "
    ))

    match dif:
        case 1:
            dif = "easy.txt"
        case 2:
            dif = "medium.txt"
        case 3:
            dif = "hard.txt"

    num_tarefas, num_maquinas = lerDados(dif)

    maquinas = []

    if dif == "medium.txt":
        maquinas = Maquina().lerMaquinas(dif)
    else:
        for i in range(num_maquinas):
            maquinas.append(Maquina(id=i+1))

    processos = Processo().lerProcessos(dif)

    tamanho_populacao = 20
    populacao = []

    for i in range(tamanho_populacao):
        individuo = gerar_individuo(processos, maquinas)
        populacao.append(individuo)

    for i, individuo in enumerate(populacao):
        print(f"Indivíduo {i + 1}: {individuo}")

    

def gerar_individuo(processos, maquinas):
    individuo = []

    for processo in processos:

        maquinas_validas = []

        for maquina in maquinas:
            if (
                maquina.capacidade is None
                or processo.tempo <= maquina.capacidade
            ):
                maquinas_validas.append(maquina)

        maquina = random.choice(maquinas_validas)

        individuo.append(maquina.id)

    return individuo

def gerar_mutante(populacao):
    individuos = random.sample(populacao, 3)

    x_r1 = individuos[0]
    x_r2 = individuos[1]
    x_r3 = individuos[2]
    

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



    
