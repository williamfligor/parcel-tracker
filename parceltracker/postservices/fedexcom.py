#!/usr/bin/env python
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

from . import TrackingService

import json
from dateutil.parser import parse as parsedate

class FedexComService(TrackingService):
    """ FedEx """

    name = "Fedex"
    url = 'https://www.fedex.com/trackingCal/track'
    post = 'data=%%7B%%22TrackPackagesRequest%%22%%3A%%7B%%22appType%%22%%3A%%22wtrk%%22%%2C%%22uniqueKey%%22%%3A%%22%%22%%2C%%22processingParameters%%22%%3A%%7B%%22anonymousTransaction%%22%%3Atrue%%2C%%22clientId%%22%%3A%%22WTRK%%22%%2C%%22returnDetailedErrors%%22%%3Atrue%%2C%%22returnLocalizedDateTime%%22%%3Afalse%%7D%%2C%%22trackingInfoList%%22%%3A%%5B%%7B%%22trackNumberInfo%%22%%3A%%7B%%22trackingNumber%%22%%3A%%22%(number)s%%22%%2C%%22trackingQualifier%%22%%3A%%22%%22%%2C%%22trackingCarrier%%22%%3A%%22%%22%%7D%%7D%%5D%%7D%%7D&action=trackpackages&locale=en_US&format=json&version=99'

    def _parse_page(self, html):
        try:
            js = json.loads(html.replace('\\x', '\u00'))
            if len(js['TrackPackagesResponse']['packageList'][0]['trackingQualifier']) > 0:
                return [(e['status'], parsedate('%s %s' % (e['date'], e['time'])), e['scanLocation'])
                        for e in js['TrackPackagesResponse']['packageList'][0]['scanEventList']]
        except:
            pass
        return []
