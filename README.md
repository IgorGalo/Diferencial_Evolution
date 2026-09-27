# Differential Evolution — Alocação de Tarefas em Máquinas Paralelas

Implementação de uma metaheurística baseada em **Differential Evolution (DE)** para resolver o problema de alocação de tarefas em máquinas paralelas, buscando minimizar o **makespan** — o tempo de término da máquina que finaliza por último.

O projeto foi desenvolvido para a disciplina de **Inteligência Artificial**, com base no conteúdo apresentado em aula sobre Evolução Diferencial.

## Problema

Dado um conjunto de tarefas com diferentes tempos de processamento e um conjunto de máquinas, cada tarefa deve ser atribuída a uma única máquina.

O objetivo é encontrar uma distribuição que minimize o makespan.
onde a carga de uma máquina é a soma dos tempos das tarefas atribuídas a ela.

O projeto utiliza três instâncias:

- **Easy** — 30 tarefas e 5 máquinas.
- **Medium** — 50 tarefas e 6 máquinas, com capacidades individuais de processamento.
- **Hard** — 40 tarefas e 5 máquinas, com restrições adicionais de precedência.

## Representação da solução

Cada indivíduo representa **uma solução completa de alocação**.

O cromossomo possui uma posição para cada tarefa:

```text
[2, 5, 1, 3, 2, ...]
```

Por exemplo:

```text
posição 1 → Tarefa 1 → Máquina 2
posição 2 → Tarefa 2 → Máquina 5
posição 3 → Tarefa 3 → Máquina 1
```

Assim:

- a dimensão `D` do indivíduo corresponde ao número de tarefas;
- cada gene representa a máquina atribuída à respectiva tarefa.

## Differential Evolution

O fluxo utilizado segue as principais etapas do DE:

```text
População inicial
        ↓
Mutação diferencial
        ↓
Crossover
        ↓
Avaliação
        ↓
Seleção
        ↓
Nova população
```

A mutação diferencial apresentada no material da disciplina é:

\[
V_i = X_r1 + F(X_r2 - X_r3)
\]

onde:

- `Xr1` é o vetor-base;
- `Xr2` e `Xr3` são indivíduos distintos;
- `F` é o fator de mutação;
- `V` é o vetor mutante.

Como o problema utiliza máquinas representadas por valores inteiros, a implementação utiliza uma etapa de **discretização** para converter os valores gerados pela mutação em identificadores de máquinas válidos.

## Adaptação para a instância Medium

A instância `medium` possui capacidades diferentes entre as máquinas.

Nesse caso, a mutação diferencial contínua pode gerar valores que, após a discretização, correspondam a máquinas incompatíveis com determinada tarefa.

Por isso, para a instância `medium`, é utilizada uma **mutação discreta adaptada**, mantendo a representação baseada em máquinas e respeitando as restrições de capacidade da tarefa.

Essa adaptação permite trabalhar com a natureza discreta do problema sem alterar a representação geral do indivíduo.

## Crossover

Após a mutação, o vetor-alvo e o vetor-mutante são combinados por crossover.

O parâmetro `CR` controla a probabilidade de uma posição do filho ser herdada do vetor-mutante.

Também é garantida pelo menos uma posição proveniente do vetor-mutante.

## Seleção

O problema é de minimização.

Para cada indivíduo, o candidato é comparado ao indivíduo-alvo, assim, uma solução candidata só substitui a solução atual quando possui makespan menor ou igual.

## Inicialização da população

A população é formada por soluções válidas.

Para instâncias com restrições de capacidade, é utilizado também um indivíduo gerado por uma heurística gulosa, que prioriza tarefas de maior duração e atribui cada tarefa à máquina elegível com menor carga atual.

Os demais indivíduos são gerados aleatoriamente respeitando as restrições disponíveis.

## Parâmetros

Os principais parâmetros utilizados pelo algoritmo são:

| Parâmetro | Descrição |
|---|---|
| `NP` | Tamanho da população |
| `F` | Fator de mutação |
| `CR` | Taxa de crossover |
| `geracoes` | Número máximo de gerações |

Exemplo de configuração:

```python
de = DiferencialEvolutivo(
    processos,
    maquinas,
    tamanho_populacao=20,
    geracoes=50,
    F=0.8,
    CR=0.9
)
```

## Execução

Certifique-se de possuir uma instalação compatível com Python 3.

Execute:

```bash
python Main.py
```

O programa solicita a instância desejada:

```text
1 - Fácil
2 - Médio
3 - Difícil
Ou 0 para Sair
```

Em seguida, informa-se a quantidade de gerações a ser executada.

Ao final, são apresentados:

- melhor solução encontrada;
- cromossomo;
- atribuição das tarefas por máquina;
- makespan inicial;
- makespan final;
- tempo de execução.

## Estrutura do projeto

Uma organização esperada do projeto é:

```text
.
├── Main.py
├── DiferencialEvolutivo.py
├── Representacao.py
├── FuncaoObjetivo.py
├── processo.py
├── Maquina.py
├── easy.txt
├── medium.txt
└── hard.txt
```

Dependendo da organização do repositório, os arquivos da implementação do DE podem estar dentro de um diretório próprio.

## Resultados de exemplo

Os resultados são estocásticos, portanto podem variar entre execuções.

Em execuções realizadas durante o desenvolvimento, foram observados, por exemplo:

| Instância | Makespan inicial | Makespan final |
|---|---:|---:|
| Easy | 53 | 45 |
| Medium | 176 | 173 |
| Hard | 185 | 165 |

Esses valores são apenas exemplos de execuções específicas e não representam necessariamente o resultado de todas as execuções.

Para a instância Easy, o valor mínimo possível é `44`, obtido pelo limite da carga total dividida entre as 5 máquinas e por uma distribuição que atinge esse limite.

Na instância Hard, o limite inferior pela carga total é `159`; além disso, a instância possui restrições de precedência que precisam ser consideradas na solução final.

## Observações

A representação utilizada é discreta, enquanto a formulação clássica do Differential Evolution foi originalmente apresentada para variáveis reais. Por isso, a implementação contém adaptações específicas para transformar os valores da mutação em máquinas válidas.

A escolha dos parâmetros (`NP`, `F`, `CR` e número de gerações) influencia diretamente a exploração do espaço de soluções e o tempo de execução.

Como o algoritmo utiliza operações aleatórias, recomenda-se executar cada instância mais de uma vez para comparar a variação dos resultados.

## Referência

Projeto desenvolvido para a disciplina de **Inteligência Artificial — UFSJ**, utilizando como referência o conteúdo apresentado em aula sobre **Evolução Diferencial (Differential Evolution)**.
