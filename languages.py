# -*- coding: utf-8 -*-

"""
L7z's language module
"""

import gettext, os, sys, conf

APP_NAME:str = 'l7z'
LOCALE_DIR:str = os.path.join(os.path.dirname(__file__), 'locales')
gettext.install(APP_NAME, LOCALE_DIR)

lang_en = gettext.translation(APP_NAME, languages=['en', 'en_US', 'en_US.UTF-8', 'C', 'C.UTF-8'], fallback=True)
lang_de = gettext.translation(APP_NAME, localedir=LOCALE_DIR, languages=['de', 'de_DE', 'de_DE.UTF-8'])
lang_sv = gettext.translation(APP_NAME, localedir=LOCALE_DIR, languages=['sv', 'sv_SE', 'sv_SE.UTF-8'])
#lang_ln = gettext.translation(APP_NAME, localedir=LOCALE_DIR, languages=['ln'])     # Custom language here, replace ln

match conf.get('L7z', 'lang'):
    case 'en'|'en_US'|'en_US.UTF-8'|'C'|'C.UTF-8':
        lang_en.install()
    case 'de'|'de_DE'|'de_DE.UTF-8':
        lang_de.install()
    case 'sv'|'sv_SE'|'sv_SE.UTF-8':
        lang_sv.install()
    # case 'ln':             # Custom language here, replace 'ln'
    #     lang_ln.install()  # with the language code of your language
    case language:
        sys_lang:str = conf.get_sys_lang()
        try:
            gettext.translation(APP_NAME, localedir=LOCALE_DIR, languages=[sys_lang])
            print(_('Unsupported lang in conf: {lang}, reverting to {sys_lang}.').format(
                lang=repr(language),
                sys_lang=repr(sys_lang)
            ), file=sys.stderr)
            conf.set('L7z', 'lang', sys_lang)
        except:
            lang_en.install()
            print(
                f"Unsupported lang in conf and unsupported system lang ({(lang, sys_lang)=}, reverting to 'en'",
                file=sys.stderr
            )
            conf.set('L7z', 'lang', value='en')

__all__:list[str] = list(obj for obj in locals() if obj.startswith('lang_'))
