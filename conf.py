#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
L7z config handler
"""

import configparser, os
config:configparser.ConfigParser = configparser.ConfigParser()
configpath:str = os.path.expanduser('~/.config/l7z.conf')
config.read(configpath)

def get_sys_lang() -> str:
    """
    Retrieves the default language.
    :return:
    """
    try:
        return os.environ['LANG']
    except OSError:
        return 'en'

if not 'L7z' in config.sections():
    config['L7z'] = {
        'lang': get_sys_lang()[:2]  # For example 'sv_SE.UTF-8' → 'sv'
    }
    os.makedirs(os.path.dirname(configpath), exist_ok=True) # Create the config directory if it doesn't already exist
    with open(configpath, 'w') as conf_file:
        config.write(conf_file)

def get(conf_name:str, section:str='L7z') -> any:
    """
    Retrieve a config value
    :param conf_name:
    :param section:
    :return:
    """
    return config[section][conf_name]

def set(conf_name:str, value:any, section:str='L7z') -> bool:
    """
    Change a config value
    :param conf_name:
    :param value:
    :param section:
    :return:
    """
    try:
        config[section][conf_name] = value
        with open(configpath, 'w') as conf_file:
            config.write(conf_file)
        return True
    except:
        return False

__all__ = ['get', 'set']

if __name__ == '__main__':
    """Create a new config or repair the existing one"""
    ... #TODO: Implement this
