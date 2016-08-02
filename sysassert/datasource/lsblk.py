import re
from sysassert.datasource import DataSource
from sysassert.cmd import rawcmd
from sysassert.tools import normalize

class LSBLKDataSource(DataSource):

    command = ['lsblk', '-Pnbo', 'KNAME,TYPE,SIZE,ALIGNMENT,MIN-IO,OPT-IO,'
                                 'PHY-SEC,LOG-SEC,ROTA,RQ-SIZE,MODEL']

    def __init__(self, blkdata=None):
        if blkdata is not None:
            self.blkdata = blkdata
        else:
            blkdata = rawcmd(self.command)
        self.data = self._parse_blk(blkdata)

    def get_items(self, blk_type=None):
        if blk_type is None:
            return self.data
        return [x for x in self.data if x.get('type') == blk_type]

    def _parse_blk(self, content):
        """
        Parse the whole lsblk output.
        Returns a list of dicts
        """
        results = []
        for line in content.split('\n'):
            if line:
                res = re.findall('([A-Z_-]+)="([^"]*)"', line)
                results.append({normalize(a): b for (a, b) in res})
        return results
