class Maquina:
    def __init__(self, id=None, capacidade=None, processos = None):
        self.id = id
        self.capacidade = capacidade
        
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
                            maquinas.append(Maquina(dados[0],dados[1]))   

            return maquinas

    def toString(self):
        return f"Maquina: {self.id} com Capacidade de Processamento = {self.capacidade}" 