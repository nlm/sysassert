from sysassert.filter import FilterPlugin

class SystemFilter(FilterPlugin):

    #attrs_to_remove = ['serial-number', 'uuid']
    attrs_to_keep = ['manufacturer', 'product-name']
