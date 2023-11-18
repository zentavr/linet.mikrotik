# -*- coding: UTF-8 -*-
"""
This module pokes Mikrotik for BGP Peers
"""
import json
import time
from libs.strings import zabbix_escape
from logging import getLogger


def run(api, ts=False, log=getLogger(__name__), ver=''):
    """
    Returns BGP LLD JSON
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

    peers = []

    if ver.startswith('7.'):
        bgpstats = api(cmd='/routing/bgp/connection/print')
        for bgpitem in bgpstats:
            peers.append(
                {
                    '{#PEERNAME}': bgpitem.get('name'),
                    #'{#PEERCOMMENT}': bgpitem.get('comment', ''),
                    '{#PEERAS}': bgpitem.get('remote.as'),
                    '{#PEERLOCALADDR}': bgpitem.get('local.address'),
                    '{#PEERREMOTEADDR}': bgpitem.get('remote.address'),
                    '{#PEERREMOTEID}': bgpitem.get('remote.id'),
                }
            )

    else:
        bgpstats = api(cmd='/routing/bgp/peer/print')
        for bgpitem in bgpstats:
            peers.append(
                {
                    '{#PEERNAME}': bgpitem.get('name'),
                    '{#PEERCOMMENT}': bgpitem.get('comment', ''),
                    '{#PEERAS}': bgpitem.get('remote-as'),
                    '{#PEERLOCALADDR}': bgpitem.get('local-address'),
                    '{#PEERREMOTEADDR}': bgpitem.get('remote-address'),
                    '{#PEERREMOTEID}': bgpitem.get('remote-id'),
                }
            )

    # Composing JSON to return
    json_data = {
        'data': peers
    }

    # Return JSON
    print("{host} {key}{unixtime}{value}".format(
        host='-',
        key='mikrotik.bgp.discovery',
        unixtime=unixtime,
        value=zabbix_escape(json.dumps(json_data))
    ))
