from PyQt5.QtWidgets import QLineEdit, QLabel
from PyQt5.QtCore import pyqtSignal, Qt

class ClickableLineEdit(QLineEdit):
    clicked = pyqtSignal() # signal when the text entry is left clicked

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton: self.clicked.emit()
        else: super().mousePressEvent(event)

class ClickableLabel(QLabel):
    clicked = pyqtSignal() # signal when the label is left clicked

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton: self.clicked.emit()
        else: super().mousePressEvent(event)
