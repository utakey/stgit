# -*- coding: utf-8 -*-
"""Template files look-up"""

from __future__ import absolute_import, division, print_function
import os
import sys

from stgit import basedir

__copyright__ = """
Copyright (C) 2006, Catalin Marinas <catalin.marinas@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License version 2 as
published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see http://www.gnu.org/licenses/.
"""


def get_template(tfile):
    """Return the string in the template file passed as argument or
    None if the file wasn't found.
    """
    tmpl_list = [ os.path.join(basedir.get(), tfile),
                  os.path.join(os.path.expanduser('~'), '.stgit', 'templates',
                               tfile),
                  os.path.join(sys.prefix, 'share', 'stgit', 'templates',
                               tfile) ]

    for t in tmpl_list:
        if os.path.isfile(t):
            with open(t) as f:
                return f.read()
    else:
        return None
