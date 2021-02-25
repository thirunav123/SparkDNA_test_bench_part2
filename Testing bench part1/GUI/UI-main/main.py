


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QTimer,QBasicTimer
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (QMessageBox,QWidget,QApplication,QProgressBar,QPushButton,QDialog)
from PyQt5.QtGui import  QIcon
import time
import serial
import sys

Time_limit=100




class firstdialog(QDialog):
    def __init__(self):
        super(firstdialog,self).__init__()
        loadUi(r"C:\Users\MAHA RAJA\Desktop\Qt design\firstDialog.ui",self)#load the UI file 
        self.nextbutton.clicked.connect(self.nextpage) #connect the next page
       
        

    def nextpage(self):
       
        serialnumber1=self.serialnumber  #value of serial number
        self.serialnumber=serialnumber1.text()
        if self.serialnumber=='ECL':                   #if not 
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
        loadUi(r"C:\Users\MAHA RAJA\Desktop\Qt design\secondDialog.ui",self) #loadui
        self.backbutton.clicked.connect(self.backfunction)   #connect the back page function
        # a=str(serial_no)
        # self.productlineEdit.setText(a)
        
        self.initUI()  
        self.thirdnextbutton.clicked.connect(self.thirdpage)

        
    
    def thirdpage(self):
        thirdpage=thirddialog()
        widget.addWidget(thirdpage)
        widget.setCurrentIndex(widget.currentIndex()+1)
       
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
       
        
        self.runbutton.clicked.connect(self.onButtonrecheck)
    
    def onButtonrecheck(self):
       
        currentpage=secondDialog()
        widget.addWidget(currentpage)
        widget.setCurrentIndex(widget.currentIndex())
       
        
        # self.productlineEdit.setText(a)
        
            
class thirddialog(QDialog):
    def __init__(self):
        super(thirddialog,self).__init__()
        loadUi(r"C:\Users\MAHA RAJA\Desktop\Qt design\thirddialog.ui",self) #loadui
        self.backbutton3.clicked.connect(self.pagetwo) 
        self.clickherebutton.clicked.connect(self.samepage) 
        self.valuelabel1=self.valuelabel
        self.DIPlabel1=self.DIP1label
        self.DIPlabel2=self.DIP2label
        self.DIPlabel3=self.DIP3label
        self.DOPlabel1=self.DOP1label
        self.DOPlabel2=self.DOP2label
        self.DOPlabel3=self.DOP3label
        self.DOPlabel4=self.DOP4label
        self.calibratelabel1=self.calibratelabel
        self.clickedbutton1=self.clickedbutton
        self.inputdevicestatus()
        
      

        self.clickedbutton.clicked.connect(self.outputdevicestatus)
    def outputdevicestatus(self):
       
        self.DOPlabel1.setStyleSheet("background-color: lightgreen")
        self.DOPlabel2.setStyleSheet("background-color: lightgreen")  
        self.DOPlabel3.setStyleSheet("background-color: lightgreen") 
        self.DOPlabel4.setStyleSheet("background-color: lightgreen")
       
        
       

    def pagetwo(self):
   
        backpage=firstdialog()
        widget.addWidget(backpage)
        widget.setCurrentIndex(widget.currentIndex()+1)   #connect the first page
        self.valuelabel1.setText("hi")
    def samepage(self):
        currentpage=thirddialog()
       
        widget.setCurrentIndex(widget.currentIndex())
        print("samepage")
       
    def inputdevicestatus(self):
        self.DIPlabel1.setStyleSheet("background-color: lightgreen") 
        self.DIPlabel2.setStyleSheet("background-color: lightgreen") 
        self.DIPlabel3.setStyleSheet("background-color: lightgreen") 
        a="calibrated value"
        self.calibratelabel1.setText(a + " hi")   
        
     
   
      
      
            
        
           








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

