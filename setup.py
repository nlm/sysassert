from setuptools import setup,find_packages

setup(
    name = "sysassert",
    version = "0.1",
    packages = ['sysassert'],
    author = "Nicolas Limage",
    author_email = 'nlimage@online.net',
    description = "system hardware validation tool",
    license = "GPL",
    keywords = "system validation",
    install_requires = [
        'toml',
        'six',
    ],
    entry_points = {
        'console_scripts': [
            'sysassert = sysassert.__main__:main',
        ],
        'sysassert_plugin_v1': [
            'dummy = sysassert.plugin.dummy:DummyPlugin',
            'memory = sysassert.plugin.memory:MemoryPlugin',
            'processor = sysassert.plugin.processor:ProcessorPlugin',
            'bios = sysassert.plugin.bios:BIOSPlugin',
        ],
        'sysassert_datasource_v1': [
            'dmi = sysassert.datasource.dmi:DMIDataSource',
        ],
    }
)
