# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 09:
# 99282 Mateus Pinho
# 99238 Inês Ji

import sys
import numpy as np
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class TakuzuState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Takuzu."""
    def __init__(self, board):
        self.board = board

    def __str__(self):
        """Devolve a representação do tabuleiro."""
        string = ""
        for row in self.board:
            for col in row:
                string += str(col) + " "
            string += "\n"
        return string

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[row , col]

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        #TODO
        pass

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        #TODO
        pass

    def transpose(self):
        """Devolve a transposição do tabuleiro."""
        return np.transpose(self.board)

    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 takuzu.py < input_T01

            > from sys import stdin
            > stdin.readline()
        """

        input = sys.stdin.readlines()[1:]
        for idx, x in enumerate(input):
            x = x[0:len(x)-1]
            list_line = x.split('\t')
            list_line = [int(i) for i in list_line]
            input[idx] = list_line
        board = np.array(input) 
        return Board(board)

    # TODO: outros metodos da classe

class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO
        pass

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe

# APAGR!!! hahahahahahah
class Test:
    # estas cenas sao kinda inuteis por agora
    test1out = """Initial:
2 1 2 0
2 2 0 2
2 0 2 2
1 1 2 0
(None, 2)
(2, None)
(0, 1)
(2, 0)"""
    test2out = """Initial:
2 1 2 0
2 2 0 2
2 0 2 2
1 1 2 0
2
1
9"""
    test3out = """Initial:
2 1 2 0
2 2 0 2
2 0 2 2
1 1 2 0
Is goal? True
Solution:
0 1 1 0
1 0 0 1
0 0 1 1
1 1 0 0
10"""
    test4out = """Is goal? True
Solution:
0 1 1 0
1 0 0 1
0 0 1 1
1 1 0 0"""

    def __init__(self):
        self.test1()
    
    @staticmethod
    def test1():
        # Ler tabuleiro do ficheiro 'i1.txt'(Figura 1):
        # $ python3 takuzu < i1.txt 
        board = Board.parse_instance_from_stdin()
        print("Initial:\n", board, sep="")  
        # Imprimir valores adjacentes
        print(board.adjacent_vertical_numbers(3, 3))
        print(board.adjacent_horizontal_numbers(3, 3))
        print(board.adjacent_vertical_numbers(1, 1))
        print(board.adjacent_horizontal_numbers(1, 1))

    @staticmethod
    def test2():
        # Ler tabuleiro do ficheiro 'i1.txt'(Figura 1):
        # $ python3 takuzu < i1.txt
        board = Board.parse_instance_from_stdin()
        print("Initial:\n", board, sep="")
        # Criar uma instância de Takuzu:
        problem = Takuzu(board)
        # Criar um estado com a configuração inicial:
        initial_state = TakuzuState(board)
        # Mostrar valor na posição (2, 2):
        print(initial_state.board.get_number(2, 2))
        # Realizar acção de inserir o número 1 na posição linha 2 e coluna 2
        result_state = problem.result(initial_state, (2, 2, 1))
        # Mostrar valor na posição (2, 2):
        print(result_state.board.get_number(2, 2))

    @staticmethod
    def test3():
        # Ler tabuleiro do ficheiro 'i1.txt'(Figura 1):
        # $ python3 takuzu < i1.txt
        board = Board.parse_instance_from_stdin()
        # Criar uma instância de Takuzu:
        problem = Takuzu(board)
        # Criar um estado com a configuração inicial:
        s0 = TakuzuState(board)
        print("Initial:\n", s0.board, sep="")
        # Aplicar as ações que resolvem a instância
        s1 = problem.result(s0, (0, 0, 0))
        s2 = problem.result(s1, (0, 2, 1))
        s3 = problem.result(s2, (1, 0, 1))
        s4 = problem.result(s3, (1, 1, 0))
        s5 = problem.result(s4, (1, 3, 1))
        s6 = problem.result(s5, (2, 0, 0))
        s7 = problem.result(s6, (2, 2, 1))
        s8 = problem.result(s7, (2, 3, 1))
        s9 = problem.result(s8, (3, 2, 0))
        # Verificar se foi atingida a solução
        print("Is goal?", problem.goal_test(s9))
        print("Solution:\n", s9.board, sep="")
    
    @staticmethod
    def test4():
        # Ler tabuleiro do ficheiro 'i1.txt'(Figura 1):
        # $ python3 takuzu < i1.txt
        board = Board.parse_instance_from_stdin()
        # Criar uma instância de Takuzu:
        problem = Takuzu(board)
        # Obter o nó solução usando a procura em profundidade:
        goal_node = depth_first_tree_search(problem)
        # Verificar se foi atingida a solução
        print("Is goal?", problem.goal_test(goal_node.state))
        print("Solution:\n", goal_node.state.board, sep="")

if __name__ == "__main__":
    # TODO:
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    Test()
