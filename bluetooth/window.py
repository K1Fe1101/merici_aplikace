from PyQt5 import  QtWidgets, QtGui, QtCore
import pandas as pd
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time
import traceback, sys, os, random
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#import smbus
import serial
import struct
from db import db
from logic import Logic
from UserForm import UserForm




class Window(QtWidgets.QWidget):
    def __init__(self, db: db, **kwargs):
        super(Window, self).__init__(**kwargs)
        self.setWindowTitle("Měřicí aplikace")
        self.graph()
        self.setFixedSize(1300, 900)
        self.qvblWindowForm = QtWidgets.QVBoxLayout()
        self.setLayout(self.qvblWindowForm)
        
        self.qhblUser = QtWidgets.QHBoxLayout()
        
        self.lName = QtWidgets.QLabel("Jméno:")
        self.lNameValue = QtWidgets.QLabel(" ")
        self.lSurname = QtWidgets.QLabel("Příjmení:")
        self.lSurnameValue = QtWidgets.QLabel(" ")
        self.lAge = QtWidgets.QLabel("Věk:")
        self.lAgeValue = QtWidgets.QLabel(" ")
        
        self.qvlUserCol1 = QtWidgets.QVBoxLayout()
        self.qvlUserCol2 = QtWidgets.QVBoxLayout()
        self.qvlUserCol3 = QtWidgets.QVBoxLayout()
        
        self.combo = QComboBox()
        self.populateCombo(0)
        self.combo.activated.connect(self.selectFromCombo)
        self.user_button = QtWidgets.QPushButton("Nový uživatel")
        

        
        for x in (self.lName, self.lSurname, self.lAge):
            x.setFont(QFont('Arial', 15))
            self.qvlUserCol1.addWidget(x)
            
        for x in (self.lNameValue, self.lSurnameValue, self.lAgeValue):
            x.setFont(QFont('Arial', 15))
            self.qvlUserCol2.addWidget(x)
            
        for x in (self.combo, self.user_button):
            x.setFont(QFont('Arial', 15))
            self.qvlUserCol3.addWidget(x)
            
        for x in (self.qvlUserCol1, self.qvlUserCol2, self.qvlUserCol3):
            self.qhblUser.addLayout(x)
            
        
        self.qhblMeasurement = QtWidgets.QVBoxLayout()

        self.qvblMeasurementRow1 = QtWidgets.QHBoxLayout()
        self.qvblMeasurementRow2 = QtWidgets.QHBoxLayout()
        

        self.sMeasured = QtWidgets.QLabel("Měřená hodnota:")
        self.sMeasuredVal = QtWidgets.QLabel(" "  + "V")
        
        for x in (self.sMeasured, self.sMeasuredVal):
            x.setFont(QFont('Arial', 15))
            self.qvblMeasurementRow1.addWidget(x)

        
        self.qvblMeasurementRow2.addWidget(self.canvas)

        for x in (self.qvblMeasurementRow1, self.qvblMeasurementRow2):
            self.qhblMeasurement.addLayout(x)

        
        self.qvblButtons = QtWidgets.QVBoxLayout()

        self.connect_button = QtWidgets.QPushButton("Měřit")
        self.pause_button = QtWidgets.QPushButton("Pozastavit")
        self.toexcel_button = QtWidgets.QPushButton("Zapsat do excelu")
        self.delete_button = QtWidgets.QPushButton("Vymazat")

        self.qhblButtonsCol1 = QtWidgets.QHBoxLayout()
        self.qhblButtonsCol2 = QtWidgets.QHBoxLayout()

        for x in (self.connect_button, self.pause_button):
            x.setFont(QFont('Arial', 15))
            self.qhblButtonsCol1.addWidget(x)
        
        for x in (self.toexcel_button, self.delete_button):
            x.setFont(QFont('Arial', 15))
            self.qhblButtonsCol2.addWidget(x)

        for x in (self.qhblButtonsCol1, self.qhblButtonsCol2):
            self.qvblButtons.addLayout(x)
        
        self.qvblWindowForm.addLayout(self.qhblUser)
        self.qvblWindowForm.addLayout(self.qhblMeasurement)
        self.qvblWindowForm.addLayout(self.qvblButtons)
        
        buttons = [self.connect_button, self.pause_button, self.toexcel_button, self.delete_button, self.user_button]
        methods = [self.connect, self.pause, self.toexcel, self.delete, self.newUser]
        for button, method in zip(buttons,methods):
            button.clicked.connect(method)


        self.logic = Logic(self)



        self.show()

    def graph(self):
        self.ydata = []
        self.xdata = []
        self.min_x = 0
        self.max_x = 100
        self.min_y = 0
        self.max_y = 100
        
        self.figure = Figure(figsize = (7, 6), dpi = 100)
        self.ax = self.figure.add_subplot(1, 1, 1)
        self.line1, = self.ax.plot([], [])
        self.ax.set_xlim(self.min_x, self.max_x)
        self.ax.set_ylim(self.min_y, self.max_y)
        self.ax.set_title("Průběh signálu")
        self.ax.grid()
        self.ax.set_xlabel("Čas [ms]", fontsize=12)
        self.ax.set_ylabel("Napětí [V]", fontsize=12)
        self.canvas = FigureCanvas(self.figure)


    def connect(self):
        self.logic.connect()

    
    def pause(self):
        self.logic.pause()
        
    def toexcel(self):
        self.logic.toexcel()

    def delete(self):
        self.logic.delete()

    def newUser(self):
        self.ufNewUser = UserForm(self)
        self.ufNewUser.show()
        
    def populateCombo(self, newUser):
        rows = db.selectNames(self, newUser)
        for row in rows:
            sFullName = str(row[1]) + " " + str(row[2])
            self.combo.addItem(sFullName)
            
    def fillUser(self, name, surname, age):
        self.lNameValue.setText(name)
        self.lSurnameValue.setText(surname)
        self.lAgeValue.setText(str(age))
    
    def selectFromCombo(self):
        sText = str(self.combo.currentIndex())
        iID = int(sText) #
        sID = str(iID)
        
        user = db.findUser(self, sID)
        print(user)
        
        self.fillUser(str(user[0][0]), str(user[0][1]), str(user[0][2]))

