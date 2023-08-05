from msilib.schema import Property
from tokenize import String
from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import QEasingCurve, QMessageLogContext, QPoint, QPropertyAnimation, QSequentialAnimationGroup, QSize, Qt

class ValueSelectorWidget(QtWidgets.QWidget):

    def __init__(self,color="blue",bgcolor="white", text="boton", color2="blue",bgcolor2 ="white",text2="boton2", animWidgColor = "black", height=100, width=100):       

        super().__init__()
    
        self.animWidgColor = animWidgColor
        
        self.b1color = color
        self.b2color = color2

        self.b1bgcolor = bgcolor
        self.b2bgcolor = bgcolor2

        self.b1text = text
        self.b2text = text2

        self.boton = QtWidgets.QPushButton(self)
        self.boton2 = QtWidgets.QPushButton(self)

        self.animWidget = QtWidgets.QWidget(self)
        self.animWidget.setStyleSheet("background-color:"+self.animWidgColor)
        self.animWidget.setGeometry(0,0,height,width)


        self.boton.setStyleSheet("color:"+color)
        self.boton.setGeometry(0,0,height,width)
        self.boton.setText(text)

        self.boton2.setStyleSheet("color:"+color2)
        self.boton2.setGeometry(width*1.5,0,height,width)
        self.boton2.setText(text2)

        self.selectedValue = self.boton2.text()
        print(self.selectedValue)

        self.anim1 = QPropertyAnimation(self.animWidget, b"pos")
        self.anim1.setEndValue(QPoint (0, 0))
        self.anim1.setDuration(80)

        self.anim2 = QPropertyAnimation(self.animWidget, b"pos")
        self.anim2.setEndValue(QPoint(height*1.5, 0))
        self.anim2.setDuration(80)

        self.anim_group = QSequentialAnimationGroup()
        self.anim_group.addAnimation(self.anim1)
        
        self.anim_group2 = QSequentialAnimationGroup()
        self.anim_group2.addAnimation(self.anim2)

        self.boton.clicked.connect(self.animation)

        self.boton2.clicked.connect(self.animation2)

        self.selectedVal = self.boton2.text()

        colorB1Text = property(String,self.setBoton1TextColor, self.getBoton1TextColor)
        colorB2Text = property(String,self.setBoton2TextColor, self.getBoton2TextColor)

        colorB1Background = property(String,self.setBoton1BackgroundColor, self.getBoton1BackgroundColor)
        colorB2Background = property(String,self.setBoton2BackgroundColor, self.getBoton2BackgroundColor) 

        textoB1 = property(String,self.setBoton1Text,self.getBoton1Text)
        textoB2 = property(String,self.setBoton2Text,self.getBoton2Text)

        animWidgBackground = property(String,self.setAnimWidgetBackgroundColor,self.getAnimWidgetBackgroundColor)

    def animation(self):
        self.anim_group.start()
        self.selectedVal = self.boton2.text()
        coords = self.animWidget.geometry().getCoords()
        print(coords)
    
    def animation2(self):
        self.anim_group2.start()
        self.selectedVal = self.boton.text()
        coords = self.animWidget.geometry().getCoords()
        print(coords)
        
    def setBoton1TextColor(self,color):
        self.boton.setStyleSheet("color:"+color)
        self.b1color = color
    
    def setBoton2TextColor(self,color):
        self.boton2.setStyleSheet("color:"+color)
        self.b2color = color

    def setBoton1BackgroundColor(self,color):
        self.boton.setStyleSheet("background-color:"+color)
        self.b1bgcolor = color

    def setBoton2BackgroundColor(self,color):
        self.boton.setStyleSheet("background-color:"+color)
        self.b2bgcolor = color

    def setBoton1Text(self,texto):
        self.boton.setText(texto)

    def setBoton2Text(self, texto):
        self.boton2.setText(texto)

    def setAnimWidgetBackgroundColor(self,color):
        self.animWidget.setStyleSheet("background-color:"+color)
        self.animWidgColor = color

    def getBoton1TextColor(self):
        return self.b1color

    def getBoton2TextColor(self):
        return self.b2color

    def getBoton1BackgroundColor(self):
        return self.b1bgcolor

    def getBoton2BackgroundColor(self):
        return self.b2bgcolor

    def getBoton1Text(self):
        return self.boton.text()

    def getBoton2Text(self):
        return self.boton2.text()

    def getAnimWidgetBackgroundColor(self):
        return self.animWidgColor