#!/usr/bin/env python

import argparse
import ssl
import os
# import pprint

from librouteros import connect
from libs.loadplugins import load_plugins


def main():
    parser = argparse.ArgumentParser(description='Zabbix Helper')
    parser.add_argument('-H', '--hostname', default='', dest='hostname', help='API Hostname.')
    parser.add_argument('-u', '--user', default='admin', dest='username', help='API User.')
    parser.add_argument('-p', '--password', default='', dest='password', help='API Password.')
    parser.add_argument('-s', '--ssl', dest='use_ssl', action='store_true', help='Use SSL.')
    parser.add_argument('-P', '--plugins', dest='plugins', default='plugins', help='The folder related to this file '
                                                                                   'where to seek for the plugins')

    args = parser.parse_args()

    # Connection Arguments
    connect_args = {
        'port': 8728
    }

    if args.use_ssl:
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

    # pp = pprint.PrettyPrinter(indent=4)

    # Dynamically import the modules
    modules = load_plugins(os.path.dirname(__file__), args.plugins)
    for m in modules:
        # pp.pprint(m)
        m.run(api)

    # Closing Mikrotik's API Session
    api.close()


if __name__ == '__main__':
    main()
