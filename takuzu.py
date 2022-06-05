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

    def set_filled_tuple (self, row: int, col: int):
        self.filled_squares = self.filled_squares + ((row, col),)

    def get_filled_tuple (self):
        return self.filled_squares

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board_matrix[row, col]

    def deepcopy_set_number(self, row: int, col: int, value: int):
        """Copia o tabuleiro e altera o valor na respetiva posição."""
        new_board = self.board_matrix.copy()
        unfilled_squares_by_row = self.unfilled_squares_by_row.copy()
        unfilled_squares_by_row[row] = unfilled_squares_by_row[row] - 1
        if new_board[row, col] != 2:
            new_board[row, col] = value
        else:
            pass
        return Board(new_board, self.unfilled_squares - 1, unfilled_squares_by_row)

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

    def board_line_sum_without_number_two(self) -> list:
        """Devolve a soma de todas as linhas do tabuleiro,
        sem considerar o número 2."""
        line_sum = []
        for (idx, row) in enumerate(self.board_matrix):
            line_sum.append(0)
            for col in row:
                if col != 2:
                    line_sum[idx] += col
        return line_sum

    def transpose(self):
        """Devolve a transposição do tabuleiro."""
        return Board(np.transpose(self.board_matrix), self.unfilled_squares, self.unfilled_squares_by_row)

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
            test = sys.stdin.readlines()
        else: 
            test = sys.stdin.readlines()[1:]
        for idx, x in enumerate(test):
            x = x[0:len(x)-1]
            list_line = x.split('\t')
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
        def sum_check(board, n, actions, has_action_dict):
            def final_list_generator(sums, actions, has_action_dict, even = True):
                final_list = []
                for idx, x in enumerate(sums):
                    final_list.append((x, board.unfilled_squares_by_row[idx]))
                if even:
                    for idx, x in enumerate(final_list):
                        if x[0] == goal_sum and x[1] > 0:
                            for col in range(n):
                                if board.get_number(idx, col) == 2:
                                    actions.append((idx, col, 0))
                                    has_action_dict[(idx, col)] = True
                        elif (abs(x[0] - x[1]) == goal_sum) and (x[1] > 0):
                            for col in range(n):
                                if board.get_number(idx, col) == 2:
                                    actions.append((idx, col, 1))
                                    has_action_dict[(idx, col)] = True
                else:
                    #TODO FOR ODD NUMBERED BOARDS
                    pass
            
            sums = board.board_line_sum_without_number_two()      
            if (n % 2 == 0):
                goal_sum = n // 2
                for i in sums:
                    if i > goal_sum:
                        return []
                    else:
                        final_list_generator(sums, actions, has_action_dict)
                        return actions
            else:
                goal_sum = n // 2
                for i in sums:
                    if i >= goal_sum:
                        return []
                    else:
                        final_list_generator(sums, actions, has_action_dict, even = False)
                        return actions
            # # print("sums", sums)
            # # print("unfilled_squares_by_row", board.unfilled_squares_by_row)

        def filter_actions_1(board: Board, n, actions, has_action_dict):
            reverse = {0: 1, 1: 0}
            for row in range(n[0]):
                for col in range(n[1]):
                    num = board.get_number(row, col)
                    nbelow, nabove = board.adjacent_vertical_numbers(row, col)
                    nleft, nright = board.adjacent_horizontal_numbers(row, col)
                    if num != 2:
                        if (nbelow == num) and (nabove == 2):
                            if (row - 1, col) not in has_action_dict:
                                actions.append((row - 1, col, reverse[num]))
                                has_action_dict[(row - 1, col)] = True
                            else:
                                pass
                        if (nabove == num) and (nbelow == 2):
                            if (row + 1, col) not in has_action_dict:
                                actions.append((row + 1, col, reverse[num]))
                                has_action_dict[(row + 1, col)] = True
                            else:
                                pass
                        if (nleft == num) and (nright == 2):
                            if (row, col + 1) not in has_action_dict:
                                actions.append((row, col + 1, reverse[num]))
                                has_action_dict[(row, col + 1)] = True
                            else:
                               pass
                        if (nright == num) and (nleft == 2):
                            if (row, col - 1) not in has_action_dict:
                                actions.append((row, col - 1, reverse[num]))
                                has_action_dict[(row, col - 1)] = True
                            else:
                                pass
                    if num == 2:
                        if (nbelow == nabove) and (nbelow != 2 and nabove != 2):
                            if (row, col) not in has_action_dict:
                                actions.append((row, col, reverse[nbelow]))
                                has_action_dict[(row, col)] = True
                            else:
                                pass
                        elif (nleft == nright) and (nleft !=2 and nright != 2):
                            if (row, col) not in has_action_dict:
                                actions.append((row, col, reverse[nleft]))
                                has_action_dict[(row, col)] = True
                            else:
                                pass
            return actions

        # good flow of code
        # first add all the actions that are possible via sum of board
        # then remove actions that are not possible via adjacent squares
        # finally add all actions not in the list

        actions = []
        has_action_dict = {}
        board = state.board
        n = board.shape
        actions = sum_check(board, n[0], actions, has_action_dict)
        # # actions = sum_check_transpose()
        actions = filter_actions_1(board, n, actions, has_action_dict)
        print("filter actions", actions)
        if actions == []:
            return []
        for i in range(n[0]):
            for j in range(n[1]):
                if (i, j) not in has_action_dict and board.get_number(i, j) != 2:
                    actions.append((i, j, 0))
                    actions.append((i, j, 1))
        print("final actions", actions)
        print("has_action_dict", has_action_dict)
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
        #?? nao sei quao importante é otimizar aqui
        board = state.board
        if board.unfilled_squares > 0:
            return False
        elif board.unfilled_squares == 0:
            boardt = state.board.transpose()
            goal_result = (Takuzu.check_more_than_two(board) == True and 
            Takuzu.check_duplicate_lines(board) == True and 
            Takuzu.check_duplicate_lines(boardt) == True and 
            Takuzu.check_numbers(board) == True and
            Takuzu.check_numbers(boardt) == True)
            return goal_result
        else:
            print("board unfilled squares", board.unfilled_squares)
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
            nrow+=1
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
                    one +=1
            if zero != one and (n[0] % 2 == 0 or abs(one - zero) != 1):
                return False
        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        return node.state.board.unfilled_squares

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
Is goal?True\nSolution:\n0\t1\t1\t0\n1\t0\t0\t1\n0\t0\t1\t1\n1\t1\t0\t0\n"""
    test4out = """Is goal?True\nSolution:\n0\t1\t1\t0\n1\t0\t0\t1\n0\t0\t1\t1\n1\t1\t0\t0\n"""
    INITIAL = "Initial:\n"
    # cores
    @staticmethod
    def pr_green(prt):
        print("\033[92m{}\033[00m".format(prt))

    @staticmethod
    def pr_cyan(prt):
        print("\033[96m{}\033[00m".format(prt))

    @staticmethod
    def pr_red(prt):
        print("\033[91m{}\033[00m".format(prt))

    def __init__(self, board: Board):
        """Construtor da classe Test."""
        # # self.test1(board)
        # # self.test2(board)
        # # self.test3(board)
        self.test4(board)
    
    @staticmethod
    def test1(board: Board):
        test_output = str(Test.INITIAL + str(board)) + "\n"
        # Imprimir valores adjacentes
        test_output += str(board.adjacent_vertical_numbers(3, 3)) + "\n"
        test_output += str(board.adjacent_horizontal_numbers(3, 3)) + "\n"
        test_output += str(board.adjacent_vertical_numbers(1, 1)) + "\n"
        test_output += str(board.adjacent_horizontal_numbers(1, 1))

        if test_output == Test.test1out:
            Test.pr_green("Test 1 is nice!")
        else:
            Test.pr_red("Wrong!")
            Test.pr_cyan(Test.test1out)
            print(test_output)

    @staticmethod
    def test2(board: Board):
        test_output = str(Test.INITIAL + str(board)) + "\n"
        # Criar uma instância de Takuzu:
        problem = Takuzu(board)
        # Criar um estado com a configuração inicial:
        initial_state = TakuzuState(board)
        # Mostrar valor na posição (2, 2):
        test_output += str(initial_state.board.get_number(2, 2)) + "\n"
        # Realizar acção de inserir o número 1 na posição linha 2 e coluna 2
        result_state = problem.result(initial_state, (2, 2, 1))
        # Mostrar valor na posição (2, 2):
        test_output += str(result_state.board.get_number(2, 2))

        if test_output == Test.test2out:
            Test.pr_green("Test 2 is nice!")
        else:
            Test.pr_red("Wrong!\n")
            Test.pr_cyan(Test.test2out)
            print(test_output)

    @staticmethod
    def test3(board: Board):
        # Criar uma instância de Takuzu:
        problem = Takuzu(board)
        # Criar um estado com a configuração inicial:
        s0 = TakuzuState(board)
        test_output = str(Test.INITIAL + str(s0.board)) + "\n"       # Aplicar as ações que resolvem a instância
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
        test_output += str("Is goal?" +  str(problem.goal_test(s9))) + "\n"
        test_output += str("Solution:\n" + str(s9.board))

        if test_output == Test.test3out:
            # print diff between test3out and testoutput
            
            Test.pr_green("Test 3 is nice!")
        else:
            Test.pr_red("Wrong!")
            Test.pr_cyan(Test.test3out)
            # Test.prRed("DIFF" + str([x for x in testOutput if x not in Test.test3out]))
            print(test_output)
    
    @staticmethod
    def test4(board: Board):
        # Criar uma instância de Takuzu:
        problem = Takuzu(board)
        # Obter o nó solução usando a procura em profundidade:
        goal_node = depth_first_graph_search(problem)
        # Verificar se foi atingida a solução

        test_output = str("Is goal?" + str(problem.goal_test(goal_node.state))) + "\n"
        test_output += ("Solution:\n" + str(goal_node.state.board))

        if test_output == Test.test4out:
            Test.pr_green("Nice!\n")
        else:
            Test.pr_red("Wrong!\n")
            Test.pr_cyan(Test.test4out)
            print(test_output)

    @staticmethod
    def test_goal_test(board: Board):
        problem = Takuzu(board)
        state = TakuzuState(board)
        print(state.board)
        test_output = str("Is goal? " + str(problem.goal_test(state)))
        print(test_output)

if __name__ == "__main__":
    # TODO:
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.

    #!! nao mexas aqui por enquanto xD
    board = Board.parse_instance_from_stdin()
    
    # problem = Takuzu(board)
    # # Obter o nó solução usando a procura em profundidade:
    # goal_node = depth_first_graph_search(problem)
    # # Verificar se foi atingida a solução
    # testOutput = str("Is goal? " + str(problem.goal_test(goal_node.state))) + "\n"
    # testOutput += ("Solution:\n" + str(goal_node.state.board))
    
    # correr tests
    Test(board)