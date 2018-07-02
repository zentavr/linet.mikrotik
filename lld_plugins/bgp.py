# -*- coding: UTF-8 -*-
"""
This module pokes Mikrotik for BGP Peers
"""
import json


def run(api):
    """
    Returns BGP LLD JSON
    :param api: initialized librouteros' connect()
    :return:
    """
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
    print "{host} {key} {value}".format(
        host='-',
        key='mikrotik.bgp.discovery',
        value=json.dumps(json_data)
    )
