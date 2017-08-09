import re
from sysassert.datasource import DataSource
from sysassert.cmd import rawcmd
from sysassert.tools import normalize

class LSPCIDataSource(DataSource):

    command = ['lspci', '-mm', '-v', '-nn']

    def __init__(self, data=None):
        if data is not None:
            self.data = data
        else:
            data = rawcmd(self.command)
        self.data = self._parse_pci(data)

    @classmethod
    def get_deps(cls):
        return [cls.command[0]]

    def get_items(self, item_class=None):
        if item_class is None:
            return self.data
        return [x for x in self.data if x.get('class') == item_class]

    @staticmethod
    def _parse_pci(content):
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
            elif ':\t' in line:
                (key, value) = line.split('\t')
                res = re.match('(.*) \[([0-9a-f]+)\]$', value)
                eid = None
                if res:
                    value = res.group(1)
                    eid = res.group(2)
                device[normalize(key.rstrip(':'))] = value
                device[normalize(key.rstrip(':')) + '_id'] = eid

        return results
