import requests
from requests.auth import HTTPBasicAuth
import json

class InspectletProxy():
    def __init__(self, site_id, user, token):
        self.site_id = site_id
        self.auth = HTTPBasicAuth(user, token)


    def _build_url(self):
        url = 'https://api.inspectlet.com'
        resource = '/v1/websites/{}/sessions'.format(self.site_id)
        return url+resource

    def find_sessions(self, user_id, timestamp):
        url = self._build_url()
        resp = requests.post(url, auth=self.auth, data=self._build_data(user_id, timestamp))
        return self._session_links_from(resp.json())


    def _session_links_from(self, json):#, timestamp):
        sessions = json['response']['sessions']
        for session in sessions:
            #err_pages = [p for p in session['pages'] if p['opened_at'] < timestamp]
            #err_page_num = len(err_pages)
            #yield session['sessionlink'].replace('pn=1', 'pn=' + str(err_page_num))
            return [session['sessionlink']]


    def _build_data(self, user_id, timestamp):
        search = {'displayname': user_id,
                  'daterange': 'custom',
                  'daterangecustom': {
                      'start': str(timestamp), 'end': str(timestamp)}
                  }
        return {'search': json.dumps(search)}
