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
    breadth_first_graph_search,
    depth_first_tree_search,
    depth_first_graph_search,
    greedy_search,
    recursive_best_first_search,
)

class Board:
    """Representação interna de um tabuleiro de Takuzu."""
    def __init__(self, board, unfilled_squares):
        self.board_matrix = board
        self.shape = board.shape
        self.unfilled_squares = unfilled_squares

    def __str__(self):
        """Devolve a representação do tabuleiro."""
        string = ""
        for row in self.board_matrix:
            for col in row:
                string += str(col) + "\t"
            string = string[:-1]
            string += "\n"
        string = string[:-1]
        return string

    def get_col(self, ncol: int):
        col = []
        n = self.shape
        for i in range(n[1]):
            col = col + [self.board_matrix[i, ncol]]
        return col

    def get_row(self, nrow: int):
        row = []
        n = self.shape
        for i in range(n[0]):
            row = row + [self.board_matrix[nrow, i]]
        return row

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board_matrix[row, col]

    def copy_board(self, row: int, col: int, value: int):
        #board = self.board_matrix
        #new_board = []
        #for r in board:
            #new_row = []
            #for num in r:
                #new_row = new_row + [num]
            #new_board = new_board + [new_row]
        #newb = np.array(new_board)
        newb = self.board_matrix.copy()
        newb[row, col] = value
        return Board(newb, self.unfilled_squares - 1)

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        n = self.shape
        if n[0] > row+1:
            nbelow = self.board_matrix[row+1, col]
        else:
            nbelow = None
        if row+1 != 1:
            nabove = self.board_matrix[row-1, col]
        else:
            nabove = None
        return (nbelow, nabove)

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        n = self.shape
        if n[1] > col+1:
            nright = self.board_matrix[row, col+1]
        else:
            nright = None
        if col+1 != 1:
            nleft = self.board_matrix[row, col-1]
        else:
            nleft = None
        
        return (nleft, nright)

    def transpose(self):
        """Devolve a transposição do tabuleiro."""
        return Board(np.transpose(self.board_matrix), self.unfilled_squares)

    @staticmethod
    def parse_instance_from_stdin(goal_test: bool = False):
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
        Por exemplo:
            $ python3 takuzu.py < input_T01
            > from sys import stdin
            > stdin.readline()
        """
        
        unfilled_squares = 0

        if goal_test == True:
            test = sys.stdin.readlines()
        else: 
            test = sys.stdin.readlines()[1:]
        for idx, x in enumerate(test):
            x = x[0:len(x)-1]
            list_line = x.split('\t')
            for i in list_line:
                if int(i) == 2:
                    unfilled_squares += 1
                list_line[list_line.index(i)] = int(i)
            test[idx] = list_line
        board = np.array(test)
        return Board(board, unfilled_squares)

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
        self.initial = TakuzuState(board)

    def filter_actions_1(board: Board, n, actions):
            reverse = {0: 1, 1: 0}
            for row in range(n[0]):
                for col in range(n[1]):
                    num = board.get_number(row, col)
                    nbelow, nabove = board.adjacent_vertical_numbers(row, col)
                    nleft, nright = board.adjacent_horizontal_numbers(row, col)
                    if num != 2:
                        if (nbelow == num) and (nabove == 2):
                            actions.append((row-1, col, reverse[num]))
                            return actions
                        elif (nabove == num) and (nbelow == 2):
                            actions.append((row+1, col, reverse[num]))
                            return actions
                        if (nleft == num) and (nright == 2):
                            actions.append((row, col+1, reverse[num]))
                            return actions
                        elif (nright == num) and (nleft == 2):
                            actions.append((row, col-1, reverse[num]))
                            return actions
                    if num == 2:
                        if (nbelow == nabove) and (nbelow !=2 and nabove != 2):
                            actions.append((row, col, reverse[nbelow]))
                            return actions
                        elif (nleft == nright) and (nleft !=2 and nright != 2):
                            actions.append((row, col, reverse[nleft]))
                            return actions
            return actions

    def filter_actions_2(board: Board, n, actions):
        half_r = n[0]/2
        half_c = n[1]/2
        for i in range(n[0]):
            col = board.get_col(i)
            row = board.get_row(i)
            blank_col = ()
            blank_row = ()
            col_0 = col_1 = row_0 = row_1 = 0
            for j in range(n[0]):
                if col[j] == 2:
                    blank_col = blank_col + ((j, i),)
                elif col[j] == 1:
                    col_1 += 1
                elif col[j] == 0:
                    col_0 += 1 
                if row[j] == 2:
                    blank_row = blank_row + ((i, j),)
                elif row[j] == 1:
                    row_1 += 1
                elif row[j] == 0:
                    row_0 += 1
            if (n[1] % 2 == 0):
                if row_0 == (half_c) and blank_row != ():
                    for (row, col) in blank_row:
                        actions.append((row, col, 1))
                        return actions
                elif row_1 == (half_c) and blank_row != ():
                    for (row, col) in blank_row:
                        actions.append((row, col, 0))
                        return actions
            else:
                if row_0 == (half_c+1) and blank_row != ():
                    for (row, col) in blank_row:
                        actions.append((row, col, 1))
                        return actions
                elif row_1 == (half_c+1) and blank_row != ():
                    for (row, col) in blank_row:
                        actions.append((row, col, 0))
                        return actions
            if (n[0] % 2 == 0):  
                if col_0 == (half_r) and blank_col != ():
                    for (row, col) in blank_col:
                        actions.append((row, col, 1))
                        return actions
                elif col_1 == (half_r) and blank_col != ():
                    for (row, col) in blank_col:
                        actions.append((row, col, 0))
                        return actions
            else:
                if col_0 == (half_r+1) and blank_col != ():
                    for (row, col) in blank_col:
                        actions.append((row, col, 1))
                        return actions
                elif col_1 == (half_r+1) and blank_col != ():
                    for (row, col) in blank_col:
                        actions.append((row, col, 0))
                        return actions
        
        return actions

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        
        # only check if there are more than two of the same number in a row
        actions = []
        board = state.board
        n = board.shape
        actions = Takuzu.filter_actions_1(board, n, actions)
        if actions == []:
            actions = Takuzu.filter_actions_2(board, n, actions)
            if actions == []:
                for row in range(n[0]):
                    for col in range(n[1]):
                        num = board.get_number(row, col)
                        if num == 2:
                            actions.append((row, col, 0))
                            actions.append((row, col, 1))
        return actions

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        board = state.board.copy_board(action[0], action[1], action[2])
        return TakuzuState(board)

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        #?? nao sei quao importante é otimizar aqui
        board = state.board
        if board.unfilled_squares > 0:
            return False
        elif board.unfilled_squares == 0:
            boardt = state.board.transpose()
            goal_result = (Takuzu.check_goal_state(board) == True and 
            Takuzu.check_goal_state(boardt) == True)
            return goal_result
        else:
            print("Error")
            
    def check_goal_state(board: Board):
        n = board.shape
        b = board.board_matrix
        nrow = 0
        check = {}
        for row in b:
            ncol = zero = one = 0
            tup = ()
            for num in row:
                tup = tup + (num,)
                adj_horizontal = board.adjacent_horizontal_numbers(nrow, ncol)
                if adj_horizontal[0] == num and adj_horizontal[1] == num:
                        return False
                if num == 0:
                    zero += 1
                elif num == 1:
                    one +=1
                ncol += 1
            if zero != one:
                if n[0] % 2 == 0:
                    return False
                elif abs(one - zero) != 1:
                    return False
            if len(check) != 0 and tup in check.values():
                return False
            check[nrow+1] = tup
            nrow +=1
        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        return node.state.board.unfilled_squares

    # TODO: outros metodos da classe


if __name__ == "__main__":
    board = Board.parse_instance_from_stdin()
    problem = Takuzu(board)
    goal_node = depth_first_graph_search(problem)
    print(goal_node.state.board)