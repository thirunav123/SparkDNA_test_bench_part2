from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QTimer,QBasicTimer
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (QMessageBox,QWidget,QApplication,QProgressBar,QPushButton,QDialog)
from PyQt5.QtGui import QIcon
import time
import serial
import sys
import csv

ser= serial.Serial(port="/dev/ttyUSB0",
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.EIGHTBITS,
        timeout=0.1)

RS232_check_time=5
RS485_check_time=5
LC_range_min=-32000
LC_range_max=32000
stability_check_time=10
Tolenrance=5
RW=754  #Reference weight in grams




rs232_rreq_AW = [ 1, 3, 0, 0]
rs232_rreq_LCC = [ 1, 3, 0, 1]
rs232_rreq_RW = [ 1, 3, 0, 16]
'''rs232_rreq_DOP1=[ 1, 3, 1, 14]
rs232_rreq_DOP2=[ 1, 3, 1, 15]
rs232_rreq_DOP3=[ 1, 3, 1, 16]
rs232_rreq_DOP4=[ 1, 3, 1, 17]'''
rs232_rreq_DIP1=[ 1, 3, 0, 250]
rs232_rreq_DIP2=[ 1, 3, 0, 251]
rs232_rreq_DIP3=[ 1, 3, 0, 252]

tcu_wreq_power_on_dut = [ 0, 6, 0, 14, 0, 1]
tcu_wreq_power_off_dut = [ 0, 6, 0, 14, 0, 0]
tcu_dop1_on = [ 0, 6, 0, 13, 0, 1]
tcu_dop2_on = [ 0, 6, 0, 12, 0, 1]
tcu_dop3_on = [ 0, 6, 0, 11, 0, 1]
tcu_dop1_off = [ 0, 6, 0, 13, 0, 0]
tcu_dop2_off = [ 0, 6, 0, 12, 0, 0]
tcu_dop3_off = [ 0, 6, 0, 11, 0, 0]
rs232_wreq_tare = [ 1, 6, 0, 25, 0, 1]
rs232_wreq_RW = [ 1, 6, 0, 16]
rs232_wreq_calibration = [ 1, 6, 0, 26, 0, 1]
'''rs232_wreq_DOP1_H=[ 1, 6, 1, 14, 0, 0]
rs232_wreq_DOP2_H=[ 1, 6, 1, 15, 0, 0]
rs232_wreq_DOP3_H=[ 1, 6, 1, 16, 0, 0]
rs232_wreq_DOP4_H=[ 1, 6, 1, 17, 0, 0]
rs232_wreq_DOP1_L=[ 1, 6, 1, 14, 0, 1]
rs232_wreq_DOP2_L=[ 1, 6, 1, 15, 0, 1]
rs232_wreq_DOP3_L=[ 1, 6, 1, 16, 0, 1]
rs232_wreq_DOP4_L=[ 1, 6, 1, 17, 0, 1]'''

RS232_rreq_AW = bytes(rs232_rreq_AW)
RS232_rreq_LCC = bytes(rs232_rreq_LCC)
RS232_rreq_RW = bytes(rs232_rreq_RW)
'''RS232_rreq_DOP1= bytes(rs232_rreq_DOP1)
RS232_rreq_DOP2= bytes(rs232_rreq_DOP2)
RS232_rreq_DOP3= bytes(rs232_rreq_DOP3)
RS232_rreq_DOP4= bytes(rs232_rreq_DOP4)'''
RS232_rreq_DIP1= bytes(rs232_rreq_DIP1)
RS232_rreq_DIP2= bytes(rs232_rreq_DIP2)
RS232_rreq_DIP3= bytes(rs232_rreq_DIP3)
RS232_wreq_tare = bytes(rs232_wreq_tare)
RS232_wreq_RW = bytes(rs232_wreq_RW)+(RW.to_bytes(2,"big"))
RS232_wreq_calibration = bytes(rs232_wreq_calibration)
'''RS232_wreq_DOP1_H= bytes(rs232_wreq_DOP1_H)
RS232_wreq_DOP2_H= bytes(rs232_wreq_DOP2_H)
RS232_wreq_DOP3_H= bytes(rs232_wreq_DOP3_H)
RS232_wreq_DOP4_H= bytes(rs232_wreq_DOP4_H)
RS232_wreq_DOP1_L= bytes(rs232_wreq_DOP1_L)
RS232_wreq_DOP2_L= bytes(rs232_wreq_DOP2_L)
RS232_wreq_DOP3_L= bytes(rs232_wreq_DOP3_L)
RS232_wreq_DOP4_L= bytes(rs232_wreq_DOP4_L)'''



