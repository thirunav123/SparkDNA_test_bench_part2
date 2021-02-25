from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QTimer,QBasicTimer
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (QMessageBox,QWidget,QApplication,QProgressBar,QPushButton,QDialog)
from PyQt5.QtGui import QIcon
import time
import serial
import sys
import serial
import time

ser= serial.Serial(port="/dev/ttyS0",
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.EIGHTBITS,
        timeout=0.1)


rs232_rreq=[1, 3, 0, 1]
rs485_rreq=[2, 3, 0, 1]
rs232_wreq=[1, 6, 0, 1]
rs485_wreq=[2, 6, 0, 1]
RS232_rreq = bytes(rs232_rreq)
RS485_rreq = bytes(rs485_rreq)
RS232_wreq = bytes(rs232_wreq)
RS485_wreq = bytes(rs485_wreq)

RS232_check_time=5
RS485_check_time=5
LC_range_min=-35000
LC_range_max=-30000
stability_check_time=10
Tolenrance=5
#erTime_limit=100

def get_data_via_rs232():
    ser.write(RS232_rreq)
    for i in range(3):
        res=ser.read()
        a=int.from_bytes(res, byteorder='big',signed=True)
    res=ser.read(a)
    rs232_data=int.from_bytes(res,byteorder='big',signed=True)
    print("rs232=",rs232_data)
    return(rs232_data)

def get_data_via_rs485():
    ser.write(RS485_rreq)
    for i in range(3):
        res=ser.read()
        a=int.from_bytes(res, byteorder='big',signed=True)
    res=ser.read(a)
    rs485_data=int.from_bytes(res,byteorder='big',signed=True)
    print("rs485=",rs485_data)
    return(rs485_data)


