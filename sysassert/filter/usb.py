from sysassert.filter import FilterPlugin

class USBFilter(FilterPlugin):

    #attrs_to_remove = ['serial-number', 'uuid']
    attrs_to_keep = ['id']
