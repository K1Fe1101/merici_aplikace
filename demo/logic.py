from PyQt5 import  QtWidgets, QtGui, QtCore
import pandas as pd
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time
import traceback, sys, os, random
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import serial
import struct
import window

class Logic():
	
	def __init__(self, window):

		self.i = 0
		self.ii = 0
		self.timer = QTimer()
		self.timer.setInterval(500)
		self.window = window


	def read_excel(self):
		
		try:
			
			self.i = self.i + 1
			self.ii = self.ii + 1
			
			dataframe1 = pd.read_excel('/media/katka/Data/kacena/pythonprojekt/final_demo/vstup.xlsx')
				
			self.data = dataframe1['hodnoty'][self.ii]  
	
			self.window.sMeasuredVal.setText(str(self.data))
	
			self.window.ydata.append(self.data)
			self.window.xdata.append(self.i)

			self.window.line1.set_xdata(self.window.xdata)
			self.window.line1.set_ydata(self.window.ydata)
			
			self.window.canvas.draw()
			self.window.figure.canvas.flush_events()

	
			if self.ii >= 71:
				self.ii = -1
				
		except:
			self.pause()
			self.msg = QMessageBox()
			self.msg.setText("Excel neexistuje")
			self.msg.show()
			
	def connect(self):
		self.timer.timeout.connect(self.read_excel)
		self.timer.start()
		
	def pause(self):
		self.timer.stop()
		
	def delete(self):
		self.timer.stop()		
		self.window.canvas.close()
		self.i = 0
		self.ii = 0
		self.window.graph()
		self.window.qvblMeasurementRow2.addWidget(self.window.canvas)
		self.window.sMeasuredVal.setText(' ' + " V")
		
	def toexcel(self):  
	
		if self.timer.isActive:
			self.timer.stop()
			
		#try:	
			dialog = QFileDialog()
			self.folder_path = dialog.getExistingDirectory(None, "Zvolte slozku")
			self.folder_path = self.folder_path + '/cisla.xlsx'
			print(self.folder_path)
			
			zapis = pd.DataFrame(list(zip(self.window.xdata, self.window.ydata)), columns=['x', 'y'])	

			print("1")
			
			with pd.ExcelWriter(self.folder_path, mode= 'w', engine='xlsxwriter') as writer:
				zapis.to_excel(writer, sheet_name='Sheet1', index=False)
			print("2")
				
		#except:
		#	self.msg = QMessageBox()
		#	self.msg.setText("Nezvolena cesta pro ulozeni excelu")
		#	self.msg.setStandardButtons(QMessageBox.Ok)
		#	self.msg.show()
