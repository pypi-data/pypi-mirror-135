# coding: utf-8
# flake8: noqa
# cligen: 0.1.7, dd: 2021-12-28

import argparse
import configparser
import datetime
import importlib
import os
import pathlib
import sys

from . import __version__


class DefaultVal:
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return str(self.val)


class ConfigBase:
    def __init__(self, path=None):
        self._data = None
        tmp_path = self.get_config_parm()
        if tmp_path:
            self._path = tmp_path
        elif isinstance(path, pathlib.Path):
            self._path = path
        elif path is not None:
            if path[0] in '~/':
                self._path = pathlib.Path(path).expanduser()
            elif '/' in path:  # assume '!Config config_dir/config_name'
                self._path = self.config_dir / path
            else:
                self._path = self.config_dir / path / (path.rsplit('.')[-1] + self.suffix)
        else:
            # could use sys.argv[0]
            raise NotImplementedError

    @property
    def data(self):
        if self._data is None:
            self._data = self.load()  # NOQA
        return self._data

    def get(self, *args, pd=None):
        data = self.data
        for arg in args:
            if arg in data:
                data = data[arg]
            else:
                break
        else:
            return data
        if args[0] != 'global':
            return self.get(*(['global'] + list(args[1:])), pd=pd)
        return pd

    def get_config_parm(self):
        # check if --config was given on commandline
        for idx, arg in enumerate(sys.argv[1:]):
            if arg.startswith('--config'):
                if len(arg) > 8 and arg[8] == '=':
                    return pathlib.Path(arg[9:])
                else:
                    try:
                        return pathlib.Path(sys.argv[idx + 2])
                    except IndexError:
                        print('--config needs an argument')
                        sys.exit(1)
        return None

    @property
    def config_dir(self):
        # https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
        attr = '_' + sys._getframe().f_code.co_name
        if not hasattr(self, attr):
            if sys.platform.startswith('win32'):
                d = os.environ['APPDATA']
            else:
                d = os.environ.get(
                    'XDG_CONFIG_HOME', os.path.join(os.environ['HOME'], '.config')
                )
            pd = pathlib.Path(d)
            setattr(self, attr, pd)
            return pd
        return getattr(self, attr)


class ConfigINI(ConfigBase):
    suffix = '.ini'

    def load(self):
        config = configparser.ConfigParser()
        config.read(self._path)
        data = {}
        for section in config.sections():
            sl = section.lower().split('.')
            if not sl[0] == 'defaults':
                continue
            if len(sl) == 1:
                data['global'] = dict(config.items(section))
            elif len(sl) == 2:
                data[sl[1]] = dict(config.items(section))
            else:
                raise NotImplementedError
        return data


class CountAction(argparse.Action):
    """argparse action for counting up and down

    standard argparse action='count', only increments with +1, this action uses
    the value of self.const if provided, and +1 if not provided

    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action=CountAction, const=1,
            nargs=0)
    parser.add_argument('--quiet', '-q', action=CountAction, dest='verbose',
            const=-1, nargs=0)
    """

    def __call__(self, parser, namespace, values, option_string=None):
        if self.const is None:
            self.const = 1
        try:
            val = getattr(namespace, self.dest) + self.const
        except TypeError:  # probably None
            val = self.const
        setattr(namespace, self.dest, val)


