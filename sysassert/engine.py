import logging
import pkg_resources as pkr
from voluptuous import Schema
from .plugin import AssertPlugin, ValidationResult

class SysAssert(object):

    def __init__(self, config):
        self.config = config
        self.plugins = self.load_plugins()
        self.log = logging.getLogger(__name__)

    @staticmethod
    def load_plugins():
        plugins = {}
        for entry in pkr.iter_entry_points(group='sysassert_plugin_v1'):
            plugin_class = entry.load()
            assert issubclass(plugin_class, AssertPlugin)
            plugins[entry.name] = entry.load()
        return plugins

    def validate(self):
        """
        do the actual job of validating the system
        """
        overall_status = True
        results = []

        for name, config in sorted(self.config.items()):
            self.log.debug('config section: {}'.format(name))
            if name not in self.plugins:
                self.log.error('plugin not found: {}'.format(name))
                return False
            self.log.debug('configuring plugin: {}'.format(name))
            plugin = self.plugins[name](config)
            self.log.info('===== BEGIN {} ====='.format(name.upper()))
            if plugin.validate() is False:
                overall_status = False
            self.log.info('===== END {} ====='.format(name.upper()))

        return overall_status
