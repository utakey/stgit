#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
from distutils.core import setup
import glob
import os
import sys

from stgit import version
from stgit import commands, completion


def __version_to_list(version):
    """Convert a version string to a list of numbers or strings
    """
    ver_list = []
    for p in version.split('.'):
        try:
            n = int(p)
        except ValueError:
            n = p
        ver_list.append(n)
    return ver_list

def __check_min_version(min_ver, ver):
    """Check whether ver is greater or equal to min_ver
    """
    min_ver_list = __version_to_list(min_ver)
    ver_list = __version_to_list(ver)
    return min_ver_list <= ver_list

def __check_python_version():
    """Check the minimum Python version
    """
    pyver = '.'.join(map(str, sys.version_info))
    if not __check_min_version(version.python_min_ver, pyver):
        print('Python version %s or newer required. Found %s'
              % (version.python_min_ver, pyver), file=sys.stderr)
        sys.exit(1)

def __check_git_version():
    """Check the minimum GIT version
    """
    from stgit.run import Run
    gitver = Run('git', '--version').output_one_line().split()[2]
    if not __check_min_version(version.git_min_ver, gitver):
        print('GIT version %s or newer required. Found %s'
              % (version.git_min_ver, gitver), file=sys.stderr)
        sys.exit(1)

def __run_setup():
    setup(name = 'stgit',
          version = version.version,
          license = 'GPLv2',
          author = 'Catalin Marinas',
          author_email = 'catalin.marinas@gmail.com',
          url = 'http://www.procode.org/stgit/',
          download_url = 'http://repo.or.cz/stgit.git',
          description = 'Stacked GIT',
          long_description = 'Push/pop utility on top of GIT',
          scripts = ['stg'],
          packages = ['stgit', 'stgit.commands', 'stgit.lib'],
          data_files = [
            ('share/stgit/templates', glob.glob('templates/*.tmpl')),
            ('share/stgit/examples', glob.glob('examples/*.tmpl')),
            ('share/stgit/examples', ['examples/gitconfig']),
            ('share/stgit/contrib', ['contrib/stgbashprompt.sh']),
            ('share/stgit/completion', ['stgit-completion.bash'])
          ],
          classifiers = [
              'Development Status :: 5 - Production/Stable',
              'Environment :: Console',
              'Intended Audience :: Developers',
              'License :: OSI Approved :: GNU General Public License v2 (GPLv2)'
              'Natural Language :: English',
              'Operating System :: OS Independent',
              'Programming Language :: Python',
              'Programming Language :: Python :: 2',
              'Programming Language :: Python :: 2.6',
              'Programming Language :: Python :: 2.7',
              'Programming Language :: Python :: Implementation :: CPython',
              'Programming Language :: Python :: Implementation :: PyPy',
              'Topic :: Software Development :: Version Control',
          ])


# Check the minimum versions required
__check_python_version()
__check_git_version()

# ensure readable template files
old_mask = os.umask(0o022)

version.write_builtin_version()

# generate the python command list
with open('stgit/commands/cmdlist.py', 'w') as f:
    commands.py_commands(commands.get_commands(allow_cached = False), f)

# generate the bash completion script
with open('stgit-completion.bash', 'w') as f:
    completion.write_completion(f)

__run_setup()

# restore the old mask
os.umask(old_mask)
