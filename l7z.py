#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
# L7z - the 7-zip GUI for *NIX

TODO: Write short description and usage help, to be output when help is requested from the terminal
'''

import sys, os
if __name__ != '__main__':
    print('\n\nL7z is not intended to be imported!\n\n', file=sys.stderr)
    raise ImportError('L7z is not intended to be imported!')

from PyQt6.QtWidgets import QApplication, QMainWindow

app = QApplication(sys.argv)

window = QMainWindow()
window.show()

...#TODO: Implement the GUI here

app.exec()