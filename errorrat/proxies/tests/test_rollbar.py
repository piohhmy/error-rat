import datetime
from unittest import TestCase
from unittest.mock import patch, Mock
from errorrat.proxies.rollbar import RollbarProxy, requests
from nose.tools import assert_equal, assert_raises
from requests.auth import HTTPBasicAuth
import json


def dummy_resp(user='userid1', ts=1459953157):
    resp = Mock()
    resp.json.return_value = {'err': 0,
           'result': {'data': {
                               'environment': 'sellery',
                               'framework': 'browser-js',
                               'language': 'javascript',
                               'level': 'warning',
                               'person': {'email': 'nnkkuja@gmail.com', 'id': user, 'userId': 3952},
                               'platform': 'browser',
                               'request': {'query_string': '',
                                           'url': 'https://sellery.sellerengine.com/se2/',
                                           'user_ip': '68.46.5.101'},
                               'timestamp': ts
                               },
                      'id': 12534393530,
                      'timestamp': ts,
                      }}
    return resp

def proxy_factory(token='fake_token'):
    return RollbarProxy(token)



@patch.object(requests, 'get', return_value=dummy_resp())
class TestRollbarProxy(TestCase):
    def test_getOccurrence_buildsUrlWithToken(self, mockrequests):
        token = 'TOKEN'
        occurence_id = 'ID1'

        rb = proxy_factory(token)
        rb.get_occurrence(occurence_id)

        expected_url = ('https://api.rollbar.com/api/1/instance/' +
                        occurence_id + '?access_token=' + token)

        mockrequests.assert_called_once_with(expected_url)

    def test_getOccurrence_returnsUser(self, mockrequests):
        rb = proxy_factory()
        user = 'userid'
        mockrequests.return_value = dummy_resp(user)

        occur = rb.get_occurrence('id1')

        assert_equal(user, occur.user_id)

    def test_getOccurrence_returnsTimestamp(self, mockrequests):
        rb = proxy_factory()
        ts = 1234567
        mockrequests.return_value = dummy_resp(ts=ts)

        occur = rb.get_occurrence('id1')

        assert_equal(ts, occur.timestamp)

    def test_getOccurrence_noPerson_nullUser(self, mockrequests):
        rb = proxy_factory()
        resp = dummy_resp()
        del(resp.json()['result']['data']['person'])
        mockrequests.return_value = resp

        occur = rb.get_occurrence('id1')

        assert_equal(None, occur.user_id)

    def test_httpError_raise(self, mockrequests):
        rb = proxy_factory()
        mock_resp = Mock()
        mock_resp.raise_for_status.side_effect = requests.HTTPError
        mockrequests.return_value = mock_resp

        with assert_raises(requests.HTTPError):
            rb.get_occurrence('id1')
