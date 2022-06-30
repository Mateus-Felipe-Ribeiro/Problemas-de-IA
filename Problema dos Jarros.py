"""
------------------------------------------------------------------------------------------------------------------------------
                                        Trabalho - Primeiro bimestre - parte 1

                                        GRUPO 8: 
                                                Mateus F. Ribeiro       RA: 17243526
                                                Matheus H.B. Miranda    RA: 16022526
                                                Paulo M.H. Filho        RA: 16094626

------------------------------------------------------------------------------------------------------------------------------

2) Adaptar o problema dos jarros d’água para três jarros (6, 4 e 3 litros). Use os seguintes métodos de busca:

a) busca em largura
b) busca em profundidade. 

O problema inicia com os jarros vazios e o objetivo é atingir uma configuração especificada pelo usuário (valor 1 ponto).
"""

from collections import deque

"""Iniciamos com os jarros vazios"""
estado_inicial = (0,0,0) 

"""Cria-se uma classe para representar os nós da árvore de busca, inicializamos com um estado e um estado pai"""

class Node:
    def __init__(self,state,parent):
        self.state = state
        self.parent = parent

	
    """
    Função que verifica se o nó é um nó objetivo.

    Usuario define qual é o objetivo!
    """
    def goal_achieved(self):
        return (self.state[0] == 4)


    """
    Função chamada quando um nó é o objetivo, para imprimir o caminho da solução do início até ele.
    """

    def trace_solution(self):
        if (self.parent is not None):
            self.parent.trace_solution()
        print(self.state)



    """
    Função que retorna os possíveis nós filhos de um nó, ou seja, os nós dos estados seguintes dependendo das ações que podem ser executadas no estado atual.
    """
    
    def children(self):
        children = []
        
        j1 = self.state[0]
        j2 = self.state[1]
        j3 = self.state[2]
		
        if (j1 == 0): # se j1 vazia
            children.append(Node((6, j2, j3), self)) # encher j1
		
        if (j2 == 0): # se j2 vazia
            children.append(Node((j1, 4, j3), self)) # encher j2

        if (j3 == 0): # se j3 vazio
            children.append(Node((j1, j2, 3), self)) #encher j3
		
        "Opções de transferência"
        "de j1 para j2 "
        if (j1 != 0 and j2 != 4): # se j1 não vazia e j2 não cheia
			# passar de j1 para j2 até encher
            transfer = 4 - j2 
            if (transfer > j1): transfer = j1
            children.append(Node((j1-transfer, j2+transfer, j3), self))

        "de j1 para j3 "
        if (j1 != 0 and j3 != 3): # se j3 não cheia e j1 não vazio
            # passar de j1 para j3 até encher
            transfer = 3 - j3
            if( transfer > j1): transfer = j1
            children.append(Node((j1-transfer,j2,j3+transfer), self))

        "de j2 para j1 "
        if (j1 != 6 and j2 != 0): # se j1 não cheia e j2 não vazia
			# passar de j2 para j1 até encher
            transfer = 6 - j1
            if (transfer > j2): transfer = j2
            children.append(Node((j1+transfer, j2-transfer, j3), self))

        "de j2 para j3 "
        if (j2 != 0 and j3 != 3): # se j3 não cheia e j2 não vazio
            # passar de j2 para j3 até encher
            transfer = 3 - j3
            if( transfer > j2): transfer = j2
            children.append(Node((j1,j2-transfer,j3+transfer), self))

        "de j3 para j2 "
        if (j2 != 4 and j3 != 0): # se j2 não cheia e j3 não vazia
			# passar de j3 para j2 até encher
            transfer = 4 - j2
            if (transfer > j3): transfer = j3
            children.append(Node((j1, j2+transfer, j3-transfer), self))
			
        "de j3 para j1 "
        if (j1 != 6 and j3 != 0): # se j1 não cheia e j3 não vazia
			# passar de j3 para j1 até encher
            transfer = 6 - j1
            if (transfer > j3): transfer = j3
            children.append(Node((j1+transfer, j2, j3-transfer), self))    

        if (j1 != 0): # se j1 não vazia
            children.append(Node((0, j2, j3), self)) # esvaziar j1
		  
        if (j2 != 0): # se j2 não vazia
            children.append(Node((j1, 0, j3), self)) # esvaziar j2
		
        if (j3 != 0): # se j3 não vazia
            children.append(Node((j1, j2, 0), self)) # esvaziar j3

        return children

"""
Busca em largura.
"""
def breadth_first():
	node = Node(estado_inicial, None) # estado inicial (raiz da árvore)
	frontier = deque() # fila da fronteira de nós a serem explorados
	explored = [] # lista de estados já explorados
	
	if node.goal_achieved():
		return node.trace_solution() # solução encontrada

	frontier.append(node)
	  
	while (True):
		if not frontier: # fronteira vazia
			return "FAILED"
		  
		node = frontier.popleft() # remoção FIFO
		explored.append(node.state)
		
		for child in node.children():
			if child.state not in explored and child not in frontier:
				if child.goal_achieved():
					return child.trace_solution() # solução encontrada no filho
				
				frontier.append(child)

"""
Busca em profundidade.
"""
def depth_first():
	node = Node(estado_inicial, None) # estado inicial, raiz
	frontier = deque() # pilha de nós da fronteira
	explored = [] # lista de estados explorados
	
	if node.goal_achieved():
	  return node.trace_solution() # solução encontrada

	frontier.append(node)
	
	while (True):
		if not frontier: # fronteira vazia
			return "FAILED"
		  
		node = frontier.pop() # remoção LIFO
		explored.append(node.state)
		
		for child in node.children():
			if child.state not in explored and child not in frontier:
				if child.goal_achieved():
					return child.trace_solution() # solução encontrada no filho
				
				frontier.append(child)

"""
Busca de custo uniforme.
(A solução de "menor custo" é a que executa o menor número de ações,
cada uma tendo então o mesmo custo = 1.)
"""
def uniform_cost():
	node = Node(estado_inicial, None)
	cost = 0
	
	frontier = {} # dict de nós e suas prioridades
	frontier[node] = 0 # nó raiz com prioridade 0
	explored = []
	
	while(True):
		if not frontier:
			return "FAILED"
		
		# pegar da fronteira o nó de menor prioridade
		min_priority = float('inf')
		min_node = None
		
		for n in frontier:
			if frontier[n] < min_priority:
				min_priority = frontier[n]
				min_node = n
		
		node = min_node
		del frontier[min_node]
		
		if node.goal_achieved():
			return node.trace_solution()
		  
		explored.append(node.state)
		
		for child in node.children():
			cost += 1
			
			if child.state not in explored and child not in frontier:
				frontier[child] = cost
			
			elif child in frontier and frontier[child] > cost:
				frontier[child] = cost



print("Busca em largura:")
breadth_first()

print("\nBusca em profundidade:")
depth_first()

print("\nBusca de custo uniforme:")
uniform_cost()