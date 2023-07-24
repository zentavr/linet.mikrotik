# -*- coding: UTF-8 -*-
"""
This module pokes Mikrotik for Radius Servers
"""
import json
import time
from libs.strings import zabbix_escape
from logging import getLogger


def run(api, ts=False, log=getLogger(__name__), ver=''):
    """
    Returns Radius LLD JSON
    :param api: initialized librouteros' connect()
    :param ts: Use timestamps
    :return:
    """
    if ts:
        unixtime = " {time} ".format(
            time=int(time.time())
        )
    else:
        unixtime = " "

    radservers = api(cmd='/radius/print')

    servers = []

    for s in radservers:
        servers.append(
            {
                '{#MTIK_RADIUS_ID}': s.get('.id').strip('*'),
                '{#MTIK_RADIUS_COMMENT}': s.get('comment', s.get('.id')),
                '{#MTIK_RADIUS_ADDRESS}': s.get('address'),
            }
        )

    # Composing JSON to return
    json_data = {
        'data': servers
    }

    # Return JSON
    print("{host} {key}{unixtime}{value}".format(
        host='-',
        key='mikrotik.radius-out.discovery',
        unixtime=unixtime,
        value=zabbix_escape(json.dumps(json_data))
    ))
