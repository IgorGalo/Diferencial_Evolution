class Maquina:
    def __init__(self, id=None, capacidade=None, processos =None):
        self.id = id
        self.capacidade = capacidade
        if processos is None:
            self.processos = []
        else:
            self.prioridades = processos
        
    def lerMaquinas(self, nome_arquivo):
        lendo_tabela = False
        maquinas = []
        with open(nome_arquivo, 'r', encoding = 'utf-8') as f:
            linhas = f.readlines()
            for linha in linhas:
                linha_limpa = linha.strip()

                if (not linha_limpa) and (lendo_tabela):
                    break

                elif linha_limpa.startswith("Máquina"):
                    lendo_tabela = True
                    continue

                elif lendo_tabela:
                    dados = linha_limpa.split()
                        
                    if len(dados) >= 2:
                        maquinas.append(Maquina(dados[0], int(dados[1])))   

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