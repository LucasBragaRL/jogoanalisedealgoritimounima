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
        item_proximo = min(nao_visitados, key=lambda item: calcular_distancia(pos_atual, (item.x, item.y)))
        rota.append(item_proximo)
        pos_atual = (item_proximo.x, item_proximo.y)
        nao_visitados.remove(item_proximo)
    return rota

def obter_rota_tsp(pos_inicial, lista_itens):
    if len(lista_itens) <= 15:
        return tsp_exato(pos_inicial, lista_itens)
    else:
        return tsp_heuristico(pos_inicial, lista_itens)

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivo = arr[len(arr) // 2].valor
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
    
    print("\n=== SUCATEIRO ESPACIAL: MAPA DE NAVEGAÇÃO ===")
    for linha in grid:
        print(" " * 4 + "".join(linha))
    print("==============================================")
    print("  R: Seu Robô  |  S1, S2, S3, S4: Sucatas Espalhadas\n")

def jogar():
    player_pos = [0, 0]
    inventario = Inventario()
    sucatas = [
        Item("Painel Solar Titan", 150, 3, 2),
        Item("Placa Microcontrolada", 90, 7, 1),
        Item("Bateria de Ions-Litio", 210, 4, 7),
        Item("Reator de Fusao Quebrado", 450, 8, 8)
    ]
    
    msg = "Comandos validados. Inicie a exploração do quadrante."
    rota_sugerida = []
    
    while True:
        limpar_tela()
        renderizar_mapa(player_pos, sucatas)
        
        print(f"📡 Radar Status: {msg}")
        print(f"📍 Coordenadas do Robô: {player_pos}")
        print(f"🎒 Inventário: [ {inventario.listar()} ]")
        
        if rota_sugerida:
            print("\n[RADAR TSP ATIVO] Rota Ótima Calculada:")
            passos = [f"{item.nome}({item.x},{item.y})" for item in rota_sugerida]
            print("  Ponto Inicial -> " + " -> ".join(passos) + " -> Retorno Base(0,0)")
            
        print("\nControles: W (Cima) | A (Esquerda) | S (Baixo) | D (Direita)")
        print("Ações:     T (Ativar Radar TSP) | O (Ordenar Inventário via QuickSort) | Q (Sair)")
        
        inp = input("\nEscolha uma ação e tecle Enter: ").strip().lower()
        msg = ""
        
        if inp == 'q':
            print("\nSessão encerrada pelo piloto.")
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
            if sucatas:
                rota_sugerida = obter_rota_tsp(tuple(player_pos), sucatas)
                msg = f"TSP executado com sucesso para n={len(sucatas)}."
            else:
                msg = "Varredura completa. Sem alvos para o TSP."
        elif inp == 'o':
            if inventario.itens:
                inventario.itens = quicksort(inventario.itens)
                msg = "QuickSort aplicado! Inventário ordenado por maior valor."
            else:
                msg = "Falha: Inventário vazio impossibilita ordenação."
        else:
            msg = "Comando desconhecido ou colisão com as bordas."
            
        for item in sucatas[:]:
            if item.x == player_pos[0] and item.y == player_pos[1]:
                inventario.adicionar(item)
                sucatas.remove(item)
                msg = f"Sucesso: {item.nome} integrado ao armazenamento!"
                rota_sugerida = []

if __name__ == '__main__':
    jogar()