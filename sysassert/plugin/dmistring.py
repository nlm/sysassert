from sysassert.plugin import AssertPlugin


class ChassisPlugin(AssertPlugin):

    def validate(self, spec, strict=True):
        return self.datasource_validate(spec, 'dmistring', 'chassis',
                                        strict=strict)

    def generate(self):
        return self.datasource_generate('dmistring', 'chassis')


class SystemPlugin(AssertPlugin):

    def validate(self, spec, strict=True):
        return self.datasource_validate(spec, 'dmistring', 'system',
                                        strict=strict)

    def generate(self):
        return self.datasource_generate('dmistring', 'system')


class BaseboardPlugin(AssertPlugin):

    def validate(self, spec, strict=True):
        return self.datasource_validate(spec, 'dmistring', 'baseboard',
                                        strict=strict)

    def generate(self):
        return self.datasource_generate('dmistring', 'baseboard')
