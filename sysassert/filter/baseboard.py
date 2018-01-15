from sysassert.filter import FilterPlugin

class BaseboardFilter(FilterPlugin):

    #attrs_to_remove = ['asset-tag', 'serial-number']
    attrs_to_keep = ['manufacturer', 'product-name']