rs485_rreq_AW = [ 2, 3, 0, 0]
rs485_rreq_LCC = [ 2, 3, 0, 1]
rs485_rreq_RW = [ 2, 3, 0, 16]
rs485_rreq_DOP1=[ 2, 3, 1, 14]
rs485_rreq_DOP2=[ 2, 3, 1, 15]
rs485_rreq_DOP3=[ 2, 3, 1, 16]
rs485_rreq_DOP4=[ 2, 3, 1, 17]
rs485_rreq_DIP1=[ 2, 3, 0, 250]
rs485_rreq_DIP2=[ 2, 3, 0, 251]
rs485_rreq_DIP3=[ 2, 3, 0, 252]

rs485_wreq_tare = [ 2, 6, 0, 25, 0, 1]
rs485_wreq_RW = [ 2, 6, 0, 16]
rs485_wreq_calibration = [ 2, 6, 0, 26, 0, 1]
rs485_wreq_DOP1_H=[ 2, 6, 1, 14, 0, 0]
rs485_wreq_DOP2_H=[ 2, 6, 1, 15, 0, 0]
rs485_wreq_DOP3_H=[ 2, 6, 1, 16, 0, 0]
rs485_wreq_DOP4_H=[ 2, 6, 1, 17, 0, 0]
rs485_wreq_DOP1_L=[ 2, 6, 1, 14, 0, 1]
rs485_wreq_DOP2_L=[ 2, 6, 1, 15, 0, 1]
rs485_wreq_DOP3_L=[ 2, 6, 1, 16, 0, 1]
rs485_wreq_DOP4_L=[ 2, 6, 1, 17, 0, 1]

RS485_rreq_AW = bytes(rs485_rreq_AW)
RS485_rreq_LCC = bytes(rs485_rreq_LCC)
RS485_rreq_RW = bytes(rs485_rreq_RW)
RS485_rreq_DOP1= bytes(rs485_rreq_DOP1)
RS485_rreq_DOP2= bytes(rs485_rreq_DOP2)
RS485_rreq_DOP3= bytes(rs485_rreq_DOP3)
RS485_rreq_DOP4= bytes(rs485_rreq_DOP4)
RS485_rreq_DIP1= bytes(rs485_rreq_DIP1)
RS485_rreq_DIP2= bytes(rs485_rreq_DIP2)
RS485_rreq_DIP3= bytes(rs485_rreq_DIP3)
TCU_wreq_power_on_DUT=bytes(tcu_wreq_power_on_dut)
TCU_wreq_power_off_DUT=bytes(tcu_wreq_power_off_dut)
TCU_DOP1_on=bytes(tcu_dop1_on)
TCU_DOP2_on=bytes(tcu_dop2_on)
TCU_DOP3_on=bytes(tcu_dop3_on)
TCU_DOP1_off=bytes(tcu_dop1_off)
TCU_DOP2_off=bytes(tcu_dop2_off)
TCU_DOP3_off=bytes(tcu_dop3_off)
RS485_wreq_tare = bytes(rs485_wreq_tare)
RS485_wreq_RW = bytes(rs485_wreq_RW)+(RW.to_bytes(2,"big"))
RS485_wreq_calibration = bytes(rs485_wreq_calibration)
RS485_wreq_DOP1_H= bytes(rs485_wreq_DOP1_H)
RS485_wreq_DOP2_H= bytes(rs485_wreq_DOP2_H)
RS485_wreq_DOP3_H= bytes(rs485_wreq_DOP3_H)
RS485_wreq_DOP4_H= bytes(rs485_wreq_DOP4_H)
RS485_wreq_DOP1_L= bytes(rs485_wreq_DOP1_L)
RS485_wreq_DOP2_L= bytes(rs485_wreq_DOP2_L)
RS485_wreq_DOP3_L= bytes(rs485_wreq_DOP3_L)
RS485_wreq_DOP4_L= bytes(rs485_wreq_DOP4_L)

