from sysassert.datasource import DataSource
from sysassert.cmd import rawcmd
from sysassert.tools import normalize

class DMIStringDataSource(DataSource):

    dmi_keywords = [
		'bios-vendor',
		'bios-version',
		'bios-release-date',
		'system-manufacturer',
		'system-product-name',
		'system-version',
		'system-serial-number',
		'system-uuid',
		'baseboard-manufacturer',
		'baseboard-product-name',
		'baseboard-version',
		'baseboard-serial-number',
		'baseboard-asset-tag',
		'chassis-manufacturer',
		'chassis-type',
		'chassis-version',
		'chassis-serial-number',
		'chassis-asset-tag',
		'processor-family',
		'processor-manufacturer',
		'processor-version',
		'processor-frequency',
	]

    command = ['dmidecode']

    def __init__(self, dmidata=None):
        if dmidata is not None:
            self.dmidata = dmidata
        else:
            self.dmidata = None

    @classmethod
    def get_deps(cls):
        return [cls.command[0]]

    @classmethod
    def get_dmidata(cls, dmi_type):
        data = {}
        for keyword in cls.dmi_keywords:
            if keyword.startswith(dmi_type):
                data[keyword] = rawcmd(['dmidecode', '-s', keyword]).strip().split('\n')
        return data

    def get_items(self, dmi_type='system'):
        if dmi_type is None:
            return []
        # get dmidata if necessary
        if self.dmidata is None:
            dmidata = self.get_dmidata(dmi_type)
        else:
            dmidata = self.dmidata

        # check that all list of a type are of the same size
        lenlist = [len(v) for k, v in dmidata.items() if k.startswith(dmi_type)]
        assert(lenlist[1:] == lenlist[:-1])
        count = lenlist[0]

        # return corresponding items
        # by transforming:
        #     {k1: [v11, v12], k2: [v21, v22]}
        # to:
        #     [{k1: v11, k2: v21}, {k1: v12, k2: v22}]
        return [{k[len(dmi_type) + 1:]: v[i]
                 for k, v in dmidata.items()
                 if k.startswith(dmi_type)}
                for i in range(count)]
