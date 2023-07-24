# -*- coding: UTF-8 -*-
"""
This module pokes Mikrotik for BGP Counters
"""
import time
from libs.time import time_convert
from libs.strings import zabbix_escape
from logging import getLogger


def run(api, ts=False, log=getLogger(__name__), ver=''):
    """
    Returns BGP Counters
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

    if ver.startswith('7.'):
        bgpstats = api(cmd='/routing/bgp/connection/print')
    else:
        bgpstats = api(cmd='/routing/bgp/peer/print')

    # The list of BGP values to monitor
    values_to_monitor = [
        'remote-as',           # Remote AS for peer
        'prefix-count',        # Accepted Prefixes
        'disabled',            # Administrative status
        # 'uptime',              # Established time for peer
        'comment',             # Printing the comment
        'updates-received',    # Updates Received
        'updates-sent',        # Updates Sent
        'withdrawn-received',  # Withdrawn Received
        'withdrawn-sent'       # Withdrawn Sent
    ]

    for bgpitem in bgpstats:
        for val in values_to_monitor:
            print("{host} \"{key}\"{unixtime}{value}".format(
                host='-',
                key='mikrotik.bgp.node[{name},{val}]'.format(
                    name=bgpitem['name'],
                    val=val
                ),
                unixtime=unixtime,
                value=zabbix_escape(bgpitem.get(val, 0))
            ))

        state = bgpitem.get('state', 'disabled')
        uptime = bgpitem.get('uptime', '0s')

        # operational status
        if state == "idle":
            bgp_state = 1
        elif state == "connect":
            bgp_state = 2
        elif state == "active":
            bgp_state = 3
        elif state == "opensent":
            bgp_state = 4
        elif state == "openconfirm":
            bgp_state = 5
        elif state == "established":
            bgp_state = 6
        else:
            bgp_state = 0

        print("{host} \"{key}\"{unixtime}{value}".format(
            host='-',
            key='mikrotik.bgp.node[{name},state]'.format(
                name=bgpitem['name']
            ),
            unixtime=unixtime,
            value=zabbix_escape(bgp_state)
        ))

        # Established time for peer
        print("{host} \"{key}\"{unixtime}{value}".format(
            host='-',
            key='mikrotik.bgp.node[{name},uptime]'.format(
                name=bgpitem['name']
            ),
            unixtime=unixtime,
            # value=bgpitem['uptime']
            value=zabbix_escape(time_convert(uptime))
        ))