#erTime_limit=100




a=0
X=0
data=0
rs_232_connection=0
rs_485_connection=0
state=0
q=0
serialno_of_DUT=""
index=0
old1=False
old2=False
old3=False
'''RS232_connection=""
RS485_connection=""
range_check=""
stability_check=""
LCC=""
DIP1_working=""
DIP2_working=""
DIP3_working=""'''


#secondpage1

def get_data_via_rs232(rd):
    global a
    global data
    if rd=="AW":
        ser.write(RS232_rreq_AW)
        for i in range(3):
            res=ser.read()
            a=int.from_bytes(res, byteorder='big',signed=True)
        res=ser.read(a)
        data=int.from_bytes(res,byteorder='big',signed=True)
        #print("rs232=",data)
        return data
    elif(rd=="LCC"):
        ser.write(RS232_rreq_LCC)
        for i in range(3):
            res=ser.read()
            a=int.from_bytes(res, byteorder='big',signed=True)
        res=ser.read(a)
        data=int.from_bytes(res,byteorder='big',signed=True)
        #print("rs232=",data)
        return data

def get_data_via_rs485(rd):
    global a
    global data
    if rd=="AW":
        ser.write(RS485_rreq_AW)
        for i in range(3):
            res=ser.read()
            a=int.from_bytes(res, byteorder='big',signed=True)
        res=ser.read(a)
        data=int.from_bytes(res,byteorder='big',signed=True)
        #print("rs232=",data)
        return data
    elif(rd=="LCC"):
        ser.write(RS485_rreq_LCC)
        for i in range(3):
            res=ser.read()
            a=int.from_bytes(res, byteorder='big',signed=True)
        res=ser.read(a)
        data=int.from_bytes(res,byteorder='big',signed=True)
        #print("rs232=",data)
        return data

def get_DIP_status(pinno):
    global a
    global data
    if(pinno==1):
        ser.write(RS232_rreq_DIP1)
        for i in range(3):
            res=ser.read()
            a=int.from_bytes(res, byteorder='big',signed=True)
        res=ser.read(a)
        data=int.from_bytes(res,byteorder='big',signed=True)
        #print("DIP1=",data)
    elif(pinno==2):
        ser.write(RS232_rreq_DIP2)
        for i in range(3):
            res=ser.read()
            a=int.from_bytes(res, byteorder='big',signed=True)
            #print(a)
        res=ser.read(a)
        data=int.from_bytes(res,byteorder='big',signed=True)
        #print("DIP2=",data)
    elif(pinno==3):
        ser.write(RS232_rreq_DIP3)
        for i in range(3):
            res=ser.read()
            a=int.from_bytes(res, byteorder='big',signed=True)
        res=ser.read(a)
        data=int.from_bytes(res,byteorder='big',signed=True)
        #print("DIP3=",data)
    else:
        
        data=0
        print("pin not found")
        
    return(data)

