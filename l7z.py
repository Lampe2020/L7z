#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
# L7z - the 7-zip GUI for *NIX

TODO: Write short description and usage help, to be output when help is requested from the terminal
'''

import sys, os, conf

# Initialize the translation right-away so even the no-import message can be localized.
from languages import *

if __name__ != '__main__':
    msg:str = _("L7z is not intended to be imported!")
    print(f'\n\n{msg}\n\n', file=sys.stderr)
    raise ImportError(msg)

from PyQt6.QtWidgets import QApplication, QMainWindow

l7z_app:QApplication = QApplication(sys.argv)

class L7z_GUI(QMainWindow):
    """The main GUI class"""
    def __init__(self):
        """Initialize the main GUI"""
        super().__init__()
        self.setWindowTitle(_('7-zip • Unofficial GUI (WIP!)'))
        #self.setWindowIcon()
        ... #TODO:

#debug
print(_('Starting L7z on {platform}…').format(platform=sys.platform))

main_window:L7z_GUI = L7z_GUI()
main_window.show()
l7z_app.exec()
