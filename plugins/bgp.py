# -*- coding: UTF-8 -*-
"""
This module pokes Mikrotik for BGP Counters
"""
import logging
import time
import pprint

from libs.time import time_convert
from libs.strings import zabbix_escape


def run(api, ts=False, log=logging.getLogger(__name__), ver=''):
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

    # The list of BGP values to monitor
    values_to_monitor = {
        "6": {
            'remote-as': 'remote-as',                    # Remote AS for peer
            'prefix-count': 'prefix-count',              # Accepted Prefixes
            'disabled': 'disabled',                      # Administrative status
            'comment': 'comment',                        # Printing the comment
            'updates-received': 'updates-received',      # Updates Received
            'updates-sent': 'updates-sent',              # Updates Sent
            'withdrawn-received': 'withdrawn-received',  # Withdrawn Received
            'withdrawn-sent': 'withdrawn-sent'           # Withdrawn Sent
        },
        "7": {
            'remote-as': 'remote.as',                    # Remote AS for peer
            'prefix-count': 'prefix-count',              # Accepted Prefixes
            'updates-received': 'remote.messages',       # Updates Received
            'updates-sent': 'local.messages',            # Updates Sent
        }
    }

    if ver.startswith('7.'):
        log.debug("BGP: Dealing with firmware version 7.x ({ver})".format(
            ver=ver
        ))
        bgpstats = api(cmd='/routing/bgp/session/print')
        major_version = "7"
    else:
        log.debug("BGP: Dealing with firmware version 6.x ({ver})".format(
            ver=ver
        ))
        bgpstats = api(cmd='/routing/bgp/peer/print')
        major_version = "6"

    for bgpitem in bgpstats:
        log.debug("BGP: Fetching item {item}".format(
            item=bgpitem
        ))
        if log.getEffectiveLevel() <= logging.DEBUG:
            pprint.pp(bgpitem)

        """
            BGP item for RouterOS v 7.12 looks like this:
            {'.id': '*2800002',
             'name': 'ucomline-1',
             'remote.address': '78.x.x.x',
             'remote.as': 12883,
             'remote.id': '213.x.x.x',
             'remote.capabilities': 'mp,rr,as4,err',
             'remote.messages': 269324,
             'remote.bytes': 31476311,
             'remote.eor': 'ip',
             'local.role': 'ebgp-customer',
             'local.address': '78.x.x.x',
             'local.as': 34605,
             'local.id': '194.x.x.x',
             'local.capabilities': 'mp,rr,gr,as4',
             'local.messages': 139711,
             'local.bytes': 17700041,
             'local.eor': '',
             'output.affinity': 'alone',
             'output.procid': 23,
             'output.filter-chain': 'UCOMLINE-OUT',
             'output.network': 'BGP-Advertisements',
             'output.keep-sent-attributes': True,
             'input.procid': 22,
             'input.filter': 'UCOMLINE-IN',
             'ebgp': '',
             'hold-time': '1m30s',
             'keepalive-time': '30s',
             'uptime': '18h8m41s680ms',
             'last-started': '2023-11-17 08:50:29',
             'last-stopped': '2023-11-17 08:50:28',
             'prefix-count': 902665,
             'established': True} 
            BGP Item for 6.49.2 looks like this:
            {'.id': '*0',
             'name': 'ucomline',
             'instance': 'default',
             'remote-address': '78.x.x.x',
             'remote-as': 12883,
             'tcp-md5-key': '*****',
             'nexthop-choice': 'default',
             'multihop': False,
             'route-reflect': False,
             'hold-time': '1m30s',
             'keepalive-time': '30s',
             'ttl': 'default',
             'in-filter': 'UCOMLINE-IN',
             'out-filter': 'UCOMLINE-OUT',
             'address-families': 'ip',
             'update-source': 'vlan202',
             'default-originate': 'never',
             'remove-private-as': False,
             'as-override': False,
             'passive': False,
             'use-bfd': False,
             'remote-id': '213.x.x.x',
             'local-address': '78.x.x.x',
             'uptime': '19w3d21h51m11s',
             'prefix-count': 902668,
             'updates-sent': 1223,
             'updates-received': 74537047,
             'withdrawn-sent': 800,
             'withdrawn-received': 4966247,
             'remote-hold-time': '3m',
             'used-hold-time': '1m30s',
             'used-keepalive-time': '30s',
             'refresh-capability': True,
             'as4-capability': True,
             'state': 'established',
             'established': True,
             'disabled': False,
             'comment': 'Ucomline'}
        """

        for zabbix_key, ros_key in values_to_monitor[major_version].items():
            print("{host} \"{key}\"{unixtime}{value}".format(
                host='-',
                key='mikrotik.bgp.node[{name},{val}]'.format(
                    name=bgpitem['name'],
                    val=zabbix_key
                ),
                unixtime=unixtime,
                value=zabbix_escape(bgpitem.get(ros_key, 0))
            ))

        # Established time for peer
        uptime = bgpitem.get('uptime', '0s')
        print("{host} \"{key}\"{unixtime}{value}".format(
            host='-',
            key='mikrotik.bgp.node[{name},uptime]'.format(
                name=bgpitem['name']
            ),
            unixtime=unixtime,
            # value=bgpitem['uptime']
            value=zabbix_escape(time_convert(uptime))
        ))

        if not ver.startswith('7.'):
            state = bgpitem.get('state', 'disabled')
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
