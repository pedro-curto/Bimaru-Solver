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
    compare_searchers,
)


class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    def __eq__(self, other):
        return self.board == other.board
    
    def __hash__(self):
        return hash(self.board)


class Board:
    """Representação interna de um tabuleiro de Bimaru."""
    def __init__(self, rows: list, cols: list, board: list, boats_rows: list \
                 , boats_cols:list) -> None:
        self.board = board
        self.rows = rows
        self.cols = cols
        self.boats_rows = boats_rows
        self.boats_cols = boats_cols
        self.bad_board = False
        self.boats_on_board = {
         "1": 0,
         "2": 0,
         "3": 0,
         "4": 0
        }  # 4 de x, 3 de xx, 2 de xxx, 1 de xxxx
        # convert board to an immutable data type, so that it can be hashed
        self.hashNum = 0
        #self.hashNum = hash(tuple(tuple(row) for row in self.board))
                
        
        
    def __eq__(self, other):
        if isinstance(other, Board):
            if self.__hash__() != other.__hash__():
                return False
            return self.board == other.board    
        return False 


    def __hash__(self):
        if self.hashNum == 0:
            self.hashNum = hash(tuple(tuple(row) for row in self.board))
        return self.hashNum


    def get_value(self, row: int, col: int) -> str:
        return self.board[row][col]


    def adjacent_cell_values(self, row: int, col: int):
        """ Returns all adjacent, even diagonal, values, that are valid within
        the board. """
        offset_list = [(-1, -1), (-1, 0), (-1, 1),
                       (0, -1),           (0, 1),
                       (1, -1),  (1, 0),  (1, 1)]
        cell_adjacent_values = []
        for offset in offset_list:
            adjacent_row, adjacent_col = row + offset[0], col + offset[1]
            # checks for each cell if it's in the board
            if 0 <= adjacent_row <= 9 and 0 <= adjacent_col <= 9: 
                cell_adjacent_values.append((self.board[adjacent_row][adjacent_col], 
                                            adjacent_row, adjacent_col))
        return cell_adjacent_values
    

    def adjacent_diagonal_values(self, row: int, col: int):
        """ Returns all adjacent diagonal values, that are valid within
        the board. """
        offset_list = [(-1, -1), (-1, 1),
                       (1, -1),  (1, 1)]
        cell_adjacent_values = []
        for offset in offset_list:
            adjacent_row, adjacent_col = row + offset[0], col + offset[1]
            # checks for each cell if it's in the board
            if 0 <= adjacent_row <= 9 and 0 <= adjacent_col <= 9:
                cell_adjacent_values.append((self.board[adjacent_row][adjacent_col], 
                                            adjacent_row, adjacent_col))
        return cell_adjacent_values
    

    def adjacent_vertical_values(self, row: int, col: int):
        if row == 0:
            return [(self.board[row + 1][col], row+1, col)]
        elif row == 9:
            return [(self.board[row - 1][col], row-1, col)]
        else:
            return [(self.board[row - 1][col], row-1, col), 
                    (self.board[row + 1][col], row+1, col)]
