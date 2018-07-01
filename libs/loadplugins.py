# -*- coding: UTF-8 -*-
"""
The idea and the code mainly had been found at https://copyninja.info/blog/dynamic-module-loading.html

"""

import os
import sys
import re
import importlib


def load_plugins(pdir=os.path.dirname(__file__)):
    """
    Dynamically loads the *.py files (except these starting with __) as modules.
    :param pdir: the root folder with the plugins
    :return: the list of modules
    """

    pysearchre = re.compile('.py$', re.IGNORECASE)
    pluginfiles = filter(pysearchre.search,
                         os.listdir(os.path.join(pdir,
                                                 'plugins')))

    form_module = lambda fp: '.' + os.path.splitext(fp)[0]
    plugins = map(form_module, pluginfiles)

    # import parent module / namespace
    importlib.import_module('plugins')
    modules = []
    for plugin in plugins:
        if not plugin.startswith('.__'):
            sys.stderr.write('Loading ' + plugin + '\n')
            modules.append(importlib.import_module(plugin, package="plugins"))

    return modules
