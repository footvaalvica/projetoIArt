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
        newb = self.board_matrix.copy()
        newb[row, col] = value
        return Board(newb, self.unfilled_squares - 1)

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        n = self.shape
        if n[0] > row + 1:
            nbelow = self.board_matrix[row + 1, col]
        else:
            nbelow = None
        if row + 1 != 1:
            nabove = self.board_matrix[row - 1, col]
        else:
            nabove = None
        return (nbelow, nabove)

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        n = self.shape
        if n[1] > col + 1:
            nright = self.board_matrix[row, col + 1]
        else:
            nright = None
        if col + 1 != 1:
            nleft = self.board_matrix[row, col - 1]
        else:
            nleft = None
        return (nleft, nright)

    def empty_positions(self):
        """Devolve a lista de posições vazias do tabuleiro."""
        empty_positions = []
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                if self.board_matrix[i, j] == 2:
                    empty_positions.append((i, j))
        return empty_positions

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
            x = x[0 : len(x) - 1]
            list_line = x.split("\t")
            for i in list_line:
                if int(i) == 2:
                    unfilled_squares += 1
                list_line[list_line.index(i)] = int(i)
            test[idx] = list_line
        board = np.array(test)
        return Board(board, unfilled_squares)


class TakuzuState:
    state_id = 0

    def __init__(self, board: Board):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = TakuzuState(board)

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        actions = []
        board = state.board
        n = board.shape
        to_fill = board.empty_positions()
        for i in to_fill:
            actions = Takuzu.correct_number(board, i)
            if actions != []:
                return actions
        if actions == []:
            for i in to_fill:
                (row, col) = i
                try_actions = [(row, col, 0), (row, col, 1)]
                actions = Takuzu.try_number(board, try_actions)
                if actions != []:
                    return actions
        return actions

    def try_number(board: Board, action):
        lis = []
        for act in action:
            new_board = board.copy_board(act[0], act[1], act[2])
            check = Takuzu.check_number(new_board, act)
            if check == True:
                lis.append(act)
        return lis

    def check_number(board: Board, action):
        num = board.get_number(action[0], action[1])
        n = board.shape
        nbelow, nabove = board.adjacent_vertical_numbers(action[0], action[1])
        nleft, nright = board.adjacent_horizontal_numbers(action[0], action[1])
        if (nbelow == num) and (nabove == num):
            return False
        if (nleft == num) and (nright == num):
            return False
        if (action[1]+1) != n[0]:
            nleft2, nright2 = board.adjacent_horizontal_numbers(action[0], action[1]+1)
            if (nright2 == nright) and (nright == num) and (num != 2):
                return False
        if action[1] != 0:
            nleft2, nright2 = board.adjacent_horizontal_numbers(action[0], action[1]-1)
            if (nleft2 == nleft) and (nleft == num) and (num != 2):
                return False
        if (action[0]+1) != n[0]:
            nbelow2, nabove2 = board.adjacent_vertical_numbers(action[0]+1, action[1])
            if (nbelow2 == nbelow) and (nbelow == num) and (num != 2):
                return False
        if action[0] != 0:
            nbelow2, nabove2 = board.adjacent_vertical_numbers(action[0]-1, action[1])
            if (nabove2 == nabove) and (nabove == num) and (num != 2):
                return False
        c = board.get_col(action[1])
        r = board.get_row(action[0])
        n = board.shape
        half = n[0]/2
        col_0 = col_1 = row_0 = row_1 = 0
        for i in range (n[0]):
            if c[i] == 0:
                col_0 +=1
            elif c[i] == 1:
                col_1 +=1
            if r[i] == 0:
                row_0 +=1
            elif r[i] == 1:
                row_1 +=1
        if n[0] % 2 == 0:
            if (col_0 > half) or (row_0 > half) or (col_1 > half) or (row_1 > half):
                return False
        else:
            if (col_0 > half+1) or (row_0 > half+1) or (col_1 > half+1) or (row_1 > half+1):
                return False
        return True
        
    @staticmethod
    def correct_number(board: Board, position):
        (row, col) = position
        actions = Takuzu.three_in_line(board, row, col)
        if actions == []:
            actions = Takuzu.line_numbers(board, row, col)
        return actions
    
    @staticmethod
    def three_in_line(board: Board, row, col):
        n = board.shape
        reverse = {0: 1, 1: 0}
        nbelow, nabove = board.adjacent_vertical_numbers(row, col)
        nleft, nright = board.adjacent_horizontal_numbers(row, col)
        if (nbelow == nabove) and (nbelow !=2):
            return [(row, col, reverse[nbelow])]
        elif (nleft == nright) and (nright != 2):
            return [(row, col, reverse[nleft])]
        if col+1 != n[0]:
            nleft2, nright2 = board.adjacent_horizontal_numbers(row, col+1)
            if (nright2 == nright) and (nright != 2):
                return[(row, col, reverse[nright])]
        if col != 0:
            nleft2, nright2 = board.adjacent_horizontal_numbers(row, col-1)
            if (nleft2 == nleft) and (nleft != 2):
                return[(row, col, reverse[nleft])]
        if row+1 != n[0]:
            nbelow2, nabove2 = board.adjacent_vertical_numbers(row+1, col)
            if (nbelow2 == nbelow) and (nbelow !=2):
                return [(row, col, reverse[nbelow])]
        if row != 0:
            nbelow2, nabove2 = board.adjacent_vertical_numbers(row-1, col)
            if (nabove2 == nabove) and (nabove !=2):
                return [(row, col, reverse[nabove])]
        return []

    @staticmethod
    def line_numbers(board: Board, row, col):
        c = board.get_col(col)
        r = board.get_row(row)
        n = board.shape
        half = n[0]/2
        col_0 = col_1 = row_0 = row_1 = 0
        for i in range (n[0]):
            if c[i] == 0:
                col_0 +=1
            elif c[i] == 1:
                col_1 +=1
            if r[i] == 0:
                row_0 +=1
            elif r[i] == 1:
                row_1 +=1
        if (n[0] % 2 == 0):
            if row_0 == half or col_0 == half:
                return [(row, col, 1)]
            elif row_1 == half or col_1 == half:
                return [(row, col, 0)]
        else:
            if row_0 == (half+1) or col_0 == (half+1):
                return [(row, col, 1)]
            elif row_1 == (half+1) or col_1 == (half+1):
                return [(row, col, 0)]
        return []

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
        board = state.board
        if board.unfilled_squares > 0:
            return False
        elif board.unfilled_squares == 0:
            return Takuzu.check_goal_state(board) == True

    def check_goal_state(board: Board):
        check_col = {}
        check_row = {}
        n = board.shape
        for i in range(n[0]):
            sumc = sumr = 0
            col = board.get_col(i)
            row = board.get_row(i)
            for j in range(n[0]):
                sumc+= col[j]
                sumr+= row[j]
                adj_horizontal = board.adjacent_horizontal_numbers(i, j)
                adj_vertical = board.adjacent_vertical_numbers(j, i)
                if adj_horizontal[0] == row[j] and adj_horizontal[1] == row[j]:
                    return False
                if adj_vertical[0] == col[j] and adj_vertical[1] == col[j]:
                    return False
            if sumc != (n[0]/2) or sumr != (n[0]/2):
                if n[0] % 2 == 0:
                    return False
                elif abs(sumc - (n[0]/2)) != 0.5 or abs(sumr - (n[0]/2)) != 0.5:
                    return False
            if (len(check_row) != 0 and len(check_col) != 0):
                if col in check_col.values() or row in check_row.values():
                    return False
            check_row[i] = row
            check_col[i] = col
        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        return node.state.board.unfilled_squares


if __name__ == "__main__":
    board = Board.parse_instance_from_stdin()
    problem = Takuzu(board)
    goal_node = depth_first_tree_search(problem)
    print(goal_node.state.board)