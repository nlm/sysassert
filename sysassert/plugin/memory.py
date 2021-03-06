from sysassert.plugin import AssertPlugin

class MemoryPlugin(AssertPlugin):

    def validate(self, spec, strict=True):
        return self.datasource_validate(spec, 'dmi', 'memory device',
                                        strict=strict)

    def generate(self):
        return self.datasource_generate('dmi', 'memory device')
