# -*- coding: utf-8 -*-
"""Patch Window to send notifications if possible"""

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

notify = lambda *kargs, **kwargs: None

from parcel_tracker_lib import Window
try:
    from gi.repository import Notify
    if Notify.init("Parcel Tracker"):
        def n(message):
            notification = Notify.Notification.new("Parcel Tracker", message, "gtk-add")
            notification.set_timeout(4)
            notification.show()
        notify = n
except ImportError:
    pass

