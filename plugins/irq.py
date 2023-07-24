# -*- coding: UTF-8 -*-
"""
This module pokes Mikrotik for IRQ Counters
"""
import time
from libs.strings import zabbix_escape
from logging import getLogger


def run(api, ts=False, log=getLogger(__name__), ver=''):
    """
    Returns IRQ Counters
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

    for irqitem in irqstats:
        print("{host} \"{key}\"{unixtime}{value}".format(
            host='-',
            key='mikrotik.irq[' + irqitem.get('users').replace(",", "__") + ']',
            unixtime=unixtime,
            value=zabbix_escape(irqitem['count'])
        ))
