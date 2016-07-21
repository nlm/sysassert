from sysassert.plugin.dmi import DMIPlugin

class ProcessorPlugin(DMIPlugin):

    def validate(self, spec):
        return self.dmi_validate('processor', spec)

    def generate(self):
        return self.dmi_generate('processor')
