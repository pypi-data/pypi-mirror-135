
from PySide6.QtCore import Property, QEasingCurve, QObject, QPoint, QPropertyAnimation, QSequentialAnimationGroup, QSize
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
import sys

class AnimatedButton(QWidget):
    def __init__(self, width, height):
        super().__init__()
        self._color = "white"
        self._text = "Button"
        self.rec = QWidget(self)
        self.rec.setStyleSheet("background-color:"+self._color)
        self.rec.setGeometry(0,0,height,width+10)

        self.button = QPushButton(self)
        self.button.setGeometry(0,0,height,width)
        self.button.setText(self._text)

        self.anim = QPropertyAnimation(self.rec, b"size")
        self.anim.setEndValue(QSize(height, width))
        self.anim.setDuration(80)

        self.anim1 = QPropertyAnimation(self.rec, b"size")
        self.anim1.setEndValue(QSize(height, width+10))
        self.anim1.setDuration(80)

        self.anim_group = QSequentialAnimationGroup()
        self.anim_group.addAnimation(self.anim)
        self.anim_group.addAnimation(self.anim1)
        

        self.button.clicked.connect(self.animation)

    def getColor(self):
        return self._color

    def setColor(self, color):
        self._color = color
        self.rec.setStyleSheet("background-color:"+color)    

    color = Property(str, getColor, setColor)

    def getText(self):
        return self._text

    def setText(self, text):
        self._text = text
        self.button.setText(text)

    text = Property(str, getText, setText)

    def animation(self):
        self.anim_group.start()


    

        
