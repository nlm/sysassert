from sysassert.plugin import AssertPlugin

class DummyPlugin(AssertPlugin):

    def __init__(self, config):
        pass

    def validate(self):
        return self.make_result(True, 'it\'s fine')
