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
from lxml import etree
from dateutil.parser import parse as parsedate


class SingPostComService(TrackingService):
    """ Singapore Post service - www.singpost.com """

    name = "SingPost"
    url = 'https://prdesb1.singpost.com/ma/GetItemTrackingDetails'
    post = '<ItemTrackingDetailsRequest xmlns="http://singpost.com/paw/ns"><ItemTrackingNumbers><TrackingNumber>%(number)s</TrackingNumber></ItemTrackingNumbers></ItemTrackingDetailsRequest>'

    def _parse_page(self, html):
        try:
            xml = (etree.fromstring(html, parser=etree.XMLParser(encoding='utf-8'))
                   .iter('{*}ItemTrackingDetail').next()
                   .iter('{*}DeliveryStatusDetail')
                   )
        except:
            return []

        result = []
        for detail in xml:
            op = detail.iter('{*}StatusDescription').next().text
            date = parsedate(detail.iter('{*}Date').next().text)
            location = detail.iter('{*}Location').next().text
            result.append((op, date, location))

        return result
