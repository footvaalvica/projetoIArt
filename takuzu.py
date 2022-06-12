# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 09:
# 99282 Mateus Pinho
# 99238 Inês Ji

from sys import stdin

# # from numpy import array, transpose
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

    def __init__(self, board, unfilled_squares, unfilled_squares_by_row):
        self.board_matrix = board
        self.shape = board.shape
        self.unfilled_squares = unfilled_squares
        self.unfilled_squares_by_row = unfilled_squares_by_row
        self.filled_squares = ()

    def __str__(self):
        """Devolve a representação do tabuleiro."""
        string = ""
        for row in self.board_matrix:
            for col in row:
                string += str(col) + "\t"
            string = string[:-1]
            string += "\n"
        return string

    def set_filled_tuple(self, row: int, col: int):
        self.filled_squares = self.filled_squares + ((row, col),)

    def get_filled_tuple(self):
        return self.filled_squares

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board_matrix[row, col]

    def deepcopy_set_number(self, row: int, col: int, value: int):
        """Copia o tabuleiro e altera o valor na respetiva posição."""
        new_board = self.board_matrix.copy()
        unfilled_squares_by_row = self.unfilled_squares_by_row.copy()
        unfilled_squares_by_row[row] = unfilled_squares_by_row[row] - 1
        new_board[row, col] = value
        return Board(new_board, self.unfilled_squares - 1, unfilled_squares_by_row)

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

    def strip_twos(self):
        board_matrix = self.board_matrix.copy()
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                if board_matrix[i, j] == 2:
                    board_matrix[i, j] = 0
        return Board(board_matrix, self.unfilled_squares, self.unfilled_squares_by_row)

    def transpose(self):
        """Devolve a transposição do tabuleiro."""
        return Board(
            np.transpose(self.board_matrix),
            self.unfilled_squares,
            self.unfilled_squares_by_row,
        )

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
        unfilled_squares_by_row = []

        if goal_test == True:
            test = stdin.readlines()
        else:
            test = stdin.readlines()[1:]
        for idx, x in enumerate(test):
            x = x[0 : len(x) - 1]
            list_line = x.split("\t")
            unfilled_squares_by_row.append(0)
            for i in list_line:
                if int(i) == 2:
                    unfilled_squares += 1
                    unfilled_squares_by_row[idx] += 1
                list_line[list_line.index(i)] = int(i)
            test[idx] = list_line
        board = np.array(test)
        return Board(board, unfilled_squares, unfilled_squares_by_row)

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

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

        def sum_check(board, n, actions):
            def final_list_generator(sums, actions, odd: bool = False):
                final_list = []
                for idx, x in enumerate(sums):
                    final_list.append((x, board.unfilled_squares_by_row[idx]))
                for idx, x in enumerate(final_list):
                    if (x[0] == (goal_sum or goal_sum + odd)) and x[1] > 0:
                        for col in range(n):
                            if (idx, col, 1) in actions:
                                actions.remove((idx, col, 1))
                            elif (x[0] - x[1] == (goal_sum or goal_sum + odd)) and x[
                                1
                            ] > 0:
                                for col in range(n):
                                    if (idx, col, 1) in actions:
                                        actions.remove((idx, col, 0))

            board2 = board.strip_twos()
            sums = board2.board_matrix.sum(axis=1)
            goal_sum = n // 2
            if n % 2 == 0:
                final_list_generator(sums, actions)
                return actions
            else:
                final_list_generator(sums, actions, odd=True)
                return actions

        def filter_actions_1(board: Board, n, actions):
            for row in range(n[0]):
                for col in range(n[1]):
                    num = board.get_number(row, col)
                    nbelow, nabove = board.adjacent_vertical_numbers(row, col)
                    nleft, nright = board.adjacent_horizontal_numbers(row, col)
                    if num != 2:
                        if (nbelow == num) and (nabove == 2):
                            actions.append((row - 1, col, not (num)))
                            board.set_filled_tuple(row - 1, col)
                        if (nabove == num) and (nbelow == 2):
                            actions.append((row + 1, col, not (num)))
                            board.set_filled_tuple(row + 1, col)
                        if (nleft == num) and (nright == 2):
                            actions.append((row, col + 1, not (num)))
                            board.set_filled_tuple(row, col + 1)
                        if (nright == num) and (nleft == 2):
                            actions.append((row, col - 1, not (num)))
                            board.set_filled_tuple(row, col - 1)
                    else:
                        if (nbelow == nabove) and (nbelow != 2 and nabove != 2):
                            actions.append((row, col, not (num)))
                            board.set_filled_tuple(row, col)
                        if (nleft == nright) and (nleft != 2 and nright != 2):
                            actions.append((row, col, not (num)))
                            board.set_filled_tuple(row, col)
            return actions

        actions = []
        board = state.board
        n = board.shape
        actions = filter_actions_1(board, n, actions)
        filled = board.get_filled_tuple()
        for row in range(n[0]):
            for col in range(n[1]):
                num = board.get_number(row, col)
                if num == 2:
                    if (row, col) not in filled:
                        actions.append((row, col, 0))
                        actions.append((row, col, 1))
        actions = sum_check(board, n[0], actions)
        return actions

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        board = state.board.deepcopy_set_number(action[0], action[1], action[2])
        return TakuzuState(board)

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        # ?? nao sei quao importante é otimizar aqui
        board = state.board
        if board.unfilled_squares > 0:
            return False
        elif board.unfilled_squares == 0:
            boardt = state.board.transpose()
            goal_result = (
                Takuzu.check_more_than_two(board) == True
                and Takuzu.check_duplicate_lines(board) == True
                and Takuzu.check_duplicate_lines(boardt) == True
                and Takuzu.check_numbers(board) == True
                and Takuzu.check_numbers(boardt) == True
            )
            return goal_result
        else:
            print("Error")

    @staticmethod
    def check_more_than_two(board: Board):
        nrow = 0
        for row in board.board_matrix:
            ncol = 0
            for num in row:
                adj_horizontal = board.adjacent_horizontal_numbers(nrow, ncol)
                if adj_horizontal[0] == num and adj_horizontal[1] == num:
                    return False
                adj_vertical = board.adjacent_vertical_numbers(nrow, ncol)
                if adj_vertical[0] == num and adj_vertical[1] == num:
                    return False
                ncol += 1
            nrow += 1
        return True

    @staticmethod
    def check_duplicate_lines(board: Board):
        check = {}
        nrow = 1
        for row in board.board_matrix:
            tup = ()
            for num in row:
                tup = tup + (num,)
            if len(check) != 0 and tup in check.values():
                return False
            check[nrow] = tup
            nrow += 1
        return True

    @staticmethod
    def check_numbers(board: Board):
        n = board.shape
        for row in board.board_matrix:
            zero = one = 0
            for num in row:
                if num == 0:
                    zero += 1
                elif num == 1:
                    one += 1
            if zero != one and (n[0] % 2 == 0 or abs(one - zero) != 1):
                return False
        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # todo improve
        return node.state.board.unfilled_squares

    # TODO: outros metodos da classe

if __name__ == "__main__":
    board = Board.parse_instance_from_stdin()
    problem = Takuzu(board)
    goal_node = depth_first_tree_search(problem)
    print(goal_node.state.board)