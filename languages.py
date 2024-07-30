# -*- coding: utf-8 -*-

"""
A simple little language module based on gettext, for the use specifically in L7z.
Usage:
```
>>> from languages import *
>>> lang_en.install()
>>> # Do whatever you want. Then, if you want to switch to German, you can do:
>>> lang_de.install()   # and boom, now you get the German strings.
```
"""

import gettext, os, sys, conf

APP_NAME:str = 'l7z'
LOCALE_DIR:str = os.path.join(os.path.dirname(__file__), 'locales')
gettext.install(APP_NAME, LOCALE_DIR)

lang_en = gettext.translation(APP_NAME, languages=['en'], fallback=True)
lang_de = gettext.translation(APP_NAME, localedir=LOCALE_DIR, languages=['de'])
lang_sv = gettext.translation(APP_NAME, localedir=LOCALE_DIR, languages=['sv'])
#lang_ln = gettext.translation(APP_NAME, localedir=LOCALE_DIR, languages=['ln'])     # Custom language here, replace ln

match conf.get('lang'):
    case 'en':
        lang_en.install()
    case 'de':
        lang_de.install()
    case 'sv':
        lang_sv.install()
    # case 'ln':             # Custom language here, replace 'ln'
    #     lang_ln.install()  # with the language code of your language
    case language:
        sys_lang:str = conf.get_sys_lang()[:2]
        try:
            gettext.translation(APP_NAME, localedir=LOCALE_DIR, languages=[sys_lang])
            print(_('Unsupported lang in conf: {lang}, reverting to {sys_lang}.').format(
                lang=repr(language),
                sys_lang=repr(sys_lang)
            ), file=sys.stderr)
            conf.set('lang', sys_lang)
        except:
            lang_en.install()
            print(
                f"Unsupported lang in conf and unsupported system lang ({(lang, sys_lang)=}, reverting to 'en'",
                file=sys.stderr
            )
            conf.set('lang', value='en')

__all__ = list(obj for obj in locals() if obj.startswith('lang_'))
