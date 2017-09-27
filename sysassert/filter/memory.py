from sysassert.filter import FilterPlugin

class MemoryFilter(FilterPlugin):

    attrs_to_remove = ['array_handle', 'serial_number',
                       'total_width', 'set']
