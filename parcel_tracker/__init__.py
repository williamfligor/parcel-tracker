# -*- coding: utf-8 -*-
### BEGIN LICENSE
# Copyright © 2012-2016 Vsevolod Velichko <torkvema@gmail.com>
# Copyright © 2012 Carlos da Costa <c.costa@outlook.com>
# Copyright © 2012-2013 Erik Christiansson <erik@christiansson.net>
# Copyright © 2013 Pål Sollie <sollie@sparkz.no>
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

import optparse

import locale
from locale import gettext as _
locale.textdomain('parcel-tracker')

from gi.repository import Gtk  # pylint: disable=E0611

from parcel_tracker import ParcelTrackerWindow

from parcel_tracker_lib import set_up_logging, get_version


def parse_options():
    """Support for command line options"""
    parser = optparse.OptionParser(version="%%prog %s" % get_version())
    parser.add_option('--minimized', action='store_true',
                      default=False, help=_('Do not show window (start minimized)'))
    parser.add_option(
        "-v", "--verbose", action="count", dest="verbose",
        help=_("Show debug messages (-vv debugs parcel_tracker_lib also)"))
    (options, args) = parser.parse_args()

    set_up_logging(options)

    return options, args


def main():
    'constructor for your class instances'
    options, args = parse_options()

    # Run the application.
    window = ParcelTrackerWindow.ParcelTrackerWindow()
    if not options.minimized:
        window.show()
    Gtk.main()