'''def DOP_H(pinno):
    global data
    if(pinno==1):
        ser.write(RS232_wreq_DOP1_H)
    elif(pinno==2):
        ser.write(RS232_wreq_DOP2_H)
    elif(pinno==3):
        ser.write(RS232_wreq_DOP3_H)
    elif(pinno==4):
        ser.write(RS232_wreq_DOP4_H)
    else:
        data=0
        print("pin not found")
        
def DOP_L(pinno):
    global data
    if(pinno==1):
        ser.write(RS232_wreq_DOP1_L)
    elif(pinno==2):
        ser.write(RS232_wreq_DOP2_L)
    elif(pinno==3):
        ser.write(RS232_wreq_DOP3_L)
    elif(pinno==4):
        ser.write(RS232_wreq_DOP4_L)
    else:
        data=0
        print("pin not found")
    return (data)

def get_DOP_status(pinno):
    global a
    global data
    if(pinno==1):
        ser.write(RS232_rreq_DOP1)
        for i in range(3):
            res=ser.read()
            a=int.from_bytes(res, byteorder='big',signed=True)
        res=ser.read(a)
        data=not((int.from_bytes(res,byteorder='big',signed=True)))
        print("DOP1=",data)
    elif(pinno==2):
        ser.write(RS232_rreq_DOP2)
        for i in range(3):
            res=ser.read()
            a=int.from_bytes(res, byteorder='big',signed=True)
        res=ser.read(a)
        data=not(int.from_bytes(res,byteorder='big',signed=True))
        print("DOP2=",data)
    elif(pinno==3):
        ser.write(RS232_rreq_DOP3)
        for i in range(3):
            res=ser.read()
            a=int.from_bytes(res, byteorder='big',signed=True)
            print(a)
        res=ser.read(a)
        data=not(int.from_bytes(res,byteorder='big',signed=True))
        print("DOP3=",data)
    elif(pinno==4):
        ser.write(RS232_rreq_DOP4)
        for i in range(3):
            res=ser.read()
            a=int.from_bytes(res, byteorder='big',signed=True)
            print(a)
        res=ser.read(a)
        data=not(int.from_bytes(res,byteorder='big',signed=True))
        print("DOP4=",data)
    else:
        data=0
        print("pin not found")
        
    return(data)'''


