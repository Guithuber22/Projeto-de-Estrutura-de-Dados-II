"""Experimento de ordenação para arrays e listas simplesmente ligadas."""

from __future__ import annotations

import argparse
import csv
import random
import time
from dataclasses import dataclass
from pathlib import Path


TAMANHOS = (500, 1000, 3000, 5000, 10000)
CENARIOS = ("medio", "melhor", "pior")


@dataclass
class No:
    valor: int
    proximo: No | None = None


def lista_ligada(valores):
    inicio = fim = None
    for valor in valores:
        novo = No(int(valor))
        if fim is None:
            inicio = novo
        else:
            fim.proximo = novo
        fim = novo
    return inicio


def valores_lista(inicio):
    resultado = []
    while inicio is not None:
        resultado.append(inicio.valor)
        inicio = inicio.proximo
    return resultado


def bubble_array(a):
    comparacoes = trocas = 0
    for fim in range(len(a) - 1, 0, -1):
        alterou = False
        for i in range(fim):
            comparacoes += 1
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                trocas += 1
                alterou = True
        if not alterou:
            break
    return comparacoes, trocas


def selection_array(a):
    comparacoes = trocas = 0
    for i in range(len(a) - 1):
        minimo = i
        for j in range(i + 1, len(a)):
            comparacoes += 1
            if a[j] < a[minimo]:
                minimo = j
        if minimo != i:
            a[i], a[minimo] = a[minimo], a[i]
            trocas += 1
    return comparacoes, trocas


def insertion_array(a):
    comparacoes = movimentacoes = 0
    for i in range(1, len(a)):
        chave = a[i]
        j = i - 1
        while j >= 0:
            comparacoes += 1
            if a[j] <= chave:
                break
            a[j + 1] = a[j]
            movimentacoes += 1
            j -= 1
        a[j + 1] = chave
    return comparacoes, movimentacoes


def bubble_ligada(inicio):
    comparacoes = trocas = 0
    if inicio is None:
        return comparacoes, trocas
    limite = None
    while inicio.proximo is not limite:
        atual = inicio
        alterou = False
        while atual.proximo is not limite:
            comparacoes += 1
            if atual.valor > atual.proximo.valor:
                atual.valor, atual.proximo.valor = atual.proximo.valor, atual.valor
                trocas += 1
                alterou = True
            atual = atual.proximo
        limite = atual
        if not alterou:
            break
    return comparacoes, trocas


def selection_ligada(inicio):
    comparacoes = trocas = 0
    atual = inicio
    while atual is not None:
        minimo = atual
        busca = atual.proximo
        while busca is not None:
            comparacoes += 1
            if busca.valor < minimo.valor:
                minimo = busca
            busca = busca.proximo
        if minimo is not atual:
            atual.valor, minimo.valor = minimo.valor, atual.valor
            trocas += 1
        atual = atual.proximo
    return comparacoes, trocas


def insertion_ligada(inicio):
    """Insere cada chave por deslocamento dos valores nos nós existentes."""
    comparacoes = movimentacoes = 0
    atual = inicio
    while atual is not None and atual.proximo is not None:
        chave = atual.proximo.valor
        busca = inicio
        anterior = None
        while busca is not atual.proximo:
            comparacoes += 1
            if busca.valor > chave:
                break
            anterior = busca
            busca = busca.proximo
        if busca is not atual.proximo:
            # Desloca valores à direita usando um valor temporário.
            carregado = chave
            while busca is not atual.proximo:
                carregado, busca.valor = busca.valor, carregado
                movimentacoes += 1
                busca = busca.proximo
            busca.valor = carregado
            movimentacoes += 1
        atual = atual.proximo
    return comparacoes, movimentacoes


ALGORITMOS = {
    ("bubble", "array"): bubble_array,
    ("selection", "array"): selection_array,
    ("insertion", "array"): insertion_array,
    ("bubble", "ligada"): bubble_ligada,
    ("selection", "ligada"): selection_ligada,
    ("insertion", "ligada"): insertion_ligada,
}


def gera_dados(tamanho, rng):
    # Equivalente aos cenários definidos no enunciado, com semente fixa.
    medio = [rng.randrange(tamanho * tamanho) for _ in range(tamanho)]
    melhor = sorted(medio)
    pior = melhor[::-1]
    return {"medio": medio, "melhor": melhor, "pior": pior}


