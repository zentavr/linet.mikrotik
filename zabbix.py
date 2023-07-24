#!/usr/bin/env python

import argparse
import ssl
import os
import logging
from sys import stdout, stdin, stderr
import re
#import pprint

from librouteros import connect
from libs.loadplugins import load_plugins
from librouteros.login import plain, token


def main():
    parser = argparse.ArgumentParser(description='Zabbix Helper')
    parser.add_argument('-H', '--hostname', default='', dest='hostname', help='API Hostname.')
    parser.add_argument('-e', '--encoding', default='ASCII', dest='encoding',
                        help='The encoding to use during the connect')
    parser.add_argument('-u', '--user', default='admin', dest='username', help='API User.')
    parser.add_argument('-p', '--password', default='', dest='password', help='API Password.')
    parser.add_argument('-s', '--ssl', dest='use_ssl', action='store_true', help='Use SSL.')
    parser.add_argument('-t', '--timestamps', dest='use_timestamps', action='store_true',
                        help='Use unixtime timestamps.')
    parser.add_argument('-P', '--plugins', dest='plugins', default='plugins', help='The folder related to this file '
                                                                                   'where to seek for the plugins')
    parser.add_argument('-m', '--login-method', dest='login_method', default='login_plain',
                        choices=['plain', 'token'], help='Mikrotik login method to use. "plain" for '
                        'firmware>=6.43, "token" for firmware<6.43.')
    parser.add_argument("-v", "--verbosity", action="count", dest='verbosity', help="increase output verbosity")

    args = parser.parse_args()

    # Setting up loglevels
    liblog = logging.getLogger('librouteros')
    applog = logging.getLogger('application')

    console = logging.StreamHandler(stderr)
    formatter = logging.Formatter(fmt='%(message)s')
    console.setFormatter(formatter)

    if args.verbosity == 1:
        liblog.setLevel(logging.ERROR)
        applog.setLevel(logging.ERROR)
    elif args.verbosity == 2:
        liblog.setLevel(logging.WARNING)
        applog.setLevel(logging.WARNING)
    elif args.verbosity == 3:
        liblog.setLevel(logging.INFO)
        applog.setLevel(logging.INFO)
    elif args.verbosity > 3:
        liblog.setLevel(logging.DEBUG)
        applog.setLevel(logging.DEBUG)

    # Set up librouteros logging
    liblog.addHandler(console)
    applog.addHandler(console)

    # Connection Arguments
    connect_args = {
        'encoding': args.encoding,
        'port': 8728
    }

    if args.use_ssl:
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE
        ssl_wrapper = ssl_ctx.wrap_socket

        connect_args.update(port=8729)
        connect_args.update(ssl_wrapper=ssl_wrapper)

    # Dynamically init the class (we expect login_plain() or login_token() here)
    method = globals()[args.login_method]
    login_methods = (method, )

    # Connect to Mikrotik
    api = connect(
        username=args.username,
        password=args.password,
        host=args.hostname,
        login_methods=login_methods,
        **connect_args
    )

    # pp = pprint.PrettyPrinter(indent=4)

    resources = api(cmd='/system/resource/print')
    firmware_version = ''
    firmware_re = re.compile(r'^(?P<version>\d+\.\d+\.\d+)')
    for r in resources:
        version_raw = r['version']
        match = firmware_re.match(version_raw)
        if match:
            firmware_version = match.group('version')

    # Dynamically import the modules
    modules = load_plugins(os.path.dirname(__file__), args.plugins)
    for m in modules:
        # pp.pprint(m)
        m.run(api, args.use_timestamps, applog, firmware_version)

    # Closing Mikrotik's API Session
    api.close()


if __name__ == '__main__':
    main()
