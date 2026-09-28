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

        with open(nome_arquivo, 'r', encoding='utf-8') as f:
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

                        id_processo = dados[0]
                        tempo = int(dados[1])
                        prioridades = []

                        # Verifica se a linha possui prioridades
                        if "Prioridade:" in linha_limpa:

                            inicio = linha_limpa.find("[")
                            fim = linha_limpa.find("]")

                            if inicio != -1 and fim != -1:
                                texto_prioridades = (
                                    linha_limpa[inicio + 1:fim]
                                )

                                if texto_prioridades.strip():
                                    prioridades = [
                                        int(x.strip())
                                        for x in texto_prioridades.split(",")
                                    ]

                        processos.append(
                            Processo(
                                id_processo,
                                tempo,
                                prioridades
                            )
                        )

        return processos

    def toString(self):
        return (
            f"Processo: {self.id} "
            f"com Tempo de Processamento {self.tempo}"
        )