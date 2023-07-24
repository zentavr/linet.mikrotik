# -*- coding: UTF-8 -*-
"""
The idea and the code mainly had been found at https://copyninja.info/blog/dynamic-module-loading.html

"""
import re


def zabbix_escape(st):
    """
    Escapes the string as Zabbix wants
    :param st: string
    :return: escaped string
    """

    # + Quoted and non - quoted entries are supported.
    # + Double - quote is the quoting character.
    # + Entries with whitespace must be quoted.
    # + Double - quote and backslash characters inside quoted entry must be escaped with a backslash.
    # + Escaping is not supported in non - quoted entries.
    # + Linefeed escape sequences(\n) are supported in quoted strings.
    # + Linefeed escape sequences are trimmed from the end of an entry.

    #> https://www.cmi.ac.in/~madhavan/courses/python-2011/docs/diveintopython3/porting-code-to-python-3-with-2to3.html#types
    # (types.StringType, types.UnicodeType, types.BufferType) => (bytes, str, memoryview)
    if isinstance(st, (bytes, str, memoryview)):
        st = re.sub(r'(\"|\\)',
                    lambda m: {
                         '\"': '\\"',
                         '\\': '\\\\',
                    }[m.group()],
                    st)

    return '"{string}"'.format(
        string=st
    )
