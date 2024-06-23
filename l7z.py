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

INSTALL_DIR:str = os.path.dirname(__file__)

from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QDialog
from PyQt6.QtGui import QIcon, QAction

l7z_app:QApplication = QApplication(sys.argv)

class L7z_GUI(QMainWindow):
    """The main GUI class"""
    mb_menus:dict[str, QMenu] = {}
    ask_quit:bool = False
    def __init__(self):
        """Initialize the main GUI"""
        super().__init__()
        self.setWindowTitle(_('7-zip • Unofficial GUI (WIP!)'))
        self.setWindowIcon(QIcon(os.path.join(INSTALL_DIR, 'icons', '7-zip.png')))
        self.menubar:QMenuBar = self.menuBar()
        self.menubar.setNativeMenuBar(conf.getbool('native_menubar'))
        self.mb_menus.update({
            'file': QMenu(_('&File'), self),
            'help': QMenu(_('&Help'), self)
        })
        for menu in self.mb_menus.values():
            self.menubar.addMenu(menu)
        self.mb_menus['file'].addSeparator()
        quit_btn:QAction = QAction(_('&Quit'), self)
        quit_btn.setStatusTip(_('Quit 7-zip'))
        quit_btn.triggered.connect(self.quit)
        self.mb_menus['file'].addAction(quit_btn)
        ... # Maybe I should completely start from scratch and redo this whole thing in QML and (I've heard it's
        # possible) JS embedded into that? I'm much more used to HTML+CSS+JS, so that would maybe be closer to that
        # workflow of creating graphical stuff.


    def show_about(self):
        """Show the "About" dialogue"""
        ... #TODO: Implement "About" dialog

    def quit(self):
        """Quit the app smoothly."""
        if self.ask_quit:
            ... #TODO: Implement a "Close?" dialog
        self.destroy(True, True)
        return sys.exit(0)

#debug
print(_('Starting L7z on {platform}…').format(platform=sys.platform))

main_window:L7z_GUI = L7z_GUI()
main_window.show()
l7z_app.exec()
