import logging
import pkg_resources as pkr
from voluptuous import Schema, Required, Optional, MultipleInvalid
from .plugin import AssertPlugin
from .filter import FilterPlugin
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
        self._filters = self.load_filters()

    @property
    def plugins(self):
        """
        returns the list of loaded plugin classes
        """
        return self._plugins

    @staticmethod
    def load_plugins():
        """
        retrieves the available plugin classes registered with pkg_resources
        under the "sysassert_plugin_v1" entrypoint
        """
        plugins = {}
        for entry in pkr.iter_entry_points(group='sysassert_plugin_v1'):
            plugin_class = entry.load()
            assert issubclass(plugin_class, AssertPlugin)
            plugins[entry.name] = entry.load()
        return plugins

    @property
    def filters(self):
        """
        returns the list of loaded filter classes
        """
        return self._filters

    @staticmethod
    def load_filters():
        """
        retrieves the available filter classes registered with pkg_resources
        under the "sysassert_filter_v1" entrypoint
        """
        plugins = {}
        for entry in pkr.iter_entry_points(group='sysassert_filter_v1'):
            plugin_class = entry.load()
            assert issubclass(plugin_class, FilterPlugin)
            plugins[entry.name] = entry.load()
        return plugins

    def dependencies(self):
        """
        generates the list of shell command dependencies
        """
        for entry in pkr.iter_entry_points(group='sysassert_datasource_v1'):
            ds_class = entry.load()
            assert issubclass(ds_class, DataSource)
            yield from ds_class.get_deps()

    def lint(self, profile):
        """
        validates a profile data structure
        """
        try:
            self.schema(profile)
        except MultipleInvalid as err:
            raise Exception(err)
        return True

    def validate(self, profile):
        """
        do the actual job of validating the system
        """
        overall_status = True
        try:
            profile = self.schema(profile)
        except MultipleInvalid as exc:
            self.log.error(_('error in configuration: {0}').format(exc))

        for plugin_name, plugin_data in sorted(profile.items()):
            self.log.debug(_('config section: {0}').format(plugin_name))
            if plugin_name not in self.plugins:
                self.log.error(_('plugin not found: {0}').format(plugin_name))
                return False
            self.log.debug(_('configuring plugin: {0}').format(plugin_name))
            plugin = self.plugins[plugin_name]()
            self.log.info(_('----- BEGIN {0} -----').format(_(plugin_name).upper()))
            if plugin.validate(plugin_data['components'],
                               **plugin_data.get('params', {})) is False:
                overall_status = False
            self.log.info(_('----- END {0} -----').format(_(plugin_name).upper()))

        return overall_status

    def generate(self, plugins=None, filtered=False):
        """
        generate configuration from what was seen by plugins
        """
        results = {}

        if plugins is None or len(plugins) == 0:
            plugins = self.plugins

        for plugin_name in sorted(set(plugins)):
            self.log.debug(_('generating with plugin: {0}').format(plugin_name))
            if plugin_name not in self.plugins:
                raise KeyError(_('unknown plugin: {0}').format(plugin_name))
            plugin = self.plugins[plugin_name]()
            #results[plugin_name] = {'components': plugin.generate()}
            # filter on string type value because we don't accurately
            # compare subtables for now
            components = [{key: value
                           for key, value in entry.items()
                           if type(value) == str}
                          for entry in plugin.generate()]
            # filter components
            self.log.debug(plugin_name in self.filters)
            if filtered and plugin_name in self.filters:
                self.log.debug(_('filtering with filter: {0}'
                                 .format(plugin_name)))
                cfilter = self.filters[plugin_name]()
                components = cfilter.filtered_components(components)

            results[plugin_name] = {'components': components}

        # output must validate input schema
        return self.schema(results)
