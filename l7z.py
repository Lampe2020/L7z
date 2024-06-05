#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
# L7z - the 7-zip GUI for *NIX


'''

import sys, os
if __name__ != '__main__':
    print('\n\nL7z is not intended to be imported!\n\n', file=sys.stderr)
    raise ImportError('L7z is not intended to be imported!')

from PyQt6.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)

window = QWidget()
window.show()

app.exec()

...#TODO: Implement the GUI