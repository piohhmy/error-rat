from collections import namedtuple

RollbarOccurrence = namedtuple('RollbarOccurrence', ['user_id', 'timestamp'])

class Rb2Insp():
    def __init__(self, rb_proxy, insp_proxy):
        self.insp_proxy = insp_proxy
        self.rb_proxy = rb_proxy

    def process(self, occur):
        sessions = self.insp_proxy.find_sessions(occur.user_id, occur.timestamp)
        if sessions:
            self.rb_proxy.post_comment('Inspectlet Session: {}'.format(sessions[0]))
