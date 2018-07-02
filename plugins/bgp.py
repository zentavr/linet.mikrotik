# -*- coding: UTF-8 -*-
"""
This module pokes Mikrotik for BGP Counters
"""

from libs.time import time_convert


def run(api):
    """
    Returns BGP Counters
    :param api: initialized librouteros' connect()
    :return:
    """
    bgpstats = api(cmd='/routing/bgp/peer/print')

    for bgpitem in bgpstats:
        # Remote AS for peer
        print "{host} {key} {value}".format(
            host='-',
            key='mikrotik.bgp.node[' + bgpitem['name'] + ',remote-as]',
            value=bgpitem['remote-as']
        )

        # Accepted Prefixes
        print "{host} {key} {value}".format(
            host='-',
            key='mikrotik.bgp.node[' + bgpitem['name'] + ',prefix-count]',
            value=bgpitem['prefix-count']
        )

        # Administrative status
        print "{host} {key} {value}".format(
            host='-',
            key='mikrotik.bgp.node[' + bgpitem['name'] + ',disabled]',
            value=bgpitem['disabled']
        )

        # Established time for peer
        print "{host} {key} {value}".format(
            host='-',
            key='mikrotik.bgp.node[' + bgpitem['name'] + ',uptime]',
            #value=bgpitem['uptime']
            value=time_convert(bgpitem['uptime'])
        )

        # operational status
        print "{host} {key} {value}".format(
            host='-',
            key='mikrotik.bgp.node[' + bgpitem['name'] + ',state]',
            value=bgpitem['state']
        )

        # Printing the comment
        print "{host} {key} {value}".format(
            host='-',
            key='mikrotik.bgp.node[' + bgpitem['name'] + ',comment]',
            value=bgpitem.get('comment', '')
        )

        # Updates Received
        print "{host} {key} {value}".format(
            host='-',
            key='mikrotik.bgp.node[' + bgpitem['name'] + ',updates-received]',
            value=bgpitem.get('updates-received')
        )

        # Updates Sent
        print "{host} {key} {value}".format(
            host='-',
            key='mikrotik.bgp.node[' + bgpitem['name'] + ',updates-sent]',
            value=bgpitem.get('updates-sent')
        )


        # Withdrawn Received
        print "{host} {key} {value}".format(
            host='-',
            key='mikrotik.bgp.node[' + bgpitem['name'] + ',withdrawn-received]',
            value=bgpitem.get('withdrawn-received')
        )

        # Withdrawn Sent
        print "{host} {key} {value}".format(
            host='-',
            key='mikrotik.bgp.node[' + bgpitem['name'] + ',withdrawn-sent]',
            value=bgpitem.get('withdrawn-sent')
        )
