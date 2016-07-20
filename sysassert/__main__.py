import argparse
import logging
import toml
from .engine import SysAssert
from .cmd import cmd, rawcmd

from pprint import pprint

def main(arguments=None):
    """
    main function
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('profile', help='machine profile to check')
    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG)

    try:
        with open('{}'.format(args.profile)) as pfd:
            profile_config = toml.load(pfd)
    except Exception as exc:
        parser.error(exc)

    sas = SysAssert(profile_config)
    sas.validate()

    #dmiout = rawcmd(['cat', 'dmidecode.txt'])
    #memdev = DMI(dmiout).memory_devices

if __name__ == '__main__':
    main()
