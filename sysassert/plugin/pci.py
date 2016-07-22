from sysassert.plugin import AssertPlugin

class PCIPlugin(AssertPlugin):

    def validate(self, spec, strict=True):
        return self.datasource_validate(spec, 'lspci', strict=strict)

    def generate(self):
        return self.datasource_generate('lspci')
