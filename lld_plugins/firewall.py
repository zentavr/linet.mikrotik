# -*- coding: UTF-8 -*-
"""
This module pokes Mikrotik for Firewall Rules
"""
import json
import time
import pprint
from string import strip
from libs.strings import zabbix_escape
from logging import getLogger


def run(api, ts=False, log=getLogger(__name__)):
    """
    Returns Firewall Rules LLD JSON
    :param api: initialized librouteros' connect()
    :param ts: Use timestamps
    :return:
    """
    pp = pprint.PrettyPrinter(indent=4)

    if ts:
        unixtime = " {time} ".format(
            time=int(time.time())
        )
    else:
        unixtime = " "

    # Fetch firewall stats
    tables = [
        "filter",
        "nat",
        "mangle",
        "raw"
    ]

    lld = []

    for t in tables:
        log.debug("Processing {table} firewall table".format(
            table=t
        ))

        cmd = '/ip/firewall/{table}/print'.format(table=t)

        log.debug(pp.pformat(cmd))

        stats = api(
            cmd=cmd,
            stats=True
        )

        for rule in stats:
            # We don't want ALL the rules here. We want only those, which has ZBX at the beginning of the comment
            comment = rule.get('comment', '')
            if not comment.startswith('ZBX'):
                continue

            lld.append(
                {
                    '{#MTIK_FW_RULE_ID}': t + '_' + strip(rule.get('.id'), '*'),
                    '{#MTIK_FW_RULE_COMMENT}': rule.get('comment', rule.get('.id'))
                }
            )

    # Composing JSON to return
    json_data = {
        'data': lld
    }

    # Return JSON
    print "{host} {key}{unixtime}{value}".format(
        host='-',
        key='mikrotik.firewall.discovery',
        unixtime=unixtime,
        value=zabbix_escape(json.dumps(json_data))
    )