#
#
    def adjacent_horizontal_values(self, row: int, col: int):
        if col == 0:
            return [(self.board[row][col + 1], row, col+1)]
        elif col == 9:
            return [(self.board[row][col - 1], row, col-1)]
        else:
            return [(self.board[row][col - 1], row, col-1),
                    (self.board[row][col + 1], row, col+1)]

    def print_board(self):
        for i in range(10):
            line = ""
            for j in range(10):
                line += self.board[i][j]
            
            print(line) #+ str(self.rows[i]))
        #line = ""
        #for i in range(10):
        #    line += str(self.cols[i]) + " "
        #print(line)

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
        boats_rows = [0 for _ in range(10)]
        boats_cols = [0 for _ in range(10)]

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
            if n != "W":
                boats_rows[x] += 1
                boats_cols[y] += 1
                
        return Board(rows, cols, board, boats_rows, boats_cols), hints

    def test_goal(self):
        #TODO falta implementar o numero de barcos total
        if self.boats_on_board["1"] != 4 or \
            self.boats_on_board["2"] != 3 or \
            self.boats_on_board["3"] != 2 or \
            self.boats_on_board["4"] != 1:
            return False

        for i in range(10):
            if self.rows[i] != self.boats_rows[i] or self.cols[i] != self.boats_cols[i]:
                return False
        return True


    def pre_processing(self, hints):
        self.fill_water()
        for i in hints:
            if i[2] != "W":
                row = i[0]
                col = i[1]
                self.handle_hint(row, col)
        self.check_boats_on_board(hints)
        #change = False
        #while not change:
        #    
        #    # after placing the hints, the extra pieces and the water around,
        #    # checks if we can fill any lines or columns
        #    x1 = self.check_fill_lines()
        #    x2 = self.check_boats_on_board(hints)
        #    change = any((x1, x2))
        #    #self.print_board()
        #    #print()


    def initial_handle_C_boat(self, row: int, col: int):
        adjacent_cells = self.adjacent_cell_values(row, col)
        #print(adjacent_cells)
        for i in range(len(adjacent_cells)):
            if adjacent_cells[i][0] == " ":
                self.board[adjacent_cells[i][1]][adjacent_cells[i][2]] = "."
                self.check_fill_water_row(row)
                self.check_fill_water_col(col)


    def initial_handle_T_boat(self, row: int, col: int):
        if row != 9 and self.board[row+1][col] == " ":
            self.board[row+1][col] = "?"
            self.boats_cols[col] += 1
            self.boats_rows[row+1] += 1
            self.check_fill_water_col(col)
            self.check_fill_water_row(row+1)
        adjacent_cells = self.adjacent_cell_values(row, col)
        #print(adjacent_cells)
        for i in range(len(adjacent_cells)):
            if adjacent_cells[i][0] == " ":
                self.board[adjacent_cells[i][1]][adjacent_cells[i][2]] = "."
    

    def initial_handle_B_boat(self, row: int, col: int):
        if row != 0 and self.board[row-1][col] == " ":
            self.board[row-1][col] = "?"
            self.boats_cols[col] += 1
            self.boats_rows[row-1] += 1
            self.check_fill_water_col(col)
            self.check_fill_water_row(row-1)
        adjacent_cells = self.adjacent_cell_values(row, col)
        #print(adjacent_cells)
        for i in range(len(adjacent_cells)):
            if adjacent_cells[i][0] == " ":
                self.board[adjacent_cells[i][1]][adjacent_cells[i][2]] = "."


    def initial_handle_L_boat(self, row: int, col: int):
        if col != 9 and self.board[row][col+1] == " ":
            self.board[row][col+1] = "?"
            self.boats_rows[row] += 1
            self.boats_cols[col+1] += 1
            self.check_fill_water_row(row)
            self.check_fill_water_col(col+1)
        adjacent_cells = self.adjacent_cell_values(row, col)
        #print(adjacent_cells)
        for i in range(len(adjacent_cells)):
            if adjacent_cells[i][0] == " ":
                self.board[adjacent_cells[i][1]][adjacent_cells[i][2]] = "."
        

    def initial_handle_R_boat(self, row: int, col: int):
        if col != 0 and self.board[row][col-1] == " ":
            self.board[row][col-1] = "?"
            self.boats_rows[row] += 1
            self.boats_cols[col-1] += 1
            self.check_fill_water_row(row)
            self.check_fill_water_col(col-1)
        adjacent_cells = self.adjacent_cell_values(row, col)
        #print(adjacent_cells)   
        for i in range(len(adjacent_cells)):
            if adjacent_cells[i][0] == " ":
                self.board[adjacent_cells[i][1]][adjacent_cells[i][2]] = "."

        
    def initial_handle_M_boat(self, row: int, col: int):
        # adds water to the diagonals if they are empty: this can always be done
        diagonal_cells = self.adjacent_diagonal_values(row, col)
        for cell in diagonal_cells:
            if cell[0] == " ":
                self.board[cell[1]][cell[2]] = "."  
        # checks if there is water above or under the piece
        if row - 1 == -1 or row + 1 == 10 or \
        self.board[row - 1][col] in (".", "W") or \
        self.board[row + 1][col] in (".", "W"):
            # adds pieces if the up/down cell is empty
            if col != 9 and self.board[row][col+1] == " ":
                self.board[row][col+1] = "?"
                self.boats_cols[col+1] += 1
                self.boats_rows[row] += 1
                self.check_fill_water_col(col+1)
            if col != 0 and self.board[row][col-1] == " ":
                self.board[row][col-1] = "?"
                self.boats_cols[col-1] += 1
                self.boats_rows[row] += 1
                self.check_fill_water_col(col-1)
            self.check_fill_water_row(row)
            # adds water to the remaining adjacent empty cells
            adjacent_cells = self.adjacent_cell_values(row, col)
            #print(adjacent_cells)
            for cell in adjacent_cells:
                if cell[0] == " ":
                    self.board[cell[1]][cell[2]] = "."

        # checks if there is water to the left or to the right of the piece
        elif col - 1 == -1 or col + 1 == 10 or \
        self.board[row][col - 1] in (".", "W") or \
        self.board[row][col + 1] in (".", "W"):
            # adds pieces if the left/right cell is empty
            if row != 9 and self.board[row+1][col] == " ":
                self.board[row+1][col] = "?"
                self.boats_cols[col] += 1
                self.boats_rows[row+1] += 1
                self.check_fill_water_row(row+1)
            if row != 0 and self.board[row-1][col] == " ":
                self.board[row-1][col] = "?"
                self.boats_cols[col] += 1
                self.boats_rows[row-1] += 1
                self.check_fill_water_row(row-1)
            self.check_fill_water_col(col)
            # adds water to the remaining adjacent empty cells
            adjacent_cells = self.adjacent_cell_values(row, col)
            for i in range(len(adjacent_cells)):
                if adjacent_cells[i][0] == " ":
                    self.board[adjacent_cells[i][1]][adjacent_cells[i][2]] = "."


    def check_fill_water_row(self, row):
        #check if the row is full of boats
        if self.rows[row] == self.boats_rows[row]:
            for i in range(10):
                if self.board[row][i] == " ":
                    self.board[row][i] = "."


    def check_fill_water_col(self, col):
        #check if the col is full of boats
        if self.cols[col] == self.boats_cols[col]:
            for i in range(10):
                if self.board[i][col] == " ":
                    self.board[i][col] = "."


    def fill_water(self):
        #this is done 1 time, in the initial check
        for i in range(10):
            if self.rows[i] == self.boats_rows[i]:
                for j in range(10):
                    if self.board[i][j] == " ":
                        self.board[i][j] = "."
            if self.cols[i] == self.boats_cols[i]:
                for j in range(10):
                    if self.board[j][i] == " ":
                        self.board[j][i] = "."
                            
                        
    def check_fill_lines(self):
        """" Checks if any column or row can be deterministically 
        filled with boat pieces. """
        # this function returns a change variable, if any change to the 
        # board was made; so, we must initialize change to False and change it  
        # to True if any change is made
        change = False
        consecutives_row, consecutives_col = 0, 0
        empties_row, empties_col = 0, 0
        lst = []
        for i in range(10):
            lst = []
            consecutives_row, consecutives_col = 0, 0
            empties_row, empties_col = 0, 0
            for j in range(10):
                if self.board[i][j] not in (".", "W"): 
                    consecutives_row += 1
                    if self.board[i][j] == " ":
                        empties_row += 1
                else: 
                    # we only allow deterministic fillings: if there are no
                    # empty cells there is nothing to fill, if there are more 
                    # than 4 consecutives, it isn't deterministic
                    if consecutives_row != 0 and consecutives_row < 5:
                        lst.append((i, j, consecutives_row))
                        consecutives_row = 0
                if self.board[j][i] not in (".", "W"): 
                    consecutives_col += 1 
                    if self.board[i][j] == " ":
                        empties_col += 1
                else: 
                    if consecutives_col != 0 and consecutives_row < 5:
                        lst.append((i, j, consecutives_col))
                        consecutives_col = 0
            if self.rows[i] - self.boats_rows[i] == empties_row:
                # places boat pieces on all empty cells
                for cell in lst:
                    if self.board[cell[0]][cell[1]] == " ":
                        adjacents = []
                        self.board[cell[0]][cell[1]] = "?"
                        self.boats_rows[cell[0]] += 1
                        self.boats_cols[cell[1]] += 1
                        self.place_water_around_unknown_piece(cell[0], cell[1], "row")
                        change = True
            if self.cols[i] - self.boats_cols[i] == empties_col:
                # places boat pieces on all empty cells
                for cell in lst:
                    if self.board[cell[0]][cell[1]] == " ":
                        self.board[cell[0]][cell[1]] = "?"
                        self.boats_rows[cell[0]] += 1
                        self.boats_cols[cell[1]] += 1
                        self.place_water_around_unknown_piece(cell[0], cell[1], "col")
                        change = True
        return change


    def place_water_around_boat(self, row: int, col: int, boat: str, size = 0):
        if boat == "C":
            self.water_C_boat(row, col)
        elif boat == "T":
            self.water_T_boat(row, col, size)
        elif boat == "L":
            self.water_L_boat(row, col, size)

    
    def water_C_boat(self, row, col):
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if i >= 0 and i < 10 and j >= 0 and j < 10 and \
                    not (i == row and j == col):
                    if self.board[i][j] == " ":
                        self.board[i][j] = "."
                    elif self.board[i][j] not in (".", "W"):
                        self.bad_board = True
                        

    def water_T_boat(self, row, col, size):
        for i in range(row - 1, row + size + 1):
            for j in range(col - 1, col + 2):
                if i >= 0 and i < 10 and j >= 0 and j < 10:
                    if not (j == col and i >= row and i < row + size):
                        if self.board[i][j] == " ":
                            self.board[i][j] = "."
                        elif self.board[i][j] not in (".", "W"):
                            self.bad_board = True
        if row - 1 >= 0:
            self.check_row_incomplete(row - 1)
        if row + 1 < 10:
            self.check_row_incomplete(row + 1)
        if col - 1 >= 0:
            self.check_col_incomplete(col - 1)
        if col + size < 10:
            self.check_col_incomplete(col + size)


    def water_L_boat(self, row, col, size):
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + size + 1):
                if i >= 0 and i < 10 and j >= 0 and j < 10:
                    if not (i == row and j >= col and j < col + size):
                        if self.board[i][j] == " ":
                            self.board[i][j] = "."
                        elif self.board[i][j] not in (".", "W"):
                            self.bad_board = True
        if col - 1 >= 0:
            self.check_col_incomplete(col - 1)
        if col + 1 < 10:
            self.check_col_incomplete(col + 1)
        if row - 1 >= 0:
            self.check_row_incomplete(row - 1)
        if row + size < 10:
            self.check_row_incomplete(row + size)


    def check_row_incomplete(self, row):
        n_spaces_left = 0
        for i in range(10):
            if self.board[row][i] == " ":
                n_spaces_left += 1
        if n_spaces_left < self.rows[row] - self.boats_rows[row]:
            self.bad_board = True


    def check_col_incomplete(self, col):
        n_spaces_left = 0
        for i in range(10):
            if self.board[i][col] == " ":
                n_spaces_left += 1
        if n_spaces_left < self.cols[col] - self.boats_cols[col]:
            self.bad_board = True


    def handle_hint(self, row: int, col: int):
        boat_piece = self.board[row][col]
        switch_case_list = {
            "C": self.initial_handle_C_boat,
            "T": self.initial_handle_T_boat,
            "L": self.initial_handle_L_boat,
            "B": self.initial_handle_B_boat,
            "R": self.initial_handle_R_boat,
            "M": self.initial_handle_M_boat
        }
        switch_case_list[boat_piece](row, col)


        #if boat == "C": 
        #    for i in range(row - 1, row + 2):
        #        for j in range(col - 1, col + 2):
        #            if i >= 0 and i < 10 and j >= 0 and j < 10:
        #                if self.board[i][j] == " ":
        #                    self.board[i][j] = "."
