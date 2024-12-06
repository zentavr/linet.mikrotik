# -*- coding: UTF-8 -*-

import re

def time_convert(t):
    """
    Converts Mikrotik's time string to seconds
    :param t: Mikrotik's time string
    :return: seconds
    """
    # print("Received time: {time}".format(time=t))

    # Validate the format first
    if not re.fullmatch(r"(\d+[a-zA-Z]+)+", t):
        raise Exception("Invalid format: {time}".format(time=t))

    time_regex = re.findall(r"(?P<count>\d+)(?P<time_mult>[a-zA-Z]+)", t, flags=re.UNICODE)
    seconds = 0

    for count, time_mult in time_regex:
        # print("Time item: {count}{time_mult}".format(
        #     count=count,
        #     time_mult=time_mult)
        # )
        count = int(count)

        if time_mult == 'ms':
            # print("{count} msec".format(count=count))
            seconds += 0
        elif time_mult == 's':
            # print("{count} sec".format(count=count))
            seconds += count
        elif time_mult == 'm':
            # print("{count} min".format(count=count))
            seconds += count * 60
        elif time_mult == 'h':
            # print("{count} hours".format(count=count))
            seconds += count * 60 * 60
        elif time_mult == 'd':
            # print("{count} days".format(count=count))
            seconds += count * 60 * 60 * 24
        elif time_mult == 'w':
            # print("{count} weeks".format(count=count))
            seconds += count * 60 * 60 * 24 * 7
        else:
            raise Exception("Have no idea how to deal with {time_mult} value".format(
                time_mult=time_mult
            ))

    return seconds
