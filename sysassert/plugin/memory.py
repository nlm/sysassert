import logging
from sysassert.plugin import AssertPlugin
from sysassert.tools import inline_dict, DictListComparator

class MemoryPlugin(AssertPlugin):

    def __init__(self, config):
        self.config = config
        self.log = logging.getLogger(__name__)

    def validate(self):
        dmi = self.get_datasource('dmi')()
        mem_devices = dmi.dmi_items('memory device')
        dlc = DictListComparator(self.config, mem_devices)

        for item in dlc.found:
            self.log.info('found matching memory device ({})'.format(inline_dict(item)))

        for item in dlc.missing:
            self.log.error('missing memory device ({})'.format(inline_dict(item)))

        for item in dlc.unwanted:
            self.log.error('unwanted memory device ({})'.format(inline_dict(item)))

        return len(dlc.found) > 0 and len(dlc.missing) == 0 and len(dlc.unwanted) == 0
