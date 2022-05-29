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

class Board:
    """Representação interna de um tabuleiro de Takuzu."""
    def __init__(self, board):
        self.board = board

    def __str__(self):
        """Devolve a representação do tabuleiro."""
        string = ""
        for row in self.board:
            for col in row:
                string += str(col) + "\t"
            string = string[:-1]
            string += "\n"
        return string

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[row, col]

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        n = self.board.shape
        if n[0] > row+1:
            nbelow = self.board[row+1, col]
        else:
            nbelow = None
        if row+1 != 1:
            nabove = self.board[row-1, col]
        else:
            nabove = None
        return (nbelow, nabove)

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        n = self.board.shape
        if n[1] > col+1:
            nright = self.board[row, col+1]
        else:
            nright = None
        if col+1 != 1:
            nleft = self.board[row, col-1]
        else:
            nleft = None
        
        return (nleft, nright)

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

class TakuzuState:
    state_id = 0

    def __init__(self, board: Board):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

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

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe

# TODO finish this class
class Test:
    """APAGR!!! hahahahahahah
    qnd tiveres a trabalhar no proj colapsa só esta classe, tá feia
    e se quiseres meter mais testes a correr altera o construtor"""
    # estas cenas sao kinda inuteis por agora
    test1out = """Initial:\n2\t1\t2\t0\n2\t2\t0\t2\n2\t0\t2\t2\n1\t1\t2\t0\n
(None, 2)
(2, None)
(0, 1)
(2, 0)"""
    test2out = """Initial:\n2\t1\t2\t0\n2\t2\t0\t2\n2\t0\t2\t2\n1\t1\t2\t0\n
2
1"""
    test3out = """Initial:\n2\t1\t2\t0\n2\t2\t0\t2\n2\t0\t2\t2\n1\t1\t2\t0\n
Is goal? True
Solution:\n0\t1\t1\t0\n1\t0\t0\t1\n0\t0\t1\t1\n1\t1\t0\t0\n"""
    test4out = """Is goal? True
Solution:\n0\t1\t1\t0\n1\t0\t0\t1\n0\t0\t1\t1\n1\t1\t0\t0\n"""

    # cores
    @staticmethod
    def prGreen(prt):
        print("\033[92m{}\033[00m".format(prt))

    @staticmethod
    def prCyan(prt):
        print("\033[96m{}\033[00m".format(prt))

    @staticmethod
    def prRed(prt):
        print("\033[91m{}\033[00m".format(prt))

    def __init__(self, board: Board):
        """Construtor da classe Test."""
        self.test1(board)
        # # self.test2(board)
        # # self.test3(board)
        # # self.test4(board)

    
    @staticmethod
    def test1(board: Board):
        testOutput = str("Initial:\n" + str(board)) + "\n"
        # Imprimir valores adjacentes
        testOutput += str(board.adjacent_vertical_numbers(3, 3)) + "\n"
        testOutput += str(board.adjacent_horizontal_numbers(3, 3)) + "\n"
        testOutput += str(board.adjacent_vertical_numbers(1, 1)) + "\n"
        testOutput += str(board.adjacent_horizontal_numbers(1, 1))

        if testOutput == Test.test1out:
            Test.prGreen("Nice!")
        else:
            Test.prRed("Wrong!")
            Test.prCyan(Test.test1out)
            print(testOutput)

    @staticmethod
    def test2(board: Board):
        testOutput = ""
        testOutput.append("Initial:\n", board, sep="")
        # Criar uma instância de Takuzu:
        problem = Takuzu(board)
        # Criar um estado com a configuração inicial:
        initial_state = TakuzuState(board)
        # Mostrar valor na posição (2, 2):
        testOutput.append(initial_state.board.get_number(2, 2))
        # Realizar acção de inserir o número 1 na posição linha 2 e coluna 2
        result_state = problem.result(initial_state, (2, 2, 1))
        # Mostrar valor na posição (2, 2):
        testOutput.append(result_state.board.get_number(2, 2))

        if testOutput == Test.test2out:
            Test.prGreen("Nice!\n")
        else:
            Test.prRed("Wrong!\n")
            Test.prCyan(Test.test2out)
            print(testOutput)

    @staticmethod
    def test3(board: Board):
        testOutput = ""
        # Criar uma instância de Takuzu:
        problem = Takuzu(board)
        # Criar um estado com a configuração inicial:
        s0 = TakuzuState(board)
        testOutput.append("Initial:\n", s0.board, sep="")
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
        testOutput.append("Is goal?", problem.goal_test(s9))
        testOutput.append("Solution:\n", s9.board, sep="")

        if testOutput == Test.test3out:
            Test.prGreen("Nice!\n")
        else:
            Test.prRed("Wrong!\n")
            Test.prCyan(Test.test3out)
            print(testOutput)
    
    @staticmethod
    def test4(board: Board):
        testOutput = ""
        # Criar uma instância de Takuzu:
        problem = Takuzu(board)
        # Obter o nó solução usando a procura em profundidade:
        goal_node = depth_first_tree_search(problem)
        # Verificar se foi atingida a solução
        testOutput.append("Is goal?", problem.goal_test(goal_node.state))
        testOutput.append("Solution:\n", goal_node.state.board, sep="")

        if testOutput == Test.test4out:
            Test.prGreen("Nice!\n")
        else:
            Test.prRed("Wrong!\n")
            Test.prCyan(Test.test4out)
            print(testOutput)

if __name__ == "__main__":
    # TODO:
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.

    #!! nao mexas aqui por enquanto xD
    board = Board.parse_instance_from_stdin()

    # correr tests
    Test(board)
