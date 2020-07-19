from Connect540.APIHelper import APIHelper
import time

key = 'f3b6ece7451f1a7245d5c9508f47aee9'
auth = 'insert key here'
opponent = 'ebot'
start_time = time.time()
poll = True

# Initialize api helper with key and base64 encoded auth string
api = APIHelper(key, auth)

# Request a new game instance
api.request_game(opponent)
print('New game started.')
print('Game ID is {}. Player color is {}.'.format(api.game_id, api.color))

# Try making a "flipdisk" move.
flipdisk_json = api.flip_disk(5, 3)
print('We made a flipdisk move. {}'.format(flipdisk_json))

# Try making a "ridrow" move.
ridrow_json = api.rid_row(5)
print('We made a ridrow move. {}'.format(ridrow_json))

# (WIP) Poll every minute to get the current state of the board.
while poll:
    status = api.get_game_status()
    print('Game status: {}. Winner: {}.'.format(status['status'], status['winner']))
    print('lol im lazy: {}'.format(status['imlazy']))

    # If no winner, make a move if player's turn.
    if status['winner'] is None:

        if status['turn'] == api.color:
            # Insert decision making process here? For the time being, just do a drop move.
            drop_json = api.drop(2)
            print('We made a drop move. {}'.format(drop_json))

        # Stop execution for a minute (minus the time taken to get to this point).
        time.sleep(60 - ((time.time() - start_time) % 60))

    # Otherwise, game has a winner and we need to exit the loop.
    else:
        print('Did we win? {}'.format(api.is_winner))
        poll = False

