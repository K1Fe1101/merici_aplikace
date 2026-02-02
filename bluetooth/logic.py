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
		self.timer = QTimer()
		self.timer.setInterval(500)
		self.window = window
		try:
			self.ser = serial.Serial(port='COM9', baudrate=9600, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_TWO, bytesize=serial.SEVENBITS, timeout=0)
		except serial.SerialException:
            self.msg = QMessageBox()
			self.msg.setText("Nelze připojit bluetooth.")
			self.msg.show()
            return
		


	def read_data(self):
		
		try:
			if self.ser.in_waiting == 0:
                return

			self.i = self.i + 1
			line = self.ser.readline().decode('ascii').strip()
      			
			if not line:
				return
			voltage = float(line)

	
			self.window.sMeasuredVal.setText(str(voltage) + " V")
			self.voltage = float(voltage)
			self.window.ydata.append(self.voltage)
			self.window.xdata.append(self.i)
			
			self.window.line1.set_xdata(self.window.xdata)
			self.window.line1.set_ydata(self.window.ydata)
			
			self.window.canvas.draw()
			self.window.figure.canvas.flush_events()
		except:
			self.pause()
			self.msg = QMessageBox()
			self.msg.setText("Nepripojeno.")
			self.msg.show()
			
	def connect(self):
		self.timer.timeout.connect(self.read_data)
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
			
		try:	
			dialog = QFileDialog()
			self.folder_path = dialog.getExistingDirectory(None, "Zvolte slozku")
			self.folder_path = self.folder_path + '/cisla.xlsx'
			print(self.folder_path)
			
			zapis = pd.DataFrame(list(zip(self.window.xdata, self.window.ydata)), columns=['x', 'y'])	

			
			with pd.ExcelWriter(self.folder_path, mode= 'w', engine='xlsxwriter') as writer:
				zapis.to_excel(writer, sheet_name='Sheet1', index=False)
				
		except:
			self.msg = QMessageBox()
			self.msg.setText("Zápis se nezdařil")
			self.msg.setStandardButtons(QMessageBox.Ok)
			self.msg.show()
