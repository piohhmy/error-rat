import unittest
from datetime import datetime
from unittest.mock import Mock

from errorrat.processor import Rb2Insp, RollbarOccurrence


def create_occurrence(user_id=1, ts=datetime.now()):
    return RollbarOccurrence(user_id, ts)

class TestProcessor(unittest.TestCase):
    def test_rb2insp_retrievesInspSessions(self):
        rb_o = create_occurrence()
        insp_proxy = Mock()
        insp_proxy.find_sessions.return_value = []
        rb_proxy = Mock()

        p = Rb2Insp(rb_proxy, insp_proxy)
        p.process(rb_o)

        insp_proxy.find_sessions.assert_called_once_with(rb_o.user_id, rb_o.timestamp)


    def test_rb2insp_postsRbCommentWithSession(self):
        rb_o = create_occurrence()
        insp_proxy = Mock()
        rb_proxy = Mock()
        fake_session = 'http://inspectlet.com/watch/123'
        insp_proxy.find_sessions.return_value = [fake_session]

        p = Rb2Insp(rb_proxy, insp_proxy)
        p.process(rb_o)

        rb_proxy.post_comment.assert_called_once_with('Inspectlet Session: {}'.format(fake_session))