def rs232_progress_bar_count():
    RS232_CT=time.time()+RS232_check_time
    count=0
    while time.time() < RS232_CT:
        count = (RS232_check_time-(RS232_CT-time.time())//RS232_check_time)*100
        time.sleep(.01)
    return count

def power_on_DUT():
    ser.write(TCU_wreq_power_on_DUT)
    time.sleep(0.1)
    
def power_off_DUT():
    ser.write(TCU_wreq_power_off_DUT)
    time.sleep(0.1)

def power_on_TCU_DOP():
    ser.write(TCU_DOP1_on)
    time.sleep(0.1)
    ser.write(TCU_DOP2_on)
    time.sleep(0.1)
    ser.write(TCU_DOP3_on)
    time.sleep(0.1)

def power_off_TCU_DOP():
    ser.write(TCU_DOP1_off)
    time.sleep(0.1)
    ser.write(TCU_DOP2_off)
    time.sleep(0.1)
    ser.write(TCU_DOP3_off)
    time.sleep(0.1)


    
  

class firstDialog(QDialog):
    
    def __init__(self):
       #print("Firstpage")
        super(firstDialog,self).__init__()
        loadUi(r"/home/pi/Desktop/Loadcell_transmitter/GUI/UI-main/firstDialog.ui",self)#load the UI file 
        self.nextbutton.clicked.connect(self.secondpage)
        old1=True
        print("value=",get_data_via_rs232("LCC"))
               
    def secondpage(self):
        global old2
        global secondpage1
        if old2:
            widget.addWidget(secondpage1)
            widget.setCurrentIndex(widget.currentIndex()+1)
            #connect the next page
        else:
                
            global serialno_of_DUT
            serialno_of_DUT=self.serialnumber.text()  #value of serial number
           # self.serialnumber.clear()
            
            if serialno_of_DUT[:6]=='ECLC02':
                #if not 
                secondpage1=secondDialog(serialno_of_DUT)
                widget.addWidget(secondpage1)
                #print("Index",widget.currentIndex()+1)
                widget.setCurrentIndex(widget.currentIndex()+1)
                old2=True#open the next page  
                #print("success",serialno_of_DUT)
                print("Secondpage")
            elif(serialno_of_DUT!=""):
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
        loadUi(r"/home/pi/Desktop/Loadcell_transmitter/GUI/UI-main/secondDialog.ui",self) #loadui
        self.initUI()
        self.stablelabel=self.stablevaluelabel
        self.backbutton.clicked.connect(self.backfunction)#connect the back page function
        self.productlineEdit.setText(serialno)        
        self.runbutton.clicked.connect(self.onButtonClick)
        self.thirdnextbutton.clicked.connect(self.checking_connection)
        
        
    def checking_connection(self):
        if 1:#RS232_connection=="Done" and RS485_connection=="Done":
            self.thirdpage()
        else:
            if RS232_connection=="Not Done":
                mbox=QMessageBox()              #popup the message box widget
                mbox.setWindowTitle("Warning")  
                mbox.setText("oops...  \nRS232 connection not done")
                mbox.setIcon(QMessageBox.Warning)
                x=mbox.exec_()
            elif RS485_connection=="Not Done":
                mbox=QMessageBox()              #popup the message box widget
                mbox.setWindowTitle("Warning")  
                mbox.setText("oops...  \nRS485 connection not done")
                mbox.setIcon(QMessageBox.Warning)
                x=mbox.exec_()
        
    def thirdpage(self):
        global old3
        global thirdpage1
        if old3:
            widget.addWidget(thirdpage1)
            widget.setCurrentIndex(widget.currentIndex()+1)
            ser.write(RS232_wreq_tare)
            time.sleep(0.5)
            power_on_TCU_DOP()
            #connect the next page
        else:
            ser.write(RS232_wreq_tare)
            time.sleep(0.5)
            thirdpage1=thirdDialog()
            widget.addWidget(thirdpage1)
            #print("Index",widget.currentIndex()+1)
            widget.setCurrentIndex(widget.currentIndex()+1)
            old3=True
            print("Thirdpage")
            ser.write(RS232_wreq_RW)
            time.sleep(0.5)
            power_on_TCU_DOP()
        
    def oldNext3(self):
        widget.addWidget(thirdpage1)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def backfunction(self):
        #global index
       # backpage=firstDialog()
        #widget.addWidget(backpage)
        widget.addWidget(mainwindow)
       # print("Index",widget.currentIndex()-1)
        widget.setCurrentIndex(widget.currentIndex()+1)   #connect the first page
        print("Firstpage")
    
    def initUI(self):
       # self.show()
        self.rs232progressBar.setMaximum(100)  #maxmium limit of progress bar
        self.rs485progressBar.setMaximum(100)
        self.stabilityprogressBar.setMaximum(100)
        self.rs232progressBar.setValue(0)
        self.rs485progressBar.setValue(0)
        self.stabilityprogressBar.setValue(0)
        self.rs232progressBar.show()
        self.rs485progressBar.show()
        self.stabilityprogressBar.show()
        self.labelcompletestatus232=self.rs232complelabel   #object definition
        self.labelcompletestatus232.hide()       
        self.labelcompletestatus485=self.rs485complelabel
        self.labelcompletestatus485.hide()
        self.resvalue=self.resultlabel
        self.resvalue.setStyleSheet("background-color: ")
        self.stabilityresult=self.stablecomplelabel
        self.stabilityresult.hide()
        self.testprogress=self.testinprogresslabel
        self.testprogress.hide()
        
       

    def onButtonClick(self):
        global RS232_connection
        global RS485_connection
        self.initUI()
        power_on_DUT()
        #self.rs232progressBar.setValue(0)
        #self.__init__(serialno_of_DUT)
       # thirdDialog.pagetwo(self)
        #time.sleep(2)
        RS232_CT=time.time()+RS232_check_time
        count = 0
        while time.time() <= RS232_CT+0.05:
            count = int((RS232_check_time-(RS232_CT-time.time()))*100/RS232_check_time)
            print(count)
            get_data_via_rs232("LCC")
            if a!=0:
                count=100
                self.rs232progressBar.setValue(count)
                break
            else:   
                self.rs232progressBar.setValue(count)   #set the value to the progress bar
        if count>=99:
            self.rs232progressBar.hide()  #hide the progress bar
            self.labelcompletestatus232.setText("   Connection done  ")
            self.labelcompletestatus232.show()
            self.labelcompletestatus232.setStyleSheet("background-color: lightgreen")  #CHANGE the background
            RS232_connection="Done"
        else:
            self.rs232progressBar.hide()
            self.labelcompletestatus232.setText("            Not found  ")
            self.labelcompletestatus232.show()
            self.labelcompletestatus232.setStyleSheet("background-color: red")
            RS232_connection="Not Done"   
        RS485_CT=time.time()+RS485_check_time
        count = 0
        while time.time() <= RS485_CT+0.05:
            count =int((RS485_check_time-(RS485_CT-time.time()))*100/RS485_check_time)
            get_data_via_rs485("LCC")
            if a!= 0:
                count=100
                self.rs485progressBar.setValue(count)
                break
            else:   
                self.rs485progressBar.setValue(count)
      
        if count>=99:
            self.rs485progressBar.hide()
            self.labelcompletestatus485.show()
            self.labelcompletestatus485.setText("   Connection done  ")
            self.labelcompletestatus485.setStyleSheet("background-color: lightgreen")
            RS485_connection="Done"

        else:
            self.rs485progressBar.hide()
            self.labelcompletestatus485.show()
            self.labelcompletestatus485.setText("            Not found  ")
            self.labelcompletestatus485.setStyleSheet("background-color: red")
            RS485_connection="Not Done"
        self.maxminvalue()

    def maxminvalue(self):
        global range_check
        global stability_check
        global LCC
        if RS232_connection=="Done":
            loadvalue=get_data_via_rs232("LCC")
            
            if loadvalue > LC_range_min and LC_range_max >loadvalue:
                self.resvalue.setStyleSheet("background-color: lightgreen") 
                range_check="In Range"
            else:
                resvalue.setStyleSheet("background-color: red")
                range_check="Not In Range"
            stability_CT=time.time()+stability_check_time
            count = 0
            test_case=get_data_via_rs232("LCC")
            while time.time() <= stability_CT+0.05:
                count = int((stability_check_time-(stability_CT-time.time()))*100/stability_check_time)
                LCC=get_data_via_rs232("LCC")
                if (LCC>=(test_case-Tolenrance) and LCC<=(test_case+Tolenrance)):
                    self.stabilityprogressBar.setValue(count)
                    self.stablelabel.setText(str(LCC))
                    #print(count)
                else:
                    break
                
            if count>=99:
                self.stabilityprogressBar.hide()
                self.stablecomplelabel.show()
                self.stablecomplelabel.setStyleSheet("background-color: lightgreen") 
                stability_check="Stable"
            else:
                self.stabilityprogressBar.hide()
                self.stablecomplelabel.show()
                self.stablecomplelabel.setText("Not stable")
                self.stablecomplelabel.setStyleSheet("background-color: red")
                stability_check="Not Stable"
            diff=abs(get_data_via_rs232("LCC") - get_data_via_rs485("LCC"))
            if (diff<=Tolenrance):
                self.testprogress.show()   #show the text completed text
            else:
                self.testprogress.show()
                self.testprogress.setText("Data of RS232&RS485 not same")
        else:
            mbox=QMessageBox()              #popup the message box widget
            mbox.setWindowTitle("Warning")  
            mbox.setText("oops...  \nRS232 connection not done")
            mbox.setIcon(QMessageBox.Warning)
            x=mbox.exec_()

class thirdDialog(QDialog):
    def __init__(self):
        super(thirdDialog,self).__init__()
        loadUi(r"/home/pi/Desktop/Loadcell_transmitter/GUI/UI-main/thirddialog.ui",self) #loadui
        self.backbutton3.clicked.connect(self.pagetwo)
        self.savebutton.clicked.connect(self.savetofile)
        self.clickherebutton.clicked.connect(self.calibration)
        self.tarebutton.clicked.connect(self.tare)
        self.weightlabel1=self.weightlabel
        self.countlabel1=self.countlabel
        self.showweight()
        self.DIPlabel1=self.DIP1label
        self.DIPlabel2=self.DIP2label
        self.DIPlabel3=self.DIP3label
        '''self.DOPlabel1=self.DOP1label
        self.DOPlabel2=self.DOP2label
        self.DOPlabel3=self.DOP3label
        self.DOPlabel4=self.DOP4label'''
        self.calibratelabel1=self.calibratelabel
        #self.clickedbutton1=self.clickedbutton
        self.inputdevicestatus()
        self.qTimer = QTimer()
        # set interval to 1 s
        self.qTimer.setInterval(10) # 10 ms 
        # connect timeout signal to signal handler
        self.qTimer.timeout.connect(self.showweight)
        self.qTimer.timeout.connect(self.inputdevicestatus)
        self.qTimer.start()
        self.calibratelabel1.setText("To calibrate with Ref. weight of "+ str(RW) +"g")
        #self.status_DOP()
        #self.clickedbutton.clicked.connect(self.changeoutput)
        
    '''def start(self):
        self.DIPlabel1.setStyleSheet("background-color: ")
        self.DIPlabel2.setStyleSheet("background-color: ")
        self.DIPlabel3.setStyleSheet("background-color: ")
        self.DOPlabel1.setStyleSheet("background-color: ")
        self.DOPlabel2.setStyleSheet("background-color: ")
        self.DOPlabel3.setStyleSheet("background-color: ")
        self.DOPlabel4.setStyleSheet("background-color: ")'''

    '''def status_DOP(self):
        global state
        state=get_DOP_status(1)
        if get_DOP_status(1):
            self.DOPlabel1.setStyleSheet("background-color: lightgreen")
            DOP1_working="On"
        else:
            self.DOPlabel1.setStyleSheet("background-color: red")
            DOP1_working="Off"
        if get_DOP_status(2):
            self.DOPlabel2.setStyleSheet("background-color: lightgreen")
            DOP2_working="On"
        else:
            self.DOPlabel2.setStyleSheet("background-color: red")
            DOP2_working="Off"
        if get_DOP_status(3):
            self.DOPlabel3.setStyleSheet("background-color: lightgreen")
            DOP3_working="On"
        else:
            self.DOPlabel3.setStyleSheet("background-color: red") 
            DOP3_working="Off"
        if get_DOP_status(4):
            self.DOPlabel4.setStyleSheet("background-color: lightgreen")
            DOP4_working="On"
        else:
            self.DOPlabel4.setStyleSheet("background-color: red") 
            DOP4_working="Off"
        
    def changeoutput(self):
        global state
        if state==0:
            DOP_H(1)
            time.sleep(.1)
            DOP_H(2)
            time.sleep(.1)
            DOP_H(3)
            time.sleep(.1)
            DOP_H(4)
            time.sleep(.1)
            self.DOPlabel1.setStyleSheet("background-color: lightgreen")
            self.DOPlabel2.setStyleSheet("background-color: lightgreen")  
            self.DOPlabel3.setStyleSheet("background-color: lightgreen") 
            self.DOPlabel4.setStyleSheet("background-color: lightgreen")
            state=1
            DOP1_working="On"
            DOP2_working="On"
            DOP3_working="On"
            DOP4_working="On"
        else:
            DOP_L(1)
            time.sleep(.1)
            DOP_L(2)
            time.sleep(.1)
            DOP_L(3)
            time.sleep(.1)
            DOP_L(4)
            time.sleep(.1)
            self.DOPlabel1.setStyleSheet("background-color: red")
            self.DOPlabel2.setStyleSheet("background-color: red")  
            self.DOPlabel3.setStyleSheet("background-color: red") 
            self.DOPlabel4.setStyleSheet("background-color: red")
            state=0
            DOP1_working="Off"
            DOP2_working="Off"
            DOP3_working="Off"
            DOP4_working="Off"'''
    def tare(self):
        ser.write(RS232_wreq_tare)
        time.sleep(0.5)
        
    def pagetwo(self):
        #self.qTimer.stop()
        #backpage1=secondDialog(serialno_of_DUT)
        widget.addWidget(secondpage1)
        print("Secondpage")
        #print("Index",widget.currentIndex()-1)
        widget.setCurrentIndex(widget.currentIndex()+1)
        power_off_TCU_DOP()
        
        
    def showweight(self): #connect the first page
        global LCC
        self.weightlabel1.setText(str(get_data_via_rs232("AW"))+" g")
        LCC=get_data_via_rs232("LCC")
        self.countlabel1.setText(str(LCC))
        self.countlabel1.show()
        self.weightlabel1.show()
        
    def calibration(self):
        ser.write(RS232_wreq_calibration)
        time.sleep(0.5)
        
    def inputdevicestatus(self):
        global DIP1_working
        global DIP2_working
        global DIP3_working
        if get_DIP_status(1):   
            self.DIPlabel1.setStyleSheet("background-color: lightgreen")
            DIP1_working="On"
        else:
            self.DIPlabel1.setStyleSheet("background-color: red")
            DIP1_working="Off"
        if get_DIP_status(2):
            self.DIPlabel2.setStyleSheet("background-color: lightgreen")
            DIP2_working="On"
        else:
            self.DIPlabel2.setStyleSheet("background-color: red")
            DIP2_working="Off"
        if get_DIP_status(3):
            self.DIPlabel3.setStyleSheet("background-color: lightgreen")
            DIP3_working="On"
        else:
            self.DIPlabel3.setStyleSheet("background-color: red") 
            DIP3_working="Off"
            
    def savetofile(self):
        global old1,old2,old3
        global serialno_of_DUT,RS232_connection,RS485_connection
        global range_check,Stability_check,LCC,DIP1_working,DIP2_working,DIP3_working
        self.qTimer.stop()
        with open(r'/home/pi/Desktop/report.csv', 'a') as f:
           writer = csv.writer(f)
           writer.writerow([serialno_of_DUT,RS232_connection,RS485_connection,range_check,stability_check,LCC,DIP1_working,DIP2_working,DIP3_working])
        mbox=QMessageBox()              #popup the message box widget
        mbox.setWindowTitle("Success")
        mbox.setText("Below Data Saved to file\n   RS232 : "+RS232_connection+"\n   RS485 : "+RS485_connection+ "\n   Range : "+range_check+"\n   Stability : "+stability_check+"\n   LCC : "+str(LCC)+"\n   DIP1 : "+DIP1_working+"\n   DIP2 : "+DIP2_working+"\n   DIP3 : "+DIP3_working)
        mbox.setIcon(QMessageBox.Warning)
        x=mbox.exec_()
        #firstDialog.serialnumber.clear()
        #index=2
        #secondDialog.backfunction(self,index)
        #index=1
        old1=False
        old2=False
        old3=False
        RS232_connection=""
        RS485_connection=""
        range_check=""
        Stability_check=""
        DIP1_working=""
        DIP2_working=""
        DIP3_working=""
        '''DOP1_working=""
        DOP2_working=""
        DOP3_working=""
        DOP4_working=""'''
        
        currentpage=firstDialog()
        widget.addWidget(currentpage)
        #print("Index",widget.currentIndex()+1)
        widget.setCurrentIndex(widget.currentIndex()+1)
        #self.showweight()'''
        power_off_DUT()
        power_off_TCU_DOP()
        
        print("Firstpage")

app=QApplication(sys.argv)
mainwindow=firstDialog()
#get_data_via_rs232()
# secondpage=secondDialog()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setWindowTitle("Spark Drives And Automation")
widget.setWindowIcon(QIcon(r'C:\Users\MAHA RAJA\Desktop\Qt design\icon.png'))
widget.showMaximized()
#widget.setFixedWidth(800)
#widget.setFixedHeight(480)
widget.show()
app.exec_()

