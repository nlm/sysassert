from sysassert.plugin.dmi import DMIPlugin

class ProcessorPlugin(DMIPlugin):

    def validate(self):
        return self.dmi_validate('processor')
