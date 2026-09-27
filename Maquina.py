class Maquina:
    def __init__(self, id=None, capacidade=None, processos =None):
        self.id = id
        self.capacidade = capacidade
        if processos is None:
            self.processos = []
        else:
            self.prioridades = processos
        
    # def lerMaquinas(self, nome_arquivo):
    #     lendo_tabela = False
    #     maquinas = []
    #     with open(nome_arquivo, 'r', encoding = 'utf-8') as f:
    #         linhas = f.readlines()

    #         for linha in linhas:
    #             linha_limpa = linha.strip()
    #             if (not linha_limpa) and (lendo_tabela):
    #                 break
    #             elif linha_limpa.startswith("Máquina"):
    #                 lendo_tabela = True
    #                 continue
    #             elif lendo_tabela:
    #                 dados = linha_limpa.split()
    #                 if len(dados) >= 2:
    #                     maquinas.append(Maquina(int(dados[0], int(dados[1]))))   

    #         return maquinas

    def lerMaquinas(self, nome_arquivo):
        lendo_tabela = False
        maquinas = []
        with open(nome_arquivo, 'r', encoding='utf-8') as f:

            for linha in f:
                linha_limpa = linha.strip()
                # Detecta o cabeçalho da tabela de máquinas
                if linha_limpa.startswith("Máquina") and "Capacidade" in linha_limpa:
                    lendo_tabela = True
                    continue
                # Depois do cabeçalho, lê:
                # 1 18
                # 2 22
                # 3 25
                # ...
                if lendo_tabela:
                    if not linha_limpa:
                        continue
                    dados = linha_limpa.split()
                    if len(dados) >= 2:
                        try:
                            id_maquina = int(dados[0])
                            capacidade = int(dados[1])
                            maquinas.append(
                                Maquina(id_maquina, capacidade)
                            )
                        except ValueError:
                            # Chegou em outra parte do arquivo
                            break

        return maquinas

    def custo(self):
        custoTotal = 0
        for processo in self.processos:
            custoTotal += processo.tempo
        return custoTotal

    def toString(self):
        processos = ""

        for processo in self.processos:
            processos += processo.toString() + "\n"

        return f"""\n--        
Maquina: {self.id} com Capacidade de Processamento = {self.capacidade}
Processos Associados:
{processos}Tempo total: {self.custo()}"""