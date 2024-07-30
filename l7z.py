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
from PyQt6.QtCore import Qt

l7z_app:QApplication = QApplication(sys.argv)

class L7z_GUI(QMainWindow):
    """The main GUI class"""
    ask_quit:bool = False
    def __init__(self):
        """Initialize the main GUI"""
        super().__init__()
        self.setWindowTitle(_('7-zip • Unofficial GUI (WIP!)'))
        try:
            self.setGeometry(*(int(d) for d in conf.get('Window', 'dimensions', '0,0,800,600').split(',')))
            if conf.getbool('Window', 'maximized', False):
                self.setWindowState(Qt.WindowState.WindowMaximized)
        except:
            conf.set('Window', 'dimensions', '0,0,800,600')
            conf.set('Window', 'maximized', 'false')
            self.setGeometry(0, 0, 800, 600)
        self.setWindowIcon(QIcon(os.path.join(INSTALL_DIR, 'icons', '7-zip.png')))
        self.menubar:QMenuBar = self.menuBar()
        self.menubar.setNativeMenuBar(conf.getbool('L7z', 'native_menubar'))

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
        # In the following there are a few `if True` blocks, they are just for structuring the code according to the
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
            menus['file'].addActions((
                self.__gen_QAction(
                    _('Rena&me'),
                    self.rename_file,
                    self.rename_file.__doc__,
                    _('F2')
                ),
                self.__gen_QAction(
                    _('&Copy to…'),
                    self.rename_file,
                    self.rename_file.__doc__,
                    _('F5')
                ),
                self.__gen_QAction(
                    _('&Move to…'),
                    self.rename_file,
                    self.rename_file.__doc__,
                    _('F6')
                ),
                self.__gen_QAction(
                    _('&Delete'),
                    self.rename_file,
                    self.rename_file.__doc__,
                    _('Del')
                )
            ))
            menus['file'].addSeparator()
            menus['file'].addActions((
                self.__gen_QAction(
                    _('&Split file…'),
                    self.split_file,
                    self.split_file.__doc__,
                    None
                ),
                self.__gen_QAction(
                    _('Com&bine files…'),
                    self.combine_files,
                    self.combine_files.__doc__,
                    None
                )
            ))
            menus['file'].addSeparator()
            menus['file'].addActions((
                self.__gen_QAction(
                    _('P&roperties'),
                    self.show_props,
                    self.show_props.__doc__,
                    _('Alt+Enter')
                ),
                self.__gen_QAction(
                    _('Comme&nt…'),
                    self.comment,
                    self.comment.__doc__,
                    _('Ctrl+Z')
                )
            ))
            menus['file'].addMenu(menus['file/CRC'])
            if True:    # 'file/CRC'
                menus['file/CRC'].addActions((
                    self.__gen_QAction(
                        _('CRC-32'),
                        self.show_crc32_checksum,
                        self.show_crc32_checksum.__doc__,
                        None
                    ),
                    self.__gen_QAction(
                        _('CRC-64'),
                        self.show_crc64_checksum,
                        self.show_crc64_checksum.__doc__,
                        None
                    ),
                    self.__gen_QAction(
                        _('XXH64'),
                        self.show_xxh64_checksum,
                        self.show_xxh64_checksum.__doc__,
                        None
                    ),
                    self.__gen_QAction(
                        _('SHA-1'),
                        self.show_sha1_checksum,
                        self.show_sha1_checksum.__doc__,
                        None
                    ),
                    self.__gen_QAction(
                        _('SHA-256'),
                        self.show_sha256_checksum,
                        self.show_sha256_checksum.__doc__,
                        None
                    ),
                    self.__gen_QAction(
                        _('BLAKE2sp'),
                        self.show_blake2sp_checksum,
                        self.show_blake2sp_checksum.__doc__,
                        None
                    ),
                    self.__gen_QAction(
                        _('*'),
                        self.show_all_checksums,
                        self.show_all_checksums.__doc__,
                        None
                    )
                ))
            menus['file'].addSeparator()
            menus['file'].addActions((
                self.__gen_QAction(
                    _('Create folder'),
                    self.new_folder,
                    self.new_folder.__doc__,
                    _('F7')
                ),
                self.__gen_QAction(
                    _('Create file'),
                    self.new_file,
                    self.new_file.__doc__,
                    _('Ctrl+N')
                )
            ))
            menus['file'].addSeparator()
            menus['file'].addActions((
                self.__gen_QAction(
                    _('&Link…'),
                    self.link,
                    self.link.__doc__,
                    None
                ),
                self.__gen_QAction(
                    _('&Alternate streams'),
                    self.show_alt_streams,
                    self.show_alt_streams.__doc__,
                    None
                )
            ))
            menus['file'].addSeparator()
            menus['file'].addActions((
                self.__gen_QAction(
                    _('E&xit'),
                    self.quit,
                    self.quit.__doc__,
                    _('Alt+F4')
                ),
            ))
            self.menubar.addMenu(menus['file'])

        if True:    # 'edit'
            menus['edit'].addActions((
                self.__gen_QAction(
                    _('Select &All'),
                    self.select_all,
                    self.select_all.__doc__,
                    _('Shift+[NumPad+]')
                ),
                self.__gen_QAction(
                    _('Deselect All'),
                    self.deselect_all,
                    self.deselect_all.__doc__,
                    _('Shift+[NumPad-]')
                ),
                self.__gen_QAction(
                    _('&Invert selection'),
                    self.select_all,
                    self.select_all.__doc__,
                    _('[NumPad*]')
                ),
                self.__gen_QAction(
                    _('Select…'),
                    self.select_all,
                    self.select_all.__doc__,
                    _('[NumPad+]')
                ),
                self.__gen_QAction(
                    _('Deselect…'),
                    self.select_all,
                    self.select_all.__doc__,
                    _('[NumPad-]')
                )
            ))
            menus['edit'].addSeparator()
            menus['edit'].addActions((
                self.__gen_QAction(
                    _('Select by Type'),
                    self.select_all,
                    self.select_all.__doc__,
                    _('Alt+[NumPad+]')
                ),
                self.__gen_QAction(
                    _('Deselect by Type'),
                    self.deselect_all,
                    self.deselect_all.__doc__,
                    _('Alt+[NumPad-]')
                )
            ))
            self.menubar.addMenu(menus['edit'])

        if True:    # 'view'
            self.menubar.addMenu(menus['view'])

        if True:    # 'favorites'
            self.menubar.addMenu(menus['favorites'])

        if True:    # 'tools'
            self.menubar.addMenu(menus['tools'])

        if True:    # 'help'
            self.menubar.addMenu(menus['help'])
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
        btn:QAction = QAction(label, self)
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

    def rename_file(self):
        """Rename the selected file"""
        ... #TODO: Implement this!

    def copy_to(self):
        """Copy the selected files to another location"""
        ... #TODO: Implement this!

    def move_to(self):
        """Move the selected files to another location"""
        self.copy_to()
        self.delete_file()
        #TODO: Make sure this is how it should be implemented!

    def delete_file(self):
        """Delete the selected files"""
        ... #TODO: Implement this!

    def split_file(self):
        """Split a file into several ones"""
        ... #TODO: Implement this!

    def combine_files(self):
        """Combine the parts of a split file back together to one"""
        ... #TODO: Implement this!

    def show_props(self):
        """Show the properties of the selected file"""
        ... #TODO: Implement this!

    def comment(self):
        """Comment on a file"""
        ... #TODO: Implement this!

    def show_crc32_checksum(self):
        """Show the selected file's CRC-32 checksum"""
        return self.show_checksum('CRC-32')

    def show_crc64_checksum(self):
        """Show the selected file's CRC-64 checksum"""
        return self.show_checksum('CRC-64')

    def show_xxh64_checksum(self):
        """Show the selected file's XXH64 checksum"""
        return self.show_checksum('XXH64')

    def show_sha1_checksum(self):
        """Show the selected file's SHA-1 checksum"""
        return self.show_checksum('SHA-1')

    def show_sha256_checksum(self):
        """Show the selected file's SHA-256 checksum"""
        return self.show_checksum('SHA-256')

    def show_blake2sp_checksum(self):
        """Show the selected file's BLAKE2sp checksum"""
        return self.show_checksum('BLAKE2sp')

    def show_all_checksums(self):
        """Show all available checksums of the selected file"""
        return self.show_checksum('*')

    def show_checksum(self, checksum_type):
        """Show the selected file's checksum of the specified type"""
        selected_checksums:dict[str, bytes] = {}
        if checksum_type in ('CRC-32', '*'):
            selected_checksums['CRC-32'] = b''      #TODO: Implement this hash!
        if checksum_type in ('CRC-64', '*'):
            selected_checksums['CRC-64'] = b''      #TODO: Implement this hash!
        if checksum_type in ('XXH64', '*'):
            selected_checksums['XXH64'] = b''       #TODO: Implement this hash!
        if checksum_type in ('SHA-1', '*'):
            selected_checksums['SHA-1'] = b''       #TODO: Implement this hash!
        if checksum_type in ('SHA-256', '*'):
            selected_checksums['SHA-256'] = b''     #TODO: Implement this hash!
        if checksum_type in ('BLAKE2sp', '*'):
            selected_checksums['BLAKE2sp'] = b''    #TODO: Implement this hash!
        ... #TODO: Implement this dialog!

    def new_folder(self):
        """Create a new folder inside the current one"""
        ... #TODO: Implement this!

    def new_file(self):
        """Create a new file inside the current directory"""
        ... #TODO: Implement this!

    def link(self):
        """Create a link"""
        ... #TODO: Implement this!

    def show_alt_streams(self):
        """Show the selected file's alternate streams"""
        ... #TODO: Implement this!

    def select_all(self):
        """Select all files in the current file view"""
        ... #TODO: Implement this!

    def deselect_all(self):
        """Deselect all files in the current file view"""
        ... #TODO: Implement this!

    def invert_selection(self):
        """Invert the selection of files in the current file view"""
        ... #TODO: Implement this!

    def select_pattern(self):
        """Select files in the current file view according to a given pattern"""
        ... #TODO: Implement this!

    def deselect_pattern(self):
        """Deselect files in the current file view according to a given pattern"""
        ... #TODO: Implement this!

    def select_type(self):
        """Select files in the current file view according to their type"""
        ... #TODO: Implement this!

    def deselect_type(self):
        """Deselect files in the current file view according to their type"""
        ... #TODO: Implement this!

    def show_about(self):
        """Show the "About" dialogue"""
        ... #TODO: Implement "About" dialog

    def quit(self):
        """Quit the app smoothly."""
        if self.ask_quit:
            ... #TODO: Implement a "Close?" dialog
        # Save the window state
        if (self.windowState() & Qt.WindowState.WindowMaximized):
            conf.set('Window', 'maximized', 'true')
        else:
            conf.set('Window', 'dimensions', f'{self.x()},{self.y()},{self.width()},{self.height()}')
            conf.set('Window', 'maximized', 'false')
        self.destroy(True, True)
        return sys.exit(0)

    def closeEvent(self, event):
        """Quit the app smoothly on external close command"""
        if self.quit():
            event.accept()
        else:
            event.ignore()

#debug
print(_('Starting L7z on {platform}…').format(platform=sys.platform))

main_window:L7z_GUI = L7z_GUI()
main_window.show()
sys.exit(l7z_app.exec())
