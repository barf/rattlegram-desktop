#!/usr/bin/env python3
#
# Rattlegram Desktop
# Copyright 2025 
# Stuart MacIntosh ZL3TUX <stuart@macintosh.nz>
#

from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.resize(348, 210)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=AboutDialog)
        self.buttonBox.setGeometry(QtCore.QRect(130, 170, 81, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Close)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(parent=AboutDialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 331, 41))
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=AboutDialog)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 331, 91))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(AboutDialog)
        self.buttonBox.accepted.connect(AboutDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(AboutDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        _translate = QtCore.QCoreApplication.translate
        AboutDialog.setWindowTitle(_translate("AboutDialog", "About"))
        self.label.setText(_translate("AboutDialog", "<html><head/><body><p><span style=\" font-size:22pt; font-weight:600;\">Rattlegram Desktop</span></p></body></html>"))
        self.label_2.setText(_translate("AboutDialog", "<html><head/><body><p>Created by Stuart MacIntosh ZL3TUX<br/>Copyright 2025<br/>Includes Rattlegram COFDM modem by Ahmet Inan<br/>0BSD License<br/><a href=\"https://github.com/aicodix/rattlegram\"><span style=\" text-decoration: underline; color:#0000ff;\">https://github.com/aicodix/rattlegram</span></a></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AboutDialog = QtWidgets.QDialog()
    ui = Ui_AboutDialog()
    ui.setupUi(AboutDialog)
    AboutDialog.show()
    sys.exit(app.exec())
