from sysassert.plugin.dmi import DMIPlugin

class BIOSPlugin(DMIPlugin):

    def validate(self):
        return self.dmi_validate('bios')
