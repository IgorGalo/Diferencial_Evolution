import time

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


def mostrar_atribuicao(individuo, processos, maquinas, titulo):
    print("\n================================")
    print(titulo)
    print("================================")

    for maquina in maquinas:
        tarefas = []
        carga = 0

        for i, id_maquina in enumerate(individuo.cromossomo):
            if id_maquina == maquina.id:
                tarefas.append(processos[i].id)
                carga += processos[i].tempo

        print(
            f"Máquina {maquina.id}: "
            f"Tarefas {tarefas} | "
            f"Carga total: {carga}"
        )

    print(f"Makespan: {individuo.valor_objetivo:.0f}")


def executar():
    while(1):
        opcao = int(input(
            "\nSelecione o arquivo dentre as opções -\n"
            "1 - Fácil\n"
            "2 - Médio\n"
            "3 - Difícil\n"
            "0 - para Sair\n: "
        ))

        match opcao:
            case 0:
                print("Saindo...")
                break

            case 1:
                arquivo = "easy.txt"

            case 2:
                arquivo = "medium.txt"

            case 3:
                arquivo = "hard.txt"

            case _:
                print("Opção inválida.")
                return

        geracoes = int(input("Por favor informe quantas gerações deseja que sejam geradas pelo programa: "))

        num_tarefas, num_maquinas = lerDados(arquivo)
        processos = Processo().lerProcessos(arquivo)

        maquinas = []

        if opcao == 2:
            maquinas = Maquina().lerMaquinas(arquivo)
        else:
            for i in range(num_maquinas):
                maquinas.append(
                    Maquina(id=i + 1)
                )

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

        de = DiferencialEvolutivo(
            processos,
            maquinas,
            tamanho_populacao=20,
            geracoes = geracoes,
            F=0.8,
            CR=0.9,
            arquivo = arquivo
        )

        inicio = time.perf_counter()

        melhor = de.executar()

        fim = time.perf_counter()

        mostrar_atribuicao(
            de.melhor_inicial,
            processos,
            maquinas,
            "ATRIBUIÇÃO INICIAL"
        )

        mostrar_atribuicao(
            melhor,
            processos,
            maquinas,
            "ATRIBUIÇÃO FINAL"
        )

        if arquivo.endswith("hard.txt"):
            print("\n================================")
            print("RESTRIÇÕES CONSIDERADAS")
            print("================================")
            print("Não-preempção: tarefas não são interrompidas")
            print("Precedências: tarefas são executadas somente após a conclusão de suas predecessoras")

        print("\n================================")
        print("RESULTADOS")
        print("================================")

        print(
            f"Makespan inicial: "
            f"{de.melhor_inicial.valor_objetivo:.0f}"
        )

        print(
            f"Makespan final: "
            f"{melhor.valor_objetivo:.0f}"
        )

        print(
            f"Tempo de execução: "
            f"{fim - inicio:.6f} segundos"
        )


if __name__ == "__main__":
    executar()