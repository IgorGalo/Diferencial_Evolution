from DE.processo import Processo
from DE.Maquina import Maquina
from DE.DiferencialEvolutivo import DiferencialEvolutivo

import os

print("Diretório atual:", os.getcwd())
print("Arquivos:", os.listdir())

arquivo = "DE_Discreto/easy.txt"

processos = Processo().lerProcessos(arquivo)

maquinas = []

for i in range(5):
    maquinas.append(Maquina(id=i + 1))
de = DiferencialEvolutivo(
    processos,
    maquinas,
    tamanho_populacao=20,
    geracoes=50,
    F=0.8,
    CR=0.9
)

melhor = de.executar()

