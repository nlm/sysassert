from sysassert.filter import FilterPlugin

class BiosFilter(FilterPlugin):

    attrs_to_remove = ['address', 'release_date']
