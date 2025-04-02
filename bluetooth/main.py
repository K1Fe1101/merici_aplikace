from PyQt5 import  QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from window import Window
import logic
import traceback, sys, os, random
from db import db

class App(QtWidgets.QApplication):
	def __init__(self):
		super(App, self).__init__(sys.argv)
		
	def builder(self):
		self.db = db()
		self.window = Window(self.db)
		sys.exit(self.exec())
		
apka = App()
apka.builder()