def executar(tamanhos, saida, semente):
    saida.mkdir(parents=True, exist_ok=True)
    linhas = []
    rng = random.Random(semente)
    for tamanho in tamanhos:
        dados = gera_dados(tamanho, rng)
        for cenario in CENARIOS:
            esperado = sorted(dados[cenario])
            for algoritmo in ("bubble", "selection", "insertion"):
                for estrutura in ("array", "ligada"):
                    entrada = (dados[cenario].copy() if estrutura == "array"
                               else lista_ligada(dados[cenario]))
                    inicio = time.perf_counter()
                    comparacoes, movimentacoes = ALGORITMOS[algoritmo, estrutura](entrada)
                    tempo = time.perf_counter() - inicio
                    obtido = entrada if estrutura == "array" else valores_lista(entrada)
                    if obtido != esperado:
                        raise AssertionError(f"Falha: {algoritmo}, {estrutura}, {cenario}, {tamanho}")
                    linha = dict(tamanho=tamanho, cenario=cenario, algoritmo=algoritmo,
                                 estrutura=estrutura, tempo_s=f"{tempo:.6f}",
                                 comparacoes=comparacoes, movimentacoes=movimentacoes)
                    linhas.append(linha)
                    print(f"{tamanho:5} {cenario:6} {algoritmo:9} {estrutura:6} "
                          f"{tempo:8.3f}s {comparacoes:10} comp {movimentacoes:10} mov", flush=True)
    with (saida / "resultados.csv").open("w", newline="", encoding="utf-8") as arq:
        escritor = csv.DictWriter(arq, fieldnames=list(linhas[0]))
        escritor.writeheader()
        escritor.writerows(linhas)
    criar_graficos(linhas, saida)
    return linhas


def criar_graficos(linhas, saida):
    """Nove gráficos SVG de barras, sem dependência de biblioteca gráfica."""
    cores = {"bubble/array": "#2563eb", "bubble/ligada": "#93c5fd",
             "selection/array": "#dc2626", "selection/ligada": "#fca5a5",
             "insertion/array": "#16a34a", "insertion/ligada": "#86efac"}
    for cenario in CENARIOS:
        grupo = [x for x in linhas if x["cenario"] == cenario]
        for campo, rotulo in (("tempo_s", "Tempo (s)"),
                              ("comparacoes", "Comparações"),
                              ("movimentacoes", "Trocas / movimentações")):
            maximo = max(float(x[campo]) for x in grupo) or 1
            partes = ['<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="610" viewBox="0 0 1180 610">',
                      '<rect width="1180" height="610" fill="white"/>',
                      f'<text x="70" y="38" font-family="Arial" font-size="22">{rotulo} — caso {cenario}</text>',
                      '<line x1="75" y1="510" x2="1140" y2="510" stroke="#333"/>']
            tamanhos = sorted({x["tamanho"] for x in grupo})
            for indice, tamanho in enumerate(tamanhos):
                x_base = 95 + indice * 210
                subgrupo = [x for x in grupo if x["tamanho"] == tamanho]
                for j, linha in enumerate(subgrupo):
                    chave = f'{linha["algoritmo"]}/{linha["estrutura"]}'
                    altura = 400 * float(linha[campo]) / maximo
                    x = x_base + j * 26
                    partes.append(f'<rect x="{x}" y="{510-altura:.2f}" width="21" height="{altura:.2f}" fill="{cores[chave]}"/>')
                partes.append(f'<text x="{x_base+45}" y="535" font-family="Arial" font-size="14">{tamanho}</text>')
            partes.append(f'<text x="75" y="570" font-family="Arial" font-size="13">Máximo: {maximo:,.3f}</text>')
            for i, (chave, cor) in enumerate(cores.items()):
                x, y = 330 + (i % 3) * 260, 558 + (i // 3) * 22
                partes.append(f'<rect x="{x}" y="{y-11}" width="13" height="13" fill="{cor}"/>')
                partes.append(f'<text x="{x+19}" y="{y}" font-family="Arial" font-size="13">{chave}</text>')
            partes.append('</svg>')
            (saida / f"{cenario}_{campo}.svg").write_text("\n".join(partes), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tamanhos", type=int, nargs="+", default=TAMANHOS)
    parser.add_argument("--semente", type=int, default=2026)
    parser.add_argument("--saida", type=Path, default=Path("resultados"))
    args = parser.parse_args()
    executar(args.tamanhos, args.saida, args.semente)
