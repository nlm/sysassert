import logging
from sysassert.plugin import AssertPlugin

class DummyPlugin(AssertPlugin):

    def __init__(self):
        self.log = logging.getLogger(__name__)

    def validate(self, spec):
        self.log.info('everything is ok')
        return True

    def generate(self):
        return {}
