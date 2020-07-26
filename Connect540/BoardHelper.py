from multiprocessing.pool import ThreadPool
from enum import Enum


# Simple enumeration to hold scores.
class Score(Enum):
    CENTER = 4
    LINE_OF_TWO = 3
    LINE_OF_THREE = 5
    WIN = 10000
    OPP_LINE_OF_TWO = 0
    OPP_LINE_OF_THREE = 500


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

    def get_best_move(self, board):
        pool = ThreadPool(processes=7)
        results = []

        # Spawn 7 processes to evaluate all columns concurrently.
        proc1 = pool.apply_async(self.__evaluate_move, (board, 0))
        proc2 = pool.apply_async(self.__evaluate_move, (board, 1))
        proc3 = pool.apply_async(self.__evaluate_move, (board, 2))
        proc4 = pool.apply_async(self.__evaluate_move, (board, 3))
        proc5 = pool.apply_async(self.__evaluate_move, (board, 4))
        proc6 = pool.apply_async(self.__evaluate_move, (board, 5))
        proc7 = pool.apply_async(self.__evaluate_move, (board, 6))

        # Wait for the processes to finish and get results.
        result1 = proc1.get()
        result2 = proc2.get()
        result3 = proc3.get()
        result4 = proc4.get()
        result5 = proc5.get()
        result6 = proc6.get()
        result7 = proc7.get()

        # These lines are for testing only. Performs evaluations one at a time. Easier to read debug lines.
        # result1 = self.__evaluate_move(board, 0)
        # result2 = self.__evaluate_move(board, 1)
        # result3 = self.__evaluate_move(board, 2)
        # result4 = self.__evaluate_move(board, 3)
        # result5 = self.__evaluate_move(board, 4)
        # result6 = self.__evaluate_move(board, 5)
        # result7 = self.__evaluate_move(board, 6)

        # Don't review results where the move is invalid (no result)
        if result1 is not None:
            results.append(result1)
        if result2 is not None:
            results.append(result2)
        if result3 is not None:
            results.append(result3)
        if result4 is not None:
            results.append(result4)
        if result5 is not None:
            results.append(result5)
        if result6 is not None:
            results.append(result6)
        if result7 is not None:
            results.append(result7)

        # Find the best move.
        best_move = None
        for result in results:
            if best_move is None or result.score > best_move.score:
                best_move = result

        # Return column index with the best move.
        print('Best move is column {} with score {}.'.format(best_move.column_index, best_move.score))
        return best_move.column_index

    def __evaluate_move(self, board, column_index):
        # This is a good place to add scoring logic
        # e.g. what decides what numerical value each possible move has
        score = 0

        if self.is_move_valid(column_index, board):
            # LOGIC GOES HERE. For example, if center move then add a certain amount of points.
            if column_index == 3:
                score += Score.CENTER.value

            score += self.__calculate_score(board, column_index, False)

            # Temporary testing - add random value to score to produce different results.
            # score += random.randint(0, 3)
        else:
            return None

        # Do some calculations, then return column index and its score.
        return Result(column_index, score)

    def __calculate_score(self, board, column_index, is_enemy):
        score = 0

        # Get the row the disc would drop to if dropped in this column.
        row_index = self.__get_drop_row_index(board, column_index)

        # Review the column for the current move being analyzed
        score += self.__review_column_connections(board[:, column_index], row_index, is_enemy)
        # print('{} column connections. Is Enemy {}'.format(col_connections, is_enemy))

        # Review the row for the current move being analyzed IF dropping a move will land on this row
        score += self.__review_row_connections(board[row_index, :], column_index, is_enemy)
        # print('{} row connections. Is Enemy {}'.format(row_connections, is_enemy))

        # Review the positive diagonal
        # todo

        # Review the negative diagonal
        # todo

        # Review flip disk
        # todo

        # Review rid row
        # todo

        return score

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

    def __map_connection_to_score(self, player_connections, enemy_connections):
        score = 0
        if player_connections == 4:  # Win is most important
            score = Score.WIN.value
        elif enemy_connections == 3:  # Blocking enemy win is second most important
            score = Score.OPP_LINE_OF_THREE.value

        # From here, can be re-ordered to prioritize blocking opponent line of two or creating player line of three
        elif player_connections == 3:
            score = Score.LINE_OF_THREE.value
        elif enemy_connections == 2:
            score = Score.OPP_LINE_OF_TWO.value
        elif player_connections == 2:
            score = Score.LINE_OF_TWO.value

        return score

    def __review_column_connections(self, column, row_index, is_enemy):
        num_connections = 1
        enemy_connections = 0
        player = self.enemy_color if is_enemy else self.color

        # If this is the bottom most row in the column, we have no other pieces in this column.
        if row_index == 5:
            score = self.__map_connection_to_score(num_connections, 0)
            # print('col! row {} player {} enemy {}'.format(row_index, num_connections, enemy_connections))
            # print('col! column {}'.format(column))
            # print('col! column score {}'.format(score))
            return score

        # Check next disc to see if we count player connections or enemy connections
        has_connection = False
        if column[row_index + 1] == player:
            has_connection = True

        if has_connection:
            for x in range(1, 4):
                next_index = row_index + x
                if next_index <= 5:
                    if column[next_index] == player:
                        # Count number of player connections
                        num_connections += 1
                    else:
                        # We hit an enemy disc. Stop counting discs.
                        break
                else:
                    # We hit the bottom of the column.
                    break
        else:
            for x in range(1, 4):
                next_index = row_index + x
                if next_index <= 5:
                    if column[next_index] != player:
                        # Count number of enemy connections
                        enemy_connections += 1
                    else:
                        # Hit player connection, stop counting enemy connections
                        break
                else:
                    # We hit the bottom of the column.
                    break

        # If there are not enough cells in this column to create a winning move, don't bother making a move here.
        if row_index - (4 - num_connections) < 0:
            num_connections = 0

        # If there are any enemy discs in this 4-cell combo, then we can't do a winning move on this column.
        if has_connection:
            score = self.__map_connection_to_score(num_connections, 0)
        else:
            score = self.__map_connection_to_score(0, enemy_connections)

        # print('col! row {} player {} enemy {}'.format(row_index, num_connections, enemy_connections))
        # print('col! column {}'.format(column))
        # print('col! column score {}'.format(score))
        return score

    def __review_row_connections(self, row, col_index, is_enemy):
        player = self.enemy_color if is_enemy else self.color

        # Determine the window of cells we need to review.
        min_index = 0 if col_index - 3 <= 0 else col_index - 3
        max_index = 6 if col_index + 3 >= 6 else col_index + 3

        max_score = 0
        # Check all 4-cell combos inside this window
        while min_index + 3 <= max_index:
            # print('new combo')
            num_connections = 0
            enemy_connections = 0
            for offset in range(0, 4):
                current_index = min_index + offset
                # print(row[current_index])
                if col_index == current_index:
                    # print('col index')
                    num_connections += 1
                elif row[current_index] == player:
                    # print('{} == {}'.format(row[current_index], player))
                    num_connections += 1
                elif row[current_index] == '-':
                    # print('empty')
                    continue
                else:
                    enemy_connections += 1

            # If there are any enemy discs in this 4-cell combo, then we can't do a winning move on this row.
            # print('row! col {} player {} enemy {}'.format(col_index, num_connections, enemy_connections))
            if enemy_connections == 0:
                score = self.__map_connection_to_score(num_connections, 0)
            else:
                score = self.__map_connection_to_score(0, enemy_connections)

            max_score = max(max_score, score)
            min_index += 1

        # print('row {} {} {} {} {} {} {}'.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

        # print('row! row {}'.format(row))
        # print('row! row score {}'.format(max_score))
        return max_score
