#!/usr/bin/env python

import argparse
import ssl
import pprint
from librouteros import connect


def main():
    parser = argparse.ArgumentParser(description='Linet Law #133/2017 Filler')
    parser.add_argument('-d', '--domains', default='/tmp/domains.txt', dest='domains',
                        help='File where to seek for the domains.')
    parser.add_argument('-H', '--hostname', default='', dest='hostname', help='API Hostname.')
    parser.add_argument('-u', '--user', default='admin', dest='username', help='API User.')
    parser.add_argument('-p', '--password', default='', dest='password', help='API Password.')

    parser.add_argument('-s', '--ssl', dest='use_ssl', action='store_true', help='Use SSL.')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Be verbose.')
    args = parser.parse_args()

    # Connection Arguments
    connect_args = {
        'port': 8728
    }

    with open(args.domains, 'r') as domains:
        if args.use_ssl:
            print "SSL will be used"
            ssl_ctx = ssl.create_default_context()
            ssl_ctx.check_hostname = False
            ssl_ctx.verify_mode = ssl.CERT_NONE

            connect_args = {
                'port': 8729,
                'ssl_wrapper': ssl_ctx.wrap_socket
            }

        # Connect to Mikrotik
        api = connect(
            username=args.username,
            password=args.password,
            host=args.hostname,
            **connect_args
        )

        pp = pprint.PrettyPrinter(indent=4)
        # Fetch Something
        stuff = api(cmd='/interface/print')
        pp.pprint(stuff)

        api.close()

if __name__ == '__main__':
    main()
