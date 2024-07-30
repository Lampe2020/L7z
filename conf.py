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

def get(conf_name:str, section:str='L7z', fallback:str='') -> str:
    """
    Retrieve a config value
    :param conf_name:
    :param section:
    :return:
    """
    try:
        return config[section][conf_name]
    except:
        return fallback

def set(conf_name:str, section:str='L7z', value:any='') -> bool:
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

def getbool(conf_name:str, section:str='L7z', fallback:bool=False) -> bool:
    """
    Retrieve a config value as a boolean
    :param conf_name:
    :param section:
    :param fallback:
    :return:
    """
    try:
        return config.getboolean(section, conf_name)
    except:
        return fallback

def getint(conf_name:str, section:str='L7z', fallback:int=0) -> int:
    """
    Retrieve a config value as an int
    :param conf_name:
    :param section:
    :param fallback:
    :return:
    """
    try:
        return config.getint(section, conf_name)
    except:
        return fallback

def getfloat(conf_name:str, section:str='L7z', fallback:float=0) -> float:
    """
    Retrieve a config value as a float
    :param conf_name:
    :param section:
    :param fallback:
    :return:
    """
    try:
        return config.getfloat(section, conf_name)
    except:
        return fallback

__all__ = ['get', 'set', 'getbool', 'getint', 'getfloat']

# Create a new config file or repair the existing one
... #TODO: Implement this
if not 'L7z' in config.sections():
    config['L7z'] = {
        'lang': get_sys_lang()[:2]  # For example 'sv_SE.UTF-8' → 'sv'
    }
if not 'Window' in config.sections():
    config['Window'] = {
        'native_menubar': 'off',
        'dimensions': '0,0,800,600',
        'maximized': 'false'
    }
    os.makedirs(os.path.dirname(configpath), exist_ok=True) # Create the config directory if it doesn't already exist
    with open(configpath, 'w') as conf_file:
        config.write(conf_file)
