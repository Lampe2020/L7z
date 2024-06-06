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

import gettext, os

APP_NAME:str = 'l7z'
LOCALE_DIR:str = os.path.join(os.path.dirname(__file__), 'locales')
gettext.install(APP_NAME, LOCALE_DIR)

lang_en = gettext.translation(APP_NAME, languages=['en'], fallback=True)
print(gettext.find(domain=APP_NAME, localedir=LOCALE_DIR, languages=['de']))
lang_de = gettext.translation(APP_NAME, localedir=LOCALE_DIR, languages=['de'])
lang_sv = gettext.translation(APP_NAME, localedir=LOCALE_DIR, languages=['sv'])

translate = (lambda msg: msg)
translate.__doc__ = """
Dummy translation function.
To mark strings for translation with this, tell the tool (like e.g. pygettext) to use this as a marker:
$ pygettext3 -k translate
"""

__all__ = [*(lang for lang in locals() if lang.startswith('lang_')), 'translate']
