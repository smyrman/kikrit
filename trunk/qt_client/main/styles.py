import os

from PyQt4 import QtCore, QtGui

from settings import PROJECT_ROOT


# Colors:
COLOR_SOFT_BLUE = QtGui.QColor(0, 170, 255, 255)
COLOR_DARK_RED = QtGui.QColor(170, 0, 0, 255)
COLOR_DARK_GREY = QtGui.QColor(142, 142, 142, 255)

# Palettes:
BLUE_PALETTE = QtGui.QPalette()
BLUE_PALETTE.setColor(QtGui.QPalette.Active, QtGui.QPalette.Button, COLOR_SOFT_BLUE)
BLUE_PALETTE.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Button, COLOR_SOFT_BLUE)

RED_PALETTE = QtGui.QPalette()
RED_PALETTE.setColor(QtGui.QPalette.Active, QtGui.QPalette.Button, COLOR_DARK_RED)
RED_PALETTE.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Button, COLOR_DARK_RED)
RED_PALETTE.setColor(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, QtCore.Qt.white)
RED_PALETTE.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, QtCore.Qt.white)

GREY_PALETTE = QtGui.QPalette()
GREY_PALETTE.setColor(QtGui.QPalette.Active, QtGui.QPalette.Button, COLOR_DARK_GREY)
GREY_PALETTE.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Button, COLOR_DARK_GREY)

# Icons:
ERROR_ICON = os.path.join(PROJECT_ROOT, "qt_client", "icons", "dialog-error.png")
CANCEL_ICON = os.path.join(PROJECT_ROOT, "qt_client", "icons", "dialog-cancel.png")
INFO_ICON = os.path.join(PROJECT_ROOT, "qt_client", "icons", "dialog-information.png")
OK_ICON = os.path.join(PROJECT_ROOT, "qt_client", "icons", "dialog-ok-apply.png")
OPEN_WALLET_ICON = os.path.join(PROJECT_ROOT, "qt_client", "icons", "wallet-open.png")
CLOSED_WALLET_ICON = os.path.join(PROJECT_ROOT, "qt_client", "icons", "wallet-closed.png")

# Styles:
# XXX: Due to the complexety of QStyle objects, tuples ar here used to describe
# the diffrent styles.
STYLE_NONE = (QtGui.QPalette(), "")
STYLE_ERROR = (RED_PALETTE, ERROR_ICON)
STYLE_CANCEL = (GREY_PALETTE, CANCEL_ICON)
STYLE_INFO = (GREY_PALETTE, INFO_ICON)
STYLE_SUCCESS1 = (BLUE_PALETTE, OK_ICON)
STYLE_SUCCESS2 = (BLUE_PALETTE, OPEN_WALLET_ICON)
STYLE_SUCCESS3 = (BLUE_PALETTE, CLOSED_WALLET_ICON)
