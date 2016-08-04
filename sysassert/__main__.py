import sys
import logging
import argparse
import yaml
from colorlog import ColoredFormatter
from logging import Formatter
from .engine import SysAssert

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
    cmd_validate.add_argument('profile', nargs='+', type=argparse.FileType('r'),
                              help='machine profile to check')

    # Generation Command
    cmd_generate = subparsers.add_parser('generate', aliases=['gen'],
                                         help='generate configuration '
                                         'from current hardware')
    cmd_generate.add_argument('plugin', nargs='*',
                              help='plugins to generate config from')

    # List Plugins Command
    subparsers.add_parser('plugins', aliases=['plu'],
                          help='list available plugins')

    # List deps
    subparsers.add_parser('dependencies', aliases=['dep'],
                          help='list system tools dependencies')

    return parser.parse_args(arguments)

def main(arguments=None):
    """
    main function
    """

    args = parse_args(arguments)
    config_logger(colored=args.color, loglevel=args.loglevel)
    logger = logging.getLogger(__name__)
    logger.info('starting sysassert')

    sas = SysAssert()
    if args.command in ('validate', 'val'):
        passed_profiles = []
        failed_profiles = []
        for profile in args.profile:
            logger.info('')
            logger.info('=========== BEGIN PROFILE {} =========='.format(profile.name))
            try:
                profile_config = yaml.safe_load(profile)
            except Exception as exc:
                raise Exception('error loading configuration')
            if sas.validate(profile_config):
                passed_profiles.append(profile.name)
            else:
                failed_profiles.append(profile.name)
        logger.info('')
        if len(passed_profiles) > 0:
            logger.info('overall result: success ({})'.format(', '.join(passed_profiles)))
        else:
            logger.error('overall result: failure')
    elif args.command in ('generate', 'gen'):
        try:
            print(yaml.safe_dump(sas.generate(args.plugin),
                                 default_flow_style=False,
                                 default_style=False))
        except Exception as exc:
            logger.error(exc)
            sys.exit(1)
    elif args.command in ('plugins', 'plu'):
        logger.info('available plugins: {}'.format(', '.join(sas.plugins)))
    elif args.command in ('dependencies', 'dep'):
        print(' '.join(sas.dependencies()))
    else:
        raise Exception('internal error')

if __name__ == '__main__':
    main()
