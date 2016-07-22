from sysassert.plugin import AssertPlugin

class BIOSPlugin(AssertPlugin):

    def validate(self, spec, strict=True):
        return self.datasource_validate(spec, 'dmi', 'bios', strict=strict)

    def generate(self):
        return self.datasource_generate('dmi', 'bios')
