from sysassert.plugin import AssertPlugin

class DiskPlugin(AssertPlugin):

    def validate(self, spec, strict=True):
        return self.datasource_validate('lsblk', 'disk', spec, strict=strict)

    def generate(self):
        return self.datasource_generate('lsblk', 'disk')
