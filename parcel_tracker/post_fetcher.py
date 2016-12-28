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


from gi.repository import Gio  # pylint: disable=E0611
from parcel_tracker_lib import post_services
from inspect import isclass
import re
import gevent
import threading
from datetime import datetime
from parcel_tracker_lib.notifier import notify

import locale
from locale import gettext as _
locale.textdomain('parcel-tracker')

__services = post_services.get_services()


def service_names():
    return [name for name in __services]


def enabled_searches():
    settings = Gio.Settings("net.launchpad.parcel-tracker")
    disabled = settings.get_strv('disabled-searches')
    result = []
    for name in service_names():
        if name not in disabled:
            result.append(__services[name])
    return result


def __fetch_one(service, parcel_to_update, callback):
    results = service.fetch()
    new_records = None
    for result in results:
        new_date = datetime.strftime(result[1], '%Y.%m.%d %H:%M')
        new_hash = str(hash(result[0].lower() + new_date + result[2].lower()))
        if new_hash not in parcel_to_update['news']:
            parcel_to_update['news'][new_hash] = [result[0], new_date, result[2]]
            parcel_to_update['unread'] = True
            if new_date > parcel_to_update['date']:
                parcel_to_update['date'] = new_date
            if new_records is None or new_date > new_records[0]:
                new_records = (parcel_to_update['date'], result[0], parcel_to_update['name'])
    parcel_to_update['updated'] = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M")
    if new_records is not None:
        s1 = new_records[2] if isinstance(new_records[2], unicode) else unicode(new_records[2], 'utf-8')
        s2 = new_records[1] if isinstance(new_records[1], unicode) else unicode(new_records[1], 'utf-8')
        notify(u"<b>%s</b>: %s" % (s1, s2))
    callback()


def fetch_parcel(postcode, parcel_to_update, callback):
    searches = enabled_searches()
    for service in searches:
        s = service(postcode)
        gevent.spawn(__fetch_one, s, parcel_to_update, callback)
    return len(searches)
