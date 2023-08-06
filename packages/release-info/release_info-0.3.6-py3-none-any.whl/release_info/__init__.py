# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

_package_data = dict(
    full_package_name='release_info',
    version_info=(0, 3, 6),
    __version__='0.3.6',
    version_timestamp='2022-01-16 09:04:17',
    author='Anthon van der Neut',
    author_email='a.van.der.neut@ruamel.eu',
    description='automatically updated python release information',
    keywords='pypi statistics',
    entry_points='python_release_info=release_info.__main__:main',
    # entry_points=None,
    license='Copyright Ruamel bvba 2007-2020',
    since=2020,
    # status="α|β|stable",  # the package status on PyPI
    # data_files="",
    install_requires=[],
    tox=dict(
        env='3',
    ),
    print_allowed=True,
    python_requires='>=3',
    # config_dir='python_release_info/config.ini',
)


version_info = _package_data['version_info']
__version__ = _package_data['__version__']


_cligen_data = """\
# all tags start with an uppercase char and can often be shortened to three and/or one
# characters. If a tag has multiple uppercase letter, only using the uppercase letters is a
# valid shortening
# Tags used:
# !Commandlineinterface, !Cli,
# !Option, !Opt, !O
  # - !Option [all, !Action store_true, !Help build sdist and wheels for all platforms]
# !PreSubparserOption, !PSO
# !Help, !H
# !Argument, !Arg
  # - !Arg [files, nargs: '*', !H files to process]
# !Module   # make subparser function calls imported from module
# !Instance # module.Class: assume subparser method calls on instance of Class imported from module
# !Action # either one of the actions in subdir _action (by stem of the file) or e.g. "store_action"
# !Config YAML/INI/PON  read defaults from config file
# !AddDefaults ' (default: %(default)s)'
# !Prolog (sub-)parser prolog/description text (for multiline use | )
# !Epilog (sub-)parser epilog text (for multiline use | )
# !NQS used on arguments, makes sure the scalar is non-quoted e.g for instance/method/function
#      call arguments, when cligen knows about what argument a keyword takes, this is not needed
!Cli 0:
- !Instance release_info.release_info.ReleaseInfo
- !AddDefaults ' (default: %(default)s)'
- !Config [INI, python_release_info/config.ini]
- !Option [verbose, v, !Help increase verbosity level, !Action count]
- !Option [dir, !Help 'base directory for all downloads and extraction']
# - !Option [config, !Help directory for config file, default: '~/.config/python_release_info/']
- !O [force, !Action store_true, !Help 'force download (and extraction), normally skipped if already there']
- !O [type, !Help 'compiler type to work on: [cpython, tbd]', default: 'cpython']
- update:
  - !Help download release_info.pon to config directory (if --dir specified also download new versions)
  - !Option [extract, !Help extract newly downloaded versions, !Action store_true]
  - !Option [build, b, !Help newly extracted versions]
  - !Option [delay, !H delay updating for DELAY days, type: int]
- current:
  - !Help list of current major.minor.micro versions
  - !Option [dd, !Action date, default: today, metavar: DATE, !Help 'show versions current on %(metavar)s)']
- pre:
  - !H list of not yet finalized releases
  - !Option [dd, !Action date, default: today, metavar: DATE, !Help 'show versions current on %(metavar)s)']
- download:
  - !H download/extract a particular version
  - !Opt [extract, !Action store_true, !Help extract downloaded tar file]
  - !Arg [version]
# - !Option [test, !Action store_true, !Help don't import version/packagedata from . (for testing cligen)]
# - !Option [all, !Action store_true, !Help build sdist and wheels for all platforms]
# - !Option [linux, !Action store_true, !Help build linux wheels using manylinux]
# - !Arg [args, nargs: '*', !H you have to do this]
# - !Prolog 'Prolog for the parser'
# - !Epilog 'Epilog for the parser'
"""  # NOQA


def release_info():
    from .release_info import release_info as ri  # NOQA

    return ri
