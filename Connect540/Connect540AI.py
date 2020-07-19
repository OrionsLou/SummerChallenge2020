from Connect540.APIHelper import APIHelper

key = 'f3b6ece7451f1a7245d5c9508f47aee9'
auth = 'insert key here'
opponent = 'ebot'

# Initialize api helper with key and base64 encoded auth string
api = APIHelper(key, auth)

# Request a new game instance
api.request_game(opponent)
print('New game started.')
print('Game ID is {}. Player color is {}.'.format(api.game_id, api.color))

# Try making a "drop" move.
drop_json = api.drop(2)
print('We made a drop move. {}'.format(drop_json))

# Try making a "ridrow" move.
ridrow_json = api.rid_row(0)
print('We made a ridrow move. {}'.format(ridrow_json))

# Try making a "flipdisk" move.
flipdisk_json = api.flip_disk(0, 3)
print('We made a flipdisk move. {}'.format(flipdisk_json))

# Get the current state of the board.
status = api.get_game_status()
print('Game status: {}. Winner: {}.'.format(status['status'], status['winner']))
print('lol im lazy: {}'.format(status['imlazy']))
