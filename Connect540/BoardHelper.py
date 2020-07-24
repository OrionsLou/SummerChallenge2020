from multiprocessing.pool import ThreadPool
from enum import Enum
import random
import numpy

# Simple enumeration to hold scores.
class Score(Enum):
    CENTER = 4
    LINE_OF_TWO = 2
    LINE_OF_THREE = 5
    WIN = 10000
    OPP_LINE_OF_TWO = -2
    OPP_LINE_OF_THREE = -500


class Result:

    def __init__(self, column_index, score):
        self.column_index = column_index
        self.score = score


class BoardHelper:

    def __init__(self, color):
        self.color = 'R' if color == 'red' else 'Y'
        self.enemy_color = 'Y' if color == 'red' else 'R'

        # variables to hold standard board data
        self.max_num_cells = 42
        self.max_row_index = 6
        self.max_col_index = 5

    def is_move_valid(self, colIndex, board):
        columnToCheck = board[:, colIndex]
        # print(columnToCheck)
        openSpot = False

        # column = board[:][column]
        for slot in columnToCheck:
            if slot == '-':
                openSpot = True
                # print('found a spot')
                break

        return openSpot
        # for column in zip(updated_board):
        # do_something(column)

    # Visualization only
    def display_board(self, board):
        for row in board:
            print(row)

    def __evaluate_move(self, board, column_index):
        # This is a good place to add scoring logic
        # e.g. what decides what numerical value each possible move has
        score = 0

        if self.is_move_valid(column_index, board):
            # LOGIC GOES HERE. For example, if center move then add a certain amount of points.
            # if self.is_winning_move(board, column_index):
            #     score += Score.WIN.value
            # else:
            if column_index == 3:
                score += Score.CENTER.value

            self.review_connections(board, column_index, False)

            # Temporary testing - add random value to score to produce different results.
            # score += random.randint(0, 3)
        else:
            return None

        # Do some calculations, then return column index and its score.
        return Result(column_index, score)

    def get_best_move(self, board):
        pool = ThreadPool(processes=7)
        results = []

        # Spawn 7 processes to evaluate all columns concurrently.
        proc1 = pool.apply_async(self.__evaluate_move, (board, 0))
        # proc2 = pool.apply_async(self.__evaluate_move, (board, 1))
        # proc3 = pool.apply_async(self.__evaluate_move, (board, 2))
        # proc4 = pool.apply_async(self.__evaluate_move, (board, 3))
        # proc5 = pool.apply_async(self.__evaluate_move, (board, 4))
        # proc6 = pool.apply_async(self.__evaluate_move, (board, 5))
        # proc7 = pool.apply_async(self.__evaluate_move, (board, 6))

        # Wait for the processes to finish and get results.
        results.append(proc1.get())
        # results.append(proc2.get())
        # results.append(proc3.get())
        # results.append(proc4.get())
        # results.append(proc5.get())
        # results.append(proc6.get())
        # results.append(proc7.get())

        # May need to add something here to force all processes to finish before moving further.

        # Find the best move.
        best_move = None
        for result in results:
            if best_move is None or result.score > best_move.score:
                best_move = result

        # Return column index with the best move.
        print('Best move is column {} with score {}.'.format(best_move.column_index, best_move.score))
        return best_move.column_index

    def review_connections(self, board, column_index, is_enemy):
        # Determine if dropping a piece at this column results in a connect 4
        row_index = self.__get_drop_row_index(board, column_index)
        print('Column index {} Row index {}'.format(column_index, row_index))

        # Review the column
        col_connections = self.__review_column_connections(board[:, column_index], row_index, is_enemy)
        # print('{} column connections. Is Enemy {}'.format(col_connections, is_enemy))

        # Review the row
        row_connections = self.__review_row_connections(board[row_index, :], column_index, is_enemy)
        print('{} row connections. Is Enemy {}'.format(row_connections, is_enemy))

        # Review the positive diagonal

        # Review the negative diagonal

        return True

    def __get_drop_row_index(self, board, column_index):
        # This returns the index a piece would fall to if dropped at this column.
        column = board[:, column_index]

        row_index = 0
        for x in range(0, column.size):
            if column[x] == '-':
                row_index = x
            else:
                break

        return row_index

    def __review_column_connections(self, column, row_index, is_enemy):
        num_connections = 1
        player = self.enemy_color if is_enemy else self.color

        # If this is the bottom most row in the column, we have no other pieces in this column.
        if row_index == 5:
            return num_connections

        # Otherwise, look at the rows below for connections.
        while row_index < 5:
            if column[row_index + 1] == player:
                num_connections += 1
                row_index += 1
            else:
                break

        return num_connections

    def __review_row_connections(self, row, col_index, is_enemy):
        num_connections = 1
        player = self.enemy_color if is_enemy else self.color

        # todo
        print(row)

        return num_connections