import logging
import pkg_resources as pkr
from voluptuous import Schema, Required, Optional, MultipleInvalid
from .plugin import AssertPlugin
from .datasource import DataSource

class SysAssert(object):

    schema = Schema({
        str: {
            Optional('params'): {'strict': bool},
            Required('components'): [dict],
        }
    })

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self._plugins = self.load_plugins()

    @property
    def plugins(self):
        return self._plugins

    @staticmethod
    def load_plugins():
        plugins = {}
        for entry in pkr.iter_entry_points(group='sysassert_plugin_v1'):
            plugin_class = entry.load()
            assert issubclass(plugin_class, AssertPlugin)
            plugins[entry.name] = entry.load()
        return plugins

    def dependencies(self):
        """
        get the list of shell command dependencies
        """
        for entry in pkr.iter_entry_points(group='sysassert_datasource_v1'):
            ds_class = entry.load()
            assert issubclass(ds_class, DataSource)
            yield from ds_class.get_deps()

    def validate(self, profile):
        """
        do the actual job of validating the system
        """
        overall_status = True
        try:
            profile = self.schema(profile)
        except MultipleInvalid as exc:
            self.log.error('error in configuration: {}'.format(exc))

        for plugin_name, plugin_data in sorted(profile.items()):
            self.log.debug('config section: {}'.format(plugin_name))
            if plugin_name not in self.plugins:
                self.log.error('plugin not found: {}'.format(plugin_name))
                return False
            self.log.debug('configuring plugin: {}'.format(plugin_name))
            plugin = self.plugins[plugin_name]()
            self.log.info('===== BEGIN {} ====='.format(plugin_name.upper()))
            if plugin.validate(plugin_data['components'],
                               **plugin_data.get('params', {})) is False:
                overall_status = False
            self.log.info('===== END {} ====='.format(plugin_name.upper()))

        return overall_status

    def generate(self, plugins=None):
        """
        generate configuration from what was seen by plugins
        """
        results = {}

        if plugins is None or len(plugins) == 0:
            plugins = self.plugins

        for plugin_name in sorted(set(plugins)):
            self.log.debug('generating with plugin: {}'.format(plugin_name))
            if plugin_name not in self.plugins:
                raise KeyError('unknown plugin: {}'.format(plugin_name))
            plugin = self.plugins[plugin_name]()
            #results[plugin_name] = {'components': plugin.generate()}
            # filter on string type value because we don't accurately
            # compare subtables for now
            components = [{key: value
                           for key, value in entry.items()
                           if type(value) == str}
                          for entry in plugin.generate()]
            results[plugin_name] = {'components': components}

        # output must validate input schema
        return self.schema(results)
