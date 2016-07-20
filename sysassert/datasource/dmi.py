from sysassert.datasource import DataSource

class DMIDataSource(DataSource):

    dmi_types = {
        0:  'bios',
        1:  'system',
        2:  'base board',
        3:  'chassis',
        4:  'processor',
        7:  'cache',
        8:  'port connector',
        9:  'system slot',
        10: 'on board device',
        11: 'OEM strings',
        #13: 'bios language',
        15: 'system event log',
        16: 'physical memory array',
        17: 'memory device',
        19: 'memory array mapped address',
        24: 'hardware security',
        25: 'system power controls',
        27: 'cooling device',
        32: 'system boot',
        41: 'onboard device',
    }

    def __init__(self, dmidata):
        self.dmidata = dmidata
        self.data = self._parse_dmi(dmidata)

    def dmi_id(self, dmi_type):
        """
        Finds a dmi id from the dmi type name
        Returns a dmi id or raises KeyError
        """
        if dmi_type not in self.dmi_types.values():
            raise KeyError
        return [item[0]
                for item in self.dmi_types.items()
                if item[1] == dmi_type][0]

    def dmi_items(self, dmi_type=None):
        """
        Returns dmi items matching an optional dmi id
        """
        if dmi_type is None:
            return [elt[1] for elt in self.data]
        dmi_id = self.dmi_id(dmi_type)
        return [elt[1] for elt in self.data if elt[0] == dmi_id]

    @property
    def memory_devices(self):
        """
        Returns the list of memory devices
        """
        return self.dmi_items('memory device')

    def _parse_dmi(self, content):
        """
        Parse the whole dmidecode output.
        Returns a list of tuples of (type int, value dict).
        """
        info = []
        lines = iter(content.strip().splitlines())
        while True:
            try:
                line = next(lines)
            except StopIteration:
                break

            if line.startswith('Handle 0x'):
                typ = int(line.split(',', 2)[1].strip()[len('DMI type'):])
                if typ in self.dmi_types:
                    info.append((typ, self._parse_handle_section(lines)))
        return info

    @staticmethod
    def _parse_handle_section(lines):
        """
        Parse a section of dmidecode output

        * 1st line contains address, type and size
        * 2nd line is title
        * line started with one tab is one option and its value
        * line started with two tabs is a member of list
        """
        data = { '_title': next(lines).rstrip() }

        for line in lines:
            line = line.rstrip()
            if line.startswith('\t\t'):
                data[k].append(line.lstrip())
            elif line.startswith('\t'):
                k, v = [i.strip() for i in line.lstrip().split(':', 1)]
                if v:
                    data[k] = v
                else:
                    data[k] = []
            else:
                break

        return data