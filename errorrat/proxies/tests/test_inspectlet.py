import datetime
from unittest import TestCase
from unittest.mock import patch
from errorrat.proxies.inspectlet import InspectletProxy, requests
from nose.tools import assert_equal

def dummy_resp():
    return {}

class TestInspectletProxy(TestCase):
    def test_getSessions_buildsUrlWithSiteId(self):
        site_id = '11111'
        proxy = InspectletProxy(site_id)

        with patch.object(requests, 'post', return_value=dummy_resp()):
            proxy.find_sessions('user', datetime.datetime.now())
            actual_url = requests.post.call_args[0][0]

        expected_url = 'https://api.inspectlet.com/v1/websites/{}/sessions'.format(site_id)
        assert_equal(expected_url, actual_url)

