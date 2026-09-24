class processo:
    def __init__(self, id, tempo):
        self.id = id
        self.tempo = tempo

    """def __init__(self, id, tempo, prioridades):
            self.id = id
            self.tempo = tempo
            self.prioridades = []"""

    def leitura():
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

    def toString(self):
        return f"Processo: {self.id} com Tempo de Processamento {self.tempo}" 