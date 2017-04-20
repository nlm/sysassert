import sys
import logging
import argparse
import yaml
import gettext
from colorlog import ColoredFormatter
from logging import Formatter
from .engine import SysAssert

gettext.install('sysassert')

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
                           help=_('set the logging level'))
    log_group.add_argument('-c', '--color', default='auto',
                           choices=('auto', 'always', 'never'),
                           help=_('colored output'))

    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    # Validation Command
    cmd_validate = subparsers.add_parser('validate', aliases=['val'],
                                         help=_('validate a machine profile'))
    cmd_validate.add_argument('profile', nargs='+', type=argparse.FileType('r'),
                              help=_('machine profile to check'))

    # Generation Command
    cmd_generate = subparsers.add_parser('generate', aliases=['gen'],
                                         help=_('generate configuration '
                                         'from current hardware'))
    cmd_generate.add_argument('plugin', nargs='*',
                              help=_('plugins to generate config from'))

    # Config Lint

    cmd_lint = subparsers.add_parser('lint',
                                    help=_('check profile file validity'))
    cmd_lint.add_argument('profile', nargs='+', type=argparse.FileType('r'),
                          help=_('machine profile to check'))

    # List Plugins Command
    subparsers.add_parser('plugins', aliases=['plu'],
                          help=_('list available plugins'))

    # List deps
    subparsers.add_parser('dependencies', aliases=['dep'],
                          help=_('list system tools dependencies'))

    return parser.parse_args(arguments)

def main(arguments=None):
    """
    main function
    """

    args = parse_args(arguments)
    config_logger(colored=args.color, loglevel=args.loglevel)
    logger = logging.getLogger(__name__)
    logger.info(_('starting sysassert'))

    sas = SysAssert()
    if args.command in ('validate', 'val'):
        passed_profiles = []
        failed_profiles = []
        for profile in args.profile:
            logger.info('')
            logger.info(_('=========== BEGIN PROFILE {0} ==========').format(profile.name))
            try:
                profile_config = yaml.safe_load(profile)
            except Exception as exc:
                raise Exception(_('error loading configuration'))
            if sas.validate(profile_config):
                passed_profiles.append(profile.name)
            else:
                failed_profiles.append(profile.name)
        logger.info('')
        if len(passed_profiles) > 0:
            logger.info(_('overall result: success ({0}))'.format(', '.join(passed_profiles)))
        else:
            logger.error(_('overall result: failure'))
    elif args.command in ('generate', 'gen'):
        try:
            print(yaml.safe_dump(sas.generate(args.plugin),
                                 default_flow_style=False,
                                 default_style=False))
        except Exception as exc:
            logger.error(exc)
            sys.exit(1)
    elif args.command in ('plugins', 'plu'):
        logger.info(_('available plugins: {0}').format(', '.join(sas.plugins)))
    elif args.command in ('dependencies', 'dep'):
        print(' '.join(sas.dependencies()))
    elif args.command in ('lint'):
        for profile in args.profile:
            logger.info(_('checking {0}').format(profile.name))
            try:
                profile_config = yaml.safe_load(profile)
                if sas.lint(profile_config):
                    logger.info(_('file format is valid'))
            except (yaml.parser.ParseError, Exception) as err:
                logger.error(_('error loading configuration: {0}').format(err))
    else:
        raise Exception(_('internal error'))

if __name__ == '__main__':
    main()
