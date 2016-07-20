import logging
from pprint import pformat
from sysassert.plugin import AssertPlugin

def _inline_dict(adict):
    return ', '.join(['{}: {}'.format(key, value)
                      for key, value in adict.items()])


class MemoryPlugin(AssertPlugin):

    def __init__(self, config):
        self.config = config
        self.log = logging.getLogger(__name__)

    def validate(self):
        dmi = self.get_datasource('dmi')()
        mem_devices = dmi.dmi_items('memory device')

        for wanted_device in self.config:
            self.log.debug('want device: {}'.format(pformat(wanted_device)))
            matching = False

            for real_device in mem_devices:

                matching = True
                for attr, value in wanted_device.items():
                    if real_device[attr] != value:
                        matching = False
                        break

                if matching:
                    self.log.debug('found matching device: {}'
                                   .format(pformat(real_device)))
                    self.log.info('memory device found ({})'
                                  .format(_inline_dict(wanted_device)))
                    mem_devices.remove(real_device)
                    break

            if not matching:
                return self.make_result(False, 'memory device not found', _inline_dict(wanted_device))

        if len(mem_devices) > 0:
            return self.make_result(False,
                                    '{} additional memory devices found'.format(len(mem_devices)),
                                    pformat(mem_devices))

        return self.make_result(True, 'all memory devices found')
