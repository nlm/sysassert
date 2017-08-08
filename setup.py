from setuptools import setup, find_packages
import sysassert

setup(
    name = "sysassert",
    version = sysassert.__version__,
    packages = find_packages(),
    author = sysassert.__author__,
    author_email = sysassert.__email__,
    description = "system hardware validation tool",
    license = sysassert.__license__,
    keywords = "system hardware validation qualification",
    install_requires = [
        'pyyaml',
        'colorlog',
        'voluptuous',
    ],
    entry_points = {
        'console_scripts': [
            'sysassert = sysassert.__main__:main',
        ],
        'sysassert_plugin_v1': [
            'memory = sysassert.plugin.memory:MemoryPlugin',
            'processor = sysassert.plugin.processor:ProcessorPlugin',
            'bios = sysassert.plugin.bios:BIOSPlugin',
            'disk = sysassert.plugin.disk:DiskPlugin',
            'pci = sysassert.plugin.pci:PCIPlugin',
            'usb = sysassert.plugin.usb:USBPlugin',
            'chassis = sysassert.plugin.dmistring:ChassisPlugin',
            'baseboard = sysassert.plugin.dmistring:BaseboardPlugin',
            'system = sysassert.plugin.dmistring:SystemPlugin',
        ],
        'sysassert_filter_v1': [
            'baseboard = sysassert.filter.baseboard:BaseboardFilter',
            'bios = sysassert.filter.bios:BiosFilter',
            'chassis = sysassert.filter.chassis:ChassisFilter',
            'disk = sysassert.filter.disk:DiskFilter',
            'memory = sysassert.filter.memory:MemoryFilter',
            'processor = sysassert.filter.processor:ProcessorFilter',
            'system = sysassert.filter.system:SystemFilter',
        ],
        'sysassert_datasource_v1': [
            'dmi = sysassert.datasource.dmi:DMIDataSource',
            'dmistring = sysassert.datasource.dmistring:DMIStringDataSource',
            'lsblk = sysassert.datasource.lsblk:LSBLKDataSource',
            'lspci = sysassert.datasource.lspci:LSPCIDataSource',
            'lsusb = sysassert.datasource.lsusb:LSUSBDataSource',
        ],
    },
    include_package_data = True,
    package_data = {
        'sysassert': ['i18n/*/LC_MESSAGES/*'],
    },
)
