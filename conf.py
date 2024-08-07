#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
L7z config handler
"""

import configparser, typing, os, re

config:configparser.ConfigParser = configparser.ConfigParser(interpolation=None)
configpath:str = os.path.expanduser('~/.config/l7z.conf')
try:
    config.read(configpath)
except configparser.ParsingError:
    with open(configpath, 'w') as conf_file:
        conf_file.write('')

def get_sys_lang() -> str:
    """Retrieves the default language."""
    try:
        return os.environ['LANG']
    except OSError:
        return 'en'

def get(section:str, key:str, fallback:str='') -> str:
    """Retrieve a config value"""
    try:
        return config[section][key]
    except:
        return fallback

def set(section:str, key:str, value:any='') -> bool:
    """Change a config value"""
    try:
        config[section][key] = value
        with open(configpath, 'w') as conf_file:
            config.write(conf_file)
        return True
    except:
        return False

def getbool(section:str, key:str, fallback:bool=False) -> bool:
    """Retrieve a config value as a boolean"""
    try:
        return config.getboolean(section, key)
    except:
        return fallback

def getint(section:str, key:str, fallback:int=0) -> int:
    """Retrieve a config value as an int"""
    try:
        return config.getint(section, key)
    except:
        return fallback

def getfloat(section:str, key:str, fallback:float=0) -> float:
    """Retrieve a config value as a float"""
    try:
        return config.getfloat(section, key)
    except:
        return fallback

# Create a new config file or repair the existing one
type_formats:dict[str, re.Pattern] = {
    'int': re.compile(r'^[0-9]|([1-9][0-9]*)$'),
    'float': re.compile(r'^[0-9]+\.[0-9]+$'),
    # Boolean format described in https://docs.python.org/3/library/configparser.html#supported-datatypes
    'bool': re.compile(r'(true)|(false)|(on)|(off)|(yes)|(no)|1|0', re.IGNORECASE)
}

def restore():
    """Restores the config into a usable state"""
    def repair_value(section:str, key:str, default:str, expected_format:str|re.Pattern|typing.Type|None=None) -> str:
        """Repairs a given config value according to the given parameters"""
        if not section in config.sections():
            config[section] = {key: default}
        if not key in config[section]:
            config[section][key] = default
        if not expected_format:
            return config[section][key]
        elif expected_format==int:
            expected_format = type_formats['int']
        elif expected_format==float:
            expected_format = type_formats['float']
        elif expected_format==bool:
            expected_format = type_formats['bool']
        elif not isinstance(expected_format, (str, re.Pattern)):    # If it isn't one of the above or one of these two
            raise TypeError(f'Got invalid {expected_format=} for {repr(section)}.{repr(key)}!') # Error out
        if not re.match(expected_format, config[section][key]):
            config[section][key] = default
        return config[section][key]
    repair_value('L7z', 'lang', get_sys_lang(), r'^[a-z]{2}(_[A-Z]{2})?$')
    repair_value('L7z', 'use_utc_time', 'no', bool)
    repair_value('L7z', 'timestamp_format', '%Y-%m-%d %H:%M')
    repair_value('Window', 'native_menubar', 'off', bool)
    repair_value('Window', 'dimensions', '0,0,800,600', f'^{type_formats["int"].pattern},{type_formats["int"].pattern},'
                                                        f'{type_formats["int"].pattern},{type_formats["int"].pattern}$')
    repair_value('Window', 'maximized', 'false', bool)
    repair_value('Fileview', 'view', 'details', r'^(large)|(small)|(list)|(detail)$')
    repair_value('Fileview', 'sort_by', 'name', f'^(name)|(type)|(date)|(size)|()$')
    repair_value('Fileview', 'flat', 'no', bool)
    repair_value('Fileview', 'second_panel', 'off', bool)
    repair_value('Fileview', 'auto-refresh', 'yes', bool)
    repair_value('Toolbars', 'archive', 'on', bool)
    repair_value('Toolbars', 'standard', 'on', bool)
    repair_value('Toolbars', 'large_buttons', 'yes', bool)
    repair_value('Toolbars', 'button_text', 'on', bool)
    repair_value('Locations', 'latest', '~')
    repair_value('Locations', 'latest_2nd', '~')
    for i in range(10):
        repair_value('Locations', f'bookmark_{i}', '')
    os.makedirs(os.path.dirname(configpath), exist_ok=True) # Create the config directory if it doesn't already exist
    with open(configpath, 'w') as conf_file:
        config.write(conf_file)

def reset():
    """Resets the config to the default"""
    with open(configpath, 'w') as conf_file:
        conf_file.write('')     # Delete all contents of the current config file
        conf_file.flush()
        for section in config.sections():
            config.remove_section(section)
    restore()

restore()   # Make sure the config is usable _before_ it gets used!

__all__ = ['get', 'set', 'getbool', 'getint', 'getfloat', 'restore', 'reset']
