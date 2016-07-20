import logging
from sysassert.plugin import AssertPlugin
from sysassert.tools import inline_dict, DictListComparator

class DMIPlugin(AssertPlugin):

    def __init__(self, config):
        self.config = config
        self.log = logging.getLogger(__name__)

    def dmi_validate(self, elttype):
        dmi = self.get_datasource('dmi')()
        dmi_items = dmi.dmi_items(elttype)
        dlc = DictListComparator(self.config, dmi_items)

        for item in dlc.found:
            self.log.info('found matching {} ({})'.format(elttype,
                                                          inline_dict(item)))

        for item in dlc.missing:
            self.log.error('missing {} ({})'.format(elttype, inline_dict(item)))

        for item in dlc.unwanted:
            self.log.error('unwanted {} ({})'.format(elttype,
                                                     inline_dict(item)))

        return (len(dlc.found) > 0
                and len(dlc.missing) == 0
                and len(dlc.unwanted) == 0)