class DateAction(argparse.Action):
    """argparse action for parsing dates with or without dashes

    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action=DateAction)
    """

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs != 1 and nargs not in [None, '?', '*']:
            raise ValueError('DateAction can only have one argument')
        default = kwargs.get('default')
        if isinstance(default, str):
            kwargs['default'] = self.special(default)
        super(DateAction, self).__init__(option_strings, dest, nargs=nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        # this is only called if the option is specified
        if values is None:
            return None
        s = values
        for c in './-_':
            s = s.replace(c, '')
        try:
            val = datetime.datetime.strptime(s, '%Y%m%d').date()
        except ValueError:
            val = self.special(s)
        #    val = self.const
        setattr(namespace, self.dest, val)

    def special(self, date_s):
        if isinstance(date_s, str):
            today = datetime.date.today()
            one_day = datetime.timedelta(days=1)
            if date_s == 'today':
                return today
            if date_s == 'yesterday':
                return today - one_day
            if date_s == 'tomorrow':
                return today + one_day
            raise ValueError


def main(cmdarg=None):
    cmdarg = sys.argv if cmdarg is None else cmdarg
    parsers = []
    config = ConfigINI(path='python_release_info/config.ini')
    parsers.append(argparse.ArgumentParser())
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(config.get('global', 'verbose', pd=0)), dest='_gl_verbose', metavar='VERBOSE', nargs=0, help='increase verbosity level', action=CountAction)
    parsers[-1].add_argument('--dir', default=DefaultVal(config.get('global', 'dir', pd=None)), dest='_gl_dir', metavar='DIR', help='base directory for all downloads and extraction (default: %(default)s)', action='store')
    parsers[-1].add_argument('--force', default=DefaultVal(config.get('global', 'force', pd=None)), dest='_gl_force', action='store_true', help='force download (and extraction), normally skipped if already there')
    parsers[-1].add_argument('--type', default=DefaultVal(config.get('global', 'type', pd='cpython')), dest='_gl_type', metavar='TYPE', help='compiler type to work on: [cpython, tbd] (default: %(default)s)', action='store')
    parsers[-1].add_argument('--version', action='store_true', help='show program\'s version number and exit')
    subp = parsers[-1].add_subparsers()
    px = subp.add_parser('update', help='download release_info.pon to config directory (if --dir specified also download new versions)')
    px.set_defaults(subparser_func='update')
    parsers.append(px)
    parsers[-1].add_argument('--extract', default=config.get('update', 'extract', pd=False), help='extract newly downloaded versions', action='store_true')
    parsers[-1].add_argument('--build', '-b', default=config.get('update', 'build', pd=None), help='newly extracted versions (default: %(default)s)')
    parsers[-1].add_argument('--delay', default=config.get('update', 'delay', pd=None), help='delay updating for DELAY days (default: %(default)s)', type=int)
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(config.get('update', 'verbose', pd=0)), nargs=0, help='increase verbosity level', action=CountAction)
    parsers[-1].add_argument('--dir', default=DefaultVal(config.get('update', 'dir', pd=None)), help='base directory for all downloads and extraction (default: %(default)s)')
    parsers[-1].add_argument('--force', default=DefaultVal(config.get('update', 'force', pd=False)), action='store_true', help='force download (and extraction), normally skipped if already there')
    parsers[-1].add_argument('--type', default=DefaultVal(config.get('update', 'type', pd='cpython')), help='compiler type to work on: [cpython, tbd] (default: %(default)s)')
    px = subp.add_parser('current', help='list of current major.minor.micro versions')
    px.set_defaults(subparser_func='current')
    parsers.append(px)
    parsers[-1].add_argument('--dd', default=config.get('current', 'dd', pd='today'), action=DateAction, metavar='DATE', help='show versions current on %(metavar)s) (default: %(default)s)')
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(config.get('current', 'verbose', pd=0)), nargs=0, help='increase verbosity level', action=CountAction)
    parsers[-1].add_argument('--dir', default=DefaultVal(config.get('current', 'dir', pd=None)), help='base directory for all downloads and extraction (default: %(default)s)')
    parsers[-1].add_argument('--force', default=DefaultVal(config.get('current', 'force', pd=False)), action='store_true', help='force download (and extraction), normally skipped if already there')
    parsers[-1].add_argument('--type', default=DefaultVal(config.get('current', 'type', pd='cpython')), help='compiler type to work on: [cpython, tbd] (default: %(default)s)')
    px = subp.add_parser('pre', help='list of not yet finalized releases')
    px.set_defaults(subparser_func='pre')
    parsers.append(px)
    parsers[-1].add_argument('--dd', default=config.get('pre', 'dd', pd='today'), action=DateAction, metavar='DATE', help='show versions current on %(metavar)s) (default: %(default)s)')
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(config.get('pre', 'verbose', pd=0)), nargs=0, help='increase verbosity level', action=CountAction)
    parsers[-1].add_argument('--dir', default=DefaultVal(config.get('pre', 'dir', pd=None)), help='base directory for all downloads and extraction (default: %(default)s)')
    parsers[-1].add_argument('--force', default=DefaultVal(config.get('pre', 'force', pd=False)), action='store_true', help='force download (and extraction), normally skipped if already there')
    parsers[-1].add_argument('--type', default=DefaultVal(config.get('pre', 'type', pd='cpython')), help='compiler type to work on: [cpython, tbd] (default: %(default)s)')
    px = subp.add_parser('download', help='download/extract a particular version')
    px.set_defaults(subparser_func='download')
    parsers.append(px)
    parsers[-1].add_argument('--extract', default=config.get('download', 'extract', pd=False), action='store_true', help='extract downloaded tar file')
    parsers[-1].add_argument('version')
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(config.get('download', 'verbose', pd=0)), nargs=0, help='increase verbosity level', action=CountAction)
    parsers[-1].add_argument('--dir', default=DefaultVal(config.get('download', 'dir', pd=None)), help='base directory for all downloads and extraction (default: %(default)s)')
    parsers[-1].add_argument('--force', default=DefaultVal(config.get('download', 'force', pd=False)), action='store_true', help='force download (and extraction), normally skipped if already there')
    parsers[-1].add_argument('--type', default=DefaultVal(config.get('download', 'type', pd='cpython')), help='compiler type to work on: [cpython, tbd] (default: %(default)s)')
    parsers.pop()
    if '--version' in cmdarg[1:]:
        if '-v' in cmdarg[1:] or '--verbose' in cmdarg[1:]:
            return list_versions(pkg_name='release_info', version=None, pkgs=[])
        print(__version__)
        return
    if '--help-all' in cmdarg[1:]:
        try:
            parsers[0].parse_args(['--help'])
        except SystemExit:
            pass
        for sc in parsers[1:]:
            print('-' * 72)
            try:
                parsers[0].parse_args([sc.prog.split()[1], '--help'])
            except SystemExit:
                pass
        sys.exit(0)
    args = parsers[0].parse_args(args=cmdarg[1:])
    for gl in ['verbose', 'dir', 'force', 'type']:
        glv = getattr(args, '_gl_' + gl, None)
        if isinstance(getattr(args, gl, None), (DefaultVal, type(None))) and glv is not None:
            setattr(args, gl, glv)
        delattr(args, '_gl_' + gl)
        if isinstance(getattr(args, gl), DefaultVal):
            setattr(args, gl, getattr(args, gl).val)
    cls = getattr(importlib.import_module('release_info.release_info'), 'ReleaseInfo')
    obj = cls(args, config=config)
    funcname = getattr(args, 'subparser_func', None)
    if funcname is None:
        parsers[0].parse_args('--help')
    fun = getattr(obj, args.subparser_func)
    return fun()

def list_versions(pkg_name, version, pkgs):
    version_data = [
        ('Python', '{v.major}.{v.minor}.{v.micro}'.format(v=sys.version_info)),
        (pkg_name, __version__ if version is None else version),
    ]
    for pkg in pkgs:
        try:
            version_data.append(
                (pkg,  getattr(importlib.import_module(pkg), '__version__', '--'))
            )
        except ModuleNotFoundError:
            version_data.append((pkg, 'NA'))
        except KeyError:
            pass
    longest = max([len(x[0]) for x in version_data]) + 1
    for pkg, ver in version_data:
        print('{:{}s} {}'.format(pkg + ':', longest, ver))


if __name__ == '__main__':
    sys.exit(main())
