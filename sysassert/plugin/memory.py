from sysassert.plugin.dmi import DMIPlugin

class MemoryPlugin(DMIPlugin):

    def validate(self, spec):
        return self.dmi_validate('memory device', spec)

    def generate(self):
        return self.dmi_generate('memory device')
