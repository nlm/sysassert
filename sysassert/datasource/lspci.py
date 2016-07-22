import re
from sysassert.datasource import DataSource
from sysassert.cmd import rawcmd
from sysassert.tools import normalize

class LSPCIDataSource(DataSource):

    #command = ['lspci', '-mm', '-v']
    command = ['cat', 'lspci.txt']

    def __init__(self, data=None):
        if data is not None:
            self.data = data
        else:
            data = rawcmd(self.command)
        self.data = self._parse_pci(data)

    def get_items(self, item_class=None):
        if item_class is None:
            return self.data
        return [x for x in self.data if x.get('class') == item_class]

    def _parse_pci(self, content):
        """
        Parse the whole lspci output.
        Returns a list of dicts
        """
        results = []
        device = {}
        for line in content.split('\n'):
            if line == '':
                if device:
                    results.append(device)
                device = {}
            else:
                key, value = line.split('\t')
                device[normalize(key.rstrip(':'))] = value

        return results