#
        #elif boat == "T":
        #    for i in range(row - 1, row + 3):
        #        for j in range(col - 1, col + 2):
        #            if i >= 0 and i < 10 and j >= 0 and j < 10:
        #                if not (j == col and i > row):
        #                    if self.board[i][j] == " ":
        #                        self.board[i][j] = "."
        #    if self.board[row+1][col] == " ":
        #        self.board[row+1][col] = "?"
        #        self.boats_cols[col] += 1
        #        self.boats_rows[row+1] += 1
        #        self.check_fill_water_col(col)
        #        self.check_fill_water_row(row+1)
        #    
#
        #elif boat == "B":
        #    for i in range(row - 2, row + 2):
        #        for j in range(col - 1, col + 2):
        #            if i >= 0 and i < 10 and j >= 0 and j < 10:
        #                if not (j == col and i < row):
        #                    if self.board[i][j] == " ":
        #                        self.board[i][j] = "."
        #    if self.board[row-1][col] == " ":
        #        self.board[row-1][col] = "?"
        #        self.boats_cols[col] += 1
        #        self.boats_rows[row-1] += 1
        #        self.check_fill_water_col(col)
        #        self.check_fill_water_row(row-1)
#
        #elif boat == "R":
        #    for i in range(row - 1, row + 2):
        #        for j in range(col - 2, col + 2):
        #            if i >= 0 and i < 10 and j >= 0 and j < 10:
        #                if not (i == row and j < col):
        #                    if self.board[i][j] == " ":
        #                        self.board[i][j] = "."
        #    if self.board[row][col-1] == " ":
        #        self.board[row][col-1] = "?"
        #        self.boats_cols[col-1] += 1
        #        self.boats_rows[row] += 1
        #        self.check_fill_water_col(col-1)
        #        self.check_fill_water_row(row)
