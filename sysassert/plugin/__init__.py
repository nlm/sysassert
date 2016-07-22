import pkg_resources as pkr
import logging
from ..tools import DictListComparator, inline_dict

class AssertPlugin(object):

    def __init__(self):
        self.log = logging.getLogger()

    def validate(self, spec, strict=True):
        raise NotImplemented

    def generate(self):
        raise NotImplemented

    @staticmethod
    def get_datasource(name):
        for entrypoint in pkr.iter_entry_points('sysassert_datasource_v1'):
            if name == entrypoint.name:
                return entrypoint.load()
        return None

    def datasource_validate(self, spec, datasource, elttype=None, strict=True):
        items = self.get_datasource(datasource)().get_items(elttype)
        dlc = DictListComparator(spec, items)

        for item in dlc.found:
            self.log.info('found matching {} ({})'.format(elttype or 'device',
                                                          inline_dict(item)))

        for item in dlc.missing:
            self.log.error('missing {} ({})'.format(elttype or 'device',
                                                    inline_dict(item)))

        if strict:
            for item in dlc.unwanted:
                self.log.error('unwanted {} ({})'.format(elttype or 'device',
                                                         inline_dict(item)))

        if strict:
            return len(dlc.missing) == 0 and len(dlc.unwanted) == 0
        else:
            return len(dlc.missing) == 0

    def datasource_generate(self, datasource, elttype=None):
        """
        generate a plugin from a datasource
        """
        return self.get_datasource(datasource)().get_items(elttype)
