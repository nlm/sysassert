import sys
import logging
import argparse
import yaml
import gettext
import colorlog
from pkg_resources import resource_filename
from logging import Formatter
from .engine import SysAssert
from .__init__ import __version__

gettext.install('sysassert', resource_filename('sysassert', 'i18n'), codeset='utf-8')

def config_logger(colored='auto', loglevel=None):
    """
    Logger Configuration
    """

    logging.NOTICE = 25
    logging.addLevelName(logging.NOTICE, 'NOTICE')

    if loglevel is not None:
        level = getattr(logging, loglevel.upper())
    else:
        level = logging.INFO

    stream = logging.StreamHandler()
    if ((colored == 'auto' and sys.stderr.isatty()) or
            colored == 'always'):
        log_format = ('%(log_color)s%(levelname)-6s%(reset)s |'
                      ' %(log_color)s%(message)s%(reset)s')
        log_colors = colorlog.default_log_colors
        log_colors.update({'NOTICE': log_colors['INFO']})
        stream.setFormatter(colorlog.ColoredFormatter(log_format,
                                                      log_colors=log_colors))
    else:
        log_format = ('%(levelname)-6s |'
                      ' %(message)s')
        stream.setFormatter(Formatter(log_format))
    logging.basicConfig(handlers=[stream], level=level)

def parse_args(arguments=None, available_plugins=None):
    """
    Parses the arguments from the command line
    """
    parser = argparse.ArgumentParser()

    log_group = parser.add_argument_group('logging')
    log_group.add_argument('-l', '--loglevel', default='info',
                           choices=('debug', 'info', 'notice',
                                    'warning', 'error', 'critical'),
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
    cmd_generate.add_argument('-f', '--filter',
                              action='store_true', default=False,
                              help='auto filter output')
    cmd_generate.add_argument('plugin', nargs='*',
                              choices=available_plugins + [[]],
                              help=_('plugins to generate config from'))

    # Config Lint
    cmd_lint = subparsers.add_parser('lint',
                                    help=_('check profile file validity'))
    cmd_lint.add_argument('profile', nargs='+', type=argparse.FileType('r'),
                          help=_('machine profile to check'))

    # Version Command
    cmd_version = subparsers.add_parser('version',
                                        help=_('show version'))

    # List Plugins Command
    subparsers.add_parser('plugins', aliases=['plu'],
                          help=_('list available plugins'))

    # List deps
    subparsers.add_parser('dependencies', aliases=['dep'],
                          help=_('list system tools dependencies'))

    return parser.parse_args(arguments)

def main(arguments=None):
    """
    CLI for SysAssert
    """
    sas = SysAssert()
    args = parse_args(arguments,
                      available_plugins=[plu for plu in sas.plugins.keys()])
    config_logger(colored=args.color, loglevel=args.loglevel)
    logger = logging.getLogger(__name__)

    if args.command in ('validate', 'val'):
        logger.info(_('starting sysassert'))
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
            logger.log(logging.NOTICE, _('overall result: success ({0})').format(', '.join(passed_profiles)))
        else:
            logger.error(_('overall result: failure'))
            return 1
    elif args.command in ('generate', 'gen'):
        try:
            print(yaml.safe_dump(sas.generate(args.plugin,
                                              filtered=args.filter),
                                 default_flow_style=False,
                                 default_style=False))
        except Exception as exc:
            logger.error(exc)
            return -1
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
                return 1
    elif args.command in ('version'):
        logger.log(logging.NOTICE, 'sysassert {0}'.format(__version__))
    else:
        raise Exception(_('internal error'))
        return -1

if __name__ == '__main__':
    sys.exit(main())