#
        #elif boat == "L":
        #    for i in range(row - 1, row + 2):
        #        for j in range(col - 1, col + 3):
        #            if i >= 0 and i < 10 and j >= 0 and j < 10:
        #                if not (i == row and j > col):
        #                    if self.board[i][j] == " ":
        #                        self.board[i][j] = "."
        #    if self.board[row][col+1] == " ":
        #        self.board[row][col+1] = "?"
        #        self.boats_cols[col+1] += 1
        #        self.boats_rows[row] += 1
        #        self.check_fill_water_col(col+1)
        #        self.check_fill_water_row(row)
#
        #elif boat == "M":
        #    # checks if there is water above or under the piece
        #    if  row - 1 == -1 or row + 1 == 10 or \
        #        self.board[row - 1][col] == "." or self.board[row + 1][col] == ".":
        #        for i in range(row - 1, row + 2):
        #            for j in range(col - 2, col + 3):
        #                if i >= 0 and i < 10 and j >= 0 and j < 10 and i != row:
        #                    if self.board[i][j] == " ":
        #                        self.board[i][j] = "."
        #        # adds pieces if the up/down cell is empty
        #        if self.board[row][col+1] == " ":
        #            self.board[row][col+1] = "?"
        #            self.boats_cols[col+1] += 1
        #            self.boats_rows[row] += 1
        #            self.check_fill_water_col(col+1)
        #        if self.board[row][col-1] == " ":
        #            self.board[row][col-1] = "?"
        #            self.boats_cols[col-1] += 1
        #            self.boats_rows[row] += 1
        #            self.check_fill_water_col(col-1)
        #        self.check_fill_water_row(row)
