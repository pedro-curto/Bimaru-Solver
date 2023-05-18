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
    def __init__(self,rows: list, cols: list, board: list) -> None:
        self.board = board
        self.rows = rows
        self.cols = cols
        pass

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        # TODO
        pass

    def adjacent_vertical_values(self, row: int, col: int):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        # TODO
        pass

    def adjacent_horizontal_values(self, row: int, col: int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        # TODO
        pass

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
        pass

            

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
            if n != "W":
                rows[x] -= 1
                cols[y] -= 1
            

        for i in range(10):
            if rows[i] == 0:
                for j in range(10):
                    if board[i][j] == " ":
                        board[i][j] = "."
            if cols[i] == 0:
                for j in range(10):
                    if board[j][i] == " ":
                        board[j][i] = "."

        

        
        print("rows:", rows, "\ncolumns:", cols, "\nhints:", hints)

        
        return Board(rows,cols,board)

    # TODO: outros metodos da classe


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO
        pass

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

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.

    x = Board.parse_instance()
    x.print_board()



    pass
