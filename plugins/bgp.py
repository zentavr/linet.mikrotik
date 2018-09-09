# -*- coding: UTF-8 -*-
"""
This module pokes Mikrotik for BGP Counters
"""
import time
from libs.time import time_convert
from libs.strings import zabbix_escape


def run(api, ts=False):
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

    bgpstats = api(cmd='/routing/bgp/peer/print')

    # The list of BGP values to monitor
    values_to_monitor = [
        'remote-as',           # Remote AS for peer
        'prefix-count',        # Accepted Prefixes
        'disabled',            # Administrative status
        'uptime',              # Established time for peer
        'comment',             # Printing the comment
        'updates-received',    # Updates Received
        'updates-sent',        # Updates Sent
        'withdrawn-received',  # Withdrawn Received
        'withdrawn-sent'       # Withdrawn Sent
    ]

    for bgpitem in bgpstats:
        for val in values_to_monitor:
            print "{host} \"{key}\"{unixtime}{value}".format(
                host='-',
                key='mikrotik.bgp.node[{name},{val}]'.format(
                    name=bgpitem['name'],
                    val=val
                ),
                unixtime=unixtime,
                value=zabbix_escape(bgpitem.get(val, 0))
            )

        # operational status
        if bgpitem['state'] == "idle":
            bgp_state = 1
        elif bgpitem['state'] == "connect":
            bgp_state = 2
        elif bgpitem['state'] == "active":
            bgp_state = 3
        elif bgpitem['state'] == "opensent":
            bgp_state = 4
        elif bgpitem['state'] == "openconfirm":
            bgp_state = 5
        elif bgpitem['state'] == "established":
            bgp_state = 6
        else:
            bgp_state = 0

        print "{host} \"{key}\"{unixtime}{value}".format(
            host='-',
            key='mikrotik.bgp.node[{name},state]'.format(
                name=bgpitem['name']
            ),
            unixtime=unixtime,
            value=zabbix_escape(bgp_state)
        )
