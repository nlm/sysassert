from sysassert.plugin import AssertPlugin

class DiskPlugin(AssertPlugin):

    def validate(self, spec):
        return self.datasource_validate('lsblk', 'disk', spec)

    def generate(self):
        return self.datasource_generate('lsblk', 'disk')
