# -*- coding: UTF-8 -*-
"""
This module pokes Mikrotik for IRQ Peers
"""
import json
import time
from libs.strings import zabbix_escape
from logging import getLogger


def run(api, ts=False, log=getLogger(__name__)):
    """
    Returns IRQ LLD JSON
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

    irqstats = api(cmd='/system/resource/irq/print')

    peers = []

    for irqitem in irqstats:
        peers.append(
            {
                '{#IRQ}': irqitem.get('users').replace(",", "__"),
            }
        )

    # Composing JSON to return
    json_data = {
        'data': peers
    }

    # Return JSON
    print "{host} {key}{unixtime}{value}".format(
        host='-',
        key='mikrotik.irq.discovery',
        unixtime=unixtime,
        value=zabbix_escape(json.dumps(json_data))
    )
