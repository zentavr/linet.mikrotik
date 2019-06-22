# -*- coding: UTF-8 -*-
"""
This module pokes Mikrotik for BGP Peers
"""
import json
import time
from libs.strings import zabbix_escape
from logging import getLogger


def run(api, ts=False, log=getLogger(__name__)):
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

    bgpstats = api(cmd='/routing/bgp/peer/print')

    peers = []

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
    print "{host} {key}{unixtime}{value}".format(
        host='-',
        key='mikrotik.bgp.discovery',
        unixtime=unixtime,
        value=zabbix_escape(json.dumps(json_data))
    )
