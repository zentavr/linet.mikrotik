# -*- coding: UTF-8 -*-
"""
This module pokes Mikrotik for Radius Servers
"""
import json
from string import strip


def run(api):
    """
    Returns Radius LLD JSON
    :param api: initialized librouteros' connect()
    :return:
    """
    radservers = api(cmd='/radius/print')

    servers = []

    for s in radservers:
        servers.append(
            {
                '{#MTIK_RADIUS_ID}': strip(s.get('.id'), '*'),
                '{#MTIK_RADIUS_COMMENT}': s.get('comment', s.get('.id')),
                '{#MTIK_RADIUS_ADDRESS}': s.get('address'),
            }
        )

    # Composing JSON to return
    json_data = {
        'data': servers
    }

    # Return JSON
    print "{host} {key} {value}".format(
        host='-',
        key='mikrotik.radius-out.discovery',
        value=json.dumps(json_data)
    )
