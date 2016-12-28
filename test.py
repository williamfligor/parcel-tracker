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

'''Fetches parcel statuses from different Post servers'''

from gevent import monkey
from gevent import ssl
try:
    ssl.SSLContext = ssl._ssl._SSLContext  # in utopic interface gevent-ssl is broken
except:
    pass
monkey.patch_all()


# SSLContext.wrap_socket is broken as well
def wrap_socket(*args, **kwargs):
    args = args[1:]
    kwargs.pop('server_hostname', None)
    return ssl.__ssl__.wrap_socket(*args, **kwargs)

try:
    # fix for gevent + python 2.7.9 (ssl is reworked there)
    ssl.__ssl__.SSLContext.wrap_socket = wrap_socket
except AttributeError:
    pass

import postservices


def get_services():
    return postservices.TrackingService.service_classes

if __name__ == '__main__':
    import sys
    import codecs
    import locale
    import logging
    # logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
    # sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)
    # service = get_services()['RussianpostRuService']('CG077165712US')
    # service = get_services()['CanparComService']('D100301463601')
    # service = get_services()['ThailandPostCoThService']('RR051974496TH')
    # service = get_services()['BelpostByService']('BV021258988BY')
    # service = get_services()['EmspostRuService']('EB006267877IT')
    # service = get_services()['EmsPostService']('EB006267877IT')
    # service = get_services()['PpxTrackComService']('RRD050599000070847')
    # service = get_services()['CorreosCl']('RP316339727SG')
    # service = get_services()['RussianpostRuService']('RM144847659CN')
    # service = get_services()['AsendiaUsaComService']('LM586057034US')
    # service = PostaSiService('RA316816466SI')
    # service = ParcelForceNetService('EK034679967GB')
    # service = PostdanmarkDkService('TS123456789DK')
    # service = SwisspostChService('RU470249572CH')
    # service = UspsComService('420917419405515901033236726959')
    # service = get_services()['UspsComService']('LN800389358US')
    # service = get_services()['UspsComService']('9400110200883101818261')
    # service = get_services()['UspsComService']('9241990101549234628999')
    # service = get_services()['CyprusPostGovCyService']('CP353366219FR')
    # service = get_services()['CorreosDeMexicoGobMxService']('RB918786998CN')
    # service = get_services()['CttPtService']('RE640520385SE')
    # service = get_services()['CttPtService']('RJ216862295CN')
    # service = get_services()['TransgroupComService']('23B514653')
    # service = get_services()['PosteItService']('EB006267877IT')
    # service = get_services()['FedexComService']('718909941913')
    # service = get_services()['UpsComService']('1Z88Y7Y21203375521')
    service = get_services()['UpsComService']('1Z18424E4406080438')
    # service = get_services()['YanwenComCnService']('11901885104')
    # service = get_services()['OnTracComService']('C11229305254319')
    # service = get_services()['JapanpostJp']('EG483450686JP')
    # service = UkrposhtaComService('RB041697087UA')
    # service = get_services()['DhlDeService']('00340433836170068547')
    # service = get_services()['HermesWorldTrackingService']('77305107155045')
    # service = CorreiosComService('RD024810847SE')
    # service = PrivpakSchenkerNuService('4199854203482')
    # service = SchenkerNuService('6273636354')
    # service = DhlmultishippingSeService('6288206664')
    # service = get_services()['DhlComService']('5008590300')
    # service = get_services()['CanadaPostCaService']('305260344086')
    # service = CorreosEsService('RA514556931CN')
    # service = get_services()['SingPostComService']('RF427535022SG')
    # service = get_services()['IParcelComService']('AEIIND10002594777')
    # service = get_services()['IParcelComService']('AEIPHX60004469610')
    print u'\t'.join((u'Operation', 'Datetime', 'Location'))
    for i in service.fetch():
        print u'\t'.join([unicode(j) for j in i])
