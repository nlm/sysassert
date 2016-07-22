from sysassert.plugin import AssertPlugin

class ProcessorPlugin(AssertPlugin):

    def validate(self, spec, strict=True):
        return self.datasource_validate('dmi', 'processor', spec, strict=strict)

    def generate(self):
        return self.datasource_generate('dmi', 'processor')
