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

    for bgpitem in bgpstats:
        # Remote AS for peer
        print "{host} {key}{unixtime}{value}".format(
            host='-',
            key='mikrotik.bgp.node[' + bgpitem['name'] + ',remote-as]',
            unixtime=unixtime,
            value=zabbix_escape(bgpitem['remote-as'])
        )

        # Accepted Prefixes
        print "{host} {key}{unixtime}{value}".format(
            host='-',
            key='mikrotik.bgp.node[' + bgpitem['name'] + ',prefix-count]',
            unixtime=unixtime,
            value=zabbix_escape(bgpitem['prefix-count'])
        )

        # Administrative status
        print "{host} {key}{unixtime}{value}".format(
            host='-',
            key='mikrotik.bgp.node[' + bgpitem['name'] + ',disabled]',
            unixtime=unixtime,
            value=zabbix_escape(bgpitem['disabled'])
        )

        # Established time for peer
        print "{host} {key}{unixtime}{value}".format(
            host='-',
            key='mikrotik.bgp.node[' + bgpitem['name'] + ',uptime]',
            unixtime=unixtime,
            #value=bgpitem['uptime']
            value=zabbix_escape(time_convert(bgpitem['uptime']))
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

        print "{host} {key}{unixtime}{value}".format(
            host='-',
            key='mikrotik.bgp.node[' + bgpitem['name'] + ',state]',
            unixtime=unixtime,
            value=zabbix_escape(bgp_state)
        )

        # Printing the comment
        print "{host} {key}{unixtime}{value}".format(
            host='-',
            key='mikrotik.bgp.node[' + bgpitem['name'] + ',comment]',
            unixtime=unixtime,
            value=zabbix_escape(bgpitem.get('comment', ''))
        )

        # Updates Received
        print "{host} {key}{unixtime}{value}".format(
            host='-',
            key='mikrotik.bgp.node[' + bgpitem['name'] + ',updates-received]',
            unixtime=unixtime,
            value=zabbix_escape(bgpitem.get('updates-received'))
        )

        # Updates Sent
        print "{host} {key}{unixtime}{value}".format(
            host='-',
            key='mikrotik.bgp.node[' + bgpitem['name'] + ',updates-sent]',
            unixtime=unixtime,
            value=zabbix_escape(bgpitem.get('updates-sent'))
        )


        # Withdrawn Received
        print "{host} {key}{unixtime}{value}".format(
            host='-',
            key='mikrotik.bgp.node[' + bgpitem['name'] + ',withdrawn-received]',
            unixtime=unixtime,
            value=zabbix_escape(bgpitem.get('withdrawn-received'))
        )

        # Withdrawn Sent
        print "{host} {key}{unixtime}{value}".format(
            host='-',
            key='mikrotik.bgp.node[' + bgpitem['name'] + ',withdrawn-sent]',
            unixtime=unixtime,
            value=zabbix_escape(bgpitem.get('withdrawn-sent'))
        )
