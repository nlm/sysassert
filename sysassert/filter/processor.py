from sysassert.filter import FilterPlugin

class ProcessorFilter(FilterPlugin):

    attrs_to_remove = ['asset_tag', 'current_speed', 'id',
                       'l1_cache_handle', 'l2_cache_handle', 'l3_cache_handle',
                       'serial_number', 'part_number', 'signature']
