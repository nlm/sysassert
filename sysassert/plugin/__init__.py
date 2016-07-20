import pkg_resources as pkr

class ValidationResult(object):

    def __init__(self, status, message=None, details=None):
        self._status = bool(status)
        self._message = message
        self._details = details

    @property
    def status(self):
        return self._status

    @property
    def message(self):
        return self._message

    @property
    def details(self):
        return self._details


class AssertPlugin(object):

    def __init__(self, config):
        print('youpi')
        raise NotImplemented

    def validate(self):
        raise NotImplemented

    @staticmethod
    def get_datasource(name):
        for entrypoint in pkr.iter_entry_points('sysassert_datasource_v1'):
            if name == entrypoint.name:
                return entrypoint.load()
        return None

    @staticmethod
    def make_result(status, message=None, details=None):
        return ValidationResult(status, message, details)
