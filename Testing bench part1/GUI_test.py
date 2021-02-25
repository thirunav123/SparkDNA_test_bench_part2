from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QTimer,QBasicTimer
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (QMessageBox,QWidget,QApplication,QProgressBar,QPushButton,QDialog)
from PyQt5.QtGui import QIcon
import time
import serial
import sys

Time_limit=100




class firstdialog(QDialog):
    def __init__(self):
        super(firstdialog,self).__init__()
        loadUi(r"/home/pi/Desktop/Testing bench/GUI/UI-main/firstDialog.ui",self)#load the UI file 
        self.nextbutton.clicked.connect(self.nextpage) #connect the next page
       
        

    def nextpage(self):
       
        self.serialnumber=self.serialnumber.text()  #value of serial number
        if self.serialnumber!="":                   #if not 
            nextpage=secondDialog()
            widget.addWidget(nextpage)
            widget.setCurrentIndex(widget.currentIndex()+1)    #open the next page  

            print("success",self.serialnumber)
        else:
            mbox=QMessageBox()              #popup the message box widget
            mbox.setWindowTitle("Warning")  
            mbox.setText("oops...  \nEnter a serial number")
            mbox.setIcon(QMessageBox.Warning)

            x=mbox.exec_()
    
   
       
        
      
class secondDialog(QDialog):
    def __init__(self):
        super(secondDialog,self).__init__()
        loadUi(r"/home/pi/Desktop/Testing bench/GUI/UI-main/secondDialog.ui",self) #loadui
        self.backbutton.clicked.connect(self.backfunction)   #connect the back page function
        self.initUI()      
        
    

       
    def backfunction(self):
   
        backpage=firstdialog()
        widget.addWidget(backpage)
        widget.setCurrentIndex(widget.currentIndex()+1)   #connect the first page
        print("firstpage")

   
    
    def initUI(self):

        
        
      
        self. rs232progressBar.setMaximum(100)  #maxmium limit of progress bar
        self.rs485progressBar.setMaximum(100)
        
        
        self.show()
        self.labelcompletestatus232=self.rs232complelabel   #object definition
        self.labelcompletestatus232.hide()       #hide the progress bar
        self.labelcompletestatus485=self.rs485complelabel
        self.labelcompletestatus485.hide()
        
        stabilityresult=self.stablecomplelabel
        self.stablecomplelabel.hide()
        self.testprogress=self.testinprogresslabel
        self.testprogress.hide()


        self.runbutton.clicked.connect(self.onButtonClick)

    def onButtonClick(self):
        
        count = 0
        while count < Time_limit:
            count += 1
            time.sleep(.01)
            self.rs232progressBar.setValue(count) #set the value to the progress bar
        if count==100:
            self.rs232progressBar.hide()
            self.labelcompletestatus232.show()
            self.labelcompletestatus232.setStyleSheet("background-color: lightgreen")  #CHANGE the background
        else:
            self.labelcompletestatus232.setStyleSheet("background-color: red")
        
        if count==100:
            counts=0
            while counts < Time_limit:
                counts +=1
                time.sleep(.01)
                self.rs485progressBar.setValue(counts)
            if counts==100:
                self.rs485progressBar.hide()
                self.labelcompletestatus485.show()
                self.labelcompletestatus485.setStyleSheet("background-color: lightgreen") 
            else:
                self.labelcompletestatus485.setStyleSheet("background-color: red")
        self.maxminvalue()

    def maxminvalue(self):


        maxvalue=1000   #set the text in the max box
        minvalue=11000
        loadvalue=1220
        resvalue=self.resultlabel
        if loadvalue > int(minvalue) and int(maxvalue)>loadvalue:
           resvalue.setStyleSheet("background-color: lightgreen") 
        else:
           resvalue.setStyleSheet("background-color: red")

 
        stable=0
        
        while stable < Time_limit:
            stable  += 1
            time.sleep(.01)
            self.stabilityprogressBar.setValue(stable)
        if stable==100 :
            self.stabilityprogressBar.hide()
            self.stablecomplelabel.show()
            self.stablecomplelabel.setStyleSheet("background-color: lightgreen") 
           
        else:
            self.stablecomplelabel.setStyleSheet("background-color: red")
        
        self.testprogress.show()   #show the text completed text
       
    
            
       

    
    
       
      
      
      
            
        
           








app=QApplication(sys.argv)
mainwindow=firstdialog()

# secondpage=secondDialog()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setWindowTitle("Spark Drives And Automation")
widget.setWindowIcon(QIcon(r'C:\Users\MAHA RAJA\Desktop\Qt design\icon.png'))

widget.setFixedWidth(800)
widget.setFixedHeight(480)
widget.show()
app.exec_()
