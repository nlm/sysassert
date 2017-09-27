from sysassert.filter import FilterPlugin

class ChassisFilter(FilterPlugin):

    attrs_to_remove = ['asset-tag', 'serial-number']