#
        #    # checks if there is water to the left or to the right of the piece
        #    elif col - 1 == -1 or col + 1 == 10 or \
        #        self.board[row][col - 1] == "." or self.board[row][col + 1] == ".":
        #        for i in range(row - 2, row + 3):
        #            for j in range(col - 1, col + 2):
        #                if i >= 0 and i < 10 and j >= 0 and j < 10 and j != col:
        #                    if self.board[i][j] == " ":
        #                        self.board[i][j] = "."
        #        # adds pieces if the left/right cell is empty
        #        if self.board[row+1][col] == " ":
        #            self.board[row+1][col] = "?"
        #            self.boats_cols[col] += 1
        #            self.boats_rows[row+1] += 1
        #            self.check_fill_water_row(row+1)
        #        if self.board[row-1][col] == " ":
        #            self.board[row-1][col] = "?"
        #            self.boats_cols[col] += 1
        #            self.boats_rows[row-1] += 1
        #            self.check_fill_water_row(row-1)
        #        self.check_fill_water_col(col)


    def place_water_around_unknown_piece(self, row: int, col: int, direction: str):
        neighbours = self.adjacent_diagonal_values(row, col)
        if direction == "row":
            neighbours.extend(self.adjacent_vertical_values(row, col))
        else:
            neighbours.extend(self.adjacent_horizontal_values(row, col))
        for cell in neighbours:
            if cell[0] == " ":
                self.board[cell[1]][cell[2]] = "."
        #TODO verificar bad board?    



    def check_boats_on_board(self, hints):
        for h in hints:
            i = int(h[0])
            j = int(h[1])
            n = h[2]
            if n == "C":
                self.boats_on_board["1"] += 1
                self.place_water_around_boat(i, j, n)
            elif n == "T":
                if self.board[i+1][j] == "B":
                    self.boats_on_board["2"] += 1
                elif self.board[i+1][j] == "M":
                    if self.board[i+2][j] == "B":
                        self.boats_on_board["3"] += 1
                    elif self.board[i+2][j] == "M" and self.board[i+3][j] == "B":
                        self.boats_on_board["4"] += 1
            elif n == "L":
                if self.board[i][j+1] == "R":
                    self.boats_on_board["2"] += 1
                elif self.board[i][j+1] == "M":
                    if self.board[i][j+2] == "B":
                        self.boats_on_board["3"] += 1
                    elif self.board[i][j+2] == "M" and self.board[i][j+3] == "B":
                        self.boats_on_board["4"] += 1
            
                

    def endgame(self):
        for i in range(10):
            n_row = 0
            n_col = 0
            for j in range(10):
                if self.board[i][j] == " ":
                    n_row += 1
                if self.board[j][i] == " ":
                    n_col += 1
            if n_row == self.rows[i] - self.boats_rows[i]:
                for j in range(10):
                    if self.board[i][j] == " ":
                        self.board[i][j] = "c"
                        self.boats_rows[i] += 1
                        self.boats_cols[j] += 1
                        self.boats_on_board["1"] += 1
                        self.place_water_around_boat(i,j,"C")
                        self.check_fill_water_col(j)
            if n_col == self.cols[i] - self.boats_cols[i]:
                for j in range(10):
                    if self.board[j][i] == " ":
                        self.board[j][i] = "c"
                        self.boats_rows[j] += 1
                        self.boats_cols[i] += 1
                        self.boats_on_board["1"] += 1
                        self.place_water_around_boat(j,i,"C")
                        self.check_fill_water_row(j)
        if self.test_goal():
            return True
        else:
            return False
        


    def place_boat_hor(self, action: list):
        board1 = copy.deepcopy(self)
        row = action[0]
        col = action[1]
        boat_size = action[2]
        boat = ("c","lr","lmr","lmmr")
        
        for i in range(boat_size):
            if board1.board[row][col+i] == " ":
                board1.board[row][col+i] = boat[boat_size-1][i]
                board1.check_fill_water_col(col+i)
                board1.boats_cols[col+i] += 1
                board1.boats_rows[row] += 1
            elif board1.board[row][col+i] == "?":
                board1.board[row][col+i] = boat[boat_size-1][i]
            

        board1.check_fill_water_row(row)

        board1.boats_on_board[str(boat_size)] += 1
        board1.water_L_boat(row, col, boat_size)
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
                board1.check_fill_water_row(row+i)
                board1.boats_cols[col] += 1
                board1.boats_rows[row+i] += 1
            elif board1.board[row+i][col] == "?":
                board1.board[row+i][col] = boat[boat_size-1][i]
        
        board1.check_fill_water_col(col)
        
        board1.boats_on_board[str(boat_size)] += 1
        board1.water_T_boat(row, col, boat_size)
        board1.fill_water()
        return board1
    
    
    def action_boat1(self):
        actions = []
        for i in range(10):
            for j in range(10):
                if self.board[i][j] == " ":
                    actions.append([i,j,1,"d"])
        return actions
    
    
    def action_boat2(self):
        actions = []
        for i in range(10):
            for j in range(9):
                if self.rows[i] >= 2:
                    if self.board[i][j] in (" ", "?", "L"):
                        if self.board[i][j+1] in (" ", "?", "R"):
                            actions.append([i,j,2,"r"])
                if self.cols[i] >= 2:
                    if self.board[j][i] in (" ", "?", "T"):
                        if self.board[j+1][i] in (" ", "?", "B"):
                            actions.append([j,i,2,"d"])
        return actions
    

    def action_boat3(self):
        actions = []
        for i in range(10):
            for j in range(8):
                if self.rows[i] >= 3:
                    if self.board[i][j] in (" ", "?", "L"):
                        if self.board[i][j+1] in (" ", "?", "M"):
                            if self.board[i][j+2] in (" ", "?", "R"):
                                actions.append([i,j,3,"r"])
                if self.cols[i] >= 3:
                    if self.board[j][i] in (" ", "?", "T"):
                        if self.board[j+1][i] in (" ", "?", "M"):
                            if self.board[j+2][i] in (" ", "?", "B"):
                                actions.append([j,i,3,"d"])
        return actions


    def action_boat4(self):
        actions = []
        for i in range(10):
            for j in range(7): #10 - 4 + 1
                if self.rows[i] >= 4:
                    if self.board[i][j] in (" ", "?", "L"):
                        if self.board[i][j+1] in (" ", "?", "M"):
                            if self.board[i][j+2] in (" ", "?", "M"):
                                if self.board[i][j+3] in (" ", "?", "R"):
                                    actions.append([i,j,4,"r"])
                if self.cols[i] >= 4:
                    if self.board[j][i] in (" ", "?", "T"):
                        if self.board[j+1][i] in (" ", "?", "M"):
                            if self.board[j+2][i] in (" ", "?", "M"):
                                if self.board[j+3][i] in (" ", "?", "B"):
                                    actions.append([j,i,4,"d"])
        return actions

        
                

class Bimaru(Problem):
    def __init__(self, board: Board):
        self.previousStates = set()
        super().__init__(BimaruState(board))

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        #state.board.print_board()
        return state.board.test_goal()


    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        board = state.board
        actions = []

        if board.bad_board == True:
            return actions


        if board.boats_on_board["4"] < 1:
            actions += state.board.action_boat4()
        elif board.boats_on_board["3"] < 2:
            actions += state.board.action_boat3()
        elif board.boats_on_board["2"] < 3:
            actions += state.board.action_boat2()
        elif board.boats_on_board["1"] < 4:
            if state in self.previousStates:
                return actions
            else:
                self.previousStates.add(state)
            if state.board.endgame():
                return [[0,0,0,"endgame"]]
            else:
                actions += state.board.action_boat1()
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
        else: 
            return BimaruState(state.board)

 
    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
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

    x, hints = Board.parse_instance()
    x.pre_processing(hints)
    problem = Bimaru(x)
    res = depth_first_tree_search(problem)
    if res:
        res.state.board.print_board()
    else:
        print("board not printed")
    

