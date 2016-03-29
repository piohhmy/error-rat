import requests

class InspectletProxy():
    def __init__(self, site_id):
        self.site_id = site_id


    def _build_url(self):
        url = 'https://api.inspectlet.com'
        resource = '/v1/websites/{}/sessions'.format(self.site_id)
        return url+resource

    def find_sessions(self, user_id, timestamp):
        url = self._build_url()
        requests.post(url)
