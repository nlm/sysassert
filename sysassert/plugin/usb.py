from sysassert.plugin import AssertPlugin

class USBPlugin(AssertPlugin):

    def validate(self, spec, strict=True):
        return self.datasource_validate(spec, 'lsusb', strict=strict)

    def generate(self):
        return self.datasource_generate('lsusb')
