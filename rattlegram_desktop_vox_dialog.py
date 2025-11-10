#!/usr/bin/env python3
#
# Rattlegram Desktop
# Copyright 2025 
# Stuart MacIntosh ZL3TUX <stuart@macintosh.nz>
#


from PyQt6 import QtCore, QtGui, QtWidgets
from rattlegram_desktop_config import RattlegramDesktopConfig

class Ui_VOXDialog(object):
    def setupUi(self, VOXDialog):
        VOXDialog.setObjectName("VOXDialog")
        VOXDialog.resize(320, 240)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=VOXDialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 200, 301, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.accepted.connect(self.buttonbox_accepted)
        self.buttonBox.rejected.connect(self.buttonbox_rejected)
        self.pilotTonecheckBox = QtWidgets.QCheckBox(parent=VOXDialog)
        self.pilotTonecheckBox.setGeometry(QtCore.QRect(10, 10, 101, 31))
        self.pilotTonecheckBox.setObjectName("pilotTonecheckBox")
        self.NoiseSymbolsSpinBox = QtWidgets.QSpinBox(parent=VOXDialog)
        self.NoiseSymbolsSpinBox.setGeometry(QtCore.QRect(10, 50, 61, 31))
        self.NoiseSymbolsSpinBox.setObjectName("NoiseSymbolsSpinBox")
        self.label = QtWidgets.QLabel(parent=VOXDialog)
        self.label.setGeometry(QtCore.QRect(90, 50, 101, 31))
        self.label.setObjectName("label")
        self.FinishBeepcheckBox = QtWidgets.QCheckBox(parent=VOXDialog)
        self.FinishBeepcheckBox.setGeometry(QtCore.QRect(110, 10, 101, 31))
        self.FinishBeepcheckBox.setObjectName("FinishBeepcheckBox")

        self.retranslateUi(VOXDialog)
        self.buttonBox.accepted.connect(VOXDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(VOXDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(VOXDialog)

    def retranslateUi(self, VOXDialog):
        _translate = QtCore.QCoreApplication.translate
        VOXDialog.setWindowTitle(_translate("VOXDialog", "VOX Settings"))
        self.pilotTonecheckBox.setText(_translate("VOXDialog", "Pilot Tone"))
        self.label.setText(_translate("VOXDialog", "Noise Symbols"))
        self.FinishBeepcheckBox.setText(_translate("VOXDialog", "Finish Beep"))

    def buttonbox_accepted(button):
        # print(dir(button.CFOspinBox))
        # cfo = int(button.CFOspinBox.cleanText())
        # button.config.set_value('CFO', cfo)
        return True

    def buttonbox_rejected(button):
        # print(dir(button))
        # print(button)
        return True

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    VOXDialog = QtWidgets.QDialog()
    ui = Ui_VOXDialog()
    ui.setupUi(VOXDialog)
    VOXDialog.show()
    sys.exit(app.exec())
