# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Bimaru."""
    def __init__(self,rows: list, cols: list, board: list, hints: list) -> None:
        self.board = board
        self.rows = rows
        self.cols = cols
        self.hints = hints
        self.boats_on_board = {
         "1":0,
         "2":0,
         "3":0,
         "4":0
        }  #4 de x, 3 de xx, 2 de xxx, 1 de xxxx


    def get_value(self, row: int, col: int) -> str:
        return self.board[row][col]

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        if row == 0:
            return ("", self.board[row + 1][col])
        elif row == 9:
            return (self.board[row - 1][col], "")
        else:
            return (self.board[row - 1][col], self.board[row + 1][col])

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        if col == 0:
            return ("", self.board[row][col + 1])
        elif col == 9:
            return (self.board[row][col - 1], "")
        else:
            return (self.board[row][col - 1], self.board[row][col + 1])

    def print_board(self):
        for i in range(10):
            line = ""
            for j in range(10):
                line += str(self.board[i][j]) + " "
            
            print(line + str(self.rows[i]))
        line = ""
        for i in range(10):
            line += str(self.cols[i]) + " "
        print(line)

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 bimaru.py < input_T01

            > from sys import stdin
            > line = stdin.readline().split()
        """
        hints = []
        rows = sys.stdin.readline().split()[1:]
        cols = sys.stdin.readline().split()[1:]

        rows = [int(num) for num in rows]
        cols = [int(num) for num in cols]

        hint_num = int(sys.stdin.readline())

        for _ in range(hint_num):
            hints.append(sys.stdin.readline().split()[1:])
        
        for i in range(len(hints)):
            hints[i][0] = int(hints[i][0])
            hints[i][1] = int(hints[i][1])


        board = [[" " for _ in range(10)] for _ in range(10)]
        for h in hints:
            x = h[0]
            y = h[1]
            n = h[2]
            board[x][y] = n

        return Board(rows,cols,board,hints)

    def test_goal(self):
        #TODO falta implementar o numero de barcos total
        for i in range(10):
            n_row = 0
            n_col = 0
            for j in range(10):
                if self.board[i][j] == " ":
                    return False
                elif self.board[i][j] != "W" and self.board[i][j] != ".":
                    n_row += 1
                elif self.board[j][i] != "W" and self.board[j][i] != ".":
                    n_col += 1
            if n_barcos != self.rows[i] or n_barcos != self.cols[i]:
                return False
        return False


    # TODO: outros metodos da classe

    def initial_check(self):
        self.fill_water()
        for i in self.hints:
            if i[2] != "W":
                row = i[0]
                col = i[1]
                self.place_water_around_boat(row, col)
        self.check_boats_on_board()
        print(self.boats_on_board)
        print(self.hints)

    def fill_water(self):
        for i in range(10):
            n_boats_row = 0
            n_boats_col = 0
            for j in range(10):
                if self.board[i][j] != "W" and self.board[i][j] != "." and self.board[i][j] != " ":
                    n_boats_row += 1
                if self.board[j][i] != "W" and self.board[j][i] != "." and self.board[j][i] != " ":
                    n_boats_col += 1
            if n_boats_row == self.rows[i]:
                for j in range(10):
                    if self.board[i][j] == " ":
                        self.board[i][j] = "."
            if n_boats_col == self.cols[i]:
                for j in range(10):
                    if self.board[j][i] == " ":
                        self.board[j][i] = "."

    def place_water_around_boat(self, row: int, col: int):
        boat = self.board[row][col]
        if boat == "C":
            for i in range(row - 1, row + 2):
                for j in range(col - 1, col + 2):
                    if i >= 0 and i < 10 and j >= 0 and j < 10:
                        if self.board[i][j] == " ":
                            self.board[i][j] = "."
        elif boat == "T":
            for i in range(row - 1, row + 3):
                for j in range(col - 1, col + 2):
                    if i >= 0 and i < 10 and j >= 0 and j < 10:
                        if not (j == col and i > row):
                            if self.board[i][j] == " ":
                                self.board[i][j] = "."
        elif boat == "B":
            for i in range(row - 2, row + 2):
                for j in range(col - 1, col + 2):
                    if i >= 0 and i < 10 and j >= 0 and j < 10:
                        if not (j == col and i < row):
                            if self.board[i][j] == " ":
                                self.board[i][j] = "."
        elif boat == "R":
            for i in range(row - 1, row + 2):
                for j in range(col - 2, col + 2):
                    if i >= 0 and i < 10 and j >= 0 and j < 10:
                        if not (i == row and j < col):
                            if self.board[i][j] == " ":
                                self.board[i][j] = "."
        elif boat == "L":
            for i in range(row - 1, row + 2):
                for j in range(col - 1, col + 3):
                    if i >= 0 and i < 10 and j >= 0 and j < 10:
                        if not (i == row and j > col):
                            if self.board[i][j] == " ":
                                self.board[i][j] = "."
        elif boat == "M":
            if self.board[row - 1][col] == "." or self.board[row + 1][col] == ".":
                for i in range(row - 1, row + 2):
                    for j in range(col - 2, col + 3):
                        if i >= 0 and i < 10 and j >= 0 and j < 10 and i != row:
                            if self.board[i][j] == " ":
                                self.board[i][j] = "."
            elif self.board[row][col - 1] == "." or self.board[row][col + 1] == ".":
                for i in range(row - 2, row + 3):
                    for j in range(col - 1, col + 2):
                        if i >= 0 and i < 10 and j >= 0 and j < 10 and j != col:
                            if self.board[i][j] == " ":
                                self.board[i][j] = "."

    def check_boats_on_board(self):
        to_remove = []
        for h in self.hints:
            if h[2] == "W":
                to_remove.append(h)
            else:
                i = int(h[0])
                j = int(h[1])
                n = h[2]
                if n == "C":
                    self.boats_on_board["1"] += 1
                    to_remove.append(h)
                elif n == "T":
                    if self.board[i+1][j] == "B":
                        self.boats_on_board["2"] += 1
                        to_remove.append(h)
                        to_remove.append([i+1, j, "B"])
                    elif self.board[i+1][j] == "M":
                        if self.board[i+2][j] == "B":
                            self.boats_on_board["3"] += 1
                            to_remove.append(h)
                            to_remove.append([i+1, j, "M"])
                            to_remove.append([i+2, j, "B"])
                        elif self.board[i+2][j] == "M" and self.board[i+3][j] == "B":
                            to_remove.append(h)
                            to_remove.append([i+1, j, "M"])
                            to_remove.append([i+2, j, "M"])
                            to_remove.append([i+3, j, "B"])
                            self.boats_on_board["4"] += 1
                elif n == "L":
                    if self.board[i][j+1] == "R":
                        to_remove.append(h)
                        to_remove.append([i, j+1, "R"])
                        self.boats_on_board["2"] += 1
                    elif self.board[i][j+1] == "M":
                        if self.board[i][j+2] == "B":
                            to_remove.append(h)
                            to_remove.append([i, j+1, "M"])
                            to_remove.append([i, j+2, "R"])
                            self.boats_on_board["3"] += 1
                        elif self.board[i][j+2] == "M" and self.board[i][j+3] == "B":
                            to_remove.append(h)
                            to_remove.append([i, j+1, "M"])
                            to_remove.append([i, j+2, "M"])
                            to_remove.append([i, j+3, "R"])
                            self.boats_on_board["4"] += 1
        
        for item in to_remove:
            self.hints.remove(item)

    def place_boat_hor(self, action: list):
        row = action[0]
        col = action[1]
        boat_size = action[2]
        boat = ("c","lr","lmr","lmmr")
        for i in range(boat_size):
            if self.board[row][col+i] == " ":
                self.board[row][col+i] = boat[boat_size-1][i]

        self.boats_on_board[str(boat_size)] += 1
        self.fill_water()
        return BimaruState(self)

    def place_boat_ver(self, action: list):
        row = action[0]
        col = action[1]
        boat_size = action[2]
        boat = ("c","tb","tmb","tmmb")
        for i in range(boat_size):
            if self.board[row][col+i] == " ":
                self.board[row][col+i] = boat[boat_size-1][i]
        
        self.boats_on_board[str(boat_size)] += 1
        self.fill_water()

        return BimaruState(self)

        
                

class Bimaru(Problem):
    def __init__(self, board: Board):
        super().__init__(BimaruState(board))

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        return state.board.test_goal()


    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        board = state.board
        actions = []
  
        if board.boats_on_board["4"] < 1:
            actions += self.action_boat(board, 4)
        elif board.boats_on_board["3"] < 2:
            actions += self.action_boat(board, 3)
        elif board.boats_on_board["2"] < 3:
            actions += self.action_boat(board, 2)
        elif board.boats_on_board["1"] < 4:
            actions += self.action_boat(board, 1)

        return actions
            


    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        if action[2] == "r":
            return state.board.place_boat_hor(action)
        elif action[2] == "b":
            return state.board.place_boat_ver(action)

 
    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        #????????????????????????????????????????????????????????????????????????????????????????????
        #TODO
        n = 0
        for i in range(10):
            for j in range(10):
                if node.state.board[i][j] == " ":
                    n += 1
        return n

    # TODO: outros metodos da classe

    def action_boat(self, board: Board, n):
        actions = []
        for i in range(10):
            if board.rows[i] >= n or board.cols[i] >= n:
                k_row = 0
                k_col = 0
                for j in range(10):
                    #rows
                    if board.get_value(i, j) == " ":
                        k_row += 1
                        if k_row >= n and board.rows[i] >= n:
                            actions.append((i-n+1, j, n, "r"))
                    elif (board.get_value(i, j) == "L" and k_row == 0) or \
                            (board.get_value(i, j) == "M" and k_row in (1, 2)):
                            k_row += 1
                    elif board.get_value(i, j) == "R" and k_row in (1, 2, 3):
                        k_row += 1
                        if k_row >= n and board.rows[i] >= n:
                            actions.append((i-n+1, j, n, "r"))
                        k_row = 0
                    else:
                        k_row = 0
                    #cols
                    if board.get_value(j, i) == " ":
                        k_col += 1
                        if k_col >= n and board.cols[i] >= n:
                            actions.append((j-n+1, i, n, "d"))
                    elif (board.get_value(j, i) == "T" and k_col == 0) or \
                            (board.get_value(j, i) == "M" and k_col in (1, 2)):
                            k_col += 1
                    elif board.get_value(j, i) == "B" and k_col in (1, 2, 3):
                        k_col += 1
                        if k_col >= n and board.cols[i] >= n:
                            actions.append((j-n+1, i, n, "d"))
                        k_col = 0
                    else:
                        k_col = 0
        return actions


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.

    x = Board.parse_instance()
    x.initial_check()
    x.print_board()
    problem = Bimaru(x)
    res = breadth_first_tree_search(problem)
    res.state.board.print_board()

    pass
