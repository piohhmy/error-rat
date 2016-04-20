import requests
from collections import namedtuple

RollbarOccurrence = namedtuple('RollbarOccurrence', ['user_id', 'timestamp'])

class RollbarProxy():
    def __init__(self, access_token):
        self.access_token = access_token

    def get_occurrence(self, occurrence_id):
        json = self._send_request(occurrence_id)
        return self._create_occurrence_from(json)

    def _create_occurrence_from(self, json):
        data = json['result']['data']
        if data.get('person') and data['person'].get('id'):
            user_id = data['person']['id']
        else:
            user_id = None
        ts = data['timestamp']
        return RollbarOccurrence(user_id, ts)

    def _send_request(self, occurrence_id):
        url = self._build_url(occurrence_id)
        result = requests.get(url)
        result.raise_for_status()
        json = result.json()
        return json

    def _build_url(self, occurrence_id):
        url = 'https://api.rollbar.com'
        resource = '/api/1/instance/{}'.format(occurrence_id)
        query_string = 'access_token={}'.format(self.access_token)
        return '{}{}?{}'.format(url, resource, query_string)


