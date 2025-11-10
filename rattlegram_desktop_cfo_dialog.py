#!/usr/bin/env python3
#
# Rattlegram Desktop
# Copyright 2025 
# Stuart MacIntosh ZL3TUX <stuart@macintosh.nz>
#

from PyQt6 import QtCore, QtGui, QtWidgets
from rattlegram_desktop_config import RattlegramDesktopConfig

class Ui_CFODialog(object):
    def __init__(self):
        self.config = RattlegramDesktopConfig()

    def setupUi(self, CFODialog):
        CFODialog.setObjectName("CFODialog")
        CFODialog.resize(301, 50)
        self.CFObuttonBox = QtWidgets.QDialogButtonBox(parent=CFODialog)
        self.CFObuttonBox.setGeometry(QtCore.QRect(120, 10, 171, 32))
        self.CFObuttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.CFObuttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.CFObuttonBox.setObjectName("CFObuttonBox")
        self.CFObuttonBox.accepted.connect(self.buttonbox_accepted)
        self.CFObuttonBox.rejected.connect(self.buttonbox_rejected)
        self.CFOspinBox = QtWidgets.QSpinBox(parent=CFODialog)
        self.CFOspinBox.setGeometry(QtCore.QRect(10, 10, 61, 31))
        self.CFOspinBox.setMinimum(800)
        self.CFOspinBox.setMaximum(2600)
        # self.CFOspinBox.setProperty("value", 1300) # not.setValue?
        self.CFOspinBox.setProperty("value", self.config.get_value('CFO'))
        self.CFOspinBox.setObjectName("CFOspinBox")
        self.label = QtWidgets.QLabel(parent=CFODialog)
        self.label.setGeometry(QtCore.QRect(80, 10, 21, 31))
        self.label.setObjectName("label")
        self.retranslateUi(CFODialog)
        self.CFObuttonBox.accepted.connect(CFODialog.accept) # type: ignore
        self.CFObuttonBox.rejected.connect(CFODialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(CFODialog)

    def retranslateUi(self, CFODialog):
        _translate = QtCore.QCoreApplication.translate
        CFODialog.setWindowTitle(_translate("CFODialog", "Carrier Frequency (SSB Offset)"))
        self.label.setText(_translate("CFODialog", "Hz"))

    def buttonbox_accepted(button):
        # print(dir(button.CFOspinBox))
        cfo = int(button.CFOspinBox.cleanText())
        button.config.set_value('CFO', cfo)

    def buttonbox_rejected(button):
        # print(dir(button))
        # print(button)
        return True

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CFODialog = QtWidgets.QDialog()
    ui = Ui_CFODialog()
    ui.setupUi(CFODialog)
    CFODialog.show()
    sys.exit(app.exec())
