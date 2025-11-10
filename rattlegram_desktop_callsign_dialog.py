#!/usr/bin/env python3
#
# Rattlegram Desktop
# Copyright 2025 
# Stuart MacIntosh ZL3TUX <stuart@macintosh.nz>
#

from PyQt6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QObject, QEvent, Qt
from PyQt6.QtGui import QFont
from PySide6.QtGui import QFontDatabase
from rattlegram_desktop_config import RattlegramDesktopConfig

import sys
from IPython import embed

BASE37_CHARS = [
        48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 65, # 0-9
        66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, # A-Z
        95, # underscore _
        16777219, # BS backspace
        16777223, # DEL
        16777232, # HOME
        16777233 # END
    ]

CONTROL_CHARS = [
        16777219, # BS backspace
        16777223, # DEL
        16777232, # HOME
        16777233 # END
        ]

class InputEventFilter(QtCore.QObject):
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Type.KeyPress:
            key_event = event
            l = len(obj.text())
            key = key_event.key()

            if l >= 13 and key not in CONTROL_CHARS:
                print('discard\tlen:%s\tkey:%s' % (l, key_event.key()))
                return True

            if key in [Qt.Key.Key_Enter, Qt.Key.Key_Return, 32] or key not in BASE37_CHARS:
                print('discard:\tkey:%s' % key_event.key())
                return True  # Event handled, discard it

            if key_event.text().islower():
                print('islower:\t%s' % key_event.text())
                c = key_event.text().upper()
                callsign = obj.text() + c
                obj.setText(callsign)
                return True # Event handled, discard it

        retvar = super().eventFilter(obj, event)
        return retvar

class Ui_callsignDialog(object):
    def __init__(self):
        self.config = RattlegramDesktopConfig()

    def setupUi(self, callsignDialog):
        fixed_width_font_family = "Monospace"
        fixed_font = QFont(fixed_width_font_family, 12) # Set font family and size

        callsignDialog.setObjectName("callsignDialog")
        callsignDialog.resize(400, 52)
        self.callsignButtonBox = QtWidgets.QDialogButtonBox(parent=callsignDialog)
        self.callsignButtonBox.setGeometry(QtCore.QRect(210, 10, 171, 32))
        self.callsignButtonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.callsignButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.callsignButtonBox.setObjectName("callsignButtonBox")
        self.callsignButtonBox.accepted.connect(self.buttonbox_accepted)
        self.callsignButtonBox.rejected.connect(self.buttonbox_rejected)
        self.callsignTextEdit = QtWidgets.QLineEdit(parent=callsignDialog)
        self.callsignTextEdit.setFont(fixed_font)
        self.callsignTextEdit.setGeometry(QtCore.QRect(10, 10, 191, 31))
        self.callsignTextEdit.setObjectName("callsignTextEdit")
        self.callsignTextEdit.setText(self.config.get_value('callsign'))
        # Install the event filter
        self.enter_key_filter = InputEventFilter()
        self.callsignTextEdit.installEventFilter(self.enter_key_filter)

        self.retranslateUi(callsignDialog)
        self.callsignButtonBox.accepted.connect(callsignDialog.accept)
        self.callsignButtonBox.rejected.connect(callsignDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(callsignDialog)

    def retranslateUi(self, callsignDialog):
        _translate = QtCore.QCoreApplication.translate
        callsignDialog.setWindowTitle(_translate("callsignDialog", "Callsign"))

    def buttonbox_accepted(button):
        callsign = button.callsignTextEdit.text()
        button.config.set_value('callsign', callsign)

    def buttonbox_rejected(button):
        # print(dir(button))
        # print(button)
        return True

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    callsignDialog = QtWidgets.QDialog()
    ui = Ui_callsignDialog()
    ui.setupUi(callsignDialog)
    callsignDialog.show()
    sys.exit(app.exec())
