import datetime
from unittest import TestCase
from unittest.mock import patch, Mock
from errorrat.proxies.inspectlet import InspectletProxy, requests
from nose.tools import assert_equal
from requests.auth import HTTPBasicAuth
import json

def dummy_session(sessionlink='http://inspectlet.com/session?pn=1', timestamps=[1]):
    session = {'sessionlink': sessionlink, 'pages': []}
    for ts in timestamps:
        session['pages'].append({'opened_at': ts})
    return session


def dummy_resp(sessionlink='http://inspectlet.com/session?pn=1', timestamps=[1]):
    json = {'response': {'sessions': [dummy_session(sessionlink, timestamps)]}}
    mock_resp = Mock()
    mock_resp.json.return_value = json

    return mock_resp


def proxy_factory(site_id='fake_site_id', user='fake_user', token='fake_token'):
    return InspectletProxy(site_id, user, token)


@patch.object(requests, 'post', return_value=dummy_resp())
class TestInspectletProxy(TestCase):
    def setUp(self):

        pass

    def test_findSessions_buildsUrlWithSiteId(self, mockrequests):
        site_id = '11111'
        proxy = proxy_factory(site_id=site_id)

        proxy.find_sessions('user', 100)

        actual_url = mockrequests.call_args[0][0]
        expected_url = 'https://api.inspectlet.com/v1/websites/{}/sessions'.format(site_id)
        assert_equal(expected_url, actual_url)


    def test_findSessions_setsHttpAuth(self, mockrequests):
        user = 'fake insp user'
        token = 'fake token'
        proxy = proxy_factory(user=user, token=token)

        proxy.find_sessions('user', 100)

        actual_auth = mockrequests.call_args[1]['auth']
        expected_auth = HTTPBasicAuth(user, token)
        assert_equal(expected_auth.username, actual_auth.username)
        assert_equal(expected_auth.password, actual_auth.password)


    def test_findSessions_buildsSearchRequest(self, mockrequests):
        proxy = proxy_factory()
        user = 'fakeuserid'
        time = 123

        proxy.find_sessions(user, time)

        data = mockrequests.call_args[1]['data']
        search = json.loads(data['search'])
        assert_equal(search['displayname'], user)
        assert_equal(search['daterange'], 'custom')
        assert_equal(search['daterangecustom']['start'], str(time))
        assert_equal(search['daterangecustom']['end'], str(time))


    def test_findSessions_1sessionFound_returnsSession(self, mockrequests):
        expected_session = 'http://test.com/session/1?pn=1'
        mockrequests.return_value = dummy_resp(expected_session)
        proxy = proxy_factory()

        actual_sessions = proxy.find_sessions(1, 100)

        assert_equal([expected_session], actual_sessions)


    def test_findSessions_2sessionsFound_returnsSessions(self, mockrequests):
        expected_session1 = 'http://test.com/session/1?pn=1'
        expected_session2 = 'http://test.com/session/2?pn=1'
        resp = dummy_resp(expected_session1)
        resp.json()['response']['sessions'].append(dummy_session(expected_session2))
        mockrequests.return_value = resp
        proxy = proxy_factory()

        actual_sessions = proxy.find_sessions(1, 100)

        assert_equal([expected_session1, expected_session2], actual_sessions)


    def test_findSessions_midsession_returnCorrectPage(self, mockrequests):
        session = 'http://test.com/session/1?pn=1'
        pages = [100,200,300]
        resp = dummy_resp(session, pages)
        mockrequests.return_value = resp
        proxy = proxy_factory()

        actual_sessions = proxy.find_sessions(1, 250)

        expected_session = 'http://test.com/session/1?pn=2'
        assert_equal([expected_session], actual_sessions)
