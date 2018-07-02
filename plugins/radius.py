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

    for coaitem in coastats:
        # Acknowledged
        print "{host} {key}{unixtime}{value}".format(
            host='-',
            key='mikrotik.radius-in.coa[acks]',
            unixtime=unixtime,
            value=zabbix_escape(coaitem['acks'])
        )

        # Bad Requests
        print "{host} {key}{unixtime}{value}".format(
            host='-',
            key='mikrotik.radius-in.coa[bad-requests]',
            unixtime=unixtime,
            value=zabbix_escape(coaitem['bad-requests'])
        )

        # Rejects
        print "{host} {key}{unixtime}{value}".format(
            host='-',
            key='mikrotik.radius-in.coa[naks]',
            unixtime=unixtime,
            value=zabbix_escape(coaitem['naks'])
        )

        # Requests
        print "{host} {key}{unixtime}{value}".format(
            host='-',
            key='mikrotik.radius-in.coa[requests]',
            unixtime=unixtime,
            value=zabbix_escape(coaitem['requests'])
        )

    # We need to figure out which Radius settings do we have
    radservers = api(cmd='/radius/print')

    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(radservers)

    for server in radservers:
        # Lets fetch the stats for the every server
        params = {'.id': server.get('.id')}
        stats = api(cmd='/radius/monitor', once=True, **params)
        # pp.pprint(stats)

        for item in stats:
            # Printing the comment
            print "{host} {key}{unixtime}{value}".format(
                host='-',
                key='mikrotik.radius-out.node[' + strip(server.get('.id'), '*') + ',comment]',
                unixtime=unixtime,
                value=zabbix_escape(server.get('comment', server.get('.id')))
            )

            # Accepts
            print "{host} {key}{unixtime}{value}".format(
                host='-',
                key='mikrotik.radius-out.node[' + strip(server.get('.id'), '*') + ',accepts]',
                unixtime=unixtime,
                value=zabbix_escape(item.get('accepts'))
            )

            # Bad Replies
            print "{host} {key}{unixtime}{value}".format(
                host='-',
                key='mikrotik.radius-out.node[' + strip(server.get('.id'), '*') + ',bad-replies]',
                unixtime=unixtime,
                value=zabbix_escape(item.get('bad-replies'))
            )

            # pending
            print "{host} {key}{unixtime}{value}".format(
                host='-',
                key='mikrotik.radius-out.node[' + strip(server.get('.id'), '*') + ',pending]',
                unixtime=unixtime,
                value=zabbix_escape(item.get('pending'))
            )

            # Rejects
            print "{host} {key}{unixtime}{value}".format(
                host='-',
                key='mikrotik.radius-out.node[' + strip(server.get('.id'), '*') + ',rejects]',
                unixtime=unixtime,
                value=zabbix_escape(item.get('rejects'))
            )

            # Requests
            print "{host} {key}{unixtime}{value}".format(
                host='-',
                key='mikrotik.radius-out.node[' + strip(server.get('.id'), '*') + ',requests]',
                unixtime=unixtime,
                value=zabbix_escape(item.get('requests'))
            )

            # Resends
            print "{host} {key}{unixtime}{value}".format(
                host='-',
                key='mikrotik.radius-out.node[' + strip(server.get('.id'), '*') + ',resends]',
                unixtime=unixtime,
                value=zabbix_escape(item.get('resends'))
            )

            # Timeouts
            print "{host} {key}{unixtime}{value}".format(
                host='-',
                key='mikrotik.radius-out.node[' + strip(server.get('.id'), '*') + ',timeouts]',
                unixtime=unixtime,
                value=zabbix_escape(item.get('timeouts'))
            )
