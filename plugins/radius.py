# -*- coding: UTF-8 -*-
"""
This module pokes Mikrotik for Radius Counters
"""
import time
# import pprint

from string import strip
from libs.strings import zabbix_escape


def run(api, ts=False):
    """
    Returns Radius Counters
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

    # Fetch Incoming (CoA) stats
    # ({   u'acks': 263085, u'bad-requests': 0, u'naks': 11304, u'requests': 274388},)
    coastats = api(cmd='/radius/incoming/monitor', once=True)

    coa_values_to_monitor = [
        'acks',          # Acknowledged
        'bad-requests',  # Bad Requests
        'naks',          # Rejects
        'requests'       # Requests

    ]

    for coaitem in coastats:
        for val in coa_values_to_monitor:
            print "{host} \"{key}\"{unixtime}{value}".format(
                host='-',
                key='mikrotik.radius-in.coa[{val}]'.format(
                    val=val
                ),
                unixtime=unixtime,
                value=zabbix_escape(coaitem.get(val, 0))
            )

    # We need to figure out which Radius settings do we have
    radservers = api(cmd='/radius/print')

    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(radservers)

    radius_values_to_monitor = [
        'accepts',      # Accepts
        'bad-replies',  # Bad Replies
        'pending',      # Pending
        'rejects',      # Rejects
        'requests',     # Requests
        'resends',      # Resends
        'timeouts',     # Timeouts
        # 'comment'
    ]

    for server in radservers:
        # Lets fetch the stats for the every server
        params = {'.id': server.get('.id')}
        stats = api(cmd='/radius/monitor', once=True, **params)
        # pp.pprint(stats)

        for item in stats:
            for val in radius_values_to_monitor:
                print "{host} \"{key}\"{unixtime}{value}".format(
                    host='-',
                    key='mikrotik.radius-out.node[' + strip(server.get('.id'), '*') + ',' + val + ']',
                    unixtime=unixtime,
                    value=zabbix_escape(item.get(val))
                )
