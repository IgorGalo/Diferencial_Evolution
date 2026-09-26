class Processo:
    def __init__(self, id=None, tempo=None, prioridades=None):
        self.id = id
        self.tempo = tempo
        
        if prioridades is None:
            self.prioridades = []
        else:
            self.prioridades = prioridades

    def lerProcessos(self, nome_arquivo):
        lendo_tabela = False
        processos = []
        with open(nome_arquivo, 'r', encoding = 'utf-8') as f:
            linhas = f.readlines()
            for linha in linhas:
                linha_limpa = linha.strip()

                if (not linha_limpa) and (lendo_tabela):
                    break

                elif linha_limpa.startswith("ID_Tarefa"):
                    lendo_tabela = True
                    continue

                elif lendo_tabela:
                    dados = linha_limpa.split()
                    
                    if len(dados) >= 2:
                        processos.append(Processo(
                            id=dados[0],
                            tempo=dados[1]
                        ))   
            return processos

    def toString(self):
        return f"Processo: {self.id} com Tempo de Processamento {self.tempo}" 