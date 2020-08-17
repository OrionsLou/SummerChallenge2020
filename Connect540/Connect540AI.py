from APIHelper import APIHelper
from BoardHelper import BoardHelper
import time

key = ''
auth = ''
opponent = 'ebot'
official = False
start_time = time.time()
poll_delay = 1
poll = True
depth = 5

# Initialize api helper with key and base64 encoded auth string
api = APIHelper(key, auth)

# Request a new game instance
api.request_game(official, opponent)
print('New game started.')
print('Game ID is {}. Player color is {}.'.format(api.game_id, api.color))

# Initialize board helper
board_helper = BoardHelper(api.color, depth)

# Try making a "flipdisk" move.
# flipdisk_json = api.flip_disk(5, 3)
# print('We made a flipdisk move. {}'.format(flipdisk_json))

# Try making a "ridrow" move.
# ridrow_json = api.rid_row(5)
# print('We made a ridrow move. {}'.format(ridrow_json))

# (WIP) Poll every minute to get the current state of the board.
while poll:

    status = api.get_game_status()
    current_board = status['board']
    poll = True
    print('Game status: {}. Winner: {}.'.format(status['status'], status['winner']))
    is_ridrow_available = board_helper.ridRowUsed(status['moves'])
    is_flipdisk_available = board_helper.flipDiskUsed(status['moves'])

   # print('moves: {}'.format(moves))
    # print('Full response: {}'.format(status['json']))

    # If no winner, make a move if player's turn.
    if status['winner'] is None:

        if status['turn'] == api.color:
            # check if move is valid
            board_helper.display_board(status['board'])


            #ridrowUsed = board_helper.ridRowUsed(moves)
            # if ridrowUsed is True:
            #     print("already used ridRow")
            # else:  
            #     print("ridRow move available")
            
            # given the current board state, get the column tha has the best move.
            # this will likely be called over and over again in minimax implementation
            best_move = board_helper.get_best_move(current_board, is_ridrow_available,is_flipdisk_available)
            best_move_column = best_move.column_index
      

            is_move_valid = board_helper.is_move_valid(best_move_column, current_board)

            if is_move_valid:
                if best_move.action == 'ridrow':
                    print('We will make a ridrow move for row_index {}'.format(best_move.row_index-1))
                    ridrow_json = api.rid_row(best_move.row_index-1)
                else:
                    drop_json = api.drop(best_move_column)
                    print('We made a drop move. {}'.format(drop_json))

            else:
                print('COLUMN IS FULL')

        # Stop execution for a certain amount of time (minus the time taken to get to this point).
        time.sleep(poll_delay - ((time.time() - start_time) % poll_delay))

    # Otherwise, game has a winner and we need to exit the loop.
    else:
        board_helper.display_board(current_board)
        print('Did we win? {}'.format(api.is_winner))
        poll = False

# Game over. Delete game.
print(api.delete_game())
