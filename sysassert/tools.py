import logging
from pprint import pformat

def inline_dict(adict):
    return ', '.join(['{}: {}'.format(key, value)
                      for key, value in adict.items()])

class DictListComparator(object):

    def __init__(self, wanted_elements, available_elements):

        self.log = logging.getLogger(__name__)
        self._found = []
        self._missing = []
        self._unwanted = []

        for wanted_element in wanted_elements:

            self.log.debug('wanted: {}'.format(pformat(wanted_element)))
            matching = False

            for available_element in available_elements:

                matching = True

                for attr, value in wanted_element.items():
                    if str(available_element[attr]) != str(value):
                        self.log.debug('attr mismatch: {} ({} <=> {})'
                                       .format(attr, value,
                                               available_element[attr]))
                        matching = False
                        break

                if matching:
                    self.log.debug('found match: {}'
                                   .format(pformat(available_element)))
                    self._found.append(wanted_element)
                    available_elements.remove(available_element)
                    break

            if not matching:
                self._missing.append(wanted_element)

        self._unwanted.extend(available_elements)

    @property
    def found(self):
        return self._found

    @property
    def missing(self):
        return self._missing

    @property
    def unwanted(self):
        return self._unwanted