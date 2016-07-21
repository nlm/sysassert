import pkg_resources as pkr

class AssertPlugin(object):

    def __init__(self):
        raise NotImplemented

    def validate(self, spec):
        raise NotImplemented

    @staticmethod
    def get_datasource(name):
        for entrypoint in pkr.iter_entry_points('sysassert_datasource_v1'):
            if name == entrypoint.name:
                return entrypoint.load()
        return None
