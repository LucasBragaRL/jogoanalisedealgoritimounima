import os
import math
import itertools

class Item:
    def __init__(self, nome, valor, x, y):
        self.nome = nome
        self.valor = valor
        self.x = x
        self.y = y

class Inventario:
    def __init__(self):
        self.itens = []

    def adicionar(self, item):
        self.itens.append(item)

    def listar(self):
        if not self.itens:
            return "Vazio"
        return ", ".join([f"{i.nome} ($ {i.valor})" for i in self.itens])

def calcular_distancia(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def tsp_exato(pos_inicial, lista_itens):
    if not lista_itens:
        return []

    melhor_rota = None
    menor_distancia = float('inf')

    for perm in itertools.permutations(lista_itens):
        dist_atual = 0
        p_atual = pos_inicial

        for item in perm:
            dist_atual += calcular_distancia(p_atual, (item.x, item.y))
            p_atual = (item.x, item.y)

        dist_atual += calcular_distancia(p_atual, pos_inicial)

        if dist_atual < menor_distancia:
            menor_distancia = dist_atual
            melhor_rota = perm

    return list(melhor_rota)

def tsp_heuristico(pos_inicial, lista_itens):
    nao_visitados = lista_itens.copy()
    pos_atual = pos_inicial
    rota = []

    while nao_visitados:
        item_proximo = min(
            nao_visitados,
            key=lambda item: calcular_distancia(
                pos_atual,
                (item.x, item.y)
            )
        )

        rota.append(item_proximo)
        pos_atual = (item_proximo.x, item_proximo.y)
        nao_visitados.remove(item_proximo)

    return rota

def obter_rota_tsp(pos_inicial, lista_itens):
    if len(lista_itens) <= 15:
        return tsp_exato(pos_inicial, lista_itens)
    return tsp_heuristico(pos_inicial, lista_itens)

def caminho_maximo(pos_inicial, lista_itens):
    if not lista_itens:
        return []

    melhor_rota = None
    maior_distancia = -1

    for perm in itertools.permutations(lista_itens):
        dist_atual = 0
        p_atual = pos_inicial

        for item in perm:
            dist_atual += calcular_distancia(
                p_atual,
                (item.x, item.y)
            )
            p_atual = (item.x, item.y)

        if dist_atual > maior_distancia:
            maior_distancia = dist_atual
            melhor_rota = perm

    return list(melhor_rota)

def fluxo_maximo(itens):
    return len(itens)

def fluxo_minimo(itens):
    return 1 if itens else 0

def cobertura_pequena(itens):
    return itens[:max(1, len(itens)//2)]

def cobertura_grande(itens):
    return itens

def gerar_circuito(base, rota):
    circuito = [base]

    for item in rota:
        circuito.append((item.x, item.y))

    circuito.append(base)

    return circuito

def quicksort(arr):
    if len(arr) <= 1:
        return arr

    pivo = arr[len(arr)//2].valor

    esq = [x for x in arr if x.valor > pivo]
    meio = [x for x in arr if x.valor == pivo]
    dir = [x for x in arr if x.valor < pivo]

    return quicksort(esq) + meio + quicksort(dir)

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def renderizar_mapa(player_pos, itens, tamanho=10):
    grid = [['. ' for _ in range(tamanho)] for _ in range(tamanho)]

    for idx, item in enumerate(itens):
        if 0 <= item.x < tamanho and 0 <= item.y < tamanho:
            grid[item.y][item.x] = f"S{idx+1}"

    grid[player_pos[1]][player_pos[0]] = 'R '

    print("\n=== SUCATEIRO ESPACIAL ===")

    for linha in grid:
        print(" " * 4 + "".join(linha))

    print("==========================")

def jogar():
    player_pos = [0, 0]

    inventario = Inventario()

    sucatas = [
        Item("Painel Solar Titan", 150, 3, 2),
        Item("Placa Microcontrolada", 90, 7, 1),
        Item("Bateria de Ions-Litio", 210, 4, 7),
        Item("Reator de Fusao Quebrado", 450, 8, 8)
    ]

    msg = "Explore o mapa."
    rota_sugerida = []

    while True:
        limpar_tela()

        renderizar_mapa(player_pos, sucatas)

        print(f"\nStatus: {msg}")
        print(f"Posição: {player_pos}")
        print(f"Inventário: {inventario.listar()}")

        if rota_sugerida:
            print("\nROTA ATUAL:")

            for item in rota_sugerida:
                print(
                    f" -> {item.nome} "
                    f"({item.x},{item.y})"
                )

        print("\nMOVIMENTO")
        print("W A S D")

        print("\nALGORITMOS")
        print("T = Caminho Mínimo")
        print("Y = Caminho Máximo")
        print("F = Fluxo Máximo")
        print("G = Fluxo Mínimo")
        print("C = Cobertura Pequena")
        print("V = Cobertura Grande")
        print("R = Circuito")
        print("O = QuickSort")
        print("Q = Sair")

        inp = input("\nComando: ").lower().strip()

        msg = ""

        if inp == 'q':
            break

        elif inp == 'w' and player_pos[1] > 0:
            player_pos[1] -= 1

        elif inp == 's' and player_pos[1] < 9:
            player_pos[1] += 1

        elif inp == 'a' and player_pos[0] > 0:
            player_pos[0] -= 1

        elif inp == 'd' and player_pos[0] < 9:
            player_pos[0] += 1

        elif inp == 't':
            rota_sugerida = obter_rota_tsp(
                tuple(player_pos),
                sucatas
            )

            msg = "Caminho mínimo calculado."

        elif inp == 'y':
            rota_sugerida = caminho_maximo(
                tuple(player_pos),
                sucatas
            )

            msg = "Caminho máximo calculado."

        elif inp == 'f':
            msg = f"Fluxo máximo = {fluxo_maximo(sucatas)}"

        elif inp == 'g':
            msg = f"Fluxo mínimo = {fluxo_minimo(sucatas)}"

        elif inp == 'c':
            cob = cobertura_pequena(sucatas)

            msg = (
                f"Cobertura pequena: "
                f"{len(cob)} pontos"
            )

        elif inp == 'v':
            cob = cobertura_grande(sucatas)

            msg = (
                f"Cobertura grande: "
                f"{len(cob)} pontos"
            )

        elif inp == 'r':
            if rota_sugerida:
                circuito = gerar_circuito(
                    (0, 0),
                    rota_sugerida
                )

                msg = (
                    f"Circuito criado com "
                    f"{len(circuito)} vértices."
                )
            else:
                msg = (
                    "Execute T ou Y primeiro."
                )

        elif inp == 'o':
            if inventario.itens:
                inventario.itens = quicksort(
                    inventario.itens
                )

                msg = (
                    "Inventário ordenado "
                    "com QuickSort."
                )
            else:
                msg = "Inventário vazio."

        else:
            msg = "Comando inválido."

        for item in sucatas[:]:
            if (
                item.x == player_pos[0]
                and item.y == player_pos[1]
            ):
                inventario.adicionar(item)
                sucatas.remove(item)

                rota_sugerida = []

                msg = (
                    f"Sucata coletada: "
                    f"{item.nome}"
                )

if __name__ == "__main__":
    jogar()
