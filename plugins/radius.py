# -*- coding: UTF-8 -*-
"""
This module pokes Mikrotik for Radius Counters
"""

# import pprint
from string import strip


def run(api):
    """
    Returns Radius Counters
    :param api: initialized librouteros' connect()
    :return:
    """

    # Fetch Incoming (CoA) stats
    # ({   u'acks': 263085, u'bad-requests': 0, u'naks': 11304, u'requests': 274388},)
    coastats = api(cmd='/radius/incoming/monitor', once=True)

    for coaitem in coastats:
        # Acknowledged
        print "{host} {key} {value}".format(
            host='-',
            key='mikrotik.radius-in.coa[acks]',
            value=coaitem['acks']
        )

        # Bad Requests
        print "{host} {key} {value}".format(
            host='-',
            key='mikrotik.radius-in.coa[bad-requests]',
            value=coaitem['bad-requests']
        )

        # Rejects
        print "{host} {key} {value}".format(
            host='-',
            key='mikrotik.radius-in.coa[naks]',
            value=coaitem['naks']
        )

        # Requests
        print "{host} {key} {value}".format(
            host='-',
            key='mikrotik.radius-in.coa[requests]',
            value=coaitem['requests']
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
            print "{host} {key} {value}".format(
                host='-',
                key='mikrotik.radius-out.node[' + strip(server.get('.id'), '*') + ',comment]',
                value=server.get('comment', server.get('.id'))
            )

            # Accepts
            print "{host} {key} {value}".format(
                host='-',
                key='mikrotik.radius-out.node[' + strip(server.get('.id'), '*') + ',accepts]',
                value=item.get('accepts')
            )

            # Bad Replies
            print "{host} {key} {value}".format(
                host='-',
                key='mikrotik.radius-out.node[' + strip(server.get('.id'), '*') + ',bad-replies]',
                value=item.get('bad-replies')
            )

            # pending
            print "{host} {key} {value}".format(
                host='-',
                key='mikrotik.radius-out.node[' + strip(server.get('.id'), '*') + ',pending]',
                value=item.get('pending')
            )

            # Rejects
            print "{host} {key} {value}".format(
                host='-',
                key='mikrotik.radius-out.node[' + strip(server.get('.id'), '*') + ',rejects]',
                value=item.get('rejects')
            )

            # Requests
            print "{host} {key} {value}".format(
                host='-',
                key='mikrotik.radius-out.node[' + strip(server.get('.id'), '*') + ',requests]',
                value=item.get('requests')
            )

            # Resends
            print "{host} {key} {value}".format(
                host='-',
                key='mikrotik.radius-out.node[' + strip(server.get('.id'), '*') + ',resends]',
                value=item.get('resends')
            )

            # Timeouts
            print "{host} {key} {value}".format(
                host='-',
                key='mikrotik.radius-out.node[' + strip(server.get('.id'), '*') + ',timeouts]',
                value=item.get('timeouts')
            )
