from sysassert.plugin import AssertPlugin
import logging

class DummyPlugin(AssertPlugin):

    def __init__(self):
        self.log = logging.getLogger(__name__)

    def validate(self, spec, strict=None):
        self.log.info('everything is ok')
        return True

    def generate(self):
        return {}
