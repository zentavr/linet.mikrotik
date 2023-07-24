# -*- coding: UTF-8 -*-
# /ip firewall filter print stats where comment ~ ".*Hotspot.*AUTH"
# /ip firewall filter print stats where comment ~ ".*Hotspot.*ACC"
# /ip firewall filter print stats where comment ~ ".*DHCP.*AUTH"
# /ip firewall filter print stats where comment ~ ".*DHCP.*ACC"
"""
This module pokes Mikrotik for Firewall Counters
"""
import time
import pprint

from libs.strings import zabbix_escape
from logging import getLogger


def run(api, ts=False, log=getLogger(__name__), ver=''):
    """
    Returns firewall counters
    :param api: initialized librouteros' connect()
    :param ts: Use timestamps
    :return:
    """
    pp = pprint.PrettyPrinter(indent=4)

    if ts:
        unixtime = " {time} ".format(
            time=int(time.time())
        )
    else:
        unixtime = " "

    # Fetch firewall stats
    tables = [
        "filter",
        "nat",
        "mangle",
        "raw"
    ]

    for t in tables:
        log.debug("Processing {table} firewall table".format(
            table=t
        ))

        cmd = '/ip/firewall/{table}/print'.format(table=t)

        log.debug(pp.pformat(cmd))

        stats = api(
            cmd=cmd,
            stats=True
        )

        metrics_to_monitor = [
            'bytes',
            'packets',
            'disabled',
            # 'comment'
        ]

        for rule in stats:
            """
            {   
                u'.id': u'*3D',
                u'action': u'accept',
                u'bytes': 113970290691,
                u'chain': u'forward',
                u'comment': u'Allow Incoming from CORE to WAN',
                u'disabled': False,
                u'dynamic': False,
                u'in-interface-list': u'CORE',
                u'invalid': False,
                u'log': False,
                u'log-prefix': u'',
                u'out-interface-list': u'WAN',
                u'packets': 102508788
            }
            """

            # We don't want ALL the rules here. We want only those, which has ZBX at the beginning of the comment
            comment = rule.get('comment', '')
            if not comment.startswith('ZBX'):
                continue

            log.info(pp.pformat(comment))
            for metric in metrics_to_monitor:
                print("{host} \"{key}\"{unixtime}{value}".format(
                    host='-',
                    key='mikrotik.firewall[{table}_{id},{metric}]'.format(
                        table=t,
                        id=rule.get('.id').strip('*'),
                        metric=metric
                    ),
                    unixtime=unixtime,
                    value=zabbix_escape(rule.get(metric))
                ))
