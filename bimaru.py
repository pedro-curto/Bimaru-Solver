# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import sys
import copy
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
    def __init__(self,rows: list, cols: list, board: list, hints: list = []) -> None:
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
        # with open("instance01.txt") as f:

        #     rows = f.readline().split()[1:]
        #     cols = f.readline().split()[1:]
        #     hint_num = int(f.readline())
        #     for _ in range(hint_num):
        #         hints.append(f.readline().split()[1:])


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
        if self.boats_on_board["1"] != 4 or \
            self.boats_on_board["2"] != 3 or \
            self.boats_on_board["3"] != 2 or \
            self.boats_on_board["4"] != 1:
            return False

        for i in range(10):
            n_row = 0
            n_col = 0
            for j in range(10):
                if self.board[i][j] == " ":
                    return False
                else:
                    if self.board[i][j] != "W" and self.board[i][j] != ".":
                        n_row += 1
                    if self.board[j][i] != "W" and self.board[j][i] != ".":
                        n_col += 1
            if n_row != self.rows[i] or n_col != self.cols[i]:
                return False
        return True


    # TODO: outros metodos da classe

    def initial_check(self):
        self.fill_water()
        for i in self.hints:
            if i[2] != "W":
                row = i[0]
                col = i[1]
                self.place_water_around_boat(row, col)
        self.check_boats_on_board()

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
            #if self.board[row+1][col] == " ":
            #    self.board[row+1][col] = "?"
        elif boat == "B":
            for i in range(row - 2, row + 2):
                for j in range(col - 1, col + 2):
                    if i >= 0 and i < 10 and j >= 0 and j < 10:
                        if not (j == col and i < row):
                            if self.board[i][j] == " ":
                                self.board[i][j] = "."
            #if self.board[row-1][col] == " ":
            #    self.board[row-1][col] = "?"
        elif boat == "R":
            for i in range(row - 1, row + 2):
                for j in range(col - 2, col + 2):
                    if i >= 0 and i < 10 and j >= 0 and j < 10:
                        if not (i == row and j < col):
                            if self.board[i][j] == " ":
                                self.board[i][j] = "."
            #if self.board[row][col-1] == " ":
            #    self.board[row][col-1] = "?"
        elif boat == "L":
            for i in range(row - 1, row + 2):
                for j in range(col - 1, col + 3):
                    if i >= 0 and i < 10 and j >= 0 and j < 10:
                        if not (i == row and j > col):
                            if self.board[i][j] == " ":
                                self.board[i][j] = "."
            #if self.board[row][col+1] == " ":
            #    self.board[row][col+1] = "?"

        elif boat == "M":
            if self.board[row - 1][col] == "." or self.board[row + 1][col] == ".":
                for i in range(row - 1, row + 2):
                    for j in range(col - 2, col + 3):
                        if i >= 0 and i < 10 and j >= 0 and j < 10 and i != row:
                            if self.board[i][j] == " ":
                                self.board[i][j] = "."
                #if self.board[row][col+1] == " ":
                #    self.board[row][col+1] = "?"
                #if self.board[row][col-1] == " ":
                #    self.board[row][col-1] = "?"

            elif self.board[row][col - 1] == "." or self.board[row][col + 1] == ".":
                for i in range(row - 2, row + 3):
                    for j in range(col - 1, col + 2):
                        if i >= 0 and i < 10 and j >= 0 and j < 10 and j != col:
                            if self.board[i][j] == " ":
                                self.board[i][j] = "."
                #if self.board[row+1][col] == " ":
                #    self.board[row+1][col] = "?"
                #if self.board[row-1][col] == " ":
                #    self.board[row-1][col] = "?"

    def check_boats_on_board(self):
        to_remove = []
        for h in self.hints:
            if h[2] == "W":
                to_remove += [h]
            else:
                i = int(h[0])
                j = int(h[1])
                n = h[2]
                if n == "C":
                    self.boats_on_board["1"] += 1
                    to_remove += [h]
                elif n == "T":
                    if self.board[i+1][j] == "B":
                        self.boats_on_board["2"] += 1
                        to_remove += (h, [i+1, j, "B"])
                    elif self.board[i+1][j] == "M":
                        if self.board[i+2][j] == "B":
                            self.boats_on_board["3"] += 1
                            to_remove += (h, [i+1, j, "M"], [i+2, j, "B"])
                        elif self.board[i+2][j] == "M" and self.board[i+3][j] == "B":
                            to_remove += (h, [i+1, j, "M"], [i+2, j, "M"], [i+3, j, "B"])
                            self.boats_on_board["4"] += 1

                elif n == "L":
                    if self.board[i][j+1] == "R":
                        to_remove += (h, [i, j+1, "R"])
                        self.boats_on_board["2"] += 1
                    elif self.board[i][j+1] == "M":
                        if self.board[i][j+2] == "B":
                            to_remove += (h, [i, j+1, "M"], [i, j+2, "R"])
                            self.boats_on_board["3"] += 1
                        elif self.board[i][j+2] == "M" and self.board[i][j+3] == "B":
                            to_remove += (h, [i, j+1, "M"], [i, j+2, "M"], [i, j+3, "R"])
                            self.boats_on_board["4"] += 1
        print(to_remove)
        for item in to_remove:
            self.hints.remove(item)
                


    def place_boat_hor(self, action: list):
        board1 = copy.deepcopy(self)
        row = action[0]
        col = action[1]
        boat_size = action[2]
        boat = ("c","lr","lmr","lmmr")
        
        for i in range(boat_size):
            if board1.board[row][col+i] == " ":
                board1.board[row][col+i] = boat[boat_size-1][i]

        board1.boats_on_board[str(boat_size)] += 1
        board1.fill_water()

        return board1

    def place_boat_ver(self, action: list):
        board1 = copy.deepcopy(self)
        row = action[0]
        col = action[1]
        boat_size = action[2]
        boat = ("c","tb","tmb","tmmb")
        
        for i in range(boat_size):
            if board1.board[row+i][col] == " ":
                board1.board[row+i][col] = boat[boat_size-1][i]
        
        board1.boats_on_board[str(boat_size)] += 1
        board1.fill_water()

        return board1

        
                

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

        #if state.board.hints != []:
        #    return self.actions_hints(state.board)
  
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

        if action[3] == "r":
            return BimaruState(state.board.place_boat_hor(action))
        elif action[3] == "d":
            return BimaruState(state.board.place_boat_ver(action))

 
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

    def actions_hints(self, board: Board):
        actions = []
        for h in board.hints:
            x = h[0]
            y = h[1]
            if h[2] == "L" and (board[x][y+1] in (" ", "?")):
                for n in range(2,5):
                    if y + n-1 < 10 and board.boats_on_board[str(n)] < 5-n and board.rows[x] >= n:
                        actions += [(x, y, n, "r")]
            elif h[2] == "R" and (board[x][y-1] in (" ", "?")):
                for n in range(2,5):
                    if y - n+1 > 0 and board.boats_on_board[str(n)] < 5-n and board.rows[x] >= n:
                        actions += [(x, y-n+1, n, "r")]
                #actions = [(x, y-1, 2, "r"), (x, y-2, 3, "r"), (x, y-3, 4, "r")]
            elif h[2] == "T" and (board[x+1][y] in (" ", "?")):
                for n in range(2,5):
                    if x + n-1 and board.boats_on_board[str(n)] < 5-n and board.cols[y] >= n:
                        actions += [(x, y, n, "d")]
                #actions = [(x, y, 2, "d"), (x, y, 3, "d"), (x, y, 4, "d")]
            elif h[2] == "B" and (board[x-1][y] in (" ", "?")):
                for n in range(2,5):
                    if x - n+1 and board.boats_on_board[str(n)] < 5-n and board.cols[y] >= n:
                        actions += [(x-n+1, y, n, "d")]
                #actions = [(x-1, y, 2, "d"), (x-2, y, 3, "d"), (x-3, y, 4, "d")]
            elif h[2] == "M" and (board[x][y+1] in (" ", "?")) and (board[x][y-1] in (" ", "?")):
                actions += [(x, y-1, 3, "d")]
                if x - n+1 and board.boats_on_board[str(n)] < 5-n and board.cols[y] >= n:
                    actions += [(x-n+1, y, n, "d")]



    def action_boat(self, board: Board, n):
        actions = []

        for i in range(10):
            if board.rows[i] >= n or board.cols[i] >= n:
                k_row = 0
                k_col = 0
                for j in range(10):
                    #rows
                    row_val = board.get_value(i, j)
                    col_val = board.get_value(j, i)

                    if row_val == " ":
                        k_row += 1
                        if k_row >= n and board.rows[i] >= n:
                            actions.append((i, j-n+1, n, "r"))
                    elif (row_val == "L" and k_row == 0) or \
                            (row_val == "M" and k_row in (1, 2)):
                            k_row += 1
                    elif row_val == "R" and k_row in (1, 2, 3):
                        k_row += 1
                        if k_row >= n and board.rows[i] >= n:
                            actions.append((i, j-n+1, n, "r"))
                        k_row = 0
                    else:
                        k_row = 0
                    #cols
                    if col_val == " ":
                        k_col += 1
                        if k_col >= n and board.cols[i] >= n:
                            actions.append((j-n+1, i, n, "d"))
                    elif (col_val == "T" and k_col == 0) or \
                            (col_val == "M" and k_col in (1, 2)):
                            k_col += 1
                    elif col_val == "B" and k_col in (1, 2, 3):
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
    res = depth_first_tree_search(problem)
    if res:
        res.state.board.print_board()
    else:
        print("po crlh")
    pass
