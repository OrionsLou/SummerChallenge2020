import requests
import json


class APIHelper:
    url = 'https://api.sg2020.540.co/fun/games'

    def __init__(self, key, auth):
        self.key = key
        self.auth = auth
        self.game_id = ''
        self.color = ''

    def request_game(self, opponent):
        r = requests.post(self.url + '?opponent=' + opponent,
                          headers={'X-API-Key': self.key, 'Content-Type': 'application/json',
                                   'Accept': 'application/json',
                                   'Authorization': self.auth})
        response_json = r.json()
        self.game_id = response_json['data']['_id']
        self.color = 'yellow' if self.key == response_json['data']['yellow'] else 'red'

    def drop(self, column):
        move_data = json.dumps({'data': {'type': 'drop', 'column': column}})
        response_json = self.__make_move(move_data)
        return response_json

    def rid_row(self, row):
        move_data = json.dumps({'data': {'type': 'ridrow', 'row': row}})
        response_json = self.__make_move(move_data)
        return response_json

    def flip_disk(self, row, column):
        move_data = json.dumps({'data': {'type': 'flipdisk', 'row': row}, 'column': column})
        response_json = self.__make_move(move_data)
        return response_json

    def __make_move(self, move_data):
        move_response = requests.post('https://api.sg2020.540.co/fun/games/{}/moves'.format(self.game_id),
                                      headers={'X-API-Key': self.key, 'Content-Type': 'application/json', 'Accept': 'application/json','Authorization': self.auth},
                                      data=move_data)
        return move_response.json()

    def get_game_status(self):
        response = requests.get('https://api.sg2020.540.co/fun/games/{}'.format(self.game_id),
                                headers={'X-API-Key': self.key, 'Content-Type': 'application/json', 'Accept': 'application/json','Authorization': self.auth})
        r_json = response.json()
        status_dictionary = {
            'status': r_json['data']['status'],
            'winner': r_json['data']['winner'],
            'imlazy': r_json
        }
        return status_dictionary
