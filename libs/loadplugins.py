# -*- coding: UTF-8 -*-
"""
The idea and the code mainly had been found at https://copyninja.info/blog/dynamic-module-loading.html

"""

import os
import sys
import re
import importlib


def load_plugins(p_root_dir=os.path.dirname(__file__), p_dir='plugins'):
    """
    Dynamically loads the *.py files (except these starting with __) as modules.
    :param p_root_dir: the root folder where to search for the plugins dir
    :param p_dir: the name of the directory in the root dir where to search for the plugins
    :return: the list of modules
    """

    pysearchre = re.compile('.py$', re.IGNORECASE)
    pluginfiles = filter(pysearchre.search,
                         os.listdir(os.path.join(p_root_dir, p_dir)))

    form_module = lambda fp: '.' + os.path.splitext(fp)[0]
    plugins = map(form_module, pluginfiles)

    # import parent module / namespace
    importlib.import_module(p_dir)
    modules = []
    for plugin in plugins:
        if not plugin.startswith('.__'):
            sys.stderr.write('Loading ' + plugin + ' from ' + os.path.join(p_root_dir, p_dir) + '\n')
            modules.append(importlib.import_module(plugin, package=p_dir))

    return modules
