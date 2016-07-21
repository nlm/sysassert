from sysassert.plugin import AssertPlugin

class BIOSPlugin(AssertPlugin):

    def validate(self, spec):
        return self.datasource_validate('dmi', 'bios', spec)

    def generate(self):
        return self.datasource_generate('dmi', 'bios')
