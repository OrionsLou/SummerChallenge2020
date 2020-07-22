from multiprocessing.pool import ThreadPool
from enum import Enum
import random


# Simple enumeration to hold scores.
class Score(Enum):
    CENTER = 4
    LINE_OF_TWO = 2
    LINE_OF_THREE = 5
    WIN = 1000
    OPP_LINE_OF_TWO = -2
    OPP_LINE_OF_THREE = -500


class Result:

    def __init__(self, column_index, score):
        self.column_index = column_index
        self.score = score


class BoardHelper:

    def __init__(self, color):
        self.color = 'R' if color == 'red' else 'Y'

    def is_move_valid(self, colIndex, board):
        columnToCheck = board[:, colIndex]
        # print(columnToCheck)
        openSpot = False

        # column = board[:][column]
        for slot in columnToCheck:
            if slot == '-':
                openSpot = True
                print('found a spot')
                break

        return openSpot
        # for column in zip(updated_board):
        # do_something(column)

    # Visualization only
    def display_board(self, board):
        for row in board:
            print(row)

    def __evaluate_column(self, board, column_index):
        # This is a good place to add scoring logic
        # e.g. what decides what numerical value each possible move has
        score = 0

        if not self.is_move_valid(column_index, board):
            return Result(column_index, -1000)

        # LOGIC GOES HERE. For example, if center move then add a certain amount of points.
        if column_index == 3:
            score += Score.CENTER.value

        # Temporary testing - add random value to score to produce different results.
        score += random.randint(0, 3)

        # Do some calculations, then return column index and its score.
        return Result(column_index, score)

    def get_best_move(self, board):
        pool = ThreadPool(processes=7)
        results = []

        # Spawn 7 processes to evaluate all columns concurrently.
        proc1 = pool.apply_async(self.__evaluate_column, (board, 0))
        proc2 = pool.apply_async(self.__evaluate_column, (board, 1))
        proc3 = pool.apply_async(self.__evaluate_column, (board, 2))
        proc4 = pool.apply_async(self.__evaluate_column, (board, 3))
        proc5 = pool.apply_async(self.__evaluate_column, (board, 4))
        proc6 = pool.apply_async(self.__evaluate_column, (board, 5))
        proc7 = pool.apply_async(self.__evaluate_column, (board, 6))

        # Wait for the processes to finish and get results.
        results.append(proc1.get())
        results.append(proc2.get())
        results.append(proc3.get())
        results.append(proc4.get())
        results.append(proc5.get())
        results.append(proc6.get())
        results.append(proc7.get())

        # May need to add something here to force all processes to finish before moving further.

        # Find the best move.
        best_move = None
        for result in results:
            if best_move is None or result.score > best_move.score:
                best_move = result

        # Return column index with the best move.
        print('Best move is column {} with score {}.'.format(best_move.column_index, best_move.score))
        return best_move.column_index




