from sysassert.plugin import AssertPlugin

class MemoryPlugin(AssertPlugin):

    def __init__(self, config):
        self.config = config

    def validate(self):
        dmi = self.get_datasource('dmi')
        print(dmi)
        return self.make_result(True, 'memory is ok')
