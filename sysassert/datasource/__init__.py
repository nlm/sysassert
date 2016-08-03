class DataSource(object):

    @classmethod
    def get_deps(cls):
        raise NotImplementedError

    def get_items(self, item_class=None):
        raise NotImplementedError
