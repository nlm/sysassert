import pkg_resources as pkr
import logging
from ..tools import DictListComparator, inline_dict

class AssertPlugin(object):

    def __init__(self):
        self.log = logging.getLogger(__name__)

    def validate(self, spec, strict=True):
        raise NotImplementedError

    def generate(self):
        raise NotImplementedError

    @staticmethod
    def get_datasource(name):
        log = logging.getLogger(__name__)
        log.debug(_('searching datasource "{0}"').format(name))
        for entrypoint in pkr.iter_entry_points('sysassert_datasource_v1'):
            if name == entrypoint.name:
                log.debug(_('found datasource "{0}"').format(name))
                return entrypoint.load()
        log.debug('datasource "{}" not found'.format(name))
        return None

    def datasource_validate(self, spec, datasource, elttype=None, strict=True):
        items = self.get_datasource(datasource)().get_items(elttype)
        dlc = DictListComparator(spec, items)

        self.log.debug(_('validating from "{0}/{1}" datasource (strict: {2})')
                       .format(datasource,
                               elttype if elttype is not None else '',
                               strict))

        for item in dlc.found:
            self.log.info(_('found matching {0} ({1})').format(_(elttype) or _('device'),
                                                               inline_dict(item)))

        for item in dlc.missing:
            self.log.error(_('missing {0} ({1})').format(_(elttype) or _('device'),
                                                         inline_dict(item)))

        if strict:
            for item in dlc.unwanted:
                self.log.error(_('unwanted {0} ({1})').format(_(elttype) or _('device'),
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
