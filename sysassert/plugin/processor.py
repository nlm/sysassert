import logging
from sysassert.plugin import AssertPlugin
from sysassert.tools import inline_dict, DictListComparator

class ProcessorPlugin(AssertPlugin):

    def __init__(self, config):
        self.config = config
        self.log = logging.getLogger(__name__)

    def validate(self):
        dmi = self.get_datasource('dmi')()
        processors = dmi.dmi_items('processor')
        dlc = DictListComparator(self.config, processors)

        for item in dlc.found:
            self.log.info('found matching processor ({})'.format(inline_dict(item)))

        for item in dlc.missing:
            self.log.error('missing processor ({})'.format(inline_dict(item)))

        for item in dlc.unwanted:
            self.log.error('unwanted processor ({})'.format(inline_dict(item)))

        return self.make_result(len(dlc.found) > 0 and len(dlc.missing) == 0 and len(dlc.unwanted) == 0)
