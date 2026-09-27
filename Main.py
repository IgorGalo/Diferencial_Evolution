from DiferencialEvolutivo import DiferencialEvolutivo
from processo import Processo
from Maquina import Maquina

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
                num_maquinas = int(
                    linha_limpa.split(":")[1].strip()
                )
            if linha_limpa.lower().startswith("número de tarefas:"):
                num_tarefas = int(
                    linha_limpa.split(":")[1].strip()
                )
            if num_maquinas > 0 and num_tarefas > 0:
                break

    return num_tarefas, num_maquinas


def executar():
    opcao = int(input(
        "Selecione o arquivo dentre as opções -\n"
        "1 - Fácil\n"
        "2 - Médio\n"
        "3 - Difícil\n: "
    ))
    match opcao:
        case 1:
            arquivo = "DE_Discreto/easy.txt"

        case 2:
            arquivo = "DE_Discreto/medium.txt"

        case 3:
            arquivo = "DE_Discreto/hard.txt"

        case _:
            print("Opção inválida.")
            return
    # LEITURA DOS DADOS
    num_tarefas, num_maquinas = lerDados(arquivo)
    processos = Processo().lerProcessos(arquivo)

    # CRIAÇÃO DAS MÁQUINAS
    maquinas = []
    if opcao == 2:
        # Medium:
        # máquinas possuem capacidades diferentes
        maquinas = Maquina().lerMaquinas(arquivo)
        for maquina in maquinas:
            print(
                f"id={maquina.id}, "
                f"capacidade={maquina.capacidade}, "
                f"tipo_id={type(maquina.id)}, "
                f"tipo_capacidade={type(maquina.capacidade)}"
            )

    else:
        # Easy e Hard:
        # máquinas idênticas
        for i in range(num_maquinas):
            maquinas.append(
                Maquina(id=i + 1)
            )
    # CONFIGURAÇÃO
    print("\n================================")
    print("CONFIGURAÇÃO DO PROBLEMA")
    print("================================")
    print(f"Arquivo: {arquivo}")
    print(f"Tarefas: {num_tarefas}")
    print(f"Máquinas: {num_maquinas}")

    if opcao == 2:
        print("\nCapacidades das máquinas:")

        for maquina in maquinas:
            print(
                f"Máquina {maquina.id}: "
                f"{maquina.capacidade}"
            )

    # DIFERENCIAL EVOLUTIVO
    de = DiferencialEvolutivo(
        processos,
        maquinas,
        tamanho_populacao=20,
        geracoes=50,
        F=0.8,
        CR=0.9
    )
    melhor = de.executar()

if __name__ == "__main__":
    executar()