def rs232_progress_bar_count():
        RS232_CT=time.time()+RS232_check_time
        count=0
        while time.time() < RS232_CT:
            count = (RS232_check_time-(RS232_CT-time.time())//RS232_check_time)*100
            time.sleep(.01)
        return count


class firstdialog(QDialog):
    def __init__(self):
        super(firstdialog,self).__init__()
        loadUi(r"/home/pi/Desktop/Testing bench part1/GUI/UI-main/firstDialog.ui",self)#load the UI file 
        self.nextbutton.clicked.connect(self.nextpage) #connect the next page
               
    def nextpage(self):
        self.serialnumber1=self.serialnumber.text()  #value of serial number
        
        if self.serialnumber1[:3]=='ECL':                   #if not 
            nextpage=secondDialog(self.serialnumber1)
            widget.addWidget(nextpage)
            widget.setCurrentIndex(widget.currentIndex()+1)    #open the next page  
            print("success",self.serialnumber1)
        elif(self.serialnumber1!=""):
            mbox=QMessageBox()              #popup the message box widget
            mbox.setWindowTitle("Warning")  
            mbox.setText("oops...  \nEnter a valid format")
            mbox.setIcon(QMessageBox.Warning)
            x=mbox.exec_()
        else:
            mbox=QMessageBox()              #popup the message box widget
            mbox.setWindowTitle("Warning")  
            mbox.setText("oops...  \nEnter a serial number")
            mbox.setIcon(QMessageBox.Warning)
            x=mbox.exec_()
            
      
class secondDialog(QDialog):
    def __init__(self,serialno):
        super(secondDialog,self).__init__()
        loadUi(r"/home/pi/Desktop/Testing bench part1/GUI/UI-main/secondDialog.ui",self) #loadui
        self.backbutton.clicked.connect(self.backfunction)#connect the back page function
        self.productlineEdit.setText(serialno)
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
        RS232_CT=time.time()+RS232_check_time
        count = 0
        while time.time() <= RS232_CT+0.05:
            count = int((RS232_check_time-(RS232_CT-time.time()))*100/RS232_check_time)
            print(count)
            if get_data_via_rs232()!=0:
                count=100
                self.rs232progressBar.setValue(count)
                break
            else:   
                self.rs232progressBar.setValue(count)#set the value to the progress bar
        if count>=100:
            self.rs232progressBar.hide()
            self.labelcompletestatus232.show()
            self.labelcompletestatus232.setStyleSheet("background-color: lightgreen")  #CHANGE the background
        else:
            self.rs232progressBar.hide()
            self.labelcompletestatus232.show()
            self.labelcompletestatus232.setText("            Not found  ")
            self.labelcompletestatus232.setStyleSheet("background-color: red")
            
        RS485_CT=time.time()+RS485_check_time
        count = 0
        while time.time() <= RS485_CT+0.05:
            count =int((RS485_check_time-(RS485_CT-time.time()))*100/RS485_check_time)
            if get_data_via_rs485()!= 0:
                count=100
                self.rs485progressBar.setValue(count)
                break
            else:   
                self.rs485progressBar.setValue(count)
      
        if count>=99:
            self.rs485progressBar.hide()
            self.labelcompletestatus485.show()
            self.labelcompletestatus485.setStyleSheet("background-color: lightgreen") 
        else:
            self.rs485progressBar.hide()
            self.labelcompletestatus485.show()
            self.labelcompletestatus485.setText("            Not found  ")
            self.labelcompletestatus485.setStyleSheet("background-color: red")
        self.maxminvalue()

    def maxminvalue(self):
        loadvalue=get_data_via_rs232()
        resvalue=self.resultlabel
        if loadvalue > LC_range_min and LC_range_max >loadvalue:
           resvalue.setStyleSheet("background-color: lightgreen") 
        else:
           resvalue.setStyleSheet("background-color: red")
            
        stability_CT=time.time()+stability_check_time
        count = 0
        test_case=get_data_via_rs232()
        while time.time() <= stability_CT+0.05:
            count = int((stability_check_time-(stability_CT-time.time()))*100/stability_check_time)
            if (get_data_via_rs232()>=(test_case-Tolenrance) and get_data_via_rs232()<=(test_case+Tolenrance)):
                self.stabilityprogressBar.setValue(count)
                #print(count)
            else:
               break
            
        if count>=100:
            self.stabilityprogressBar.hide()
            self.stablecomplelabel.show()
            self.stablecomplelabel.setStyleSheet("background-color: lightgreen") 
           
        else:
            self.stabilityprogressBar.hide()
            self.stablecomplelabel.show()
            self.stablecomplelabel.setText("Not stable")
            self.stablecomplelabel.setStyleSheet("background-color: red")
        diff=abs(get_data_via_rs232() - get_data_via_rs485())
        if (diff<=Tolenrance):
            self.testprogress.show()   #show the text completed text
        else:
            self.testprogress.show()
            self.testprogress.setText("Data of RS232&RS485 not same")

class thirddialog(QDialog):
    def __init__(self):
        super(thirddialog,self).__init__()
        loadUi(r"/home/pi/Desktop/Testing bench part1/GUI/UI-main/thirddialog.ui",self) #loadui
        self.backbutton3.clicked.connect(self.pagetwo) 
        self.clickherebutton.clicked.connect(self.samepage) 
        self.valuelabel1=self.valuelabel
        
       

    def pagetwo(self):
   
        backpage=firstdialog()
        widget.addWidget(backpage)
        widget.setCurrentIndex(widget.currentIndex()+1)   #connect the first page
        self.valuelabel1.setText("hi")
    def samepage(self):
        currentpage=thirddialog()
       
        widget.setCurrentIndex(widget.currentIndex())
        print("samepage")

app=QApplication(sys.argv)
mainwindow=firstdialog()
#get_data_via_rs232()
# secondpage=secondDialog()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setWindowTitle("Spark Drives And Automation")
widget.setWindowIcon(QIcon(r'C:\Users\MAHA RAJA\Desktop\Qt design\icon.png'))
widget.setFixedWidth(800)
widget.setFixedHeight(480)
widget.show()
app.exec_()

