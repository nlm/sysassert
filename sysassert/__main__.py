import sys
import logging
import argparse
import yaml
from colorlog import ColoredFormatter
from .engine import SysAssert
from .cmd import cmd, rawcmd

from pprint import pprint

def config_logger(colored=False, loglevel=None):

    logging.SPARSE = 25

    if loglevel is not None:
        level = getattr(logging, loglevel)
    else:
        level = logging.INFO

    stream = logging.StreamHandler()
    if ((colored == 'auto' and sys.stderr.isatty()) or
        colored == 'always'):
        log_format = ("%(log_color)s%(levelname)-5s%(reset)s |"
                      " %(log_color)s%(message)s%(reset)s")
        stream.setFormatter(ColoredFormatter(log_format))
    else:
        log_format = ("%(levelname)-5s |"
                      " %(message)s")
        stream.setFormatter(Formatter(log_format))
    logging.basicConfig(handlers=[stream], level=level)


def main(arguments=None):
    """
    main function
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('profile', help='machine profile to check')
    parser.add_argument('-l', '--loglevel', default='INFO',
                        choices=('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'),
                        help="Set the logging level")
    args = parser.parse_args()

    config_logger(colored='always', loglevel=args.loglevel)
    logger = logging.getLogger(__name__)

    try:
        with open('{}'.format(args.profile)) as pfd:
            profile_config = yaml.safe_load(pfd)
    except Exception as exc:
        parser.error(exc)

    sas = SysAssert(profile_config)
    result = sas.validate()
    if result[0] is True:
        logger.info('overall result: all tests passed')
    else:
        logger.error('overall result: some tests failed')

    #dmiout = rawcmd(['cat', 'dmidecode.txt'])
    #memdev = DMI(dmiout).memory_devices

if __name__ == '__main__':
    main()
