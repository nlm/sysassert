from setuptools import setup, find_packages

setup(
    name = "sysassert",
    version = "0.2",
    packages = find_packages(),
    author = "Nicolas Limage",
    author_email = 'nlimage@online.net',
    description = "system hardware validation tool",
    license = "GPL",
    keywords = "system validation",
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
