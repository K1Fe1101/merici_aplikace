from PyQt5 import  QtWidgets, QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sqlite3
from db import db

class UserForm(QtWidgets.QWidget):
	def __init__(self, window, **kwargs):
		super(UserForm, self).__init__(**kwargs)
		
		self.setWindowTitle("Nový uživatel")
		
		self.setFixedSize(300, 150)
        
		self.qvblUserForm = QtWidgets.QVBoxLayout()
		self.setLayout(self.qvblUserForm)

		self.window = window

		self.qvblLeftCol = QtWidgets.QVBoxLayout()
		self.qvblRightCol = QtWidgets.QVBoxLayout()


		self.lName = QtWidgets.QLabel("Jméno ")
		self.qvblLeftCol.addWidget(self.lName)
		self.eName = QtWidgets.QLineEdit()
		self.qvblRightCol.addWidget(self.eName)

		self.lSurname = QtWidgets.QLabel("Příjmení ")
		self.qvblLeftCol.addWidget(self.lSurname)
		self.eSurname = QtWidgets.QLineEdit()
		self.qvblRightCol.addWidget(self.eSurname)

		self.lAge = QtWidgets.QLabel("Věk ")
		self.qvblLeftCol.addWidget(self.lAge)
		self.eAge = QtWidgets.QLineEdit()
		self.qvblRightCol.addWidget(self.eAge)

		self.qhblUser = QtWidgets.QHBoxLayout()

		self.qhblUser.addLayout(self.qvblLeftCol)
		self.qhblUser.addLayout(self.qvblRightCol)

		self.qvblUserForm.addLayout(self.qhblUser)

		self.bNewUser = QtWidgets.QPushButton("Novy uzivatel")
		self.qvblUserForm.addWidget(self.bNewUser)
		self.bNewUser.clicked.connect(self.save_to_db)

		self.show()

	def save_to_db(self):

		sName = self.eName.text()
		print(sName)
		sSurname = self.eSurname.text()
		sAge = self.eAge.text()


		if sName != "" and sSurname != "" and sAge != "":
			try:
			
				iAge = int(sAge)

				if self.isFloat(sName) and self.isFloat(sSurname):

					db.insertToDB(sName, sSurname, sAge, self.window)

					self.window.fillUser(sName, sSurname, iAge)

					self.window.combo.setCurrentText(sName + " " + sSurname)

					self.close()


			except ValueError:
				self.showError("Vek musi byt cele cislo")

		else:
			self.showError("Vsechna pole musi byt vyplnena")

	def isFloat(self, text):
		count = 0
		for char in text:
			if char.isdigit():
				count = count + 1
		if count > 0:
			self.showError("Jmeno a prijmeni nesmi obsahovat cisla")
			return False

		else:
			return True

	def showError(self, message):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Critical)
		msg.setText(message)
		msg.setWindowTitle("Error")
		msg.exec_()
