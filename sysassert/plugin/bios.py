from sysassert.plugin.dmi import DMIPlugin

class BIOSPlugin(DMIPlugin):

    def validate(self, spec):
        return self.dmi_validate('bios', spec)

    def generate(self):
        return self.dmi_generate('bios')
