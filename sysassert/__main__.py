import sys
import logging
import argparse
import yaml
from colorlog import ColoredFormatter
from .engine import SysAssert
from .cmd import cmd, rawcmd

from pprint import pprint

def config_logger(colored='auto', loglevel=None):

    logging.SPARSE = 25

    if loglevel is not None:
        level = getattr(logging, loglevel.upper())
    else:
        level = logging.INFO

    stream = logging.StreamHandler()
    if ((colored == 'auto' and sys.stderr.isatty()) or
        colored == 'always'):
        log_format = ('%(log_color)s%(levelname)-5s%(reset)s |'
                      ' %(log_color)s%(message)s%(reset)s')
        stream.setFormatter(ColoredFormatter(log_format))
    else:
        log_format = ('%(levelname)-5s |'
                      ' %(message)s')
        stream.setFormatter(Formatter(log_format))
    logging.basicConfig(handlers=[stream], level=level)

def parse_args(arguments=None):

    parser = argparse.ArgumentParser()

    log_group = parser.add_argument_group('logging')
    log_group.add_argument('-l', '--loglevel', default='info',
                           choices=('debug', 'info', 'warning',
                                    'error', 'critical'),
                           help='set the logging level')
    log_group.add_argument('-c', '--color', default='auto',
                           choices=('auto', 'always', 'never'),
                           help='colored output')

    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    # Validation Command
    cmd_validate = subparsers.add_parser('validate', aliases=['val'],
                                         help='validate a machine profile')
    cmd_validate.add_argument('profile', type=argparse.FileType('r'),
                              help='machine profile to check')

    # Generation Command
    cmd_generate = subparsers.add_parser('generate', aliases=['gen'],
                                         help='generate configuration from current hardware')
    cmd_generate.add_argument('plugin', nargs='*',
                              help='plugins to generate config from')

    # List Plugins Command
    cmd_plugins = subparsers.add_parser('plugins', aliases=['plu'],
                                        help='list available plugins')

    return parser.parse_args(arguments)

def main(arguments=None):
    """
    main function
    """

    args = parse_args(arguments)
    config_logger(colored=args.color, loglevel=args.loglevel)
    logger = logging.getLogger(__name__)

    sas = SysAssert()
    if args.command in ('validate', 'val'):
        try:
            profile_config = yaml.safe_load(args.profile)
        except Exception as exc:
            raise Exception('error loading configuration')
        if sas.validate(profile_config) is True:
            logger.info('overall result: success')
        else:
            logger.error('overall result: failure')
    elif args.command in ('generate', 'gen'):
        try:
            print(yaml.dump(sas.generate(args.plugin),
                            default_flow_style=False))
        except Exception as exc:
            logger.error(exc)
            sys.exit(1)
    elif args.command in ('plugins', 'plu'):
        logger.info('available plugins: {}'.format(', '.join(sas.plugins)))
    else:
        raise Exception('internal error')

if __name__ == '__main__':
    main()
