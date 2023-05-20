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

        board = [[" " for _ in range(10)] for _ in range(10)]
        for i in range(len(hints)):
            x = int(hints[i][0])
            y = int(hints[i][1])
            n = hints[i][2]
            board[x][y] = n

        return Board(rows,cols,board,hints)

    def test_goal(self):
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


    # TODO: outros metodos da classe

    def initial_check(self):
        self.fill_water()
        for i in self.hints:
            if i[2] != "W":
                row = int(i[0])
                col = int(i[1])
                self.place_water_around_boat(row, col)

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

        # TODO
        pass

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass
 
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


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.

    x = Board.parse_instance()
    x.initial_check()
    x.print_board()



    pass
