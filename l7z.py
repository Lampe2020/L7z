#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
# L7z - the 7-zip GUI for *NIX

TODO: Write short description and usage help, to be output when help is requested from the terminal
'''

import sys, os, conf, datetime
from typing import Callable

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
    ask_quit:bool = False
    def __init__(self):
        """Initialize the main GUI"""
        super().__init__()
        self.setWindowTitle(_('7-zip • Unofficial GUI (WIP!)'))
        self.setWindowIcon(QIcon(os.path.join(INSTALL_DIR, 'icons', '7-zip.png')))
        self.menubar:QMenuBar = self.menuBar()
        self.menubar.setNativeMenuBar(conf.getbool('native_menubar'))

        ###########################
        # Initialize the menu bar #
        ###########################
        menus:dict[str, QMenu] = {
            'file': QMenu(_('&File'), self),
            'file/CRC': QMenu(_('CRC'), self),
            'edit': QMenu(_('&Edit'), self),
            'view': QMenu(_('&View'), self),
                                   # ↓ is updated whenever the menu is opened, so doesn't need to be translated
            'view/timeformat': QMenu(datetime.datetime.now().strftime('%Y-%m-%d'), self),
            'view/toolbars': QMenu(_('Toolbars'), self),
            'favorites': QMenu(_('F&avorites'), self),
            'favorites/add': QMenu(_('&Add folder to favorites as'), self),
            'tools': QMenu(_('&Tools'), self),
            'help': QMenu(_('&Help'), self)
        }
        # In the following there are a few `if True` blocks, there are just for structuring the code according to the
        # menu it's currently working on.
        if True:    # 'file'
            menus['file'].addActions((
                self.__gen_QAction(
                    _('&Open'),
                    self.open_selected,
                    self.open_selected.__doc__,
                    _('Enter')
                ),
                self.__gen_QAction(
                    _('Open &Inside'),
                    self.open_selected_inside,
                    self.open_selected_inside.__doc__,
                    _('Ctrl+PgDn')
                ),
                self.__gen_QAction(
                    _('Open Inside *'),
                    self.open_selected_star,
                    self.open_selected_star.__doc__,
                    None
                ),
                self.__gen_QAction(
                    _('Open Inside #'),
                    self.open_selected_hashtag,
                    self.open_selected_hashtag.__doc__,
                    None
                ),
                self.__gen_QAction(
                    _('Open O&utside'),
                    self.open_selected_outside,
                    self.open_selected_outside.__doc__,
                    _('Shift+Enter')
                ),
                self.__gen_QAction(
                    _('&View'),
                    self.view_selected,
                    self.view_selected.__doc__,
                    _('F3')
                ),
                self.__gen_QAction(
                    _('&Edit'),
                    self.edit_selected,
                    self.edit_selected.__doc__,
                    _('F4')
                )
            ))
            menus['file'].addSeparator()
            ... #TODO: Implement this!
            self.menubar.addMenu(menus['file']) # FIXME: Menu doesn't open when activated!
        ... #TODO: Implement this!

        ##########################
        # Initialize the toolbar #
        ##########################
        ... #TODO: Implement this!

        ###############################
        # Initialize the file view(s) #
        ###############################
        ... #TODO: Implement this!

    def __gen_QAction(self, label:str, action:Callable, tooltip:str=None, shortcut:str=None) -> QAction:
        """Generates a button with the given properties"""
        btn:QAction = QAction(label)
        btn.setStatusTip(tooltip)
        if tooltip:
            btn.setStatusTip(tooltip)
        if shortcut:
            btn.setShortcut(shortcut)
        btn.triggered.connect(action)
        return btn

    def open_selected(self):
        """Opens the selected file"""
        ... #TODO: Implement this!

    def open_selected_inside(self):
        """Opens the selected file in 7-zip"""
        ... #TODO: Implement this!


    def open_selected_star(self):
        """Opens the selected file TODO: Find out meaning of star!"""
        ... #TODO: Implement this!
    def open_selected_hashtag(self):
        """Opens the selected file TODO: Find out meaning of hashtag!"""
        ... #TODO: Implement this!
    def open_selected_outside(self):
        """Opens the selected file in an external program"""
        ... #TODO: Implement this!

    def view_selected(self):
        """View the selected file"""
        return self.edit_selected() #TODO: Change this if needed!

    def edit_selected(self):
        """Edit the selected file"""
        ... #TODO: Implement this!

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
sys.exit(l7z_app.exec())
