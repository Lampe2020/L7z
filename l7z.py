#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
# L7z - the 7-zip GUI for *NIX

TODO: Write short description and usage help, to be output when help is requested from the terminal
'''

import sys, os, conf, datetime
from typing import Callable, Literal

INSTALL_DIR:str = os.path.dirname(__file__)

from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QDialog, QToolBar
from PyQt6.QtGui import QIcon, QAction, QActionGroup
from PyQt6.QtCore import Qt, QTranslator

# Initialize the translation right-away so even the no-import message can be localized.
translator:QTranslator = QTranslator()
try:
    translator.load(os.path.join(INSTALL_DIR, 'locales', f'{conf.get("L7z", "lang")}.qm'))
except:
    print(f'Error loading translation file locales/{conf.get("L7z", "lang", "no_LN")}.qm')

if __name__ != '__main__':
    msg:str = self.tr("L7z is not intended to be imported!")
    print(f'\n\n{msg}\n\n', file=sys.stderr)
    raise ImportError(msg)

l7z_app:QApplication = QApplication(sys.argv)
l7z_app.installTranslator(translator)

class L7z_GUI(QMainWindow):
    """The main GUI class"""
    ask_quit:bool = False

    __hashes:tuple[str, ...] = 'CRC-32|CRC-64|XXH64|SHA-1|SHA-256|BLAKE2sp|*'.split('|')
    __view_sizes:tuple[str, ...] = 'large|small|list|detail'.split('|')
    __sort_by:tuple[str, ...] = 'name|type|date|size|none'.split('|')
    __timeformats:tuple[str, ...] = (
        '%Y-%m-%d',
        '%Y-%m-%d %H:%M',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M:%S.%f',
        #'%Y-%m-%d %H:%M:%S.%f'  # There's no Python strftime directive for more precision than %f
    )

    def __init__(self):
        """Initialize the main GUI"""
        super().__init__()
        self.setWindowTitle(self.tr('7-zip • Unofficial GUI (WIP!)'))
        try:
            self.setGeometry(*(int(d) for d in conf.get('Window', 'dimensions', '0,0,800,600').split(',')))
            if conf.getbool('Window', 'maximized', False):
                self.setWindowState(Qt.WindowState.WindowMaximized)
        except:
            print(self.tr('Could not set window geometry!'))
        self.setWindowIcon(QIcon(os.path.join(INSTALL_DIR, 'icons', '7z.png')))
        self.menubar:QMenuBar = self.menuBar()
        self.menubar.setNativeMenuBar(conf.getbool('L7z', 'native_menubar'))

        ###########################
        # Initialize the menu bar #
        ###########################
        menus:dict[str, QMenu] = {
            'file': QMenu(self.tr('&File'), self),
            'edit': QMenu(self.tr('&Edit'), self),
            'view': QMenu(self.tr('&View'), self),
            'favorites': QMenu(self.tr('F&avorites'), self),
            'tools': QMenu(self.tr('&Tools'), self),
            'help': QMenu(self.tr('&Help'), self)
        }
        menus.update({**menus,
            'file/7-zip': QMenu('7-Zip', menus['file']),
            'file/crc': QMenu(self.tr('CRC'), menus['file']),
                                   # ↓ is updated whenever the menu is opened, so doesn't need to be translated
            'view/timeformat': QMenu(datetime.datetime.now().strftime('%Y-%m-%d'), menus['view']),
            'view/toolbars': QMenu(self.tr('Toolbars'), menus['view']),
            'favorites/add': QMenu(self.tr('&Add folder to favorites as'), menus['favorites'])
        })
        menus.update({**menus,
            'file/7-zip/crc': QMenu(self.tr('CRC SHA'), menus['file/7-zip'])
        })
        # In the following there are a few `if True` blocks, they are just for structuring the code according to the
        # menu it's currently working on.
        if True:    # 'file'
            if True:    # 'file/7-zip'
                #TODO: Update this whenever the selection is changed. When a single file is selected, set filename to
                # the selected file's name, if multiple are selected set it to the parent dir's name.
                menus['file/7-zip'].addActions((
                    self.__gen_QAction(
                        self.tr('Add to archive...'),
                        self.add_to_archive,
                        self.add_to_archive.__doc__,
                        None
                    ),
                    self.__gen_QAction(
                        self.tr('Compress and email...'),
                        self.add_to_archive,
                        self.add_to_archive.__doc__,
                        None
                    ),
                    self.__gen_QAction(
                        self.tr('Add to "{filename}.7z"'),
                        self.add_to_archive,
                        self.add_to_archive.__doc__,
                        None
                    ),
                    self.__gen_QAction(
                        self.tr('Compress to "{filename}".7z and email'),
                        self.add_to_archive,
                        self.add_to_archive.__doc__,
                        None
                    ),
                    self.__gen_QAction(
                        self.tr('Add to "{filename}.zip"'),
                        self.add_to_archive,
                        self.add_to_archive.__doc__,
                        None
                    ),
                    self.__gen_QAction(
                        self.tr('Compress to "{filename}.zip" and email'),
                        self.add_to_archive,
                        self.add_to_archive.__doc__,
                        None
                    )
                ))
                if True:    # 'file/7-zip/crc
                    menus['file/7-zip/crc'].addActions((
                        self.__gen_QAction(
                            self.tr('CRC-32'),
                            (lambda: self.show_checksum('CRC-32')),
                            self.show_checksum.__doc__,
                            None
                        ),
                        self.__gen_QAction(
                            self.tr('CRC-64'),
                            (lambda: self.show_checksum('CRC-64')),
                            self.show_checksum.__doc__,
                            None
                        ),
                        self.__gen_QAction(
                            self.tr('XXH64'),
                            (lambda: self.show_checksum('XXH64')),
                            self.show_checksum.__doc__,
                            None
                        ),
                        self.__gen_QAction(
                            self.tr('SHA-1'),
                            (lambda: self.show_checksum('SHA-1')),
                            self.show_checksum.__doc__,
                            None
                        ),
                        self.__gen_QAction(
                            self.tr('SHA-256'),
                            (lambda: self.show_checksum('SHA-256')),
                            self.show_checksum.__doc__,
                            None
                        ),
                        self.__gen_QAction(
                            self.tr('BLAKE2sp'),
                            (lambda: self.show_checksum('BLAKE2sp')),
                            self.show_checksum.__doc__,
                            None
                        ),
                        self.__gen_QAction(
                            self.tr('*'),
                            (lambda: self.show_checksum('*')),
                            self.show_checksum.__doc__,
                            None
                        )
                    ))
                    menus['file/7-zip/crc'].addSeparator()
                    menus['file/7-zip/crc'].addActions((
                        self.__gen_QAction(
                            self.tr('SHA-256 -> {filename}.sha256'),
                            self.save_sha256,
                            self.save_sha256.__doc__,
                            None
                        ),
                        self.__gen_QAction(
                            self.tr('Test Archive : Checksum'),
                            self.save_sha256,
                            self.save_sha256.__doc__,
                            None
                        )
                    ))
                    menus['file/7-zip'].addMenu(menus['file/7-zip/crc'])
                menus['file'].addMenu(menus['file/7-zip'])
            menus['file'].addActions((
                self.__gen_QAction(
                    self.tr('&Open'),
                    self.open_selected,
                    self.open_selected.__doc__,
                    'Enter'
                ),
                self.__gen_QAction(
                    self.tr('Open &Inside'),
                    self.open_selected_inside,
                    self.open_selected_inside.__doc__,
                    'Ctrl+PgDn'
                ),
                self.__gen_QAction(
                    self.tr('Open Inside *'),
                    self.open_selected_star,
                    self.open_selected_star.__doc__
                ),
                self.__gen_QAction(
                    self.tr('Open Inside #'),
                    self.open_selected_hashtag,
                    self.open_selected_hashtag.__doc__
                ),
                self.__gen_QAction(
                    self.tr('Open O&utside'),
                    self.open_selected_outside,
                    self.open_selected_outside.__doc__,
                    'Shift+Enter'
                ),
                self.__gen_QAction(
                    self.tr('&View'),
                    self.view_selected,
                    self.view_selected.__doc__,
                    'F3'
                ),
                self.__gen_QAction(
                    self.tr('&Edit'),
                    self.edit_selected,
                    self.edit_selected.__doc__,
                    'F4'
                )
            ))
            menus['file'].addSeparator()
            menus['file'].addActions((
                self.__gen_QAction(
                    self.tr('Rena&me'),
                    self.rename_file,
                    self.rename_file.__doc__,
                    'F2'
                ),
                self.__gen_QAction(
                    self.tr('&Copy to...'),
                    self.rename_file,
                    self.rename_file.__doc__,
                    'F5'
                ),
                self.__gen_QAction(
                    self.tr('&Move to...'),
                    self.rename_file,
                    self.rename_file.__doc__,
                    'F6'
                ),
                self.__gen_QAction(
                    self.tr('&Delete'),
                    self.rename_file,
                    self.rename_file.__doc__,
                    'Del'
                )
            ))
            menus['file'].addSeparator()
            menus['file'].addActions((
                self.__gen_QAction(
                    self.tr('&Split file...'),
                    self.split_file,
                    self.split_file.__doc__
                ),
                self.__gen_QAction(
                    self.tr('Com&bine files...'),
                    self.combine_files,
                    self.combine_files.__doc__
                )
            ))
            menus['file'].addSeparator()
            menus['file'].addActions((
                self.__gen_QAction(
                    self.tr('P&roperties'),
                    self.show_props,
                    self.show_props.__doc__,
                    'Alt+Enter'
                ),
                self.__gen_QAction(
                    self.tr('Comme&nt...'),
                    self.comment,
                    self.comment.__doc__,
                    'Ctrl+Z'
                )
            ))
            menus['file'].addMenu(menus['file/crc'])
            if True:    # 'file/crc'
                menus['file/crc'].addActions((
                    self.__gen_QAction(
                        self.tr('CRC-32'),
                        (lambda: self.show_checksum('CRC-32')),
                        self.show_checksum.__doc__,
                        None
                    ),
                    self.__gen_QAction(
                        self.tr('CRC-64'),
                        (lambda: self.show_checksum('CRC-64')),
                        self.show_checksum.__doc__,
                        None
                    ),
                    self.__gen_QAction(
                        self.tr('XXH64'),
                        (lambda: self.show_checksum('XXH64')),
                        self.show_checksum.__doc__,
                        None
                    ),
                    self.__gen_QAction(
                        self.tr('SHA-1'),
                        (lambda: self.show_checksum('SHA-1')),
                        self.show_checksum.__doc__,
                        None
                    ),
                    self.__gen_QAction(
                        self.tr('SHA-256'),
                        (lambda: self.show_checksum('SHA-256')),
                        self.show_checksum.__doc__,
                        None
                    ),
                    self.__gen_QAction(
                        self.tr('BLAKE2sp'),
                        (lambda: self.show_checksum('BLAKE2sp')),
                        self.show_checksum.__doc__,
                        None
                    ),
                    self.__gen_QAction(
                        self.tr('*'),
                        (lambda: self.show_checksum('*')),
                        self.show_checksum.__doc__,
                        None
                    )
                ))
            menus['file'].addSeparator()
            menus['file'].addActions((
                self.__gen_QAction(
                    self.tr('Create folder'),
                    self.new_folder,
                    self.new_folder.__doc__,
                    'F7'
                ),
                self.__gen_QAction(
                    self.tr('Create file'),
                    self.new_file,
                    self.new_file.__doc__,
                    'Ctrl+N'
                )
            ))
            menus['file'].addSeparator()
            menus['file'].addActions((
                self.__gen_QAction(
                    self.tr('&Link...'),
                    self.link,
                    self.link.__doc__
                ),
                self.__gen_QAction(
                    self.tr('&Alternate streams'),
                    self.show_alt_streams,
                    self.show_alt_streams.__doc__
                )
            ))
            menus['file'].addSeparator()
            menus['file'].addActions((
                self.__gen_QAction(
                    self.tr('E&xit'),
                    self.quit,
                    self.quit.__doc__,
                    'Alt+F4'
                ),
            ))
            self.menubar.addMenu(menus['file'])

        if True:    # 'edit'
            menus['edit'].addActions((
                self.__gen_QAction(
                    self.tr('Select &All'),
                    self.select_all,
                    self.select_all.__doc__,
                    'Shift++'   # 'Shift+[NumPad+]'
                ),
                self.__gen_QAction(
                    self.tr('Deselect All'),
                    self.deselect_all,
                    self.deselect_all.__doc__,
                    'Shift+-'   # 'Shift+[NumPad-]'
                ),
                self.__gen_QAction(
                    self.tr('&Invert selection'),
                    self.select_all,
                    self.select_all.__doc__,
                    '*'         # '[NumPad*]'
                ),
                self.__gen_QAction(
                    self.tr('Select...'),
                    self.select_all,
                    self.select_all.__doc__,
                    '+'         # '[NumPad+]'
                ),
                self.__gen_QAction(
                    self.tr('Deselect...'),
                    self.select_all,
                    self.select_all.__doc__,
                    '-'         # '[NumPad-]'
                )
            ))
            menus['edit'].addSeparator()
            menus['edit'].addActions((
                self.__gen_QAction(
                    self.tr('Select by Type'),
                    self.select_all,
                    self.select_all.__doc__,
                    'Alt++'     # 'Alt+[NumPad+]'
                ),
                self.__gen_QAction(
                    self.tr('Deselect by Type'),
                    self.deselect_all,
                    self.deselect_all.__doc__,
                    'Alt+-'     # 'Alt+[NumPad-]'
                )
            ))
            self.menubar.addMenu(menus['edit'])

        if True:    # 'view'
            ... #TODO: Implement this menu!
            view_size:QActionGroup = QActionGroup(self)
            view_size.setExclusive(True)
            for action in (
                self.__gen_QAction(
                    self.tr('Lar&ge icons'),
                    (lambda: self.view_size('large')),
                    self.view_size.__doc__,
                    'Ctrl+1',
                    True
                ),
                self.__gen_QAction(
                    self.tr('S&mall icons'),
                    (lambda: self.view_size('small')),
                    self.view_size.__doc__,
                    'Ctrl+2',
                    True
                ),
                self.__gen_QAction(
                    self.tr('&List'),
                    (lambda: self.view_size('list')),
                    self.view_size.__doc__,
                    'Ctrl+3',
                    True
                ),
                self.__gen_QAction(
                    self.tr('&Details'),
                    (lambda: self.view_size('detail')),
                    self.view_size.__doc__,
                    'Ctrl+4',
                    True
                )
            ):
                view_size.addAction(action)
            view_size.actions()[self.__view_sizes.index(self.get_view_size())].setChecked(True)
            menus['view'].addActions(view_size.actions())
            menus['view'].addSeparator()
            sort_by:QActionGroup = QActionGroup(self)
            sort_by.setExclusive(True)
            for action in (
                self.__gen_QAction(
                    self.tr('Name'),
                    (lambda: self.sort_by('name')),
                    self.sort_by.__doc__,
                    'Ctrl+F3',
                    True
                ),
                self.__gen_QAction(
                    self.tr('Type'),
                    (lambda: self.sort_by('type')),
                    self.sort_by.__doc__,
                    'Ctrl+F4',
                    True
                ),
                self.__gen_QAction(
                    self.tr('Date'),
                    (lambda: self.sort_by('date')),
                    self.sort_by.__doc__,
                    'Ctrl+F5',
                    True
                ),
                self.__gen_QAction(
                    self.tr('Size'),
                    (lambda: self.sort_by('size')),
                    self.sort_by.__doc__,
                    'Ctrl+F6',
                    True
                ),
                self.__gen_QAction(
                    self.tr('Unsorted'),
                    (lambda: self.sort_by('none')),
                    self.sort_by.__doc__,
                    'Ctrl+F7',
                    True
                )
            ):
                sort_by.addAction(action)
            sort_by.actions()[self.__sort_by.index(self.get_sort_by())].setChecked(True)
            menus['view'].addActions(sort_by.actions())
            menus['view'].addSeparator()
            menus['view'].addActions((
                self.__gen_QAction(
                    self.tr('Flat view'),
                    self.flat_view,
                    self.flat_view.__doc__,
                    None,
                    True
                ),
                self.__gen_QAction(
                    self.tr('&2 Panels'),
                    self.two_panels,
                    self.two_panels.__doc__,
                    'F9',
                    True
                )
            ))
            menus['view'].actions()[-2].setChecked(self.get_flat_view())
            menus['view'].actions()[-1].setChecked(self.get_two_panels())
            if True:    # 'view/timeformat'
                timeformat_list:QActionGroup = QActionGroup(self)
                timeformat_list.setExclusive(True)
                for timeformat in self.__timeformats:
                    timeformat_list.addAction(self.__gen_QAction(
                        (f'{datetime.datetime.now().strftime(timeformat)}'
                         f'{"Z" if conf.getbool("L7z", "use_utc_time") else ""}'),
                        (lambda *args, tf=timeformat: self.set_timeformat(tf)),
                        self.set_timeformat.__doc__,
                        None,
                        True
                    ))
                try:
                    (timeformat_list.actions()[self.__timeformats.index(conf.get('L7z', 'timestamp_format'))]
                     .setChecked(True))
                except ValueError:
                    print(self.tr('Custom timestamp format detected: {timestamp_format}')
                          .format(timestamp_format=conf.get('L7z', 'timestamp_format')))
                menus['view/timeformat'].addActions(timeformat_list.actions())
                menus['view/timeformat'].addAction(self.__gen_QAction(
                    self.tr('UTC'),
                    self.toggle_utc,
                    self.toggle_utc.__doc__,
                    None,
                    True
                ))
                menus['view/timeformat'].actions()[-1].setChecked(conf.getbool('L7z', 'use_utc_time'))
                menus['view'].addMenu(menus['view/timeformat'])
            if True:    # 'view/toolbars'
                visible_toolbars:QActionGroup =QActionGroup(self)
                visible_toolbars.setExclusive(False)
                for action in (
                    self.__gen_QAction(
                        self.tr('Archive Toolbar'),
                        self.toggle_archive_toolbar,
                        self.toggle_archive_toolbar.__doc__,
                        None,
                        True
                    ),
                    self.__gen_QAction(
                        self.tr('Standard Toolbar'),
                        self.toggle_standard_toolbar,
                        self.toggle_standard_toolbar.__doc__,
                        None,
                        True
                    )
                ):
                    visible_toolbars.addAction(action)
                visible_toolbars.actions()[0].setChecked(conf.getbool('Toolbars', 'archive'))
                visible_toolbars.actions()[1].setChecked(conf.getbool('Toolbars', 'standard'))
                menus['view/toolbars'].addActions(visible_toolbars.actions())
                menus['view/toolbars'].addSeparator()
                toolbarbutton_settings:QActionGroup = QActionGroup(self)
                toolbarbutton_settings.setExclusive(False)
                for action in (
                    self.__gen_QAction(
                        self.tr('Large Buttons'),
                        self.toggle_large_toolbar_buttons,
                        self.toggle_large_toolbar_buttons.__doc__,
                        None,
                        True
                    ),
                    self.__gen_QAction(
                        self.tr('Show Buttons Text'),
                        self.toggle_toolbar_button_text,
                        self.toggle_toolbar_button_text.__doc__,
                        None,
                        True
                    )
                ):
                    toolbarbutton_settings.addAction(action)
                toolbarbutton_settings.actions()[0].setChecked(conf.getbool('Toolbars', 'large_buttons'))
                toolbarbutton_settings.actions()[1].setChecked(conf.getbool('Toolbars', 'button_text'))
                menus['view/toolbars'].addActions(toolbarbutton_settings.actions())
                menus['view'].addMenu(menus['view/toolbars'])
            menus['view'].addActions((
                self.__gen_QAction(
                    self.tr('Open Root Folder'),
                    self.navigate_to_root,
                    self.navigate_to_root.__doc__,
                    '\\'
                ),
                self.__gen_QAction(
                    self.tr('Up One Level'),
                    self.navigate_up,
                    self.navigate_up.__doc__,
                    'Backspace'
                ),
                self.__gen_QAction(
                    self.tr('Folders History...'),
                    self.show_history,
                    self.show_history.__doc__,
                    'Alt+F12'
                ),
                self.__gen_QAction(
                    self.tr('Refresh'),
                    self.refresh_fileview,
                    self.refresh_fileview.__doc__,
                    'Ctrl+R'
                ),
                self.__gen_QAction(
                    self.tr('Auto Refresh'),
                    self.toggle_auto_refresh,
                    self.toggle_auto_refresh.__doc__,
                    None,
                    True
                ),
            ))
            menus['view'].actions()[-1].setChecked(conf.getbool('Fileview', 'auto-refresh'))
            self.menubar.addMenu(menus['view'])

        if True:    # 'favorites'
            if True:    # 'favorites/add'
                menus['favorites/add'].addActions(
                    self.__gen_QAction(
                        self.tr('Bookmark {i}').format(i=i),
                        (lambda *args, i=i: self.set_bookmark(i)),
                        self.set_bookmark.__doc__,
                        f'Alt+Shift+{i}'
                    ) for i in range(10)
                )
                menus['favorites'].addMenu(menus['favorites/add'])
            menus['favorites'].addActions(
                self.__gen_QAction(
                    (conf.get('Locations', f'bookmark_{i}', '-') or '-'),
                    (lambda *args, i=i: self.navigate_to_bookmark(i)),
                    self.navigate_to_bookmark.__doc__,
                    f'Alt+{i}'
                ) for i in range(10)
            )
            self.menubar.addMenu(menus['favorites'])

        if True:    # 'tools'
            menus['tools'].addAction((
                self.__gen_QAction(
                    self.tr('&Options...'),
                    self.show_settings_dialog,
                    self.show_settings_dialog.__doc__
                )
            ))
            menus['tools'].addSeparator()
            menus['tools'].addAction((
                self.__gen_QAction(
                    self.tr('&Benchmark'),
                    self.benchmark,
                    self.benchmark.__doc__
                )
            ))
            menus['tools'].addAction((
                self.__gen_QAction(
                    self.tr('Delete Temporary Files...'),
                    self.del_temp_files,
                    self.del_temp_files.__doc__
                )
            ))
            menus['tools'].addSeparator()
            menus['tools'].addSeparator()
            self.menubar.addMenu(menus['tools'])

        if True:    # 'help'
            menus['help'].addAction(
                self.__gen_QAction(
                    self.tr('&Contents...'),
                    self.show_help_dialog,
                    self.show_help_dialog.__doc__,
                    'F1'
                )
            )
            menus['help'].addSeparator()
            menus['help'].addAction(
                self.__gen_QAction(
                    self.tr('&About L7z...'),
                    self.show_about_dialog,
                    self.show_about_dialog.__doc__
                )
            )
            self.menubar.addMenu(menus['help'])

        #############################
        # Initialize the toolbar(s) #
        #############################
        toolbar:QToolBar = QToolBar('toolbar', self)
        toolbar.setMovable(False)
        toolbar.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        toolbar.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonTextUnderIcon if conf.getbool('Toolbars', 'button_text')
            else Qt.ToolButtonStyle.ToolButtonIconOnly)
        archive_toolbar:dict[str, QAction] = {
            'add': self.__gen_QAction(
                self.tr('Add'),
                self.add_to_archive,
                self.add_to_archive.__doc__
            ),
            'extract': self.__gen_QAction(
                self.tr('Extract'),
                self.extract_archive,
                self.extract_archive.__doc__
            ),
            'test': self.__gen_QAction(
                self.tr('Test'),
                self.test_archive,
                self.test_archive.__doc__
            )
        }
        for action in archive_toolbar:
            archive_toolbar[action].setIcon(QIcon(os.path.join(
                INSTALL_DIR, 'icons', 'toolbar', ('big' if conf.getbool('Toolbars', 'large_buttons') else ''),
                #FIXME: This setting is somehow inverted?!?
                f'{action}.png'
            )))
        standard_toolbar:dict[str, QAction] = {
            'copy': self.__gen_QAction(
                self.tr('Copy'),
                self.copy_to,
                self.copy_to.__doc__
            ),
            'move': self.__gen_QAction(
                self.tr('Move'),
                self.move_to,
                self.move_to.__doc__
            ),
            'delete': self.__gen_QAction(
                self.tr('Delete'),
                self.delete_file,
                self.delete_file.__doc__
            ),
            'info': self.__gen_QAction(
                self.tr('Info'),
                self.show_props,
                self.show_props.__doc__
            )
        }
        for action in standard_toolbar:
            standard_toolbar[action].setIcon(QIcon(os.path.join(
                INSTALL_DIR, 'icons', 'toolbar', ('big' if conf.getbool('Toolbars', 'large_buttons') else ''),
                #FIXME: This setting is somehow inverted?!?
                f'{action}.png'
            )))
        if conf.getbool('Toolbars', 'archive'):
            toolbar.addActions(archive_toolbar.values())
        if conf.getbool('Toolbars', 'standard'):
            toolbar.addActions(standard_toolbar.values())
        self.addToolBar(toolbar)

        ###############################
        # Initialize the file view(s) #
        ###############################
        ... #TODO: Implement this!

    def __gen_QAction(
            self,
            label:str,
            action:Callable,
            tooltip:str=None,
            shortcut:str=None,
            checkable:bool=False
    ) -> QAction:
        """Generates a button with the given properties"""
        btn:QAction = QAction(label, self)
        if tooltip:
            btn.setStatusTip(tooltip)
        if shortcut:
            btn.setShortcut(shortcut)
        if checkable:
            btn.setCheckable(True)
        btn.triggered.connect(action)
        return btn

    def add_to_archive(self):
        """Add the selected file(s) to a new archive"""
        ... #TODO: Implement this!

    def save_sha256(self):
        """Add the selected file(s) to a new archive"""
        ... #TODO: Implement this!

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

    def extract_archive(self):
        """Extract the selected archive"""
        ... #TODO: Implement this!

    def test_archive(self):
        """Test the selected archive for errors"""
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

    def show_checksum(self, checksum_type:Literal[__hashes]):
        """Show the selected file's checksum of the specified type"""
        if checksum_type not in self.__hashes:
            return  #TODO: Open up an error dialog saying that an invalid hash type has been requested!
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

    def view_size(self, size:Literal[__view_sizes]):
        """Change the size of the file entries in the file view"""
        if size not in self.__view_sizes:
            return  #TODO: Open up an error dialog saying that an invalid view size has been requested!
        ... #TODO: Implement this!
    def get_view_size(self) -> str:
        """Get the current view size"""
        ... #TODO: Implement this!
        return 'detail'

    def sort_by(self, param:Literal[__sort_by]):
        """Change the property of the file entries in the file view that they are sorted by"""
        if param not in self.__sort_by:
            return  #TODO: Open up an error dialog saying that an invalid sorting property has been requested!
        ... #TODO: Implement this!
        conf.set('Fileview', 'sort_by', param)
    def get_sort_by(self) -> str:
        """Get the current sort_by property"""
        ... #TODO: Implement this!
        return 'name'

    def flat_view(self):
        """Toggle flat view"""
        ... #TODO: Hook this into the GUI
        conf.set('Fileview', 'flat', ('no' if conf.getbool('Fileview', 'flat') else 'yes'))
    def get_flat_view(self) -> bool:
        """Check if flat view is enabled"""
        return conf.getbool('Fileview', 'flat')

    def two_panels(self):
        """Toggle second panel"""
        ... #TODO: Hook this into the GUI
        conf.set('Fileview', 'second_panel', ('off' if conf.getbool('Fileview', 'second_panel') else 'on'))
    def get_two_panels(self) -> bool:
        """Check if second panel is enabled"""
        return conf.getbool('Fileview', 'second_panel')

    def set_timeformat(self, format):
        """Set the format to be used in timestamps"""
        ... #TODO: Hook this into the GUI
        conf.set('L7z', 'timestamp_format', format)
    def get_timeformat(self) -> str:
        """Get the currently-used timestamp format"""
        return f'{conf.get("L7z", "timestamp_format")}{"Z" if conf.getbool("L7z", "use_utc_time") else ""}'

    def toggle_utc(self):
        """Toggle timestamp format between local timezone and UTC"""
        ... #TODO: Hook this into the GUI
        conf.set('L7z', 'use_utc_time', ('no' if conf.getbool('L7z', 'use_utc_time') else 'yes'))

    def toggle_archive_toolbar(self):
        """Toggle the archive toolbar on or off"""
        ... #TODO: Hook this into the GUI
        conf.set('Toolbars', 'archive', ('off' if conf.getbool('Toolbars', 'archive') else 'on'))

    def toggle_standard_toolbar(self):
        """Toggle the standard toolbar on or off"""
        ... #TODO: Hook this into the GUI
        conf.set('Toolbars', 'standard', ('off' if conf.getbool('Toolbars', 'standard') else 'on'))

    def toggle_large_toolbar_buttons(self):
        """Toggle the toolbar button size between small and large"""
        ... #TODO: Hook this into the GUI
        conf.set('Toolbars', 'large_buttons', ('no' if conf.getbool('Toolbars', 'large_buttons') else 'yes'))

    def toggle_toolbar_button_text(self):
        """Toggle the toolbar button text on or off"""
        ... #TODO: Hook this into the GUI
        conf.set('Toolbars', 'button_text', ('off' if conf.getbool('Toolbars', 'button_text') else 'on'))

    def navigate_to_root(self):
        """Navigate the currently-focused panel to the system root"""
        ... #TODO: Implement this!

    def navigate_up(self):
        """Navigate the currently-focused panel one level up"""
        ... #TODO: Implement this!

    def show_history(self):
        """Show the history of visited folders"""
        ... #TODO: Implement this!

    def refresh_fileview(self):
        """Refresh the currently-focused panel"""
        ... #TODO: Implement this!

    def toggle_auto_refresh(self):
        """Toggle auto-refresh"""
        ... #TODO: Hook this into the GUI
        conf.set('Fileview', 'auto-refresh', ('no' if conf.getbool('Fileview', 'auto-refresh') else 'yes'))

    def set_bookmark(self, i):
        """Places your current location into the i'th bookmark"""
        ... #TODO: Implement this!

    def navigate_to_bookmark(self, i):
        """Navigates to your i'th bookmark"""
        ... #TODO: Implement this!

    def show_settings_dialog(self):
        """Show the "Options" dialog"""
        ... #TODO: Implement "Options" dialog

    def benchmark(self):
        """Benchmark compression performance"""
        ... #TODO: Implement this!

    def del_temp_files(self):
        """Delete L7z's and 7-Zip's temporary files"""
        ... #TODO: Implement this!

    def show_help_dialog(self):
        """Show the "Help" dialog"""
        ... #TODO: Implement "Help" dialog

    def show_about_dialog(self):
        """Show the "About" dialog"""
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

main_window:L7z_GUI = L7z_GUI()
main_window.show()
sys.exit(l7z_app.exec())
