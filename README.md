# Differential Evolution — Alocação de Tarefas em Máquinas Paralelas

Implementação de uma metaheurística baseada em **Differential Evolution (DE)** para resolver o problema de alocação de tarefas em máquinas paralelas, buscando minimizar o **makespan** — o tempo em que a última máquina termina sua execução.

O projeto foi desenvolvido para a disciplina de **Inteligência Artificial**, com base no conteúdo apresentado em aula sobre **Evolução Diferencial**.

## Problema

Dado um conjunto de tarefas com diferentes tempos de processamento e um conjunto de máquinas, cada tarefa deve ser atribuída a uma única máquina.

O objetivo é encontrar uma distribuição que minimize o makespan.

O projeto utiliza três instâncias, com diferentes níveis de dificuldade:

- **Easy** — 30 tarefas e 5 máquinas idênticas.
- **Medium** — 50 tarefas e 6 máquinas com capacidades diferentes.
- **Hard** — 40 tarefas e 5 máquinas idênticas, com restrições de precedência e não-preempção.

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
V_i = X_{r1} + F(X_{r2} - X_{r3})
\]

onde:

- `Xr1` é o vetor-base;
- `Xr2` e `Xr3` são indivíduos distintos;
- `F` é o fator de mutação;
- `V` é o vetor mutante.

Como o problema utiliza máquinas representadas por valores inteiros, a implementação utiliza **discretização** para converter os valores gerados pela mutação em identificadores de máquinas válidos.

## Adaptação para a instância Medium

A instância `medium` possui máquinas com capacidades diferentes. As capacidades utilizadas são limites para o **tempo individual da tarefa** que cada máquina pode executar.

Assim, uma tarefa somente pode ser atribuída a uma máquina quando:

```text
tempo da tarefa ≤ capacidade da máquina
```

Como a mutação diferencial contínua pode gerar valores que, após a discretização, resultem em máquinas incompatíveis com determinadas tarefas, a instância `medium` utiliza uma **mutação discreta adaptada**.

Além disso, após o crossover é aplicado um procedimento de **reparo**, que substitui atribuições inválidas por máquinas que conseguem executar a tarefa.

A população inicial também inclui uma solução gerada por uma heurística gulosa, que prioriza tarefas de maior duração e as atribui a máquinas elegíveis com menor carga atual.

## Adaptação para a instância Hard

A instância `hard` adiciona duas restrições ao problema:

- **não-preempção** — uma tarefa, uma vez iniciada, deve ser concluída sem interrupção;
- **precedência** — algumas tarefas só podem começar após a conclusão de determinadas tarefas predecessoras.

As relações de precedência são **lidas diretamente do arquivo `hard.txt`**, sem serem codificadas manualmente no algoritmo.

Durante a avaliação da solução, o programa transforma essas relações em predecessoras e monta o cronograma respeitando:

1. o momento em que a máquina escolhida fica disponível;
2. o momento em que todas as predecessoras da tarefa terminam.

Assim, o início de uma tarefa é determinado por:

```text
início = max(máquina disponível, fim das predecessoras)
```

Por esse motivo, na instância `hard`, o makespan pode ser maior que a maior soma simples das cargas das máquinas, devido aos períodos de espera causados pelas precedências.

## Crossover

Após a mutação, o vetor-alvo e o vetor-mutante são combinados por crossover binomial.

O parâmetro `CR` controla a probabilidade de uma posição do filho ser herdada do vetor-mutante.

Também é garantida pelo menos uma posição proveniente do vetor-mutante.

## Seleção

O problema é de minimização.

Para cada indivíduo, o candidato é comparado ao indivíduo-alvo. Assim, uma solução candidata substitui a solução atual quando possui makespan menor ou igual:

```python
candidato.valor_objetivo <= alvo.valor_objetivo
```

O terminal também informa a quantidade de candidatos **aceitos** em cada geração, isto é, quantos candidatos substituíram seus respectivos indivíduos-alvo.

## Inicialização da população

Para as instâncias sem restrições de capacidade, a população é formada por soluções geradas aleatoriamente.

Na instância `medium`, além dos indivíduos aleatórios, é incluído um indivíduo gerado por uma heurística gulosa, construído respeitando as capacidades das máquinas.

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
    geracoes=1000,
    F=0.8,
    CR=0.9
)
```

## Execução

Certifique-se de possuir uma instalação compatível com **Python 3**.

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

Durante a execução, o terminal apresenta a evolução do melhor makespan e a quantidade de candidatos aceitos em cada geração.

Ao final, são apresentados:

- melhor solução encontrada;
- cromossomo;
- atribuição das tarefas por máquina;
- makespan inicial;
- makespan final;
- tempo de execução.

Na instância `hard`, também é apresentada uma indicação de que as restrições de não-preempção e precedência foram consideradas.

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

Os resultados são estocásticos e podem variar entre execuções.

Em uma execução com **1000 gerações**, foram obtidos os seguintes resultados:

| Instância | Makespan inicial | Makespan final | Tempo de execução |
|---|---:|---:|---:|
| Easy | 56 | **44** | 0,620001 s |
| Medium | 176 | **173** | 0,996069 s |
| Hard | 186 | **168** | 10,821221 s |

### Easy

A solução final possui cargas:

```text
M1 = 42
M2 = 43
M3 = 44
M4 = 43
M5 = 44
```

Logo:

\[
C_{max} = 44
\]

A soma total dos tempos de processamento é 216, produzindo o limite inferior:

\[
\left\lceil \frac{216}{5} \right\rceil = 44
\]

Como a solução encontrada atinge esse limite, `44` é o menor makespan possível para essa instância.

### Medium

A solução final apresentou cargas:

```text
M1 = 155
M2 = 170
M3 = 173
M4 = 93
M5 = 173
M6 = 140
```

Logo:

\[
C_{max} = 173
\]

A solução respeita as capacidades individuais das máquinas e `173` corresponde ao menor makespan possível para a instância sob essa interpretação das capacidades.

### Hard

A solução final apresentou cargas de processamento por máquina:

```text
M1 = 162
M2 = 168
M3 = 162
M4 = 132
M5 = 168
```

O makespan calculado pelo cronograma, considerando as precedências, foi:

\[
C_{max} = 168
\]

A solução encontrada é válida segundo as restrições de precedência e não-preempção. O valor `168` é apresentado como o melhor resultado observado nessa execução; este README não o considera necessariamente o ótimo global da instância.

## Observações

A representação utilizada é discreta, enquanto a formulação clássica do Differential Evolution foi apresentada para variáveis reais. Por isso, a implementação utiliza adaptações para transformar os valores produzidos pela mutação em identificadores de máquinas válidos.

A instância `medium` utiliza uma mutação discreta específica e um mecanismo de reparo para lidar com as restrições de capacidade.

A instância `hard` utiliza uma avaliação específica que constrói o cronograma respeitando as relações de precedência lidas do arquivo e a não-preempção.

A escolha dos parâmetros (`NP`, `F`, `CR` e número de gerações) influencia a exploração do espaço de soluções e o tempo de execução.

Como o algoritmo utiliza operações aleatórias, recomenda-se executar cada instância mais de uma vez para observar a variação dos resultados.

## Referência

Projeto desenvolvido para a disciplina de **Inteligência Artificial — UFSJ**, utilizando como referência o conteúdo apresentado em aula sobre **Evolução Diferencial (Differential Evolution)**.
