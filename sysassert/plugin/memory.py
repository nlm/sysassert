from sysassert.plugin import AssertPlugin

class MemoryPlugin(AssertPlugin):

    def validate(self, spec):
        return self.datasource_validate('dmi', 'memory device', spec)

    def generate(self):
        return self.datasource_generate('dmi', 'memory device')
