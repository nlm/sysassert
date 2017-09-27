class FilterPlugin(object):

    attrs_to_remove = None
    attrs_to_keep = None

    def filtered_components(self, components_data):
        """
        syntaxic sugar to filter a list of components
        """
        return [self.filtered_component(component)
                for component in components_data]

    def filtered_component(self, component_data):
        """
        takes a standard sysassert component
        and returns a filtered component
        """
        return {key: value for key, value in component_data.items()
                if ((self.attrs_to_remove is None
                     or key not in self.attrs_to_remove)
                    and (self.attrs_to_keep is None
                         or key in self.attrs_to_keep))}
