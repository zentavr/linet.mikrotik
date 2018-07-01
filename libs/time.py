# -*- coding: UTF-8 -*-

import re


def time_convert(t):
    """
    Converts Mikrotik's time string to seconds
    :param t: Mikrotik's time string
    :return: seconds
    """
    timeRegEx = re.split('(\d+\w)', t, flags=re.UNICODE)
    seconds = 0

    for time_item in timeRegEx:
        match = re.match(r"(?P<count>\d+)(?P<time_mult>\w)", time_item)
        if match:
            if match.group('time_mult') == 's':
                # print "{count} sec".format(count=bgp_match.group('count'))
                seconds += int(match.group('count'))
            elif match.group('time_mult') == 'm':
                # print "{count} min".format(count=bgp_match.group('count'))
                seconds += int(match.group('count')) * 60
            elif match.group('time_mult') == 'h':
                # print "{count} hours".format(count=bgp_match.group('count'))
                seconds += int(match.group('count')) * 60 * 60
            elif match.group('time_mult') == 'd':
                # print "{count} days".format(count=bgp_match.group('count'))
                seconds += int(match.group('count')) * 60 * 60 * 24
            elif match.group('time_mult') == 'w':
                # print "{count} weeks".format(count=bgp_match.group('count'))
                seconds += int(match.group('count')) * 60 * 60 * 24 * 7
            else:
                raise Exception("Have no idea how to deal with {time_mult} value".format(
                    time_mult=match.group('time_mult')
                ))

    return seconds
