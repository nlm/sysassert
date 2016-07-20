from sysassert.plugin.dmi import DMIPlugin

class MemoryPlugin(DMIPlugin):

    def validate(self):
        return self.dmi_validate('memory device')
