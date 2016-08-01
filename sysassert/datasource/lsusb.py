from sysassert.datasource import DataSource
from sysassert.cmd import rawcmd
from sysassert.tools import normalize
import re

class LSUSBDataSource(DataSource):

    command = ['lsusb']

    def __init__(self, data=None):
        if data is not None:
            self.data = data
        else:
            data = rawcmd(self.command)
        self.data = self._parse_usb(data)

    def get_items(self, item_class=None):
        if item_class is None:
            return self.data
        return [x for x in self.data if x.get('class') == item_class]

    def _parse_usb(self, content):
        """
        Parse the whole lsusb output.
        Returns a list of dicts
        """
        results = []
        device = {}
        for line in content.split('\n'):
            # example: Bus 002 Device 002: ID 8087:0024 Intel Corp. Integrated Rate Matching Hub
            res = re.match('^Bus (?P<bus>\d+) Device (?P<device>\d+): ID (?P<id>\d+:\d+) (?P<desc>.*)$', line)
            if res:
                results.append({key: res.group(key) for key in ['bus', 'device', 'id', 'desc']})
        return results
