# Estruturas de Dados II — ordenação simples
Alunos: Guilherme de Almeida e Castro - 5170584
       / Wanderson Santos Lemos - 5170227

## Como executar

Requer Python 3.10 ou superior; não há pacotes externos.

```bash
python ordenacao.py
```

O comando testa os tamanhos 500, 1.000, 3.000, 5.000 e 10.000, nos casos médio, melhor e pior, para Bubble Sort, Selection Sort e Insertion Sort em array e lista simplesmente ligada. A saída fica em `resultados/resultados.csv` e em nove gráficos SVG de barras (um para cada combinação de cenário e métrica). Para um teste rápido:

```bash
python ordenacao.py --tamanhos 10 30 --saida teste
```

Os dados aleatórios seguem a faixa `0` a `size*size - 1` do enunciado. A semente `2026` torna a amostra reproduzível; use `--semente NUMERO` para mudá-la. Cada algoritmo recebe uma cópia dos mesmos valores. A saída ordenada é verificada contra `sorted` em todas as execuções.

## Critério de contagem

- **Comparação:** uma comparação entre valores, sem incluir testes de índices ou ponteiros.
- **Troca/movimentação:** em Bubble e Selection, uma troca de valores conta como 1; em Insertion, cada deslocamento de um valor entre posições ou nós conta como 1. A retirada e a colocação da chave no array não são contadas; na lista, a colocação final após o deslocamento é contada. Por isso, o número de Insertion não representa a mesma operação física dos outros dois métodos.
- **Tempo:** medido apenas durante a ordenação. A construção da lista, a cópia dos dados e a validação ficam fora do cronômetro.
- A lista é simplesmente ligada. Para comparar os algoritmos sobre a mesma estrutura, os nós permanecem no lugar e seus valores são trocados ou deslocados.

## Respostas:

### 1. Qual algoritmo teve mais comparações?

**Selection Sort** fez sempre `n(n−1)/2` comparações: 49.995.000 com 10.000 valores, independentemente da ordem inicial e da estrutura. Empatou com Bubble no pior caso e com Insertion em array no pior caso. Na lista ligada, o Insertion implementado também empatou com Selection no melhor caso, pois procura a posição de inserção a partir do início. Portanto, não há um único vencedor em todos os cenários; Selection é o método com maior contagem constante e os empates dependem do caso.

No caso médio de 10.000 valores, Selection fez 49.995.000 comparações, Bubble fez 49.986.089, Insertion em array fez 25.376.466 e Insertion em lista ligada fez 24.638.512.

### 2. Qual algoritmo fez mais trocas?

**Bubble Sort** concentrou mais trocas reais de pares, empatando em quantidade com os deslocamentos do Insertion em array quando os dados estão em ordem inversa. Com 10.000 valores no pior caso, ambos registraram 49.995.000 operações. Selection fez apenas 5.000 trocas. O Insertion em lista ligada registrou 50.004.999 movimentações nesse caso, pois sua inserção inclui uma gravação adicional por chave deslocada; pelo critério de **movimentações totais** usado no CSV, ele é o maior. No caso médio, Bubble fez 25.366.480 trocas, contra 9.992 do Selection; Insertion em array fez 25.366.480 deslocamentos e em lista ligada fez 25.376.472 movimentações.

### 3. Existe relação entre o número de trocas e a eficiência?

**Sim, mas a quantidade de trocas sozinha não determina o tempo.** No caso médio de 10.000 valores em array, Selection fez 9.992 trocas e levou 2,435 s; Bubble fez 25.366.480 trocas e levou 5,451 s. Esse par sugere que muitas trocas podem custar tempo. Porém Selection manteve 49.995.000 comparações mesmo no melhor caso, enquanto Bubble e Insertion em array terminaram rapidamente com apenas 9.999 comparações e nenhuma troca ou deslocamento. A estrutura de dados e a forma de acesso também influenciam o tempo: no caso médio de 10.000 valores, Bubble levou 5,451 s em array e 7,591 s em lista ligada, embora as contagens tenham sido iguais.
