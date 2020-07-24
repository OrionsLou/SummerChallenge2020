from Connect540.APIHelper import APIHelper
from Connect540.BoardHelper import BoardHelper
import time

key = ''
auth = ''
opponent = 'ebot'
start_time = time.time()
poll_delay = 5
poll = True

# Initialize api helper with key and base64 encoded auth string
api = APIHelper(key, auth)

# Request a new game instance
api.request_game(opponent)
print('New game started.')
print('Game ID is {}. Player color is {}.'.format(api.game_id, api.color))

# Initialize board helper
board = BoardHelper(api.color)

# Try making a "flipdisk" move.
# flipdisk_json = api.flip_disk(5, 3)
# print('We made a flipdisk move. {}'.format(flipdisk_json))

# Try making a "ridrow" move.
# ridrow_json = api.rid_row(5)
# print('We made a ridrow move. {}'.format(ridrow_json))

# (WIP) Poll every minute to get the current state of the board.
while poll:

    status = api.get_game_status()
    poll = True
    print('Game status: {}. Winner: {}.'.format(status['status'], status['winner']))
    # print('Full response: {}'.format(status['json']))

    # If no winner, make a move if player's turn.
    if status['winner'] is None:

        if status['turn'] == api.color:
            # check if move is valid
            board.display_board(status['board'])

            # given the current board state, get the column tha has the best move.
            # this will likely be called over and over again in minimax implementation
            best_move_column = board.get_best_move(status['board'])

            is_move_valid = board.is_move_valid(best_move_column, status['board'])

            if is_move_valid:
                drop_json = api.drop(best_move_column)
                print('We made a drop move. {}'.format(drop_json))

            else:
                print('COLUMN IS FULL')

            # Stop execution for a certain amount of time (minus the time taken to get to this point).
            time.sleep(poll_delay - ((time.time() - start_time) % poll_delay))

    # Otherwise, game has a winner and we need to exit the loop.
    else:
        print('Did we win? {}'.format(api.is_winner))
        poll = False
