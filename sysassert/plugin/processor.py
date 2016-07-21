from sysassert.plugin import AssertPlugin

class ProcessorPlugin(AssertPlugin):

    def validate(self, spec):
        return self.datasource_validate('dmi', 'processor', spec)

    def generate(self):
        return self.datasource_generate('dmi', 'processor')
