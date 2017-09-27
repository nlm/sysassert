from sysassert.filter import FilterPlugin

class DiskFilter(FilterPlugin):

    attrs_to_remove = ['alignment', 'kname', 'min_io', 'opt_io', 'rq_size']
